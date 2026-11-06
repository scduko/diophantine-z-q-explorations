"""Independent literal four-tangent check on small pinned root dictionaries."""
if not __debug__:
    raise RuntimeError('Assertions must remain enabled for the tangent audit')

from copy import deepcopy
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path

PARENT='1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2'
PRODUCER='a136e6cce43277ed63351fd1989c428c48b811b9a8682d213f6609d6a95f5cb2'
BLOCKS=[('A',2,4,36,14),('S',10,12,46,24),('T',14,16,56,34),('Z',18,20,66,44)]
GONE={38,39,48,49,58,59,68,69}
DELETED={16,17,26,27,36,37,46,47}
VM={old:new for new,old in enumerate(i for i in range(219) if i not in GONE)}
RM={old:new for new,old in enumerate(i for i in range(203) if i not in DELETED)}


class TangentResourceError(RuntimeError):
    pass


def preflight(obj):
    stack=[(obj,0)];count=0
    while stack:
        value,depth=stack.pop();count+=1
        if count>200000 or depth>32:raise TangentResourceError('Tangent JSON node/depth limit')
        if type(value) is dict:
            if len(value)>4096:raise TangentResourceError('Tangent JSON object limit')
            assert all(type(k) is str for k in value),'Tangent JSON keys'
            stack.extend((v,depth+1) for v in value.values())
            stack.extend((k,depth+1) for k in value)
        elif type(value) is list:
            if len(value)>4096:raise TangentResourceError('Tangent JSON list limit')
            stack.extend((v,depth+1) for v in value)
        elif type(value) is str:
            if len(value)>8192:raise TangentResourceError('Tangent JSON string limit')
        elif type(value) is int:
            if value.bit_length()>1024:raise TangentResourceError('Tangent JSON integer limit')
        elif value is None or type(value) is bool:pass
        else:raise AssertionError('Tangent JSON scalar type')


def canonical(x):
    preflight(x)
    return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
def exact(x,y,message):assert canonical(x)==canonical(y),message
def vi(values):return [VM[x] for x in values]
def ri(values):return [RM[x] for x in values]
def row(*terms):return [[c,sorted(m)] for c,m in sorted(terms,key=lambda x:tuple(sorted(x[1])))]


def expected(parent):
    assert sha256(canonical(parent)).hexdigest()==PARENT,'Four-tangent parent pin'
    oldrows=deepcopy(parent['residuals']);labels={};records=[];incidence=[]
    for role,x,y,q,at in BLOCKS:
        l=q+4
        oldrows[at+4]=row((11,[]),(2,[y,l]),(4,[y+1,l+1]),(-3,[q]))
        oldrows[at+5]=row((-6,[]),(2,[y,l+1]),(2,[y+1,l]),(-3,[q+1]))
        for k in range(2):labels[at+4+k]='direct tangent '+role+'.1.'+str(k)
        h={q+2,q+3}
        consumers=[i for i,r in enumerate(parent['residuals']) if any(h.intersection(m) for _,m in r)]
        calls=[i for i,c in enumerate(parent['calls']) if h.intersection(c['args'])]
        assert consumers==list(range(at+2,at+6)) and not calls,'Private inverse incidence'
        incidence.append(dict(role=role,removed_inverse=sorted(h),residual_consumers=consumers,call_consumers=calls))
        records.append(dict(role=role,step=1,
            input_x=[[[1,[VM[x]]]],[[1,[VM[x+1]]]]],
            input_y=[[[1,[VM[y]]]],[[1,[VM[y+1]]]]],
            square=vi([q,q+1]),slope=vi([l,l+1]),square_rows=ri([at,at+1]),
            tangent_rows=ri([at+4,at+5]),slope_square_rows=ri([at+6,at+7]),
            ordinate_product_rows=ri([at+8,at+9])))
    result=deepcopy(parent);result['locals']=210
    result['residuals']=[[[c,vi(m)] for c,m in oldrows[i]] for i in range(203) if i not in DELETED]
    result['calls']=[dict(c,args=vi(c['args'])) for c in parent['calls']]
    result['construction_log']=[]
    for kind,index,label in parent['construction_log']:
        mapping=VM if kind=='variable' else RM
        if index in mapping:
            result['construction_log'].append([kind,mapping[index],labels.get(index,label) if kind=='equation' else label])
    result['proxy_indices']=vi(parent['proxy_indices'])
    result['point_coordinates']={role:vi(values) for role,values in parent['point_coordinates'].items()}
    result['joint_chart_targets']=[{key:vi(values) for key,values in obj.items()} for obj in parent['joint_chart_targets']]
    result['root_targets']=[{key:value if key=='kind' else vi(value) for key,value in obj.items()} for obj in parent['root_targets']]
    result['general_root_charts']={role:{key:value if key=='kind' else ri(value) if key.endswith('_rows') else vi(value)
        for key,value in obj.items()} for role,obj in parent['general_root_charts'].items()}
    result['fixed_target_bindings']={key:ri(values) if key.endswith('rows') else vi(values)
        for key,values in parent['fixed_target_bindings'].items()}
    result['target_two_bindings']=dict(rows=ri(parent['target_two_bindings']['rows']),first_doubling_only=True)
    result['direct_tangent_doublings']=records
    result['root_doubling_model']='direct tangent with retained square coordinates'
    result['direct_tangent_rewrite']=dict(parent_root_canonical_sha256=PARENT,
        parent_removed_variables=sorted(GONE),parent_removed_rows=sorted(DELETED),
        historical_index_scope='parent_* IDs refer to the pre-tangent target-two root module',
        raw_variable_delta=-8,raw_row_delta=-8,doublings=4,
        nonzero_proof='y*[2*lambda*(3*q-2*D)-9*x*y]=2*D^2, D=11-6sqrt(2) nonzero',
        inverse_recovery='inverse(2*y)=[2*lambda*(3*q-2*D)-9*x*y]/(4*D^2)',source_pin_authorized=False)
    return result,incidence


def check(parent,candidate):
    exp,incidence=expected(parent)
    exact(candidate,exp,'Complete four-tangent root mismatch')
    return incidence


def audit_root_transition(target2_root,tangent_root):
    """Exact root-only transition. Outer checker owns full source acceptance."""
    incidence=check(target2_root,tangent_root)
    return dict(status='PASS: exact four-tangent root transition',inverse_incidence=incidence,
                removed_variables=8,removed_rows=8,complete_source_acceptance=False)


def square_sum(rows):
    result={}
    for r in rows:
        for ca,ma in r:
            for cb,mb in r:
                key=tuple(sorted(ma+mb));result[key]=result.get(key,0)+ca*cb
    return {key:value for key,value in result.items() if value}


def fixed_aggregate(parent,candidate,report):
    names=['x0','x1','F0','F1','q0','q1','s0','s1','t0','t1','r0','r1','u0','u1']
    pmeta=parent['fixed_target_bindings'];cmeta=candidate['fixed_target_bindings']
    old_ids=pmeta['coordinates']+pmeta['linear_coordinates']
    old_rows=pmeta['rows']+pmeta['linear_rows']
    old_names=dict(zip(old_ids,names));old_names.update({80:'J0',81:'J1'})
    new_names={VM[v]:name for v,name in old_names.items()}
    def encode(obj,rows,names):return [[[c,[names[v] for v in m]] for c,m in obj['residuals'][i]] for i in rows]
    a=square_sum(encode(parent,old_rows,old_names))
    b=square_sum(encode(candidate,cmeta['rows']+cmeta['linear_rows'],new_names))
    assert a==b,'Fixed-target binding polynomial changed'
    literal={tuple(m):c for c,m in report['fourteen_binding_sos']['terms']}
    assert a==literal,'Fixed-target binding report mismatch'
    const=lambda obj:sum(sum(c for c,m in r if not m)**2 for r in obj['residuals'])
    before,after=const(parent),const(candidate)
    assert (before,after,after-before)==(5061814037,5061814661,624)
    return dict(fixed_binding_rows=14,fixed_sos_unchanged=True,
        fixed_sos_constant=a.get((),0),fixed_sos_max=max(map(abs,a.values())),
        root_sos_constant_before=before,root_sos_constant_after=after,root_sos_constant_delta=after-before)


def load(name,path,pin):
    assert sha256(path.read_bytes()).hexdigest()==pin,'Probe dependency pin'
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();base=Path(__file__).resolve().parents[3]
    b=load('base_audit',base/'charts/sub5000/half-generator-review/audit_root_rewrite.py',
        '05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2')
    a=load('target2_audit',base/'charts/sub5000/root-target2/audit_target2.py',
        'b2737e3575ad8512dcc33c6c1d84f38178172e53b5d786193d8eed5c1df886c3')
    emitter=load('tangent_emitter',base/'elimination/sub5000/doubling-target-two/compress_doublings.py',PRODUCER)
    constants=base/'charts/sub5000/root-target2/FIXED_TARGET2.json'
    assert sha256(constants.read_bytes()).hexdigest()=='2a52cbd19d92fedcf75b94e0cc0bc11673fd40775fde83cec621ba23c7b93c62'
    parent=a.expected_root(b,b.load_parent(args.parents)['Z_definition'])
    candidate,_=emitter.rewrite_root(parent)
    incidence=check(parent,candidate)
    aggregate=fixed_aggregate(parent,candidate,json.loads(constants.read_text(encoding='utf-8')))
    tests=[]
    changed=[RM[at+k] for _,_,_,_,at in BLOCKS for k in (4,5)]
    fixed=candidate['fixed_target_bindings']['rows']+candidate['fixed_target_bindings']['linear_rows']
    for i in changed+fixed:
        bad=deepcopy(candidate);bad['residuals'][i][0][0]+=1
        try:check(parent,bad)
        except AssertionError as error:assert str(error)=='Complete four-tangent root mismatch'
        else:raise AssertionError('Mutated candidate accepted')
        tests.append(i)
    for label,mutate in (
            ('missing row',lambda o:o['residuals'].pop()),
            ('extra row',lambda o:o['residuals'].append([[1,[0]]])),
            ('wrong call',lambda o:o['calls'][0]['args'].__setitem__(0,1)),
            ('wrong fixed record',lambda o:o['fixed_target_bindings']['rows'].__setitem__(0,0)),
            ('wrong target record',lambda o:o['target_two_bindings']['rows'].__setitem__(0,0)),
            ('wrong old receipt',lambda o:o['general_root_rewrite'].update(raw_variable_delta=0)),
            ('extra metadata',lambda o:o.update(unchecked=1)),
            ('boolean coordinate count',lambda o:o.update(free=True))):
        bad=deepcopy(candidate);mutate(bad)
        try:audit_root_transition(parent,bad)
        except AssertionError as error:assert str(error)=='Complete four-tangent root mismatch'
        else:raise AssertionError('Structural mutation accepted')
        tests.append(label)
    bad=deepcopy(parent);bad['residuals'][0][0][0]+=1
    try:audit_root_transition(bad,candidate)
    except AssertionError as error:assert str(error)=='Four-tangent parent pin'
    else:raise AssertionError('Parent mutation accepted')
    tests.append('parent pin')
    try:audit_root_transition(parent,{'oversized':'x'*8193})
    except TangentResourceError:pass
    else:raise AssertionError('Tangent resource limit failed')
    result=dict(status='PASS: INDEPENDENT FOUR-TANGENT ROOT PROBE',
        parent_canonical_sha256=PARENT,producer_sha256=PRODUCER,
        output_canonical_sha256=sha256(canonical(candidate)).hexdigest(),
        unchanged_rows=187,semantic_rejections=len(tests),resource_abort_cases=1,inverse_incidence=incidence,
        fixed_aggregation=aggregate,source_locals=210,source_rows=195,
        full_source_accepted=False,full_source_generated=False)
    args.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='inverse_incidence'}))


if __name__=='__main__':main()
