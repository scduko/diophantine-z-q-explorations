"""Small fail-closed bindings for the release planner and reproduction runner."""
if not __debug__:
    raise RuntimeError('Assertions required')
import ast,gzip,hashlib,json,re
from pathlib import Path,PurePosixPath

PIPELINE_SHA='7654b06f450db87a3181dd5e16fe23949cb4e57d22751aef3681fed80a1fcf26'
CANDIDATE=('source-residuals.jsonl.gz','certificate.jsonl.gz','candidate-rows.json.gz',
           'residuals.json.gz','variable-map.json','weights.json','polynomial.expanded.txt','polynomial.expanded.txt.gz')
SELECTION_KEYS={'format','source_pipeline_manifest_sha256','source_entry_sha256','source_archive_sha256',
    'base_checker_sha256','final_checker_sha256','final_certificate_sha256','final_expansion_sha256',
    'arithmetic_review_sha256','cleanup_manifest_sha256'}
COUNT_KEYS=('variables','witnesses','rows','degree','monomials','max_abs_coefficient','expanded_bytes','compressed_bytes')
MAX_JSON=32*1024**2

def need(value,message):
    if not value:raise ValueError(message)
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def load(path):
    need(path.stat().st_size<=MAX_JSON,'JSON byte limit')
    return json.loads(path.read_bytes())
def save(path,obj):
    path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def pin(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}',value),'Full lowercase SHA-256 required')
    return value
def child(root,name):
    need(type(name) is str and bool(name) and '\\' not in name and ':' not in name,'Invalid relative path')
    parts=PurePosixPath(name)
    need(not parts.is_absolute() and all(p not in ('','.','..') for p in name.split('/')),'Invalid relative path')
    path=root.joinpath(*parts.parts)
    need(root.resolve() in path.resolve().parents,'Path escapes input root')
    need(all(not p.is_symlink() for p in (path,*path.parents) if p==root or root in p.parents),'Symlink in input path')
    return path
def selection(obj):
    need(type(obj) is dict and set(obj)==SELECTION_KEYS,'Selection keys differ')
    need(obj['format']=='quartic-release-selection/v1','Selection format')
    for k,v in obj.items():
        if k=='format' or k=='cleanup_manifest_sha256' and v is None:continue
        pin(v)
    need(obj['source_pipeline_manifest_sha256']==PIPELINE_SHA,'Unreviewed source family')
    if obj['final_checker_sha256']!=obj['base_checker_sha256']:
        need(obj['cleanup_manifest_sha256'] is not None,'Final checker extension requires cleanup packet')
    return obj
def registry(path):
    need(path.stat().st_size<=MAX_JSON,'Checker byte limit')
    code=path.read_text(encoding='utf-8');nodes=[n for n in ast.parse(code).body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name) and t.id=='SOURCE_ENTRIES' for t in n.targets)]
    need(len(nodes)==1,'Expected one source registry')
    node=nodes[0]
    need(len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='SOURCE_ENTRIES','Registry target')
    span=''.join(code.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
    need(span.strip()==ast.get_source_segment(code,node),'Registry has neighboring statements')
    return ast.literal_eval(node.value)
def inspect_registry(path,entry):
    values=registry(path)
    need(set(values)=={'original64',entry['source_id']},'Unexpected registry entry set')
    need(values[entry['source_id']]==entry,'Selected source registry differs')
    need(values['original64']==dict(source_sha256='6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2',source_variables=15672,source_rows=15107),'Historical registry differs')
def first_record(path):
    with gzip.open(path,'rb') as f:line=f.readline(MAX_JSON+1)
    need(len(line)<=MAX_JSON and line.endswith(b'\n'),'Certificate first record limit')
    return json.loads(line)
def inspect_certificate(path,entry,entry_sha):
    first=first_record(path)
    need(first.get('source_id')==entry['source_id'],'Certificate source id')
    need(first.get('source_entry_sha256')==entry_sha,'Certificate entry pin')
def manifest_files(root,obj):
    files=obj['files'];need(type(files) is dict and files,'Empty manifest')
    seen=set()
    for name,item in files.items():
        need(name.casefold() not in seen,'Case-alias destination');seen.add(name.casefold())
        path=child(root,name)
        need(path.is_file() and path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],'Manifest file differs: '+name)
def report_counts(report):
    need(report.get('status')=='PASS','Unverified final report')
    out={k:report[k] for k in COUNT_KEYS}
    need(all(type(v) is int and v>0 for v in out.values()),'Report count types')
    need(out['variables']==out['witnesses']+1,'Input coordinate count')
    need(out['degree']==4 and out['max_abs_coefficient']<2**80,'Quartic coefficient bound')
    need(out['variables']<5000,'Release threshold not met')
    return out

def expected_report(report,entry,s):
    result=report_counts(report)
    values=dict(source_id=entry['source_id'],source_sha256=s['source_archive_sha256'],
        checker_sha256=s['final_checker_sha256'],certificate_sha256=s['final_certificate_sha256'],
        expanded_sha256=s['final_expansion_sha256'])
    need(all(report.get(k)==v for k,v in values.items()),'Final report identity differs')
    return dict(result,**values)
