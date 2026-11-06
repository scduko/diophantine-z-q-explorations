"""Small pinned-root fixtures only; never generates or flattens a full source."""
import argparse
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import audit_root_rewrite as a

PRODUCER_SHA = '5a9d82fdb68db591a275c67b2c555735e1376a6a86da21221d76976abd68d479'


def run(parents, producer_path=None):
    expected = {name:(a.expected_root(obj) if name=='Z_definition' else a.expected_comparison(obj))
                for name,obj in parents.items()}
    baseline = a.check_modules(parents, expected)
    if producer_path is not None:
        path = Path(producer_path)
        assert sha256(path.read_bytes()).hexdigest() == PRODUCER_SHA, 'Producer fixture pin'
        spec = importlib.util.spec_from_file_location('root_producer_fixture', path)
        producer = importlib.util.module_from_spec(spec); spec.loader.exec_module(producer)
        emitted, receipt = producer.postprocess_modules(parents)
        a.check_modules(parents, emitted)
        assert set(receipt['changed_modules']) == set(a.PINS)
    cases=[]
    def reject(label, name, mutation):
        obj=deepcopy(expected[name]);mutation(obj)
        wanted='Complete doubled-index root mismatch' if name=='Z_definition' else 'Complete doubled-index comparator mismatch'
        try:
            (a.check_root if name=='Z_definition' else a.check_comparison)(parents[name],obj)
        except AssertionError as error:
            assert str(error)==wanted,(label,str(error))
        else:
            raise AssertionError('Mutation accepted: '+label)
        cases.append(label)
    def wrong_coefficient(row_index):
        def mutation(obj):obj['residuals'][row_index][0][0]+=1
        return mutation
    root='Z_definition'
    # Every added curve equation and fixed-target binding has an independent case.
    for old in range(329,345):
        reject('new chart row '+str(old),root,wrong_coefficient(a.ROW_MAP[old]))
    for old in (196,197,271,272):
        reject('fixed binding '+str(old),root,wrong_coefficient(a.ROW_MAP[old]))
    # All retained inverse rows and all four reused square pairs.
    for old in (72,73,194,195,102,103,122,123,142,143,162,163,100,101,120,121,140,141,160,161):
        reject('retained inverse/square '+str(old),root,wrong_coefficient(a.ROW_MAP[old]))
    for old in (0,25,26,27,28,57,74,75,328):
        reject('other retained row '+str(old),root,wrong_coefficient(a.ROW_MAP[old]))
    reject('missing chart row',root,lambda o:o['residuals'].pop())
    reject('extra row',root,lambda o:o['residuals'].append([[1,[0]]]))
    reject('extra log item',root,lambda o:o['construction_log'].append(['variable',259,'rogue']))
    reject('extra call',root,lambda o:o['calls'].append(deepcopy(o['calls'][0])))
    reject('extra metadata',root,lambda o:o.update(unchecked=True))
    reject('wrong locals',root,lambda o:o.update(locals=259))
    reject('wrong free',root,lambda o:o.update(free=True))
    reject('missing comparison base',root,lambda o:o.pop('comparison_base'))
    reject('old carrier',root,lambda o:o.update(root_carrier='2E(K)'))
    reject('wrong semantics',root,lambda o:o.update(root_index_semantics='Q=n_Q Pstar'))
    reject('wrong height multiplier',root,lambda o:o.update(height_effective_multiplier=1))
    reject('wrong historical receipt',root,lambda o:o['lucas_proxy_removal'].update(original_row=58))
    reject('wrong replacement receipt',root,lambda o:o['general_root_rewrite'].update(original_replaced_rows=[]))
    reject('wrong square source',root,lambda o:o['general_root_charts']['A'].update(square=o['general_root_charts']['S']['square']))
    reject('wrong J k',root,lambda o:o['general_root_charts']['common comparison J'].update(k=o['general_root_charts']['height J']['k']))
    reject('wrong fixed target type',root,lambda o:o['root_targets'][0].update(kind='quadruple'))
    reject('wrong fixed q map',root,lambda o:o['root_targets'][0].update(p=o['root_targets'][1]['p']))
    reject('wrong joint u map',root,lambda o:o['joint_chart_targets'][0].update(u=o['joint_chart_targets'][1]['u']))
    for mode in ('q_compare4','q_compare_beta','q_compare_lucas'):
        def wrong_call(obj,mode=mode):
            call=next(c for c in obj['calls'] if c['module']==mode);call['args'][0]+=1
        reject('root call '+mode,root,wrong_call)
        reject('old target label '+mode,mode,lambda o:o.update(comparison_fixed_target='4Pstar'))
        reject('old layout '+mode,mode,lambda o:o.update(input_layout=o['input_layout'].replace('Fq(R4)','Fq(P4)')))
        reject('extra comparison row '+mode,mode,lambda o:o['residuals'].append([[1,[0]]]))
        reject('comparison call '+mode,mode,lambda o:o['calls'][0]['args'].__setitem__(0,1))
    for mode in ('q_compare4','q_compare_beta'):
        reject('beta coefficient '+mode,mode,wrong_coefficient(expected[mode]['beta_field_row']))
        reject('beta scale '+mode,mode,lambda o:o.update(beta_comparison_scale=1))
        reject('beta receipt '+mode,mode,lambda o:o.update(beta_rewrite_parent_sha256='0'*64))
    # Parent tampering must fail at the pin rather than be inherited by expected().
    for name in a.PINS:
        changed=deepcopy(parents[name]);changed['residuals'][0][0][0]+=1
        try:
            (a.expected_root if name==root else a.expected_comparison)(changed)
        except AssertionError as error:
            assert str(error)=='Pinned parent '+name
        else:raise AssertionError('Altered parent accepted')
        cases.append('altered parent '+name)
    # A resource failure is not one of the semantic mutation rejections.
    try:a.check_root(parents[root],{'oversized':'x'*10001})
    except a.AuditResourceError:pass
    else:raise AssertionError('Resource limit not enforced')
    return dict(status='PASS: SMALL ROOT AUDIT FIXTURES',negative_cases=len(cases),
                resource_abort_cases=1,producer_compared=producer_path is not None,
                new_root=baseline['root'],full_source_generated=False)


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions required')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parents',type=Path,required=True)
    parser.add_argument('--producer',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(a.load_parent(args.parents),args.producer),sort_keys=True))
