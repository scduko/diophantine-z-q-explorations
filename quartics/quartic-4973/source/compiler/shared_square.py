"""Pure shared-field square source pass; requires full independent source audit."""
from collections import Counter
from copy import deepcopy
import json

MODES={
    'q_compare4':dict(count=13,free=58,slots=[21,22],batch='q_conic13',field=5),
    'q_compare_beta':dict(count=8,free=28,slots=[9,10],batch='q_conic6',field=2),
    'q_compare_lucas':dict(count=16,free=47,slots=[16,17],batch='q_conic10',field=4),
}
TYPE='pre-squared shared field'
BATCH_KEYS={'name','free','locals','residuals','calls','construction_log','orders',
    'field_inequality_orders','norm_tree','norm_level_sizes','parity_module',
    'squareclass_correction','input_layout','comparison_norm','conic_private',
    'conic_equations','field_input_order','sorted_field_indices','field_bindings',
    'contact_powers','norm_root','semantics','pole_model','pole_inputs'}
FIELD_KEYS={'type','field','order','inputs','evaluation','norm','power'}

def require(ok,message):
    if not ok:raise ValueError(message)

def equal(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False)

def row(*terms):
    values={}
    for coefficient,monomial in terms:
        key=tuple(sorted(monomial));values[key]=values.get(key,0)+coefficient
    return [[v,list(k)] for k,v in sorted(values.items()) if v]

def channel(slots,index):
    return dict(field='conj_fJ',input_slots=list(slots),field_index=index,order=1,input_type=TYPE)

def rewrite_batch(original,index):
    require(set(original)==BATCH_KEYS,'Unexpected parent batch keys')
    require(original['parity_module']=='q_linearnormalpole','Expected normalized-ten parent pole')
    require(0<=index<len(original['field_bindings']),'Wrong shared field index')
    old=original['field_bindings'][index]
    require(set(old)==FIELD_KEYS and old['field']==index and old['order']==1,'Wrong shared field binding')
    a,b=1+2*index,2+2*index
    require(equal(old['inputs'],[a,b]),'Wrong shared coefficient slots')
    y,w,power=old['evaluation'],old['norm'],old['power'];theta=original['conic_private']['theta']
    require(all(type(v) is int for v in (y,w,power,theta)),'Noninteger field reference')
    require(original['free']<=y<original['free']+original['locals'],'Nonlocal evaluation')
    powers={entry['exponent']:entry['variable'] for entry in original['contact_powers']}
    require(powers.get(2)==power,'Shared field does not use r squared')
    expected_y=row((1,[y]),(-1,[a]),(-1,[theta,b]))
    expected_w=row((1,[power,w]),(-2,[a,y]),(1,[a,a]),(-2,[b,b]))
    matches_y=[i for i,r in enumerate(original['residuals']) if equal(r,expected_y)]
    matches_w=[i for i,r in enumerate(original['residuals']) if equal(r,expected_w)]
    require(len(matches_y)==len(matches_w)==1,'Missing unique shared evaluation/norm rows')
    ry,rw=matches_y[0],matches_w[0]
    incidents={i for i,r in enumerate(original['residuals']) if any(y in mon for _,mon in r)}
    require(incidents=={ry,rw},'Shared evaluation has an outside row consumer')
    require(not any(y in call['args'] for call in original['calls']),'Shared evaluation has a call consumer')
    require(['variable',y,'conic evaluation'] in original['construction_log'],'Missing evaluation allocation')
    require(['equation',ry,'conic evaluation'] in original['construction_log'],'Missing evaluation equation')
    require(['equation',rw,'conic packed field norm'] in original['construction_log'],'Missing norm equation')
    def var(v):
        require(type(v) is int and v!=y,'Unexpected deleted-coordinate reference')
        return v-1 if v>y else v
    def equation(v):
        require(type(v) is int and v!=ry,'Unexpected deleted-row reference')
        return v-1 if v>ry else v
    def field(record):
        require(set(record)==FIELD_KEYS,'Unexpected field record keys')
        result=deepcopy(record)
        result['inputs']=[var(v) for v in record['inputs']]
        result['norm']=var(record['norm']);result['power']=var(record['power'])
        if record['field']==index:
            require(equal(record,old),'Inconsistent shared field metadata')
            result['evaluation']=None;result['input_type']=TYPE
        else:result['evaluation']=var(record['evaluation'])
        return result
    d=deepcopy(original);d['locals']-=1
    replacement=row((1,[power,w]),(-1,[a]),(-1,[theta,b]))
    d['residuals']=[[[c,[var(v) for v in mon]] for c,mon in (replacement if i==rw else r)]
                    for i,r in enumerate(original['residuals']) if i!=ry]
    log=[]
    for kind,number,label in original['construction_log']:
        if (kind,number) in {('variable',y),('equation',ry)}:continue
        require(kind in {'variable','equation'},'Unknown construction-log event')
        log.append([kind,var(number) if kind=='variable' else equation(number),label])
    d['construction_log']=log
    d['calls']=[{**call,'args':[var(v) for v in call['args']]} for call in original['calls']]
    d['conic_private']={k:var(v) for k,v in original['conic_private'].items()}
    d['conic_equations']=[equation(v) for v in original['conic_equations']]
    d['field_input_order']=[[var(v) for v in pair] for pair in original['field_input_order']]
    d['field_bindings']=[field(record) for record in original['field_bindings']]
    require(original['norm_tree'][0]=={'type':'literal','value':1},'Wrong constant leaf')
    d['norm_tree']=[deepcopy(original['norm_tree'][0])]+[field(record) for record in original['norm_tree'][1:]]
    d['contact_powers']=[dict(exponent=entry['exponent'],variable=var(entry['variable'])) for entry in original['contact_powers']]
    d['norm_root']=var(original['norm_root']);d['pole_inputs']=[var(v) for v in original['pole_inputs']]
    d['shared_square_input']={**channel([a,b],index),
        'removed_evaluation':y,'removed_equation':ry}
    return d

def rewrite_comparison(original,spec):
    slots=spec['slots'];index=spec['field'];d=deepcopy(original)
    require(original['free']==spec['free'],'Unexpected comparison arity')
    require('shared_square_input' not in original,'Shared square already installed')
    require(not any(v in slots for r in original['residuals'] for _,mon in r for v in mon),'Common field has a residual consumer')
    require(len(original['calls'])==1 and original['calls'][0]['module']==spec['batch'],'Wrong comparison call')
    args=original['calls'][0]['args'];start=1+2*index
    require(equal(args[start:start+2],slots),'Wrong comparison common field call')
    require(all(args.count(v)==1 for v in slots),'Common field has another call consumer')
    require(original['input_layout'].count('conj_fJ')==1,'Wrong common field layout token')
    d['input_layout']=original['input_layout'].replace('conj_fJ','square_conj_fJ')
    d['shared_square_input']=channel(slots,index)
    return d

def postprocess_modules(modules):
    """Return a new dictionary. The caller writes it before fresh flattening."""
    result=deepcopy(modules);root=result['Z_definition']
    require('shared_square_root' not in root,'Shared square already installed')
    calls=[call for call in root['calls'] if call['module'] in MODES]
    require(Counter(call['module'] for call in calls)==Counter({n:s['count'] for n,s in MODES.items()}),'Wrong comparison multiplicities')
    pairs=[tuple(call['args'][i] for i in MODES[call['module']]['slots']) for call in calls]
    require(len(set(pairs))==1,'Comparison calls disagree on common field')
    a,b=pairs[0];n=root['free']+root['locals'];nr=len(root['residuals'])
    require(all(type(v) is int and root['free']<=v<n for v in (a,b)) and a!=b,'Invalid original common pair')
    c,d=n,n+1;root['locals']+=2
    root['residuals'] += [row((1,[c]),(-1,[a,a]),(-2,[b,b])),row((1,[d]),(-2,[a,b]))]
    root['construction_log'] += [['variable',c,'shared conic field square.0'],['variable',d,'shared conic field square.1'],
        ['equation',nr,'shared conic field square.0'],['equation',nr+1,'shared conic field square.1']]
    for call in calls:
        for slot,value in zip(MODES[call['module']]['slots'],(c,d)):call['args'][slot]=value
    root['shared_square_root']=dict(field='conj_fJ',original_pair=[a,b],square_pair=[c,d],equations=[nr,nr+1],occurrences=37)
    for name,spec in MODES.items():
        result[name]=rewrite_comparison(modules[name],spec)
        result[spec['batch']]=rewrite_batch(modules[spec['batch']],spec['field'])
    changed=sorted(name for name in modules if not equal(modules[name],result[name]))
    require(set(changed)=={'Z_definition',*MODES,*(s['batch'] for s in MODES.values())},'Unexpected changed module set')
    return result,dict(changed_modules=changed,original_pair=[a,b],square_pair=[c,d],
        deleted_evaluations=37,added_root_coordinates=2,source_pin_authorized=False)
