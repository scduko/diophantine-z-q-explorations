"""Small source-template and rational-map tests; no full source or expansion."""
if not __debug__:raise RuntimeError('Assertions must remain enabled')
import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import conic_pole_kernel as kernel
import check_conic_pole as checker
import parity_scale_rule as scale


def load(name,path,digest):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def evaluate(row,env):
    total=F(0)
    for coefficient,mon in row:
        term=F(coefficient)
        for v in mon:term*=env[v]
        total+=term
    return total


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--builder',type=Path,required=True);p.add_argument('--emitter',type=Path,required=True)
    a=p.parse_args()
    b=load('tiny_conic_pole_builder',a.builder,'c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912')
    e=load('tiny_conic_pole_emitter',a.emitter,'42fcb55ec95be9ee34e98c5d0b0e672062b7cce6c5f9f9d0e676edff72e5ed86')
    b.write=lambda *args:None
    # Construct only three isolated batches with the pinned emitter. The
    # complete installed source and theorem are outside this tiny fixture.
    for spec in e.MODES.values():e.make_conic_batch(b,spec['batch'],spec['orders'])
    originals=deepcopy(b.MODULES);b.MODULES.clear();b._private_conic_installed=True
    kernel.install(b)
    for spec in e.MODES.values():e.make_conic_batch(b,spec['batch'],spec['orders'])
    pole=b.MODULES['q_conicpole'];checker.check_pole(pole)
    for name,old in originals.items():checker.check_batch(b.MODULES[name],old)
    assert pole['locals']==12 and len(pole['residuals'])==10
    assert max(len(mon) for row in pole['residuals'] for _,mon in row)==2
    assert max(abs(c) for row in pole['residuals'] for c,_ in row)==867
    rejected=[]
    for i in range(10):
        bad=deepcopy(pole);bad['residuals'][i][0][0]+=1
        try:checker.check_pole(bad)
        except ValueError:rejected.append('changed pole row '+str(i))
        else:raise AssertionError(i)
    for name,old in originals.items():
        for label,change in [
            ('wrong theta call',lambda m:m['calls'][0]['args'].__setitem__(1,0)),
            ('changed conic',lambda m:m['residuals'][1][0].__setitem__(0,999)),
            ('changed field',lambda m:m['field_bindings'][0].update(order=999)),
            ('extra call',lambda m:m['calls'].append({'module':'q_primeparity','args':[0]}))]:
            bad=deepcopy(b.MODULES[name]);change(bad)
            try:checker.check_batch(bad,old)
            except ValueError:rejected.append(name+': '+label)
            else:raise AssertionError(label)
    samples=[]
    for theta in [F(0),F(1),F(3,2),F(2),F(-5,2)]:
        for sc in [F(1),F(2,3)]:samples.append((theta,sc,F(0),1))
    for sc in [F(1),F(2,3)]:
        for W in [F(-2),F(1),F(3,5)]:samples.append((F(3,2),sc,W,1))
    for root in [F(1),F(2,3)]:
        for W in [F(-2),F(3,5)]:samples.append((F(5,2),1/(2*root),W,0))
    for theta,sc,W,ev in samples:
        r=(theta*theta-2)/(sc*sc);D=4*theta*theta-7;U=r*(2-D)/D
        L=W*U;z=L*L;c=r*ev;w=c*(17*r-z)
        if ev:pval=F(0);sp=17*r;q=F(0);assert not L
        else:
            root=1/(2*sc);pval=17*root;sp=q=F(0)
        vals=[D,U,L,z,F(ev),pval,c,w,sp,q,sp*sp,r*q]
        env={0:r,1:theta,2:W,**dict(zip(range(3,15),vals))}
        assert all(evaluate(row,env)==0 for row in pole['residuals'])
        v=4*r*sc/D
        assert U*U+r*v*v==r*r
        scaled=[U,v,r*v,L,z,F(ev),pval,c,w,sp,q,sp*sp,r*q]
        encoded=scale.new_rows(0,1,list(range(2,15)))
        senv={0:r,1:W,**dict(zip(range(2,15),scaled))}
        assert all(evaluate([[a,list(m)] for m,a in row.items()],senv)==0 for row in encoded)
        if W:
            to=2*sc/W;uo=W*W*U;arg=r*W*W
            assert uo*(1+arg*to*to)==arg*(1-arg*to*to)
    print(json.dumps({'status':'PASS: tiny source and rational fixtures only','batches':len(originals),
        'negative_cases':rejected,'rational_fixtures':len(samples),'new_private':12,'rows':10,
        'max_residual_coefficient':867,'full_source_acceptance':False}))


if __name__=='__main__':main()
