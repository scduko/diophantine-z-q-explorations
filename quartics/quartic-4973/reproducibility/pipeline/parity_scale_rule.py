"""Independent exact checker for square-factor/parity fusion.

This module imports neither a producer nor a source compiler. See the proof
for both rational maps and the zero-square-factor branch.
"""
if not __debug__:raise RuntimeError('Assertions must remain enabled')
from collections import defaultdict
from fractions import Fraction as F
from math import gcd,lcm


def add(*terms):
    out=defaultdict(F)
    for coefficient,row in terms:
        for mon,c in row.items():out[mon]+=coefficient*c
    return {m:c for m,c in out.items() if c}


def mul(left,right):
    out=defaultdict(F)
    for m,c in left.items():
        for n,d in right.items():out[tuple(sorted(m+n))]+=c*d
    return {m:c for m,c in out.items() if c}


def var(i):return {(i,):F(1)}


def norm(row):
    if not row:return ()
    den=lcm(*(F(c).denominator for c in row.values()))
    ints={m:int(c*den) for m,c in row.items() if c}
    common=gcd(*ints.values())
    if ints[min(ints)]<0:common=-common
    return tuple(sorted((m,c//common) for m,c in ints.items()))


def variables(row):return {v for m in row for v in m}


def old_rows(r,W,B2,b,private):
    r,W,B2,b=map(var,(r,W,B2,b))
    u,v,a,z,e,p,c,w,s,q,j,k=map(var,private)
    return [add((1,B2),(-1,mul(W,W))),add((1,b),(-1,mul(r,B2))),
        add((1,z),(-1,mul(u,u))),add((1,a),(-1,mul(b,v))),
        add((1,z),(1,mul(v,a)),(-1,mul(b,b))),
        add((1,c),(-1,mul(b,e))),
        add((1,mul(p,p)),(-17,b),(-34,c),(51,mul(e,c))),
        add((1,w),(-17,mul(b,c)),(1,mul(c,z))),
        add((1,j),(-1,mul(s,s))),add((1,k),(-1,mul(b,q))),
        add((1,mul(j,j)),(34,mul(j,w)),(-867,mul(w,w)),(-17,mul(q,k)))]


def new_rows(r,W,private):
    r,W=map(var,(r,W));u,v,a,L,z,e,p,c,w,s,q,j,k=map(var,private)
    return [add((1,a),(-1,mul(r,v))),
        add((1,mul(u,u)),(1,mul(v,a)),(-1,mul(r,r))),
        add((1,L),(-1,mul(W,u))),add((1,z),(-1,mul(L,L))),
        add((1,c),(-1,mul(r,e))),
        add((1,mul(p,p)),(-17,r),(-34,c),(51,mul(e,c))),
        add((1,w),(-17,mul(r,c)),(1,mul(c,z))),
        add((1,j),(-1,mul(s,s))),add((1,k),(-1,mul(r,q))),
        add((1,mul(j,j)),(34,mul(j,w)),(-867,mul(w,w)),(-17,mul(q,k)))]


def check_rule(rows,incidence,data,nextvar):
    assert set(data)=={'factor','square_factor','squared','argument','old_witnesses','argument_rows','residual_rows','new_variables'}
    r,W,B2,b=(data[k] for k in ('factor','square_factor','squared','argument'))
    old=data['old_witnesses'];new=data['new_variables']
    assert type(nextvar) is int and nextvar>0
    assert all(type(v) is int and 0<=v<nextvar for v in (r,W))
    assert type(old) is list and len(old)==12
    removed=[B2,b]+old
    assert all(type(v) is int and 0<v<nextvar for v in removed)
    assert len(set(removed))==14 and not set(removed)&{r,W}
    assert type(new) is list and all(type(v) is int for v in new)
    assert new==list(range(nextvar,nextvar+13))
    ar=data['argument_rows'];rr=data['residual_rows']
    assert type(ar) is list and len(ar)==2 and type(rr) is list and len(rr)==9
    ids=ar+rr
    assert all(type(i) is int and 0<=i<len(rows) for i in ids)
    assert len(set(ids))==11
    selected=set(ids)
    for v in removed:
        assert incidence.get(v,set())<=selected, 'Outside use of deleted parity coordinate'
    for i,expected in zip(ids,old_rows(r,W,B2,b,old)):
        assert all(len(m)<=2 for m in rows[i]), 'Old row is not quadratic'
        assert norm(rows[i])==norm(expected), 'Wrong old parity or argument row'
    replacements=new_rows(r,W,new)
    assert len(replacements)==10 and all(len(m)<=2 for row in replacements for m in row)
    patches={i:{} for i in selected}
    for i,row in zip(sorted(selected),replacements):patches[i]=dict(norm(row))
    return patches,nextvar+13


def old_to_new(r,W,old):
    r,W=F(r),F(W)
    if not W:return [r,F(0),F(0),F(0),F(0),F(1),F(0),r,17*r*r,17*r,F(0),289*r*r,F(0)]
    uo,vo,ao,zo,e,po,co,wo,so,qo,jo,ko=map(F,old)
    u,v=uo/W**2,vo/W;L=W*u
    p,w,s,q=po/W,wo/W**4,so/W**2,qo/W**3
    return [u,v,r*v,L,L*L,e,p,r*e,w,s,q,s*s,r*q]


def new_to_old(r,W,new):
    r,W=F(r),F(W);b=r*W*W
    u,v,a,L,z,e,p,c,w,s,q,j,k=map(F,new)
    uo,vo,po,so,qo=W*W*u,W*v,W*p,W*W*s,W**3*q
    return [uo,vo,b*vo,uo*uo,e,po,b*e,W**4*w,so,qo,so*so,b*qo]
