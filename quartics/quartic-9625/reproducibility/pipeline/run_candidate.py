"""Root-dispatched bounded Linux trial of the selective-beta source."""
import argparse,hashlib,json,os,platform,signal,subprocess,sys,time,zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def main():
    if not __debug__ or sys.flags.optimize:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=['exploratory'],required=True)
    p.add_argument('--stage-seconds',type=int,default=180);p.add_argument('--source-only',action='store_true');a=p.parse_args()
    assert os.name=='posix','Use only the root bounded Linux worker';assert 1<=a.stage_seconds<=600
    repo=a.repo.resolve();out=a.output.resolve();assert not out.exists()
    manifest=load(HERE/'manifest.json')
    for name,record in manifest['files'].items():
        path=(HERE/name).resolve();assert path.is_relative_to(HERE)
        assert path.stat().st_size==record['bytes'] and sha(path)==record['sha256'],name
    for record in manifest['external_inputs']:assert sha(repo/record['path'])==record['sha256'],record['path']
    out.mkdir(parents=True);start=time.monotonic();steps=[];complete=False;endpoint=None
    inputs={'manifest_sha256':sha(HERE/'manifest.json'),'arithmetic_acceptance':False,'mode':a.mode,
            'python':sys.version,'platform':platform.platform(),'zlib':zlib.ZLIB_RUNTIME_VERSION}
    save(out/'RUN_INPUTS.json',inputs)
    def run(name,script,*args,multiplier=1):
        cmd=[sys.executable,'-E','-B',str(script),*map(str,args)];before=time.monotonic();log=out/(name+'.log')
        print(json.dumps({'stage':name,'command':cmd}),flush=True)
        with log.open('w',encoding='utf-8') as stream:
            proc=subprocess.Popen(cmd,cwd=repo,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            try:code=proc.wait(timeout=a.stage_seconds*multiplier)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait();code='timeout'
        row={'stage':name,'command':cmd,'exit':code,'seconds':round(time.monotonic()-before,3),'log':log.name,'log_sha256':sha(log)}
        steps.append(row);save(out/'progress.json',steps);print(json.dumps(row),flush=True)
        if code!=0:
            print(log.read_text(encoding='utf-8',errors='replace')[-12000:],flush=True);raise RuntimeError('Failed/incomplete stage: '+name)
    try:
        toolchain=repo/'research/quartic-variables';rules=toolchain/'astra-wave11';baseline=HERE/'baseline'
        run('syntax',HERE/'check_packet_syntax.py','--toolchain',toolchain,'--rules',rules)
        run('locator-fixtures',HERE/'test_locators.py','--base-adapter',HERE/'base_adapter.py',
            '--producer',rules/'batching/absorb_batch_error.py')
        run('build-source',HERE/'build_source.py','--baseline',baseline,'--out',out/'source')
        run('audit-source',HERE/'check_source.py','--source',out/'source','--baseline',baseline,
            '--report',out/'source-audit.json','--map',out/'construction-map.json','--seconds',a.stage_seconds)
        run('source-mutations',HERE/'test_source.py','--source',out/'source','--baseline',baseline,
            '--report',out/'source-mutations.json','--seconds',a.stage_seconds)
        run('repeat-source',HERE/'build_source.py','--baseline',baseline,'--out',out/'source-repeat')
        def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in path.rglob('*') if p.is_file()}
        first=tree(out/'source');assert first==tree(out/'source-repeat'),'Nondeterministic source files'
        save(out/'source-determinism.json',{'status':'PASS','files':first})
        if not a.source_only:
            adapter=out/'adapter'
            run('prepare-adapter',HERE/'prepare_adapter.py','--source',out/'source','--audit',out/'source-audit.json',
                '--construction-map',out/'construction-map.json','--audit-checker',HERE/'check_source.py',
                '--toolchain',toolchain,'--rules',rules,'--output',adapter)
            run('algebraic-pipeline',adapter/'tools/run_pipeline.py','--adapter',adapter,'--output',out/'stages',
                '--stage-seconds',a.stage_seconds,'--optimize',multiplier=20)
            endpoint=Path(load(out/'stages/SUMMARY.json')['last_verified_candidate'])
            assert endpoint.resolve().is_relative_to((out/'stages').resolve())
            run('named-source-mutations',HERE/'test_named_source.py','--adapter',adapter,'--candidate',endpoint,
                '--report',out/'named-source-mutations.json','--seconds',a.stage_seconds)
        complete=True
    finally:
        summary={**inputs,'status':'SOURCE CHECKS PASSED' if complete and a.source_only else 'ALGEBRAIC CANDIDATE VERIFIED' if complete else 'INCOMPLETE OR FAILED',
                 'seconds':round(time.monotonic()-start,3),'steps':steps}
        if complete and endpoint is not None:
            report=load(endpoint/'verification.json');summary['endpoint']=str(endpoint.relative_to(out));summary['verification_sha256']=sha(endpoint/'verification.json')
            summary['verified']={k:report[k] for k in ('source_id','variables','witnesses','rows','degree','monomials','max_abs_coefficient','expanded_sha256','certificate_sha256','checker_sha256')}
            summary['below10000']=report['variables']<10000
        save(out/'SUMMARY.json',summary);print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
