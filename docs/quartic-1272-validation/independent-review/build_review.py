"""Bind the independent review to its final checked artifacts."""
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def pin(path):
    return {'path': path.relative_to(WORK).as_posix(), 'sha256': sha256(path.read_bytes()).hexdigest(),
            'bytes': path.stat().st_size}

def main():
    table = load(HERE/'package-check.json')
    release = load(HERE/'release-check.json')
    inventory = load(HERE/'inventory-validation.json')
    replay_path = WORK/'package/replay-crossplatform-final/REPRODUCTION.json'
    replay = load(replay_path)
    serialization = load(HERE/'serialization-patch-check.json')
    assert table['status'] == 'PASS_FINITE_TABLE'
    assert release['status'] == 'PASS_RELEASE_BINDING'
    assert inventory['status'] == 'PASS'
    assert replay['status'] == 'PASS' and replay['byteIdentical']
    assert replay['packageManifestSha256'] == table['manifest']['sha256']
    assert serialization['status'] == 'PASS_SERIALIZATION_PATCH'
    assert serialization['currentManifestSha256'] == table['manifest']['sha256']
    assert inventory['inputPins']['quartic_1272.tex'] == release['manuscript']['sha256']
    assert release['manuscript']['sha256'] == '16033e0471df605093b28210a9f81718c2486b147016ec8afc75d166dff0b90f'
    paths = [HERE/x for x in ('REVIEW.md', 'check_package.py', 'package-check.json',
                              'check_release.py', 'release-check.json', 'check_inventory.py',
                              'inventory-validation.json', 'inventory-validation.log', 'FT-local-repair.md',
                              'check_serialization_patch.py', 'serialization-patch-check.json')]
    result = {
        'schema': 'quartic-v5-independent-review-v1',
        'date': '2026-11-06',
        'reviewer': 'astra_rebuild_oracle',
        'status': 'ACCEPTED_WITH_RECORDED_INPUTS',
        'unresolvedReviewFindings': [],
        'manuscript': release['manuscript'],
        'acceptedFragments': release['reviewedFragments'],
        'packageManifestSha256': table['manifest']['sha256'],
        'polynomialSha256': '02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586',
        'mathematicalReview': 'Reviewed the three new fragments and exact consumption of identified inherited interfaces. No unresolved mathematical objection within those inputs.',
        'independentFiniteCheck': {'residuals':1229, 'variables':1272, 'monomials':48001,
                                   'degree':4, 'primitiveContent':1, 'height':'64*3^(2^28)',
                                   'method':'Exact independent convolution of all actual final residuals; no package code imported.'},
        'inventoryValidation': {'status':'PASS', 'mode':'Read-only authored validator with independently selected input hash; files unchanged during validation.'},
        'serializationPatch': {'status':'PASS', 'baselineCommit':serialization['baselineCommit'],
                               'baselineManifestSha256':serialization['baselineManifestSha256'],
                               'mathematicalModulesCompared':len(serialization['mathematicalModules']),
                               'coreArtifactsCompared':len(serialization['coreArtifacts']),
                               'polynomialBytesUnchanged':True,
                               'exactByteComparisonsRetained':True,
                               'scope':'Only explicit UTF8 and line-ending settings change mathematical Python modules. Core data are identical. Metadata changes are timestamps, runtime measurements, hashes, and provenance.'},
        'packageAuthorReplay': {**pin(replay_path), 'elapsedSeconds':replay['elapsedSeconds'],
                                'checkCount':len(replay['checks']), 'attribution':'Separate package author replay, not the independent convolution.'},
        'limitations': [
            'Frei-Tinkova Theorem 1.4 is checked in arXiv 2408.17441v3, reported accepted by Mathematika. No final journal text is claimed verified.',
            'The local transferred inverse-theorem exponent correction is checked. Dodos-Kanellopoulos is compared to arXiv v4, not the final typeset statement; the correction does not close the whole Frei-Tinkova proof.',
            'Inherited source-version and arithmetic qualifications remain applicable; this review does not reprove every inherited or external theorem.',
            'Source evaluator samples supplement static review and exact algebraic checks; they do not establish global arithmetic existence or implications.',
            'The 1272-variable polynomial is an independent reconstruction, not a recovered unavailable 1315-variable artifact.',
            'No Lean verification or PDF layout approval is asserted.'
        ],
        'artifacts':[pin(p) for p in paths],
    }
    (HERE/'REVIEW.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'], 'manuscript':result['manuscript'],
                      'packageManifestSha256':result['packageManifestSha256']},indent=2))

if __name__ == '__main__': main()
