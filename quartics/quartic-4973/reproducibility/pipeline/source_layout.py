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
           'q_compare4', 'q_conic13', 'q_compare_beta', 'q_conic6',
           'q_compare_lucas', 'q_conic10', 'q_linearnormalpole')
COMPARISONS = {'q_compare4':'q_conic13', 'q_compare_beta':'q_conic6',
               'q_compare_lucas':'q_conic10'}
BATCHES = tuple(COMPARISONS.values())
BOUNDARIES={'q_compare4':(58,28),'q_compare_beta':(28,16),'q_compare_lucas':(47,23)}


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
    guards = []; charts = []; parity = []; batches = []; roots = []; poles = []
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
        is_jacobi = (inst['module'] in COMPARISONS and module.get('difference_model') ==
                     'joint f,p,A,K curve and complete z graph; no difference formal tests')
        if inst['module']=='Z_definition':
            assert module.get('chart')=='general_E_mixed' and module.get('baseline_chart')==10, 'Wrong general root chart'
            assert type(module.get('comparison_target_multiplier')) is int and module.get('comparison_target_multiplier')==2, 'Wrong root target multiplier'
            assert module.get('root_carrier')=='nontorsion E(K)', 'Wrong root carrier'
            assert module.get('root_index_semantics')=='2Q=n_Q Pstar, n_Q integer', 'Wrong root index semantics'
            assert type(module.get('beta_comparison_scale')) is int and module.get('beta_comparison_scale')==2, 'Wrong root beta scale'
            assert module.get('shared_square_root',{}).get('occurrences')==37, 'Missing shared root square'
            assert module.get('root_doubling_model')=='direct tangent with retained square coordinates', 'Wrong direct tangent model'
            assert [item.get('role') for item in module.get('direct_tangent_doublings',[])]==['A','S','T','Z'], 'Wrong direct tangent sites'
            tangent=module.get('direct_tangent_rewrite',{})
            assert encoded({key:tangent.get(key) for key in ('doublings','raw_variable_delta','raw_row_delta')})==encoded(dict(doublings=4,raw_variable_delta=-8,raw_row_delta=-8)), 'Wrong direct tangent rewrite'
        if inst['module'] in COMPARISONS:
            call, = module['calls']
            assert call['module'] == COMPARISONS[inst['module']]
            assert len(call['args']) == modules[call['module']]['free']
            assert module.get('comparison_norm')=='private conic field norm v1', 'Wrong conic comparison model'
            assert module.get('local_lucas_residual') is (inst['module']!='q_compare_beta'), 'Wrong local Lucas flag'
            assert module.get('global_lucas_proxy_inputs') is False, 'Old global Lucas proxy inputs'
            if inst['module']=='q_compare_beta':
                assert 'normalized_lucas_residual' not in module and 'global_numerator_p_nonzero' not in module, 'Changed beta normalization metadata'
            else:
                assert module.get('normalized_lucas_residual') is True, 'Missing normalized Lucas flag'
                assert module.get('global_numerator_p_nonzero') is False, 'Wrong global numerator scope'
            index,slot={'q_compare4':(5,21),'q_compare_beta':(2,9),'q_compare_lucas':(4,16)}[inst['module']]
            marker=dict(field='conj_fJ',input_slots=[slot,slot+1],field_index=index,order=1,input_type='pre-squared shared field')
            assert encoded(module.get('shared_square_input'))==encoded(marker), 'Wrong comparison square channel'
            assert module.get('root_index_semantics')=='2Q=n_Q Pstar, n_Q integer', 'Wrong comparison root index'
            assert type(module.get('comparison_target_multiplier')) is int and module.get('comparison_target_multiplier')==2, 'Wrong comparison target multiplier'
            assert module.get('comparison_fixed_target')=='2R=Pstar', 'Wrong fixed target'
            free,legacy=BOUNDARIES[inst['module']]
            assert module['free']==free, 'Wrong joint comparison arity'
            assert module.get('conic_legacy_input_count')==legacy and module.get('extra_target_start')==legacy, 'Wrong joint legacy count'
            ignored=[legacy-3,legacy-2]
            assert module.get('ignored_shared_root_inputs')==ignored, 'Wrong ignored root slots'
            assert not set(ignored)&set(call['args']), 'Legacy root input reaches conic batch'
            assert call['args'][0]==legacy-1, 'Wrong joint raw contact slot'
            inverses = [i for i,label in variables if label=='distinct abscissae guard']
            rows = [i for i,label in equations if label=='distinct abscissae guard']
            if is_jacobi:
                assert (module.get('primary_square_transfer') is False and module.get('x_squareclass_membership') is False
                        and module.get('difference_formal_tests') is False and module.get('rational_difference_four_fields') is False and module.get('joint_primary_difference_chart') is True
                        and module.get('private_index_group')=='(1/2)Z via doubling'), 'Incomplete joint chart flags'
                assert not inverses and not rows, 'Unexpected guard in joint chart source'
            else:
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
        if inst['module'] in COMPARISONS:
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
        if inst['module']=='q_linearnormalpole':
            assert module['free']==3 and module['locals']==10 and len(module['residuals'])==8, 'Wrong conic pole signature'
            poles.append(dict(path=inst['path'],inputs=inst['arguments']))
        if inst['module'] in BATCHES:
            assert module.get('comparison_norm')=='private conic field norm v1', 'Wrong conic batch model'
            assert module['norm_tree'][0]=={'type':'literal','value':1}, 'Missing literal-one leaf'
            fields=module['norm_tree'][1:]
            assert fields and fields[0]['type']=='conic_first_numerator' and all(p['type']=='conic_field' for p in fields[1:]), 'Wrong conic field nodes'
            first=fields[0];fusion=module.get('first_norm_fusion',{})
            expected_keys={'field','role','order','numerator','first_node','numerator_row','first_node_row','original_power','virtual_denominator','virtual_denominator_exponent'}
            assert set(fusion)==expected_keys and all(type(fusion[k]) is int for k in expected_keys-{'role'}), 'Wrong first-norm metadata'
            assert (fusion['field'],fusion['role'],fusion['order'],fusion['virtual_denominator'],fusion['virtual_denominator_exponent'])==(0,'H.f',1,0,1), 'Wrong first-norm meaning'
            expected_first={'type':'conic_first_numerator','field':0,'order':1,'inputs':[1,2],
                'evaluation':first.get('evaluation'),'norm':None,'power':0,'numerator':fusion['numerator'],'virtual_denominator_exponent':1}
            assert encoded(first)==encoded(expected_first), 'Wrong first numerator record'
            assert type(first['evaluation']) is int and module['free']<=first['evaluation']<module['free']+module['locals'], 'Wrong first evaluation'
            assert len({fusion[k] for k in ('numerator','first_node','original_power')})==3 and all(module['free']<=fusion[k]<module['free']+module['locals'] for k in ('numerator','first_node','original_power')), 'Wrong first-norm coordinates'
            assert fusion['numerator_row']!=fusion['first_node_row'] and all(0<=fusion[k]<len(module['residuals']) for k in ('numerator_row','first_node_row')), 'Wrong first-norm rows'
            assert (fusion['numerator_row'],'first conic field numerator') in equations and (fusion['first_node_row'],'fused first norm node') in equations, 'Wrong first-norm labels'
            index={'q_conic13':5,'q_conic6':2,'q_conic10':4}[inst['module']]
            marker=module.get('shared_square_input',{})
            assert type(marker.get('field_index')) is int and marker.get('field_index')==index and type(marker.get('order')) is int and marker.get('order')==1 and marker.get('input_type')=='pre-squared shared field', 'Wrong batch square channel'
            special=[p for p in fields if p.get('evaluation') is None]
            assert len(special)==1 and special[0]['field']==index and special[0].get('input_type')=='pre-squared shared field' and special[0]['order']==1, 'Wrong pre-squared field record'
            assert all(type(p['evaluation']) is int and 'input_type' not in p for p in fields if p['field']!=index), 'Wrong ordinary field record'
            norm_rows=[i for i,label in equations if label in ('conic packed field norm','first conic field numerator')]
            assert len(fields)==len(norm_rows), 'Wrong packed-row count'
            assert 2*len(fields)+1==module['free'], 'Wrong raw-field batch arity'
            assert module.get('conic_equations')==[0,1], 'Wrong conic equation positions'
            private=module['conic_private']
            assert set(private)=={'theta','s','square'} and len(set(private.values()))==3, 'Conic private coordinate alias'
            assert all(type(v) is int and module['free']<=v<module['free']+module['locals'] for v in private.values())
            assert not any(label in ('nonzero contact factor','constant leaf norm','fused constant leaf norm')
                           for i,label in variables+equations), 'Old inverse or error leaf in conic batch'
            assert module['calls']==[{'module':'q_linearnormalpole','args':[0,private['theta'],module['norm_root']]}], 'Wrong conic pole boundary'
            assert module.get('pole_inputs')==[0,private['theta'],module['norm_root']], 'Wrong conic pole metadata'
            def field_record(p):
                common=dict(inputs=[gv(v) for v in p['inputs']],evaluation=None if p['evaluation'] is None else gv(p['evaluation']),
                            input_type=p.get('input_type','ordinary field'),norm=None if p['norm'] is None else gv(p['norm']),order=p['order'])
                if p['type']=='conic_first_numerator':
                    common.update(input_type='first field numerator',numerator=gv(p['numerator']),power=gv(p['power']),
                                  virtual_denominator_exponent=1,first_node=gv(fusion['first_node']))
                return common
            batches.append(dict(path=inst['path'],module=inst['module'],factor=inst['arguments'][0],
                                conic_private={k:gv(v) for k,v in private.items()},pole_inputs=[gv(i) for i in module['calls'][0]['args']],
                                field_rows=[inst['first_residual']+i for i in norm_rows],
                                fields=[field_record(p) for p in fields]))
        if inst['module']=='Z_definition':
            rootrow, = [i for i,label in equations if label=='root error']
            roots.append(inst['first_residual']+rootrow)
    for intervals in (local_ranges,row_ranges):
        ordered=sorted(intervals)
        assert all(a[1]<=b[0] for a,b in zip(ordered,ordered[1:])), 'overlapping instantiations'
    assert len(roots)==1 and not charts, 'Old chart locator in general root source'
    assert all(counts[comparison]==counts[batch] for comparison,batch in COMPARISONS.items())
    assert counts['q_primeparity']==1 and counts['q_linearnormalpole']==37, 'Wrong pole instance counts'
    assert Counter(tuple(p['inputs']) for p in poles)==Counter(tuple(b['pole_inputs']) for b in batches), 'Wrong instantiated pole inputs'
    return dict(module_counts=dict(sorted(counts.items())),norm_guards=guards,charts=charts,
                parity=parity,batches=batches,conic_poles=poles,root_row=roots[0],
                counts=dict(comparisons=sum(counts[n] for n in COMPARISONS),norm_guards=len(guards),
                            uncompressed_charts=len(charts),parity=len(parity),batches=len(batches),
                            batch_pairs=0,conic_fields=sum(len(b['field_rows']) for b in batches),
                            private_conics=len(batches),conic_poles=len(poles),
                            conic_evaluations=sum(p['evaluation'] is not None for b in batches for p in b['fields']),
                            conic_first_numerators=sum(p['norm'] is None for b in batches for p in b['fields']),
                            conic_norm_fields=sum(p['norm'] is not None for b in batches for p in b['fields'])))


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
