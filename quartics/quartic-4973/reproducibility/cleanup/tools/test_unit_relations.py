"""Small positive and malformed fixtures; no released polynomial expansion."""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from types import SimpleNamespace
import json
import time

import check_localized as check
import probe_localized as loc
from probe_unit_relations import UnitSearch


def fixture():
    # 1=E, 2=theta, 3=R, 4=F, 5=x, 6=u, 7=v, 8=y, 9=z, 10=t.
    rows=[{(1,):1,(2,2):-1,():2}, {(3,4):1,(3,):-1,(1,1):-1},
          {(3,5):1,(6,7):-1}, {(5,8):1,(9,):-1}, {(6,8):1,(10,):-1}]
    proof={'kind':'product_unit','row':1,'factor':[[1,[3]]],
           'cofactor':[[1,[4]],[-1,[]]],'monomial':[1,1],'coefficient':1,
           'known':[[1,{'kind':'root_error','row':0,'error':1,'root':2}]]}
    data={'row':2,'variable':5,'denominator':[[1,[3]]],'numerator':[[1,[6,7]]],
          'nonzero':proof,'affected':[3],
          'reductions':[{'row':3,'terms':[{'support':4,'multiplier':{'terms':[[1,[7]]],'denominator':1}}]}],
          'cancellations':[{'row':3,'factors':[]}]}
    patches=[[2,[]],[3,[[1,[7,10]],[-1,[3,9]]]]]
    return rows,data,patches


def verify(rows,data,patches):
    incidence=defaultdict(set)
    for i,row in enumerate(rows):
        for v in check.vars_in(row): incidence[v].add(i)
    return check.relation_expected(rows,data,12,incidence,patches)


def main():
    assert __debug__
    rows,data,patches=fixture()
    verify(rows,data,patches)
    # A proportional denominator and numerator represent the same pivot.
    scaled=deepcopy(data)
    scaled['denominator']=[[7,[3]]]; scaled['numerator']=[[7,[6,7]]]
    scaled['reductions'][0]['terms'][0]['multiplier']['terms']=[[7,[7]]]
    verify(rows,scaled,patches)
    # Rational support multipliers are independently decoded.
    scaledrows=deepcopy(rows); scaledrows[4]={m:3*c for m,c in rows[4].items()}
    rational=deepcopy(data); rational['reductions'][0]['terms'][0]['multiplier']['denominator']=3
    verify(scaledrows,rational,patches)
    # Direct cancellation remains covered by the same identity rule.
    simple=deepcopy(rows); simple[2]={(3,5):1,(3,6):-1}
    cancellation=deepcopy(data); cancellation['numerator']=[[1,[3,6]]]
    cancellation['reductions'][0]['terms']=[]
    cancellation['cancellations'][0]['factors']=[{'factor':[[1,[3]]],'proof':deepcopy(data['nonzero'])}]
    verify(simple,cancellation,[[2,[]],[3,[[1,[6,8]],[-1,[9]]]]])
    mutations=[]
    def add(name, mutate):
        rr,dd,pp=fixture(); mutate(rr,dd,pp); mutations.append((name,rr,dd,pp))
    add('input0',lambda r,d,p:d.update(variable=0))
    add('missing_consumer',lambda r,d,p:d.update(affected=[]))
    add('duplicate_consumer',lambda r,d,p:d.update(affected=[3,3]))
    add('extra_consumer',lambda r,d,p:d.update(affected=[3,4]))
    add('missing_patch',lambda r,d,p:p.pop())
    add('duplicate_patch',lambda r,d,p:p.append(deepcopy(p[1])))
    add('extra_patch',lambda r,d,p:p.append([4,[]]))
    add('keep_definition',lambda r,d,p:p[0].__setitem__(1,[[1,[5]]]))
    add('wrong_output',lambda r,d,p:p[1][1][0].__setitem__(0,2))
    add('missing_relation',lambda r,d,p:d['reductions'][0].update(terms=[]))
    add('changed_support',lambda r,d,p:d['reductions'][0]['terms'][0].update(support=2))
    add('support_wrong_row',lambda r,d,p:d['reductions'][0]['terms'][0].update(support=0))
    add('duplicate_support',lambda r,d,p:d['reductions'][0]['terms'].append(deepcopy(d['reductions'][0]['terms'][0])))
    add('zero_denominator',lambda r,d,p:d['reductions'][0]['terms'][0]['multiplier'].update(denominator=0))
    add('multiplier_uses_removed',lambda r,d,p:d['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1,[5]]]))
    add('multiplier_unknown_var',lambda r,d,p:d['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1,[12]]]))
    add('multiplier_degree3',lambda r,d,p:d['reductions'][0]['terms'][0]['multiplier'].update(terms=[[1,[6,7,8]]]))
    add('wrong_numerator',lambda r,d,p:d.update(numerator=[[2,[6,7]]]))
    add('wrong_denominator',lambda r,d,p:d.update(denominator=[[1,[4]]]))
    add('root_square_rational',lambda r,d,p:r[0].update({():1}))
    add('wrong_root',lambda r,d,p:d['nonzero']['known'][0][1].update(root=3))
    add('no_root_unit_proof',lambda r,d,p:d['nonzero'].update(known=[]))
    add('duplicate_root_unit',lambda r,d,p:d['nonzero']['known'].append(deepcopy(d['nonzero']['known'][0])))
    add('zero_unit_coefficient',lambda r,d,p:d['nonzero'].update(coefficient=0))
    add('wrong_cofactor',lambda r,d,p:d['nonzero'].update(cofactor=[[1,[4]]]))
    add('wrong_certified_factor',lambda r,d,p:d['nonzero'].update(factor=[[1,[4]]]))
    add('proof_row_uses_removed',lambda r,d,p:r[1].update({(5,):1}))
    add('proof_support_replaced',lambda r,d,p:p.append([1,[]]))
    add('output_uses_removed',lambda r,d,p:p[1][1].append([1,[5]]))
    add('output_degree3',lambda r,d,p:p[1][1].append([1,[6,7,8]]))
    for name,rr,dd,pp in mutations:
        try: verify(rr,dd,pp)
        except AssertionError: continue
        raise AssertionError('malformed case accepted: '+name)
    # The producer must discover the exact new proof, then generate an event
    # that the separately implemented checker accepts.
    units=loc.discover_units(rows)
    assert any(p['kind']=='product_unit' for _,p in units[loc.signature({(3,):1})])
    args=SimpleNamespace(max_support_terms=12,max_consumers=8,max_high_terms=240,
        max_rows_per_term=16,max_generators=240,max_linear_terms=1200,max_bits=512,
        max_row_terms=96,allocated=12)
    search=UnitSearch(deepcopy(rows),args)
    candidates=search.candidates()
    proof=next(p for i,v,p in candidates if (i,v)==(2,5))
    event,changed,stats=search.attempt(2,5,proof,time.monotonic()+5)
    verify(rows,event['data'],event['patches'])
    assert stats['support_rows']>0
    print(json.dumps({'status':'PASS','positive_identities':4,'malformed_rejections':len(mutations),
                      'producer_discovery_and_replay':True},sort_keys=True))


if __name__=='__main__': main()
