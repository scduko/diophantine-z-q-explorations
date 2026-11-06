"""Bounded independent normalized-Lucas source mutation suite.

Run on an emitted source only after its outer pin/contract/flattening audit.
Resource aborts and code errors are not counted as semantic rejections.
"""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import audit_normalized_lucas as audit
import check_lucas_batch as batch

CORE_SHA='0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8'
ANCHOR_SHA='0e5f93f61114f9bd6589dc950271938b5d630820a920565043f63ab749081e30'
BASELINE={
    'Z_definition':'26b6b8674056bb3e7b4ba8ca75bd5b2b47cba7a58c1d84db78ba108a2f264117',
    'q_anchor':'e5b74df60328d739e94224f199efb16dd817c994658c95d5dd781704bcf94fb1',
    'q_batch41':'a45569adc62e09ce254b01cb38a3b31eb891842a73f515f21732eeeb24799985',
    'q_compare4':'ef3aba59c082b9dc312993cc5ea8d0298cc1c81b21e58d4762186bb9a53d4eb2',
    'q_height_batch':'22e3074cafdc80a71d39baf69d2012a8b039533d665f85f76da7f889dfe25761',
    'q_primeparity':'df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a',
}


def load_code(path,name,pin):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin,('Code pin',name)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def reject(name,action,reason):
    try:
        action()
    except AssertionError as error:
        assert error.args==(reason,),(name,'Wrong rejection checkpoint',error.args,reason)
        return name
    raise AssertionError((name,'Malformed source accepted'))


def row_id(obj,label,number=0):
    return [i for kind,i,tag in obj['construction_log'] if kind=='equation' and tag==label][number]


def flip(obj,label,number=0):
    i=row_id(obj,label,number)
    assert len(obj['residuals'][i])>=2
    obj['residuals'][i][0][0]*=-1
    return i


def sync_fields(obj):
    args=obj['calls'][0]['args']
    obj['conic_field_inputs']=[args[i:i+2] for i in range(1,len(args),2)]


def comparison_cases(c,source):
    name=source['name'];spec=audit.MODES[name];n=spec['n'];passed=[]
    def checked(label,obj,reason):
        passed.append(reject(name+' '+label,lambda:audit.check_comparison(c,obj),reason))
    tags=['joint chart K=(A-r)p.0','joint chart first relation.0',
          'joint chart second relation.0','H pH=GH.0']
    if spec['proxy_count']:tags+=['A=C p.0','A H=G.0']
    for tag in tags:
        obj=deepcopy(source);i=flip(obj,tag)
        checked(tag,obj,('Core equation',tag,i))
    for key,value,reason in (
            ('extra_target_start',source['extra_target_start']+3,'Extra-target metadata'),
            ('conic_legacy_input_count',source['free'],'Conic legacy input count'),
            ('ignored_shared_root_inputs',[source['free']-3,source['free']-2],'Ignored root inputs'),
            ('global_lucas_proxy_inputs',True,'Global proxy metadata'),
            ('difference_formal_tests',True,'Difference-test metadata'),
            ('joint_primary_difference_chart',False,'Joint-chart metadata')):
        obj=deepcopy(source);obj[key]=value;checked(key,obj,reason)
    obj=deepcopy(source);obj['calls'].append(deepcopy(obj['calls'][0]))
    checked('extra batch call',obj,'Comparison call count')
    obj=deepcopy(source);obj['calls'][0]['args'][0]=0
    checked('wrong contact',obj,('Ordered argument',0))
    obj=deepcopy(source);theta=source['ignored_shared_root_inputs'][0]
    obj['calls'][0]['args'][1]=theta;sync_fields(obj)
    checked('old theta passed as field',obj,'Old root input in conic call')
    obj=deepcopy(source);obj['conic_field_inputs'][0][0]=theta
    checked('false field metadata',obj,'Conic field input metadata')
    # Check the actual ordered expressions with self-consistent metadata.
    common=1+2*(n+1)
    alternate=1+2*(len(spec['orders'])-(n+1))
    for index,label in ((1,'primary formal'),(common,'common formal'),(alternate,'alternate')):
        obj=deepcopy(source);obj['calls'][0]['args'][index]=obj['calls'][0]['args'][2]
        sync_fields(obj);checked(label,obj,('Ordered argument',index))
    if spec['proxy_count']:
        index=1+2*(n+2)
        obj=deepcopy(source);obj['calls'][0]['args'][index]=obj['calls'][0]['args'][2]
        sync_fields(obj);checked('beta primary',obj,('Ordered argument',index))
    if name=='q_compare_beta':
        obj=deepcopy(source);obj['local_lucas_residual']=True
        checked('invented Lucas flag',obj,'Local Lucas metadata')
        obj=deepcopy(source);obj['local_lucas_evaluation']={}
        checked('invented Lucas evaluation',obj,'Local Lucas evaluation metadata')
        obj=deepcopy(source);obj['normalized_lucas_residual']=True
        checked('invented normalized metadata',obj,'Changed beta metadata')
    else:
        tags=['normalized Lucas B_'+role+' Lambda=G_'+role for role in ('s','t','z')]
        tags+=['normalized Lucas P Bs=ps','normalized Lucas (U+V)pt=P Bt',
               'normalized Lucas K pt=(1-2P)Bt','normalized Lucas V pz=(1-2P)Bz',
               'normalized Lucas E=U2-KV-P2']
        for label in tags:
            for component in (0,1):
                tag=label+'.'+str(component);obj=deepcopy(source);i=flip(obj,tag)
                checked(tag,obj,('Core equation',tag,i))
        obj=deepcopy(source);tag='normalized Lucas E=U2-KV-P2.0';i=row_id(obj,tag)
        obj['residuals'][i]=[[1,[obj['normalized_lucas_evaluation']['E'][0]]]]
        checked('exact zero replaces residual',obj,('Core equation',tag,i))
        obj=deepcopy(source);B=obj['normalized_lucas_evaluation']['B'];B['s'],B['t']=B['t'],B['s']
        checked('swapped evaluation numerators',obj,'Normalized Lucas evaluation metadata')
        for key in ('P','E'):
            obj=deepcopy(source);obj['normalized_lucas_evaluation'][key]=obj['normalized_lucas_evaluation']['V'][:]
            checked('false '+key+' metadata',obj,'Normalized Lucas evaluation metadata')
        obj=deepcopy(source);obj['normalized_lucas_evaluation']['order']=12
        checked('false evaluation order metadata',obj,'Normalized Lucas evaluation metadata')
        obj=deepcopy(source);obj['normalized_lucas_evaluation']['normalization']='F(C_s,C_t,C_z)'
        checked('unnormalized interpretation',obj,'Normalized Lucas evaluation metadata')
        obj=deepcopy(source);obj['normalized_lucas_residual']=False
        checked('normalized flag',obj,'Normalized Lucas metadata')
        obj=deepcopy(source);obj['global_numerator_p_nonzero']=True
        checked('obsolete global nonzero claim',obj,'Global numerator nonzero scope')
        obj=deepcopy(source);obj['local_lucas_evaluation']=None
        checked('restored unnormalized metadata',obj,'Obsolete unnormalized evaluation metadata')
        field=7 if name=='q_compare4' else 5;index=1+2*field
        obj=deepcopy(source);obj['field_inequality_orders'][field]=12
        checked('wrong residual order',obj,'Field orders')
        obj=deepcopy(source);obj['calls'][0]['args'][index:index+2]=obj['normalized_lucas_evaluation']['P'][:]
        sync_fields(obj);checked('P replaces E field',obj,('Ordered argument',index))
        obj=deepcopy(source);args=obj['calls'][0]['args'];args[index:index+4]=args[index+2:index+4]+args[index:index+2]
        sync_fields(obj);checked('E swaps with alternate',obj,('Ordered argument',index))
        obj=deepcopy(source);i=len(obj['residuals'])
        obj['residuals'].append([[1,[obj['normalized_lucas_evaluation']['E'][0]]]])
        obj['construction_log'].append(['equation',i,'exact zero Lucas residual'])
        checked('extra exact zero equation',obj,'Core row labels')
        obj=deepcopy(source);i=row_id(obj,'normalized Lucas B_s Lambda=G_s.0');del obj['residuals'][i]
        obj['construction_log']=[op for op in obj['construction_log'] if not (op[0]=='equation' and op[1]==i)]
        for op in obj['construction_log']:
            if op[0]=='equation' and op[1]>i:op[1]-=1
        checked('missing B_s equation',obj,'Core row labels')
        obj=deepcopy(source);fresh=obj['free']+obj['locals'];obj['locals']+=1
        obj['construction_log'].append(['variable',fresh,'forbidden normalization inverse'])
        P_id=obj['normalized_lucas_evaluation']['P'][0];i=len(obj['residuals'])
        obj['residuals'].append([[-1,[]],[1,sorted([P_id,fresh])]])
        obj['construction_log'].append(['equation',i,'forbidden normalization inverse'])
        checked('extra normalization inverse',obj,'Core row labels')
        # Use the already allocated B_s in the later B_t row, so this reaches
        # the equation check rather than merely failing forward-reference parsing.
        obj=deepcopy(source);tag='normalized Lucas B_t Lambda=G_t.0';i=row_id(obj,tag)
        B=obj['normalized_lucas_evaluation']['B'];swaps=dict(zip(B['t'],B['s']))
        for term in obj['residuals'][i]:term[1]=sorted(swaps.get(v,v) for v in term[1])
        checked('changed numerator role in equation',obj,('Core equation',tag,i))
        obj=deepcopy(source);tag='normalized Lucas K pt=(1-2P)Bt.0';i=row_id(obj,tag)
        P_ids=set(obj['normalized_lucas_evaluation']['P'])
        term=next(term for term in obj['residuals'][i] if len(term[1])==2 and P_ids.intersection(term[1]))
        assert term[0]%2==0;term[0]//=2
        checked('normalization factor two',obj,('Core equation',tag,i))
    return passed


def root_cases(c,source,old):
    passed=[]
    def checked(label,obj,reason):
        passed.append(reject('root '+label,lambda:audit.check_root(c,obj,old),reason))
    for tag in ('jacobi target reciprocal.0','jacobi target ordinate ratio.0',
                'shared joint coefficient r.0','shared joint coefficient s.0',
                'shared joint coefficient t.0','shared joint coefficient u.0'):
        obj=deepcopy(source);i=flip(obj,tag);checked(tag,obj,('Root equation',i))
    for name,spec in audit.MODES.items():
        obj=deepcopy(source);call=next(item for item in obj['calls'] if item['module']==name)
        index=spec['proxy_count'];call['args'][index:index+4]=call['args'][index+2:index+4]+call['args'][index:index+2]
        checked(name+' target swap',obj,('Root field','calls'))
        obj=deepcopy(source);call=next(item for item in obj['calls'] if item['module']==name)
        base=spec['proxy_count']+4*(spec['n']+1)+7
        call['args'][base:base+4]=call['args'][base+2:base+4]+call['args'][base:base+2]
        checked(name+' extra-target swap',obj,('Root field','calls'))
    for module in ('q_anchor','q_height_batch'):
        obj=deepcopy(source);call=next(item for item in obj['calls'] if item['module']==module)
        call['args'][0]=0;checked(module+' target',obj,('Root field','calls'))
    for key,value in (
            ('proxy_indices',[0]),('retained_proxy_roles',['beta','s']),
            ('local_lucas_residual',False),('local_lucas_polynomial','E=0'),
            ('lucas_proxy_removal',{}),('joint_chart_extra_target_coordinates',42)):
        obj=deepcopy(source);obj[key]=value;checked(key,obj,('Root field',key))
    obj=deepcopy(source);obj['pell_equation']='restored'
    checked('restored proxy metadata',obj,'Root metadata fields')
    obj=deepcopy(source);i=len(obj['residuals']);obj['residuals'].append([[1,[0]]])
    obj['construction_log'].append(['equation',i,'extra root condition'])
    checked('extra equation',obj,('Root field','construction_log'))
    return passed


def batch_cases(c,source,orders):
    name=source['name'];passed=[]
    def checked(label,obj,reason):
        passed.append(reject(name+' '+label,lambda:batch.check_batch(c,obj,orders),reason))
    for tag in ('private conic square','private conic discriminant','conic evaluation',
                'conic packed field norm','cubic norm node','batched square','parity argument'):
        obj=deepcopy(source);i=flip(obj,tag);checked(tag,obj,('Conic equation',tag,i))
    obj=deepcopy(source);i=row_id(obj,'private conic discriminant')
    for term in obj['residuals'][i]:term[1]=sorted(1 if v==0 else v for v in term[1])
    checked('wrong raw contact',obj,('Conic equation','private conic discriminant',i))
    obj=deepcopy(source);i=row_id(obj,'conic packed field norm');power=obj['norm_tree'][1]['power']
    for term in obj['residuals'][i]:term[1]=sorted(0 if v==power else v for v in term[1])
    checked('odd raw normalization',obj,('Conic equation','conic packed field norm',i))
    obj=deepcopy(source);i=row_id(obj,'conic packed field norm');del obj['residuals'][i]
    obj['construction_log']=[op for op in obj['construction_log'] if not (op[0]=='equation' and op[1]==i)]
    for op in obj['construction_log']:
        if op[0]=='equation' and op[1]>i:op[1]-=1
    checked('missing field constraint',obj,('Conic row multiplicity','conic packed field norm'))
    for key in ('field_input_order','sorted_field_indices','field_bindings','contact_powers'):
        obj=deepcopy(source);obj[key]=list(reversed(obj[key]));checked(key,obj,('Conic metadata',key))
    obj=deepcopy(source);obj['norm_tree'][0]['value']=0
    checked('missing literal one',obj,('Conic metadata','norm_tree'))
    obj=deepcopy(source);obj['conic_private']['theta']=1
    checked('conic boundary capture',obj,('Conic metadata','conic_private'))
    obj=deepcopy(source);obj['calls'][0]['args']=[0]
    checked('wrong pole argument',obj,'Conic parity call')
    obj=deepcopy(source);obj['calls'].append(deepcopy(obj['calls'][0]))
    checked('extra pole call',obj,'Conic parity call')
    obj=deepcopy(source);fresh=obj['free']+obj['locals'];obj['locals']+=1
    obj['construction_log'].append(['variable',fresh,'old error leaf'])
    checked('extra old leaf',obj,'Unaccounted conic coordinates')
    obj=deepcopy(source);i=len(obj['residuals']);obj['residuals'].append([[1,[0]]])
    obj['construction_log'].append(['equation',i,'extra conic condition'])
    checked('extra condition',obj,'Unconsumed conic rows')
    return passed


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('core','source','baseline','report'):p.add_argument('--'+flag,type=Path,required=True)
    p.add_argument('--anchor-checker',type=Path)
    p.add_argument('--seconds',type=int,default=180)
    args=p.parse_args();assert 1<=args.seconds<=600
    c=load_code(args.core,'local_lucas_core',CORE_SHA);c.DEADLINE=time.monotonic()+args.seconds
    deadline=c.DEADLINE;c.DEADLINE=0
    try:
        reject('deadline regression',c.tick,'not a resource failure')
    except c.CheckerResourceError:
        resource_regressions=1
    else:
        raise RuntimeError('Resource abort became a semantic rejection')
    finally:
        c.DEADLINE=deadline
    old={}
    for name,pin in BASELINE.items():
        path=args.baseline/'modules'/(name+'.json')
        assert c.file_sha256(path)==pin,('Baseline pin',name)
        old[name]=c.load(path)
    assert {p.stem for p in (args.source/'modules').glob('*.json')}==audit.MODULES
    modules={name:c.load(args.source/'modules'/(name+'.json')) for name in audit.MODULES}
    anchor=None
    if args.anchor_checker:anchor=load_code(args.anchor_checker,'local_lucas_anchor',ANCHOR_SHA).check_anchor
    positive=audit.check_modules(c,modules,old,conic_batch_check=batch.check_batch,anchor_check=anchor)
    passed=root_cases(c,modules['Z_definition'],old['Z_definition'])
    for name,spec in audit.MODES.items():
        passed+=comparison_cases(c,modules[name])
        passed+=batch_cases(c,modules[spec['batch']],audit.field_orders(spec))
    assert len(passed)==len(set(passed)),'Duplicate mutation names'
    # Explicit family inventory: root22 + comparisons126 + batches60.
    assert len(passed)==208,('Mutation inventory',len(passed))
    c.tick()
    report=dict(status='PASS',negative_count=len(passed),negative_cases=passed,
                resource_abort_regressions=resource_regressions,module_positive=positive,
                core_sha256=CORE_SHA,auditor_sha256=c.file_sha256(Path(audit.__file__)),
                batch_checker_sha256=c.file_sha256(Path(batch.__file__)),test_sha256=c.file_sha256(Path(__file__)),
                scope='Module semantics only; outer pins/contract/flattening and finite replay required')
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',negative_count=len(passed))))


if __name__=='__main__':main()
