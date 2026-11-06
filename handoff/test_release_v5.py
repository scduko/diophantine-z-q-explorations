"""Small adversarial Version 5 packaging tests; no arithmetic claim or archive build."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile

from release_config import (V5_CONTRACT, V5_METRICS, V5_CHECKS, V5_PACKAGE_REQUIRED,
                            validate_current, validate_release, generated_state, generated_start)


def encoded(value):
    return json.dumps(value, sort_keys=True).encode()


def record(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def fixture():
    root = 'quartics/quartic-1272/'
    package = {name: ('test fixture '+name).encode() for name in sorted(V5_PACKAGE_REQUIRED)}
    package['MANIFEST.json'] = encoded({'schema': 'quartic-1272-package-manifest-v1',
                                       'polynomial': {'path': 'compiler/translated/polynomial.json',
                                                      'sha256': record(package['compiler/translated/polynomial.json'])['sha256']},
                                       'files': [{'path': name, **record(raw)} for name, raw in package.items()]})
    objects = {root+name: raw for name, raw in package.items()}
    receipt = 'handoff/releases/version5/REPRODUCTION.json'
    polynomial = record(package['compiler/translated/polynomial.json'])['sha256']
    objects.update({'quartic_1272.tex': b'Version 5', 'quartic_1272.pdf': b'%PDF fixture',
                    'docs/quartic-1272/README.md': b'fixture inventory', 'quartic_4973.tex': b'preserved Version 4'})
    objects[receipt] = encoded({'schema': 'quartic-1272-reproduction-v1', 'status': 'PASS',
                                'packageManifestSha256': record(package['MANIFEST.json'])['sha256'],
                                'frozenPolynomialSha256': polynomial, 'rebuiltPolynomialSha256': polynomial,
                                'byteIdentical': True, 'result': {'variablesIncludingInput': 1272,
                                'existentialWitnesses': 1271, 'degree': 4, 'monomials': 48001,
                                'quadraticResiduals': 1229, 'primitiveContent': '1', 'height': '64*3^(2^28)'},
                                'checks': [{'name': name, 'status': 'PASS'} for name in V5_CHECKS]})
    release = {'format': 'quartic-handoff-release/v2', 'version': 5, 'date': '2026-11-06',
               'release_tag': 'quartic-1272-version-5',
               'assets': {'full': 'z-in-q-version5-full-handoff.zip', 'current': 'z-in-q-version5-current-handoff.zip'},
               'manuscript': 'quartic_1272.tex', 'pdf': 'quartic_1272.pdf', 'package': root[:-1],
               'inventory': 'docs/quartic-1272/README.md', 'source_id': 'brox-direct-lucas-independent-reconstruction-1272',
               'package_manifest': 'MANIFEST.json', 'polynomial': 'compiler/translated/polynomial.json',
               'polynomial_sha256': polynomial, 'source_contract': deepcopy(V5_CONTRACT),
               'expected': deepcopy(V5_METRICS), 'verification_receipt': receipt,
               'snapshot_pins': {name: record(raw) for name, raw in objects.items() if name != 'quartic_4973.tex'},
               'preserved_pins': {'quartic_4973.tex': record(objects['quartic_4973.tex'])}}
    objects['handoff/release.json'] = encoded(release)
    return release, objects, receipt


def run_tests():
    release, objects, receipt = fixture()
    validate_current(objects.__getitem__, set(objects), release, receipt)
    cases = []
    def reject(name, mutate, rebind=False):
        release, objects, receipt = fixture()
        mutate(release, objects, receipt)
        if rebind:
            release['snapshot_pins'] = {name: record(objects[name]) for name in release['snapshot_pins'] if name in objects}
            objects['handoff/release.json'] = encoded(release)
        try:
            validate_current(objects.__getitem__, set(objects), release, receipt)
        except (ValueError, KeyError):
            cases.append(name)
        else:
            raise AssertionError('Accepted invalid Version 5 fixture: '+name)
    def alter_receipt(objects, receipt, key, value):
        obj = json.loads(objects[receipt]); obj[key] = value; objects[receipt] = encoded(obj)
    reject('stale version asset', lambda r,o,p: r['assets'].update(current='z-in-q-version4-current-handoff.zip'))
    reject('wrong variable count', lambda r,o,p: r['expected'].update(variables=1315))
    reject('uncommitted descriptor', lambda r,o,p: o.update({'handoff/release.json': b'{}'}))
    reject('changed frozen table', lambda r,o,p: o.update({r['package']+'/'+r['polynomial']: b'changed'}))
    reject('changed preserved manuscript', lambda r,o,p: o.update({'quartic_4973.tex': b'changed'}))
    reject('missing package file', lambda r,o,p: o.pop(r['package']+'/reproduce.py'))
    reject('extra replay tree', lambda r,o,p: o.update({r['package']+'/replay-output/temporary.json': b'{}'}))
    reject('extra unpinned inventory file', lambda r,o,p: o.update({'docs/quartic-1272/extra.md': b'extra'}))
    reject('failed fresh reproduction', lambda r,o,p: alter_receipt(o,p,'status','FAIL'), True)
    reject('wrong replay package', lambda r,o,p: alter_receipt(o,p,'packageManifestSha256','0'*64), True)
    reject('wrong rebuilt table', lambda r,o,p: alter_receipt(o,p,'rebuiltPolynomialSha256','0'*64), True)
    reject('not byte-identical', lambda r,o,p: alter_receipt(o,p,'byteIdentical',False), True)
    reject('missing fresh checks', lambda r,o,p: alter_receipt(o,p,'checks',[]), True)
    reject('incomplete fresh checks', lambda r,o,p: alter_receipt(o,p,'checks',[{'name': V5_CHECKS[0], 'status':'PASS'}]), True)
    reject('failed fresh check', lambda r,o,p: alter_receipt(o,p,'checks',[{'name':'fixture','status':'FAIL'}]), True)
    reject('wrong metrics', lambda r,o,p: alter_receipt(o,p,'result',{}), True)
    reject('stale manuscript version', lambda r,o,p: o.update({'quartic_1272.tex': b'Version 4'}), True)
    reject('not a PDF', lambda r,o,p: o.update({'quartic_1272.pdf': b'plain text'}), True)
    reject('unexpected historical editorial override', lambda r,o,p: r.update(
        preserved_editorial_overrides={'quartic_4973.tex': {'before': r['preserved_pins']['quartic_4973.tex'],
            'after': record(b'changed'), 'reason': 'User-requested full given name in project credit; no mathematical change'}}))
    r, objects, receipt = fixture()
    name = 'October 11 Manuscript/README.md'
    before = ('Credit: '+'Jenn'+' Park').encode()
    objects[name] = b'Credit: Jennifer Park'
    r['preserved_pins'][name] = record(before)
    r['preserved_editorial_overrides'] = {name: {'before': record(before), 'after': record(objects[name]),
        'reason': 'User-requested full given name in project credit; no mathematical change'}}
    objects['handoff/release.json'] = encoded(r)
    validate_current(objects.__getitem__, set(objects), r, receipt)
    # Exercise the complete ZIP verification and extraction path with small
    # Version 5 metadata fixtures, including externally bound ZIP and plan hashes.
    from verify_handoff import BASELINE_BYTES, BASELINE_SHA, extract_verified
    r, objects, receipt = fixture()
    helpers = ('verify_handoff.py', 'release_config.py', 'legacy_verify_handoff_v2.py')
    for helper in helpers:
        objects['handoff/'+helper] = ('fixture helper '+helper).encode()
    baseline = {'filename': 'z-in-q-research-handoff-2026-11-04-r2.zip',
                'bytes': BASELINE_BYTES, 'sha256': BASELINE_SHA, 'url': 'https://example.invalid/baseline'}
    plan = {'format': 'quartic-handoff-plan/v2', 'snapshot_commit': 'a'*40,
            'release': r, 'verification_receipt': receipt, 'baseline': baseline,
            'files': [{'kind': 'git', 'path': name, 'archive_path': 'current/'+name,
                       'git_blob': 'b'*40, **record(raw)} for name, raw in objects.items()]}
    state = generated_state(plan, False)
    entries = {'current/'+name: raw for name, raw in objects.items()}
    entries.update({'PLAN.json': encoded(plan), 'CURRENT_STATE.json': encoded(state),
                    'START_HERE.md': generated_start(plan, False)})
    entries.update({helper: objects['handoff/'+helper] for helper in helpers})
    manifest = {'format': 'quartic-public-handoff/v2', 'snapshot_commit': plan['snapshot_commit'],
                'current_files': list(objects), 'files': {name: record(raw) for name, raw in entries.items()},
                'baseline': {**baseline, 'included': False, 'archive_path': 'baseline/'+baseline['filename']},
                'history_scope': state['selected_history']}
    with tempfile.TemporaryDirectory(prefix='v5-handoff-fixture-') as temporary:
        path = Path(temporary)/'current.zip'
        with zipfile.ZipFile(path, 'w') as archive:
            for name, raw in entries.items():
                archive.writestr(name, raw)
            archive.writestr('MANIFEST.json', encoded(manifest))
        result = extract_verified(path, Path(temporary)/'extracted',
                                  record(entries['PLAN.json'])['sha256'], record(path.read_bytes())['sha256'])
        assert result['status'] == 'PASS' and result['externally_bound_archive']
        assert (Path(temporary)/'extracted/current/quartic_1272.tex').read_bytes() == b'Version 5'
    return cases


if __name__ == '__main__':
    print(json.dumps({'status': 'PASS', 'scope': 'Small metadata fixtures only', 'cases': run_tests()}, indent=2))
