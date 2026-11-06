"""Numerical check of the proof mechanism for Lemma CPO (NOT a proof).

Primes are drawn from the pinned progression p = c (mod W) (c = 18484837801,
W = 25878772920).  A prime is L0-good if no odd prime l <= L0 divides
d_{p,1} d_{p,2} = (p+1)^2 - 4a^2.  Orientation is the forced 2-adic one
(d_{p,2} = 4 mod 8).  For sets of k L0-good primes we test the CRT
compatibility conditions (X1), (X2) of NOTE.md exactly.

Usage: python3 -I frobenius_mechanism.py L0 trials k [seed]
"""
import math, random, sys
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

L0, TRIALS, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
c, W = 18484837801, 25878772920
small = [l for l in range(3, L0 + 1, 2) if all(l % q for q in range(3, int(l ** .5) + 1, 2))]

def draw():
    tries = 0
    while True:
        p = c + W * random.randrange(10**3, 10**5); tries += 1
        if any((p + 1) % q == 0 for q in (3, 5, 11, 13, 17, 19, 23, 29)) or not is_prime(p):
            continue
        a, _ = two_squares(p)
        prod = (p + 1) ** 2 - 4 * a * a
        if any(prod % l == 0 for l in small):
            continue
        d = sorted((p + 1 - 2 * a, p + 1 + 2 * a), key=lambda x: (x // 4) % 2 == 1)  # v2>=3 first
        assert d[0] % 8 == 0 and d[1] % 8 == 4
        return p, d[0], d[1]

def compatible(S):
    for i, (p, d1, _) in enumerate(S):
        for j, (q, _, e2) in enumerate(S):
            if i != j and (math.gcd(d1, e2) != 4 or d1 % q == 0):
                return False
    return True

ok = sum(compatible([draw() for _ in range(K)]) for _ in range(TRIALS))
print(f'L0={L0} k={K}: compatible {ok}/{TRIALS}')
