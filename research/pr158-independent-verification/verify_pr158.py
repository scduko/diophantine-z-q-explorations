#!/usr/bin/env python3
"""Independent exact verification of the data chain in elliotglazer/diophantine-z-q PR #158.

Written from scratch for this review. It reads every input as data and imports
nothing from the PR package, from José Brox's repository, or from upstream.
Standard library only; exact integer and rational arithmetic throughout.

Inputs (all paths are arguments, so nothing is resolved relative to the inputs):
  --pkg   research/brox-explicit229-v68 at the PR head
  --v19   quadratic-family.json and transformation.json exported from upstream main
          research/version19/construction/inputs/jose/computation/quartic/affine_laurent195_v45/
  --brox  quadratic.json, polynomial.json, graft.json, contact-change.json from
          JoseBrox/diophantine-z-q_improvements@7501669 computation/quartic/explicit229_v62/
  --main  docs/explicit-record/{README.md,measure_plain_text.py} exported from upstream main

Every check is an explicit comparison; the script exits nonzero on the first failure.
"""
import argparse, hashlib, json, re, sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from math import gcd

if sys.flags.optimize:
    raise SystemExit('run without -O')

RESULTS = []
def check(name, cond, detail=''):
    if not cond:
        raise SystemExit(f'FAIL: {name} {detail}')
    RESULTS.append((name, detail))
    print(f'ok  {name}' + (f'  [{detail}]' if detail else ''))

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def load(path):
    return json.load(open(path))

# ---------------------------------------------------------------- polynomials
# A polynomial is a dict mapping (C-power, sorted monomial tuple) -> Fraction.
def poly(terms):
    out = defaultdict(Q)
    for t in terms:
        out[(int(t.get('parameterPower', 0)), tuple(sorted(t['monomial'])))] += Q(t['coefficient'])
    return {k: c for k, c in out.items() if c}

def padd(*ps):
    out = defaultdict(Q)
    for p in ps:
        for k, c in p.items():
            out[k] += c
    return {k: c for k, c in out.items() if c}

def pscale(p, c):
    return {k: v * c for k, v in p.items() if v * c}

def pmul(a, b):
    out = defaultdict(Q)
    for (u, m), c in a.items():
        for (v, n), d in b.items():
            out[(u + v, tuple(sorted(m + n)))] += c * d
    return {k: c for k, c in out.items() if c}

def var(i, cpow=0):
    return {(cpow, (i,)): Q(1)}

def const(c):
    return {(0, ()): Q(c)} if c else {}

def proportional(p, q):
    """p == lam*q for a nonzero rational lam (exact)."""
    if not p or not q or set(p) != set(q):
        return None
    k = next(iter(q))
    lam = p[k] / q[k]
    return lam if all(p[m] == lam * q[m] for m in q) else None

# Q(sqrt2) elements as pairs of polynomials (a0, a1) meaning a0 + a1*rho.
def kadd(*xs):
    return padd(*[x[0] for x in xs]), padd(*[x[1] for x in xs])

def kmul(x, y):
    return (padd(pmul(x[0], y[0]), pscale(pmul(x[1], y[1]), 2)),
            padd(pmul(x[0], y[1]), pmul(x[1], y[0])))

def kscal(x, p):
    return pmul(x[0], p), pmul(x[1], p)

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    for a in ('pkg', 'v19', 'brox', 'main'):
        ap.add_argument('--' + a, required=True)
    A = ap.parse_args()
    P = lambda *x: '/'.join((A.pkg,) + x)

    # ---------------------------------------------------------- 1. provenance
    check('195 table hash (paper §1 digest)', sha(P('source/quadratic195.json')) == '304f94843c1a4ac94fcd5f1295fee8b532e7f0424e638314d892c556e2fbfdf9')
    check('195 table == upstream main Version 19 quadratic-family.json',
          open(P('source/quadratic195.json'), 'rb').read() == open(A.v19 + '/quadratic-family.json', 'rb').read())
    check('195 transformation == upstream main Version 19 transformation.json',
          open(P('source/transformation195.json'), 'rb').read() == open(A.v19 + '/transformation.json', 'rb').read())
    tr = load(P('transformation.json'))
    check('229 source hash == transformation.json pin', sha(P('source/quadratic229-v62.json')) == tr['source']['sha256'] == 'f0e6fc3f62525d7b251a10fc5f4cf0e6663c3f6f08beeef3cb28092b2e1555a8')
    check('229 source == Brox@7501669 explicit229_v62/quadratic.json',
          open(P('source/quadratic229-v62.json'), 'rb').read() == open(A.brox + '/quadratic.json', 'rb').read())
    for f in ('graft.json', 'contact-change.json'):
        check(f'{f} == Brox@7501669 copy', open(P(f), 'rb').read() == open(A.brox + '/' + f, 'rb').read())
    for f, g in (('upstream/explicit-record-README.md', 'explicit-record-README.md'), ('upstream/measure_plain_text.py', 'measure_plain_text.py')):
        check(f'{f} == upstream main', open(P(f), 'rb').read() == open(A.main + '/' + g, 'rb').read())

    old, new = load(P('source/quadratic195.json')), load(P('source/quadratic229-v62.json'))
    orows = {r['id']: r for r in old['residuals']}
    nrows = {r['id']: r for r in new['residuals']}
    check('table sizes', (old['variables'], len(old['residuals']), new['variables'], len(new['residuals'])) == (195, 175, 229, 207))
    check('row ids contiguous', sorted(orows) == list(range(1, 176)) and sorted(nrows) == list(range(1, 208)))
    check('input coordinate is 1 in both', old['inputCoordinate'] == new['inputCoordinate'] == 1)
    check('parameter powers in {0,1}', {t['parameterPower'] for r in new['residuals'] for t in r['terms']} <= {0, 1})

    # ---------------------------------------------------------- 2. graft structure as stated in paper.tex §1
    ocoord = {c['id']: c['name'] for c in old['coordinates']}
    ncoord = {c['id']: c for c in new['coordinates']}
    check('first 195 coordinate names unchanged', all(ncoord[i]['name'] == ocoord[i] for i in range(1, 196)))
    local = sorted(i for i, n in ocoord.items() if 'detector1' in n or 'det1' in n)
    stated = list(range(7, 11)) + list(range(86, 100)) + list(range(134, 150))
    check('second-detector local coordinates == {7..10} u {86..99} u {134..149} (paper §1)', local == stated, f'{len(local)} coordinates')
    clone = {ncoord[i]['clonedFrom195Id']: i for i in range(196, 230)}
    check('copies are x196..x229 in increasing order', [clone[i] for i in local] == list(range(196, 230)))
    check('new stored argument is x200 = copy of x86', clone[86] == 200)
    check('copied guard coordinates are x204, x205', (clone[90], clone[91]) == (204, 205))
    check('copied coordinate names: detector index replaced by 2',
          all(ncoord[clone[i]]['name'] == ocoord[i].replace('detector1', 'detector2').replace('det1', 'det2') for i in local))
    graft = load(P('graft.json'))
    check('graft.json coordinate map agrees', {int(k): v for k, v in graft['cloned_coordinate_map'].items()} == clone)

    is_local_row = lambda r: 'detector1' in r['name'] or 'det1' in r['name']
    users = defaultdict(set)
    for r in old['residuals']:
        if not is_local_row(r):
            for t in r['terms']:
                for i in set(t['monomial']) & set(local):
                    users[i].add(r['id'])
    check('only x86 is used outside the detector-1 rows, and only by row 175', dict(users) == {86: {175}})

    changed = [i for i in range(1, 175) if orows[i] != nrows[i]]
    check('rows 1..174 identical to the 195 table except the six contact rows', changed == [22, 24, 25, 34, 36, 37], str(changed))
    cc = load(P('contact-change.json'))
    check('contact-change.json lists the same changed rows (+ copies)', cc['changed_rows'] == changed + [176, 178, 179])
    det1_rows = [r for r in old['residuals'] if is_local_row(r)]
    check('31 detector-1 rows', len(det1_rows) == 31)
    for k, r in enumerate(det1_rows):
        src = nrows[r['id']]                    # copy the NEW version (new contact rows)
        dst = nrows[176 + k]
        want = {(p, tuple(sorted(clone.get(i, i) for i in m))): c for (p, m), c in poly(src['terms']).items()}
        ok = poly(dst['terms']) == want and dst['name'] == src['name'].replace('detector1', 'detector2').replace('det1', 'det2')
        check(f'row {176+k} is the coordinate-mapped copy of row {r["id"]}', ok)
    names = Counter(r['name'] for r in new['residuals'])
    check('residual names unique in the 229 table', max(names.values()) == 1)

    # ---------------------------------------------------------- 3. contact circuit (paper §3)
    theta = [Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407)]
    c, hc = Q(3, 11), Q(3, 22)
    contacts = theta + [c - t for t in theta]
    check('ten contacts distinct, diameter 25/11, midpoint 3/22 not a contact',
          len(set(contacts)) == 10 and max(contacts) - min(contacts) == Q(25, 11) and hc not in contacts)
    alpha = [(22 * t - 3) ** 2 for t in theta]
    check('paired constants 9,196,625,(7175/2399)^2,(175/37)^2',
          sorted(alpha) == sorted([Q(9), Q(196), Q(625), Q(7175, 2399) ** 2, Q(175, 37) ** 2]))
    # elementary symmetric functions
    e = [Q(1)]
    for a in alpha:
        e = [(e[j] if j < len(e) else 0) + (e[j - 1] * a if j >= 1 else 0) for j in range(len(e) + 1)]
    L = 7878870169
    check('L*e_j table (paper §3)', [L * x for x in e[1:]] == [6786192246520, 1229741066709366, 42042541279847500, 476802068222265625, 1738195040039062500]
          and all((L * x).denominator == 1 for x in e))
    # P5((22t-3)^2) == 22^10 prod (t-theta)(t-c+theta), as polynomials in t
    def umul(a, b):
        out = defaultdict(Q)
        for i, x in a.items():
            for j, y in b.items():
                out[i + j] += x * y
        return {k: v for k, v in out.items() if v}
    lhs, rr, pw = {}, {2: Q(484), 1: Q(-132), 0: Q(9)}, {0: Q(1)}
    coeffs = [(-1) ** (5 - k) * e[5 - k] for k in range(6)]   # P5 = sum_k coeffs[k] r^k
    for k in range(6):
        lhs = padd_u = {i: lhs.get(i, 0) + coeffs[k] * pw.get(i, 0) for i in set(lhs) | set(pw)}
        pw = umul(pw, rr)
    lhs = {i: v for i, v in lhs.items() if v}
    rhs = {0: Q(22 ** 10)}
    for t in theta:
        rhs = umul(rhs, {1: Q(1), 0: -t})
        rhs = umul(rhs, {1: Q(1), 0: t - c})
    check('P5((22t-3)^2) = 22^10 prod_theta (t-theta)(t-c+theta)', lhs == rhs)

    # Twelve contact rows: substitute the physical values of the table in §3 and compare
    # with the physical equations up to a nonzero rational factor.
    # Symbols: q, t, r, s, v, w, C (Laurent exponents allowed). Polynomials: dict exponent-tuple -> Q.
    SY = ['q', 't', 'r', 's', 'v', 'w', 'C']
    def mono(**ex):
        return tuple(ex.get(s, 0) for s in SY)
    def lmul(a, b):
        out = defaultdict(Q)
        for m, x in a.items():
            for n, y in b.items():
                out[tuple(i + j for i, j in zip(m, n))] += x * y
        return {k: v for k, v in out.items() if v}
    def ladd(*ps):
        out = defaultdict(Q)
        for p in ps:
            for k, v in p.items():
                out[k] += v
        return {k: v for k, v in out.items() if v}
    def lc(x, **ex):
        return {mono(**ex): Q(x)}
    def lprop(p, q):
        """p == lam * monomial * q for a nonzero rational lam and a Laurent monomial."""
        if not p or not q or len(p) != len(q):
            return None
        mp, mq = min(p), min(q)
        shift = tuple(i - j for i, j in zip(mp, mq))
        lam = p[mp] / q[mq]
        ok = all(p.get(tuple(i + j for i, j in zip(m, shift))) == lam * v for m, v in q.items())
        return (lam, dict(zip(SY, shift))) if ok else None
    layout = {0: dict(t=2, r=74, s=75, v=76, w=None), 1: dict(t=86, r=87, s=88, v=89, w=91), 2: dict(t=200, r=201, s=202, v=203, w=205)}
    for j, ids in layout.items():
        sub = {77: lc(1, q=1)}
        sub[ids['t']] = lc(1, t=1, q=1)
        sub[ids['r']] = lc(1, r=1, q=1)
        sub[ids['s']] = lc(1, s=1, q=1)
        sub[ids['v']] = lc(L, v=1, q=1, C=-1) if j == 0 else lc(L, v=1, q=1)
        if ids['w'] is not None:
            sub[ids['w']] = lc(1, w=1, q=1)
        W = lc(1, q=-1) if j == 0 else lc(1, w=1)          # physical w
        one_w = ladd(lc(1), W)
        t, r, s, v = lc(1, t=1), lc(1, r=1), lc(1, s=1), lc(1, v=1)
        phys = {
            'contactSquare': ladd(r, lmul(lc(-1), lmul(ladd(lmul(lc(22), t), lc(-3)), ladd(lmul(lc(22), t), lc(-3))))),
            'contactFourthPower': ladd(s, lmul(lc(-1), lmul(r, r))),
            'contactCombination': ladd(v, lmul(lc(-1), ladd(lmul(r, s), lmul(lc(-e[1]), lmul(one_w, s)), lmul(lc(e[2]), lmul(one_w, r))))),
            'contactRelation': ladd(lmul(s, v), lmul(lc(-1), lmul(one_w, ladd(lmul(lc(e[3]), s), lmul(lc(-e[4]), r), lc(e[5]))))),
        }
        for suffix, eq in phys.items():
            row = [r_ for r_ in new['residuals'] if r_['name'] == f'additive.detector{j}.{suffix}']
            check(f'detector {j} {suffix}: exactly one row', len(row) == 1)
            row = row[0]
            got = {}
            for term in row['terms']:
                acc = lc(Q(term['coefficient']), C=term['parameterPower'])
                for i in term['monomial']:
                    if i not in sub:
                        raise SystemExit(f'FAIL: row {row["id"]} uses unexpected coordinate x{i}')
                    acc = lmul(acc, sub[i])
                got = ladd(got, acc)
            res = lprop(got, eq)
            check(f'detector {j} {suffix} (row {row["id"]}) = nonzero multiple of the physical equation', res is not None and res[0] != 0,
                  f'factor {res[0]}*{ {k: v for k, v in res[1].items() if v} }' if res else '')

    # Literal unit guards
    for a, b in ((77, 78), (90, 91), (204, 205)):
        want = {(0, ()): Q(1), (0, (a, b)): Q(-1)}
        hits = [r['id'] for r in new['residuals'] if proportional(poly(r['terms']), want)]
        check(f'guard x{a}*x{b}=1 present exactly once', len(hits) == 1, f'row {hits}')

    # ---------------------------------------------------------- 4. aggregate rows (paper §2)
    q = var(77)
    D = (const(11), const(-6))
    def kv(i0, i1, cpow=0):
        return (var(i0, cpow), var(i1, cpow))
    f1, g1, s1 = kv(152, 153), kv(156, 157), kv(160, 161)
    f3, g3, s3 = kv(162, 163, 1), kv(166, 167), kv(170, 171)
    f4, g4, s4 = kv(172, 173, 1), kv(176, 177), kv(180, 181)
    p = kv(192, 193)
    Acomp = kadd(kmul(s1, s1), kmul(s3, s3), kmul(s4, s4),
                 kscal(kmul(D, kadd(f1, g1, f3, g3, f4, g4)), q), kscal(p, q))
    A0, A1 = Acomp
    qq = pmul(q, q)
    x2, x86, x200 = var(2), var(86), var(200)
    old_agg = padd(A0, pscale(qq, 14), pscale(pmul(q, padd(x2, pscale(x86, -1))), 2))
    new_agg = padd(A0, pscale(qq, 26), pscale(pmul(q, padd(x2, pscale(x86, -1))), 2))
    shift = padd(A1, pscale(qq, -8), pscale(pmul(q, padd(x2, pscale(x86, -2), x200)), 2))
    check('195 aggregate row 175 = 2q(x2-x86)+14q^2+A0 (nonzero multiple)', proportional(poly(orows[175]['terms']), old_agg) is not None)
    check('229 row 175 = 2q(x2-x86)+26q^2+A0 (eq:trace)', proportional(poly(nrows[175]['terms']), new_agg) is not None)
    check('229 row 207 = 2q(x2-2x86+x200)-8q^2+A1 (eq:shift)', proportional(poly(nrows[207]['terms']), shift) is not None)
    check('row 175 changes only its q^2 coefficient 14 -> 26',
          padd(poly(nrows[175]['terms']), pscale(poly(orows[175]['terms']), -1)) == {(0, (77, 77)): Q(12)} or
          padd(poly(nrows[175]['terms']), pscale(poly(orows[175]['terms']), -1)) == {(0, (77, 77)): Q(-12)})

    # ---------------------------------------------------------- 5. dropped original assertion: symbolic expansion
    def expand(rows):
        out = defaultdict(Q)
        for r in rows:
            items = list(poly(r['terms']).items())
            for a in range(len(items)):
                for b in range(a, len(items)):
                    (u, m), x = items[a]
                    (v, n), y = items[b]
                    out[(u + v, tuple(sorted(m + n)))] += x * y * (1 if a == b else 2)
        return {k: v for k, v in out.items() if v}
    sym = expand(new['residuals'])
    brox_poly = poly(load(A.brox + '/polynomial.json')['terms'])
    check("symbolic sum of squares == Brox's 490 kB polynomial family (assertion omitted by check_graft.py)", sym == brox_poly, f'{len(sym)} parameter terms')

    # ---------------------------------------------------------- 6. N=15 specialization and diagonal map
    C = 149 ** 15
    check('fixed parameter C = 149^15', int(tr['fixed_parameter']) == C and tr['fixed_N'] == 15 and tr['base'] == 149)
    a, b = tr['coordinate_powers'], tr['row_powers']
    check('exponent list lengths; input exponent 0', len(a) == 229 and len(b) == 207 and a[0] == 0)
    # printed exponent tables in paper.tex
    tex = open(P('paper.tex')).read()
    def table(header):
        block = tex.split(r'\subsection*{' + header + '}', 1)[1].split(r'\bottomrule', 1)[0]
        out = {}
        for chunk in block.split('\\\\'):
            line = chunk.replace(r'\endhead', '').replace(r'\midrule', '').strip()
            m = re.match(r'\s*(-?\d+)\s*&\s*([\d,\s]+)$', line)
            if m:
                for i in m.group(2).split(','):
                    out[int(i)] = int(m.group(1))
        return out
    ta, tb = table('Coordinate exponents'), table('Row exponents')
    check('paper.tex coordinate-exponent table == transformation.json', all(ta.get(i + 1, 0) == a[i] for i in range(229)) and all(0 < i <= 229 for i in ta), f'{len(ta)} nonzero entries')
    check('paper.tex row-exponent table == transformation.json', all(tb.get(j + 1, 0) == b[j] for j in range(207)) and all(0 < j <= 207 for j in tb), f'{len(tb)} nonzero entries')
    final = load(P('quadratic.json'))
    check('quadratic.json: 229 variables, input 1, 207 rows', final['variables'] == 229 and final['inputCoordinate'] == 1 and len(final['residuals']) == 207)
    rows = []
    for j, r in enumerate(new['residuals']):
        out = defaultdict(Q)
        for (cp, m), x in poly(r['terms']).items():
            e_ = b[j] + sum(a[i - 1] for i in m)
            out[m] += x * Q(C) ** cp * Q(149) ** e_
        out = {m: x for m, x in out.items() if x}
        check_int = all(x.denominator == 1 for x in out.values())
        if not check_int:
            raise SystemExit(f'FAIL: transformed row {j+1} not integral')
        rows.append({m: int(x) for m, x in out.items()})
    got = [{tuple(sorted(t['monomial'])): int(t['coefficient']) for t in r['terms']} for r in final['residuals']]
    check('every transformed row == quadratic.json (207/207)', rows == got)
    check('every transformed row integral, primitive, degree <= 2',
          all(gcd(*r.values()) == 1 and max(len(m) for m in r) <= 2 for r in rows))
    # the source parameter at N=15 before normalization: height 149^32 (thm:source)
    srcN = defaultdict(int)
    for (cp, m), x in sym.items():
        srcN[m] += int(x) * C ** cp
    check('unnormalized N=15 quartic: max |coefficient| = 149^32 (thm:source)', max(abs(v) for v in srcN.values() if v) == 149 ** 32)

    # ---------------------------------------------------------- 7. expansion and literal text
    quart = defaultdict(int)
    for r in rows:
        items = list(r.items())
        for i in range(len(items)):
            for k in range(i, len(items)):
                (m, x), (n, y) = items[i], items[k]
                quart[tuple(sorted(m + n))] += x * y * (1 if i == k else 2)
    quart = {m: v for m, v in quart.items() if v}
    pj = load(P('polynomial.json'))
    check('expansion == polynomial.json (every coefficient)', quart == {tuple(t['monomial']): int(t['coefficient']) for t in pj['terms']})
    check('3,312 monomials; degree 4; content 1; x1^4 coefficient 1',
          len(quart) == 3312 and max(map(len, quart)) == 4 and gcd(*quart.values()) == 1 and quart[(1, 1, 1, 1)] == 1)
    check('all 229 variables occur', {i for m in quart for i in m} == set(range(1, 230)))
    hmax = max(abs(v) for v in quart.values())
    check('max |coefficient| = 149^30 (217 bits)', hmax == 149 ** 30 and hmax.bit_length() == 217)
    check('monomial support unchanged by the normalization', set(quart) == {m for m, v in srcN.items() if v})
    # canonical text per docs/explicit-record/README.md, implemented independently
    parts = []
    for m in sorted(quart):
        v = quart[m]
        body = '*'.join(f'x{i}' + (f'^{k}' if k > 1 else '') for i, k in sorted(Counter(m).items()))
        mag = abs(v)
        termtxt = body if (mag == 1 and body) else (str(mag) + ('*' + body if body else ''))
        sign = '-' if v < 0 else ('+' if parts else '')
        parts.append(sign + termtxt)
    text = ''.join(parts).encode('ascii')
    lit = open(P('quartic229-N15.txt'), 'rb').read()
    check('independently rendered canonical text == quartic229-N15.txt', text == lit, f'{len(text)} bytes')
    check('74,007 bytes, strictly below 100,000; SHA-256 as claimed',
          len(lit) == 74007 and hashlib.sha256(lit).hexdigest() == '45bdea1ea7876bf6ec10b5427f9403cf1f94c144fab35817aa545bcb2cea1975')

    print(f'\nPASS: {len(RESULTS)} checks')

if __name__ == '__main__':
    main()
