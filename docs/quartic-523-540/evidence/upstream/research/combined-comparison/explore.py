"""Reproduce additive variants of the pinned Version 5 source.

Run from any directory with --out pointing to a new directory outside the repo.
Uses the upstream builder, exact compiler, and independently written checker.
No shipped upstream artifact is modified. Arithmetic justification is separate.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'quartics/quartic-1272'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def replace_once(s, old, new):
    if s.count(old) != 1:
        raise ValueError('Upstream builder changed: ' + old[:100])
    return s.replace(old, new)

def builder_variant(original, precision, scalar_order):
    s = original
    old = "let n0=normTree('scalar.n0',one,leaves[0]),n1=normTree('scalar.n1',leaves[1],leaves[2]),n3=normTree('scalar.n3',leaves[4],leaves[5]);"
    new = "let n0=assign('scalar.n0',add(one,mul(PU[0].f[0],leaves[0]))),n1=assign('scalar.n1',add(sq(leaves[1]),mul(PS.f[0],leaves[2]))),n3=normTree('scalar.n3',leaves[4],leaves[5]);"
    s = replace_once(s, old, new)
    if precision == 'h19':
        s = replace_once(s, 'j<=12;j++', 'j<=9;j++')
        s = replace_once(s, 'b=e===16?4:3', 'b=3')
        s = replace_once(s, "i===1?16:52)),LV=PV.map((p,i)=>log('logV'+i,p,i===1?16:52))", "i===1?12:40)),LV=PV.map((p,i)=>log('logV'+i,p,i===1?12:40))")
        s = replace_once(s, 'order:i===1?16:52', 'order:i===1?12:40')
        s = replace_once(s, 'order:16},{value:FF,order:52}', 'order:12},{value:FF,order:40}')
        s = replace_once(s, 'for(let m of [1,16,52])', 'for(let m of [1,12,40])')
        start = s.index(" let e2=rsq('detector'+r+'.e2'")
        end = s.index(" let wi=inv('detector'+r+'.w0Inverse'", start)
        s = s[:start] + """ let e2=rsq('detector'+r+'.e2',ep),e3=rm('detector'+r+'.e3',e2,ep),e6=rsq('detector'+r+'.e6',e3),e9=rm('detector'+r+'.e9',e6,e3),e11=rm('detector'+r+'.e11',e9,e2),e22=rsq('detector'+r+'.e22',e11),e33=rm('detector'+r+'.e33',e22,e11),e39=rm('detector'+r+'.e39',e33,e6),e78=rsq('detector'+r+'.e78',e39);
 let q12=rm('detector'+r+'.q12',q1,e22),q40=rm('detector'+r+'.q40',q1,e78);
 let w=fmul('detector'+r+'.W',fmul('detector'+r+'.Wfirst',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E12',coeffs[12],q12)),evalSym('detector'+r+'.E40',coeffs[40],q40));
""" + s[end:]
    if scalar_order == 24:
        s = replace_once(s, "ri32=rp('scalar.rInverse32',ri,32)", "ri32=rp('scalar.rInverse24',ri,24)")
    return s

def call(args, log):
    with log.open('w') as f:
        r = subprocess.run([str(x) for x in args], stdout=f, stderr=subprocess.STDOUT)
    if r.returncode:
        raise RuntimeError(f'Command failed; see {log}')

def term(c, m):
    return {'monomial': m, 'sPower': 0, 'coefficient': str(c)}

def chain_lift(compiled, first_power=10, last_power=27):
    """Replace S by a unique constant chain, keeping every residual quadratic."""
    data = copy.deepcopy(compiled)
    # The compact starting constant 3^(2^10) has 489 decimal digits.
    # Its square is smaller than the existing 5339-bit coefficient bound.
    first = 1 + max(c['id'] for c in data['coordinates'])
    chain = list(range(first, first + last_power + 1 - first_power))
    for row in data['residuals']:
        for t in row['terms']:
            power = t['sPower']
            if power:
                assert power == 1 and len(t['monomial']) <= 1
                t['monomial'] = sorted(t['monomial'] + [chain[-1]])
                t['sPower'] = 0
    for k, v in enumerate(chain):
        data['coordinates'].append({'id': v, 'name': f'constant.3pow2pow{first_power+k}',
                                    'kind': 'base', 'protected': True})
        terms = [term(1, [v]), term(-pow(3, 2**first_power), [])] if k == 0 else [term(1, [v]), term(-1, [chain[k-1], chain[k-1]])]
        data['residuals'].append({'id': f'constant-chain-{k}', 'name': f'constant-chain-{k}', 'terms': terms})
    # Retain the upstream IR's required S declaration for its unmodified reader.
    # No residual uses it; the ordinary export removes this legacy metadata.
    data['fixedParameterUsed'] = False
    data['constantChain'] = {'firstPower': first_power, 'lastPower': last_power, 'coordinates': chain,
                             'conclusion': f'last coordinate is uniquely 3^(2^{last_power})',
                             'scope': 'unchanged fixed constant' if last_power == 27 else 'smaller anchor justified in ARITHMETIC.md; not an identity with the old fixed-S source'}
    # Retain original gate definitions for the independent source-gate check.
    # The anchor is structural, so no gate expression contains the fixed S.
    assert all(not t['sPower'] for g in data.get('gates', []) for t in g.get('expression', []))
    for key in ['sourceGates', 'values', 'guards', 'anchor', 'census', 'counts']:
        data.pop(key, None)
    return data

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        raise ValueError('--out must be a new directory')
    out.mkdir(parents=True)
    pins = json.loads((Path(__file__).parent/'INPUTS.json').read_text())
    for name, sha in pins['sha256'].items():
        assert digest(ROOT/name) == sha, name
    spec = importlib.util.spec_from_file_location('upstream_compiler', PACKAGE/'compiler/compile_ir.py')
    compiler = importlib.util.module_from_spec(spec); spec.loader.exec_module(compiler)
    original = (PACKAGE/'builder/build_source.cjs').read_text()
    summary = {'baseCommit': pins['baseCommit'], 'inputHashes': pins['sha256'], 'variants': {}}
    for name, precision, order in [('scalar_fused', 'v5', 32), ('h19_scalar32', 'h19', 32), ('h19_scalar24', 'h19', 24)]:
        dest = out/name; build = dest/'builder'; build.mkdir(parents=True)
        sources = dest/'sources'; sources.mkdir()
        shutil.copyfile(PACKAGE/'sources/diophantine_optimization_20261106_v3.tex', sources/'diophantine_optimization_20261106_v3.tex')
        script = build/'build_source.cjs'; script.write_text(builder_variant(original, precision, order))
        call(['node', script], dest/'builder.log')
        raw = build/'raw-translated-ir.json'; compiled = dest/'compiled'
        data = json.loads(raw.read_text())
        data['source']['historicalUpstreamRefinements'] = data['source'].pop('refinements')
        data['source']['variant'] = {'name': name, 'scalarNormFusion': True,
                                    'comparisonOrders': [12,40,40,40] if precision == 'h19' else [16,52,52,52],
                                    'scalarOrder': order, 'status': 'additive proposal; see ARITHMETIC.md'}
        raw.write_text(json.dumps(data,indent=2)+'\n')
        report = compiler.run(raw, compiled)
        call(['node', PACKAGE/'checker/checker.cjs', '--input', raw, '--compiled', compiled/'compiled-ir.json',
              '--certificate', compiled/'reduction-certificate.json', '--coordinate-map', compiled/'coordinate-map.json',
              '--quartic', compiled/'polynomial.json', '--report', dest/'independent-check.json'], dest/'checker.log')
        item = {'finite': report['final'], 'builderSha256': digest(script), 'polynomialSha256': digest(compiled/'polynomial.json')}
        # Introduce the chain in the raw system so the independent checker can
        # still verify every original gate and replay the complete reduction.
        ordinary = dest/'ordinary-source.json'
        last_power = 26 if precision == 'h19' else 27
        ordinary.write_text(json.dumps(chain_lift(data, last_power=last_power), indent=2)+'\n')
        ordinary_out = dest/'ordinary'
        ordinary_report = compiler.run(ordinary, ordinary_out)
        call(['node', PACKAGE/'checker/checker.cjs', '--input', ordinary, '--compiled', ordinary_out/'compiled-ir.json',
              '--certificate', ordinary_out/'reduction-certificate.json', '--coordinate-map', ordinary_out/'coordinate-map.json',
              '--quartic', ordinary_out/'polynomial.json', '--report', dest/'ordinary-independent-check.json'], dest/'ordinary-checker.log')
        table = json.loads((ordinary_out/'polynomial.json').read_text())
        assert all(t['sPower'] == 0 for t in table['terms'])
        coefficients = [abs(int(t['coefficient'])) for t in table['terms']]
        item['ordinary'] = {**ordinary_report['final'], 'maximumCoefficientBits': max(coefficients).bit_length(),
                            'polynomialSha256': digest(ordinary_out/'polynomial.json'),
                            'constantChainVariables': last_power - 9, 'anchorConstant': f'3^(2^{last_power})'}
        # A clean export has ordinary integer coefficients, with no S convention.
        table['fixedParameter'] = None
        table['schema'] = 'ordinary-integer-quartic-v1'
        table['terms'] = [{'monomial': t['monomial'], 'coefficient': t['coefficient']} for t in table['terms']]
        export = ordinary_out/'ordinary-polynomial.json'; export.write_text(json.dumps(table,indent=2)+'\n')
        item['ordinary']['ordinaryExportSha256'] = digest(export)
        summary['variants'][name] = item
        (out/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(name, json.dumps(item), flush=True)

if __name__ == '__main__':
    main()
