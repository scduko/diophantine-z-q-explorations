"""Independent checker for the exact q_primeparity conic replacement.

No producer or repository modules are imported. See PROOF.md for rational
solution maps, including both zero and exceptional-chart cases.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, lcm


def add(*terms):
    out = defaultdict(F)
    for k, row in terms:
        for mon, c in row.items():
            out[mon] += k*c
    return {m: c for m, c in out.items() if c}


def mul(left, right):
    out = defaultdict(F)
    for m, c in left.items():
        for n, d in right.items():
            out[tuple(sorted(m+n))] += c*d
    return {m: c for m, c in out.items() if c}


def var(v):
    return {(v,): F(1)}


def norm(row):
    if not row:
        return ()
    den = lcm(*(F(c).denominator for c in row.values()))
    ints = {m: int(c*den) for m, c in row.items() if c}
    divisor = gcd(*ints.values())
    if ints[min(ints)] < 0:
        divisor = -divisor
    return tuple(sorted((m, c//divisor) for m, c in ints.items()))


def variables(row):
    return {v for m in row for v in m}


def expand(row, definitions):
    result = {}
    for mon, c in row.items():
        term = {(): c}
        for v in mon:
            term = mul(term, definitions.get(v, var(v)))
        result = add((1, result), (1, term))
    return result


def source_rows(b, witnesses):
    b = var(b)
    t, u, e, p, q, s, h = map(var, witnesses)
    tt, uu, ss = mul(t,t), mul(u,u), mul(s,s)
    return [
        add((1,u),(-1,b),(1,mul(mul(b,b),tt)),(1,mul(mul(b,u),tt))),
        add((1,mul(p,p)),(-17,b),(-34,mul(b,e)),(51,mul(b,mul(e,e)))),
        add((1,h),(-17,mul(b,e)),(1,mul(e,uu))),
        add((17,mul(b,mul(q,q))),(-1,mul(ss,ss)),
            (-34,mul(mul(b,h),ss)),(867,mul(mul(b,b),mul(h,h))))]


def replacement_rows(b, fresh):
    b = var(b)
    u,v,a,z,e,p,c,w,s,q,j,k = map(var, fresh)
    return [
        add((1,z),(-1,mul(u,u))),
        add((1,a),(-1,mul(b,v))),
        add((1,z),(1,mul(v,a)),(-1,mul(b,b))),
        add((1,c),(-1,mul(b,e))),
        add((1,mul(p,p)),(-17,b),(-34,c),(51,mul(e,c))),
        add((1,w),(-17,mul(b,c)),(1,mul(c,z))),
        add((1,j),(-1,mul(s,s))),
        add((1,k),(-1,mul(b,q))),
        add((1,mul(j,j)),(34,mul(j,w)),(-867,mul(w,w)),(-17,mul(q,k)))]


def check_rule(rows, incidence, data, nextvar):
    """Return expected patches and new allocation count; fail closed."""
    b = data['input']
    old = data['old_witnesses']
    ids = data['residual_rows']
    defs = data['definitions']
    new = data['new_variables']
    assert type(b) is int and 0 <= b < nextvar
    assert len(old) == len(set(old)) == 7
    assert all(type(v) is int and 0 < v < nextvar and v != b for v in old)
    assert len(ids) == len(set(ids)) == 4
    assert all(type(i) is int and 0 <= i < len(rows) for i in ids)
    assert len(new) == 12 and new == list(range(nextvar, nextvar+12))
    assert all(isinstance(d, list) and len(d) == 2 for d in defs)
    di = [i for i,v in defs]
    dv = [v for i,v in defs]
    assert len(di) == len(set(di)) and len(dv) == len(set(dv))
    assert not set(di)&set(ids)
    assert all(type(i) is int and 0 <= i < len(rows) for i in di)
    assert all(type(v) is int and 0 < v < nextvar for v in dv)
    assert not set(dv)&(set(old)|{b})
    selected = set(ids)|set(di)
    removed = set(old)|set(dv)
    assert len(selected) >= 9
    for v in removed:
        assert incidence.get(v,set()) <= selected, 'Outside use of removed parity coordinate'
    expanded = {}
    for i,v in defs:
        row = rows[i]
        coefficient = row.get((v,),0)
        assert coefficient
        rhs = add((-1/F(coefficient),row),(1,var(v)))
        assert v not in variables(rhs)
        assert variables(rhs) <= set(old)|{b}|set(expanded), 'Non-acyclic or external definition'
        expanded[v] = expand(rhs,expanded)
    expected_source = source_rows(b,old)
    for i,source in zip(ids,expected_source):
        assert norm(expand(rows[i],expanded)) == norm(source), 'Wrong source parity residual'
    expected = {i:{} for i in selected}
    for i,row in zip(sorted(selected),replacement_rows(b,new)):
        assert all(len(m)<=2 for m in row)
        expected[i] = dict(norm(row))
    return expected,nextvar+12


def check_patches(expected, supplied):
    assert len(supplied) == len({i for i,row in supplied})
    actual = {i:{tuple(m):c for c,m in row} for i,row in supplied}
    assert actual.keys() == expected.keys()
    for i,row in actual.items():
        assert all(type(c) is int and c and len(m)<=2 for m,c in row.items())
        assert norm(row) == norm(expected[i]), 'Incorrect supplied replacement'


def old_to_new(b, old):
    t,u,e,p,q,s,h = map(F,old)
    b = F(b)
    denominator = 1+b*t*t
    assert denominator != 0
    v = 2*b*t/denominator
    return [u,v,b*v,u*u,e,p,b*e,b*h,s,q,s*s,b*q]


def new_to_old(b, new):
    b = F(b)
    u,v,a,z,e,p,c,w,s,q,j,k = map(F,new)
    if not b:
        assert u == 0
        t = F(0)
    elif u+b:
        t = v/(u+b)
    else:
        assert u == -b and v == 0
        u = b
        t = F(0)
    return [t,u,e,p,q,s,e*(17*b-z)]
