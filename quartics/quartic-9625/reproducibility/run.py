"""Replay and cleanly reproduce one manifest-bound quartic release package.

All source/checker/producer files are immutable. Generated files go only to a
fresh --output directory. Linux, the standard library and compatible gzip
behavior are required. Arithmetic theorem acceptance remains separate.
"""
if not __debug__:raise RuntimeError('Run without Python optimization')
import argparse
import ctypes
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import signal
import subprocess
import sys
import time
import zlib

CANDIDATE=('source-residuals.jsonl.gz','certificate.jsonl.gz','candidate-rows.json.gz',
           'residuals.json.gz','variable-map.json','weights.json','polynomial.expanded.txt',
           'polynomial.expanded.txt.gz')
_active=None
_parent_pid=None
MEMORY_BYTES=2*1024**3

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def load(path):return json.loads(path.read_bytes())
def save(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')

def contained(root,name):
    p=PurePosixPath(name)
    assert not p.is_absolute() and '\\' not in name and ':' not in name
    assert all(x not in ('','.','..') for x in p.parts)
    target=root.joinpath(*p.parts).resolve();assert root in target.parents
    return target

def validate(package):
    manifest=load(package/'reproducibility/manifest.json')
    assert manifest['format']=='quartic-release-reproducibility/v2'
    for name,item in manifest['files'].items():
        path=contained(package,name)
        assert path.is_file() and path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],name
    actual={p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
    assert actual==set(manifest['files'])|{'reproducibility/manifest.json'},'Unmanifested package files'
    expected=manifest['expected'];entry=load(package/'source-entry.json');recipe=manifest['recipe']
    assert entry['source_id']==expected['source_id'] and entry['source_sha256']==expected['source_sha256']
    assert sha(package/'verify_certificate.py')==expected['checker_sha256']
    assert sha(package/'source-entry.json')==recipe['source_entry_sha256']
    assert sha(package/'source-audit.json')==entry['source_audit_sha256']
    assert sha(package/'construction-map.json')==entry['construction_map_sha256']
    assert sha(package/'source-layout.json')==entry['source_layout_sha256']
    pipeline=package/'reproducibility/pipeline';packet=load(pipeline/'manifest.json')
    assert sha(pipeline/'check_source.py')==entry['source_audit_checker_sha256']
    assert sha(pipeline/'manifest.json')==recipe['packet_manifest_sha256']
    assert len(packet['external_inputs'])==recipe['external_inputs']==13
    for name,item in packet['files'].items():assert sha(contained(pipeline,name))==item['sha256']
    external=package/'reproducibility/external-repository'
    for item in packet['external_inputs']:assert sha(contained(external,item['path']))==item['sha256']
    for name,pin in entry['inspected_files_sha256'].items():assert sha(contained(package/'source',name))==pin
    return manifest,entry

def compare_json(actual,expected):
    a=dict(actual);b=dict(expected);a.pop('seconds',None);b.pop('seconds',None)
    assert a==b,'Report differs beyond its top-level elapsed seconds'

def child_setup():
    os.setsid()
    libc=ctypes.CDLL(None,use_errno=True)
    if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:os._exit(125)
    if os.getppid()!=_parent_pid:os.kill(os.getpid(),signal.SIGKILL)
    import resource
    resource.setrlimit(resource.RLIMIT_AS,(MEMORY_BYTES,MEMORY_BYTES))

def kill(sig=9):
    if _active is not None:
        try:os.killpg(_active.pid,sig)
        except ProcessLookupError:pass

def interrupted(sig,frame):
    kill();raise SystemExit(128+sig)

def main():
    global _active,_parent_pid
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--stage-seconds',type=int,default=180)
    a=p.parse_args();assert 1<=a.stage_seconds<=600
    package=a.package.resolve();output=a.output.resolve()
    manifest,entry=validate(package);expected=manifest['expected'];recipe=manifest['recipe']
    if not sys.platform.startswith('linux'):raise RuntimeError('Bounded reproduction requires Linux process groups and prctl')
    assert output!=package and package not in output.parents and not output.exists(),'Use a fresh output outside the immutable package'
    raw=(package/'source/residuals.jsonl').read_bytes();compressed=(package/'source-residuals.jsonl.gz').read_bytes()
    assert gzip.decompress(compressed)==raw
    assert gzip.compress(raw,compresslevel=1,mtime=0)==compressed,(
        'Exact compressed reproduction requires the original gzip behavior; use Linux CPython3.12 with compatible zlib. '
        'The unchanged verifier can separately replay the frozen artifact elsewhere.')
    output.mkdir(parents=True);_parent_pid=os.getpid()
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    started=time.monotonic();steps=[]
    summary=dict(status='RUNNING',expected=expected,source_id=entry['source_id'],source_sha256=entry['source_sha256'],
                 checker_sha256=expected['checker_sha256'],package_manifest_sha256=sha(package/'reproducibility/manifest.json'),
                 source_arithmetic_acceptance=False,steps=steps)
    pipeline=package/'reproducibility/pipeline';external=package/'reproducibility/external-repository'
    toolchain=external/'research/quartic-variables';rules=toolchain/'astra-wave11'
    checker=package/'verify_certificate.py';python=[sys.executable,'-E','-B']
    def run(label,script,*arguments):
        global _active
        command=python+[str(script),*map(str,arguments)];log=output/(label+'.log');before=time.monotonic()
        print(json.dumps(dict(step=label,command=command)),flush=True)
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
        with log.open('wb') as f:
            _active=subprocess.Popen(command,cwd=output,env=env,stdout=f,stderr=subprocess.STDOUT,preexec_fn=child_setup)
            timed_out=False
            try:code=_active.wait(timeout=a.stage_seconds)
            except subprocess.TimeoutExpired:
                timed_out=True;kill(signal.SIGTERM)
                try:_active.wait(timeout=3)
                except subprocess.TimeoutExpired:kill();_active.wait(timeout=5)
                code=_active.returncode
            finally:kill();_active=None
        item=dict(step=label,exit_code=code,timeout=timed_out,seconds=round(time.monotonic()-before,3),
                  log=log.name,log_sha256=sha(log));steps.append(item);save(output/'steps.json',steps)
        assert not timed_out and code==0,('Failed stage',label,log)
    def verify(label,candidate,endpoint=False):
        run(label,checker,candidate);report=load(candidate/'verification.json')
        assert report['status']=='PASS' and report['source_id']==entry['source_id']
        assert report['source_sha256']==entry['source_sha256'] and report['checker_sha256']==expected['checker_sha256']
        assert report['degree']==4 and report['max_abs_coefficient']<2**80
        if endpoint:
            for key,value in expected.items():
                if key!='certificate_sha256':assert report[key]==value,(key,report[key],value)
        return report
    def source_audit(label,source):
        audit=output/(label+'.json');mapping=output/(label+'-map.json')
        run(label,pipeline/'check_source.py','--source',source,'--baseline',pipeline/'baseline',
            '--report',audit,'--map',mapping,'--seconds',a.stage_seconds)
        compare_json(load(audit),load(package/'source-audit.json'))
        assert sha(mapping)==entry['construction_map_sha256']
        return mapping
    try:
        run('syntax',pipeline/'check_packet_syntax.py','--toolchain',toolchain,'--rules',rules)
        run('locator-fixtures',pipeline/'test_locators.py','--base-adapter',pipeline/'base_adapter.py',
            '--producer',rules/'batching/absorb_batch_error.py')
        if recipe['jacobi_locator']:run('jacobi-locators',pipeline/'test_jacobi_locators.py')
        source_audit('frozen-source-audit',package/'source')
        mutation_args=['--source',package/'source','--baseline',pipeline/'baseline','--report',output/'source-mutations.json']
        if recipe['source_mutation_has_core']:mutation_args+=['--core',pipeline/'core_audit.py']
        else:mutation_args+=['--seconds',a.stage_seconds]
        run('source-mutations',pipeline/recipe['source_mutation_script'],*mutation_args)
        compare_json(load(output/'source-mutations.json'),recipe['expected_source_mutations'])
        reference=output/'reference';reference.mkdir()
        for name in CANDIDATE:shutil.copyfile(package/name,reference/name)
        frozen=verify('frozen-certificate',reference,True)
        assert frozen['certificate_sha256']==expected['certificate_sha256']
        frozen_adapter=output/'frozen-adapter';frozen_adapter.mkdir()
        shutil.copytree(package/'source',frozen_adapter/'source')
        for name in ('source-entry.json','source-audit.json','construction-map.json','source-layout.json','source-residuals.jsonl.gz'):
            shutil.copyfile(package/name,frozen_adapter/name)
        shutil.copyfile(checker,frozen_adapter/'verify_named_source.py')
        shutil.copyfile(package/'reproducibility/frozen-adapter-manifest.json',frozen_adapter/'adapter-manifest.json')
        run('frozen-named-mutations',pipeline/'test_named_source.py','--adapter',frozen_adapter,'--candidate',reference,
            '--report',output/'frozen-named-mutations.json','--seconds',a.stage_seconds)
        compare_json(load(output/'frozen-named-mutations.json'),recipe['expected_named_mutations'])
        rebuilt=output/'rebuilt-source'
        run('source-regeneration',pipeline/'build_source.py','--baseline',pipeline/'baseline','--out',rebuilt)
        for name,pin in entry['inspected_files_sha256'].items():assert sha(contained(rebuilt,name))==pin,('Regenerated source differs',name)
        rebuilt_map=source_audit('rebuilt-source-audit',rebuilt)
        adapter=output/'rebuilt-adapter'
        # The fresh audit was compared in full except elapsed time above.
        # Passing the frozen byte-identical report preserves the named-entry
        # digest even for an auditor which records elapsed time.
        run('adapter-regeneration',pipeline/'prepare_adapter.py','--source',rebuilt,'--audit',package/'source-audit.json',
            '--construction-map',rebuilt_map,'--audit-checker',pipeline/'check_source.py',
            '--toolchain',toolchain,'--rules',rules,'--output',adapter)
        assert sha(adapter/'source-entry.json')==recipe['source_entry_sha256']
        assert sha(adapter/'verify_named_source.py')==expected['checker_sha256']
        frozen_manifest=load(package/'reproducibility/frozen-adapter-manifest.json')
        assert load(adapter/'adapter-manifest.json')==frozen_manifest
        for name,pin in frozen_manifest['generated_sha256'].items():assert sha(contained(adapter,name))==pin,name
        tools=adapter/'tools';current=output/'fresh-lift'
        run('fresh-lift',tools/'fresh_lift.py','--adapter',adapter,'--output',current);verify('verify-fresh-lift',current)
        for name,script in [('norms','reduce_norms.py'),('charts','replace_charts.py'),('ordinates','remove_chart_ordinates.py'),
                            ('parity','produce_parity.py'),('batch','absorb_batch_error.py')]:
            target=output/name
            options=['--adapter' if name=='norms' else '--repo',adapter,'--parent',current,'--output',target]
            if name=='charts':options+=['--diagnostic',output/'chart-diagnostic.json']
            run(name,tools/script,*options);verify('verify-'+name,target);current=target
        target=output/'optimized'
        run('optimize',tools/'optimize.py','--parent',current,'--output',target,'--max-terms',96,'--rounds',8,
            '--rational','--gaussian','--row-combine','--row-order','reverse')
        verify('verify-optimized',target);current=target;target=output/'coordinates'
        run('merge-coordinates',tools/'merge_coordinates.py','--parent',current,'--output',target)
        regenerated=verify('verify-regenerated-endpoint',target,True)
        for name in CANDIDATE:
            if name!='certificate.jsonl.gz':assert (package/name).read_bytes()==(target/name).read_bytes(),name
        def records(path):
            value=[json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
            for item in value:
                if item['kind']=='final':item['report'].pop('seconds',None)
            return value
        assert records(package/'certificate.jsonl.gz')==records(target/'certificate.jsonl.gz')
        run('regenerated-named-mutations',pipeline/'test_named_source.py','--adapter',adapter,'--candidate',target,
            '--report',output/'regenerated-named-mutations.json','--seconds',a.stage_seconds)
        compare_json(load(output/'regenerated-named-mutations.json'),recipe['expected_named_mutations'])
        summary.update(status='PASS: FROZEN REPLAY AND CLEAN REPRODUCTION',
            regenerated_certificate_sha256=regenerated['certificate_sha256'],
            certificate_comparison='All records identical after removing only final.report.seconds',
            source_mutations=load(output/'source-mutations.json'),named_source_mutations=load(output/'regenerated-named-mutations.json'),
            python=sys.version,platform=platform.platform(),zlib_compile_version=zlib.ZLIB_VERSION,zlib_runtime_version=zlib.ZLIB_RUNTIME_VERSION,
            scope='Exact finite construction, source audit, projection-preserving replay, full expansion and reproducibility; arithmetic theorem acceptance remains separate')
    except BaseException as exc:
        summary.update(status='FAIL: NOT VERIFIED',error=repr(exc));raise
    finally:
        kill();summary['seconds']=round(time.monotonic()-started,3);save(output/'SUMMARY.json',summary)
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':main()
