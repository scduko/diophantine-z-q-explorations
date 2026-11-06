"""Check exact input binding without executing a checker or expanding a polynomial."""
if not __debug__:
    raise RuntimeError('Assertions required')

import ast
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

CORE_SHA256 = '0c118eb0d38178f34c40096b6ff84ab7136a6fde08b3ec7a5544ab339fd37b71'
ORIGINAL64 = dict(source_sha256='6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2',
                  source_variables=15672, source_rows=15107)
MAX_BYTES = 64*1024**2
ARTIFACT_FILES = ('candidate-rows.json.gz', 'certificate.jsonl.gz', 'polynomial.expanded.txt',
                  'polynomial.expanded.txt.gz', 'residuals.json.gz', 'source-residuals.jsonl.gz',
                  'variable-map.json', 'weights.json')
COUNT_KEYS = ('variables', 'witnesses', 'rows', 'monomials', 'degree', 'max_abs_coefficient')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pinned(path, expected):
    assert re.fullmatch('[0-9a-f]{64}', expected), 'Use a lowercase full SHA-256'
    assert path.is_file() and not path.is_symlink(), str(path)
    assert sha(path) == expected, ('SHA-256 mismatch', str(path))


def read(path):
    assert path.stat().st_size <= MAX_BYTES, ('Input too large', str(path))
    return path.read_bytes()


def ungzip(path):
    with gzip.open(path, 'rb') as stream:
        data = stream.read(MAX_BYTES+1)
    assert len(data) <= MAX_BYTES, ('Decompressed input too large', str(path))
    return data


def registry(path):
    content = read(path).decode('utf-8')
    content = content.replace('\r\n', '\n')
    nodes = [node for node in ast.parse(content).body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == 'SOURCE_ENTRIES' for target in node.targets)]
    assert len(nodes) == 1, 'Expected one source registry'
    node = nodes[0]
    assert len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'SOURCE_ENTRIES', 'Registry must have exactly one assignment target'
    lines = content.splitlines(keepends=True)
    span = ''.join(lines[node.lineno-1:node.end_lineno])
    assert span.strip() == ast.get_source_segment(content, node), 'Registry lines contain content outside the assignment'
    core = ''.join(lines[:node.lineno-1]+['SOURCE_ENTRIES = PINNED_REGISTRY\n']+lines[node.end_lineno:])
    assert hashlib.sha256(core.encode()).hexdigest() == CORE_SHA256, 'Unreviewed checker core'
    result = ast.literal_eval(node.value)
    assert result['original64'] == ORIGINAL64, 'Changed historical source entry'
    return result


def validate_kit(root):
    manifest = json.loads(read(root/'KIT_MANIFEST.json'))
    assert manifest['format'] == 'reusable-elimination-kit-v1'
    for name, item in manifest['files'].items():
        rel = PurePosixPath(name)
        assert name and not rel.is_absolute() and '\\' not in name and ':' not in name
        assert all(part not in ('', '.', '..') for part in rel.parts)
        path = root.joinpath(*rel.parts)
        assert root in path.resolve().parents and not path.is_symlink(), name
        assert path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], name
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == set(manifest['files']) | {'KIT_MANIFEST.json'}, 'Kit file set differs'
    return manifest


def inspect_inputs(artifact, entry_path, checker, expected_entry, expected_checker, expected_certificate):
    pinned(entry_path, expected_entry)
    pinned(checker, expected_checker)
    pinned(artifact/'certificate.jsonl.gz', expected_certificate)
    entry_bytes = read(entry_path)
    entry = json.loads(entry_bytes)
    assert entry_bytes == canonical(entry)+b'\n', 'Source entry is not canonical'
    registered = registry(checker)
    source_id = entry['source_id']
    assert type(source_id) is str and source_id != 'original64'
    assert set(registered) == {'original64', source_id}, 'Unexpected source registry entries'
    assert registered[source_id] == entry, 'Registry does not contain the exact source entry'
    for name in ARTIFACT_FILES:
        assert (artifact/name).is_file() and not (artifact/name).is_symlink(), name
    pinned(artifact/'source-residuals.jsonl.gz', entry['source_sha256'])
    source = ungzip(artifact/'source-residuals.jsonl.gz')
    assert hashlib.sha256(source).hexdigest() == entry['uncompressed_sha256'], 'Raw source differs'
    lines = source.splitlines()
    assert json.loads(lines[0]) == entry['source_header']
    assert len(lines)-1 == entry['source_rows']
    records = [json.loads(line) for line in ungzip(artifact/'certificate.jsonl.gz').splitlines()]
    first, final = records[0], records[-1]
    assert first['kind'] == 'initial' and final['kind'] == 'final'
    assert sum(r['kind']=='initial' for r in records) == sum(r['kind']=='final' for r in records) == 1
    assert first['source_id'] == source_id
    assert first['source_entry_sha256'] == expected_entry
    assert first['source_sha256'] == entry['source_sha256']
    assert first['source_variables'] == entry['source_variables'] and first['source_rows'] == entry['source_rows']
    candidate = json.loads(ungzip(artifact/'candidate-rows.json.gz'))
    assert hashlib.sha256(canonical(candidate)).hexdigest() == final['rows_sha256'], 'Candidate row digest differs'
    weights = json.loads(read(artifact/'weights.json'))
    assert weights and all(type(w) is int and w == 1 for w in weights), 'Only all-one weights are supported'
    events = [r for r in records if r['kind']=='weights']
    assert len(events) == 1 and len(events[0]['values']) == len(candidate)
    assert all(type(w) is int and w == 1 for w in events[0]['values'])
    active = json.loads(read(artifact/'variable-map.json'))
    assert active and active[0] == 0 and len(active) == len(set(active))
    assert all(type(v) is int and 0 <= v < final['allocated_variables'] for v in active)
    report = json.loads(read(artifact/'verification.json'))
    assert report['status'] == 'PASS' and report['source_id'] == source_id
    assert report['source_sha256'] == entry['source_sha256'] and report['certificate_sha256'] == expected_certificate
    assert report['expanded_sha256'] == sha(artifact/'polynomial.expanded.txt')
    assert ungzip(artifact/'polynomial.expanded.txt.gz') == read(artifact/'polynomial.expanded.txt')
    counts = {key: report[key] for key in COUNT_KEYS}
    assert all(type(v) is int and v > 0 for v in counts.values())
    assert counts['degree'] == 4 and counts['max_abs_coefficient'] < 2**80
    assert counts['variables'] == counts['witnesses']+1 == len(active)
    assert counts['rows'] == sum(bool(row) for row in candidate) == len(weights)
    assert all(final['report'][key] == value for key, value in counts.items())
    return entry, counts, report
