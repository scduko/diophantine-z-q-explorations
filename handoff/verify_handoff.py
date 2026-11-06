"""Verify a release handoff ZIP; optionally extract into a new directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import re
import zipfile
from release_config import validate_release, validate_current, generated_state, generated_start

BASELINE_SHA='827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b'
BASELINE_BYTES=339860770


def safe_name(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\x00' in name:
        raise ValueError('Unsafe archive name')
    path=PurePosixPath(name)
    if path.is_absolute() or any(p in ('','.', '..') for p in name.split('/')) or str(path)!=name:
        raise ValueError('Unsafe archive name: '+name)
    devices={'con','prn','aux','nul'}|{'com'+str(i) for i in range(1,10)}|{'lpt'+str(i) for i in range(1,10)}
    if any(p.endswith((' ','.')) or p.split('.')[0].casefold() in devices for p in path.parts):
        raise ValueError('Nonportable archive name: '+name)
    return name


def stream_hash(stream):
    digest=hashlib.sha256(); size=0
    for chunk in iter(lambda:stream.read(1024*1024),b''):
        digest.update(chunk); size+=len(chunk)
    return dict(sha256=digest.hexdigest(),bytes=size)


def verify(path,expected_plan_sha256=None,expected_archive_sha256=None):
    if expected_archive_sha256 is not None:
        if not re.fullmatch('[0-9a-f]{64}', expected_archive_sha256):
            raise ValueError('Invalid expected archive SHA256')
        with Path(path).open('rb') as stream:
            if stream_hash(stream)['sha256'] != expected_archive_sha256:
                raise ValueError('Archive differs from externally supplied SHA256')
    with zipfile.ZipFile(path) as archive:
        members=archive.infolist(); names=[safe_name(m.filename) for m in members]
        if len(names)!=len(set(names)) or len(names)!=len({n.casefold() for n in names}):
            raise ValueError('Duplicate or case-colliding ZIP names')
        for member in members:
            mode=(member.external_attr>>16)&0xffff
            if member.is_dir() or stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in (0,stat.S_IFREG):
                raise ValueError('Nonregular ZIP member: '+member.filename)
        manifest=json.loads(archive.read('MANIFEST.json'))
        if manifest['format']=='quartic-12504-public-handoff/v1':
            if expected_plan_sha256 is not None:
                raise ValueError('Legacy Version 2 requires the independently published whole-ZIP SHA256, checked before legacy integrity verification; plan-only authentication is supported for Version 3')
            from legacy_verify_handoff_v2 import verify as verify_v2
            result=verify_v2(path)
            result['scope']='Legacy Version 2 integrity only. Authenticate first with the independently published whole-ZIP SHA256; Version 3 exact-plan guarantees do not apply.'
            return result
        if manifest['format']!='quartic-public-handoff/v2':
            raise ValueError('Unknown handoff format')
        expected=manifest['files']
        if set(names)!=set(expected)|{'MANIFEST.json'}:
            raise ValueError('ZIP inventory differs from manifest')
        for name,record in expected.items():
            safe_name(name)
            with archive.open(name) as stream:
                actual=stream_hash(stream)  # Reading to EOF also checks CRC.
            if actual!=record:
                raise ValueError('Wrong member bytes: '+name)
        plan_raw=archive.read('PLAN.json')
        plan_sha=hashlib.sha256(plan_raw).hexdigest()
        if expected_plan_sha256 is not None and plan_sha!=expected_plan_sha256:
            raise ValueError('Handoff plan differs from externally supplied digest')
        plan=json.loads(plan_raw)
        if plan['format']!='quartic-handoff-plan/v2' or plan['snapshot_commit']!=manifest['snapshot_commit']:
            raise ValueError('Wrong embedded snapshot plan')
        release=validate_release(plan['release'])
        planned={item['archive_path']:{key:item[key] for key in ('sha256','bytes')} for item in plan['files']}
        if len(planned)!=len(plan['files']):
            raise ValueError('Duplicate planned member')
        git_items=[item for item in plan['files'] if item['kind']=='git']
        if len(git_items)!=len({item['path'] for item in git_items}) or any(item['archive_path']!='current/'+item['path'] for item in git_items):
            raise ValueError('Wrong current source/destination mapping')
        for name,record in planned.items():
            if expected.get(name)!=record:
                raise ValueError('Member differs from frozen plan: '+name)
        baseline=manifest['baseline']
        if type(baseline['included']) is not bool:
            raise ValueError('Invalid baseline inclusion flag')
        baseline_path='baseline/'+plan['baseline']['filename']
        if baseline != dict(**plan['baseline'],included=baseline['included'],archive_path=baseline_path):
            raise ValueError('Baseline metadata differs from frozen plan')
        if baseline['sha256']!=BASELINE_SHA or baseline['bytes']!=BASELINE_BYTES:
            raise ValueError('Wrong historical baseline identity')
        if baseline['included']:
            if expected[baseline['archive_path']]!={'sha256':BASELINE_SHA,'bytes':BASELINE_BYTES}:
                raise ValueError('Nested baseline bytes differ')
        elif baseline['archive_path'] in expected:
            raise ValueError('Unexpected nested baseline')
        helpers={'verify_handoff.py','release_config.py','legacy_verify_handoff_v2.py'}
        generated={'PLAN.json','START_HERE.md','CURRENT_STATE.json'}|helpers
        allowed=set(planned)|generated|({baseline_path} if baseline['included'] else set())
        if set(planned)&generated or set(expected)!=allowed:
            raise ValueError('Unplanned or missing archive member')
        for helper in helpers:
            if expected[helper] != expected.get('current/handoff/'+helper):
                raise ValueError('Generated helper differs from committed helper: '+helper)
        current=manifest['current_files']
        if len(current)!=len(set(current)) or set('current/'+p for p in current)!={n for n in expected if n.startswith('current/')}:
            raise ValueError('Current snapshot inventory differs')
        if set(current)!={item['path'] for item in plan['files'] if item['kind']=='git'}:
            raise ValueError('Current snapshot differs from frozen Git file manifest')
        validate_current(lambda name:archive.read('current/'+safe_name(name)),set(current),
                         release,plan['verification_receipt'])
        state=json.loads(archive.read('CURRENT_STATE.json'))
        if state != generated_state(plan,baseline['included']):
            raise ValueError('Stale current-state fields')
        if archive.read('START_HERE.md') != generated_start(plan,baseline['included']):
            raise ValueError('Generated guide differs from frozen plan')
        if manifest['history_scope'] != state['selected_history']:
            raise ValueError('Manifest history scope differs from frozen plan')
    return dict(status='PASS',archive_files=len(names),current_files=len(current),
                snapshot_commit=manifest['snapshot_commit'],baseline_included=baseline['included'],
                baseline_sha256=BASELINE_SHA,all_member_hashes_and_crc_verified=True,
                plan_sha256=plan_sha,externally_bound_plan=expected_plan_sha256 is not None,
                externally_bound_archive=expected_archive_sha256 is not None,
                scope='Payload integrity and exact current proof-package closure. Authenticate the snapshot using the published archive or plan SHA256.')


def extract_verified(path,destination,expected_plan_sha256=None,expected_archive_sha256=None):
    report=verify(path,expected_plan_sha256,expected_archive_sha256)
    destination=destination.resolve()
    if destination.exists():
        raise ValueError('Extraction destination must be new')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(path) as archive:
        manifest=json.loads(archive.read('MANIFEST.json'))
        for member in archive.infolist():
            name=safe_name(member.filename)
            target=destination.joinpath(*PurePosixPath(name).parts)
            if not target.resolve().is_relative_to(destination):
                raise ValueError('Extraction path escaped destination')
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.open(member) as source, target.open('xb') as output:
                shutil.copyfileobj(source,output,1024*1024)
            if name!='MANIFEST.json':
                with target.open('rb') as stream:
                    if stream_hash(stream)!=manifest['files'][name]:
                        raise ValueError('Extracted bytes changed: '+name)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path)
    p.add_argument('--extract',type=Path)
    p.add_argument('--report',type=Path)
    p.add_argument('--expected-plan-sha256')
    p.add_argument('--expected-archive-sha256')
    a=p.parse_args()
    report=extract_verified(a.archive,a.extract,a.expected_plan_sha256,a.expected_archive_sha256) if a.extract else verify(a.archive,a.expected_plan_sha256,a.expected_archive_sha256)
    text=json.dumps(report,indent=2)+'\n'
    if a.report:
        a.report.write_text(text,encoding='utf-8',newline='\n')
    print(text,end='')


if __name__=='__main__':
    main()
