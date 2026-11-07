"""Finite regression checks; universal arguments are in ELEMENTARY_SEPARATION.md."""
import json
from math import gcd,isqrt
from fractions import Fraction
from pathlib import Path
import hashlib

primes=[p for p in range(3,301) if all(p%d for d in range(2,isqrt(p)+1))]
cases=0
for p in primes:
    for q in primes:
        if max(p,q)>2*min(p,q): continue
        for d in range(4,2*q-1,4):
            assert d%p != 0
            cases+=1
curves=0
for p in primes:
    squares={y*y%p for y in range(1,p)}
    for a in range(2,min(p,12)):
        # y^2=x(x-1)(x-a), three distinct roots.
        size=1
        for x in range(p):
            r=x*(x-1)*(x-a)%p
            size+=1 if r==0 else 2 if r in squares else 0
        assert size%4==0 and size<=2*p-2
        curves+=1
assert 16**16>5*2**40
assert (6_553_600)==(5*2**9)**2
# Squared exact inequalities avoid floating point in the primitive bound.
for B in range(16,10001):
    assert B**16>5*2**40
for C in range(1,101):
    u=3*C+1; w=1
    ps=[Fraction(u-C*w*w),Fraction(u+C*w*w)]
    assert ps[1]<2*ps[0]
root=Path(__file__).resolve().parents[2]
paths=['research/conceptual-simplification/ELEMENTARY_SEPARATION.md',
       'research/conceptual-simplification/check_separation.py',
       'docs/quartic-523-540/addition.tex']
print(json.dumps({'status':'PASS_FINITE_EXACT_CHECKS','abstract_group_order_cases':cases,
 'finite_field_curves':curves,'primitive_bound_integer_cases':9985,
 'proof_scope':'Elementary separation lemma proved in prose; primitive replacement conditional on missing local encoding.',
 'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
 'independent_human_review':False,'production_polynomial_changed':False},indent=2))
