"""Exact finite checks for NORM_PACKING.md, not a proof of the main theorem."""
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import hashlib
import json


def det_mod(a,p):
    a=[row[:] for row in a]; out=1
    for j in range(len(a)):
        q=next((i for i in range(j,len(a)) if a[i][j]%p),None)
        if q is None:return 0
        if q!=j:a[j],a[q]=a[q],a[j];out=-out
        u=a[j][j]%p;out=out*u%p;iv=pow(u,-1,p)
        for i in range(j+1,len(a)):
            c=a[i][j]*iv%p
            for k in range(j,len(a)):a[i][k]=(a[i][k]-c*a[j][k])%p
    return out%p


def mul(a,b,f,p):
    r=[0]*(2*len(f)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]=(r[i+j]+x*y)%p
    n=len(f)
    for k in range(len(r)-1,n-1,-1):
        for j,c in enumerate(f):r[k-n+j]=(r[k-n+j]-r[k]*c)%p
    return r[:n]


def norm(a,f,p):
    n=len(f); cols=[]
    for j in range(n):
        e=[0]*n;e[j]=1;cols.append(mul(a,e,f,p))
    return det_mod([[cols[j][i] for j in range(n)] for i in range(n)],p)


def find_field(n):
    # Search monic polynomials x^n+sum f_i x^i over F_2 by the norm criterion.
    for f in product(range(2),repeat=n):
        if not f[0]:continue
        if all(norm(list(a),list(f),2) for a in product(range(2),repeat=n) if any(a)):
            return list(f)
    raise AssertionError(n)


fields={}
for n in range(2,9):
    f=find_field(n);fields[str(n)]=f
    for a in product(range(2),repeat=n):
        assert (norm(list(a),f,2)==0)==(not any(a))

# F is the degree-16 subfield of Q(zeta_97).  Verify that 5 generates the
# full order-96 group, so its image in the quotient of order 16 has order 16.
ell=97;g=5
assert all(ell%d for d in range(2,isqrt(ell)+1))
orders=[d for d in range(1,97) if 96%d==0 and pow(g,d,ell)==1]
assert orders==[96]
assert min(d for d in range(1,17) if pow(g,d,ell) in
           {pow(g,16*k,ell) for k in range(6)})==16
# The Gaussian class 1+2i has norm 5 and keeps both reduced group orders
# nonzero modulo 97.
a,b=1,2
assert (a*a+b*b)%ell==5
assert ((a-1)**2+b*b)%ell==4
assert ((a+1)**2+b*b)%ell==8
assert gcd(97,8)==1

# Mixed-precision equivalence is checked directly on a valuation grid.
cases=0
for xs in product(range(-2,3),repeat=3):
    for ys in product(range(-2,43,11),repeat=2):
        left=min([40*v for v in xs]+list(ys))>=40
        right=all(v>=1 for v in xs) and all(v>=40 for v in ys)
        assert left==right;cases+=1

# Verify (6) term by term.  A tuple records exponents of (D, delta, R).
r=16;M=40
common=(0,-(M+1),-M)  # factor distributed inside the degree-r norm
order_one_c=(M,1-M,0)
order_m_c=(1,0,0)
add=lambda x,y:tuple(a+b for a,b in zip(x,y))
scale=lambda n,x:tuple(n*a for a in x)
assert add(order_one_c,common)==(M,-2*M,-M)  # s_1^M
assert add(order_m_c,common)==(1,-(M+1),-M)  # s_M
# Outside the norm, delta^(1-r)/(delta^(rM+1) R^(rM))
# is exactly the r-th power of the common factor.
assert (0,(1-r)-(r*M+1),-r*M)==scale(r,(0,-(M+1),-M))
assert r*M==640 and r*M+1==641 and 1-r==-15 and 1-M==-39

root=Path(__file__).resolve().parents[2]
paths=['research/conceptual-simplification/NORM_PACKING.md',
       'research/conceptual-simplification/check_norm_packing.py',
       'manuscripts/quartic_v10.tex']
print(json.dumps({'status':'PASS_EXACT_FINITE_REGRESSIONS',
 'finite_field_norm_degrees':fields,'mixed_precision_cases':cases,
 'cyclotomic_field':{'conductor':97,'frobenius_class':5,
                     'ambient_frobenius_order':96,
                     'quotient_frobenius_order':16,
                     'relative_degree_over_Q_sqrt_2':16,
                     'gaussian_residue':[1,2],
                     'reduced_group_orders_mod_97':[4,8]},
 'detector_normalization':{'packed_order':640,'delta_exponent':641,
                           'order_one_rescaling':-39,'outer_rescaling':-15},
 'scope':'Finite norm anisotropy, mixed-valuation logic, and cyclotomic congruence arithmetic only.',
 'prime_pattern_application_reproved':False,'production_candidate':False,
 'independent_human_review':False,
 'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}},indent=2))
