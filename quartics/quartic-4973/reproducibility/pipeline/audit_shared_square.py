"""Independent exact restoration for the shared conjugate-fJ square delta.

The caller must run its pinned complete parent source checker on the restored
view. This helper never imports the emitter. Its acceptance is conditional on
that parent check, which also proves the original common pair is conj(fJ).
"""
from copy import deepcopy
import json

MODES={
    'q_compare4':dict(batch='q_conic13',free=58,slot=21,field=5,count=13),
    'q_compare_beta':dict(batch='q_conic6',free=28,slot=9,field=2,count=8),
    'q_compare_lucas':dict(batch='q_conic10',free=47,slot=16,field=4,count=16),
}
TYPE='pre-squared shared field'


class SharedSquareResourceError(RuntimeError):
    pass


def preflight(value,*,node_limit=300000):
    """Bound JSON traversal before deepcopy or serialization, including metadata."""
    stack=[(value,0)];nodes=0;characters=0
    while stack:
        obj,depth=stack.pop();nodes+=1
        if nodes>node_limit or depth>48:
            raise SharedSquareResourceError('JSON node/depth resource limit')
        if obj is None or type(obj) is bool:continue
        if type(obj) is int:
            if obj.bit_length()>4096:raise SharedSquareResourceError('JSON integer resource limit')
        elif type(obj) is str:
            characters+=len(obj)
            if len(obj)>8192 or characters>2_000_000:
                raise SharedSquareResourceError('JSON string resource limit')
        elif type(obj) is list:
            if len(obj)>16384:raise SharedSquareResourceError('JSON list resource limit')
            stack.extend((v,depth+1) for v in obj)
        elif type(obj) is dict:
            if len(obj)>16384:raise SharedSquareResourceError('JSON object resource limit')
            for key,val in obj.items():
                assert type(key) is str, 'JSON object keys must be strings'
                stack.append((key,depth+1));stack.append((val,depth+1))
        else:
            raise AssertionError('Only integer-valued JSON data is permitted')


def same(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==\
           json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)


def integer(x):
    assert type(x) is int, 'Integer coordinate required'
    return x


def row(*terms):
    p={}
    for a,m in terms:
        key=tuple(sorted(m));p[key]=p.get(key,0)+a
    return [[v,list(k)] for k,v in sorted(p.items()) if v]


def bound(module):
    preflight(module)
    for key in ('residuals','construction_log','calls'):
        if len(module[key])>4096:raise SharedSquareResourceError('Module resource limit')
    if integer(module['free'])+integer(module['locals'])>8192:
        raise SharedSquareResourceError('Variable resource limit')


def marker(spec,batch=False):
    f=spec['field'];slot=1+2*f if batch else spec['slot']
    return dict(field='conj_fJ',input_slots=[slot,slot+1],field_index=f,
                order=1,input_type=TYPE)


def restore_comparison(candidate,spec):
    bound(candidate);d=deepcopy(candidate);slot=spec['slot'];f=spec['field']
    assert integer(d['free'])==spec['free']
    assert same(d.pop('shared_square_input'),marker(spec)), 'Comparison square marker'
    parts=d['input_layout'].split(';')
    assert parts.count('square_conj_fJ')==1 and 'conj_fJ' not in parts, 'Comparison square layout'
    parts[parts.index('square_conj_fJ')]='conj_fJ';d['input_layout']=';'.join(parts)
    assert same(d['conic_field_inputs'][f],[slot,slot+1]), 'Comparison field slots'
    assert integer(d['field_inequality_orders'][f])==1
    assert not any(v in mon for rw in d['residuals'] for _,mon in rw for v in (slot,slot+1)), 'Comparison common-slot outside use'
    assert len(d['calls'])==1 and d['calls'][0]['module']==spec['batch']
    args=d['calls'][0]['args'];assert same(args[1+2*f:3+2*f],[slot,slot+1])
    assert args.count(slot)==args.count(slot+1)==1, 'Comparison common-slot repeated call use'
    return d


def restore_batch(candidate,spec):
    bound(candidate);d=deepcopy(candidate);f=spec['field']
    meta=d.pop('shared_square_input');assert set(meta)==set(marker(spec,True))|{'removed_evaluation','removed_equation'}
    Y=integer(meta['removed_evaluation']);ri=integer(meta['removed_equation'])
    expected=marker(spec,True);expected.update(removed_evaluation=Y,removed_equation=ri)
    assert same(meta,expected), 'Batch square marker'
    assert d['free']<=Y<=d['free']+d['locals'] and 0<=ri<len(d['residuals'])
    assert integer(d['orders'][f])==integer(d['field_inequality_orders'][f])==1
    matches=[x for x in d['field_bindings'] if x['field']==f]
    tree_matches=[x for x in d['norm_tree'] if x.get('type')!='literal' and x['field']==f]
    assert len(matches)==len(tree_matches)==1 and same(matches[0],tree_matches[0])
    rec=matches[0]
    assert set(rec)=={'type','field','order','inputs','evaluation','norm','power','input_type'}
    assert rec['type']=='conic_field' and rec['input_type']==TYPE and rec['evaluation'] is None
    assert same(rec['inputs'],[1+2*f,2+2*f]) and integer(rec['order'])==1
    W=integer(rec['norm']);P=integer(rec['power']);th=integer(d['conic_private']['theta'])
    A,B=rec['inputs']
    assert W==Y, 'Restored Y must precede its norm coordinate'
    assert any(same(x,{'exponent':2,'variable':P}) for x in d['contact_powers']), 'Existing r-squared power required'
    assert same(d['residuals'][ri],row((1,[P,W]),(-1,[A]),(-1,[th,B]))), 'Pre-squared norm row'
    assert ['equation',ri,'conic packed field norm'] in d['construction_log']
    assert sum(x==['variable',W,'conic packed field norm'] for x in d['construction_log'])==1

    def up(v):
        v=integer(v);return v+1 if v>=Y else v
    def upr(i):
        i=integer(i);return i+1 if i>=ri else i
    d['locals']+=1
    d['residuals']=[[[a,[up(v) for v in mon]] for a,mon in rw] for rw in d['residuals']]
    oldW,oldP,oldth=up(W),up(P),up(th)
    d['residuals'][ri]=row((1,[oldP,oldW]),(-2,[A,Y]),(1,[A,A]),(-2,[B,B]))
    d['residuals'].insert(ri,row((1,[Y]),(-1,[A]),(-1,[oldth,B])))
    log=[]
    for item in d['construction_log']:
        assert len(item)==3 and item[0] in ('variable','equation'), 'Unexpected batch log event'
        k,i,label=item
        if k=='variable' and i==W:
            log += [['variable',Y,'conic evaluation'],['equation',ri,'conic evaluation']]
        log.append([k,up(i) if k=='variable' else upr(i),label])
    d['construction_log']=log
    for call in d['calls']:call['args']=[up(v) for v in call['args']]
    d['conic_private']={key:up(v) for key,v in d['conic_private'].items()}
    d['conic_equations']=[upr(i) for i in d['conic_equations']]
    d['field_input_order']=[[up(v) for v in pair] for pair in d['field_input_order']]
    d['contact_powers']=[dict(x,variable=up(x['variable'])) for x in d['contact_powers']]
    for key in ('norm_root','norm_root_square','parity_argument'):
        if key in d:d[key]=up(d[key])
    if 'pole_inputs' in d:d['pole_inputs']=[up(v) for v in d['pole_inputs']]
    def restore_record(x):
        x=deepcopy(x)
        if x['type']=='literal':return x
        designated=integer(x['field'])==f
        if designated:
            assert x.pop('input_type')==TYPE and x['evaluation'] is None
            x['evaluation']=Y
        else:
            assert 'input_type' not in x and x['evaluation'] is not None
            x['evaluation']=up(x['evaluation'])
        x['inputs']=[up(v) for v in x['inputs']]
        x['norm']=up(x['norm']);x['power']=up(x['power'])
        return x
    d['field_bindings']=[restore_record(x) for x in d['field_bindings']]
    d['norm_tree']=[restore_record(x) for x in d['norm_tree']]
    return d


def restore_root(candidate):
    bound(candidate);d=deepcopy(candidate);meta=d.pop('shared_square_root')
    assert set(meta)=={'field','original_pair','square_pair','equations','occurrences'}
    C=d['free']+d['locals']-2;D=C+1;nr=len(d['residuals'])
    old=meta['original_pair'];assert len(old)==2
    A,B=map(integer,old);assert 0<=A<C and 0<=B<C and A!=B
    expected=dict(field='conj_fJ',original_pair=[A,B],square_pair=[C,D],equations=[nr-2,nr-1],occurrences=37)
    assert same(meta,expected), 'Root square marker'
    assert same(d['residuals'][-2:],[row((1,[C]),(-1,[A,A]),(-2,[B,B])),row((1,[D]),(-2,[A,B]))]), 'Root square definitions'
    assert same(d['construction_log'][-4:],[
        ['variable',C,'shared conic field square.0'],['variable',D,'shared conic field square.1'],
        ['equation',nr-2,'shared conic field square.0'],['equation',nr-1,'shared conic field square.1']]), 'Root square log'
    assert not any(v in mon for rw in d['residuals'][:-2] for _,mon in rw for v in (C,D)), 'New square coordinate in old root row'
    counts={name:0 for name in MODES}
    for call in d['calls']:
        if call['module'] in MODES:
            name=call['module'];spec=MODES[name];slot=spec['slot'];args=call['args']
            assert len(args)==spec['free'] and same(args[slot:slot+2],[C,D]), 'Root shared-square call pair'
            assert args.count(C)==args.count(D)==1, 'Square coordinate has another root-call use'
            args[slot:slot+2]=[A,B];counts[name]+=1
        else:
            assert C not in call['args'] and D not in call['args'], 'Square coordinate has outside call'
    assert counts=={name:spec['count'] for name,spec in MODES.items()}, 'Root comparison counts'
    d['locals']-=2;d['residuals']=d['residuals'][:-2];d['construction_log']=d['construction_log'][:-4]
    return d


def restore_modules(modules):
    preflight(modules)
    if len(modules)>32:raise SharedSquareResourceError('Module count limit')
    for name in ['Z_definition']+list(MODES)+[s['batch'] for s in MODES.values()]:
        assert name in modules and modules[name]['name']==name
    # Copy only after checking sizes of the affected structures.
    for obj in modules.values():bound(obj)
    restored=deepcopy(modules)
    restored['Z_definition']=restore_root(modules['Z_definition'])
    for name,spec in MODES.items():
        restored[name]=restore_comparison(modules[name],spec)
        restored[spec['batch']]=restore_batch(modules[spec['batch']],spec)
    return restored


def check_modules(modules,parent_check):
    """parent_check(restored_modules) must raise on every parent-audit failure.

    It may include a separately pinned root-carrier source checker. In particular
    it must prove the restored root pair is the original conjugate fJ. A callback
    that merely accepts the restored shape is insufficient. A boolean-returning
    predicate is forbidden; successful checking may return a report or None.
    """
    restored=restore_modules(modules)
    inherited=parent_check(restored)
    if type(inherited) is bool:
        raise TypeError('parent_check must raise on failure, not return a boolean')
    return dict(status='PASS: shared-square delta and delegated parent',
                inherited=inherited,deleted_evaluations=37,added_shared_coordinates=2,
                exact_net_source_coordinates=-35,new_lift_gates=0,
                measured_endpoint_delta=False)
