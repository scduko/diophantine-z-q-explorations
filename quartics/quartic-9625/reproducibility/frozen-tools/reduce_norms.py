"""Untrusted source-map locators for existing norm and redundant-inverse rules."""
import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path

import polynomial_ops as op
from export_artifact import enc, export
from source_layout import BATCHES, load_layout


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--adapter', type=Path, required=True)
    p.add_argument('--parent', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    entry = json.loads((a.adapter/'source-entry.json').read_bytes())
    layout = load_layout(a.adapter)
    source = a.parent/'source-residuals.jsonl.gz'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == entry['source_sha256']
    records = [json.loads(line) for line in gzip.decompress((a.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    initial = records[0]; assert initial['source_id'] == entry['source_id']
    allocated = records[-1]['allocated_variables']
    records = [x for x in records if x['kind'] not in ('weights','final')]
    rows = [{tuple(m): c for c,m in raw} for raw in json.loads(gzip.decompress((a.parent/'candidate-rows.json.gz').read_bytes()))]
    gates = {g['variable']:(initial['source_rows']+i,tuple(g['product'])) for i,g in enumerate(initial['gates'])}
    modules = {name:json.loads((a.adapter/'source/modules'/f'{name}.json').read_bytes()) for name in ('Z_definition',)+BATCHES}
    visits = json.loads((a.adapter/'construction-map.json').read_bytes())['instantiations']
    incidence = defaultdict(set)
    for i,row in enumerate(rows):
        for v in op.vars_in(row):
            incidence[v].add(i)
    def gv(inst, module, v):
        if v < 0:
            return -v
        return inst['arguments'][v] if v<module['free'] else inst['first_local']+v-module['free']
    def var(v):
        return {(v,):1}
    def add(*parts):
        out = {}
        for c,row in parts:
            op.poly_add(out,row,c)
        return out
    def apply(kind,data,patches):
        patches = {i:dict(op.primitive(row)) if row else {} for i,row in patches.items()}
        records.append(dict(kind=kind,data=data,patches=[[i,enc(row)] for i,row in sorted(patches.items())]))
        for i,row in patches.items():
            for v in op.vars_in(rows[i]):
                incidence[v].remove(i)
            rows[i] = row
            for v in op.vars_in(row):
                incidence[v].add(i)

    applied = 0; skipped = []
    for guard in layout['norm_guards']:
            u = guard['inverse']; i = guard['row']
            components = [add((1,var(x)),(-1,var(y))) for x,y in zip(guard['point'],guard['target'])]
            closure = set()
            def expand(v):
                if v not in gates:
                    return (v,)
                closure.add(v); row_id,pair = gates[v]
                assert rows[row_id] == {pair:-1,(v,):1}
                return tuple(sorted(expand(pair[0])+expand(pair[1])))
            expanded = defaultdict(int)
            for mon,c in rows[i].items():
                expanded[tuple(sorted(x for v in mon for x in expand(v)))] += c
            norm = add((1,op.square(components[0])),(-2,op.square(components[1])))
            expected = add((1,op.product(var(u),norm)),(-1,{():1}))
            assert op.primitive({mon:c for mon,c in expanded.items() if c})==op.primitive(expected)
            removed = {u}|{v for v in closure if u in expand(v)}
            changed = {i}|{gates[v][0] for v in removed if v in gates}
            outside = {v:sorted(incidence[v]-changed) for v in removed if incidence[v]-changed}
            if outside or len(removed)<2:
                skipped.append(dict(row=i,removed=len(removed),outside=outside)); continue
            s,t = allocated,allocated+1; allocated += 2
            real = add((1,op.product(components[0],var(s))),(2,op.product(components[1],var(t))),(-1,{():1}))
            imag = add((1,op.product(components[0],var(t))),(1,op.product(components[1],var(s))))
            second = min(changed-{i}); patches = {k:{} for k in changed}
            patches[i]=real; patches[second]=imag
            data = dict(row=i,inverse=u,definitions=[[gates[v][0],v] for v in sorted(closure)],
                        removed=sorted(removed),components=[enc(x) for x in components],new_variables=[s,t])
            apply('norm_inverse',data,patches); applied += 1

    root, = [v for v in visits if v['module']=='Z_definition']
    rm = modules['Z_definition']
    local_root, = [i for kind,i,label in rm['construction_log'] if kind=='equation' and label=='root error']
    root_row = root['first_residual']+local_root
    assert root_row == layout['root_row']
    theta, = [mon[0] for mon in rows[root_row] if len(mon)==2 and mon[0]==mon[1]]
    error, = [mon[0] for mon in rows[root_row] if len(mon)==1]
    assert op.primitive(rows[root_row]) == op.primitive({(error,):1,(theta,theta):-1,():2})
    def affine(poly):
        return dict(denominator=1,terms=enc(poly))
    redundant = 0
    for inst in visits:
        if inst['module'] not in BATCHES:
            continue
        bm = modules[inst['module']]
        inverse_local, = [i for kind,i,label in bm['construction_log'] if kind=='variable' and label=='nonzero contact factor']
        inverse_row, = [i for kind,i,label in bm['construction_log'] if kind=='equation' and label=='nonzero contact factor']
        first_local, = [i for kind,i,label in bm['construction_log'] if kind=='variable' and label=='constant leaf norm']
        first_row, = [i for kind,i,label in bm['construction_log'] if kind=='equation' and label=='fused constant leaf norm']
        factor=inst['arguments'][0]; inverse=gv(inst,bm,inverse_local); first=gv(inst,bm,first_local)
        i=inst['first_residual']+inverse_row; relation=inst['first_residual']+first_row
        # The retained relation is already R*(F-1)=E^2. The existing inverse
        # checker accepts the affine cofactor F-1 directly.
        assert op.primitive(rows[i])==op.primitive({tuple(sorted((factor,inverse))):1,():-1})
        assert op.primitive(rows[relation])==op.primitive({tuple(sorted((factor,first))):1,(factor,):-1,(error,error):-1})
        assert incidence[inverse]=={i}
        data=dict(row=i,inverse=inverse,factor=affine(var(factor)),
                  nonzero=dict(kind='root_error',root_row=root_row,relation_row=relation,
                               root=affine(var(theta)),error=affine(var(error)),cofactor=affine({(first,):1,():-1})))
        apply('redundant_inverse',data,{i:{}}); redundant += 1
    assert applied+len(skipped)==layout['counts']['norm_guards']
    assert redundant==layout['counts']['batches']
    report=export(a.output,source,rows,records,allocated,
                  dict(norm_inverse_replacements=applied,skipped_norms=skipped,redundant_inverse_removals=redundant))
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
