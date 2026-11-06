"""Freeze historical file pins, then prepare Version 5 metadata after replay.

Neither command builds archives, publishes anything, or edits the mathematical
package. Run descriptor only after the manuscript, package and receipt are final.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from release_config import V5_CONTRACT, V5_METRICS, relative, validate_current


def record(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def encode(data):
    return (json.dumps(data, sort_keys=True, indent=2)+'\n').encode()


def freeze_history(repo, commit, output):
    if output.exists():
        raise ValueError('Historical pin file already exists; do not overwrite it')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args])
    commit = git('rev-parse', '--verify', commit+'^{commit}').decode().strip()
    files = {}
    for entry in git('ls-tree', '-r', '-z', '--full-tree', commit).split(b'\0'):
        if not entry:
            continue
        header, path = entry.split(b'\t', 1)
        name = path.decode()
        if (name.startswith(('quartics/', 'degree8-original/', 'construction/', 'October 11 Manuscript/')) or
                name in ('quartic_4973.tex', 'quartic_4973.pdf', 'quartic_9625.tex', 'quartic_9625.pdf',
                         'quartic_12504.tex', 'quartic_12504.pdf')):
            mode, kind, oid = header.decode().split()
            if mode not in ('100644', '100755') or kind != 'blob':
                raise ValueError('Historical member is not regular: '+name)
            files[relative(name)] = record(git('cat-file', 'blob', oid))
    if not {'quartic_4973.tex', 'quartic_4973.pdf'} <= set(files):
        raise ValueError('Wrong historical snapshot')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encode({'schema': 'quartic-v4-preserved-files-v1', 'commit': commit, 'files': files}))
    return {'status': 'HISTORICAL PINS FROZEN', 'commit': commit, 'files': len(files), **record(output.read_bytes())}


def descriptor(repo, receipt, preserved, output):
    receipt = relative(receipt)
    roots = ('quartics/quartic-1272', 'docs/quartic-1272', 'handoff/releases/version5',
             'docs/quartic-1272-validation')
    pins = {}
    for root in roots:
        directory = repo/root
        if root == 'docs/quartic-1272-validation' and not directory.exists():
            continue
        if not directory.is_dir():
            raise ValueError('Required package or inventory is missing: '+root)
        for path in sorted(directory.rglob('*')):
            if path.is_symlink():
                raise ValueError('Symlink in new package')
            if path.is_file():
                name = path.relative_to(repo).as_posix()
                if set(path.parts) & {'__pycache__', '.pytest_cache', 'replay-output', 'replay-tmp', '.git'}:
                    raise ValueError('Generated cache or replay directory in new package: '+name)
                pins[name] = record(path.read_bytes())
    for name in ('quartic_1272.tex', 'quartic_1272.pdf', 'scripts/check_quartic1272.py', receipt):
        pins[name] = record((repo/name).read_bytes())
    old = json.loads(preserved.read_bytes())
    if old['schema'] != 'quartic-v4-preserved-files-v1':
        raise ValueError('Wrong historical pin schema')
    overrides = {}
    for name, original in old['files'].items():
        raw = (repo/name).read_bytes()
        if record(raw) == original:
            continue
        if name != 'October 11 Manuscript/README.md':
            raise ValueError('Unapproved change to preserved historical file: '+name)
        before = subprocess.check_output(['git', '-C', str(repo), 'show', old['commit']+':'+name])
        if record(before) != original or before.replace(b'Jenn'+b' Park', b'Jennifer Park') != raw:
            raise ValueError('Historical editorial change is not the requested credit correction')
        overrides[name] = {'before': original, 'after': record(raw),
                           'reason': 'User-requested full given name in project credit; no mathematical change'}
    release = {'format': 'quartic-handoff-release/v2', 'version': 5, 'date': '2026-11-06',
               'release_tag': 'quartic-1272-version-5',
               'assets': {'full': 'z-in-q-version5-full-handoff.zip', 'current': 'z-in-q-version5-current-handoff.zip'},
               'manuscript': 'quartic_1272.tex', 'pdf': 'quartic_1272.pdf', 'package': roots[0],
               'inventory': 'docs/quartic-1272/README.md', 'package_manifest': 'MANIFEST.json',
               'verification_receipt': receipt, 'polynomial': 'compiler/translated/polynomial.json',
               'polynomial_sha256': pins[roots[0]+'/compiler/translated/polynomial.json']['sha256'],
               'source_id': 'brox-direct-lucas-independent-reconstruction-1272',
               'source_contract': V5_CONTRACT, 'expected': V5_METRICS,
               'snapshot_pins': pins, 'preserved_pins': old['files'], 'preserved_commit': old['commit'],
               'preserved_editorial_overrides': overrides}
    names = {p.relative_to(repo).as_posix() for p in repo.rglob('*') if p.is_file()}
    raw = encode(release)
    def read(name):
        return raw if name == 'handoff/release.json' else (repo/name).read_bytes()
    validate_current(read, names, release, receipt)
    output.write_bytes(raw)
    return {'status': 'VERSION 5 DESCRIPTOR PREPARED; ARCHIVES NOT BUILT',
            'pinnedCurrentFiles': len(pins), 'preservedFiles': len(old['files']), **record(raw)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    commands = parser.add_subparsers(dest='command', required=True)
    history = commands.add_parser('freeze-history')
    history.add_argument('--commit', required=True)
    history.add_argument('--output', type=Path)
    final = commands.add_parser('descriptor')
    final.add_argument('--receipt', required=True)
    final.add_argument('--preserved', type=Path)
    final.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    standard = repo/'handoff/releases/version4/PRESERVED_FILES.json'
    if args.command == 'freeze-history':
        result = freeze_history(repo, args.commit, args.output or standard)
    else:
        result = descriptor(repo, args.receipt, args.preserved or standard, args.output or repo/'handoff/release.json')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
