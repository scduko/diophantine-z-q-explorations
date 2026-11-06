"""Verify a Version 2 handoff ZIP; optionally extract it into a new directory."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import zipfile

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


def verify(path,expected_plan_sha256=None):
    with zipfile.ZipFile(path) as archive:
        members=archive.infolist(); names=[safe_name(m.filename) for m in members]
        if len(names)!=len(set(names)) or len(names)!=len({n.casefold() for n in names}):
            raise ValueError('Duplicate or case-colliding ZIP names')
        for member in members:
            mode=(member.external_attr>>16)&0xffff
            if member.is_dir() or stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in (0,stat.S_IFREG):
                raise ValueError('Nonregular ZIP member: '+member.filename)
        manifest=json.loads(archive.read('MANIFEST.json'))
        if manifest['format']!='quartic-12504-public-handoff/v1':
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
        if plan['format']!='quartic-12504-handoff-plan/v1' or plan['snapshot_commit']!=manifest['snapshot_commit']:
            raise ValueError('Wrong embedded snapshot plan')
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
        if baseline['sha256']!=BASELINE_SHA or baseline['bytes']!=BASELINE_BYTES:
            raise ValueError('Wrong historical baseline identity')
        if baseline['included']:
            if expected[baseline['archive_path']]!={'sha256':BASELINE_SHA,'bytes':BASELINE_BYTES}:
                raise ValueError('Nested baseline bytes differ')
        elif baseline['archive_path'] in expected:
            raise ValueError('Unexpected nested baseline')
        current=manifest['current_files']
        if len(current)!=len(set(current)) or set('current/'+p for p in current)!={n for n in expected if n.startswith('current/')}:
            raise ValueError('Current snapshot inventory differs')
        if set(current)!={item['path'] for item in plan['files'] if item['kind']=='git'}:
            raise ValueError('Current snapshot differs from frozen Git file manifest')
        polynomial='current/quartics/quartic-12504/polynomial.expanded.txt'
        if expected[polynomial]['sha256']!='7f5aa3117af82a0b323f0a4e74a18599204f5540408106d3ce99612b5ed830ca':
            raise ValueError('Wrong current quartic')
        root='current/quartics/quartic-12504/'
        required_pins={'verify_certificate.py':'d2079177a4960740c5b7d42fbd0756dfc4ce8953cc947cee91c8786ba26fa8ba',
                       'certificate.jsonl.gz':'9f7979c1e786bebad624b9ea4631b7eccd879f4bebb5b9ab69250b945973b268',
                       'source-residuals.jsonl.gz':'ce9eeac7c4730aced8cfb70a1ab3b1b6a7fb2110c597afad1f56ddc92aeea73f',
                       'source-entry.json':'c0fc67ef6ead31dd018ca92643dc4988fcf28f9755dd9be7e017651bf4b14abc',
                       'source-audit.json':'7c67ff1736e4a4f0e1f7e70e7f5e47c956dfb0c644fd5264acd0c224bbd60e01',
                       'construction-map.json':'edad166ce99d33fe50271e2afdc1628bbec0361d812762212240cadd30f93cfe'}
        for name,digest in required_pins.items():
            if expected.get(root+name,{}).get('sha256')!=digest:
                raise ValueError('Missing or wrong current proof artifact: '+name)
        entry=json.loads(archive.read(root+'source-entry.json'))
        for name,digest in entry['inspected_files_sha256'].items():
            if expected.get(root+'source/'+safe_name(name),{}).get('sha256')!=digest:
                raise ValueError('Incomplete pinned source package: '+name)
        package=json.loads(archive.read(root+'reproducibility/manifest.json'))
        for name,record in package['files'].items():
            if expected.get(root+safe_name(name))!=record:
                raise ValueError('Incomplete reproducibility package: '+name)
        for name in ('current/quartic_12504.tex','current/quartic_12504.pdf','current/docs/quartic-12504/README.md'):
            if name not in expected:
                raise ValueError('Missing current manuscript or inventory')
        receipt=json.loads(archive.read('current/'+safe_name(plan['verification_receipt'])))
        if receipt['status']!='PASS: FROZEN REPLAY AND CLEAN REPRODUCTION':
            raise ValueError('Missing fresh full reproduction receipt')
    return dict(status='PASS',archive_files=len(names),current_files=len(current),
                snapshot_commit=manifest['snapshot_commit'],baseline_included=baseline['included'],
                baseline_sha256=BASELINE_SHA,all_member_hashes_and_crc_verified=True,
                plan_sha256=plan_sha,externally_bound_plan=expected_plan_sha256 is not None,
                scope='Payload integrity and exact current proof-package closure. Authenticate the snapshot using the published archive or plan SHA256.')


def extract_verified(path,destination,expected_plan_sha256=None):
    report=verify(path,expected_plan_sha256)
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
    a=p.parse_args()
    report=extract_verified(a.archive,a.extract,a.expected_plan_sha256) if a.extract else verify(a.archive,a.expected_plan_sha256)
    text=json.dumps(report,indent=2)+'\n'
    if a.report:
        a.report.write_text(text,encoding='utf-8',newline='\n')
    print(text,end='')


if __name__=='__main__':
    main()
