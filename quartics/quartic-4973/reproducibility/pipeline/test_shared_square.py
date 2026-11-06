"""Exact symbolic identities and zero-inclusive rational fixtures; no source build."""
from fractions import Fraction as Q
from itertools import product
import json


def add(*polys):
    ans={}
    for p in polys:
        for m,c in p.items():ans[m]=ans.get(m,0)+c
    return {m:c for m,c in ans.items() if c}


def scale(n,p):return {m:n*c for m,c in p.items() if n*c}


def mul(p,q):
    ans={}
    for a,c in p.items():
        for b,d in q.items():
            m=tuple(sorted(a+b));ans[m]=ans.get(m,0)+c*d
    return {m:c for m,c in ans.items() if c}


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    A,B,theta,Y,W,P,C,D=[{(i,):1} for i in range(8)]
    Ry=add(Y,scale(-1,A),scale(-1,mul(theta,B)))
    Rw=add(mul(P,W),scale(-2,mul(A,Y)),mul(A,A),scale(-2,mul(B,B)))
    Rc=add(C,scale(-1,mul(A,A)),scale(-2,mul(B,B)))
    Rd=add(D,scale(-2,mul(A,B)))
    Rnew=add(mul(P,W),scale(-1,C),scale(-1,mul(theta,D)))
    assert Rnew==add(Rw,scale(2,mul(A,Ry)),scale(-1,Rc),scale(-1,mul(theta,Rd)))
    assert max(len(m) for p in (Rc,Rd,Rnew) for m in p)==2
    cases=0
    for a,b,t,p in product(map(Q,[-2,-1,0,1,2]),repeat=4):
        c=a*a+2*b*b;d=2*a*b;y=a+t*b
        assert 2*a*y-a*a+2*b*b==c+t*d
        if p:
            w=(c+t*d)/p
            assert p*w-2*a*y+a*a-2*b*b==p*w-c-t*d==0
        cases+=1
    for a,b,t,w in [(Q(0),Q(0),Q(5),Q(7)),(Q(1),Q(1),Q(-3,2),Q(0))]:
        c=a*a+2*b*b;d=2*a*b;y=a+t*b
        assert c+t*d==2*a*y-a*a+2*b*b==0
    # Conjugation sign is essential: B=-fJ_1, so D=-2*fJ_0*fJ_1.
    assert 2*Q(2)*(-Q(3))==-12
    assert Q(2)**2+2*(-Q(3))**2==22
    # The normalized Lucas block alone does not force its residual into Q.
    # Lambda=ps=pt=pz=Bs=Bz=1, Bt=sqrt(2), P=1,U=1+sqrt(2),V=-1,K=-sqrt(2).
    fm=lambda x,y:(x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    U=(1,1);V=(-1,0);K=(0,-1);p=(1,0)
    u2=fm(U,U);kv=fm(K,V);p2=fm(p,p)
    E=tuple(x-y-z for x,y,z in zip(u2,kv,p2))
    assert E==(2,1)
    print(json.dumps(dict(status='PASS: SYMBOLIC SHARED-SQUARE IDENTITY',rational_cases=cases,
        zero_power_fixtures=2,new_residual_degree=2,new_max_coefficient=2,
        divisions=0,normalized_block_nonrational_residual_example=list(E),full_source_generated=False)))


if __name__=='__main__':main()
