"""Authenticate and extract a Version 5 current ZIP, then replay its quartic.

All replay products stay in a separate new directory outside the extracted
snapshot. The historical baseline is not extracted or rebuilt.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from release_config import validate_reproduction_v5
from verify_handoff import extract_verified


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--expected-archive-sha256', required=True)
    parser.add_argument('--expected-plan-sha256', required=True)
    parser.add_argument('--extract', type=Path, required=True)
    parser.add_argument('--replay-output', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    destination = args.extract.resolve()
    replay = args.replay_output.resolve()
    if replay.is_relative_to(destination) or destination.is_relative_to(replay):
        raise ValueError('Replay output must be separate from the extracted snapshot')
    report_path = args.report.resolve()
    if report_path.is_relative_to(destination) or report_path.is_relative_to(replay):
        raise ValueError('Report and log must be outside the extracted snapshot and replay directory')
    if replay.exists() or args.report.exists():
        raise ValueError('Use new replay and report paths')
    # This preflight chooses the intended archive type. Full authentication is
    # still performed by extract_verified before any extraction takes place.
    with zipfile.ZipFile(args.archive) as archive:
        manifest = json.loads(archive.read('MANIFEST.json'))
        if manifest.get('baseline', {}).get('included') or 'current/quartics/quartic-1272/MANIFEST.json' not in archive.namelist():
            raise ValueError('Use the Version 5 current-only archive for this replay')
    archive_report = extract_verified(args.archive, destination, args.expected_plan_sha256, args.expected_archive_sha256)
    if archive_report['baseline_included']:
        raise ValueError('Use the current-only archive for this replay')
    current = destination/'current'
    package = current/'quartics/quartic-1272'
    command = [sys.executable, '-E', '-B', str(package/'reproduce.py'), '--out', str(replay)]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    log = args.report.with_suffix('.log')
    with log.open('x', encoding='utf-8') as output:
        result = subprocess.run(command, cwd=current, stdout=output, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError('Extracted package reproduction failed; see '+str(log))
    receipt_raw = (replay/'REPRODUCTION.json').read_bytes()
    receipt = json.loads(receipt_raw)
    manifest_hash = hashlib.sha256((package/'MANIFEST.json').read_bytes()).hexdigest()
    polynomial_hash = hashlib.sha256((package/'compiler/translated/polynomial.json').read_bytes()).hexdigest()
    validate_reproduction_v5(receipt, manifest_hash, polynomial_hash)
    report = {'schema': 'quartic-v5-handoff-extracted-replay-v1', 'status': 'PASS',
              'archive': archive_report, 'reproductionReceiptSha256': hashlib.sha256(receipt_raw).hexdigest(),
              'packageManifestSha256': manifest_hash, 'polynomialSha256': polynomial_hash,
              'replayOutsideExtractedSnapshot': True, 'checks': [c['name'] for c in receipt['checks']]}
    args.report.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
