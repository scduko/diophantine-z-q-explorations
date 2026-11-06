"""Fresh source generation and exact frozen-certificate replay for one release."""
if not __debug__:
    raise RuntimeError('Assertions required')
import argparse,ctypes,gzip,json,os,platform,shutil,signal,subprocess,sys,time,zlib
from pathlib import Path
from common import *

ACTIVE=None
PARENT_PID=None
def available_memory():
    data=Path('/proc/meminfo').read_text()
    values={line.split(':',1)[0]:int(line.split()[1])*1024 for line in data.splitlines() if line.startswith('MemAvailable:')}
    need('MemAvailable' in values,'Cannot establish available memory')
    return values['MemAvailable']
def child_setup():
    os.setsid()
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:os._exit(125)
    if os.getppid()!=PARENT_PID:os.kill(os.getpid(),signal.SIGKILL)
    import resource
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
def kill_active():
    if ACTIVE is not None:
        try:os.killpg(ACTIVE.pid,signal.SIGKILL)
        except ProcessLookupError:pass
def interrupted(sig,frame):
    kill_active();raise SystemExit(128+sig)
def same_report(a,b):
    a=dict(a);b=dict(b);a.pop('seconds',None);b.pop('seconds',None)
    need(a==b,'Report differs beyond top-level elapsed seconds')
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in path.rglob('*') if p.is_file()}
def validate(package):
    manifest=load(package/'reproducibility/manifest.json')
    need(manifest['format']=='quartic-release-reproducibility/v2','Package format')
    manifest_files(package,manifest)
    need(set(tree(package))==set(manifest['files'])|{'reproducibility/manifest.json'},'Unmanifested package files')
    recipe=manifest['recipe'];need(recipe['profile']=='target2-tangent-first-norm/v1','Unsupported release profile')
    s=selection(recipe['selection']);need(load(package/'reproducibility/selection.json')==s,'Selection copy differs')
    need(type(recipe['cleanup']) is bool and recipe['cleanup']==(s['cleanup_manifest_sha256'] is not None),'Cleanup selection differs')
    entry=load(package/'source-entry.json')
    need(sha(package/'source-entry.json')==s['source_entry_sha256'],'Entry pin')
    need(sha(package/'source-residuals.jsonl.gz')==s['source_archive_sha256']==entry['source_sha256'],'Source archive pin')
    for name,key in [('source-audit.json','source_audit_sha256'),('construction-map.json','construction_map_sha256'),('source-layout.json','source_layout_sha256')]:
        need(sha(package/name)==entry[key],'Metadata pin '+name)
    for name,pin_value in entry['inspected_files_sha256'].items():need(sha(child(package/'source',name))==pin_value,'Source file pin '+name)
    pipeline=package/'reproducibility/pipeline'
    need(sha(pipeline/'manifest.json')==s['source_pipeline_manifest_sha256'],'Source pipeline pin')
    need(sha(pipeline/'check_source.py')==entry['source_audit_checker_sha256'],'Source checker pin')
    need(sha(package/'reproducibility/base/verify_named_source.py')==s['base_checker_sha256'],'Base checker pin')
    need(sha(package/'verify_certificate.py')==s['final_checker_sha256'],'Final checker pin')
    inspect_registry(package/'verify_certificate.py',entry)
    inspect_registry(package/'reproducibility/base/verify_named_source.py',entry)
    inspect_certificate(package/'certificate.jsonl.gz',entry,s['source_entry_sha256'])
    need(sha(package/'certificate.jsonl.gz')==s['final_certificate_sha256'],'Certificate pin')
    need(sha(package/'polynomial.expanded.txt')==s['final_expansion_sha256'],'Expansion pin')
    need(sha(package/'evidence/arithmetic-source-review.md')==s['arithmetic_review_sha256'],'Arithmetic review pin')
    need(manifest['expected']==expected_report(load(package/'evidence/final-verification.json'),entry,s),'Expected report mismatch')
    if recipe['cleanup']:
        cleanup=package/'reproducibility/cleanup'
        need(sha(cleanup/'MANIFEST.json')==s['cleanup_manifest_sha256'],'Cleanup packet pin')
        manifest_files(cleanup,load(cleanup/'MANIFEST.json'))
        need(sha(cleanup/'inputs/base-checker.py')==s['base_checker_sha256'],'Cleanup base pin')
        need(sha(cleanup/'tools/verify_elimination.py')==s['final_checker_sha256'],'Cleanup final pin')
        binding=load(cleanup/'BINDING.json')
        need(binding['source_id']==entry['source_id'] and binding['explicit_input_pins']['source_entry']==s['source_entry_sha256'],'Cleanup source binding')
    return manifest,entry,s

def main():
    global ACTIVE,PARENT_PID
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--output',type=Path,required=True);p.add_argument('--stage-seconds',type=int,default=180)
    p.add_argument('--rediscover',action='store_true');a=p.parse_args()
    need(sys.platform.startswith('linux'),'Linux process controls required')
    need(1<=a.stage_seconds<=600,'Stage timeout range')
    need(available_memory()>=8*1024**3,'At least 8 GiB available memory required to start')
    package=a.package.resolve();out=a.output.resolve();manifest,entry,s=validate(package)
    need(out!=package and package not in out.parents and not out.exists(),'Fresh output outside package required')
    if a.rediscover:need(manifest['recipe']['cleanup'],'Rediscovery requires a selected cleanup packet')
    out.mkdir(parents=True);PARENT_PID=os.getpid()
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    pipeline=package/'reproducibility/pipeline';baseline=pipeline/'baseline'
    external=package/'reproducibility/external-repository';toolchain=external/'research/quartic-variables';rules=toolchain/'astra-wave11'
    expected=manifest['expected'];steps=[];started=time.monotonic()
    summary=dict(status='RUNNING',mandatory_status='NOT COMPLETED',rediscovery_status='NOT REQUESTED',
        source_id=entry['source_id'],expected=expected,selection=s,steps=steps,
        package_manifest_sha256=sha(package/'reproducibility/manifest.json'),source_arithmetic_acceptance=False)
    def run(label,script,*args,timeout=None,reject=False):
        global ACTIVE
        command=[sys.executable,'-E','-B',str(script),*map(str,args)]
        log=out/(label+'.log');before=time.monotonic();timed_out=False;memory_abort=False
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
        with log.open('wb') as f:
            ACTIVE=subprocess.Popen(command,cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,preexec_fn=child_setup)
            try:
                deadline=before+(timeout or a.stage_seconds)
                while ACTIVE.poll() is None:
                    memory_abort=available_memory()<4*1024**3
                    timed_out=time.monotonic()>=deadline
                    if memory_abort or timed_out:kill_active();break
                    try:ACTIVE.wait(timeout=min(0.25,max(0.001,deadline-time.monotonic())))
                    except subprocess.TimeoutExpired:pass
                code=ACTIVE.wait()
            finally:kill_active();ACTIVE=None
        steps.append(dict(step=label,exit_code=code,timeout=timed_out,memory_abort=memory_abort,expected_rejection=reject,
                          seconds=round(time.monotonic()-before,3),log=log.name,log_sha256=sha(log)))
        save(out/'steps.json',steps)
        need(not timed_out and not memory_abort and (code>0 if reject else code==0),'Failed or incomplete stage '+label)
        if reject:need(b'AssertionError' in log.read_bytes(),'Negative case failed outside an assertion: '+label)
    def verify(label,checker,candidate,final=False):
        run(label,checker,candidate);r=load(candidate/'verification.json')
        need(r.get('status')=='PASS' and r['source_id']==entry['source_id'] and r['source_sha256']==s['source_archive_sha256'],'Replay identity')
        need(r['checker_sha256']==sha(checker),'Replay checker identity')
        need(r['degree']==4 and r['max_abs_coefficient']<2**80,'Replay quartic bound')
        if final:need(all(r[k]==v for k,v in expected.items()),'Final replay differs from selected artifact')
        return r
    def audit(label,source):
        result=out/(label+'.json');mapping=out/(label+'-map.json')
        run(label,pipeline/'check_source.py','--source',source,'--baseline',baseline,'--report',result,'--map',mapping,'--seconds',a.stage_seconds)
        same_report(load(result),load(package/'source-audit.json'))
        need(sha(mapping)==entry['construction_map_sha256'],'Regenerated map differs')
        return mapping
    try:
        run('syntax',pipeline/'check_packet_syntax.py','--toolchain',toolchain,'--rules',rules)
        run('locators',pipeline/'test_conic_locators.py')
        run('linear-pole',pipeline/'test_linear.py','--builder',baseline/'compiler/archive_build.py','--report',out/'linear-pole.json')
        run('pole-integration',pipeline/'test_linear_integration.py','--report',out/'pole-integration.json')
        for label,name in [('joint-chart','test_joint_chart.py'),('first-norm','test_first_norm_identities.py'),
            ('shared-square','test_shared_square.py'),('shared-resources','test_shared_square_resources.py'),
            ('normalized-lucas','test_normalization_identity.py')]:run(label,pipeline/name)
        run('target-two',pipeline/'test_target2_audit.py','--parents',pipeline/'parent/modules','--base-audit',pipeline/'audit_root_rewrite.py','--producer',pipeline/'target2_rewrite.py')
        run('tangent-identities',pipeline/'test_doublings.py','--parent-root',pipeline/'parent/modules/Z_definition.json','--root-helper',pipeline/'target2_rewrite.py','--report',out/'tangent-identities.json')
        run('tangent-mutations',pipeline/'test_tangent_portable.py','--parents',pipeline/'parent/modules','--report',out/'tangent-mutations.json')
        run('anchor',pipeline/'test_anchor_four.py','--builder',baseline/'compiler/archive_build.py')
        source=out/'source';fixture=out/'proxy-root.json'
        run('build-source',pipeline/'build_source.py','--baseline',baseline,'--out',source,'--proxy-fixture',fixture)
        for name,pin_value in entry['inspected_files_sha256'].items():need(sha(child(source,name))==pin_value,'Fresh source differs: '+name)
        mapping=audit('fresh-source-audit',source)
        run('source-mutations',pipeline/'test_root_shared_source.py','--source',source,'--baseline',baseline,'--report',out/'source-mutations.json','--seconds',a.stage_seconds)
        same_report(load(out/'source-mutations.json'),load(package/'evidence/source-run/source-mutations.json'))
        run('parent-mutations',pipeline/'test_normalized_pole_source.py','--source',pipeline/'parent','--baseline',baseline,'--report',out/'parent-mutations.json','--core',pipeline/'core_audit.py','--anchor-checker',pipeline/'check_anchor_four.py','--seconds',a.stage_seconds)
        run('proxy-guards',pipeline/'test_proxy_removal.py','--builder',baseline/'compiler/archive_build.py','--joint-root',fixture,'--out',out/'proxy-guards.json')
        run('repeat-source',pipeline/'build_source.py','--baseline',baseline,'--out',out/'source-repeat')
        need(tree(source)==tree(out/'source-repeat'),'Nondeterministic source generation')
        adapter=out/'adapter'
        run('prepare-adapter',pipeline/'prepare_adapter.py','--source',source,'--audit',package/'source-audit.json','--construction-map',mapping,'--audit-checker',pipeline/'check_source.py','--toolchain',toolchain,'--rules',rules,'--output',adapter)
        need(sha(adapter/'source-entry.json')==s['source_entry_sha256'],'Regenerated source entry differs')
        need(sha(adapter/'verify_named_source.py')==s['base_checker_sha256'],'Regenerated base checker differs')
        need(load(adapter/'adapter-manifest.json')==load(package/'reproducibility/base/adapter-manifest.json'),'Regenerated adapter differs')
        basechecker=adapter/'verify_named_source.py';tools=adapter/'tools'
        current=out/'fresh-lift';run('fresh-lift',tools/'fresh_lift.py','--adapter',adapter,'--output',current);verify('verify-lift',basechecker,current)
        target=out/'parity';run('parity',tools/'produce_parity.py','--repo',adapter,'--parent',current,'--output',target);verify('verify-parity',basechecker,target);current=target
        for name,script,args in [('optimized','optimize.py',['--max-terms',96,'--rounds',8,'--rational','--gaussian','--row-combine','--row-order','reverse']),('coordinates','merge_coordinates.py',[])]:
            target=out/name;run(name,tools/script,'--parent',current,'--output',target,*args);verify('verify-'+name,basechecker,target);current=target
        run('base-named-mutations',pipeline/'test_named_source.py','--adapter',adapter,'--candidate',current,'--report',out/'base-named-mutations.json','--seconds',a.stage_seconds)
        finalchecker=out/'verify-final.py'
        if manifest['recipe']['cleanup']:
            ct=package/'reproducibility/cleanup/tools'
            for name in ('test_unit_relations.py','test_relation_eliminate.py','test_affine_units.py'):run('cleanup-'+name[:-3],ct/name,timeout=30)
            run('cleanup-supplemental',ct/'supplemental_tests.py',ct,timeout=30)
            run('regenerate-final-checker',ct/'make_frozen_checker.py','--base',basechecker,'--output',finalchecker,timeout=30)
        else:shutil.copyfile(basechecker,finalchecker)
        need(sha(finalchecker)==s['final_checker_sha256'],'Regenerated final checker differs');inspect_registry(finalchecker,entry)
        reference=out/'selected-final';reference.mkdir()
        for name in CANDIDATE:shutil.copyfile(package/name,reference/name)
        fresh_archive=adapter/'source-residuals.jsonl.gz'
        need(sha(fresh_archive)==s['source_archive_sha256'],'Fresh source compression differs')
        shutil.copyfile(fresh_archive,reference/'source-residuals.jsonl.gz')
        summary['final_verification']=verify('verify-selected-final',finalchecker,reference,True)
        for case in ('wrong-source','wrong-entry','wrong-expansion'):
            bad=out/('reject-'+case);shutil.copytree(reference,bad)
            if case=='wrong-source':
                path=bad/'source-residuals.jsonl.gz'
                # Keep the gzip and source header valid, so rejection reaches
                # the pinned mathematical source hash instead of the decoder.
                lines=gzip.decompress(path.read_bytes()).splitlines()
                row=json.loads(lines[1]);row[0][0]+=1
                lines[1]=json.dumps(row,separators=(',',':')).encode()
                path.write_bytes(gzip.compress(b'\n'.join(lines)+b'\n',compresslevel=1,mtime=0))
            elif case=='wrong-entry':
                path=bad/'certificate.jsonl.gz';lines=gzip.decompress(path.read_bytes()).splitlines();head=json.loads(lines[0]);head['source_entry_sha256']='0'*64;lines[0]=json.dumps(head,separators=(',',':')).encode();path.write_bytes(gzip.compress(b'\n'.join(lines)+b'\n',compresslevel=1,mtime=0))
            else:
                path=bad/'polynomial.expanded.txt';lines=path.read_bytes().splitlines();parts=lines[1].split();parts[0]=str(int(parts[0])+1).encode();lines[1]=b' '.join(parts);raw=b'\n'.join(lines)+b'\n';path.write_bytes(raw);(bad/'polynomial.expanded.txt.gz').write_bytes(gzip.compress(raw,compresslevel=1,mtime=0))
            run('reject-'+case,finalchecker,bad,reject=True)
        summary['mandatory_status']='PASS: FRESH SOURCE AND EXACT FROZEN CERTIFICATE REPLAY'
        if a.rediscover:
            summary['rediscovery_status']='RUNNING'
            cleanup=package/'reproducibility/cleanup';ct=cleanup/'tools';binding=load(cleanup/'BINDING.json')
            run('power-locator',ct/'test_source_locator.py',timeout=30)
            run('power-identities',ct/'test_power_chain.py','--checker',basechecker,'--tools',ct,timeout=30)
            current=out/'discovery-baseline';shutil.copytree(cleanup/'inputs/parent',current)
            shutil.copyfile(fresh_archive,current/'source-residuals.jsonl.gz');verify('rediscovery-baseline',basechecker,current)
            need(sha(current/'source-entry.json')==s['source_entry_sha256'],'Discovery entry pin')
            target=out/'power-chain'
            run('power-chain',ct/'power_chain.py','--artifact',current,'--adapter',adapter,'--conic-module','q_conic13','--checker',basechecker,
                '--expect-source-entry',s['source_entry_sha256'],'--expect-checker',s['base_checker_sha256'],
                '--expect-certificate',binding['pins']['inputs/parent/certificate.jsonl.gz'],'--report',out/'power-chain-report.json','--output',target,'--tools',ct)
            verify('verify-power-chain',basechecker,target);current=target
            for name,script,args in [('pre-linear','optimize.py',['--max-terms',96,'--rounds',8,'--rational','--gaussian','--row-combine','--row-order','reverse']),('pre-coordinates','merge_coordinates.py',[])]:
                target=out/name;run(name,ct/script,'--parent',current,'--output',target,*args);shutil.copyfile(current/'source-entry.json',target/'source-entry.json');verify('verify-'+name,basechecker,target);current=target
            for name,script in [('constant-relation','probe_relation_eliminate.py'),('affine-after-relation','probe_affine_unit_relations.py'),('relation-again','probe_relation_eliminate.py')]:
                target=out/name;run(name,ct/script,'--research-dir',ct,'--seconds',120,'--candidate-seconds',1,'--max-candidates',20000,'--max-operations',2000,'--max-consumers',48,'--parent',current,'--source-entry',current/'source-entry.json','--output',target,'--report',out/(name+'.json'),'--events',out/(name+'-events.jsonl'))
                verify('verify-'+name,finalchecker,target);current=target
            for name,script,args in [('post-linear','optimize.py',['--max-terms',96,'--rounds',8,'--rational','--gaussian','--row-combine','--row-order','reverse']),('post-coordinates','merge_coordinates.py',[])]:
                target=out/name;run(name,ct/script,'--parent',current,'--output',target,*args);shutil.copyfile(current/'source-entry.json',target/'source-entry.json');r=verify('verify-'+name,finalchecker,target);current=target
            summary['rediscovery_status']='PASS: SEPARATE HEURISTIC RESULT'
            summary['rediscovery']=dict(verification=r,expansion_matches_selected=r['expanded_sha256']==s['final_expansion_sha256'],certificate_matches_selected=r['certificate_sha256']==s['final_certificate_sha256'])
        summary.update(status='PASS',python=sys.version,platform=platform.platform(),zlib_runtime=zlib.ZLIB_RUNTIME_VERSION)
    except BaseException as error:
        summary.update(status='FAIL OR INCOMPLETE',error=repr(error));raise
    finally:
        kill_active();summary['seconds']=round(time.monotonic()-started,3);save(out/'SUMMARY.json',summary)
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':main()
