"""Bounded semantic mutations for the independently audited conic source.

Full source generation and this suite belong in the root's remote workflow.
Resource exceptions and unexpected program errors are never rejections.
"""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import audit_conic_source as audit

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


def remove_row(obj,i):
    del obj['residuals'][i]
    obj['construction_log']=[op for op in obj['construction_log'] if not (op[0]=='equation' and op[1]==i)]
    for op in obj['construction_log']:
        if op[0]=='equation' and op[1]>i:
            op[1]-=1


def batch_cases(c,source,orders):
    name=source['name'];passed=[]
    for tag in ('private conic square','private conic discriminant','conic evaluation',
                'conic packed field norm','cubic norm node','batched square','parity argument'):
        obj=deepcopy(source);i=flip(obj,tag)
        passed.append(reject(name+' changed '+tag,lambda:audit.check_batch(c,obj,orders),('Conic equation',tag,i)))
    obj=deepcopy(source);i=row_id(obj,'private conic discriminant')
    for term in obj['residuals'][i]:
        term[1]=sorted(1 if x==0 else x for x in term[1])
    passed.append(reject(name+' wrong raw contact',lambda:audit.check_batch(c,obj,orders),('Conic equation','private conic discriminant',i)))
    obj=deepcopy(source);i=row_id(obj,'conic packed field norm')
    power=source['norm_tree'][1]['power']
    for term in obj['residuals'][i]:
        term[1]=sorted(0 if x==power else x for x in term[1])
    passed.append(reject(name+' wrong normalization power',lambda:audit.check_batch(c,obj,orders),('Conic equation','conic packed field norm',i)))
    obj=deepcopy(source);i=row_id(obj,'conic packed field norm');remove_row(obj,i)
    passed.append(reject(name+' missing field constraint',lambda:audit.check_batch(c,obj,orders),('Conic row multiplicity','conic packed field norm')))
    for key in ('field_input_order','sorted_field_indices','field_bindings','contact_powers'):
        obj=deepcopy(source);obj[key]=list(reversed(obj[key]))
        passed.append(reject(name+' changed '+key,lambda:audit.check_batch(c,obj,orders),('Conic metadata',key)))
    obj=deepcopy(source);obj['norm_tree'][0]['value']=0
    passed.append(reject(name+' missing literal one',lambda:audit.check_batch(c,obj,orders),('Conic metadata','norm_tree')))
    obj=deepcopy(source);obj['conic_private']['theta']=1
    passed.append(reject(name+' conic boundary capture',lambda:audit.check_batch(c,obj,orders),('Conic metadata','conic_private')))
    obj=deepcopy(source);obj['calls'][0]['args']=[0]
    passed.append(reject(name+' wrong pole argument',lambda:audit.check_batch(c,obj,orders),'Conic parity call'))
    obj=deepcopy(source);obj['calls'].append(deepcopy(obj['calls'][0]))
    passed.append(reject(name+' extra pole call',lambda:audit.check_batch(c,obj,orders),'Conic parity call'))
    obj=deepcopy(source);fresh=obj['free']+obj['locals'];obj['locals']+=1
    obj['construction_log'].append(['variable',fresh,'old error leaf'])
    passed.append(reject(name+' extra old leaf',lambda:audit.check_batch(c,obj,orders),'Unaccounted conic coordinates'))
    obj=deepcopy(source);i=len(obj['residuals']);obj['residuals'].append([[1,[source['conic_private']['theta']]]])
    obj['construction_log'].append(['equation',i,'outside conic constraint'])
    passed.append(reject(name+' extra constraint',lambda:audit.check_batch(c,obj,orders),'Unconsumed conic rows'))
    return passed


def main():
    if not __debug__:
        raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('core','source','baseline','report'):
        p.add_argument('--'+flag,type=Path,required=True)
    p.add_argument('--anchor-checker',type=Path)
    p.add_argument('--seconds',type=int,default=180)
    a=p.parse_args();assert 1<=a.seconds<=600
    c=load_code(a.core,'conic_test_core',CORE_SHA);c.DEADLINE=time.monotonic()+a.seconds
    # Prove the rejection wrapper does not count an exhausted budget as PASS.
    deadline=c.DEADLINE;c.DEADLINE=0
    try:
        reject('resource regression',c.tick,'not a resource failure')
    except c.CheckerResourceError:
        resource_regressions=1
    else:
        raise RuntimeError('Resource abort became a semantic rejection')
    finally:
        c.DEADLINE=deadline
    old={}
    for name,pin in BASELINE.items():
        path=a.baseline/'modules'/(name+'.json')
        assert c.file_sha256(path)==pin,('Baseline pin',name)
        old[name]=c.load(path)
    assert {p.stem for p in (a.source/'modules').glob('*.json')}==audit.MODULES
    modules={name:c.load(a.source/'modules'/(name+'.json')) for name in audit.MODULES}
    anchor=None
    if a.anchor_checker:
        anchor=load_code(a.anchor_checker,'conic_anchor_checker',ANCHOR_SHA).check_anchor
    positive=audit.check_modules(c,modules,old,anchor_check=anchor);passed=[]
    for name,spec in audit.MODES.items():
        source=modules[name];orders=audit.field_orders(spec)
        passed.extend(batch_cases(c,modules[spec['batch']],orders))
        obj=deepcopy(source);obj['calls'][0]['args'][0]=0
        passed.append(reject(name+' wrong contact argument',lambda:audit.check_comparison(c,obj),('Ordered argument',0)))
        obj=deepcopy(source);obj['calls'][0]['args'][1]=source['free']-3
        obj['conic_field_inputs'][0][0]=source['free']-3
        passed.append(reject(name+' old theta passed to conic',lambda:audit.check_comparison(c,obj),'Old root input in conic call'))
        obj=deepcopy(source);obj['calls'][0]['args'][1:5]=obj['calls'][0]['args'][3:5]+obj['calls'][0]['args'][1:3]
        obj['conic_field_inputs'][0:2]=list(reversed(obj['conic_field_inputs'][0:2]))
        passed.append(reject(name+' reordered field inputs',lambda:audit.check_comparison(c,obj),('Ordered argument',1)))
        for tag in ('H.p2=x-Df.0','H.xf=1.0','H pH=GH.0'):
            obj=deepcopy(source);i=flip(obj,tag)
            passed.append(reject(name+' changed '+tag,lambda:audit.check_comparison(c,obj),('Core equation',tag,i)))
        obj=deepcopy(source);obj['ignored_shared_root_inputs']=[source['free']-2]
        passed.append(reject(name+' wrong ignored roots',lambda:audit.check_comparison(c,obj),'Ignored root inputs'))
    root=modules['Z_definition']
    obj=deepcopy(root);calls=[call for call in obj['calls'] if call['module'] in audit.MODES]
    calls[1]['args'][-1]=calls[0]['args'][-1]
    passed.append(reject('shared raw contact across occurrences',lambda:audit.check_root(c,obj,old['Z_definition']),('Root field','calls')))
    obj=deepcopy(root);i=flip(obj,'jacobi target reciprocal.0')
    passed.append(reject('changed root target reciprocal',lambda:audit.check_root(c,obj,old['Z_definition']),('Root equation',i)))
    if anchor:
        obj=deepcopy(modules['q_anchor']);obj['residuals'][0][0][0]*=-1
        try:
            anchor(obj)
        except ValueError as error:
            assert str(error)=='Anchor differs from the independent four-witness specification'
            passed.append('changed independent anchor')
        else:
            raise AssertionError('Changed anchor accepted')
    assert len(passed)==len(set(passed))==83+(anchor is not None)
    c.tick()
    report=dict(status='PASS: MODULE SEMANTIC MUTATIONS',negative_count=len(passed),negative_cases=passed,
                resource_regressions=resource_regressions,positive=positive,core_sha256=CORE_SHA,
                auditor_sha256=c.file_sha256(Path(audit.__file__)),test_sha256=c.file_sha256(Path(__file__)),
                anchor_checker_sha256=ANCHOR_SHA if anchor else None,
                scope='Module semantics; outer contract, flat stream, map, and source pins remain required')
    a.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=report['status'],negative_count=len(passed))))


if __name__=='__main__':
    main()
