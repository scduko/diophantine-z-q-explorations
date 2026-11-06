"""Tiny source and rational tests; no source flattening or quartic expansion."""
if not __debug__:raise RuntimeError('Assertions required')
import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

from anchor_four_kernel import install
from check_anchor_four import check_anchor,expected_anchor

BUILDER_SHA='c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912'


def valuation(x,p):
    x=F(x)
    if not x:return float('inf')
    n,d=abs(x.numerator),x.denominator;v=0
    while n%p==0:n//=p;v+=1
    while d%p==0:d//=p;v-=1
    return v


def evaluate(row,env):
    total=F(0)
    for coefficient,mon in row:
        term=F(coefficient)
        for index in mon:term*=env[index]
        total+=term
    return total


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--builder',type=Path,required=True);a=parser.parse_args()
    assert hashlib.sha256(a.builder.read_bytes()).hexdigest()==BUILDER_SHA
    spec=importlib.util.spec_from_file_location('isolated_anchor_four_builder',a.builder)
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    b.ANCHOR_SQUARINGS=25;b.write=lambda name,data:None
    b.make_anchor();old=b.MODULES['q_anchor']
    assert old['free']==2 and old['locals']==16 and len(old['residuals'])==6
    install(b);b.make_anchor();new=b.MODULES['q_anchor'];report=check_anchor(new)
    assert new==expected_anchor()
    assert max(len(mon) for row in new['residuals'] for _,mon in row)==2
    assert max(abs(c) for row in new['residuals'] for c,_ in row)==24
    assert {i for row in new['residuals'] for _,mon in row for i in mon}=={-26,0,1,2,3,4,5}
    rejected=[]
    def reject(name,change):
        bad=deepcopy(new);change(bad)
        try:check_anchor(bad)
        except ValueError:rejected.append(name)
        else:raise AssertionError('Accepted malformed anchor: '+name)
    reject('wrong shared constant',lambda m:m['residuals'][0][0][1].__setitem__(0,-25))
    reject('wrong constant square',lambda m:m['residuals'][0][0].__setitem__(0,-3))
    reject('unscaled trace',lambda m:m['residuals'][0][1].__setitem__(1,[2]))
    reject('wrong coefficient sign',lambda m:m['residuals'][0][3].__setitem__(0,3))
    reject('omitted input',lambda m:m['residuals'][0].pop())
    reject('wrong trace scale',lambda m:m['residuals'][1][0].__setitem__(0,-1))
    reject('wrong norm sign',lambda m:m['residuals'][1][-1].__setitem__(0,-24))
    reject('cubic residual',lambda m:m['residuals'][1][1][1].append(2))
    reject('missing trace equation',lambda m:m['residuals'].pop())
    reject('coefficient boolean alias',lambda m:m['residuals'][0][1].__setitem__(0,True))
    reject('coefficient float alias',lambda m:m['residuals'][0][1].__setitem__(0,1.0))
    reject('extra anchor call',lambda m:m['calls'].append(dict(module='q_primeparity',args=[3])))
    reject('extra local',lambda m:m.update(locals=5))
    reject('changed source dependency',lambda m:m.update(arithmetic_dependency='unreviewed'))
    rejected_wrong_order=False
    b.ANCHOR_SQUARINGS=24
    try:install(b)
    except ValueError:rejected_wrong_order=True
    assert rejected_wrong_order

    samples=[F(0),F(1),F(-1),F(1,2),F(1,3),F(1,6),F(3,5),F(-4,7),F(1,8),F(1,9)]
    pairs=0
    for a in samples:
        for b in samples:
            n=a*a+b*b;h=9+3*n;pairs+=1
            for p in (2,3):
                va,vb=valuation(a,p),valuation(b,p);m=min(va,vb)
                expected=2*m+(1 if p==2 and va==vb and m!=float('inf') else 0)
                assert valuation(n,p)==expected
                if m<0:
                    assert valuation(h,p)==expected+(1 if p==3 else 0)<0
                elif p==3:assert valuation(h,p)>=1
                else:assert valuation(h,p)==0 or valuation(h,p)>=2

    # Explicit rational quaternion witnesses include both zero inputs,
    # each separate zero input, and the two-unit case. Scale C arbitrarily.
    fixtures=[(0,0,F(1,2),F(5,2),0),(1,0,2,3,0),(0,1,2,3,0),(1,1,5,F(3,2),F(1,2))]
    checked=0
    for a,b,u,v,w in fixtures:
        h=F(9)+3*(F(a)**2+F(b)**2)
        assert h*h-8*F(u)**2-12*F(v)**2+24*F(w)**2==4
        for C in (F(3),F(5,7),F(-2)):
            env={-26:C,0:C*a,1:C*b,2:C*h,3:C*u,4:C*v,5:C*w}
            assert all(evaluate(row,env)==0 for row in new['residuals'])
            env[2]+=1
            assert evaluate(new['residuals'][0],env)!=0
            checked+=1
    print(json.dumps(dict(**report,malformed_cases=rejected,wrong_anchor_order_rejected=True,
                         rational_valuation_pairs=pairs,scaled_witness_fixtures=checked,
                         source_variable_saving=12,source_row_saving=4)))


if __name__=='__main__':main()
