"""Remote root/comparator positives and 59 semantic negative tests.

Run only after the outer source auditor verifies contract, flattening and map.
No malformed flat stream can mask a module-semantic failure in these tests.
"""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import audit_joint_conic as audit

CORE_SHA='0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8'
BASELINE={
    'Z_definition':'26b6b8674056bb3e7b4ba8ca75bd5b2b47cba7a58c1d84db78ba108a2f264117',
    'q_anchor':'e5b74df60328d739e94224f199efb16dd817c994658c95d5dd781704bcf94fb1',
    'q_batch41':'a45569adc62e09ce254b01cb38a3b31eb891842a73f515f21732eeeb24799985',
    'q_compare4':'ef3aba59c082b9dc312993cc5ea8d0298cc1c81b21e58d4762186bb9a53d4eb2',
    'q_height_batch':'22e3074cafdc80a71d39baf69d2012a8b039533d665f85f76da7f889dfe25761',
    'q_primeparity':'df89176d00ab6cc61e86416c5d1209554fcf87f45f30a866177c76683c2a306a',
}


def reject(name,action,reason):
    try:action()
    except AssertionError as error:
        assert error.args==(reason,),(name,'Wrong assertion',error.args)
        return name
    raise AssertionError((name,'Mutation accepted'))


def mutate_equation(obj,tag,count):
    rows=[i for kind,i,label in obj['construction_log'] if kind=='equation' and label==tag]
    assert len(rows)==count,(tag,rows)
    i=rows[0];assert len(obj['residuals'][i])>=2
    obj['residuals'][i][0][0]*=-1
    return i


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('core','source','baseline','report'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    assert hashlib.sha256(args.core.read_bytes()).hexdigest()==CORE_SHA
    spec=importlib.util.spec_from_file_location('mode_test_core',args.core)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    c.DEADLINE=time.monotonic()+600
    old={}
    for name,pin in BASELINE.items():
        path=args.baseline/'modules'/(name+'.json')
        assert c.file_sha256(path)==pin,('Baseline',name)
        old[name]=c.load(path)
    assert {p.stem for p in (args.source/'modules').glob('*.json')}==audit.MODULES
    modules={name:c.load(args.source/'modules'/(name+'.json')) for name in audit.MODULES}
    # The outer source audit must already have checked the pinned independent
    # conic batches and anchor. These mutation tests isolate the changed root
    # and comparison semantics without replacing those callback checks.
    positive=dict(root=audit.check_root(c,modules['Z_definition'],old['Z_definition']),
                  comparisons={name:audit.check_comparison(c,modules[name]) for name in audit.MODES})
    passed=[]
    root=modules['Z_definition']
    for tag in ('jacobi target reciprocal.0','jacobi target ordinate ratio.0',
                'shared joint coefficient r.0','shared joint coefficient s.0',
                'shared joint coefficient t.0','shared joint coefficient u.0'):
        obj=deepcopy(root);i=mutate_equation(obj,tag,5)
        passed.append(reject(tag,lambda:audit.check_root(c,obj,old['Z_definition']),('Root equation',i)))
    for name,spec in audit.MODES.items():
        obj=deepcopy(root);call=next(call for call in obj['calls'] if call['module']==name);at=spec['n']
        call['args'][at:at+4]=call['args'][at+2:at+4]+call['args'][at:at+2]
        passed.append(reject(name+' root target swap',lambda:audit.check_root(c,obj,old['Z_definition']),('Root field','calls')))
        obj=deepcopy(root);call=next(call for call in obj['calls'] if call['module']==name);at=5*spec['n']+11
        call['args'][at:at+4]=call['args'][at+2:at+4]+call['args'][at:at+2]
        passed.append(reject(name+' root extra-target swap',lambda:audit.check_root(c,obj,old['Z_definition']),('Root field','calls')))
    for key in ('jacobi_targets','jacobi_mode_counts','beta_only_positions',
                'joint_chart_targets','joint_chart_extra_target_coordinates'):
        obj=deepcopy(root)
        if key=='jacobi_targets':obj[key][0]['f'][0]=obj[key][0]['p'][0]
        elif key=='jacobi_mode_counts':obj[key]['q_compare4']+=1
        elif key=='beta_only_positions':obj[key]=obj[key][1:]
        elif key=='joint_chart_targets':obj[key][0]['r'][0]=obj[key][0]['s'][0]
        else:obj[key]+=2
        passed.append(reject('changed '+key,lambda:audit.check_root(c,obj,old['Z_definition']),('Root field',key)))
    for name,spec in audit.MODES.items():
        n=spec['n'];source=modules[name]
        for tag in ('joint chart K=(A-r)p.0','joint chart first relation.0','joint chart second relation.0'):
            obj=deepcopy(source);i=mutate_equation(obj,tag,n+1)
            passed.append(reject(name+' '+tag,lambda:audit.check_comparison(c,obj),('Core equation',tag,i)))
        for tag,count in (('H pH=GH.0',1),('A H=G.0',n)):
            obj=deepcopy(source);i=mutate_equation(obj,tag,count)
            passed.append(reject(name+' '+tag,lambda:audit.check_comparison(c,obj),('Core equation',tag,i)))
        for index,label in ((2*n+3,'common formal proxy'),(2*n+5,'primary ratio'),(4*n+5,'alternate ratio')):
            obj=deepcopy(source);obj['calls'][0]['args'][index]=obj['calls'][0]['args'][2]
            # Keep metadata coherent so this reaches the semantic ordered
            # expression assertion, rather than only the metadata guard.
            changed_args=obj['calls'][0]['args']
            obj['conic_field_inputs']=[changed_args[i:i+2] for i in range(1,len(changed_args),2)]
            passed.append(reject(name+' '+label,lambda:audit.check_comparison(c,obj),('Ordered argument',index)))
        obj=deepcopy(source);obj['calls'].append(deepcopy(obj['calls'][0]))
        passed.append(reject(name+' extra call',lambda:audit.check_comparison(c,obj),'Comparison call count'))
        for key,value,reason in (('primary_square_transfer',True,'Square-transfer metadata'),
                                ('difference_formal_tests',True,'Difference-test metadata'),
                                ('joint_primary_difference_chart',False,'Joint-chart metadata')):
            obj=deepcopy(source);obj[key]=value
            passed.append(reject(name+' '+key,lambda:audit.check_comparison(c,obj),reason))
        obj=deepcopy(source);obj['ignored_shared_root_inputs']=[obj['free']-3,obj['free']-2]
        passed.append(reject(name+' enlarged-free root slots',lambda:audit.check_comparison(c,obj),'Ignored root inputs'))
        obj=deepcopy(source);obj['conic_legacy_input_count']=obj['free']
        passed.append(reject(name+' enlarged legacy count',lambda:audit.check_comparison(c,obj),'Conic legacy input count'))
    assert len(passed)==59 and len(set(passed))==59
    c.tick()
    report=dict(status='PASS',negative_count=59,negative_cases=passed,module_positive=positive,
                core_sha256=CORE_SHA,auditor_sha256=c.file_sha256(Path(audit.__file__)),
                test_sha256=c.file_sha256(Path(__file__)),
                scope='Module semantics only; outer source audit required for contract, flat stream and map')
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',negative_count=59)))


if __name__=='__main__':main()
