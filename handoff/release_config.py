"""Validate release-specific metadata against the exact current artifact."""
from datetime import date
import gzip
import hashlib
import io
import json
from pathlib import PurePosixPath
import re

PROOF_FILES = {'polynomial.expanded.txt','verify_certificate.py','certificate.jsonl.gz',
               'source-residuals.jsonl.gz','source-entry.json','source-audit.json','construction-map.json'}
METRICS = {'variables','witnesses','rows','monomials','degree','max_abs_coefficient','expanded_sha256'}

def relative(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name:
        raise ValueError('Unsafe release path')
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ('','.','..') for part in name.split('/')):
        raise ValueError('Unsafe release path')
    return name

def validate_release(release):
    if release.get('version') == 5:
        return validate_release_v5(release)
    if release.get('format') != 'quartic-handoff-release/v1':
        raise ValueError('Wrong release metadata format')
    version = release['version']; expected = release['expected']; count = expected['variables']
    if type(version) is not int or version != 4 or type(count) is not int or count != 4973 or release['date'] != '2026-11-06':
        raise ValueError('This packet requires Version 4, 4973 total variables, and date 2026-11-06')
    if set(expected) != METRICS or expected['witnesses'] != count-1 or expected['degree'] != 4:
        raise ValueError('Inconsistent release counts')
    for key in METRICS-{'expanded_sha256'}:
        if type(expected[key]) is not int or expected[key] <= 0:
            raise ValueError('Invalid release metric: '+key)
    if expected['max_abs_coefficient'] >= 2**80:
        raise ValueError('Release coefficient exceeds bound')
    date.fromisoformat(release['date'])
    relative(release['verification'])
    required = {'manuscript':f'quartic_{count}.tex','pdf':f'quartic_{count}.pdf',
                'package':f'quartics/quartic-{count}','inventory':f'docs/quartic-{count}/README.md',
                'replayed_certificate':f'docs/quartic-{count}-validation/replayed-certificate.jsonl.gz',
                'release_tag':f'quartic-{count}-version-{version}'}
    for key,value in required.items():
        if release[key] != value:
            raise ValueError('Stale release name: '+key)
        relative(value)
    if release['assets'] != {'full':f'z-in-q-version{version}-full-handoff.zip',
                            'current':f'z-in-q-version{version}-current-handoff.zip'}:
        raise ValueError('Stale handoff asset names')
    pins = release['proof_pins']
    if set(pins) != PROOF_FILES or any(not re.fullmatch('[0-9a-f]{64}',s) for s in pins.values()):
        raise ValueError('Incomplete release proof pins')
    if pins['polynomial.expanded.txt'] != expected['expanded_sha256']:
        raise ValueError('Inconsistent expanded polynomial pin')
    if not isinstance(release['source_id'],str) or not release['source_id']:
        raise ValueError('Missing source identifier')
    contract = release['source_contract']
    if contract != {'ordinary_contacts': 37, 'full_comparisons': 13, 'beta_only_comparisons': 8, 'height_exponent': 19, 'high_precision': 40, 'beta_precision': 12, 'anchor_squarings': 25, 'scalar_orders': [1, 1, 1, 1, 32, 32], 'lucas_only_comparisons': 16, 'root_carrier': 'general_E_mixed', 'comparison_target_multiplier': 2, 'direct_tangent_doublings': 4, 'first_norm_instances': 37, 'first_norm_virtual_denominator_exponent': 1, 'shared_square_fields': 37}:
        raise ValueError('Wrong Version 4 source contract')
    if release['next_release'] != {'version': 5, 'total_variable_upper_bound': 2486, 'total_includes_input': True, 'status': 'Research target only; Version 4 remains the fixed 4973-variable release'}:
        raise ValueError('Wrong future-release threshold')
    return release

def certificate_without_final_seconds(raw):
    """Decode exactly, discarding only the final record's report.seconds slot."""
    if len(raw)>50_000_000:
        raise ValueError('Compressed certificate exceeds bound')
    with gzip.GzipFile(fileobj=io.BytesIO(raw),mode='rb') as stream:
        decoded=stream.read(150_000_001)
    if len(decoded)>150_000_000:
        raise ValueError('Decoded certificate exceeds bound')
    def unique_object(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('Duplicate certificate JSON key')
            result[key]=value
        return result
    def bad_constant(value):
        raise ValueError('Nonfinite certificate JSON number')
    records=[json.loads(line,object_pairs_hook=unique_object,parse_constant=bad_constant)
             for line in decoded.splitlines()]
    if not records or any(not isinstance(item,dict) or not isinstance(item.get('kind'),str) for item in records):
        raise ValueError('Invalid certificate record structure')
    finals=[i for i,item in enumerate(records) if item['kind']=='final']
    if finals != [len(records)-1] or not isinstance(records[-1].get('report'),dict):
        raise ValueError('Certificate must have one final report at the end')
    records[-1]['report'].pop('seconds',None)
    # Canonical JSON preserves numeric types, unlike Python's True == 1 == 1.0.
    return json.dumps(records,sort_keys=True,separators=(',',':'),allow_nan=False)

def compare_reproduced_certificate(frozen,regenerated,expected_regenerated_sha):
    if not isinstance(expected_regenerated_sha,str) or not re.fullmatch('[0-9a-f]{64}',expected_regenerated_sha):
        raise ValueError('Invalid regenerated certificate hash')
    if hashlib.sha256(regenerated).hexdigest()!=expected_regenerated_sha:
        raise ValueError('Regenerated certificate bytes differ from reproduction receipt')
    if certificate_without_final_seconds(frozen)!=certificate_without_final_seconds(regenerated):
        raise ValueError('Certificates differ outside final.report.seconds')

def validate_current(read, names, release, receipt_path):
    """read takes a repository-relative name; names is the full Git inventory."""
    if release.get('version') == 5:
        return validate_current_v5(read, names, release, receipt_path)
    validate_release(release); root = release['package']+'/'
    receipt_path = relative(receipt_path)
    required = {release['manuscript'],release['pdf'],release['inventory'],receipt_path,release['replayed_certificate'],
                root+'reproducibility/manifest.json',root+release['verification'],'handoff/release.json'}
    if not required <= set(names):
        raise ValueError('Missing current snapshot files: '+repr(sorted(required-set(names))))
    if json.loads(read('handoff/release.json')) != release:
        raise ValueError('Release metadata is not the committed metadata')
    if not read(release['pdf']).startswith(b'%PDF'):
        raise ValueError('Current PDF is not a PDF')
    if ('Version '+str(release['version'])).encode() not in read(release['manuscript']):
        raise ValueError('Missing current manuscript version')
    for name,digest in release['proof_pins'].items():
        if hashlib.sha256(read(root+name)).hexdigest() != digest:
            raise ValueError('Wrong current proof artifact: '+name)
    entry = json.loads(read(root+'source-entry.json'))
    if entry['source_id'] != release['source_id'] or entry['source_sha256'] != release['proof_pins']['source-residuals.jsonl.gz']:
        raise ValueError('Wrong current source entry')
    for name,digest in entry['inspected_files_sha256'].items():
        if hashlib.sha256(read(root+'source/'+relative(name))).hexdigest() != digest:
            raise ValueError('Incomplete pinned source package: '+name)
    package_raw = read(root+'reproducibility/manifest.json')
    package = json.loads(package_raw)
    for name,record in package['files'].items():
        raw = read(root+relative(name))
        if record != {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}:
            raise ValueError('Incomplete reproducibility package: '+name)
    for key,value in release['expected'].items():
        if package['expected'][key] != value:
            raise ValueError('Stale reproducibility expectation: '+key)
    verification = json.loads(read(root+release['verification']))
    receipt = json.loads(read(receipt_path))
    if verification['status'] != 'PASS' or receipt.get('status') != 'PASS' or receipt.get('mandatory_status') != 'PASS: FRESH SOURCE AND EXACT FROZEN CERTIFICATE REPLAY':
        raise ValueError('Current verification or fresh reproduction did not pass')
    if receipt['source_id'] != release['source_id']:
        raise ValueError('Wrong reproduction source')
    for report in (verification,receipt['final_verification']):
        if report['source_id'] != release['source_id'] or report['source_sha256'] != release['proof_pins']['source-residuals.jsonl.gz']:
            raise ValueError('Wrong verified source')
        if report['checker_sha256'] != release['proof_pins']['verify_certificate.py']:
            raise ValueError('Wrong verified checker')
        for key,value in release['expected'].items():
            if report[key] != value or receipt['expected'][key] != value:
                raise ValueError('Stale verified count or digest: '+key)
    if receipt['expected']['certificate_sha256'] != release['proof_pins']['certificate.jsonl.gz']:
        raise ValueError('Reproduction expectation differs from frozen certificate pin')
    replayed=read(release['replayed_certificate'])
    if replayed != read(root+'certificate.jsonl.gz') or hashlib.sha256(replayed).hexdigest() != receipt['final_verification']['certificate_sha256']:
        raise ValueError('Replayed certificate differs from exact frozen certificate')
    steps=receipt.get('steps',[])
    if not steps or any(type(s.get('exit_code')) is not int or s.get('timeout') or s.get('memory_abort') or
                        (s['exit_code'] <= 0 if s.get('expected_rejection') else s['exit_code'] != 0) for s in steps):
        raise ValueError('Missing or incomplete reproduction stages')
    if receipt['package_manifest_sha256'] != hashlib.sha256(package_raw).hexdigest():
        raise ValueError('Reproduction receipt belongs to another package manifest')
    return verification

def generated_state(plan,included):
    release=validate_release(plan['release'])
    return dict(manuscript='Version '+str(release['version']),date=release['date'],
        manuscript_path='current/'+release['manuscript'],pdf_path='current/'+release['pdf'],
        snapshot_commit=plan['snapshot_commit'],current_snapshot='Complete exact file tree of the recorded public commit',
        verification_receipt='current/'+plan['verification_receipt'],source_id=release['source_id'],
        source_contract=release['source_contract'],next_release=release.get('next_release'),**release['expected'],
        baseline_included=included,baseline=plan['baseline'],
        selected_history='Explicit project mathematical notes; raw private archives and conversations are not included',
        historical_filtering='Baseline retains its previously recorded filtering policy; no new baseline content audit is claimed')

def generated_start(plan,included):
    release=validate_release(plan['release']);baseline=plan['baseline']
    baseline_path='baseline/'+baseline['filename']
    current_note = ('The selected construction is the independently reconstructed 1,272-coordinate quartic. Its complete source, certificates, reviews and manifest are included. The Version 4 manuscript and package and the original construction remain available at their historical paths.'
                    if release['version'] == 5 else
                    'The selected three-mode, target-two, tangent, shared-square and first-norm source defines Version 4. Optional scalar/J0 fusion and unadopted alternatives remain historical research.')
    replay_path = ('README.md' if release['version'] == 5 else 'reproducibility/README.md')
    return f'''# Version {release['version']} public research handoff

Release date: {release['date']}.

Start with [the manuscript](current/{release['pdf']}), its [TeX](current/{release['manuscript']}),
the [quartic package](current/{release['package']}/README.md), and
[research notes](RESEARCH_NOTES.md). [COVERAGE.md](COVERAGE.md) explains included and omitted material.

The complete current snapshot is public commit `{plan['snapshot_commit']}`.
A later publication commit may add this archive's checksum or receipt; those
metadata additions cannot appear inside the archive they identify.

The historical public baseline is {'included unchanged at `'+baseline_path+'`' if included else 'NOT included in this current-only ZIP'}.
Its size is {baseline['bytes']:,} bytes and SHA-256 is `{baseline['sha256']}`.
Download: {baseline['url']}
The baseline's own `current/` directory means current at its historical date.
This archive includes only the public snapshot and explicitly selected project research.
{current_note}

Run `python verify_handoff.py PATH_TO_THIS_ZIP` to check every entry and the
complete payload inventory. Add `--extract NEW_DIRECTORY` to verify and extract
into a new directory. For the full handoff, extract the nested baseline separately
and use its own index and restoration script for historical paths.

First compare this ZIP's SHA-256 with the checksum obtained from the public
release. An embedded manifest alone does not authenticate its claimed Git origin.
Alternatively bind the plan with `--expected-plan-sha256 DIGEST`, using the
plan digest from the independently obtained release build receipt.

Archive integrity is separate from the mathematical and computational reviews.
The exact quartic replay and fresh reproduction instructions are in
`current/{release['package']}/{replay_path}`.
The main Lean theorem remains unproved; the retained helper sources do not change that status.
'''.encode('utf-8')


V5_METRICS = {'variables': 1272, 'witnesses': 1271, 'rows': 1229,
              'monomials': 48001, 'degree': 4, 'primitive_content': '1',
              'coefficient_height': '64*3^(2^28)'}
V5_CONTRACT = {'construction': 'Independent reconstruction of the displayed Brox direct-Lucas source',
               'original_missing_program_recovered': False,
               'coordinate_detector_orders': [1, 16, 52],
               'coordinate_detector_test_counts': [10, 2, 4],
               'scalar_orders': [1, 1, 1, 1, 32, 32],
               'fixed_parameter': 'S = 3^(2^27)', 'fixed_parameter_is_coordinate': False}
V5_CHECKS = ['package_integrity', 'build', 'source_inventory', 'source_semantics', 'source_oracle',
             'compiler_selftest', 'compile_direct', 'compile_translated', 'independent_certificate_checks',
             'independent_identity_checks', 'independent_table_checks', 'optimization_checks',
             'checker_review_probes', 'frozen_table_identity']
V5_PACKAGE_REQUIRED = {
    'README.md', 'reproduce.py', 'integrity.py', 'PROVENANCE.json',
    'builder/build_source.cjs', 'builder/raw-ir.json', 'builder/raw-translated-ir.json',
    'compiler/compile_ir.py', 'compiler/review_checker.cjs',
    'checker/checker.cjs', 'checker/run_all.cjs', 'checker/mutation_tests.cjs',
    'checker/FINAL_CHECK.json', 'checker/direct-check.json', 'checker/translated-check.json',
    'source-review/SOURCE_REVIEW.md', 'source-review/source_inventory.json',
    'source-review/build_inventory.py', 'source-review/check_builder_semantics.py',
    'oracle/check_oracle.py', 'identity/check_identity.py', 'identity/check_reconstructed_tables.py',
    'optimization/verify_optimization.py', 'sources/SOURCES.json',
    'sources/diophantine_optimization_20261106_v3.tex',
} | {'compiler/'+stage+'/'+name for stage in ('direct', 'translated')
     for name in ('compiled-ir.json', 'reduction-certificate.json', 'coordinate-map.json', 'polynomial.json')}


def validate_release_v5(release):
    if release.get('format') != 'quartic-handoff-release/v2' or release.get('date') != '2026-11-06':
        raise ValueError('Wrong Version 5 descriptor format or date')
    required = {'version': 5, 'release_tag': 'quartic-1272-version-5',
                'manuscript': 'quartic_1272.tex', 'pdf': 'quartic_1272.pdf',
                'package': 'quartics/quartic-1272', 'inventory': 'docs/quartic-1272/README.md',
                'source_id': 'brox-direct-lucas-independent-reconstruction-1272',
                'package_manifest': 'MANIFEST.json',
                'polynomial': 'compiler/translated/polynomial.json'}
    if any(release.get(k) != v for k, v in required.items()):
        raise ValueError('Wrong Version 5 release paths or identity')
    if release.get('assets') != {'full': 'z-in-q-version5-full-handoff.zip',
                                  'current': 'z-in-q-version5-current-handoff.zip'}:
        raise ValueError('Wrong Version 5 asset names')
    if release.get('expected') != V5_METRICS or release.get('source_contract') != V5_CONTRACT:
        raise ValueError('Wrong Version 5 expected metrics or source contract')
    for field in ('snapshot_pins', 'preserved_pins'):
        if not isinstance(release.get(field), dict) or not release[field]:
            raise ValueError('Missing Version 5 file pins: '+field)
        for name, record in release[field].items():
            relative(name)
            if (set(record) != {'bytes', 'sha256'} or type(record['bytes']) is not int or record['bytes'] < 0 or
                    not isinstance(record['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', record['sha256'])):
                raise ValueError('Malformed Version 5 file pin')
    relative(release['verification_receipt'])
    overrides = release.get('preserved_editorial_overrides', {})
    if not isinstance(overrides, dict) or set(overrides) - {'October 11 Manuscript/README.md'}:
        raise ValueError('Unexpected historical editorial override')
    for name, change in overrides.items():
        if (change.get('before') != release['preserved_pins'].get(name) or
                change.get('reason') != 'User-requested full given name in project credit; no mathematical change' or
                set(change.get('after', {})) != {'bytes', 'sha256'} or
                type(change['after'].get('bytes')) is not int or change['after']['bytes'] < 0 or
                not isinstance(change['after'].get('sha256'), str) or
                not re.fullmatch('[0-9a-f]{64}', change['after']['sha256'])):
            raise ValueError('Invalid historical credit correction record')
    if not re.fullmatch('[0-9a-f]{64}', release.get('polynomial_sha256', '')):
        raise ValueError('Missing Version 5 polynomial hash')
    return release


def validate_current_v5(read, names, release, receipt_path):
    validate_release_v5(release)
    names = set(names)
    root = release['package']+'/'
    if receipt_path != release['verification_receipt']:
        raise ValueError('Version 5 replay receipt path differs from descriptor')
    if json.loads(read('handoff/release.json')) != release:
        raise ValueError('Release metadata is not the committed metadata')
    pins = release['snapshot_pins']
    required = {release['manuscript'], release['pdf'], release['inventory'], receipt_path,
                root+'MANIFEST.json', root+'reproduce.py', root+'README.md',
                root+'PROVENANCE.json', root+'checker/FINAL_CHECK.json',
                root+'checker/translated-check.json', root+'checker/direct-check.json',
                root+release['polynomial']}
    required |= {root+name for name in V5_PACKAGE_REQUIRED}
    if not required <= set(pins) or not set(pins) <= names:
        raise ValueError('Missing pinned Version 5 artifacts')
    package_names = {name for name in names if name.startswith(root)}
    if package_names != {name for name in pins if name.startswith(root)}:
        raise ValueError('Version 5 package differs from exact pinned inventory')
    inventory_names = {name for name in names if name.startswith('docs/quartic-1272/')}
    if inventory_names != {name for name in pins if name.startswith('docs/quartic-1272/')}:
        raise ValueError('Version 5 published inventory differs from descriptor')
    for mapping in (pins, release['preserved_pins']):
        for name, expected in mapping.items():
            if mapping is release['preserved_pins'] and name in release.get('preserved_editorial_overrides', {}):
                expected = release['preserved_editorial_overrides'][name]['after']
            if name not in names:
                raise ValueError('Missing preserved or current artifact: '+name)
            raw = read(name)
            if expected != {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}:
                raise ValueError('Pinned artifact changed: '+name)
    if not read(release['pdf']).startswith(b'%PDF') or b'Version 5' not in read(release['manuscript']):
        raise ValueError('Missing Version 5 manuscript or PDF')
    manifest_raw = read(root+'MANIFEST.json')
    manifest = json.loads(manifest_raw)
    if manifest.get('schema') != 'quartic-1272-package-manifest-v1':
        raise ValueError('Wrong Version 5 package manifest schema')
    if manifest.get('polynomial') != {'path': release['polynomial'], 'sha256': release['polynomial_sha256']}:
        raise ValueError('Wrong primary polynomial in Version 5 package manifest')
    expected_files = {}
    for entry in manifest['files']:
        name = relative(entry['path'])
        if name in expected_files:
            raise ValueError('Duplicate Version 5 package manifest entry')
        expected_files[name] = {'bytes': entry['bytes'], 'sha256': entry['sha256']}
    if set(expected_files) != {n[len(root):] for n in package_names if n != root+'MANIFEST.json'}:
        raise ValueError('Incomplete Version 5 package manifest')
    for name, record in expected_files.items():
        if record != pins[root+name]:
            raise ValueError('Version 5 manifest pin mismatch: '+name)
    polynomial_hash = hashlib.sha256(read(root+release['polynomial'])).hexdigest()
    if polynomial_hash != release['polynomial_sha256']:
        raise ValueError('Wrong Version 5 polynomial')
    receipt = json.loads(read(receipt_path))
    validate_reproduction_v5(receipt, hashlib.sha256(manifest_raw).hexdigest(), polynomial_hash)
    return receipt


def validate_reproduction_v5(receipt, manifest_hash, polynomial_hash):
    if receipt.get('schema') != 'quartic-1272-reproduction-v1' or receipt.get('status') != 'PASS':
        raise ValueError('Version 5 fresh reproduction did not pass')
    if receipt.get('packageManifestSha256') != manifest_hash:
        raise ValueError('Version 5 replay belongs to another package')
    if (receipt.get('frozenPolynomialSha256') != polynomial_hash or receipt.get('rebuiltPolynomialSha256') != polynomial_hash or
            receipt.get('byteIdentical') is not True):
        raise ValueError('Version 5 exact polynomial replay did not pass')
    expected_result = {'variablesIncludingInput': 1272, 'existentialWitnesses': 1271, 'degree': 4,
                       'monomials': 48001, 'quadraticResiduals': 1229, 'primitiveContent': '1',
                       'height': '64*3^(2^28)'}
    if receipt.get('result') != expected_result:
        raise ValueError('Version 5 reproduction metrics differ')
    checks = receipt.get('checks')
    if (not isinstance(checks, list) or [c.get('name') for c in checks] != V5_CHECKS or
            any(c.get('status') != 'PASS' for c in checks)):
        raise ValueError('Version 5 replay checks incomplete')
    return receipt
