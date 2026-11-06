"""Independent literal conic-pole module and batch-boundary delta.

The original batch must come from the independent conic auditor, not from
the proposed producer. This does not itself audit the whole source.
"""
from copy import deepcopy
import json


def equal(a,b):
    encode=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)
    return encode(a)==encode(b)


def expected_pole():
    variables=['D','U','L','z','e','p','c','w','s_p','q','j','k']
    equations=['denominator','Cayley value','scaled U','scaled square','scaled e',
               'first conic','shared expression','square','scaled q','second conic']
    return dict(name='q_conicpole',free=3,locals=12,residuals=[
        [[7,[]],[-4,[1,1]],[1,[3]]],
        [[-2,[0]],[1,[0,3]],[1,[3,4]]],
        [[-1,[2,4]],[1,[5]]],
        [[-1,[5,5]],[1,[6]]],
        [[-1,[0,7]],[1,[9]]],
        [[-17,[0]],[51,[7,9]],[1,[8,8]],[-34,[9]]],
        [[-17,[0,9]],[1,[6,9]],[1,[10]]],
        [[-1,[11,11]],[1,[13]]],
        [[-1,[0,12]],[1,[14]]],
        [[-867,[10,10]],[34,[10,13]],[-17,[12,14]],[1,[13,13]]],
    ],calls=[],construction_log=
        [['variable',i+3,'conic pole '+name] for i,name in enumerate(variables)]+
        [['equation',i,'conic pole '+name] for i,name in enumerate(equations)],
        input_layout='r;private theta;upper norm root',
        pole_model='private conic Cayley parameter 2*s_c',
        required_caller_premise='same theta^2-r*s_c^2=2',
        arithmetic_source_restriction=True)


def expected_batch(original):
    d=deepcopy(original)
    if d['name'] not in {'q_conic13','q_conic6','q_conic10'}:raise ValueError('Wrong conic module')
    W=d['norm_root'];W2=d['norm_root_square'];arg=d['parity_argument'];theta=d['conic_private']['theta']
    n=d['free']+d['locals'];nr=len(d['residuals'])
    if [W2,arg]!=[n-2,n-1] or d['calls']!=[{'module':'q_primeparity','args':[arg]}]:
        raise ValueError('Wrong old boundary')
    if not equal(d['residuals'][-2:],[[[-1,[W,W]],[1,[W2]]],[[-1,[0,W2]],[1,[arg]]]]):
        raise ValueError('Wrong old argument rows')
    expected_log=[['variable',W2,'batched square'],['equation',nr-2,'batched square'],
                  ['variable',arg,'parity argument'],['equation',nr-1,'parity argument']]
    if d['construction_log'][-4:]!=expected_log:raise ValueError('Wrong old boundary log')
    if d['parity_module']!='q_primeparity':raise ValueError('Wrong old pole')
    # Deleted coordinates must not appear in any retained row.
    for row in d['residuals'][:-2]:
        if any(v in {W2,arg} for _,mon in row for v in mon):raise ValueError('Old tail has outside use')
    d['locals']-=2;d['residuals']=d['residuals'][:-2];d['construction_log']=d['construction_log'][:-4]
    d['calls']=[{'module':'q_conicpole','args':[0,theta,W]}]
    del d['norm_root_square'];del d['parity_argument']
    d.update(parity_module='q_conicpole',pole_model='private conic Cayley parameter 2*s_c',
        pole_inputs=[0,theta,W],
        semantics='Private theta^2-r*s_c^2=2; original packed fields and upper tree; conic-conditioned pole at (r,theta,root)')
    return d


def check_pole(module):
    if not equal(module,expected_pole()):raise ValueError('Conic-pole module differs from literal specification')
    return dict(status='PASS: literal module only',private_variables=12,rows=10,degree=2,max_coefficient=867)


def check_batch(proposed,original):
    if not equal(proposed,expected_batch(original)):raise ValueError('Conic batch differs outside approved tail delta')
    return dict(status='PASS: full batch delta only',removed_variables=2,removed_rows=2)
