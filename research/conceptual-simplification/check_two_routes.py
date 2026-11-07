"""Exact regression checks for TWO_ROUTES.md; not a proof of the main theorem."""
from fractions import Fraction as Q
from math import gcd, lcm, isqrt
from pathlib import Path
import hashlib
import json


def primes(n):
    return [p for p in range(3, n + 1) if all(p % d for d in range(2, isqrt(p) + 1))]


def valuation(n, p):
    if not n:
        return float('inf')
    n = Q(n)
    def count(a):
        v = 0
        while a % p == 0:
            a //= p
            v += 1
        return v
    return count(abs(n.numerator)) - count(n.denominator)


def curve_add(P, R):
    # E: y^2=x^3-2. All arithmetic is rational, including inversions.
    if P is None:
        return R
    if R is None:
        return P
    x, y = P
    u, v = R
    if x == u and y == -v:
        return None
    slope = (3*x*x)/(2*y) if P == R else (v-y)/(u-x)
    X = slope*slope-x-u
    return X, slope*(x-X)-y


def main():
    checks = {}
    cases = 0
    for p in primes(31):
        for d in range(1, p):
            if pow(d, (p-1)//2, p) != p-1:
                continue
            for a in range(-p, p+1):
                for b in range(-p, p+1):
                    if a == b == 0:
                        continue
                    x, y = Q(a, p), Q(b, p*p)
                    assert valuation(x*x-d*y*y, p) == 2*min(valuation(x,p),valuation(y,p))
                    cases += 1
    checks['binary_norm_rational_cases'] = cases
    assert valuation(1+2**2, 5) == 1
    checks['real_positive_local_cancellation'] = {'p':5,'x':1,'y':2,'norm':5}
    assert (5*5-2) == 23 and (5+5) % 23 != 0
    checks['conjugate_ideal_example'] = {'norm':23,'roots_mod_23':[5,18]}

    # Exhaust all F_(p^2) squares for several inert residue characteristics.
    inert = []
    for p in primes(31):
        if pow(2, (p-1)//2, p) != p-1:
            continue
        squares = {((a*a+2*b*b)%p,(2*a*b)%p) for a in range(p) for b in range(p)}
        assert all((d,0) in squares for d in range(1,p))
        inert.append(p)
    checks['rational_units_square_in_quadratic_residue_field'] = inert

    cases = 0
    for A in range(1,13):
        for B in range(1,13):
            for L in range(1,9):
                period = lcm(A,B,L)
                for h0 in range(L):
                    predicted = gcd(A,B)==1 and h0%gcd(A,L)==0 and (h0-1)%gcd(B,L)==0
                    actual = any(h%A==0 and (h-1)%B==0 and (h-h0)%L==0 for h in range(period))
                    assert predicted == actual
                    cases += 1
    checks['generalized_CRT_cases'] = cases

    P = (Q(3),Q(5))
    points = []
    R = None
    for n in range(1,7):
        R = curve_add(R,P)
        assert R is not None and R[1]**2 == R[0]**3-2
        points.append(R)
    primitive = []
    support_cases = 0
    for p in primes(149):
        if p == 3: # discriminant -1728; 2 not in this list
            continue
        # Independent finite-group arithmetic via repeated addition modulo p.
        R = None
        for order in range(1, 2*p+5):
            if R is None:
                R = (3%p,5%p)
            else:
                x,y = R
                if x == 3%p and (y+5)%p == 0:
                    R = None
                else:
                    numerator,denominator = ((3*x*x,2*y) if R==(3%p,5%p) else (5-y,3-x))
                    assert denominator%p != 0
                    s = numerator*pow(denominator,-1,p)%p
                    X = (s*s-x-3)%p
                    R = (X,(s*(x-X)-y)%p)
            if R is None:
                break
        else:
            raise AssertionError('finite order not found')
        group_size = 1+sum(1 for x in range(p) for y in range(p) if (y*y-x*x*x+2)%p==0)
        assert group_size%order==0 and (group_size-p-1)**2<=4*p
        for n,(x,y) in enumerate(points,1):
            assert (x.denominator%p==0) == (n%order==0)
            support_cases += 1
            if n==order:
                primitive.append({'index':n,'prime':p,'group_size':group_size})
                assert n<=p+1 or (n-p-1)**2<=4*p
    checks['denominator_reduction_order_cases'] = support_cases
    checks['primitive_places_in_small_test'] = primitive

    # Check exponent bookkeeping without floating-point approximations.
    exponent = Q(19,80)
    margin = 2-8*exponent
    assert margin == Q(1,10)
    assert exponent/margin == Q(19,8)
    assert 2*exponent/margin == Q(19,4)
    checks['packed_height_coefficients'] = {'margin':'1/10','log29':'19/8','h_beta':'19/4'}
    root = Path(__file__).resolve().parents[2]
    pins = {}
    for rel in ['docs/quartic-523-540/addition.tex','research/conceptual-simplification/TWO_ROUTES.md','research/conceptual-simplification/check_two_routes.py']:
        pins[rel]=hashlib.sha256((root/rel).read_bytes()).hexdigest()
    return {'status':'PASS_EXACT_FINITE_REGRESSIONS','checks':checks,'sha256':pins,
            'scope':'Finite regressions and rational exponent identities only; universal deductions are proved in prose.',
            'main_arithmetic_theorem_verified':False,'independent_human_review':False,
            'polynomial_changed':False}


if __name__ == '__main__':
    print(json.dumps(main(),indent=2))
