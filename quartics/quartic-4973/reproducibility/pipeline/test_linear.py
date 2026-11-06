"""Tiny exact module, polynomial scaling, zero-branch and valuation tests."""
if not __debug__:raise RuntimeError('Assertions required')
import argparse,hashlib,importlib.util,json
from fractions import Fraction as F
from copy import deepcopy
from pathlib import Path
import emit_linear,spec_linear

def add(*terms):
    out={}
    for scalar,row in terms:
        for mon,c in row.items():out[mon]=out.get(mon,0)+scalar*c
    return {m:c for m,c in out.items() if c}
def mul(a,b):
    out={}
    for m,c in a.items():
        for n,d in b.items():
            key=tuple(sorted(m+n));out[key]=out.get(key,0)+c*d
    return {m:c for m,c in out.items() if c}
def power(a,n):
    out={():1}
    for _ in range(n):out=mul(out,a)
    return out
def evaluate(row,env):
    out={}
    for c,mon in row:
        term={():c}
        for v in mon:term=mul(term,env[v])
        out=add((1,out),(1,term))
    return out
def valuation(q,p):
    q=F(q)
    if not q:return 10**9
    out=0;n,d=abs(q.numerator),q.denominator
    while n%p==0:n//=p;out+=1
    while d%p==0:d//=p;out-=1
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--builder',type=Path,required=True);ap.add_argument('--report',type=Path);a=ap.parse_args()
    assert hashlib.sha256(a.builder.read_bytes()).hexdigest()=='c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912'
    s=importlib.util.spec_from_file_location('linear_pole_builder',a.builder);b=importlib.util.module_from_spec(s);s.loader.exec_module(b);b.write=lambda *args:None
    negative=[]
    for normalized in (False,True):
        obj=emit_linear.make(b,normalized);spec_linear.check(obj,normalized)
        assert max(len(mon) for row in obj['residuals'] for _,mon in row)==2
        for i in range(len(obj['residuals'])):
            bad=deepcopy(obj);bad['residuals'][i][0][0]+=1
            try:spec_linear.check(bad,normalized)
            except ValueError:negative.append((normalized,i))
            else:raise AssertionError('Changed row accepted')
        bad=deepcopy(obj);bad['calls']=[{'module':'hidden','args':[0]}]
        try:spec_linear.check(bad,normalized)
        except ValueError:negative.append((normalized,'hidden call'))
        else:raise AssertionError('Hidden call accepted')
    direct=spec_linear.module()['residuals'];normal=spec_linear.module(True)['residuals']
    v=[{(i,):1} for i in range(13)];r=v[0];g=add((3,{():1}),(-2,v[1]));r2=power(r,2)
    env={0:v[0],1:v[1],2:v[2],3:mul(r,g),4:mul(r,v[3]),5:mul(r2,v[4]),
         6:v[5],7:v[6],8:v[7],9:mul(r2,v[8]),10:mul(r,v[9]),11:mul(r2,v[10]),12:mul(r2,v[11]),13:mul(r2,v[12])}
    dn=[evaluate(row,env) for row in direct];nn=[evaluate(row,dict(enumerate(v))) for row in normal]
    expected=[{},mul(r,nn[0]),mul(r2,nn[1]),nn[2],nn[3],
        add((1,mul(r2,nn[4])),(-17,mul(r,nn[2]))),mul(r2,nn[5]),mul(r2,nn[6]),mul(power(r,4),nn[7])]
    assert dn==expected,'Scaling polynomial identity'
    cases=[]
    for theta in (F(0),F(1),F(3,2),F(2),F(-5,2)):
        for sc in (F(1),F(2,3)):cases.append((theta,sc,F(0),1))
    for sc in (F(1),F(2,3)):
        for W in (F(-2),F(1),F(3,5)):cases.append((F(3,2),sc,W,1))
    for root in (F(1),F(2,3)):
        for W in (F(-2),F(3,5)):cases.append((F(5,2),1/(2*root),W,0))
    for theta,sc,W,e in cases:
        r=(theta*theta-2)/(sc*sc);l=(3-2*theta)*W;z=l*l;c=r*e;w=17*e-c*z
        p=F(0) if e else 17/(2*sc);sp=F(17) if e else F(0);q=F(0)
        values=[r,theta,W,l,z,F(e),p,c,w,sp,q,sp*sp,r*q]
        assert all(not evaluate(row,{i:{():x} for i,x in enumerate(values)}) for row in normal)
    checked=0
    for den in range(1,7):
        for num in range(-12,13):
            theta=F(num,den)
            for sc in (F(1),F(2,3),F(5,7)):
                r=(theta*theta-2)/(sc*sc)
                for prime in (3,5,7,11,17,19,23):
                    if valuation(r,prime)%2:
                        assert valuation(theta,prime)>=0
                        assert valuation(3-2*theta,prime)==valuation(3+2*theta,prime)==0
                        checked+=1
    result=dict(status='PASS: tiny algebra and fixtures only',literal_negative_cases=len(negative),
        polynomial_scaling_identities=9,rational_solution_fixtures=len(cases),odd_valuation_fixtures=checked,
        direct=dict(variables=11,rows=9),normalized=dict(variables=10,rows=8),degree=2,max_coefficient=867,
        full_source_acceptance=False)
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
