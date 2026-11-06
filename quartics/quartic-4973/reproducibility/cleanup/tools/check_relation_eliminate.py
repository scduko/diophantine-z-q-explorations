"""Independent exact checker for elimination modulo untouched equations.

No producer/search module is imported. Integrate relation_eliminate_expected
as the handler for ``relation_eliminate`` and retain all ordinary patch,
degree, allocated-coordinate, source, and final expansion checks.
"""
from collections import defaultdict
from fractions import Fraction

if not __debug__:
    raise RuntimeError('Assertion-based certificate checks require normal Python mode')
from math import gcd, lcm


def variables(p):
    return {v for mon in p for v in mon}


def decode(terms):
    p = {}
    for c, mon in terms:
        assert type(c) is int and c != 0
        assert type(mon) is list and all(type(v) is int and v >= 0 for v in mon)
        key = tuple(mon)
        assert key == tuple(sorted(key)) and key not in p
        p[key] = Fraction(c)
    return p


def add(*parts):
    p = defaultdict(Fraction)
    for scalar, poly in parts:
        for mon, c in poly.items():
            p[mon] += scalar*c
    return {mon: c for mon, c in p.items() if c}


def multiply(p, q):
    r = defaultdict(Fraction)
    for mon, c in p.items():
        for other, d in q.items():
            r[tuple(sorted(mon+other))] += c*d
    return {mon: c for mon, c in r.items() if c}


def substitute(poly, variable, replacement):
    result = {}
    for mon, coefficient in poly.items():
        term = {(): coefficient}
        for v in mon:
            term = multiply(term, replacement if v == variable else {(v,): 1})
        result = add((1, result), (1, term))
    return result


def normalize(poly):
    if not poly:
        return ()
    denominator = lcm(*(Fraction(c).denominator for c in poly.values()))
    integer = {mon: int(c*denominator) for mon, c in poly.items()}
    divisor = gcd(*integer.values())
    if integer[min(integer)] < 0:
        divisor = -divisor
    return tuple(sorted((mon, c//divisor) for mon, c in integer.items()))


def rational_polynomial(data, limit, excluded, degree):
    denominator = data['denominator']
    assert type(denominator) is int and denominator > 0
    p = decode(data['terms'])
    assert all(len(mon) <= degree for mon in p)
    assert all(v < limit for v in variables(p))
    assert not variables(p) & excluded
    return {mon: c/denominator for mon, c in p.items()}


def relation_eliminate_expected(rows, data, nextvar, incidence):
    i, v = data['row'], data['variable']
    assert type(i) is int and 0 <= i < len(rows)
    assert type(v) is int and 0 < v < nextvar
    replacement = rational_polynomial(data['replacement'], nextvar, {v}, 2)
    defining = add((1, {(v,): 1}), (-1, replacement))
    assert normalize(rows[i]) == normalize(defining)
    affected = set(incidence.get(v, set())) - {i}
    assert i in incidence.get(v, set())
    reductions = data['reductions']
    ids = [r['row'] for r in reductions]
    assert all(type(j) is int and 0 <= j < len(rows) for j in ids)
    assert len(ids) == len(set(ids)) and set(ids) == affected
    frozen_forbidden = affected | {i}
    expected = {i: {}}
    for reduction in reductions:
        j = reduction['row']
        transformed = substitute(rows[j], v, replacement)
        support_ids = []
        for term in reduction['terms']:
            k = term['support']
            assert type(k) is int and 0 <= k < len(rows)
            assert k not in frozen_forbidden
            assert v not in variables(rows[k]) and rows[k]
            multiplier = rational_polynomial(term['multiplier'], nextvar, {v}, 2)
            assert multiplier
            support_ids.append(k)
            transformed = add((1, transformed), (-1, multiply(multiplier, rows[k])))
        assert len(support_ids) == len(set(support_ids))
        assert all(len(mon) <= 2 for mon in transformed)
        assert v not in variables(transformed)
        expected[j] = transformed
    return expected


def verify_event(rows, event, nextvar):
    assert event['kind'] == 'relation_eliminate'
    incidence = defaultdict(set)
    for i, poly in enumerate(rows):
        for v in variables(poly):
            incidence[v].add(i)
    expected = relation_eliminate_expected(rows, event['data'], nextvar, incidence)
    supplied = {i: decode(poly) for i, poly in event['patches']}
    assert len(supplied) == len(event['patches']) and supplied.keys() == expected.keys()
    assert all(normalize(supplied[i]) == normalize(poly) for i, poly in expected.items())
    return supplied


if __name__ == '__main__':
    import argparse
    import gzip
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Check supplied relation-elimination events against a parent.')
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    args = parser.parse_args()
    rows = [decode(poly) for poly in json.loads(gzip.decompress((args.parent/'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((args.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    limit = records[-1]['allocated_variables']
    events = [json.loads(line) for line in args.events.read_text().splitlines() if line.strip()]
    for event in events:
        for i, row in verify_event(rows, event, limit).items():
            rows[i] = row
    print(json.dumps({'status': 'PASS', 'events': len(events),
                      'scope': 'event identities only; parent and final expansion checked separately'}))
