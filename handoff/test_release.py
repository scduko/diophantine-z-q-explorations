"""Small metadata fixtures; they are not mathematical certificate fixtures."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

from release_config import (validate_release,validate_current,generated_state,generated_start,
                            compare_reproduced_certificate)

def encode(value):
    return json.dumps(value,sort_keys=True).encode()

def certificate(records):
    return gzip.compress(b''.join(encode(record)+b'\n' for record in records),mtime=0)

def certificate_fixture():
    return [dict(kind='initial',rows=[[[1,[0]],[-1,[1]]]],operation_count=1,seconds=12),
            dict(kind='final',report=dict(variables=9625,seconds=0.673))]

def fixtures():
    release=json.loads((Path(__file__).parent/'releases/version4/release.json').read_bytes())
    root=release['package']+'/'
    files={name:('fixture '+name).encode() for name in release['proof_pins']}
    records=certificate_fixture()
    files['certificate.jsonl.gz']=certificate(records)
    # V4 replays the exact selected certificate rather than rediscovering it.
    regenerated=certificate(records)
    files['source-entry.json']=encode(dict(source_id=release['source_id'],
        source_sha256=hashlib.sha256(files['source-residuals.jsonl.gz']).hexdigest(),inspected_files_sha256={}))
    release['proof_pins']={name:hashlib.sha256(raw).hexdigest() for name,raw in files.items()}
    release['expected']['expanded_sha256']=release['proof_pins']['polynomial.expanded.txt']
    objects={root+name:raw for name,raw in files.items()}
    objects[release['replayed_certificate']]=regenerated
    objects['handoff/release.json']=encode(release)
    objects[release['manuscript']]=b'Version 4'
    objects[release['pdf']]=b'%PDF fixture'
    objects[release['inventory']]=b'fixture inventory'
    verification=dict(status='PASS',source_id=release['source_id'],
        source_sha256=release['proof_pins']['source-residuals.jsonl.gz'],
        checker_sha256=release['proof_pins']['verify_certificate.py'],certificate_sha256=release['proof_pins']['certificate.jsonl.gz'],**release['expected'])
    objects[root+release['verification']]=encode(verification)
    objects[root+'reproducibility/manifest.json']=encode(dict(expected=release['expected'],files={}))
    receipt='fixture-reproduction.json'
    objects[receipt]=encode(dict(status='PASS',mandatory_status='PASS: FRESH SOURCE AND EXACT FROZEN CERTIFICATE REPLAY',
        final_verification=verification,steps=[dict(step='fixture-only',exit_code=0,timeout=False,memory_abort=False,expected_rejection=False)],
        source_id=release['source_id'],source_sha256=verification['source_sha256'],
        checker_sha256=verification['checker_sha256'],expected=dict(release['expected'],certificate_sha256=release['proof_pins']['certificate.jsonl.gz']),
        package_manifest_sha256=hashlib.sha256(objects[root+'reproducibility/manifest.json']).hexdigest(),
        rediscovery_status='NOT REQUESTED'))
    return release,objects,receipt

def run_tests():
    release,objects,receipt=fixtures()
    validate_current(objects.__getitem__,set(objects),release,receipt)
    tests=[]
    def reject(name,change):
        r,o,p=fixtures();change(r,o,p)
        try:
            validate_current(o.__getitem__,set(o),r,p)
        except (ValueError,KeyError):
            tests.append(name)
        else:
            raise AssertionError('Accepted stale release fixture: '+name)
    def edit(o,name,key,value):
        data=json.loads(o[name]);data[key]=value;o[name]=encode(data)
    reject('stale manuscript name',lambda r,o,p:r.update(manuscript='quartic_12504.tex'))
    reject('stale Version 3',lambda r,o,p:r.update(version=3))
    reject('wrong release date',lambda r,o,p:r.update(date='2026-11-05'))
    reject('different variable target',lambda r,o,p:r['expected'].update(variables=8777))
    reject('stale asset name',lambda r,o,p:r['assets'].update(full='z-in-q-version2-full-handoff.zip'))
    reject('stale comparison profile',lambda r,o,p:r['source_contract'].update(full_comparisons=37))
    reject('missing proof pin',lambda r,o,p:r['proof_pins'].pop('source-audit.json'))
    reject('changed proof bytes',lambda r,o,p:o.__setitem__(r['package']+'/certificate.jsonl.gz',b'changed'))
    reject('uncommitted descriptor',lambda r,o,p:o.__setitem__('handoff/release.json',b'{}'))
    reject('missing PDF',lambda r,o,p:o.pop(r['pdf']))
    reject('stale manuscript subtitle',lambda r,o,p:o.__setitem__(r['manuscript'],b'Version 2'))
    reject('wrong reproduction source',lambda r,o,p:edit(o,p,'source_id','old-source'))
    reject('failed reproduction',lambda r,o,p:edit(o,p,'status','FAIL'))
    reject('changed replayed certificate',lambda r,o,p:o.__setitem__(r['replayed_certificate'],b'changed'))
    reject('incomplete mandatory reproduction',lambda r,o,p:edit(o,p,'mandatory_status','NOT COMPLETED'))
    reject('missing reproduction stages',lambda r,o,p:edit(o,p,'steps',[]))
    reject('missing replayed certificate',lambda r,o,p:o.pop(r['replayed_certificate']))
    reject('changed reproduction manifest',lambda r,o,p:edit(o,p,'package_manifest_sha256','0'*64))
    reject('stale verification count',lambda r,o,p:edit(o,r['package']+'/'+r['verification'],'variables',12504))
    def stale_receipt(r,o,p):
        data=json.loads(o[p]);data['expected']['monomials']=135721;o[p]=encode(data)
    reject('stale reproduction count',stale_receipt)
    originals=certificate_fixture();frozen=certificate(originals)
    timing=deepcopy(originals);timing[-1]['report']['seconds']=100.5
    compare_reproduced_certificate(frozen,certificate(timing),hashlib.sha256(certificate(timing)).hexdigest())
    def reject_certificate(label,change):
        changed=deepcopy(originals);change(changed);raw=certificate(changed)
        try:compare_reproduced_certificate(frozen,raw,hashlib.sha256(raw).hexdigest())
        except ValueError as error:
            assert 'outside final.report.seconds' in str(error),(label,str(error))
            tests.append(label)
        else:raise AssertionError('Accepted changed certificate: '+label)
    reject_certificate('changed mathematical row',lambda rs:rs[0]['rows'][0][0].__setitem__(0,2))
    reject_certificate('removed final non-timing field',lambda rs:rs[-1]['report'].pop('variables'))
    reject_certificate('removed other seconds field',lambda rs:rs[0].pop('seconds'))
    reject_certificate('changed operation integer to boolean',lambda rs:rs[0].update(operation_count=True))
    reject_certificate('changed operation integer to float',lambda rs:rs[0].update(operation_count=1.0))
    for label,raw_text in [('duplicate JSON key',b'{"kind":"initial","x":1,"x":2}\n{"kind":"final","report":{}}\n'),
                           ('nonfinite JSON number',b'{"kind":"initial","x":NaN}\n{"kind":"final","report":{}}\n')]:
        raw=gzip.compress(raw_text,mtime=0)
        try:compare_reproduced_certificate(frozen,raw,hashlib.sha256(raw).hexdigest())
        except ValueError:tests.append(label)
        else:raise AssertionError('Accepted malformed certificate: '+label)
    from verify_handoff import BASELINE_BYTES, BASELINE_SHA, verify
    r,o,p=fixtures()
    helpers=('verify_handoff.py','release_config.py','legacy_verify_handoff_v2.py')
    for helper in helpers:o['handoff/'+helper]=('helper fixture '+helper).encode()
    commit='a'*40
    baseline=dict(filename='z-in-q-research-handoff-2026-11-04-r2.zip',bytes=BASELINE_BYTES,
                  sha256=BASELINE_SHA,url='https://example.invalid/baseline')
    entries={'current/'+name:raw for name,raw in o.items()}
    plan=dict(format='quartic-handoff-plan/v2',snapshot_commit=commit,release=r,verification_receipt=p,
              files=[dict(kind='git',path=name,archive_path='current/'+name,git_blob='b'*40,
                          bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for name,raw in o.items()],
              baseline=baseline)
    state=generated_state(plan,False)
    entries['PLAN.json']=encode(plan);entries['CURRENT_STATE.json']=encode(state)
    entries['START_HERE.md']=generated_start(plan,False)
    for helper in helpers:entries[helper]=o['handoff/'+helper]
    def archive(path,contents):
        inventory={name:dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()) for name,raw in contents.items()}
        manifest=dict(format='quartic-public-handoff/v2',snapshot_commit=commit,files=inventory,
                      current_files=list(o),baseline=dict(**baseline,included=False,
                      archive_path='baseline/'+baseline['filename']),history_scope=state['selected_history'])
        with zipfile.ZipFile(path,'w') as target:
            for name,raw in contents.items():target.writestr(name,raw)
            target.writestr('MANIFEST.json',encode(manifest))
    with tempfile.TemporaryDirectory(prefix='handoff-v3-fixture-') as temp:
        path=Path(temp)/'small.zip';archive(path,entries)
        assert verify(path,hashlib.sha256(entries['PLAN.json']).hexdigest())['status']=='PASS'
        digest=hashlib.sha256(entries['PLAN.json']).hexdigest()
        mutations=[('stale generated current state','CURRENT_STATE.json',encode(dict(state,variables=12504)),'Stale current-state'),
                   ('unplanned root entry','extra.py',b'extra','Unplanned'),
                   ('unplanned history entry','history/extra.md',b'extra','Unplanned'),
                   ('altered generated helper','verify_handoff.py',b'changed','Generated helper'),
                   ('altered generated guide','START_HERE.md',b'changed','Generated guide')]
        for label,name,raw,expected_error in mutations:
            bad=dict(entries);bad[name]=raw;archive(path,bad)
            try:verify(path,digest)
            except ValueError as error:
                assert expected_error in str(error),(label,str(error))
                tests.append(label)
            else:raise AssertionError('Accepted malformed authenticated-plan archive: '+label)
    return tests

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions required')
    print(json.dumps(dict(status='PASS',cases=run_tests()),indent=2))
