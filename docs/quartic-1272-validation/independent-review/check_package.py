"""Independent finite check of the portable V5 table. No package imports."""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent/'repository/quartics/quartic-1272'
EXPECTED = '02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586'


def digest(path): return sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def collect(terms, coordinate_map=None):
    answer = defaultdict(Fraction)
    for term in terms:
        monomial = tuple(coordinate_map[i] if coordinate_map else i for i in term['monomial'])
        assert all(type(i) is int and 0 <= i < 1272 for i in monomial)
        assert monomial == tuple(sorted(monomial))
        power = term['sPower']
        assert type(power) is int and power >= 0
        answer[(power,monomial)] += Fraction(term['coefficient'])
    return {key: value for key,value in answer.items() if value}


def main():
    started = time.monotonic()
    table_path = PACKAGE/'compiler/translated/polynomial.json'
    rows_path = PACKAGE/'compiler/translated/compiled-ir.json'
    map_path = PACKAGE/'compiler/translated/coordinate-map.json'
    table, raw_rows = load(table_path), load(rows_path)
    assert digest(table_path) == EXPECTED
    rows = raw_rows['residuals']
    assert len(rows) == 1229
    sorted_ids = sorted(c['id'] for c in raw_rows['coordinates'])
    coordinate_map = dict(zip(sorted_ids,range(len(sorted_ids))))
    assert coordinate_map == {x['sourceId']:x['compactId'] for x in load(map_path)['mapping']}
    assert all(table['coordinates'][j]['sourceId']==i for i,j in coordinate_map.items())
    actual = collect(table['terms'])
    convolution = defaultdict(Fraction)
    for row in rows:
        entries = list(collect(row['terms'],coordinate_map).items())
        assert all(len(m) <= 2 for (s,m),c in entries)
        for i, ((s1,m1),c1) in enumerate(entries):
            for j in range(i,len(entries)):
                (s2,m2),c2 = entries[j]
                convolution[(s1+s2,tuple(sorted(m1+m2)))] += c1*c2*(1 if i==j else 2)
    convolution = {key: value for key,value in convolution.items() if value}
    assert convolution == actual
    assert all(c.denominator == 1 for c in actual.values())
    support = defaultdict(list)
    for (s,m),c in actual.items(): support[m].append((s,c))
    assert len(support) == len(actual) == 48001
    assert all(len(v)==1 for v in support.values())
    powers = Counter(s for s,m in actual)
    assert powers == {0:47993,1:7,2:1}
    active = set(i for s,m in actual for i in m)
    assert active == set(range(1272))
    assert max(map(len,support)) == 4
    assert actual[(0,(0,0,0,0))] == 1
    assert actual[(2,(79,79))] == 64
    assert max(abs(c.numerator) for (s,m),c in actual.items() if s==1) == 768
    maximum_constant_bits = max(abs(c.numerator).bit_length() for (s,m),c in actual.items() if s==0)
    assert maximum_constant_bits == 5339
    # S > 2^(2^27). These tiny exponent comparisons prove domination
    # without constructing S, its decimal expansion, or 2^(2^27).
    assert 2*(2**27)+6 > maximum_constant_bits
    assert 2**27 > (768).bit_length()
    content = 0
    for (s,m),c in actual.items():
        if s==0: content=gcd(content,c.numerator)
    assert content == 1
    receipt = {'status':'PASS_FINITE_TABLE',
        'scope':'Independent integer convolution and exact coefficient support. Not an arithmetic theorem or source-program proof.',
        'inputs':{str(p.relative_to(PACKAGE)):{'sha256':digest(p),'bytes':p.stat().st_size} for p in [table_path,rows_path,map_path]},
        'residuals':len(rows),'activeCoordinates':len(active),'degree':4,'monomials':len(support),
        'sPowerCounts':dict(powers),'maximumSFreeCoefficientBits':maximum_constant_bits,
        'maximumLinearSMultiplier':768,'maximumCoefficient':'64*S^2','primitiveIntegerContent':1,
        'noParameterExpansion':True}
    alias=PACKAGE/'polynomial.json'
    receipt['topLevelAliasPresent']=alias.exists()
    if alias.exists(): assert digest(alias)==EXPECTED
    manifest_path=PACKAGE/'MANIFEST.json'
    if manifest_path.exists():
        manifest=load(manifest_path)
        expected_paths={r['path'] for r in manifest['files']}
        actual_paths={p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()
                      and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
        assert actual_paths==expected_paths
        for rec in manifest['files']:
            p=PACKAGE/rec['path']
            assert p.stat().st_size==rec['bytes'] and digest(p)==rec['sha256']
        receipt['manifest']={'sha256':digest(manifest_path),'files':len(expected_paths),'status':'PASS'}
    receipt['wallSeconds']=round(time.monotonic()-started,3)
    (HERE/'package-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
