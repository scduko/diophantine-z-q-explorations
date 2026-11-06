"""Targeted malformed local-Lucas modules for an independent audit harness.

Yield one case at a time. The caller must first accept the original complete
module set, reject every named case, and separately propagate resource and
deadline exceptions. This module does not import any producer or auditor.
"""
from copy import deepcopy


EXPECTED_CASES = {
    'full-V-coefficient', 'full-D-coefficient', 'full-E-constant',
    'lucas-V-coefficient', 'lucas-D-coefficient', 'lucas-E-constant',
    'full-E-test-replaced-by-V', 'lucas-E-test-replaced-by-V',
    'full-E-test-swapped-with-alternate', 'lucas-E-test-swapped-with-alternate',
    'full-evaluation-ratio-order', 'lucas-evaluation-ratio-order',
    'full-exact-zero-E', 'lucas-exact-zero-E',
    'full-E-field-order', 'lucas-E-field-order',
    'full-conic-odd-power', 'lucas-conic-odd-power',
    'full-extra-target-boundary', 'lucas-extra-target-boundary',
    'beta-primary-call-input', 'beta-false-Lucas-metadata',
    'root-retained-proxy-role', 'root-proxy-index', 'root-removal-receipt',
    'root-anchor-argument', 'root-scalar-argument', 'root-joint-target-index',
    'root-restored-Pell-metadata', 'root-comparison-target-argument',
}


def mutation_cases(modules):
    seen = set()
    def clone(name):
        if name in seen or name not in EXPECTED_CASES:
            raise RuntimeError('Invalid mutation case inventory')
        seen.add(name)
        return deepcopy(modules)
    def equation(obj,label):
        ids = [i for kind,i,text in obj['construction_log'] if kind=='equation' and text==label]
        if len(ids)!=1:
            raise RuntimeError('Valid fixture lacks a unique equation: '+label)
        return ids[0]
    def sync_inputs(obj):
        args=obj['calls'][0]['args']
        obj['conic_field_inputs']=[args[i:i+2] for i in range(1,len(args),2)]

    for short,name,batch,e_field in [('full','q_compare4','q_conic13',7),
                                    ('lucas','q_compare_lucas','q_conic10',5)]:
        for letter,label in [('V','local Lucas V=(Cs-2)Cz.0'),
                             ('D','local Lucas D=CsCt-V.0')]:
            case=short+'-'+letter+'-coefficient';bad=clone(case)
            row=bad[name]['residuals'][equation(bad[name],label)]
            row[0][0] += 1 if row[0][0]>0 else -1
            yield case,bad
        case=short+'-E-constant';bad=clone(case)
        row=bad[name]['residuals'][equation(bad[name],'local Lucas E=Ct2-VD-1.0')]
        constant=[term for term in row if term[1]==[]]
        if len(constant)!=1:raise RuntimeError('E fixture has no unique constant')
        constant[0][0]*=-1
        yield case,bad

        case=short+'-E-test-replaced-by-V';bad=clone(case)
        bad[name]['calls'][0]['args'][1+2*e_field:3+2*e_field]=bad[name]['local_lucas_evaluation']['V'][:]
        sync_inputs(bad[name])
        yield case,bad
        case=short+'-E-test-swapped-with-alternate';bad=clone(case)
        args=bad[name]['calls'][0]['args'];at=1+2*e_field
        args[at:at+4]=args[at+2:at+4]+args[at:at+2]
        sync_inputs(bad[name])
        yield case,bad
        case=short+'-evaluation-ratio-order';bad=clone(case)
        pair=bad[name]['local_lucas_evaluation']['ratios']
        pair[0],pair[1]=pair[1],pair[0]
        yield case,bad
        case=short+'-exact-zero-E';bad=clone(case)
        at=equation(bad[name],'local Lucas E=Ct2-VD-1.0')
        bad[name]['residuals'][at]=[[1,[bad[name]['local_lucas_evaluation']['E'][0]]]]
        yield case,bad
        case=short+'-E-field-order';bad=clone(case)
        bad[name]['field_inequality_orders'][e_field]=12
        yield case,bad
        case=short+'-conic-odd-power';bad=clone(case)
        binding=bad[batch]['field_bindings'][e_field]
        candidates=[i for kind,i,label in bad[batch]['construction_log']
                    if kind=='equation' and label=='conic packed field norm'
                    and any(binding['norm'] in mon and binding['power'] in mon
                            for coefficient,mon in bad[batch]['residuals'][i])]
        if len(candidates)!=1:raise RuntimeError('Cannot find the packed E norm')
        row=bad[batch]['residuals'][candidates[0]]
        for coefficient,mon in row:
            if binding['norm'] in mon and binding['power'] in mon:
                mon[mon.index(binding['power'])]=0;mon.sort()
        yield case,bad
        case=short+'-extra-target-boundary';bad=clone(case)
        bad[name]['extra_target_start']+=3
        yield case,bad

    case='beta-primary-call-input';bad=clone(case)
    bad['q_compare_beta']['calls'][0]['args'][7]=bad['q_compare_beta']['calls'][0]['args'][1]
    sync_inputs(bad['q_compare_beta'])
    yield case,bad
    case='beta-false-Lucas-metadata';bad=clone(case)
    bad['q_compare_beta']['local_lucas_residual']=True
    yield case,bad
    case='root-retained-proxy-role';bad=clone(case)
    bad['Z_definition']['retained_proxy_roles'].append('s')
    yield case,bad
    case='root-proxy-index';bad=clone(case)
    bad['Z_definition']['proxy_indices'][0]=0
    yield case,bad
    case='root-removal-receipt';bad=clone(case)
    bad['Z_definition']['lucas_proxy_removal']['original_variables'][0]+=1
    yield case,bad
    for case,module in [('root-anchor-argument','q_anchor'),('root-scalar-argument','q_height_batch')]:
        bad=clone(case);calls=[call for call in bad['Z_definition']['calls'] if call['module']==module]
        if len(calls)!=1:raise RuntimeError('Valid root has unexpected auxiliary call count')
        calls[0]['args'][0]=0
        yield case,bad
    case='root-joint-target-index';bad=clone(case)
    bad['Z_definition']['joint_chart_targets'][0]['r'][0]+=1
    yield case,bad
    case='root-restored-Pell-metadata';bad=clone(case)
    bad['Z_definition']['pell_equation']='t^2-s*(s-2)*t*z+(s-2)^2*z^2-1=0'
    yield case,bad
    case='root-comparison-target-argument';bad=clone(case)
    calls=[call for call in bad['Z_definition']['calls'] if call['module']=='q_compare4']
    calls[0]['args'][1],calls[0]['args'][2]=calls[0]['args'][2],calls[0]['args'][1]
    yield case,bad
    if seen!=EXPECTED_CASES:
        raise RuntimeError('Incomplete mutation coverage')


def run_cases(modules, check, semantic_errors=(AssertionError,)):
    """Run only with an independently supplied whole-module checker.

    RuntimeError, MemoryError, TimeoutError and other operational failures
    are deliberately not semantic rejections.
    """
    if semantic_errors!=(AssertionError,):
        raise ValueError('Only AssertionError is a semantic rejection here')
    check(modules)
    rejected=[]
    for name,bad in mutation_cases(modules):
        try:
            check(bad)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Mutation was accepted: '+name)
    if set(rejected)!=EXPECTED_CASES or len(rejected)!=len(EXPECTED_CASES):
        raise AssertionError('Incomplete negative coverage')
    return dict(valid_source_accepted=True, rejected=sorted(rejected),
                count=len(rejected), scope='targeted local-Lucas whole-module mutations')
