"""Rebuild and independently check the complete 1272-variable coefficient table.

Python 3.10+ and Node.js 18+ are required. Only standard libraries are used.
The output directory must be empty; no shipped package file is overwritten.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
from integrity import POLYNOMIAL, POLYNOMIAL_SHA256, assert_serialization, sha256, verify

HERE = Path(__file__).resolve().parent
REQUIRED_CHECKS = [
    'package_integrity', 'build', 'source_inventory', 'source_semantics', 'source_oracle',
    'compiler_selftest', 'compile_direct', 'compile_translated',
    'independent_certificate_checks', 'independent_identity_checks',
    'independent_table_checks', 'optimization_checks', 'checker_review_probes',
    'frozen_table_identity',
]
RESULT = {'variablesIncludingInput': 1272, 'existentialWitnesses': 1271, 'degree': 4,
          'monomials': 48001, 'quadraticResiduals': 1229, 'primitiveContent': '1',
          'height': '64*3^(2^28)'}


def portable_receipts(root):
    """Report paths are provenance labels, not arithmetic. Store them relatively."""
    def clean(value):
        if isinstance(value, str):
            for prefix in (str(root) + os.sep, root.as_posix() + '/'):
                if value.startswith(prefix):
                    return value[len(prefix):].replace('\\', '/')
            return value
        if isinstance(value, list): return [clean(x) for x in value]
        if isinstance(value, dict): return {k: clean(v) for k, v in value.items()}
        return value
    for relative in ('checker/FINAL_CHECK.json', 'checker/direct-check.json', 'checker/translated-check.json'):
        path = root / relative
        value = json.loads(path.read_text(encoding='utf-8'))
        path.write_text(json.dumps(clean(value), indent=2) + '\n', encoding='utf-8', newline='\n')


def pipeline(root, logs, node):
    """Run only on an isolated copy, or on an unpublished package being prepared."""
    logs.mkdir(parents=True, exist_ok=True)
    checks = []
    stable = ['builder/raw-ir.json', 'builder/raw-translated-ir.json', 'source-review/source_inventory.json']
    stable += ['compiler/' + stage + '/' + name for stage in ('direct', 'translated')
               for name in ('compiled-ir.json', 'reduction-certificate.json', 'coordinate-map.json', 'polynomial.json')]
    before = {name: sha256(root / name) for name in stable if (root / name).exists()}

    def run(name, command):
        start = time.monotonic()
        process = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, encoding='utf-8', errors='replace',
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        log = logs / (name + '.log')
        log.write_text(process.stdout, encoding='utf-8', newline='\n')
        checks.append({'name': name, 'status': 'PASS' if process.returncode == 0 else 'FAIL',
                       'seconds': round(time.monotonic() - start, 3), 'log': 'logs/' + log.name})
        print(name + ': ' + checks[-1]['status'], flush=True)
        if process.returncode:
            raise RuntimeError(f'{name} failed; inspect {log}')

    py = sys.executable
    run('build', [node, 'builder/build_source.cjs'])
    run('source_inventory', [py, 'source-review/build_inventory.py'])
    run('source_semantics', [py, 'source-review/check_builder_semantics.py'])
    run('source_oracle', [py, 'oracle/check_oracle.py'])
    run('compiler_selftest', [py, 'compiler/compile_ir.py', '--self-test'])
    for stage, raw in [('direct', 'raw-ir.json'), ('translated', 'raw-translated-ir.json')]:
        run('compile_' + stage, [py, 'compiler/compile_ir.py', 'builder/' + raw, 'compiler/' + stage])
    run('independent_certificate_checks', [node, 'checker/run_all.cjs'])
    run('independent_identity_checks', [py, 'identity/check_identity.py'])
    run('independent_table_checks', [py, 'identity/check_reconstructed_tables.py'])
    run('optimization_checks', [py, 'optimization/verify_optimization.py'])
    run('checker_review_probes', [node, 'compiler/review_checker.cjs'])
    for name, expected in before.items():
        if sha256(root / name) != expected:
            raise RuntimeError('Rebuilt frozen artifact differs: ' + name)
    if sha256(root / POLYNOMIAL) != POLYNOMIAL_SHA256:
        raise RuntimeError('Rebuilt coefficient table differs from the pinned polynomial')
    check = json.loads((root / 'checker/translated-check.json').read_text(encoding='utf-8'))
    stats = check['statistics']
    expected = {'degree': 4, 'activeCoordinateCount': 1272, 'monomials': 48001,
                'primitiveContent': '1', 'integerCoefficients': True, 'specializedSupportCertified': True}
    if check['coordinateCount'] != 1272 or check['residualCount'] != 1229 or check['gateIdentities']['checked'] != 1214:
        raise RuntimeError('Verified construction counts differ')
    if any(stats.get(k) != v for k, v in expected.items()):
        raise RuntimeError('Verified coefficient statistics differ')
    if stats['maximumAbsoluteCoefficient']['coefficient'] != [{'sPower': 2, 'coefficient': '64/1'}]:
        raise RuntimeError('Verified exact coefficient height differs')
    mutations = json.loads((root / 'checker/MUTATION_TESTS.json').read_text(encoding='utf-8'))
    if not mutations['allRejected'] or mutations['adversarialMutations'] < 36:
        raise RuntimeError('Expected mutation tests did not pass')
    probes = json.loads((root / 'compiler/checker-review-probes.json').read_text(encoding='utf-8'))
    if any(not p.get('matchesExpectation', p.get('rejected', False)) for p in probes['observations']):
        raise RuntimeError('Checker review probe failed')
    portable_receipts(root)
    assert_serialization(root)
    checks.append({'name': 'frozen_table_identity', 'status': 'PASS', 'seconds': 0,
                   'log': None, 'sha256': POLYNOMIAL_SHA256})
    return checks


def reproduce(output):
    start = time.monotonic()
    output = output.resolve()
    if output.is_relative_to(HERE):
        raise ValueError('Choose an output directory outside the shipped package')
    integrity = verify(HERE)
    node = shutil.which('node')
    if not node: raise RuntimeError('Node.js 18+ is required on PATH')
    node_version = subprocess.check_output([node, '--version'], text=True).strip()
    if int(node_version.lstrip('v').split('.')[0]) < 18:
        raise RuntimeError('Node.js 18+ is required')
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Choose an empty output directory; existing files are never overwritten')
    output.mkdir(parents=True, exist_ok=True)
    project = output / 'quartic-1272'
    project.mkdir()
    manifest = json.loads((HERE / 'MANIFEST.json').read_text(encoding='utf-8'))
    for name in [record['path'] for record in manifest['files']] + ['MANIFEST.json']:
        target = project / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / name, target)
    checks = [{'name': 'package_integrity', 'status': 'PASS', 'seconds': 0, 'log': None}]
    checks += pipeline(project, output / 'logs', node)
    if [check['name'] for check in checks] != REQUIRED_CHECKS:
        raise RuntimeError('Reproduction check inventory differs')
    record = {'schema': 'quartic-1272-reproduction-v1', 'status': 'PASS',
              'packageManifestSha256': integrity['packageManifestSha256'],
              'frozenPolynomialSha256': POLYNOMIAL_SHA256,
              'rebuiltPolynomialSha256': sha256(project / POLYNOMIAL), 'byteIdentical': True,
              'result': RESULT, 'checks': checks, 'requiredChecks': REQUIRED_CHECKS,
              'runtimes': {'python': sys.version.split()[0], 'node': node_version},
              'elapsedSeconds': round(time.monotonic() - start, 3),
              'scope': 'Complete finite reconstruction and coefficient verification. Source arithmetic theorems remain stated inputs; no Lean proof is asserted.'}
    (output / 'REPRODUCTION.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: record[k] for k in ('status', 'result', 'byteIdentical', 'elapsedSeconds')}, indent=2))
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='Empty output directory to retain all rebuilt artifacts and logs')
    args = parser.parse_args()
    if args.out:
        reproduce(args.out)
    else:
        with tempfile.TemporaryDirectory(prefix='quartic1272-') as directory:
            reproduce(Path(directory))
