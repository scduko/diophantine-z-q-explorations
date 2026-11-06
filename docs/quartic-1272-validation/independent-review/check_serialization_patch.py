"""Compare the portability patch with the previously accepted Git snapshot."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / 'repository'
PACKAGE = REPO / 'quartics/quartic-1272'
BASELINE = '81de7e45d60d458414ea0f96eb0f68ad8981a3a3'
OLD_MANIFEST = '37a5d9d0e4d1d9f51562a1ba4a004827ad5bc7c0fbdf3a7d74f031e9ddc933e3'

def old_bytes(relative):
    return subprocess.check_output(['git', 'show', BASELINE+':quartics/quartic-1272/'+relative], cwd=REPO)
def digest(data): return sha256(data).hexdigest()

class RemoveSerializationOnly(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        writer = isinstance(node.func, ast.Attribute) and node.func.attr == 'write_text'
        helper = isinstance(node.func, ast.Name) and node.func.id == 'write_json'
        if writer or helper:
            kept = []
            for kw in node.keywords:
                if writer and kw.arg == 'encoding':
                    assert isinstance(kw.value, ast.Constant) and kw.value.value == 'utf-8'
                elif kw.arg == 'newline':
                    assert ((isinstance(kw.value, ast.Constant) and kw.value.value in ('\n','\r\n'))
                            or (writer and isinstance(kw.value, ast.Name) and kw.value.id == 'newline'))
                else: kept.append(kw)
            node.keywords = kept
        return node
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.name == 'write_json':
            pairs = list(zip(node.args.kwonlyargs,node.args.kw_defaults))
            kept = []
            for arg, default in pairs:
                if arg.arg == 'newline':
                    assert isinstance(default, ast.Constant) and default.value == '\n'
                else: kept.append((arg,default))
            node.args.kwonlyargs = [p[0] for p in kept]
            node.args.kw_defaults = [p[1] for p in kept]
        return node

def normalized_ast(data):
    return ast.dump(RemoveSerializationOnly().visit(ast.parse(data)),include_attributes=False)

def changed_paths(a,b,path=''):
    if type(a) is not type(b): return [path]
    if isinstance(a,dict):
        paths = [path+'/'+key for key in a.keys() ^ b.keys()]
        for key in a.keys() & b.keys(): paths += changed_paths(a[key],b[key],path+'/'+key)
        return paths
    if isinstance(a,list):
        if len(a) != len(b): return [path+'[length]']
        return sum((changed_paths(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
    return [] if a == b else [path]

def allowed_metadata_change(file,path):
    if file == 'PROVENANCE.json':
        return (path in ('/changes','/serialization') or
                (path.startswith('/copiedSourceFiles/') and path.endswith(('/packagedSha256','/byteIdentical'))))
    return (path.endswith(('/checkedAtUTC','/testedAtUTC','/generated_utc','/elapsedSeconds','/wallSeconds','/sha256'))
            or path.startswith('/artifacts/') or path in ('/inputSha256/compiled','/inputSha256/trace'))

def main():
    old_manifest = old_bytes('MANIFEST.json')
    assert digest(old_manifest) == OLD_MANIFEST
    math_code = ['compiler/compile_ir.py', 'identity/check_identity.py',
                 'optimization/find_affine_dependencies.py', 'optimization/verify_optimization.py',
                 'oracle/check_oracle.py', 'source-review/build_inventory.py',
                 'source-review/check_builder_semantics.py']
    code_checks = []
    for relative in math_code:
        before, after = old_bytes(relative), (PACKAGE/relative).read_bytes()
        assert normalized_ast(before) == normalized_ast(after), relative
        code_checks.append({'path':relative,'oldSha256':digest(before),'newSha256':digest(after),
                            'status':'AST_IDENTICAL_EXCEPT_EXPLICIT_UTF8_AND_NEWLINES'})
    core = ['builder/raw-ir.json','builder/raw-translated-ir.json','source-review/source_inventory.json']
    core += ['compiler/'+stage+'/'+name for stage in ('direct','translated')
             for name in ('compiled-ir.json','reduction-certificate.json','coordinate-map.json',
                          'polynomial.json','specialization-certificate.json')]
    core_checks = []
    for relative in core:
        before, after = old_bytes(relative), (PACKAGE/relative).read_bytes()
        assert json.loads(before) == json.loads(after), relative
        if relative.endswith('polynomial.json'): assert before == after, relative
        core_checks.append({'path':relative,'jsonIdentical':True,'byteIdentical':before==after,
                            'oldSha256':digest(before),'newSha256':digest(after)})
    for relative in ('builder/build_source.cjs','checker/checker.cjs','checker/run_all.cjs'):
        # A missing historical name is an error, rather than silently skipping it.
        assert old_bytes(relative) == (PACKAGE/relative).read_bytes(), relative
    assert old_bytes('polynomial.json') == (PACKAGE/'polynomial.json').read_bytes()
    old_entries = json.loads(old_manifest)['files']
    new_entries = json.loads((PACKAGE/'MANIFEST.json').read_bytes())['files']
    assert {e['path'] for e in old_entries} == {e['path'] for e in new_entries}
    metadata_changes = []
    changed_files = []
    manual_files = {'integrity.py','reproduce.py','README.md'}
    for entry in old_entries:
        relative = entry['path']
        before,after = old_bytes(relative),(PACKAGE/relative).read_bytes()
        if before == after: continue
        changed_files.append(relative)
        if relative.endswith('.json'):
            differences = sorted(changed_paths(json.loads(before),json.loads(after)))
            assert all(allowed_metadata_change(relative,p) for p in differences), (relative,differences)
            if differences: metadata_changes.append({'path':relative,'changedFields':differences})
        else:
            assert relative in set(math_code) | manual_files, relative
    provenance = json.loads((PACKAGE/'PROVENANCE.json').read_bytes())['serialization']
    for relative in provenance['lfFiles']:
        data=(PACKAGE/relative).read_bytes()
        data.decode('utf-8')
        assert data.endswith(b'\n') and b'\r' not in data, relative
    for relative in provenance['publishedCrlfTables']:
        data=(PACKAGE/relative).read_bytes()
        rest=data.replace(b'\r\n',b'')
        assert data.endswith(b'\r\n') and b'\r' not in rest and b'\n' not in rest, relative
    result = {'status':'PASS_SERIALIZATION_PATCH',
              'scope':'Independent AST comparison of mathematical Python modules and exact parsed-data comparison of all core artifacts against the previously accepted Git snapshot. Integrity/replay policy reviewed separately.',
              'baselineCommit':BASELINE,'baselineManifestSha256':OLD_MANIFEST,
              'currentManifestSha256':digest((PACKAGE/'MANIFEST.json').read_bytes()),
              'mathematicalModules':code_checks,'coreArtifacts':core_checks,
              'changedFiles':changed_files,'nonCoreMetadataChanges':metadata_changes,
              'explicitLineEndingsChecked':True,
              'polynomialBytesUnchanged':True}
    (HERE/'serialization-patch-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'],'baselineCommit':BASELINE,
                      'currentManifestSha256':result['currentManifestSha256'],
                      'mathematicalModules':len(code_checks),'coreArtifacts':len(core_checks),
                      'polynomialBytesUnchanged':True},indent=2))

if __name__ == '__main__': main()
