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
    if release.get('format') != 'quartic-handoff-release/v1':
        raise ValueError('Wrong release metadata format')
    version = release['version']; expected = release['expected']; count = expected['variables']
    if type(version) is not int or version != 3 or type(count) is not int or count != 9625 or release['date'] != '2026-11-06':
        raise ValueError('This packet requires Version 3, 9625 total variables, and date 2026-11-06')
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
                'regenerated_certificate':f'docs/quartic-{count}/verification/regenerated-certificate.jsonl.gz',
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
    if contract != dict(ordinary_contacts=37,full_comparisons=29,beta_only_comparisons=8,
                        height_exponent=19,high_precision=40,beta_precision=12,anchor_squarings=25,
                        scalar_orders=[1,1,1,1,32,32]):
        raise ValueError('Version 3 requires the accepted selective-beta source contract')
    if release['next_release'] != dict(version=4,strict_total_variable_upper_bound=5000,
            total_includes_input=True,status='Research target only; Version 3 remains the fixed 9625-variable release'):
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
    validate_release(release); root = release['package']+'/'
    receipt_path = relative(receipt_path)
    required = {release['manuscript'],release['pdf'],release['inventory'],receipt_path,release['regenerated_certificate'],
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
    if verification['status'] != 'PASS' or receipt['status'] != 'PASS: FROZEN REPLAY AND CLEAN REPRODUCTION':
        raise ValueError('Current verification or fresh reproduction did not pass')
    for report in (verification,receipt):
        if report['source_id'] != release['source_id'] or report['source_sha256'] != release['proof_pins']['source-residuals.jsonl.gz']:
            raise ValueError('Wrong verified source')
        if report['checker_sha256'] != release['proof_pins']['verify_certificate.py']:
            raise ValueError('Wrong verified checker')
    for key,value in release['expected'].items():
        if verification[key] != value or receipt['expected'][key] != value:
            raise ValueError('Stale verified count or digest: '+key)
    if receipt['expected']['certificate_sha256'] != release['proof_pins']['certificate.jsonl.gz']:
        raise ValueError('Reproduction expectation differs from frozen certificate pin')
    compare_reproduced_certificate(read(root+'certificate.jsonl.gz'),read(release['regenerated_certificate']),
                                   receipt['regenerated_certificate_sha256'])
    if receipt['package_manifest_sha256'] != hashlib.sha256(package_raw).hexdigest():
        raise ValueError('Reproduction receipt belongs to another package manifest')
    return verification

def generated_state(plan,included):
    release=validate_release(plan['release'])
    return dict(manuscript='Version '+str(release['version']),date=release['date'],
        manuscript_path='current/'+release['manuscript'],pdf_path='current/'+release['pdf'],
        snapshot_commit=plan['snapshot_commit'],current_snapshot='Complete exact file tree of the recorded public commit',
        verification_receipt='current/'+plan['verification_receipt'],source_id=release['source_id'],
        source_contract=release['source_contract'],next_release=release['next_release'],**release['expected'],
        baseline_included=included,baseline=plan['baseline'],
        selected_history='Explicit project mathematical notes; raw private archives and conversations are not included',
        historical_filtering='Baseline retains its previously recorded filtering policy; no new baseline content audit is claimed')

def generated_start(plan,included):
    release=validate_release(plan['release']);baseline=plan['baseline']
    baseline_path='baseline/'+baseline['filename']
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
Three-mode, Jacobi and other separately labeled research do not define Version 3.

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
`current/{release['package']}/reproducibility/README.md`.
The main Lean theorem remains unproved; the retained helper sources do not change that status.
'''.encode('utf-8')
