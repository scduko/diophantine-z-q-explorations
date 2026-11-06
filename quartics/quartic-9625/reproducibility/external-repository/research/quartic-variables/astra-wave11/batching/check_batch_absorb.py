"""Independent checker for root-error absorption in a quadratic norm batch.

Integration: import batch_absorb_expected; dispatch the event kind
``batch_absorb`` to expected,nextvar=batch_absorb_expected(rows,d,nextvar,incidence).
The caller must check every supplied patch against ``expected`` up to a nonzero
rational scalar and retain the usual final expansion checks.
"""
from collections import defaultdict
from fractions import Fraction
from math import gcd, lcm


def dec(terms):
    p = {}
    for c, m in terms:
        assert type(c) is int and c != 0
        assert type(m) is list and all(type(v) is int and v >= 0 for v in m)
        t = tuple(m)
        assert t == tuple(sorted(t)) and t not in p
        p[t] = Fraction(c)
    return p


def vs(p):
    return {v for m in p for v in m}


def add(*parts):
    out = defaultdict(Fraction)
    for c, p in parts:
        for m, a in p.items():
            out[m] += c*a
    return {m: a for m, a in out.items() if a}


def mul(p, q):
    out = defaultdict(Fraction)
    for m, a in p.items():
        for n, b in q.items():
            out[tuple(sorted(m+n))] += a*b
    return {m: a for m, a in out.items() if a}


def v(i):
    return {(i,): Fraction(1)}


def canon(p):
    if not p:
        return ()
    den = lcm(*(Fraction(c).denominator for c in p.values()))
    q = {m: int(c*den) for m, c in p.items()}
    g = gcd(*q.values())
    if q[min(q)] < 0:
        g = -g
    return tuple(sorted((m, c//g) for m, c in q.items()))


def expand(p, defs):
    out = {}
    for m, a in p.items():
        term = {(): a}
        for i in m:
            term = mul(term, defs.get(i, v(i)))
        out = add((1, out), (1, term))
    return out


def batch_absorb_expected(rows, d, nextvar, incidence):
    old_limit = nextvar
    def old(i):
        assert type(i) is int and 0 < i < old_limit
        return v(i)
    def row(i):
        assert type(i) is int and 0 <= i < len(rows)
        return rows[i]
    def eq(i, p):
        assert p and canon(row(i)) == canon(p)
    E, T = old(d['error']), old(d['root'])
    assert d['error'] != d['root']
    root_row = d['root_row']
    eq(root_row, add((1, E), (-1, mul(T, T)), (2, {(): 1})))
    # Over Q the retained root row implies E != 0: sqrt(2) is irrational.
    # Every retained first-leaf row then proves its R != 0.
    proofs = {}
    proof_rows = {root_row}
    for r, f, i in d['first_leaves']:
        R, F = old(r), old(f)
        assert r not in proofs and i not in proof_rows
        eq(i, add((1, mul(R, F)), (-1, R), (-1, mul(E, E))))
        proofs[r] = f
        proof_rows.add(i)
    assert proofs

    items = d['definitions']
    targets = [t for _, t in items]
    indices = [i for i, _ in items]
    assert len(targets) == len(set(targets))
    assert len(indices) == len(set(indices))
    assert not set(indices) & proof_rows
    target_set = set(targets)
    expanded = {}
    for i, t in items:
        old(t)
        rr = row(i)
        c = rr.get((t,), 0)
        assert c
        rhs = add((-Fraction(1, c), rr), (1, v(t)))
        assert t not in vs(rhs)
        assert vs(rhs) & target_set <= expanded.keys()
        expanded[t] = expand(rhs, expanded)

    removed_list = d['removed']
    removed = set(removed_list)
    assert len(removed) == len(removed_list) and removed <= target_set
    pair_rows = [p['row'] for p in d['pairs']]
    assert pair_rows and len(pair_rows) == len(set(pair_rows))
    assert not set(pair_rows) & (set(indices) | proof_rows)
    changed = set(pair_rows) | {i for i, t in items if t in removed}
    for t in removed:
        assert incidence.get(t, set()) <= changed
    expected = {i: {} for i in changed}

    # Every new coordinate is explicitly defined. Odd powers use the proved
    # unit R; squares use a polynomial definition. No square root is chosen.
    new_rows = []
    odds = {}
    squares = {}
    def fresh(t):
        nonlocal nextvar
        assert type(t) is int and t == nextvar
        nextvar += 1
    for spec in d['new_variables']:
        kind = spec['kind']; t = spec['variable']; fresh(t)
        if kind == 'odd_power':
            r, p = spec['factor'], spec['even']
            R, P = old(r), old(p)
            assert r in proofs and (r, p) not in odds
            assert not {r, p} & removed
            odds[r, p] = t
            new_rows.append(add((1, mul(R, v(t))), (-1, P)))
        else:
            assert kind == 'square'
            B = dec(spec['base'])
            assert B and all(len(m) <= 1 for m in B)
            assert all(i < old_limit for i in vs(B)) and not vs(B) & removed
            squares[t] = B
            new_rows.append(add((1, v(t)), (-1, mul(B, B))))
    low = {}
    for r, p, i in d['low_powers']:
        R, P = old(r), old(p)
        assert r in proofs and (r, p) not in low and (r, p) not in odds
        assert i not in changed and not {r, p} & removed
        eq(i, add((1, P), (-1, mul(R, R))))
        low[r, p] = r
    used_odds = set(); used_squares = set(); used_proofs = set(); used_low = set()
    for pair in d['pairs']:
        i, r, f, p, o, n, t, q = (pair[k] for k in
            ('row', 'factor', 'first', 'even', 'odd', 'norm', 'test', 'square'))
        R, F, P, N, U = (old(j) for j in (r, f, p, n, t))
        assert proofs.get(r) == f
        assert o == (odds | low).get((r, p))
        B = dec(pair['base'])
        assert B and all(len(m) <= 1 for m in B)
        assert all(j < old_limit for j in vs(B))
        assert q in squares and mul(B, B) == mul(squares[q], squares[q])
        assert not (vs(B) | {r, f, p, n, t}) & (removed | target_set)
        want = add((1, mul(P, N)), (-1, mul(mul(E, E), mul(B, B))),
                   (-1, mul(R, mul(U, U))))
        assert canon(expand(row(i), expanded)) == canon(want)
        expected[i] = add((1, mul(v(o), N)), (-1, mul(F, v(q))),
                          (1, v(q)), (-1, mul(U, U)))
        used_proofs.add(r); used_squares.add(q)
        (used_odds if (r, p) in odds else used_low).add((r, p))
    assert used_proofs == proofs.keys()
    assert used_odds == odds.keys() and used_low == low.keys()
    assert used_squares == squares.keys()
    for k, rr in enumerate(new_rows):
        expected[len(rows)+k] = rr
    assert not set(expected) & proof_rows
    assert all(not vs(rr) & removed and all(len(m) <= 2 for m in rr)
               for rr in expected.values())
    return expected, nextvar


if __name__ == '__main__':
    import argparse
    import gzip
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Check one batch-absorb event against its parent rows.')
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--event', type=Path, required=True)
    args = parser.parse_args()
    rr = [dec(x) for x in json.loads(gzip.decompress((args.parent/'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((args.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    limit = records[-1]['allocated_variables']
    incidence = defaultdict(set)
    for i, poly in enumerate(rr):
        for t in vs(poly):
            incidence[t].add(i)
    event = json.loads(args.event.read_bytes())
    assert event['kind'] == 'batch_absorb'
    want, limit = batch_absorb_expected(rr, event['data'], limit, incidence)
    patches = {i: dec(poly) for i, poly in event['patches']}
    assert len(patches) == len(event['patches']) and patches.keys() == want.keys()
    assert all(canon(patches[i]) == canon(poly) for i, poly in want.items())
    print(json.dumps({'status': 'PASS', 'scope': 'one exact event; parent certificate and final expansion not checked here',
                      'pairs': len(event['data']['pairs']), 'patches': len(patches), 'allocated_variables': limit}))
