"""Numerical probe of the cross-prime orientation lemma (NOT a proof).

Samples primes p = 1 mod 8 with (7/p) = -1 and p+1 a unit at every odd
q <= 29 (as in the pinned prime pattern), writes p = a^2 + b^2, and sets
d = p + 1 -/+ 2a.  For a shift constant c (4 in the pinned source) a shared
private multiplier h with h = 0 mod d_{p,1}, h = c mod d_{p,2} for all
sampled p exists iff, for some orientation, gcd(d_{p,1}, d_{p',2}) | c and
p' does not divide d_{p,1} (p != p').  Orientations are solved exactly by 2-SAT.

Usage: python3 -I cross_prime_experiment.py [seed] [trials]
"""
import math, random, sys
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
TRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 40

def is_prime(n):
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

def two_squares(p):                      # p = 1 mod 4
    for g in range(2, 200):
        if pow(g, (p - 1) // 2, p) == p - 1: break
    t = pow(g, (p - 1) // 4, p); a, b = p, t
    while b * b > p: a, b = b, a % b
    c = math.isqrt(p - b * b); assert b * b + c * c == p
    return (b, c) if b % 2 else (c, b)   # odd part first: Frobenius trace is 2*(odd part)

def sample(lo=10**12):
    while True:
        p = random.randrange(lo, 2 * lo) | 1
        if p % 8 != 1 or pow(7, (p - 1) // 2, p) != p - 1: continue
        if any((p + 1) % q == 0 for q in (3, 5, 7, 11, 13, 17, 19, 23, 29)): continue
        if is_prime(p):
            a, _ = two_squares(p); return p, (p + 1 - 2 * a, p + 1 + 2 * a)

def ok(P, o, Q, r, c):
    (p, dp), (q, dq) = P, Q
    p1, p2, q1, q2 = dp[o], dp[1 - o], dq[r], dq[1 - r]
    return c % math.gcd(p1, q2) == 0 and c % math.gcd(q1, p2) == 0 and p1 % q and q1 % p

def satisfiable(D, c):
    n = len(D); g = [[] for _ in range(2 * n)]
    for i in range(n):
        if not (ok(D[i], 0, D[i], 0, c) or ok(D[i], 1, D[i], 1, c)): pass
        for j in range(i + 1, n):
            for vi in (0, 1):
                for vj in (0, 1):
                    if not ok(D[i], vi, D[j], vj, c):
                        g[2*i+vi].append(2*j+1-vj); g[2*j+vj].append(2*i+1-vi)
    # Tarjan-free: Kosaraju
    order, seen = [], [False] * (2 * n)
    for s in range(2 * n):
        if seen[s]: continue
        stack = [(s, 0)]; seen[s] = True
        while stack:
            v, k = stack.pop()
            if k < len(g[v]):
                stack.append((v, k + 1)); w = g[v][k]
                if not seen[w]: seen[w] = True; stack.append((w, 0))
            else: order.append(v)
    rg = [[] for _ in range(2 * n)]
    for v in range(2 * n):
        for w in g[v]: rg[w].append(v)
    comp = [-1] * (2 * n); cnum = 0
    for s in reversed(order):
        if comp[s] >= 0: continue
        stack = [s]; comp[s] = cnum
        while stack:
            v = stack.pop()
            for w in rg[v]:
                if comp[w] < 0: comp[w] = cnum; stack.append(w)
        cnum += 1
    return all(comp[2*i] != comp[2*i+1] for i in range(n))

print('shift c | k=2  k=3  k=5  k=9  k=20 k=41   (successes out of %d)' % TRIALS)
for c in (4, 12, 4 * 3 * 5, 4 * 9 * 5 * 7 * 13):
    res = []
    for k in (2, 3, 5, 9, 20, 41):
        res.append(sum(satisfiable([sample() for _ in range(k)], c) for _ in range(TRIALS)))
    print(str(c).rjust(7), '|', ' '.join(str(x).rjust(4) for x in res))
