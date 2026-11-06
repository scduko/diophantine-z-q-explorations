"""Independent exact restoration to a REQUIRED fully audited parent.

Restoration is a specification comparison, not an old-witness map: the
denominator change is justified by the separately reviewed arithmetic proof.
No producer is imported. The parent callback must raise on failure.
"""
from copy import deepcopy
import json


class ResourceError(RuntimeError):
    pass


def bounded(value):
    stack=[(value,0)];nodes=0;chars=0
    while stack:
        x,depth=stack.pop();nodes+=1
        if nodes>300000 or depth>48:raise ResourceError('JSON tree bound')
        if isinstance(x,(list,dict)):
            if len(x)>16384:raise ResourceError('JSON container bound')
            stack.extend((v,depth+1) for v in (x if isinstance(x,list) else list(x.values())+list(x.keys())))
        elif isinstance(x,str):
            chars+=len(x)
            if len(x)>8192 or chars>2000000:raise ResourceError('JSON string bound')
        elif type(x) is int:
            if x.bit_length()>4096:raise ResourceError('JSON integer bound')
        elif x is not None and type(x) is not bool:
            raise AssertionError('Unexpected JSON scalar')


def same(a,b):
    return json.dumps(a,sort_keys=True,separators=(',',':'))==json.dumps(b,sort_keys=True,separators=(',',':'))


def need(value,message):
    if not value:raise AssertionError(message)


def enc(terms):
    return [[c,list(mon)] for mon,c in sorted(terms.items()) if c]


def restore_batch(obj):
    bounded(obj);b=deepcopy(obj)
    need(b['name'] in ('q_conic13','q_conic6','q_conic10'),'Batch name')
    meta=b.pop('first_norm_fusion')
    keys={'field','role','order','numerator','first_node','numerator_row','first_node_row',
          'original_power','virtual_denominator','virtual_denominator_exponent'}
    need(set(meta)==keys,'Fusion metadata keys')
    need(meta['role']=='H.f','Field role')
    for k in keys-{'role'}:need(type(meta[k]) is int,'Metadata integer type')
    need(meta['field']==0 and meta['order']==1 and meta['virtual_denominator']==0 and
         meta['virtual_denominator_exponent']==1,'Fusion field/order/denominator')
    T,N,P=meta['numerator'],meta['first_node'],meta['original_power']
    ri,ni=meta['numerator_row'],meta['first_node_row']
    total=b['free']+b['locals']
    need(len({T,N,P})==3 and all(b['free']<=v<total for v in (T,N,P)),'Local IDs')
    need(0<=ri<len(b['residuals']) and 0<=ni<len(b['residuals']) and ri!=ni,'Row IDs')
    f=b['field_bindings'][0]
    need(set(f)=={'type','field','order','inputs','evaluation','norm','power','numerator',
                 'virtual_denominator_exponent'},'Typed field keys')
    need(f['type']=='conic_first_numerator' and type(f['field']) is int and f['field']==0
         and type(f['order']) is int and f['order']==1 and same(f['inputs'],[1,2])
         and f['norm'] is None and type(f['power']) is int and f['power']==0
         and type(f['numerator']) is int and f['numerator']==T
         and type(f['virtual_denominator_exponent']) is int and f['virtual_denominator_exponent']==1,
         'Typed first field')
    Y=f['evaluation'];need(type(Y) is int and b['free']<=Y<total,'Evaluation ID')
    need(same(b['norm_tree'][0],dict(type='literal',value=1)) and same(b['norm_tree'][1],f),'First tree pair')
    need(same(b['residuals'][ri],enc({(T,):1,(1,1):1,tuple(sorted((1,Y))):-2,(2,2):-2})), 'Numerator equation')
    need(same(b['residuals'][ni],enc({tuple(sorted((0,N))):1,(0,):-1,(T,T):-1})), 'Fused first node equation')
    occurrences={i for i,row in enumerate(b['residuals']) if any(T in mon for _,mon in row)}
    need(occurrences=={ri,ni} and all(T not in call['args'] for call in b['calls']),'Outside numerator use')
    f.pop('numerator');f.pop('virtual_denominator_exponent')
    f.update(type='conic_field',norm=T,power=P)
    b['norm_tree'][1]=deepcopy(f)
    b['residuals'][ri]=enc({tuple(sorted((P,T))):1,(1,1):1,tuple(sorted((1,Y))):-2,(2,2):-2})
    b['residuals'][ni]=enc({():-1,(0,T,T):-1,(N,):1})
    replacements={('variable',T):('first conic field numerator','conic packed field norm'),
                  ('equation',ri):('first conic field numerator','conic packed field norm'),
                  ('variable',N):('fused first norm node','cubic norm node'),
                  ('equation',ni):('fused first norm node','cubic norm node')}
    counts={key:0 for key in replacements}
    for item in b['construction_log']:
        key=tuple(item[:2])
        if key in replacements:
            before,after=replacements[key];need(item[2]==before,'New label')
            counts[key]+=1;item[2]=after
    need(all(n==1 for n in counts.values()),'Unique changed log events')
    suffix='; first H.f virtual leaf is numerator/r, fused with literal1'
    need(b['semantics'].endswith(suffix),'Explicit fused semantics')
    b['semantics']=b['semantics'][:-len(suffix)]
    return b


def restore_modules(modules):
    bounded(modules);out=deepcopy(modules)
    for name in ('q_conic13','q_conic6','q_conic10'):
        need(name in modules,'Required batch')
        out[name]=restore_batch(modules[name])
    return out


def check_modules(modules,parent_check):
    restored=restore_modules(modules)
    result=parent_check(restored)
    if type(result) is bool:raise TypeError('Parent checker must raise on failure, not return Boolean')
    return dict(status='PASS: exact delta and required parent check',parent=result,
                source_pin_authorized=False)
