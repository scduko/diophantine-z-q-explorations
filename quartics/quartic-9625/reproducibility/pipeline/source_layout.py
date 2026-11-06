"""Small deterministic locator pass over audited module and instantiation data.

These locators are producer hints. Every emitted algebraic event is still
checked against the current rows and complete incidence by the independent
certificate checker. Nothing here permits a rewrite by source label alone.
"""
from collections import Counter
from functools import reduce
import hashlib
import json
from math import gcd

MODULES = ('Z_definition', 'q_anchor', 'q_height_batch', 'q_primeparity',
           'q_compare4', 'q_batch41', 'q_compare_beta', 'q_batch17')
COMPARISONS = {'q_compare4':'q_batch41', 'q_compare_beta':'q_batch17'}
BATCHES = tuple(COMPARISONS.values())


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')+b'\n'


def global_var(inst, module, variable):
    if variable < 0:
        return -variable
    return inst['arguments'][variable] if variable < module['free'] else inst['first_local']+variable-module['free']


def normalize(row):
    row = {m:c for m,c in row.items() if c}
    if not row:
        return ()
    divisor = reduce(gcd, map(abs, row.values()))
    ordered = sorted(row)
    if row[ordered[0]] < 0:
        divisor = -divisor
    return tuple((m, row[m]//divisor) for m in ordered)


def norm_row(inverse, point, target):
    row = {():-1}
    for scalar, x, y in zip((1, -2), point, target):
        for coefficient, monomial in ((scalar,(inverse,x,x)),
                                      (-2*scalar,(inverse,x,y)),
                                      (scalar,(inverse,y,y))):
            key = tuple(sorted(monomial))
            row[key] = row.get(key,0)+coefficient
    return normalize(row)


def derive_layout(modules, visits):
    assert set(modules) == set(MODULES)
    assert len({v['path'] for v in visits}) == len(visits)
    counts = Counter(v['module'] for v in visits)
    assert set(counts) == set(MODULES) and counts['Z_definition'] == 1
    guards = []; charts = []; parity = []; batches = []; roots = []
    local_ranges = []; row_ranges = []
    for inst in visits:
        module = modules[inst['module']]
        assert inst['local_count'] == module['locals']
        assert inst['residual_count'] == len(module['residuals'])
        assert len(inst['arguments']) == module['free']
        local_ranges.append((inst['first_local'],inst['first_local']+inst['local_count']))
        row_ranges.append((inst['first_residual'],inst['first_residual']+inst['residual_count']))
        variables = [(i,label) for kind,i,label in module['construction_log'] if kind=='variable']
        equations = [(i,label) for kind,i,label in module['construction_log'] if kind=='equation']
        labels = {label:i for i,label in variables}
        gv = lambda v: global_var(inst,module,v)
        if inst['module'] in COMPARISONS:
            call, = module['calls']
            assert call['module'] == COMPARISONS[inst['module']]
            assert len(call['args']) == modules[call['module']]['free']
            inverses = [i for i,label in variables if label=='distinct abscissae guard']
            rows = [i for i,label in equations if label=='distinct abscissae guard']
            assert len(inverses)==len(rows)>0
            points = [(labels[label],labels[label[:-1]+'1']) for label in labels if label.endswith('.x.0')]
            for inverse, row in zip(inverses,rows):
                exact = normalize({tuple(m):c for c,m in module['residuals'][row]})
                # Recover target coordinates from the exact cubic norm row,
                # without assuming argument positions or a number of points.
                matches = [(point,(k,k+1)) for point in points for k in range(module['free']-1)
                           if norm_row(inverse,point,(k,k+1))==exact]
                assert len(matches)==1, ('ambiguous norm locator',inst['path'],row,matches)
                point,target = matches[0]
                guards.append(dict(path=inst['path'],row=inst['first_residual']+row,
                                   inverse=gv(inverse),point=list(map(gv,point)),target=list(map(gv,target))))
        if inst['module']=='Z_definition' or inst['module'] in COMPARISONS:
            for label in labels:
                if label.endswith('.w.0'):
                    prefix=label[:-4]
                    assert all(prefix+'.'+part+'.'+str(k) in labels
                               for part in ('u','v','w','z','f','h','x','y') for k in range(2))
                    charts.append(dict(path=inst['path'],prefix=prefix))
        if inst['module']=='q_primeparity':
            # Seven and four are the audited parity rule's local signature,
            # never the number of instantiations of that rule.
            assert module['free']==1 and module['locals']==7 and len(module['residuals'])==4
            parity.append(dict(path=inst['path'],input=inst['arguments'][0],
                               witnesses=list(range(inst['first_local'],inst['first_local']+inst['local_count'])),
                               rows=list(range(inst['first_residual'],inst['first_residual']+inst['residual_count']))))
        if inst['module'] in BATCHES:
            pairs = [p for p in module['norm_tree'] if p['type']=='pair']
            norm_rows = [i for i,label in equations if label=='fused normalized pair']
            assert len(pairs)==len(norm_rows)>0
            assert 2*len(pairs)+2 == module['free'], 'Nonpaired batch inputs'
            batches.append(dict(path=inst['path'],module=inst['module'],factor=inst['arguments'][0],error=inst['arguments'][1],
                                pair_rows=[inst['first_residual']+i for i in norm_rows]))
        if inst['module']=='Z_definition':
            rootrow, = [i for i,label in equations if label=='root error']
            roots.append(inst['first_residual']+rootrow)
    for intervals in (local_ranges,row_ranges):
        ordered=sorted(intervals)
        assert all(a[1]<=b[0] for a,b in zip(ordered,ordered[1:])), 'overlapping instantiations'
    assert len(roots)==1
    assert all(counts[comparison]==counts[batch] for comparison,batch in COMPARISONS.items())
    return dict(module_counts=dict(sorted(counts.items())),norm_guards=guards,charts=charts,
                parity=parity,batches=batches,root_row=roots[0],
                counts=dict(comparisons=sum(counts[n] for n in COMPARISONS),norm_guards=len(guards),
                            uncompressed_charts=len(charts),parity=len(parity),batches=len(batches),
                            batch_pairs=sum(len(b['pair_rows']) for b in batches)))


def load_layout(adapter):
    entry=json.loads((adapter/'source-entry.json').read_bytes())
    mapping=(adapter/'construction-map.json').read_bytes()
    assert hashlib.sha256(mapping).hexdigest()==entry['construction_map_sha256']
    modules={}
    for name in MODULES:
        relative='modules/'+name+'.json'
        raw=(adapter/'source'/relative).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==entry['inspected_files_sha256'][relative]
        modules[name]=json.loads(raw)
    layout=derive_layout(modules,json.loads(mapping)['instantiations'])
    raw=(adapter/'source-layout.json').read_bytes()
    assert raw==encoded(layout) and hashlib.sha256(raw).hexdigest()==entry['source_layout_sha256']
    assert layout['counts']==entry['layout_counts']
    return layout
