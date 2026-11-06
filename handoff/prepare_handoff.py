"""Freeze an explicit handoff plan from one complete public Git commit.

Run remotely after the current release files and fresh verification receipt are
committed. This neither downloads nor compresses the historical baseline.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

from verify_handoff import safe_name, BASELINE_SHA, BASELINE_BYTES
from release_config import validate_release, validate_current

BAD_PARTS={'.git','.lake','node_modules','__pycache__','.aws','.codex','conversations','transcripts'}
BAD_NAMES={'auth.json','credentials.json','cookies.json','cookies.sqlite','token.json','tokens.json',
           'conversation.json','conversation.txt','transcript.json','transcript.txt','chat.json','chat.txt',
           'host.stdout.txt','stdin.txt'}
SECRET=re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{30,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16})\b')
DIALOGUE=re.compile(rb'"role"\s*:\s*"(?:user|assistant|system|tool)"|(?im:^\s*(?:Human|Assistant|User)\s*:\s)|<\|im_start\|>|<conver' rb'sation>')
CREDENTIAL=re.compile(rb'"(?:access_token|refresh_token|id_token|api_key|client_secret|password)"\s*:\s*"([^"\r\n]{12,})"',re.I)


def scan(name,raw):
    safe_name(name)
    parts=name.casefold().split('/'); leaf=parts[-1]
    if set(parts)&BAD_PARTS or leaf in BAD_NAMES or leaf.startswith('.env') or leaf.endswith(('.pem','.p12','.key','.pyc','.olean','.ilean')):
        raise ValueError('Forbidden payload path: '+name)
    def content(data):
        if SECRET.search(data) or DIALOGUE.search(data):
            raise ValueError('Credential or dialogue marker requires review: '+name)
        for match in CREDENTIAL.finditer(data):
            if not any(x in match[1].lower() for x in (b'placeholder',b'example',b'environment',b'${',b'<',b'null',b'string',b'redacted')):
                raise ValueError('Credential field requires review: '+name)
    content(raw)
    if name.endswith('.gz'):
        with gzip.GzipFile(fileobj=io.BytesIO(raw),mode='rb') as stream:
            decoded=stream.read(150_000_001)
        if len(decoded)>150_000_000:
            raise ValueError('Expanded payload exceeds size bound')
        content(decoded)


def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--commit',required=True)
    p.add_argument('--payload',type=Path,default=Path(__file__).with_name('payload'))
    p.add_argument('--selection',type=Path,default=Path(__file__).with_name('selection.json'))
    p.add_argument('--release',type=Path,default=Path(__file__).with_name('release.json'))
    p.add_argument('--verification-receipt',required=True,help='Repository-relative fresh full reproduction SUMMARY.json')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():
        raise ValueError('Use a new plan path')
    commit=git(a.repo,'rev-parse','--verify',a.commit+'^{commit}').decode().strip()
    if not re.fullmatch(r'[0-9a-f]{40}',commit):
        raise ValueError('Expected a full immutable Git commit ID')
    objects={}; files=[]
    for record in git(a.repo,'ls-tree','-r','-z','--full-tree',commit).split(b'\0'):
        if not record:
            continue
        metadata,path=record.split(b'\t',1); mode,kind,oid=metadata.decode().split()
        name=path.decode('utf-8'); safe_name(name)
        if mode not in ('100644','100755') or kind!='blob':
            raise ValueError('Current commit contains a nonregular member: '+name)
        raw=git(a.repo,'cat-file','blob',oid)
        scan(name,raw)
        objects[name]=raw
        files.append(dict(kind='git',path=name,archive_path='current/'+name,git_blob=oid,
                          bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    release=validate_release(json.loads(a.release.read_bytes()))
    validate_current(objects.__getitem__,set(objects),release,a.verification_receipt)
    selection=json.loads(a.selection.read_bytes())
    if selection['format']!='quartic-handoff-selection/v2':
        raise ValueError('Unknown selection format')
    for item in selection['files']:
        name=safe_name(item['path']); path=(a.payload/name).resolve()
        if not (name.startswith('history/') or name in ('COVERAGE.md','RESEARCH_NOTES.md')):
            raise ValueError('Selected history has an unauthorized destination')
        if not path.is_relative_to(a.payload.resolve()):
            raise ValueError('Selected payload escaped root')
        raw=path.read_bytes(); scan(name,raw)
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise ValueError('Selected note changed: '+name)
        files.append(dict(kind='payload',path=name,archive_path=name,bytes=len(raw),sha256=item['sha256'],
                          original_path=item.get('original_path'),scope=item['scope']))
    names=[f['archive_path'] for f in files]
    if len(names)!=len(set(names)) or len(names)!=len({n.casefold() for n in names}):
        raise ValueError('Colliding current and history names')
    plan=dict(format='quartic-handoff-plan/v2',snapshot_commit=commit,files=files,release=release,
              verification_receipt=a.verification_receipt,
              baseline=dict(filename='z-in-q-research-handoff-2026-11-04-r2.zip',sha256=BASELINE_SHA,bytes=BASELINE_BYTES,
                            url='https://github.com/elliotglazer/diophantine-z-q/releases/download/research-handoff-2026-11-04-r2/z-in-q-research-handoff-2026-11-04-r2.zip'),
              scope='Complete public commit plus explicitly selected project mathematical history; raw private archives and conversations are not included',
              scan='New payload bytes and gzip text checked for credential/dialogue patterns; unchanged public baseline is not rescanned')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(plan,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status='PLAN FROZEN; ARCHIVE NOT BUILT',snapshot_commit=commit,files=len(files),
                          plan_sha256=hashlib.sha256(a.output.read_bytes()).hexdigest()),indent=2))


if __name__=='__main__':
    main()
