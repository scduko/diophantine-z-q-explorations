"""Root-dispatched bounded Linux trial of the rational-difference source."""
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
        run('conic-locator-fixtures',HERE/'test_conic_locators.py')
        run('linear-pole-identities',HERE/'test_linear.py','--builder',baseline/'compiler/archive_build.py','--report',out/'linear-pole-identities.json')
        run('pole-integration',HERE/'test_linear_integration.py','--report',out/'pole-integration.json')
        run('joint-chart-identities',HERE/'test_joint_chart.py')
        run('first-norm-identities',HERE/'test_first_norm_identities.py')
        run('shared-square-identities',HERE/'test_shared_square.py')
        run('shared-square-resources',HERE/'test_shared_square_resources.py')
        run('root-delta-mutations',HERE/'test_target2_audit.py','--parents',HERE/'parent/modules','--base-audit',HERE/'audit_root_rewrite.py','--producer',HERE/'target2_rewrite.py')
        run('tangent-identities',HERE/'test_doublings.py','--parent-root',HERE/'parent/modules/Z_definition.json','--root-helper',HERE/'target2_rewrite.py','--report',out/'tangent-identities.json')
        run('tangent-mutations',HERE/'test_tangent_portable.py','--parents',HERE/'parent/modules','--report',out/'tangent-mutations.json')
        run('normalized-lucas-identities',HERE/'test_normalization_identity.py')
        run('anchor4-identities',HERE/'test_anchor_four.py','--builder',baseline/'compiler/archive_build.py')
        run('build-source',HERE/'build_source.py','--baseline',baseline,'--out',out/'source','--proxy-fixture',out/'proxy-root.json')
        run('audit-source',HERE/'check_source.py','--source',out/'source','--baseline',baseline,
            '--report',out/'source-audit.json','--map',out/'construction-map.json','--seconds',a.stage_seconds)
        run('source-mutations',HERE/'test_root_shared_source.py','--source',out/'source','--baseline',baseline,
            '--report',out/'source-mutations.json','--seconds',a.stage_seconds)
        run('inherited-source-mutations',HERE/'test_normalized_pole_source.py','--source',HERE/'parent','--baseline',baseline,
            '--report',out/'inherited-source-mutations.json','--core',HERE/'core_audit.py',
            '--anchor-checker',HERE/'check_anchor_four.py','--seconds',a.stage_seconds)
        run('proxy-removal-guards',HERE/'test_proxy_removal.py','--builder',baseline/'compiler/archive_build.py',
            '--joint-root',out/'proxy-root.json','--out',out/'proxy-removal-guards.json')
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
            summary['below5000']=report['variables']<5000
        save(out/'SUMMARY.json',summary);print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
