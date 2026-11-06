"""Small target-two delta fixtures, with exact rejection checkpoints."""
import argparse
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import audit_target2 as audit

PRODUCER_SHA='fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799'


def load(name,path,pin):
    assert sha256(path.read_bytes()).hexdigest()==pin,'Pinned test dependency'
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run(base,parents,producer=None):
    expected={n:audit.expected_root(base,p) if n=='Z_definition' else audit.expected_comparison(base,p)
              for n,p in parents.items()}
    positive=audit.check_modules(base,parents,expected)
    if producer is not None:
        output,_=producer.postprocess_modules(parents)
        audit.check_modules(base,parents,output)
    removed=base.REMOVED_ROWS|audit.SECOND_ROWS
    rowmap={old:new for new,old in enumerate(i for i in range(345) if i not in removed)}
    passed=[]
    def reject(label,name,mutate):
        obj=deepcopy(expected[name]);mutate(obj)
        wanted='Complete target-two root mismatch' if name=='Z_definition' else 'Complete target-two comparison mismatch'
        try:
            (audit.check_root if name=='Z_definition' else audit.check_comparison)(base,parents[name],obj)
        except AssertionError as error:
            assert str(error)==wanted,(label,str(error))
        else:raise AssertionError('Accepted mutation '+label)
        passed.append(label)
    def coefficient(i):
        def mutate(obj):obj['residuals'][i][0][0]+=1
        return mutate
    root='Z_definition'
    for old in sorted(audit.replacements(base)[0]):
        reject('replacement '+str(old),root,coefficient(rowmap[old]))
    for old in range(329,345):
        reject('general curve '+str(old),root,coefficient(rowmap[old]))
    for old in (100,101,102,103,120,121,122,123,140,141,142,143,160,161,162,163,72,73,194,195):
        reject('retained square/inverse '+str(old),root,coefficient(rowmap[old]))
    for old in (0,25,26,27,28,57,74,75,328):
        reject('unchanged scalar/chart '+str(old),root,coefficient(rowmap[old]))
    reject('restore second-double row',root,lambda o:o['residuals'].append([[1,[0]]]))
    reject('omit last curve row',root,lambda o:o['residuals'].pop())
    reject('undeclared extra coordinate',root,lambda o:o['construction_log'].append(['variable',219,'extra']))
    reject('extra call',root,lambda o:o['calls'].append(deepcopy(o['calls'][0])))
    reject('extra metadata',root,lambda o:o.update(unchecked=1))
    reject('wrong locals',root,lambda o:o.update(locals=219))
    reject('boolean free',root,lambda o:o.update(free=True))
    reject('wrong multiplier',root,lambda o:o.update(comparison_target_multiplier=4))
    reject('old fixed target',root,lambda o:o['comparison_base'].update(fixed_target='4R=2Pstar'))
    reject('wrong target type',root,lambda o:o['root_targets'][1].update(kind='quadruple'))
    reject('old target base type',root,lambda o:o['root_targets'][0].update(kind='fixed_4R'))
    reject('wrong root proof pin',root,lambda o:o['general_root_rewrite'].update(target_two_proof_sha256='0'*64))
    reject('wrong review pin',root,lambda o:o['general_root_rewrite'].update(target_two_review_sha256='0'*64))
    reject('wrong removed rows',root,lambda o:o['general_root_rewrite']['original_removed_rows'].pop())
    reject('wrong historical receipt',root,lambda o:o['lucas_proxy_removal'].update(original_row=58))
    reject('wrong target record',root,lambda o:o['target_two_bindings'].update(first_doubling_only=False))
    reject('wrong linear record',root,lambda o:o['fixed_target_bindings'].update(linear_rows=[]))
    reject('wrong constant record',root,lambda o:o['fixed_target_bindings'].update(coordinates=[]))
    reject('wrong root square',root,lambda o:o['general_root_charts']['A'].update(square=o['general_root_charts']['S']['square']))
    reject('wrong joint target',root,lambda o:o['joint_chart_targets'][0].update(u=o['joint_chart_targets'][1]['u']))
    for name in parents:
        if name==root:continue
        def mutate_call(obj,name=name):
            next(c for c in obj['calls'] if c['module']==name)['args'][0]+=1
        reject('root call '+name,root,mutate_call)
        reject('mode target '+name,name,lambda o:o.update(comparison_fixed_target='4R=2Pstar'))
        reject('mode multiplier '+name,name,lambda o:o.update(comparison_target_multiplier=4))
        reject('mode layout '+name,name,lambda o:o.update(input_layout=o['input_layout'].replace('Fq(Pstar)','Fq(P4)')))
        reject('mode extra row '+name,name,lambda o:o['residuals'].append([[1,[0]]]))
        if name!='q_compare_lucas':
            reject('beta factor '+name,name,coefficient(expected[name]['beta_field_row']))
    try:audit.check_root(base,parents[root],{'nested':'x'*10001})
    except base.AuditResourceError:pass
    else:raise AssertionError('Resource failure not propagated')
    return dict(status='PASS: SMALL TARGET-TWO AUDIT FIXTURES',semantic_rejections=len(passed),
                resource_abort_cases=1,root=positive['root'],producer_compared=producer is not None,
                full_source_generated=False)


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions required')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents',type=Path,required=True)
    parser.add_argument('--base-audit',type=Path,required=True)
    parser.add_argument('--producer',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    base=load('target4_audit',args.base_audit,audit.BASE_AUDIT_SHA)
    producer=load('target2_producer',args.producer,PRODUCER_SHA) if args.producer else None
    report=run(base,base.load_parent(args.parents),producer)
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
