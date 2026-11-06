"""Small module-dictionary tests only; never flatten or expand a source."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import first_norm as producer
import audit_first_norm as audit


def parent_checker(expected):
    def check(actual):
        if not audit.same(actual,expected):raise AssertionError('Complete parent differs')
        return dict(status='exact complete parent dictionary')
    return check


def mutation_cases(modules):
    for name in producer.NAMES:
        original=modules[name];meta=original['first_norm_fusion'];f=original['field_bindings'][0]
        ri=meta['numerator_row'];ni=meta['first_node_row'];T=meta['numerator']
        edits=[]
        def add(label,change):edits.append((name+': '+label,change))
        for row_name,index in [('numerator',ri),('first node',ni)]:
            add(row_name+' coefficient',lambda m,i=index:m['residuals'][i][0].__setitem__(0,9))
            add(row_name+' missing term',lambda m,i=index:m['residuals'][i].pop())
        for key,value in [('field',1),('role','X0.f'),('order',2),('numerator',T+1),
                          ('first_node',T),('original_power',0),('virtual_denominator',1),
                          ('virtual_denominator_exponent',2),('order',True)]:
            add('metadata '+key+' '+str(value),lambda m,k=key,v=value:m['first_norm_fusion'].__setitem__(k,v))
        for key,value in [('type','conic_field'),('norm',T),('power',meta['original_power']),
                          ('numerator',T+1),('virtual_denominator_exponent',True),('order',2)]:
            def change(m,k=key,v=value):
                m['field_bindings'][0][k]=v;m['norm_tree'][1][k]=v
            add('coherent field '+key,change)
        add('tree pair mismatch',lambda m:m['norm_tree'][1].__setitem__('numerator',T+1))
        add('literal anchor',lambda m:m['norm_tree'][0].__setitem__('value',2))
        add('retained conic changed',lambda m:m['residuals'][1][0].__setitem__(0,-3))
        add('outside numerator use',lambda m:m['residuals'].append([[1,[T]]]))
        add('outside numerator call',lambda m:m['calls'][0]['args'].append(T))
        add('last node missing',lambda m:m['residuals'].pop())
        add('last node changed',lambda m:m['residuals'][-1][0].__setitem__(0,11))
        add('semantics omitted',lambda m:m.__setitem__('semantics','old interpretation'))
        add('new hidden variable',lambda m:m.__setitem__('locals',m['locals']+1))
        add('unknown metadata',lambda m:m['first_norm_fusion'].__setitem__('skip_check',True))
        for label,change in edits:
            changed=deepcopy(modules);change(changed[name]);yield label,changed


def run(modules):
    before=deepcopy(modules);after,_=producer.postprocess_modules(modules)
    if not audit.same(before,modules):raise AssertionError('Producer mutated input')
    audit.check_modules(after,parent_checker(before))
    accepted=[]
    for label,changed in mutation_cases(after):
        try:audit.check_modules(changed,parent_checker(before))
        except AssertionError:accepted.append(label)
        else:raise AssertionError('Malformed module accepted: '+label)
    resources=[]
    for label,value in [('wide list',[0]*16385),('long string','x'*8193),('large integer',1<<4096)]:
        changed=deepcopy(after);changed['resource_fixture']=value
        try:audit.restore_modules(changed)
        except audit.ResourceError:resources.append(label)
        else:raise AssertionError('Resource limit not raised: '+label)
    deep=0
    for _ in range(50):deep=[deep]
    changed=deepcopy(after);changed['resource_fixture']=deep
    try:audit.restore_modules(changed)
    except audit.ResourceError:resources.append('deep list')
    else:raise AssertionError('Depth limit not raised')
    callback_rejections=0
    for result in (False,True):
        try:audit.check_modules(after,lambda m,r=result:r)
        except TypeError:callback_rejections+=1
        else:raise AssertionError('Boolean callback accepted')
    return dict(status='PASS: module dictionaries only',semantic_rejections=len(accepted),
                resource_aborts=len(resources),boolean_callback_rejections=callback_rejections,
                exact_parent_restoration=True,source_generated=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--modules',type=Path,required=True)
    p.add_argument('--report',type=Path)
    a=p.parse_args();modules={};pins={}
    files=sorted(a.modules.glob('*.json'))
    if not 10<=len(files)<=20:raise ValueError('Expected a small complete module set')
    for path in files:
        data=path.read_bytes()
        if len(data)>4_000_000:raise audit.ResourceError('Module byte bound')
        modules[path.stem]=json.loads(data);pins[path.name]=hashlib.sha256(data).hexdigest()
    report=run(modules);report['module_sha256']=pins
    if a.report:a.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='module_sha256'}))


if __name__=='__main__':main()
