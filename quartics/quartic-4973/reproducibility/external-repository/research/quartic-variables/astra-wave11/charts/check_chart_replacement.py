"""Independent verifier for the seven-field-coordinate sparse 2E chart.

This file imports no producer code. See PROOF.md for the solution maps.
"""
from collections import defaultdict
from fractions import Fraction
from functools import reduce
from math import gcd, lcm


def add(*terms):
    answer = defaultdict(Fraction)
    for scalar, polynomial in terms:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += scalar * coefficient
    return {m: c for m, c in answer.items() if c}


def multiply(left, right):
    answer = defaultdict(Fraction)
    for m, c in left.items():
        for n, d in right.items():
            answer[tuple(sorted(m + n))] += c * d
    return {m: c for m, c in answer.items() if c}


def normalize(polynomial):
    if not polynomial:
        return ()
    denominator = lcm(*(Fraction(c).denominator for c in polynomial.values()))
    integer = {m: int(c * denominator) for m, c in polynomial.items()}
    common = reduce(gcd, integer.values())
    if integer[min(integer)] < 0:
        common = -common
    return tuple(sorted((m, c // common) for m, c in integer.items()))


def variables(polynomial):
    return {v for m in polynomial for v in m}


def fadd(left, right, scalar=1):
    return tuple(add((1, a), (scalar, b)) for a, b in zip(left, right))


def fmul(left, right):
    a, b = left
    c, d = right
    return add((1, multiply(a, c)), (2, multiply(b, d))), add((1, multiply(a, d)), (1, multiply(b, c)))


def chart_expected(rows, data, nextvar, incidence):
    """Return exact replacement rows and next unused variable, or reject."""
    names = ('u', 'v', 'w', 'z', 'f', 'h', 'x', 'y')
    blocks = ('f=u^2', 'v2+df=1', 'w2+v2=2', 'h=vw', 'zh+u=0', 'xf=1', 'yz+x=0')
    assert set(data) == {'coordinates', 'rows', 'new_variables', 'droot'}
    assert data['droot'] == [3, -1], 'Unexpected pinned curve parameter'
    coordinates = data['coordinates']
    assert set(coordinates) == set(names)
    old_variables = []
    for name in names:
        pair = coordinates[name]
        assert type(pair) is list and len(pair) == 2
        assert all(type(v) is int and 0 < v < nextvar for v in pair)
        old_variables.extend(pair)
    assert len(set(old_variables)) == 16, 'Aliased chart coordinates'
    row_ids = data['rows']
    assert set(row_ids) == set(blocks)
    selected = []
    for block in blocks:
        pair = row_ids[block]
        assert type(pair) is list and len(pair) == 2
        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)
        selected.extend(pair)
    assert len(set(selected)) == 14, 'Duplicate proof row'
    u, v, w, z, f, h, x, y = [tuple({(i,): 1} for i in coordinates[name]) for name in names]
    one, two = ({(): 1}, {}), ({(): 2}, {})
    droot, dsquare = ({(): 3}, {(): -1}), ({(): 11}, {(): -6})
    old = (
        fadd(f, fmul(u, u), -1),
        fadd(fadd(fmul(v, v), fmul(droot, f)), one, -1),
        fadd(fadd(fmul(w, w), fmul(v, v)), two, -1),
        fadd(h, fmul(v, w), -1),
        fadd(fmul(z, h), u),
        fadd(fmul(x, f), one, -1),
        fadd(fmul(y, z), x),
    )
    for block, pair in zip(blocks, old):
        for index, expected in zip(row_ids[block], pair):
            assert normalize(rows[index]) == normalize(expected), ('Chart proof row differs', block, index)
    changed = set(row_ids['w2+v2=2'] + row_ids['h=vw'] + row_ids['zh+u=0'])
    removed = set(coordinates['w'] + coordinates['h'])
    for v in removed:
        assert incidence.get(v, set()) <= changed, ('Removed chart coordinate used outside', v)
    fresh = data['new_variables']
    assert type(fresh) is list and len(fresh) == 2
    assert all(type(v) is int for v in fresh)
    assert fresh == [nextvar, nextvar + 1], 'Nonfresh p coordinate'
    p = tuple({(i,): 1} for i in fresh)
    new = (fadd(p, fmul(y, f), -1), fadd(fadd(fmul(p, p), x, -1), fmul(dsquare, f)))
    patches = {i: {} for i in changed}
    for block, pair in zip(('w2+v2=2', 'h=vw'), new):
        for index, expected in zip(row_ids[block], pair):
            assert all(len(m) <= 2 for m in expected)
            assert not variables(expected) & removed
            patches[index] = expected
    return patches, nextvar + 2


def ordinate_expected(rows, data, nextvar, incidence):
    """Eliminate y=x*p, using xf=1 to preserve the two chart relations."""
    assert set(data) == {'coordinates', 'rows'}
    coordinates, row_ids = data['coordinates'], data['rows']
    names = ('x', 'y', 'z', 'f', 'p')
    blocks = ('xf=1', 'p=yf', 'yz+x=0')
    assert set(coordinates) == set(names) and set(row_ids) == set(blocks)
    flat = []
    for name in names:
        pair = coordinates[name]
        assert type(pair) is list and len(pair) == 2
        assert all(type(v) is int and 0 < v < nextvar for v in pair)
        flat.extend(pair)
    assert len(set(flat)) == 10, 'Aliased ordinate proof coordinates'
    indices = []
    for block in blocks:
        pair = row_ids[block]
        assert type(pair) is list and len(pair) == 2
        assert all(type(i) is int and 0 <= i < len(rows) for i in pair)
        indices.extend(pair)
    assert len(set(indices)) == 6, 'Duplicate ordinate proof row'
    x, y, z, f, p = [tuple({(i,): 1} for i in coordinates[name]) for name in names]
    one = ({(): 1}, {})
    old = (fadd(fmul(x, f), one, -1), fadd(p, fmul(y, f), -1), fadd(fmul(y, z), x))
    for block, pair in zip(blocks, old):
        for i, expected in zip(row_ids[block], pair):
            assert normalize(rows[i]) == normalize(expected), ('Ordinate proof row differs', block, i)
    removed = set(coordinates['y'])
    replacements = dict(zip(coordinates['y'], fmul(x, p)))
    affected = set().union(*(incidence.get(v, set()) for v in removed))
    assert set(row_ids['p=yf'] + row_ids['yz+x=0']) <= affected
    patches = {}
    for i in affected:
        if i in row_ids['p=yf']:
            patches[i] = {}
            continue
        if i in row_ids['yz+x=0']:
            k = row_ids['yz+x=0'].index(i)
            patches[i] = fadd(fmul(p, z), one)[k]
            continue
        replacement = {}
        for monomial, coefficient in rows[i].items():
            term = {(): coefficient}
            for v in monomial:
                term = multiply(term, replacements.get(v, {(v,): 1}))
            replacement = add((1, replacement), (1, term))
        assert all(len(m) <= 2 for m in replacement), 'Ordinate substitution exceeds quadratic degree'
        assert not variables(replacement) & removed
        patches[i] = replacement
    return patches, nextvar
