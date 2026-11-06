"""Freeze an explicit copy plan for one verified source-pipeline endpoint.

Reads and hashes files only. Never generates or expands a polynomial.
"""
if not __debug__: raise RuntimeError('Assertions required')
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath

CANDIDATE=('source-residuals.jsonl.gz','certificate.jsonl.gz','candidate-rows.json.gz',
           'residuals.json.gz','variable-map.json','weights.json','polynomial.expanded.txt',
           'polynomial.expanded.txt.gz')
RUNTIME=('run.py','prepare_package.py','plan_package.py','README.md')

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def read(path):return json.loads(path.read_bytes())

def checked(root,name):
    rel=PurePosixPath(name)
    assert not rel.is_absolute() and '\\' not in name and ':' not in name
    assert all(p not in ('','.','..') for p in rel.parts)
    result=root.joinpath(*rel.parts).resolve()
    assert root in result.parents and result.is_file(),name
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('artifact','packet','repository','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args(); runtime=Path(__file__).resolve().parent
    roots={key:getattr(a,key).resolve() for key in ('artifact','packet','repository')};roots['runtime']=runtime
    summary=read(roots['artifact']/'SUMMARY.json');packet=read(roots['packet']/'manifest.json')
    assert summary['status']=='ALGEBRAIC CANDIDATE VERIFIED'
    assert sha(roots['packet']/'manifest.json')==summary['manifest_sha256']
    assert summary['endpoint']=='stages/coordinates'
    endpoint=roots['artifact']/'stages/coordinates';report=read(endpoint/'verification.json')
    entry=read(roots['artifact']/'adapter/source-entry.json')
    assert report['status']=='PASS' and report['source_id']==entry['source_id']
    assert summary['verification_sha256']==sha(endpoint/'verification.json')
    assert report['variables']==report['witnesses']+1
    assert report['degree']==4 and report['max_abs_coefficient']<2**80
    assert sha(endpoint/'source-residuals.jsonl.gz')==report['source_sha256']==entry['source_sha256']
    assert sha(endpoint/'certificate.jsonl.gz')==report['certificate_sha256']
    assert sha(endpoint/'polynomial.expanded.txt')==report['expanded_sha256']
    assert sha(roots['artifact']/'adapter/verify_named_source.py')==report['checker_sha256']
    checker_ast=ast.parse((roots['artifact']/'adapter/verify_named_source.py').read_text())
    registries=[n for n in checker_ast.body if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id=='SOURCE_ENTRIES' for t in n.targets)]
    assert len(registries)==1 and ast.literal_eval(registries[0].value)[entry['source_id']]==entry
    assert sha(roots['artifact']/'adapter/source-layout.json')==entry['source_layout_sha256']
    assert sha(roots['packet']/'check_source.py')==entry['source_audit_checker_sha256']
    assert len(packet['external_inputs'])==13,'Review changed external dependency set explicitly'
    rows=[]; destinations=set()
    def add(family,source,destination,pin=None,size=None):
        path=checked(roots[family],source); digest=sha(path); length=path.stat().st_size
        assert pin is None or digest==pin,(family,source)
        assert size is None or length==size,(family,source)
        key=destination.casefold();assert key not in destinations,destination;destinations.add(key)
        rows.append(dict(input=family,source=source,destination=destination,sha256=digest,bytes=length))
    for name in CANDIDATE:add('artifact','stages/coordinates/'+name,name)
    add('artifact','adapter/verify_named_source.py','verify_certificate.py',report['checker_sha256'])
    for name in ('source-entry.json','source-audit.json','construction-map.json','source-layout.json'):
        add('artifact','adapter/'+name,name)
    assert sha(roots['artifact']/'adapter/source-audit.json')==entry['source_audit_sha256']
    assert sha(roots['artifact']/'adapter/construction-map.json')==entry['construction_map_sha256']
    for name,pin in entry['inspected_files_sha256'].items():add('artifact','source/'+name,'source/'+name,pin)
    for name,record in packet['files'].items():
        add('packet',name,'reproducibility/pipeline/'+name,record['sha256'],record['bytes'])
    add('packet','manifest.json','reproducibility/pipeline/manifest.json',summary['manifest_sha256'])
    for item in packet['external_inputs']:
        add('repository',item['path'],'reproducibility/external-repository/'+item['path'],item['sha256'])
    adapter_manifest=read(roots['artifact']/'adapter/adapter-manifest.json')
    assert adapter_manifest['source_id']==entry['source_id']
    add('artifact','adapter/adapter-manifest.json','reproducibility/frozen-adapter-manifest.json')
    for name,pin in adapter_manifest['generated_sha256'].items():
        if name=='verify_named_source.py':assert pin==report['checker_sha256'];continue
        assert name.startswith('tools/')
        add('artifact','adapter/'+name,'reproducibility/frozen-'+name,pin)
    for name in ('SUMMARY.json','RUN_INPUTS.json','source-mutations.json','named-source-mutations.json',
                 'source-determinism.json'):
        add('artifact',name,'evidence/original-run/'+name)
    for stage in ('fresh-lift','norms','charts','ordinates','parity','batch','optimized','coordinates'):
        add('artifact','stages/'+stage+'/verification.json','evidence/stages/'+stage+'.json')
    add('artifact','stages/SUMMARY.json','evidence/original-run/stages.json')
    for name in RUNTIME:add('runtime',name,'reproducibility/'+name)
    expected={key:report[key] for key in ('source_id','source_sha256','variables','witnesses','rows','monomials',
        'degree','max_abs_coefficient','expanded_bytes','compressed_bytes','expanded_sha256','certificate_sha256','checker_sha256')}
    available=set(packet['files'])
    mutation='test_mode_source.py' if 'test_mode_source.py' in available else 'test_source.py'
    assert mutation in available
    recipe=dict(source_mutation_script=mutation,source_mutation_has_core=(mutation=='test_mode_source.py'),
                jacobi_locator=('test_jacobi_locators.py' in available),external_inputs=13,
                source_entry_sha256=sha(roots['artifact']/'adapter/source-entry.json'),
                packet_manifest_sha256=summary['manifest_sha256'],
                expected_source_mutations=read(roots['artifact']/'source-mutations.json'),
                expected_named_mutations=read(roots['artifact']/'named-source-mutations.json'))
    plan=dict(format='quartic-release-copy-plan/v2',expected=expected,recipe=recipe,files=rows,
              source_arithmetic_acceptance=False,
              scope='Explicit finite reproduction package; mathematical acceptance remains separate')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    assert not a.output.exists(),'Plan output must be fresh'
    a.output.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='COPY PLAN FROZEN; no computation performed',files=len(rows),
                         bytes=sum(r['bytes'] for r in rows),source_id=entry['source_id'],plan_sha256=sha(a.output))))

if __name__=='__main__':main()
