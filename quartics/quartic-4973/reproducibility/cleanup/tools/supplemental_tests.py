"""Independent small regressions for the localized elimination trust boundary."""
if not __debug__:
    raise RuntimeError('These checks require assertions')

import argparse
from collections import defaultdict
from copy import deepcopy
import importlib.util
import json
from pathlib import Path


def load(path):
    spec = importlib.util.spec_from_file_location('reviewed_localized_rule', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def incidence(rows):
    result = defaultdict(set)
    for i, row in enumerate(rows):
        for monomial in row:
            for v in monomial:
                result[v].add(i)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elimination', type=Path)
    args = parser.parse_args()
    c = load(args.elimination/'check_localized.py')
    root = {'kind':'root_error','row':0,'error':1,'root':2}
    rproof = {'kind':'product_unit','row':1,'factor':[[1,[3]]],
              'cofactor':[[1,[4]],[-1,[]]],'monomial':[1,1],
              'coefficient':1,'known':[[1,root]]}
    fproof = deepcopy(rproof)
    fproof['factor'], fproof['cofactor'] = fproof['cofactor'], fproof['factor']
    base = [{(1,):1,(2,2):-1,():2}, {(3,4):1,(3,):-1,(1,1):-1}]
    rejected = []

    def reject(label, function):
        try:
            function()
        except AssertionError:
            rejected.append(label)
            return
        raise AssertionError('Accepted '+label)

    # Independent pivot R*x=u; the retained first-leaf equation certifies R.
    rows = base + [{(3,5):1,(6,):-1}, {(5,7):1,(8,):-1}]
    data = {'row':2,'variable':5,'denominator':[[1,[3]]],
            'numerator':[[1,[6]]],'nonzero':rproof,'affected':[3],
            'reductions':[{'row':3,'terms':[]}],
            'cancellations':[{'row':3,'factors':[]}]}
    patches = [[2,[]],[3,[[1,[6,7]],[-1,[3,8]]]]]
    assert c.relation_expected(rows,data,12,incidence(rows),patches)
    c.prove_unit(rows,{(4,):1,():-1},fproof,5,12)

    # The tempting circular deletion: remove R from R*(F-1)=E^2 and R*x=0,
    # cancel E^2 to leave x=0, and wrongly use the deleted row to prove F-1.
    # The putative new system permits theta=0,E=-2,F=1,x=0, while no R can
    # satisfy its deleted first-leaf row. Every algebraic identity is valid;
    # it is specifically the missing retained nonzero proof that invalidates it.
    circular_rows = base + [{(3,5):1}]
    circular = {'row':1,'variable':3,'denominator':[[1,[4]],[-1,[]]],
                'numerator':[[1,[1,1]]],'nonzero':fproof,'affected':[2],
                'reductions':[{'row':2,'terms':[]}],
                'cancellations':[{'row':2,'factors':[
                    {'factor':[[1,[1]]],'proof':root},
                    {'factor':[[1,[1]]],'proof':root}]}]}
    reject('deleted first-leaf row cannot prove its own denominator',
           lambda: c.relation_expected(circular_rows,circular,12,incidence(circular_rows),[[1,[]],[2,[[1,[5]]]]]))
    assert -2-0**2+2 == 0 and (1-1) == 0 and (-2)**2 != 0

    reject('removed R in direct proof', lambda: c.prove_unit(base,{(4,):1,():-1},fproof,3,12))
    reject('removed F in direct proof', lambda: c.prove_unit(base,{(3,):1},rproof,4,12))
    hidden = deepcopy(base)
    hidden[0] = {(1,):1,(5,5):-1,():2}
    hidden_proof = deepcopy(rproof); hidden_proof['known'][0][1]['root'] = 5
    reject('removed variable hidden in child proof', lambda: c.prove_unit(hidden,{(3,):1},hidden_proof,5,12))

    bad = deepcopy(data); bad['nonzero']['row'] = 2
    reject('pivot row used as nonzero support', lambda: c.relation_expected(rows,bad,12,incidence(rows),patches))
    badpatch = deepcopy(patches); badpatch[1][1].append([1,[12]])
    reject('unallocated output coordinate', lambda: c.relation_expected(rows,data,12,incidence(rows),badpatch))
    bad = deepcopy(data); bad['cancellations'][0]['factors'] = [{'factor':[[1,[4]]],'proof':rproof}]
    reject('uncertified canceled factor', lambda: c.relation_expected(rows,bad,12,incidence(rows),patches))
    stale = deepcopy(rows); stale[0][()] = 1
    reject('stale child proof reread against current row', lambda: c.relation_expected(stale,data,12,incidence(stale),patches))

    tautology = {'kind':'product_unit','row':0,'factor':[[1,[3]]],
                 'cofactor':[[1,[4]]],'monomial':[3,4],'coefficient':1,'known':[]}
    reject('tautological product identity', lambda: c.prove_unit([{}],{(3,):1},tautology,5,12))

    # A deliberately cyclic in-memory proof graph must reject, rather than
    # recurse until a Python resource error. JSON proofs cannot contain object
    # cycles; the same guard also rejects repeated proof claims in their trees.
    cycle_rows = [{(3,4):1,(1,1):-1}]
    cp = {'kind':'product_unit','row':0,'factor':[[1,[3]]],
          'cofactor':[[1,[4]]],'monomial':[1,1],'coefficient':1}
    ce = {'kind':'product_unit','row':0,'factor':[[1,[1]]],
          'cofactor':[[1,[1]]],'monomial':[3,4],'coefficient':1}
    cf = {'kind':'product_unit','row':0,'factor':[[1,[4]]],
          'cofactor':[[1,[3]]],'monomial':[1,1],'coefficient':1}
    cp['known'] = [[1,ce]]; ce['known'] = [[3,cp],[4,cf]]; cf['known'] = [[1,ce]]
    reject('cyclic unit proof graph', lambda: c.prove_unit(cycle_rows,{(3,):1},cp,5,12))
    print(json.dumps({'status':'PASS','independent_positive_cases':2,
                      'rejected':rejected,'rejection_count':len(rejected)},indent=2))


if __name__ == '__main__':
    main()
