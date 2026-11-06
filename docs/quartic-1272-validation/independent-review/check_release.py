"""Independent release binding checks; no imports from the release programs."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK / 'repository'
FRAGMENTS = {
    'new1272': ('manuscript/new1272.tex', '506675ede05bb3d369d9882945958c86d2d39c8fbe4d6e1e393c6a4e17f00000'),
    'arithmetic-bridges': ('bridge-review/arithmetic_bridges.tex', '94696c3d3113c6ff23b8ff3039a17447424151d49f5ecbf1f178304aaf2d5544'),
    'sun-appendix': ('sun-proof/sun_appendix.tex', '620e2e5652048c827efd8a1d9dae78462679e65992beeb20c3f089b3115fb77b'),
}

def digest(path): return sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text(encoding='utf-8'))

def main():
    manuscript = REPO / 'quartic_1272.tex'
    text = manuscript.read_text(encoding='utf-8')
    fragments = []
    for name, (relative, expected) in FRAGMENTS.items():
        path = WORK / relative
        assert digest(path) == expected, name + ' changed since review'
        fragment = path.read_text(encoding='utf-8').strip()
        assert text.count(fragment) == 1, name + ' is not integrated exactly once'
        start = text.index(fragment)
        fragments.append({'id': name, 'path': relative, 'sha256': expected,
                          'firstLine': text.count('\n', 0, start) + 1,
                          'lastLine': text.count('\n', 0, start + len(fragment)) + 1})
    labels = Counter(re.findall(r'\\label\{([^}]+)\}', text))
    duplicates = {label: count for label, count in labels.items() if count > 1}
    refs = re.findall(r'\\(?:eqref|ref|pageref|autoref)\*?\{([^}]+)\}', text)
    missing = sorted(set(refs) - labels.keys())
    assert not duplicates, duplicates
    assert not missing, missing
    # Check the eight retained foundational text blocks against the frozen V4
    # source, using the source review's declared ranges and hashes.
    foundation = load(WORK / 'bridge-review/foundation_comparison.json')
    v4 = REPO / 'quartic_4973.tex'
    assert digest(v4) == foundation['current_source']['sha256']
    v4_lines = v4.read_text(encoding='utf-8').splitlines(keepends=True)
    retained = []
    for block in foundation['blocks']:
        if not block['identical_text']: continue
        first, stop = block['current_lines']
        fragment = ''.join(v4_lines[first-1:stop-1])
        assert sha256(fragment.encode()).hexdigest() == block['current_block_sha256'], block['id']
        assert fragment in text, block['id'] + ' not retained'
        retained.append(block['id'])
    assert len(retained) == 8
    coverage_path = REPO / 'docs/quartic-1272/coverage.json'
    coverage = load(coverage_path)
    assert coverage['manuscript']['sha256'] == digest(manuscript)
    assert coverage['all_external_inputs_published'] is False
    pending_keys = ('interfaces_missing_labels', 'new_applications_missing_labels',
                    'new_results_without_review_record', 'pending_review_records',
                    'unregistered_citations', 'unresolved_application_bridges', 'unresolved_references')
    pending = {key: coverage[key] for key in pending_keys if coverage[key]}
    receipt = {
        'status': 'PASS_RELEASE_BINDING' if not pending else 'PENDING_INVENTORY_REGISTRATION',
        'scope': 'Exact reviewed-fragment integration, foundational text retention, simple TeX reference closure, and inventory binding. Not a proof of the external arithmetic inputs.',
        'manuscript': {'path': 'quartic_1272.tex', 'sha256': digest(manuscript), 'bytes': manuscript.stat().st_size},
        'reviewedFragments': fragments, 'retainedFoundationBlocks': retained,
        'labelCount': len(labels), 'referenceCount': len(refs),
        'coverageSha256': digest(coverage_path), 'coverageStatus': coverage['status'],
        'allExternalInputsPublished': False, 'pending': pending,
    }
    (HERE / 'release-check.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__': main()
