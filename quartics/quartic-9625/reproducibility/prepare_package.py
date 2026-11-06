"""Apply a hash-bound release copy plan into a fresh package directory."""
if not __debug__:raise RuntimeError('Assertions required')
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def child(root,name):
    p=PurePosixPath(name)
    assert not p.is_absolute() and '\\' not in name and ':' not in name
    assert all(x not in ('','.','..') for x in p.parts)
    result=root.joinpath(*p.parts).resolve();assert root in result.parents
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,required=True);p.add_argument('--input',action='append',default=[])
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    plan=json.loads(a.plan.read_bytes());assert plan['format']=='quartic-release-copy-plan/v2'
    roots={}
    for item in a.input:
        key,value=item.split('=',1);assert key not in roots;roots[key]=Path(value).resolve()
    assert set(roots)=={x['input'] for x in plan['files']}
    out=a.output.resolve();assert not out.exists(),'Output must be fresh'
    checked=[];names=set()
    for item in plan['files']:
        source=child(roots[item['input']],item['source']);destination=child(out,item['destination'])
        name=item['destination'].casefold();assert name not in names;names.add(name)
        assert source.is_file() and source.stat().st_size==item['bytes'] and sha(source)==item['sha256']
        checked.append((source,destination,item))
    assert 'reproducibility/manifest.json' not in names
    assert 'reproducibility/copy-plan.json' not in names
    out.mkdir(parents=True)
    for source,destination,item in checked:
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,destination)
        assert sha(destination)==item['sha256']
    shutil.copyfile(a.plan,out/'reproducibility/copy-plan.json')
    files={x['destination']:{k:x[k] for k in ('sha256','bytes')} for x in plan['files']}
    files['reproducibility/copy-plan.json']=dict(sha256=sha(a.plan),bytes=a.plan.stat().st_size)
    manifest=dict(format='quartic-release-reproducibility/v2',expected=plan['expected'],recipe=plan['recipe'],
                  source_arithmetic_acceptance=False,files=files)
    path=out/'reproducibility/manifest.json'
    path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='PACKAGED; fresh reproduction still required',files=len(files),manifest_sha256=sha(path))))

if __name__=='__main__':main()
