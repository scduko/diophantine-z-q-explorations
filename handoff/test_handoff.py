"""Small adversarial checks; no baseline download, compression, or proof run."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import stat
import tempfile
import zipfile

from build_handoff import validate_git_plan
from prepare_handoff import DIALOGUE, scan
from verify_handoff import safe_name, verify
from test_release import run_tests as release_tests
from test_release_v5 import run_tests as release_v5_tests


def reject(label,function,message):
    try:
        function()
    except ValueError as error:
        if message not in str(error):
            raise AssertionError((label,'wrong rejection',str(error))) from error
        return label
    raise AssertionError('Accepted malformed fixture: '+label)


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    tests=[]
    # Freeze the runtime pattern and flags from the original scanner policy.
    assert hashlib.sha256(DIALOGUE.pattern).hexdigest()=='d3017908981af04c663a0b97f3d160719e717b585221fa930ac1945b55c18d71'
    assert DIALOGUE.flags==0
    self_sources=[]
    for name in ('prepare_handoff.py','test_handoff.py'):
        raw=Path(__file__).with_name(name).read_bytes()
        scan('handoff/'+name,raw)
        scan('handoff/'+name+'.gz',gzip.compress(raw))
        self_sources.append(name)
    examples=[('serialized '+role,json.dumps({''.join(('ro','le')):role}).encode())
              for role in ('user','assistant','system','tool')]
    examples += [('user heading',b'Us'+b'er: prompt'),
                 ('assistant heading',b'  Assis'+b'tant: response'),
                 ('human heading',b'Hu'+b'man: prompt'),
                 ('chat marker',b'<|im_'+b'start|>'),
                 ('conversation marker',b'<conver'+b'sation>')]
    for label,raw in examples:
        tests.append(reject(label,lambda raw=raw:scan('fixture.txt',raw),'dialogue marker'))
        tests.append(reject('gzip '+label,lambda raw=raw:scan('fixture.txt.gz',gzip.compress(raw)),'dialogue marker'))
    for name in ('../x','/x','C:x','a\\b','a/../b','a//b','CON.txt','x.','dir /x','AUX'):
        tests.append(reject(name,lambda name=name:safe_name(name),'archive name'))
    good=dict(snapshot_commit='a'*40,files=[dict(kind='git',path='a',archive_path='current/a',git_blob='1'),
                                           dict(kind='git',path='b',archive_path='current/b',git_blob='2')])
    assert validate_git_plan(good,{'a':'1','b':'2'})=={'a':'1','b':'2'}
    bad=deepcopy(good); bad['files'][0]['archive_path']='current/b'; bad['files'][1]['archive_path']='current/a'
    tests.append(reject('swapped destinations',lambda:validate_git_plan(bad,{'a':'1','b':'2'}),'destination'))
    missing=deepcopy(good); missing['files'].pop()
    tests.append(reject('omitted Git file',lambda:validate_git_plan(missing,{'a':'1','b':'2'}),'complete exact'))
    secret=json.dumps({''.join(('pass','word')):'mock-value-for-negative-test'}).encode()
    tests.append(reject('raw credential field',lambda:scan('fixture.json',secret),'Credential field'))
    tests.append(reject('gzip credential field',lambda:scan('fixture.json.gz',gzip.compress(secret)),'Credential field'))
    scan('fixture.json.gz',gzip.compress(b'{"status":"PASS"}'))
    with tempfile.TemporaryDirectory(prefix='handoff-negative-') as temporary:
        root=Path(temporary)
        for name,entries,message in [('case',[('x',None),('X',None)],'case-colliding'),
                                     ('link',[('link',stat.S_IFLNK|0o777)],'Nonregular')]:
            path=root/(name+'.zip')
            with zipfile.ZipFile(path,'w') as archive:
                for member,mode in entries:
                    info=zipfile.ZipInfo(member)
                    if mode is not None:
                        info.external_attr=mode<<16
                    archive.writestr(info,b'target')
            tests.append(reject(name,lambda path=path:verify(path),message))
        legacy=root/'legacy.zip'
        with zipfile.ZipFile(legacy,'w') as archive:
            archive.writestr('MANIFEST.json',json.dumps({'format':'quartic-12504-public-handoff/v1'}))
        tests.append(reject('legacy plan-only authentication',lambda:verify(legacy,'0'*64),'Legacy Version 2 requires'))
        tests.append(reject('wrong external archive hash',lambda:verify(legacy,expected_archive_sha256='0'*64),'externally supplied SHA256'))
        tests.append(reject('malformed external archive hash',lambda:verify(legacy,expected_archive_sha256='bad'),'Invalid expected archive'))
    tests.extend(release_tests())
    tests.extend(release_v5_tests())
    print(json.dumps(dict(status='PASS',small_negative_cases=len(tests),cases=tests,
                         runtime_dialogue_pattern_unchanged=True,self_sources_scan_passed=self_sources),indent=2))


if __name__=='__main__':
    main()
