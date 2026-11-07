"""Independent sparse-ring checks. Imports no code from the submitted archive."""
from collections import defaultdict
from fractions import Fraction as Q
from functools import reduce
import hashlib
import json
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parent
import os
OUT = Path(os.environ.get('ODD_PRODUCT_OUTPUT', str(ROOT.parents[1]/'build/odd-product')))
OUT.mkdir(parents=True, exist_ok=True)
DATA = ROOT.parents[1] / 'quartics/quartic-523-540'


def read(path):
    return json.loads(path.read_bytes())


def poly(terms):
    out = defaultdict(Q)
    for term in terms:
        variables = tuple(term['monomial'])
        assert tuple(sorted(variables)) == variables
        key = (term.get('sPower', 0), variables)
        assert key[0] >= 0
        out[key] += Q(term['coefficient'])
    return {key: value for key, value in out.items() if value}


def add(*polys):
    if not polys:
        return {}
    result = polys[0].copy()
    for p in polys[1:]:
        for key, value in p.items():
            updated = result.get(key, Q(0)) + value
            if updated:
                result[key] = updated
            else:
                result.pop(key, None)
    return result


def mul(p, q):
    result = defaultdict(Q)
    for (sp, mp), cp in p.items():
        for (sq, mq), cq in q.items():
            result[sp+sq, tuple(sorted(mp+mq))] += cp*cq
    return {key: value for key, value in result.items() if value}


def sub(p, variable, value):
    result = {}
    for (power, monomial), coefficient in p.items():
        term = {(power, tuple(v for v in monomial if v != variable)): coefficient}
        for _ in range(monomial.count(variable)):
            term = mul(term, value)
        result = add(result, term)
    return result


def support(p):
    return {v for s, m in p for v in m}


def degree(p):
    return max((len(m) for s, m in p), default=0)


def normalize(p):
    denominator = lcm(*(value.denominator for value in p.values()))
    content = gcd(*(int(value*denominator) for value in p.values()))
    return {key: value*denominator/content for key, value in p.items()}


def rows(document):
    result = {r['id']: poly(r['terms']) for r in document['residuals']}
    assert len(result) == len(document['residuals'])
    return result


def coords(document):
    result = {c['id']: c for c in document['coordinates']}
    assert len(result) == len(document['coordinates'])
    return result


def eliminate(folder, precursor, variant):
    source = read(folder / precursor)
    table = rows(source)
    variables = coords(source)
    cert = read(folder / variant / 'modulo-certificate.json')
    assert hashlib.sha256((folder / precursor).read_bytes()).hexdigest() == cert['baselineSha256']
    for operation in cert['operations']:
        if operation.get('kind') == 'shear':
            free = operation['free']
            assert free in variables
            for shear in operation['shears']:
                v = shear['coordinate']
                assert v in variables and v not in (0, free) and not variables[v].get('protected')
                replacement = {(0, (v,)): Q(1), (0, (free,)): Q(shear['factor'])}
                table = {key: sub(p, v, replacement) for key, p in table.items()}
                assert all(degree(p) <= 2 for p in table.values())
            continue
        v, pivot = operation['coordinate'], operation['pivot']
        replacement = poly(operation['replacement'])
        assert v in variables and v != 0 and not variables[v].get('protected')
        assert v not in support(replacement)
        equation = table[pivot]
        assert equation.get((0, (v,)), 0) != 0
        assert all(v not in m or (s, m) == (0, (v,)) for s, m in equation)
        assert not sub(equation, v, replacement)
        affected = {key for key, p in table.items() if v in support(p)}
        assert {entry['row'] for entry in operation['changes']} == affected - {pivot}
        assert len(operation['changes']) == len(affected)-1
        changes = {}
        for entry in operation['changes']:
            candidate = sub(table[entry['row']], v, replacement)
            for summand in entry['multiples']:
                factor = poly(summand['factor'])
                assert summand['row'] not in affected and v not in support(factor)
                candidate = add(candidate, mul(factor, table[summand['row']]))
            assert candidate == poly(entry['result']) and degree(candidate) <= 2
            changes[entry['row']] = candidate
        table.update(changes)
        del table[pivot]
        del variables[v]
    candidate = read(folder / variant / 'candidate-ir.json')
    assert table == rows(candidate) and variables == coords(candidate)
    integer = read(folder / variant / 'integer-candidate-ir.json')
    assert coords(integer) == variables
    assert rows(integer) == {key: normalize(p) for key, p in table.items()}
    return len(coords(source)) - len(variables)


def check_table(folder, variant):
    directory = folder / variant
    compiled = read(directory / 'polynomial/compiled-ir.json')
    serialized = read(directory / 'polynomial/polynomial.json')
    actual = poly(serialized['terms'])
    active = set()
    expected = {}
    for row in rows(compiled).values():
        assert degree(row) <= 2 and all(value.denominator == 1 for value in row.values())
        active |= support(row)
        expected = add(expected, mul(row, row))
    mapping = {c['sourceId']: c['id'] for c in serialized['coordinates']}
    assert len(mapping) == len(serialized['coordinates']) == len(active)
    assert set(mapping) == active == set(coords(compiled)) and mapping[0] == 0
    assert set(mapping.values()) == set(range(len(mapping)))
    expected = {(s, tuple(sorted(mapping[v] for v in m))): c for (s, m), c in expected.items()}
    assert expected == actual and degree(actual) == 4
    grouped = defaultdict(dict)
    for (s, m), c in actual.items():
        assert c.denominator == 1
        grouped[m][s] = int(c)
    # Each coordinate monomial has a single nonzero S-power; specialization cannot cancel it.
    assert all(len(terms) == 1 for terms in grouped.values())
    constant_coefficients = [value for terms in grouped.values() for power, value in terms.items() if power == 0]
    assert gcd(*constant_coefficients) == 1
    maximum_by_power = {s: max(abs(int(c)) for (power, m), c in actual.items() if power == s)
                        for s in {key[0] for key in actual}}
    report = {'variables': len(mapping), 'residuals': len(rows(compiled)), 'degree': 4,
              'nonzero_monomials': len(grouped), 'content': 1,
              'sha256': hashlib.sha256((directory / 'polynomial/polynomial.json').read_bytes()).hexdigest()}
    if set(maximum_by_power) == {0}:
        maximum = maximum_by_power[0]
        report['maximum_absolute_coefficient_bits'] = maximum.bit_length()
        report['maximum_minus_3_to_2048'] = str(maximum - 3**2048)
    else:
        # S=3^(2^26)>2^(2^26); compare bit lengths without constructing S.
        assert all(c.bit_length() <= 2**26 for c in maximum_by_power.values())
        assert max(maximum_by_power) == 2 and maximum_by_power[2] == 64
        report['maximum_absolute_coefficient'] = '64*3^(2^27)'
        report['maximum_coefficient_integer_multipliers_by_S_power'] = maximum_by_power
    return report


def lift(folder, symbolic, ordinary):
    before = read(folder / symbolic / 'integer-candidate-ir.json')
    after = read(folder / ordinary / 'lifted-ir.json')
    chain = after['constantChain']['coordinates']
    assert len(chain) == len(set(chain)) == 17
    assert not set(chain) & set(coords(before))
    assert set(coords(after)) == set(coords(before)) | set(chain)
    result = rows(after)
    for key, row in rows(before).items():
        expected = {}
        for (s, m), c in row.items():
            assert s in (0, 1) and len(m)+s <= 2
            expected[0, tuple(sorted(m + (chain[-1],)*s))] = c
        assert result.pop(key) == expected
    for i, variable in enumerate(chain):
        expected = {(0, (variable,)): Q(1),
                    (0, () if i == 0 else (chain[i-1], chain[i-1])): Q(-3**1024 if i == 0 else -1)}
        assert result.pop('constant-chain-' + str(i)) == expected
    assert not result


def main():
    manifest = read(DATA / 'SHA256SUMS.json')
    files = {p.relative_to(DATA).as_posix() for p in DATA.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.json'}
    assert files == set(manifest)
    for name, sha in manifest.items():
        assert hashlib.sha256((DATA / name).read_bytes()).hexdigest() == sha, name
    report = {'all_archive_hashes_verified': len(manifest), 'imports_submitted_code': False, 'variants': {}}
    for name, precursor, symbolic, ordinary in [('final554_571', 'source561.json', 'symbolic554', 'ordinary571'),
                                                 ('final523_540', 'source532.json', 'symbolic523', 'ordinary540')]:
        folder = DATA / name
        count = eliminate(folder, precursor, symbolic)
        lift(folder, symbolic, ordinary)
        report['variants'][name] = {'certified_eliminations': count, 'constant_chain': '17 unique rational coordinates',
                                    symbolic: check_table(folder, symbolic), ordinary: check_table(folder, ordinary)}
        print('Verified ' + name, flush=True)
    (OUT / 'INDEPENDENT_FINITE.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
