#!/usr/bin/env python3
"""Independent recomputation of the numerical steps in paper.tex section 5
(effective soundness at N=15) and the exceptional-set claim of section 4.

Exact integers and fractions throughout; logarithms use decimal.Decimal.ln at 80
digits, which is correctly rounded, so every comparison below holds with a margin
of at least 10^-60 over the rounding error. Standard library only; nothing is
imported from the PR package. The inputs (c0, C0, S, Gamma, contacts, the
inequalities themselves) are transcribed from paper.tex; whether those inputs
and the logical steps between them are correct is NOT checked here.
"""
import sys
from decimal import Decimal as Dec, getcontext
from fractions import Fraction as Q
from math import prod, isqrt, floor

getcontext().prec = 80
if sys.flags.optimize:
    raise SystemExit('run without -O')
n = 0
def check(name, cond):
    global n
    if not cond:
        raise SystemExit('FAIL: ' + name)
    n += 1
    print('ok ', name)

ln = lambda x: (Dec(x.numerator) / Dec(x.denominator)).ln() if isinstance(x, Q) else Dec(x).ln()
EPS = Dec(10) ** -60
def isprime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

S = [2, 3, 5, 7, 11, 13, 17, 37, 41, 2399]
Gamma = S + [79, 89, 647, 3593]
c0, C0 = Q(74712001, 10 ** 6), 2 ** 68 * 3 ** 16 * 5 ** 16 * 7 ** 4
E = lambda ps: prod(Q(p + 1, p) for p in ps)

# section 4: every contact denominator, contact difference and c/2 - theta has support in Gamma
theta = [Q(0), Q(-1, 2), Q(-1), Q(1, 2399), Q(-32, 407)]
c = Q(3, 11)
cont = theta + [c - t for t in theta]
def support(x):
    m, out = abs(x.numerator) * x.denominator, set()
    for p in range(2, 10 ** 4):
        while m % p == 0:
            out.add(p); m //= p
    assert m == 1, x
    return out
sup = set()
for t in cont:
    sup |= support(Q(t.denominator)) | support(c / 2 - t)
    for u in cont:
        if u != t:
            sup |= support(t - u)
check('all Gamma entries prime', all(isprime(p) for p in Gamma))
check('contact denominators, differences and c/2-theta supported in Gamma', sup <= set(Gamma))
check('Gamma \\ S = {79, 89, 647, 3593} is exactly what the contacts need', sup - set(S) == {79, 89, 647, 3593})

# section 5 constants
J = prod(Gamma)
check('J* = 30366775457346956958330 < 2^75', J == 30366775457346956958330 and J < 2 ** 75)
check('c0*C0 < 2^149', c0 * C0 < 2 ** 149)
calC = c0 * C0 * J ** 2 * E(Gamma)
check('calC = c0 C0 J*^2 E(J*) < 2^300', calC < 2 ** 300)
small = [p for p in range(2, 1001) if isprime(p) and p not in Gamma]
check('prod_{p<=1000, p not in Gamma} (1+1/p) < 21/10', E(small) < Q(21, 10))
check('p log p > 6006 for every prime p > 1000 (smallest is 1009)', 1009 * ln(1009) > 6006 and 1000 * ln(1000) > 6006)
check('inverse maps: height constants 3 and 33 (max row l1-norms)',
      max(abs(0) + abs(1), abs(1) + abs(-2)) == 3 and max(abs(3) + abs(-17), abs(11) + abs(-22)) == 33)
check('coarse bound: 1 + 75 log 2 < 54 < 4*22', 1 + 75 * ln(2) < 54 < 88)
check('121 sqrt(21/10) 14^(1/3+1/36036) < 500',
      Dec(121) * (Dec(21) / 10).sqrt() * (ln(14) * (Dec(1) / 3 + Dec(1) / 36036)).exp() < 500)
check('log J* + (1/6) log 14 < 53', ln(J) + ln(14) / 6 < 53)
check('exponent: 2 - 4(1/3+1/36036) = (2/3)(1-1/6006)', 2 - 4 * (Q(1, 3) + Q(1, 36036)) == Q(2, 3) * (1 - Q(1, 6006)))
L15 = floor(Q(9 * (2 * 15 - 1), 4)) + 1
check('L_15 = floor(9(2N-1)/4)+1 = 66', L15 == 66)
s0 = 66 * ln(149)
lhs = Dec(2) / 3 * (1 - Dec(1) / 6006) * s0
rhs = ln(500) + 300 * ln(2) + ln(53 + Dec(2) / 3 * s0)
check(f'decisive comparison at s = 66 log 149: {lhs:.6f} > {rhs:.6f} (margin {lhs - rhs:.4f})', lhs - rhs > EPS)
check('stated rational bounds: 220*6005/6006 > 219.963 and 25/4 + 300*173287/250000 + 45/8 = 219.8194',
      Q(220 * 6005, 6006) > Q(219963, 1000) and Q(25, 4) + 300 * Q(173287, 250000) + Q(45, 8) == Q(2198194, 10000))
check('those rational bounds are valid: log149 in (5, 5.01), log 500 < 25/4, log 2 < 173287/250000, log 274 < 45/8, 53+44*5.01 < 274',
      5 < ln(149) < Dec('5.01') and ln(500) < Dec('6.25') and ln(2) < Dec(173287) / 250000 and ln(274) < Dec('5.625') and 53 + 44 * Dec('5.01') < 274)
check('f(s) = exp(a s)/(53 + 2s/3) increasing for s >= 0 (a*53 > 2/3)', Q(2, 3) * (1 - Q(1, 6006)) * 53 > Q(2, 3))
check('484 * 529 = 256036', 484 * 529 == 256036)
check('(23/22) log(256036 * 2^304) < 240', Dec(23) / 22 * (ln(256036) + 304 * ln(2)) < 240)
check('149^66 > 2^239, 149^66 > 600, log(149^66) > 330', 149 ** 66 > 2 ** 239 and 149 ** 66 > 600 and 66 * ln(149) > 330)
check('(c-6)*330 > 320c + 240 for c >= 149^66 (so s > 320 c_a > 240 + c_a)', (149 ** 66 - 6) * 330 > 320 * 149 ** 66 + 240)
BS = prod(S)
check('B_S = 1857890364330', BS == 1857890364330)
check('H4.2 scalar constant c0 C0 B_S^2 E(B_S) log B_S < 2^237',
      Dec(c0.numerator) / Dec(c0.denominator) * C0 * BS ** 2 * Dec((E(S)).numerator) / Dec((E(S)).denominator) * ln(BS) < Dec(2) ** 237)
# |Delta| <= t^2 + (a^2+1)|t||b| + (|a|+1)^2 b^2 + 1 <= B^2 + (B^2+1)B^2 + (B+1)^2 B^2 + 1 =: g(B).
# 14B^4 - g(B) = 12B^4 - 2B^3 - 3B^2 - 1, which is 6 at B = 1 and has derivative
# 48B^3 - 6B^2 - 6B = 6B(8B^2 - B - 1) > 0 for B >= 1, so it is positive for all real B >= 1.
gdiff = lambda B: 14 * B ** 4 - (B ** 2 + (B ** 2 + 1) * B ** 2 + (B + 1) ** 2 * B ** 2 + 1)
check('|Delta| <= 14 B^4 for all B >= 1, where |a|,|t|,|b| <= B: 14B^4 - g(B) = 12B^4-2B^3-3B^2-1, = 6 at B=1, increasing on B >= 1',
      all(gdiff(B) == 12 * B ** 4 - 2 * B ** 3 - 3 * B ** 2 - 1 for B in range(-5, 6)) and gdiff(1) == 6 and 8 - 1 - 1 > 0)
print(f'PASS: {n} checks')
