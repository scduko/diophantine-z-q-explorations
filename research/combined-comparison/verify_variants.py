"""Check the constant-chain transformation and arithmetic budgets separately.

Does not import the builder, compiler, or explore.py. Upstream's independent
checker separately verifies all gates, reductions, and coefficient tables.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

def require(ok, message):
    if not ok: raise ValueError(message)

def read(path):
    return json.loads(path.read_text())

def canonical(terms):
    result = {}
    for t in terms:
        key = t['sPower'], tuple(t['monomial'])
        result[key] = result.get(key, Fraction()) + Fraction(t['coefficient'])
    return {k: c for k, c in result.items() if c}

def check_chain(old, new, last_power):
    count = last_power - 9
    old_ids = [c['id'] for c in old['coordinates']]
    first = max(old_ids) + 1
    fresh = list(range(first, first + count))
    require(new['coordinates'][:len(old_ids)] == old['coordinates'], 'original coordinate metadata changed')
    require([c['id'] for c in new['coordinates'][len(old_ids):]] == fresh, 'chain coordinate inventory')
    require(new.get('gates') == old.get('gates'), 'original gate equations changed')
    require(len(new['residuals']) == len(old['residuals']) + count, 'chain residual inventory')
    touched = 0
    for a, b in zip(old['residuals'], new['residuals']):
        expected = {}
        for (power, m), c in canonical(a['terms']).items():
            require(power == 0 or (power == 1 and len(m) == 1), 'S must occur only linearly times an anchor coordinate')
            touched += bool(power)
            key = 0, tuple(sorted(m + (fresh[-1],)*power))
            expected[key] = expected.get(key, Fraction()) + c
        require(b['id'] == a['id'] and canonical(b['terms']) == expected, 'source row changed beyond S substitution')
    require(touched == 1, 'expected exactly one fixed-parameter term')
    exponent = 1024
    for i, row in enumerate(new['residuals'][len(old['residuals']):]):
        expected = {(0, (fresh[i],)): Fraction(1)}
        if i == 0: expected[0, ()] = -3**1024
        else:
            expected[0, (fresh[i-1], fresh[i-1])] = Fraction(-1)
            exponent *= 2
        require(canonical(row['terms']) == expected, 'incorrect constant-chain equation')
    require(exponent == 2**last_power, 'wrong terminal exponent')
    return count

def budgets():
    # log2(3)>3/2 follows from 3^2>2^3, with no floating point input.
    require(3**2 > 2**3, 'logarithm comparison')
    anchor_lower = 1 + Fraction(3,2)*(2**24-1)
    threshold_upper = 10*(6+2093966)
    require(anchor_lower > threshold_upper, 'smaller anchor is insufficient')
    for order in [24, 32]:
        require(10*(1-Fraction(19,order)) > 1, 'scalar height budget')
    require(2-Fraction(4*19,40) == Fraction(1,10), 'Lucas precision budget')
    require(2-Fraction(19,12) == Fraction(5,12), 'beta precision budget')
    require(Fraction(12+19,5*40) == Fraction(31,200), 'beta contradiction constant')
    chain = [1,2,3,6,9,11,22,33,39,78]
    for i, x in enumerate(chain[1:],1):
        require(any(a+b == x for a in chain[:i] for b in chain[:i]), 'invalid power chain')
    for m in [1,12,40]:
        # Exponents in (A, delta, F) of q1*e^(2m-2) and
        # delta^(-2m-2)*R^(1-2m), respectively.
        lhs = (5*(2*m-1),5*(2*m-1)-3,-(2*m-1))
        rhs = (-5*(1-2*m),-6*(1-2*m)-2*m-2,1-2*m)
        require(lhs == rhs, 'detector weight mismatch')
    return {'anchorLog2LowerBound':str(anchor_lower), 'requiredLog2UpperBound':threshold_upper,
            'powerChain':chain, 'status':'exact rational budgets passed; not a proof of inherited theorems'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results',type=Path)
    args=parser.parse_args(); out=args.results.resolve()
    report={'budgets':budgets(),'variants':{}}
    for name in ['scalar_fused','h19_scalar32','h19_scalar24']:
        dest=out/name
        old=read(dest/'builder/raw-translated-ir.json'); new=read(dest/'ordinary-source.json')
        count=check_chain(old,new,27 if name=='scalar_fused' else 26)
        # Ensure a changed initial constant is rejected.
        bad=copy.deepcopy(new)
        bad['residuals'][len(old['residuals'])]['terms'][1]['coefficient']='-9'
        try: check_chain(old,bad,27 if name=='scalar_fused' else 26)
        except ValueError: pass
        else: raise ValueError('incorrect constant accepted')
        table=read(dest/'ordinary/ordinary-polynomial.json')
        legacy=read(dest/'ordinary/polynomial.json')
        require(table['fixedParameter'] is None, 'ordinary export still declares S')
        require(all(t['sPower']==0 for t in legacy['terms']), 'residual fixed-parameter coefficient')
        require(table['terms']==[{'monomial':t['monomial'],'coefficient':t['coefficient']} for t in legacy['terms']], 'ordinary export differs')
        for receipt in ['independent-check.json','ordinary-independent-check.json']:
            r=read(dest/receipt)
            require(r['status']=='passed_exact_algebra_checks' and r['quarticTableCompared'], 'missing independent replay')
            for item in r['artifactHashes'].values():
                require(hashlib.sha256(Path(item['file']).read_bytes()).hexdigest()==item['sha256'],'stale checker receipt')
        report['variants'][name]={'chainCoordinates':count,'chainAndExport':'passed','changedConstantRejected':True}
    (out/'VARIANT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
