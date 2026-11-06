"""Check every shipped payload byte before executing reconstruction programs."""
from pathlib import Path, PurePosixPath
import hashlib
import json

HERE = Path(__file__).resolve().parent
POLYNOMIAL = 'compiler/translated/polynomial.json'
POLYNOMIAL_SHA256 = '02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586'
CRLF_JSON = {'polynomial.json', 'compiler/direct/polynomial.json', POLYNOMIAL}
LF_JSON = {
    'MANIFEST.json', 'PROVENANCE.json', 'sources/SOURCES.json', 'builder/FROZEN.json',
    'builder/raw-ir.json', 'builder/raw-translated-ir.json', 'builder/census.json',
    'source-review/source_inventory.json', 'source-review/builder_semantic_checks.json',
    'source-review/review_verdict.json', 'oracle/results.json',
    'compiler/checker-review-probes.json', 'checker/FINAL_CHECK.json',
    'checker/direct-check.json', 'checker/translated-check.json',
    'checker/ANCHOR_CHECK.json', 'checker/MUTATION_TESTS.json',
    'identity/anchor_certificate.json', 'identity/checks.json',
    'identity/reconstructed_table_checks.json', 'identity/source_receipts.json',
    'optimization/optimization-check.json',
}
LF_JSON.update('compiler/' + stage + '/' + name
               for stage in ('direct', 'translated')
               for name in ('compiled-ir.json', 'compiler-report.json', 'coordinate-map.json',
                            'reduction-certificate.json', 'specialization-certificate.json'))


def assert_serialization(root):
    """Check explicit line endings in addition to, never instead of, byte hashes."""
    for name in sorted(LF_JSON | CRLF_JSON):
        raw = (root / name).read_bytes()
        raw.decode('utf-8')
        if name in CRLF_JSON:
            remainder = raw.replace(b'\r\n', b'')
            valid = raw.endswith(b'\r\n') and b'\r' not in remainder and b'\n' not in remainder
        else:
            valid = raw.endswith(b'\n') and b'\r' not in raw
        if not valid:
            raise ValueError('Noncanonical JSON line endings: ' + name)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=HERE):
    root = root.resolve()
    manifest_path = root / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'quartic-1272-package-manifest-v1':
        raise ValueError('Unknown package manifest schema')
    names = set()
    for record in manifest['files']:
        name = record['path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or ':' in name or name in names:
            raise ValueError('Invalid or duplicate manifest path: ' + name)
        names.add(name)
        target = root.joinpath(*relative.parts)
        if target.is_symlink() or not target.resolve().is_relative_to(root) or not target.is_file():
            raise ValueError('Missing or symlinked package file: ' + name)
        if target.stat().st_size != record['bytes'] or sha256(target) != record['sha256']:
            raise ValueError('Package bytes differ: ' + name)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.relative_to(root).as_posix() != 'MANIFEST.json'}
    if actual != names:
        raise ValueError('Package file inventory differs: ' + repr(sorted(actual ^ names)))
    if POLYNOMIAL not in names or sha256(root / POLYNOMIAL) != POLYNOMIAL_SHA256:
        raise ValueError('Frozen 1272-variable polynomial hash differs')
    if 'polynomial.json' not in names or sha256(root / 'polynomial.json') != POLYNOMIAL_SHA256:
        raise ValueError('Top-level polynomial alias differs')
    sources = json.loads((root / 'sources/SOURCES.json').read_text(encoding='utf-8'))
    for entry in sources['files']:
        if sha256(root / 'sources' / entry['path']) != entry['sha256']:
            raise ValueError('Pinned mathematical source differs: ' + entry['path'])
    assert_serialization(root)
    return {'status': 'PASS', 'files': len(names), 'packageManifestSha256': sha256(manifest_path),
            'frozenPolynomialSha256': POLYNOMIAL_SHA256}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
