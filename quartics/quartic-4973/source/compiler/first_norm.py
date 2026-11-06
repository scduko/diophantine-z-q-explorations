"""Pure module postpass. Complete parent and new-source audits are mandatory."""
from copy import deepcopy

NAMES=('q_conic13','q_conic6','q_conic10')
SUFFIX='; first H.f virtual leaf is numerator/r, fused with literal1'


def need(value,message):
    if not value:raise ValueError(message)


def polynomial(row):
    return {tuple(mon):c for c,mon in row}


def encoded(row):
    return [[c,list(mon)] for mon,c in sorted(row.items()) if c]


def apply_batch(old):
    need(old['name'] in NAMES and 'first_norm_fusion' not in old,'Wrong parent batch')
    b=deepcopy(old);f=b['field_bindings'][0]
    need(f['type']=='conic_field' and f['field']==0 and f['order']==1,'First field')
    need(f['inputs']==[1,2] and b['norm_tree'][:2]==[dict(type='literal',value=1),f], 'First tree pair')
    T=f['norm'];P=f['power'];Y=f['evaluation'];A,B=f['inputs']
    need(type(T) is int and type(P) is int and type(Y) is int,'Coordinate types')
    old_leaf={(A,A):1,tuple(sorted((A,Y))):-2,(B,B):-2,tuple(sorted((P,T))):1}
    leaves=[i for i,row in enumerate(b['residuals']) if polynomial(row)==old_leaf]
    need(len(leaves)==1,'Packed row');ri=leaves[0]
    nodes=[]
    for i,row in enumerate(b['residuals']):
        d=polynomial(row)
        for mon,c in d.items():
            if len(mon)==1 and c==1 and d=={():-1,(0,T,T):-1,mon:1}:
                nodes.append((i,mon[0]))
    need(len(nodes)==1,'First constant norm node');ni,N=nodes[0]
    uses={i for i,row in enumerate(b['residuals']) if any(T in mon for _,mon in row)}
    need(uses=={ri,ni} and all(T not in c['args'] for c in b['calls']),'Outside leaf use')
    b['residuals'][ri]=encoded({(T,):1,(A,A):1,tuple(sorted((A,Y))):-2,(B,B):-2})
    b['residuals'][ni]=encoded({tuple(sorted((0,N))):1,(0,):-1,(T,T):-1})
    labels={('variable',T):('conic packed field norm','first conic field numerator'),
            ('equation',ri):('conic packed field norm','first conic field numerator'),
            ('variable',N):('cubic norm node','fused first norm node'),
            ('equation',ni):('cubic norm node','fused first norm node')}
    seen=set()
    for event in b['construction_log']:
        key=tuple(event[:2])
        if key in labels:
            before,after=labels[key];need(event[2]==before,'Old label')
            event[2]=after;seen.add(key)
    need(seen==set(labels),'Complete labels')
    replacement=deepcopy(f)
    replacement.update(type='conic_first_numerator',norm=None,power=0,numerator=T,
                       virtual_denominator_exponent=1)
    b['field_bindings'][0]=deepcopy(replacement);b['norm_tree'][1]=deepcopy(replacement)
    b['first_norm_fusion']=dict(field=0,role='H.f',order=1,numerator=T,
        first_node=N,numerator_row=ri,first_node_row=ni,original_power=P,
        virtual_denominator=0,virtual_denominator_exponent=1)
    b['semantics']+=SUFFIX
    return b


def postprocess_modules(modules):
    need(set(NAMES)<=set(modules),'Missing comparison batch')
    result=deepcopy(modules)
    for name in NAMES:result[name]=apply_batch(modules[name])
    return result,dict(transformed_batches=list(NAMES),source_coordinate_delta=0,
                       source_row_delta=0,straightforward_lift_delta=-37,
                       measured_endpoint_delta=False)
