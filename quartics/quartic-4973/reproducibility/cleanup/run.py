"""Run the frozen source-pinned sequential elimination wave in a fresh output directory.

Relocatable Linux packet; all heavy work is sequential and bounded. A PASS
is finite algebraic replay, not acceptance of the exploratory source theorem.
"""
if not __debug__:
    raise RuntimeError('Run without Python optimization')

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import signal
import subprocess
import sys
import time

BINDING = {'source_id': 'target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b', 'baseline': {'variables': 5295, 'witnesses': 5294, 'rows': 4873, 'monomials': 74046, 'degree': 4, 'max_abs_coefficient': 685783949153203534233890}, 'pins': {'inputs/parent/certificate.jsonl.gz': '232d536ee6e884cdc283e1ddd9528c2a7123e6c6ef1504019677b992874cf177', 'inputs/parent/source-residuals.jsonl.gz': '94f8a1972cbfc0cf6493d418e628a18482307dec5c427db72e86d3eacb1a6f5d', 'inputs/parent/source-entry.json': '39af6e354ce265a7954c2fbae53373862a89f81114e6c24c56eb9ff3020d9857', 'inputs/parent/polynomial.expanded.txt': '058e438b3112a8d463661663a7d6581e86760f5a9bc2cf5d5d0e3e2a5bba1bad', 'inputs/base-checker.py': '324ab603f1ce1175da6de18f3f600aa2b0c1e2474ea65a575b4a4cac48e09f90', 'tools/verify_elimination.py': 'b7180b01029b3d9364d94914401a4f1f66b190762f10b99a38e9fd4f49437ffe'}, 'kit_manifest_sha256': '2dc466d42df919e443874c5960729730e23eb1a0bc41b547c1e7ed62f892883c', 'reviewed_core_sha256': '0c118eb0d38178f34c40096b6ff84ab7136a6fde08b3ec7a5544ab339fd37b71', 'explicit_input_pins': {'source_entry': '39af6e354ce265a7954c2fbae53373862a89f81114e6c24c56eb9ff3020d9857', 'checker': '324ab603f1ce1175da6de18f3f600aa2b0c1e2474ea65a575b4a4cac48e09f90', 'certificate': '232d536ee6e884cdc283e1ddd9528c2a7123e6c6ef1504019677b992874cf177'}, 'scope': 'Exact algebraic replay only; source arithmetic acceptance remains separate'}
SOURCE_ID = BINDING['source_id']
PINS = BINDING['pins']
BASE_COUNTS = BINDING['baseline']
MEMORY_BYTES = 2*1024**3
_active = None


def sha(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()


def validate_packet(root):
    manifest = json.loads((root/'MANIFEST.json').read_text())
    assert manifest['format'] == 'pinned-elimination-wave-v1'
    assert manifest['source_id'] == SOURCE_ID
    assert manifest['baseline'] == BASE_COUNTS
    files = manifest['files']
    assert set(PINS) <= files.keys()
    assert all(files[name]['sha256'] == digest for name,digest in PINS.items())
    for name, expected in files.items():
        rel = PurePosixPath(name)
        assert name and not rel.is_absolute() and '\\' not in name and ':' not in name
        assert all(part not in ('', '.', '..') for part in rel.parts)
        path = root.joinpath(*rel.parts)
        assert root in path.resolve().parents
        assert all(not p.is_symlink() for p in (path, *path.parents) if p == root or root in p.parents)
        assert path.is_file() and path.stat().st_size == expected['bytes'], name
        assert sha(path) == expected['sha256'], name
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == set(files) | {'MANIFEST.json'}, sorted(actual ^ (set(files) | {'MANIFEST.json'}))
    entry = json.loads((root/'inputs/parent/source-entry.json').read_text())
    assert entry['source_id'] == SOURCE_ID
    assert entry['source_sha256'] == PINS['inputs/parent/source-residuals.jsonl.gz']
    return manifest


def child_setup():
    # Each child leads a group, dies if this runner dies, and has a hard
    # address-space limit. There is never more than one active heavy child.
    parent = _parent_pid
    os.setsid()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0: os._exit(125)
    if os.getppid() != parent: os.kill(os.getpid(), signal.SIGKILL)
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))


def kill_active(sig=9):
    if _active is not None:
        try: os.killpg(_active.pid, sig)
        except ProcessLookupError: pass


def interrupted(sig, frame):
    kill_active()
    raise SystemExit(128+sig)


def write_json(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def run_step(label, command, timeout, output, records):
    global _active
    start = time.monotonic()
    log = output/(label+'.log')
    record = dict(step=label,command=list(map(str,command)),timeout_seconds=timeout,log=log.name)
    with log.open('wb') as f:
        _active = subprocess.Popen(list(map(str,command)), stdout=f,stderr=subprocess.STDOUT,
                                   cwd=output,preexec_fn=child_setup)
        try:
            record['exit_code'] = _active.wait(timeout=timeout)
            record['status'] = 'PASS' if record['exit_code']==0 else 'FAIL'
        except subprocess.TimeoutExpired:
            record['status'] = 'TIMEOUT'
            kill_active(signal.SIGTERM)
            try: _active.wait(timeout=3)
            except subprocess.TimeoutExpired:
                kill_active(); _active.wait(timeout=5)
            record['exit_code'] = _active.returncode
        finally:
            # Descendants cannot survive a completed stage and overlap the
            # next one, even if the direct child exited before them.
            kill_active()
            _active = None
    record.update(seconds=round(time.monotonic()-start,3),log_sha256=sha(log))
    records.append(record)
    write_json(output/'progress.json',records)
    print(json.dumps(record),flush=True)
    return record['status']=='PASS'


def inspect_verification(path, baseline=False, base=False):
    report=json.loads((path/'verification.json').read_text())
    assert report['status']=='PASS'
    assert report['source_id']==SOURCE_ID
    assert report['source_sha256']==PINS['inputs/parent/source-residuals.jsonl.gz']
    assert report['checker_sha256']==PINS['inputs/base-checker.py' if base else 'tools/verify_elimination.py']
    assert report['degree']==4 and report['max_abs_coefficient']<2**80
    assert report['witnesses']==report['variables']-1
    if baseline:
        assert all(report[key]==value for key,value in BASE_COUNTS.items())
        assert report['expanded_sha256']==PINS['inputs/parent/polynomial.expanded.txt']
    return report


def main():
    global _parent_pid
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=validate_packet(root)
    if not sys.platform.startswith('linux'):
        raise RuntimeError('This bounded runner requires Linux process groups and prctl')
    output=args.output.resolve()
    assert output!=root and root not in output.parents, 'Output must be outside the frozen packet'
    assert not output.exists(), 'Output must be fresh'
    output.mkdir(parents=True)
    _parent_pid=os.getpid()
    signal.signal(signal.SIGTERM,interrupted); signal.signal(signal.SIGINT,interrupted)
    tools=root/'tools'; python=[sys.executable,'-E','-B']
    records=[]
    summary=dict(status='RUNNING',scope='Finite algebraic search and full replay; exploratory source arithmetic not accepted',
                 source_id=SOURCE_ID,manifest_sha256=sha(root/'MANIFEST.json'),baseline=BASE_COUNTS,
                 memory_bytes_per_child=MEMORY_BYTES,steps=records,candidates={})
    started=time.monotonic()
    try:
        for name in ('test_relation_eliminate.py','test_unit_relations.py','test_affine_units.py'):
            assert run_step(name[:-3],python+[tools/name],30,output,records),name
        assert run_step('independent-supplemental',python+[tools/'supplemental_tests.py',tools],30,output,records)
        regenerated=output/'regenerated-checker.py'
        assert run_step('regenerate-checker',python+[tools/'make_frozen_checker.py','--base',root/'inputs/base-checker.py',
                    '--output',regenerated],30,output,records)
        assert sha(regenerated)==PINS['tools/verify_elimination.py']
        assert run_step('tiny-source-locator',python+[tools/'test_source_locator.py'],30,output,records)
        assert run_step('tiny-power-chain',python+[tools/'test_power_chain.py','--checker',root/'inputs/base-checker.py','--tools',tools],30,output,records)
        parent=output/'baseline'
        shutil.copytree(root/'inputs/parent',parent)
        checker=root/'inputs/base-checker.py'
        assert run_step('replay-baseline',python+[checker,parent],90,output,records)
        summary['baseline_verification']=inspect_verification(parent,True,True)
        current=parent
        previous_count=BASE_COUNTS['variables']
        candidate=output/'power-chain'
        command=python+[tools/'power_chain.py','--artifact',current,'--adapter',root/'inputs/adapter',
            '--conic-module','q_conic13',
            '--checker',checker,'--expect-source-entry',PINS['inputs/parent/source-entry.json'],
            '--expect-checker',PINS['inputs/base-checker.py'],'--expect-certificate',PINS['inputs/parent/certificate.jsonl.gz'],
            '--report',output/'power-chain-report.json','--output',candidate,'--tools',tools]
        assert run_step('power-chain',command,180,output,records)
        assert run_step('replay-power-chain',python+[checker,candidate],90,output,records)
        verified=inspect_verification(candidate,base=True)
        summary['candidates']['power-chain']={'parent':current.name,'verification':verified,
            'variables_removed_from_parent':previous_count-verified['variables']}
        current=candidate;previous_count=verified['variables']
        write_json(output/'SUMMARY.json',summary)
        for name,script,options in (
                ('pre-linear-cleanup','optimize.py',['--max-terms','96','--rounds','8','--rational',
                    '--gaussian','--row-combine','--row-order','reverse']),
                ('pre-coordinates','merge_coordinates.py',[])):
            candidate=output/name
            assert run_step(name,python+[tools/script,'--parent',current,'--output',candidate]+options,90,output,records),name
            shutil.copyfile(current/'source-entry.json',candidate/'source-entry.json')
            assert run_step('replay-'+name,python+[checker,candidate],90,output,records),name
            verified=inspect_verification(candidate,base=True)
            summary['candidates'][name]={'parent':current.name,'verification':verified,
                'variables_removed_from_parent':previous_count-verified['variables']}
            current=candidate;previous_count=verified['variables']
            write_json(output/'SUMMARY.json',summary)
        # Only the previously reviewed relation/affine rules are enabled.
        checker=tools/'verify_elimination.py'
        common=['--research-dir',tools,'--seconds','120','--candidate-seconds','1',
                '--max-candidates','20000','--max-operations','2000','--max-consumers','48']
        for name,script in (('constant-relation','probe_relation_eliminate.py'),
                            ('affine-after-relation','probe_affine_unit_relations.py'),
                            ('relation-again','probe_relation_eliminate.py')):
            candidate=output/name
            command=python+[tools/script]+common+['--parent',current,'--source-entry',current/'source-entry.json',
                '--output',candidate,'--report',output/(name+'-producer.json'),'--events',output/(name+'-events.jsonl')]
            assert run_step('search-'+name,command,180,output,records),name
            assert run_step('replay-'+name,python+[checker,candidate],90,output,records),name
            verified=inspect_verification(candidate)
            summary['candidates'][name]={'parent':current.name,'verification':verified,
                'variables_removed_from_parent':previous_count-verified['variables']}
            current=candidate; previous_count=verified['variables']
            write_json(output/'SUMMARY.json',summary)
        for name,script,options in (
                ('linear-cleanup','optimize.py',['--max-terms','96','--rounds','8','--rational',
                    '--gaussian','--row-combine','--row-order','reverse']),
                ('coordinates','merge_coordinates.py',[])):
            candidate=output/name
            assert run_step(name,python+[tools/script,'--parent',current,'--output',candidate]+options,90,output,records),name
            shutil.copyfile(current/'source-entry.json',candidate/'source-entry.json')
            assert run_step('replay-'+name,python+[checker,candidate],90,output,records),name
            verified=inspect_verification(candidate)
            summary['candidates'][name]={'parent':current.name,'verification':verified,
                'variables_removed_from_parent':previous_count-verified['variables']}
            current=candidate; previous_count=verified['variables']
            write_json(output/'SUMMARY.json',summary)
        summary['status']='PASS'
        summary['final_variables']=previous_count
        summary['variables_removed_from_baseline']=BASE_COUNTS['variables']-previous_count
        summary['below_5000_algebraic_variables']=previous_count<5000
    except BaseException as exc:
        summary['status']='FAIL'
        summary['error']=repr(exc)
        raise
    finally:
        kill_active()
        summary['seconds']=round(time.monotonic()-started,3)
        write_json(output/'SUMMARY.json',summary)
    if summary['status']!='PASS': raise SystemExit(1)
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__=='__main__': main()
