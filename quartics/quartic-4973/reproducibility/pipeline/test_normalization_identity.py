"""Tiny exact normalization fixtures; not a whole-source arithmetic checker."""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from math import isqrt
from pathlib import Path


def add(a,b):
    result=dict(a)
    for mon,c in b.items():result[mon]=result.get(mon,Q(0))+c
    return {mon:c for mon,c in result.items() if c}


def scale(a,c):return {mon:v*c for mon,v in a.items() if v*c}


def mul(a,b):
    result={}
    for m,c in a.items():
        for n,d in b.items():
            mon=tuple(x+y for x,y in zip(m,n))
            result[mon]=result.get(mon,Q(0))+c*d
    return {mon:c for mon,c in result.items() if c}


def square(a):return mul(a,a)


def symbolic_identity():
    one={(0,0,0):Q(1)};S={(1,0,0):Q(1)};T={(0,1,0):Q(1)};Z={(0,0,1):Q(1)}
    sm2=add(S,scale(one,-2))
    # S^2 * (U^2-KV-P^2), after clearing the common S denominator.
    numerator=add(add(square(add(T,scale(mul(sm2,Z),-1))),
                      scale(mul(square(sm2),mul(T,Z)),-1)),scale(one,-1))
    wanted=add(add(add(square(T),scale(mul(mul(S,sm2),mul(T,Z)),-1)),
                   mul(square(sm2),square(Z))),scale(one,-1))
    assert numerator==wanted
    return len(numerator)


def F(s,t,z):return t*t-s*(s-2)*t*z+(s-2)**2*z*z-1


def block(bs,bt,bz,ps,pt,pz,p,u,v,k,e):
    return (p*bs-ps,(u+v)*pt-p*bt,k*pt-(1-2*p)*bt,
            v*pz-(1-2*p)*bz,e-u*u+k*v+p*p)


def ordinary_case(s,t,z):
    ps,pt,pz=Q(2),Q(-3),Q(5)
    bs,bt,bz=s*ps,t*pt,z*pz
    p=1/s;v=(1-2*p)*z;u=p*t-v;k=(1-2*p)*t;e=u*u-k*v-p*p
    assert all(value==0 for value in block(bs,bt,bz,ps,pt,pz,p,u,v,k,e))
    assert s*s*e==F(s,t,z)
    return e


def valuation(value,p):
    value=Q(value)
    if not value:return None
    n,d=abs(value.numerator),value.denominator;result=0
    while n%p==0:n//=p;result+=1
    while d%p==0:d//=p;result-=1
    return result


def run():
    terms=symbolic_identity();count=0
    for s,t,z in product(map(Q,[-3,-1,Q(1,2),1,2,5]),map(Q,[-2,1,3]),map(Q,[-1,2,Q(5,2)])):
        ordinary_case(s,t,z);count+=1
    assert count==54
    # C_s=2 requires no division by 1-2P. V=K=0 is legitimate.
    assert ordinary_case(Q(2),Q(3),Q(5))==2
    # Algebraic ratio-block branches only. These are not claimed to be full
    # elliptic/logarithm witnesses, and cannot occur at a consumed prime.
    assert all(x==0 for x in block(Q(1),Q(1),Q(1),Q(0),Q(1),Q(1),
                                  Q(0),Q(-1),Q(1),Q(1),Q(0)))
    assert all(x==0 for x in block(Q(1),Q(1),Q(1),Q(1,2),Q(1),Q(0),
                                  Q(1,2),Q(-3,2),Q(2),Q(0),Q(2)))
    # At a prime where C_s is nonunit, E order40 implies F order42.
    prime=1000003
    assert all(prime%d for d in range(2,isqrt(prime)+1))
    s=Q(prime);t=Q(prime+prime**41);z=Q(1,prime-2)
    e=ordinary_case(s,t,z)
    assert valuation(s,prime)==1 and valuation(e,prime)==40 and valuation(F(s,t,z),prime)==42
    return dict(status='PASS',symbolic_identity_terms=terms,ordinary_exact_cases=count,
                special_Cs2=True,ratio_only_zero_ordinate_cases=2,
                nonunit_case=dict(prime=prime,v_Cs=1,v_E=40,v_F=42),
                scope='Exact polynomial identity and ratio-block fixtures; no whole-source or prime-pattern certification')


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path)
    args=parser.parse_args();result=run();text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.out:args.out.write_text(text,encoding='utf-8')
    print(text,end='')


if __name__=='__main__':main()
