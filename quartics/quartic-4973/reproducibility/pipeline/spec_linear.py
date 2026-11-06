"""Independent literal quadratic specifications; not whole-source acceptance."""
from copy import deepcopy
import json

def module(normalized=False):
    if normalized:
        name='q_linearnormalpole';variables=['l','z','e','p','c','w','s_p','q','j','k']
        rows=[[[2,[1,2]],[-3,[2]],[1,[3]]],
              [[-1,[3,3]],[1,[4]]],
              [[-1,[0,5]],[1,[7]]],
              [[-17,[0]],[51,[5,7]],[1,[6,6]],[-34,[7]]],
              [[1,[4,7]],[-17,[5]],[1,[8]]],
              [[-1,[9,9]],[1,[11]]],
              [[-1,[0,10]],[1,[12]]],
              [[-867,[8,8]],[34,[8,11]],[-17,[10,12]],[1,[11,11]]]]
        labels=['linear product','scaled square','scaled e','first conic','shared expression','square','scaled q','second conic']
    else:
        name='q_linearconicpole';variables=['U','L','z','e','p','c','w','s_p','q','j','k']
        rows=[[[-3,[0]],[2,[0,1]],[1,[3]]],
              [[-1,[2,3]],[1,[4]]],
              [[-1,[4,4]],[1,[5]]],
              [[-1,[0,6]],[1,[8]]],
              [[-17,[0]],[51,[6,8]],[1,[7,7]],[-34,[8]]],
              [[-17,[0,8]],[1,[5,8]],[1,[9]]],
              [[-1,[10,10]],[1,[12]]],
              [[-1,[0,11]],[1,[13]]],
              [[-867,[9,9]],[34,[9,12]],[-17,[11,13]],[1,[12,12]]]]
        labels=['linear unit','scaled U','scaled square','scaled e','first conic','shared expression','square','scaled q','second conic']
    return dict(name=name,free=3,locals=len(variables),residuals=rows,calls=[],
        construction_log=[['variable',3+i,'linear pole '+v] for i,v in enumerate(variables)]+
            [['equation',i,'linear pole '+v] for i,v in enumerate(labels)],
        input_layout='r;private theta;upper norm root',pole_model='linear unit 3-2*theta',
        required_caller_premise='same theta^2-r*s_c^2=2',arithmetic_source_restriction=True,
        r_normalized=normalized)

def check(value,normalized=False):
    encode=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
    if encode(value)!=encode(module(normalized)):raise ValueError('Wrong literal linear pole module')
    return dict(status='PASS: literal module only',variables=10 if normalized else 11,rows=8 if normalized else 9,degree=2,max_coefficient=867)
