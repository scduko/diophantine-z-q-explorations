"""Remote-only streaming builder for full and current-only public handoffs.

The large public baseline is supplied as a local path on the remote worker.
It is copied unchanged with ZIP_STORED, never downloaded or recompressed here.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile
from datetime import date

from verify_handoff import BASELINE_SHA, BASELINE_BYTES, safe_name, stream_hash, verify
from release_config import validate_release, generated_state, generated_start


def encoded(value):
    return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode('utf-8')


def validate_git_plan(plan,tree):
    if not re.fullmatch(r'[0-9a-f]{40}',plan['snapshot_commit']):
        raise ValueError('Expected a full immutable Git commit ID')
    wanted={f['path']:f['git_blob'] for f in plan['files'] if f['kind']=='git'}
    if len(wanted)!=sum(f['kind']=='git' for f in plan['files']):
        raise ValueError('Repeated Git source path')
    if any(f['archive_path']!='current/'+f['path'] for f in plan['files'] if f['kind']=='git'):
        raise ValueError('Git destination differs from its exact current path')
    if tree!=wanted:
        raise ValueError('Plan is not the complete exact public commit')
    return wanted


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--payload',type=Path,default=Path(__file__).with_name('payload'))
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    plan=json.loads(a.plan.read_bytes())
    if plan['format']!='quartic-handoff-plan/v2':
        raise ValueError('Wrong plan format')
    release=validate_release(plan['release'])
    if not re.fullmatch(r'[0-9a-f]{40}',plan['snapshot_commit']):
        raise ValueError('Expected a full immutable Git commit ID')
    if plan['baseline']['sha256']!=BASELINE_SHA or plan['baseline']['bytes']!=BASELINE_BYTES:
        raise ValueError('Wrong pinned baseline')
    with a.baseline.open('rb') as stream:
        if stream_hash(stream)!={'sha256':BASELINE_SHA,'bytes':BASELINE_BYTES}:
            raise ValueError('Supplied public baseline bytes differ')
    if a.output.exists():
        raise ValueError('Use a new output directory')
    # Confirm every planned Git name and blob against the complete commit tree.
    tree={}
    raw_tree=subprocess.check_output(['git','-C',str(a.repo),'ls-tree','-r','-z','--full-tree',plan['snapshot_commit']])
    for record in raw_tree.split(b'\0'):
        if record:
            metadata,path=record.split(b'\t',1); mode,kind,oid=metadata.decode().split()
            if mode not in ('100644','100755') or kind!='blob':
                raise ValueError('Nonregular current Git member')
            tree[safe_name(path.decode('utf-8'))]=oid
    wanted=validate_git_plan(plan,tree)
    names=[safe_name(f['archive_path']) for f in plan['files']]
    if len(names)!=len(set(names)) or len(names)!=len({n.casefold() for n in names}):
        raise ValueError('Duplicate or case-colliding plan names')
    reserved={'MANIFEST.json','START_HERE.md','CURRENT_STATE.json','verify_handoff.py','PLAN.json',
              'release_config.py','legacy_verify_handoff_v2.py'}
    if {n.casefold() for n in reserved}&{n.casefold() for n in names}:
        raise ValueError('Plan overwrites generated handoff metadata')
    a.output.mkdir(parents=True)
    full_path=a.output/release['assets']['full']
    current_path=a.output/release['assets']['current']
    inventories=[{},{}]
    def write(archive,index,name,stream,wanted=None,stored=False):
        safe_name(name)
        stamp=date.fromisoformat(release['date'])
        info=zipfile.ZipInfo(name,date_time=(stamp.year,stamp.month,stamp.day,0,0,0))
        info.create_system=3
        info.compress_type=zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
        info._compresslevel=1; info.external_attr=0o100644<<16
        digest=hashlib.sha256(); size=0
        with archive.open(info,'w',force_zip64=True) as target:
            for chunk in iter(lambda:stream.read(1024*1024),b''):
                target.write(chunk); digest.update(chunk); size+=len(chunk)
        actual=dict(sha256=digest.hexdigest(),bytes=size)
        if wanted is not None and actual!=wanted:
            raise ValueError('Source changed or plan hash is wrong: '+name)
        inventories[index][name]=actual
    with zipfile.ZipFile(full_path,'w',allowZip64=True) as full, zipfile.ZipFile(current_path,'w',allowZip64=True) as current:
        archives=(full,current)
        for item in plan['files']:
            if item['kind']=='git':
                raw=subprocess.check_output(['git','-C',str(a.repo),'cat-file','blob',item['git_blob']])
            elif item['kind']=='payload':
                source=(a.payload/safe_name(item['path'])).resolve()
                if not source.is_relative_to(a.payload.resolve()):
                    raise ValueError('Payload path escaped root')
                raw=source.read_bytes()
            else:
                raise ValueError('Unknown source kind')
            expected={k:item[k] for k in ('sha256','bytes')}
            for i,archive in enumerate(archives):
                write(archive,i,item['archive_path'],io.BytesIO(raw),expected)
        baseline_path='baseline/'+plan['baseline']['filename']
        with a.baseline.open('rb') as source:
            write(full,0,baseline_path,source,dict(sha256=BASELINE_SHA,bytes=BASELINE_BYTES),stored=True)
        current_files=sorted(wanted)
        for i,archive in enumerate(archives):
            included=i==0
            state=generated_state(plan,included)
            start=generated_start(plan,included)
            for name,raw in [('START_HERE.md',start),('CURRENT_STATE.json',encoded(state)),
                             ('PLAN.json',a.plan.read_bytes()),('verify_handoff.py',Path(__file__).with_name('verify_handoff.py').read_bytes()),
                             ('release_config.py',Path(__file__).with_name('release_config.py').read_bytes()),
                             ('legacy_verify_handoff_v2.py',Path(__file__).with_name('legacy_verify_handoff_v2.py').read_bytes())]:
                write(archive,i,name,io.BytesIO(raw))
            manifest=dict(format='quartic-public-handoff/v2',snapshot_commit=plan['snapshot_commit'],
                          current_files=current_files,files=inventories[i],
                          baseline=dict(**plan['baseline'],included=included,archive_path=baseline_path),
                          history_scope=state['selected_history'])
            # The manifest covers every other entry. Its whole-file identity is
            # subsequently bound by the external ZIP checksum and receipt.
            stamp=date.fromisoformat(release['date'])
            info=zipfile.ZipInfo('MANIFEST.json',date_time=(stamp.year,stamp.month,stamp.day,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            archive.writestr(info,encoded(manifest),compress_type=zipfile.ZIP_DEFLATED,compresslevel=1)
    reports=[]
    for path in (full_path,current_path):
        report=verify(path,hashlib.sha256(a.plan.read_bytes()).hexdigest())
        with path.open('rb') as source:
            report.update(stream_hash(source))
        report['filename']=path.name; reports.append(report)
    (a.output/'SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['filename']+'\n' for r in reports),encoding='ascii')
    (a.output/'BUILD_RECEIPT.json').write_bytes(encoded(dict(status='PASS',version=release['version'],date=release['date'],archives=reports,
        plan_sha256=hashlib.sha256(a.plan.read_bytes()).hexdigest(),
        builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        verifier_sha256=hashlib.sha256(Path(__file__).with_name('verify_handoff.py').read_bytes()).hexdigest())))
    print(json.dumps(reports,indent=2))


if __name__=='__main__':
    main()
