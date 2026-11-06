"""Plain quadratic lift (degree <= 8 source -> sum of squares of quadratics).

Introduces one product variable per distinct unordered pair used to split
degree-3/4 monomials (reusing existing source equations c*v = c'*x*y), then
checks exactly that substituting the definitions back recovers every source
row.  This is a baseline: it does not apply the pinned pipeline's norm,
chart, ordinate, parity, batch, optimisation and merge reductions.

Usage: python3 -I naive_lift.py residuals.jsonl
"""
import json, sys
from fractions import Fraction
from collections import Counter
rows = [{tuple(m): Fraction(c) for c, m in json.loads(l)} for l in open(sys.argv[1]).read().splitlines()[1:]]
nv = 1 + max(v for r in rows for m in r for v in m)
pair = {}
# reuse explicit source definitions  c1*v + c2*x*y = 0
for r in rows:
    if len(r) == 2:
        lin = [m for m in r if len(m) == 1 and m[0] != 0]; quad = [m for m in r if len(m) == 2]
        if len(lin) == 1 and len(quad) == 1 and quad[0] not in pair and lin[0][0] not in quad[0]:
            pair[quad[0]] = (lin[0][0], -r[lin[0]] / r[quad[0]])   # x*y = s*v  ->  store v, s
freq = Counter()
for r in rows:
    for m in r:
        if len(m) >= 3:
            for i in range(len(m)):
                for j in range(i + 1, len(m)):
                    freq[(m[i], m[j])] += 1
new = []
def get(p):
    global nv
    if p not in pair:
        pair[p] = (nv, Fraction(1)); new.append(p); nv += 1
    return pair[p]
def split(m):
    m = list(m)
    if len(m) <= 2: return [((), Fraction(1), tuple(m))]
    best = None
    opts = []
    if len(m) == 3:
        for k in range(3):
            p = tuple(sorted(m[:k] + m[k+1:])); opts.append(([p], (m[k],)))
    else:
        a, b, c, d = m
        for p, q in [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]:
            opts.append(([tuple(sorted(p)), tuple(sorted(q))], ()))
    opts.sort(key=lambda o: (sum(p not in pair for p in o[0]), -sum(freq[p] for p in o[0])))
    ps, rest = opts[0]
    s = Fraction(1); vs = list(rest)
    for p in ps:
        v, sc = get(p); s *= sc; vs.append(v)
    return [(ps, s, tuple(sorted(vs)))]
out = []
for r in rows:
    q = {}
    for m, c in r.items():
        for ps, s, mm in split(m):
            q[mm] = q.get(mm, 0) + c * s
    out.append({m: c for m, c in q.items() if c})
defs = [{(pair[p][0],): Fraction(1), p: Fraction(-1)} for p in new]
quad = out + defs
assert all(len(m) <= 2 for r in quad for m in r)
# exact back-substitution check
back = {pair[p][0]: (p, pair[p][1]) for p in pair}   # v -> x*y / s
def expand(m):
    res = {(): Fraction(1)}
    for v in m:
        if v in back and back[v][0] in new or (v in back and v >= len_src):
            p, s = back[v]; term = {tuple(p): 1 / s}
        else:
            term = {(v,): Fraction(1)}
        res = {tuple(sorted(a + b)): ca * cb for a, ca in res.items() for b, cb in term.items()}
    return res
len_src = 1 + max(v for r in rows for m in r for v in m)
for r0, r1 in zip(rows, out):
    acc = {}
    for m, c in r1.items():
        for mm, cc in expand(m).items():
            acc[mm] = acc.get(mm, 0) + c * cc
    acc = {m: c for m, c in acc.items() if c}
    # reused source definitions: residual equality holds modulo those rows, so compare after
    # replacing source product vars too only when needed
    if acc != r0:
        # allow differences explained by reused source equations (v = x*y/s)
        full = {}
        for m, c in r1.items():
            t = {(): Fraction(1)}
            for v in m:
                term = {tuple(back[v][0]): 1 / back[v][1]} if v in back else {(v,): Fraction(1)}
                t = {tuple(sorted(a + b)): ca * cb for a, ca in t.items() for b, cb in term.items()}
            for mm, cc in t.items(): full[mm] = full.get(mm, 0) + c * cc
        r0f = {}
        for m, c in r0.items():
            t = {(): Fraction(1)}
            for v in m:
                term = {tuple(back[v][0]): 1 / back[v][1]} if v in back else {(v,): Fraction(1)}
                t = {tuple(sorted(a + b)): ca * cb for a, ca in t.items() for b, cb in term.items()}
            for mm, cc in t.items(): r0f[mm] = r0f.get(mm, 0) + c * cc
        assert {m: c for m, c in full.items() if c} == {m: c for m, c in r0f.items() if c}
print(json.dumps({'source_vars_incl_X': len_src, 'lift_new_vars': len(new),
                  'quartic_vars_incl_X': nv, 'quadratic_residuals': len(quad)}))

# ---- integer rows, full expansion, statistics --------------------------------
import math, hashlib, os
def integral(r):
    l = 1
    for c in r.values(): l = l * c.denominator // math.gcd(l, c.denominator)
    g = 0
    for c in r.values(): g = math.gcd(g, int(c * l))
    return {m: int(c * l) // g for m, c in r.items()}
irows = [integral(r) for r in quad if r]
poly = {}
for r in irows:
    items = list(r.items())
    for i, (m1, c1) in enumerate(items):
        for m2, c2 in items[i:]:
            m = tuple(sorted(m1 + m2)); c = c1 * c2 * (1 if m1 == m2 else 2)
            poly[m] = poly.get(m, 0) + c
poly = {m: c for m, c in poly.items() if c}
used = set(v for m in poly for v in m)
stats = {'variables_incl_X': nv, 'variables_occurring': len(used), 'degree': max(len(m) for m in poly),
         'monomials': len(poly), 'max_abs_coefficient': max(abs(c) for c in poly.values()),
         'quadratic_residuals': len(irows)}
if len(sys.argv) > 2:
    od = sys.argv[2]; os.makedirs(od, exist_ok=True)
    with open(os.path.join(od, 'quadratic-residuals.jsonl'), 'w') as fh:
        for r in irows: fh.write(json.dumps([[c, list(m)] for m, c in sorted(r.items())]) + '\n')
    lines = ['# coefficient followed by nondecreasing variable indices; variable 0 is X'] + \
            [' '.join([str(c)] + [str(v) for v in m]) for m, c in sorted(poly.items())]
    data = ('\n'.join(lines) + '\n').encode()
    open(os.path.join(od, 'polynomial.expanded.txt'), 'wb').write(data)
    stats['expanded_sha256'] = hashlib.sha256(data).hexdigest()
    json.dump(stats, open(os.path.join(od, 'stats.json'), 'w'), indent=1)
print(json.dumps(stats))
