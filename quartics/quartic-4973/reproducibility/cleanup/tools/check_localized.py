"""Independent checker for one localized_eliminate certificate operation.

Does not import the producer. Add the dispatcher hook documented in RESULT.md
to the main certificate checker to validate full candidate artifacts.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import math

if not __debug__:
    raise RuntimeError('Assertion-based certificate checks require normal Python mode')


def decode(terms):
    out = {}
    for c, m in terms:
        assert type(c) is int and c != 0
        assert all(type(v) is int and v >= 0 for v in m)
        key = tuple(m)
        assert key == tuple(sorted(key)) and key not in out
        out[key] = Fraction(c)
    return out


def vars_in(poly):
    return {v for term in poly for v in term}


def combine(terms):
    out = defaultdict(Fraction)
    for scale, poly in terms:
        for m, c in poly.items():
            out[m] += scale * c
    return {m: c for m, c in out.items() if c}


def product(*polys):
    out = defaultdict(Fraction)
    for terms in itertools.product(*(tuple(p.items()) for p in polys)):
        coefficient = Fraction(1)
        monomial = []
        for m, c in terms:
            coefficient *= c
            monomial.extend(m)
        out[tuple(sorted(monomial))] += coefficient
    return {m: c for m, c in out.items() if c}


def proportional(a, b):
    if not a or not b:
        return not a and not b
    if set(a) != set(b):
        return False
    anchor = min(a)
    return all(a[m] * b[anchor] == b[m] * a[anchor] for m in a)


def prove_unit(rows, factor, proof, removed, allocated, ancestors=()):
    assert factor and all(len(m) <= 1 for m in factor)
    assert removed not in vars_in(factor)
    assert all(v < allocated for v in vars_in(factor))
    i = proof["row"]
    assert type(i) is int and 0 <= i < len(rows)
    row = rows[i]
    assert len(ancestors) <= 256
    # Retaining the proof without the eliminated coordinate is essential.
    assert removed not in vars_in(row)
    if proof["kind"] == "inverse":
        w = proof["witness"]
        assert type(w) is int and 0 <= w < allocated
        assert row.get((), 0) != 0
        nonconstant = {m: c for m, c in row.items() if m}
        assert proportional(nonconstant, product(factor, {(w,): Fraction(1)}))
    elif proof["kind"] == "root_error":
        e, t = proof["error"], proof["root"]
        assert all(type(v) is int and 0 <= v < allocated for v in (e, t))
        assert e != t
        assert proportional(factor, {(e,): Fraction(1)})
        assert proportional(row, {(e,): Fraction(1), (t, t): Fraction(-1), (): Fraction(2)})
        # For rational t, t^2 != 2 by the usual coprime numerator/denominator proof.
    elif proof["kind"] == "product_unit":
        # The retained row states factor*cofactor = c*monomial. All
        # variables in monomial are independently nonzero and c != 0.
        # This includes R*(F-1)=E^2, without assuming F is nonzero.
        certified_factor = decode(proof["factor"])
        assert certified_factor and all(len(m) <= 1 for m in certified_factor)
        assert proportional(factor, certified_factor)
        cofactor = decode(proof["cofactor"])
        monomial = tuple(proof["monomial"])
        assert monomial == tuple(sorted(monomial))
        assert all(type(w) is int and 0 <= w < allocated for w in monomial)
        assert cofactor and all(len(m) <= 1 for m in cofactor)
        assert removed not in vars_in(cofactor)
        assert all(w < allocated for w in vars_in(cofactor))
        coefficient = proof["coefficient"]
        assert type(coefficient) is int and coefficient != 0
        assert (i, tuple(sorted(factor.items()))) not in ancestors
        expected_row = combine([(1, product(certified_factor, cofactor)),
                                (-coefficient, {monomial: Fraction(1)})])
        assert expected_row and proportional(row, expected_row)
        known = {w: child for w, child in proof["known"]}
        assert len(known) == len(proof["known"]) and set(known) == set(monomial)
        for w, child in known.items():
            assert type(w) is int
            prove_unit(rows, {(w,): Fraction(1)}, child, removed, allocated,
                       ancestors + ((i, tuple(sorted(factor.items()))),))
    elif proof["kind"] == "binomial":
        v = proof["variable"]
        assert type(v) is int and 0 <= v < allocated
        assert proportional(factor, {(v,): Fraction(1)})
        assert len(row) == 2
        left = [m for m in row if v in m]
        right = [m for m in row if v not in m]
        assert len(left) == len(right) == 1
        assert (i, v) not in ancestors
        known = {w: child for w, child in proof["known"]}
        assert len(known) == len(proof["known"]) and set(known) == set(right[0])
        for w, child in known.items():
            assert type(w) is int
            prove_unit(rows, {(w,): Fraction(1)}, child, removed, allocated, ancestors + ((i, v),))
        # Both binomial coefficients are nonzero. The right monomial is
        # nonzero, hence so is the left monomial and each of its factors.
    else:
        raise AssertionError("unknown nonzero proof")


def expected(rows, data, allocated, incidence, patches, relations=False):
    """Validate and return the complete patch map; no mutation occurs here."""
    i, v = data["row"], data["variable"]
    assert type(i) is int and 0 <= i < len(rows)
    assert type(v) is int and 0 < v < allocated
    a, n = decode(data["denominator"]), decode(data["numerator"])
    assert a and max(map(len, a)) == 1
    assert all(len(m) <= 2 for m in n)
    assert v not in vars_in(a) | vars_in(n)
    assert all(w < allocated for w in vars_in(a) | vars_in(n))
    assert proportional(rows[i], combine([(1, product(a, {(v,): Fraction(1)})), (-1, n)]))
    prove_unit(rows, a, data["nonzero"], v, allocated)
    affected = sorted(incidence[v] - {i})
    assert data["affected"] == affected
    assert len(patches) == len(affected) + 1
    supplied = {j: decode(poly) for j, poly in patches}
    assert len(supplied) == len(patches) and set(supplied) == set(affected) | {i}
    assert supplied[i] == {}
    factors_by_row = {entry["row"]: entry["factors"] for entry in data["cancellations"]}
    assert len(factors_by_row) == len(data["cancellations"])
    assert set(factors_by_row) == set(affected)
    reductions = {}
    if relations:
        reductions = {entry['row']: entry['terms'] for entry in data['reductions']}
        assert len(reductions) == len(data['reductions'])
        assert set(reductions) == set(affected)
    for j in affected:
        new = supplied[j]
        assert all(len(m) <= 2 for m in new)
        assert v not in vars_in(new)
        assert all(w < allocated for w in vars_in(new))
        original = rows[j]
        exponent = max((Counter(m)[v] for m in original), default=0)
        assert 0 <= exponent <= 2
        summands = []
        for monomial, coefficient in original.items():
            occurrences = Counter(monomial)[v]
            other = tuple(w for w in monomial if w != v)
            summands.append((coefficient, product({other: Fraction(1)},
                             *([n] * occurrences), *([a] * (exponent - occurrences)))))
        cleared = combine(summands)
        if relations:
            used = set()
            for term in reductions[j]:
                support = term['support']
                assert type(support) is int and 0 <= support < len(rows)
                assert support not in supplied and support not in used
                used.add(support)
                assert rows[support] and v not in vars_in(rows[support])
                denominator = term['multiplier']['denominator']
                assert type(denominator) is int and denominator > 0
                numerator = decode(term['multiplier']['terms'])
                assert all(len(m) <= 2 for m in numerator)
                assert v not in vars_in(numerator)
                assert all(w < allocated for w in vars_in(numerator))
                cleared = combine([(1, cleared),
                                   (-Fraction(1, denominator), product(numerator, rows[support]))])
        factors = []
        assert len(factors_by_row[j]) <= 8
        for entry in factors_by_row[j]:
            factor = decode(entry["factor"])
            assert factor and max(map(len, factor)) == 1
            prove_unit(rows, factor, entry["proof"], v, allocated)
            factors.append(factor)
        assert proportional(cleared, product(new, *factors)), ("failed identity", j)
    return supplied


def relation_expected(rows, data, allocated, incidence, patches):
    return expected(rows, data, allocated, incidence, patches, relations=True)
