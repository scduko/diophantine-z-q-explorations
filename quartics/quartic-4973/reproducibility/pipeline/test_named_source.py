"""Negative tests of generated source-name and source-byte binding.

Only AssertionError at the specified checker source line earns a rejection.
Timeouts, unrelated exceptions, missing files, and resource aborts fail.
"""
import argparse, gzip, hashlib, importlib.util, json, linecache, subprocess, sys, tempfile, traceback
from pathlib import Path

CASES={
 'unknown_source_id':'assert source_id in SOURCE_ENTRIES',
 'wrong_source_entry_digest':"first['source_entry_sha256']",
 'changed_source_header':"==entry['source_header']",
 'changed_source_body':"==entry['uncompressed_sha256']",
 'changed_source_gzip_bytes':'==SOURCE_SHA',
}
def digest(data):return hashlib.sha256(data).hexdigest()
def child(checker,fixture,expected):
    spec=importlib.util.spec_from_file_location('named_source_negative_checker',checker)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    try:module.verify(fixture,write_report=False)
    except AssertionError as exc:
        frames=traceback.extract_tb(exc.__traceback__)
        hit=[x for x in frames if Path(x.filename).resolve()==checker.resolve() and expected in (x.line or linecache.getline(x.filename,x.lineno))]
        if hit:
            print(json.dumps({'status':'EXPECTED SEMANTIC REJECTION','line':hit[-1].lineno,'assertion':hit[-1].line}));return
        raise RuntimeError('Assertion was at an unexpected checker location') from exc
    raise RuntimeError('Malformed source was accepted')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adapter',type=Path);p.add_argument('--candidate',type=Path)
    p.add_argument('--report',type=Path);p.add_argument('--seconds',type=int,default=180)
    p.add_argument('--child',action='store_true');p.add_argument('--checker',type=Path)
    p.add_argument('--fixture',type=Path);p.add_argument('--expect')
    a=p.parse_args()
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions must be enabled')
    if a.child:child(a.checker,a.fixture,a.expect);return
    assert a.adapter and a.candidate and a.report and 1<=a.seconds<=600
    checker=(a.adapter/'verify_named_source.py').resolve()
    manifest=json.loads((a.adapter/'adapter-manifest.json').read_bytes())
    assert digest(checker.read_bytes())==manifest['generated_sha256']['verify_named_source.py']
    cert_bytes=(a.candidate/'certificate.jsonl.gz').read_bytes()
    source_bytes=(a.candidate/'source-residuals.jsonl.gz').read_bytes()
    assert len(cert_bytes)<50_000_000 and len(source_bytes)<50_000_000
    cert=gzip.decompress(cert_bytes);source=gzip.decompress(source_bytes)
    assert len(cert)<150_000_000 and len(source)<150_000_000
    first,*remaining=cert.splitlines();initial=json.loads(first)
    entry=json.loads((a.adapter/'source-entry.json').read_bytes())
    assert initial['source_id']==entry['source_id']==manifest['source_id']
    cases=[]
    with tempfile.TemporaryDirectory(prefix='quartic-named-source-') as temp:
        fixture=Path(temp)
        for name,expected in CASES.items():
            cb,sb=cert_bytes,source_bytes
            if name.startswith('unknown') or name=='wrong_source_entry_digest':
                record=dict(initial)
                if name=='unknown_source_id':record['source_id']='unregistered-source'
                else:record['source_entry_sha256']='0'*64
                cb=gzip.compress(json.dumps(record,sort_keys=True,separators=(',',':')).encode()+b'\n'+b'\n'.join(remaining)+b'\n',mtime=0)
            elif name=='changed_source_header':
                header,*body=source.splitlines();header=json.loads(header);header['witnesses']+=1
                sb=gzip.compress(json.dumps(header).encode()+b'\n'+b'\n'.join(body)+b'\n',mtime=0)
            elif name=='changed_source_body':sb=gzip.compress(source+b'\n',mtime=0)
            elif name=='changed_source_gzip_bytes':sb=gzip.compress(source,compresslevel=1,mtime=1)
            (fixture/'certificate.jsonl.gz').write_bytes(cb)
            (fixture/'source-residuals.jsonl.gz').write_bytes(sb)
            cmd=[sys.executable,'-E','-B',str(Path(__file__).resolve()),'--child','--checker',str(checker),'--fixture',str(fixture),'--expect',expected]
            proc=subprocess.run(cmd,capture_output=True,text=True,timeout=a.seconds)
            if proc.returncode!=0:raise RuntimeError(name+' failed:\n'+proc.stdout+proc.stderr)
            outcome=json.loads(proc.stdout.strip());assert outcome['status']=='EXPECTED SEMANTIC REJECTION'
            cases.append({'case':name,**outcome})
    result={'status':'PASS','source_id':entry['source_id'],'checker_sha256':digest(checker.read_bytes()),'cases':cases,
            'scope':'Five source-name/byte binding mutations; full rule mutation coverage remains inherited from the exact pinned rule tests.'}
    a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
