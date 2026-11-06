"""Actual composed-source mutations; complete selected-parent audit required."""
import argparse,hashlib,json,time
from copy import deepcopy
from pathlib import Path
import check_source as outer
import audit_root_shared as composed
import shared_square_cases as cases
import audit_first_norm
import test_first_norm_cases as first_cases

HERE=Path(__file__).resolve().parent
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser()
    for name in ('source','baseline','report'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    c=outer.core();c.DEADLINE=time.monotonic()+a.seconds
    _,old=outer.baseline(c,a.baseline)
    for name,pin in outer.POLE_HELPERS.items():assert c.file_sha256(HERE/name)==pin
    import audit_normalized_lucas as normalized
    import check_lucas_batch as conic
    import check_anchor_four as anchor
    assert c.file_sha256(Path(normalized.__file__))==outer.JACOBI_AUDIT_SHA
    assert c.file_sha256(Path(conic.__file__))==outer.CONIC_AUDIT_SHA
    assert c.file_sha256(Path(anchor.__file__))==outer.ANCHOR_AUDIT_SHA
    assert c.file_sha256(Path(cases.__file__))=='42b33b7506998584b53d7ca7a6f309a1a8846c3d464cb9e620cabc5fe1c1cc7a'
    assert {p.stem for p in (a.source/'modules').glob('*.json')}==set(outer.MODULES)
    actual={name:c.load(a.source/'modules'/(name+'.json')) for name in outer.MODULES}
    def actual_check(items):return composed.check_modules(c,items,old,normalized,conic,anchor)
    actual_positive=actual_check(actual)
    assert c.file_sha256(Path(first_cases.__file__))=='e63a0ef152d0c9442330430d881e6c9f22b00230d9dd0355f8ad1147af7d9822'
    first_rejections=[]
    for label,changed in first_cases.mutation_cases(actual):
        try:actual_check(changed)
        except AssertionError:first_rejections.append(label)
        else:raise AssertionError('First-norm mutation accepted: '+label)
    assert len(first_rejections)==87
    first_resources=[]
    deep=0
    for _ in range(50):deep=[deep]
    for label,value in [('wide list',[0]*16385),('long string','x'*8193),('large integer',1<<4096),('deep list',deep)]:
        changed=deepcopy(actual);changed['resource_fixture']=value
        try:audit_first_norm.restore_modules(changed)
        except audit_first_norm.ResourceError:first_resources.append(label)
        else:raise AssertionError('First-norm resource limit failed: '+label)
    callback_rejections=0
    for result in (False,True):
        try:audit_first_norm.check_modules(actual,lambda items,r=result:r)
        except TypeError:callback_rejections+=1
        else:raise AssertionError('Boolean parent callback accepted')
    # Explicit restored specification view, after actual-source acceptance.
    # These inherited mutations exercise the unchanged root/shared layer.
    modules=audit_first_norm.restore_modules(actual)
    def check(items):return composed.check_parent_modules(c,items,old,normalized,conic,anchor)
    positive=check(modules);report=cases.run_cases(modules,check)
    assert report['negative_count']==109
    tangent_cases=[]
    changed=[i for record in modules['Z_definition']['direct_tangent_doublings'] for i in record['tangent_rows']]
    for row in changed:
        bad=deepcopy(modules);bad['Z_definition']['residuals'][row][0][0]+=1
        try:check(bad)
        except AssertionError as error:assert str(error)=='Complete four-tangent root mismatch'
        else:raise AssertionError('Actual tangent row mutation accepted')
        tangent_cases.append('tangent row '+str(row))
    for label,mutate in (
        ('doubling model',lambda root:root.update(root_doubling_model='old inverse')),
        ('missing tangent site',lambda root:root['direct_tangent_doublings'].pop()),
        ('inverse receipt',lambda root:root['direct_tangent_rewrite'].update(raw_variable_delta=0)),
        ('target binding',lambda root:root['target_two_bindings']['rows'].__setitem__(0,0))):
        bad=deepcopy(modules);mutate(bad['Z_definition'])
        try:check(bad)
        except AssertionError as error:assert str(error)=='Complete four-tangent root mismatch'
        else:raise AssertionError('Actual tangent metadata mutation accepted')
        tangent_cases.append(label)
    assert len(tangent_cases)==12
    report['tangent_negative_cases']=tangent_cases
    deadline=c.DEADLINE;c.DEADLINE=0
    try:cases.must_reject('deadline',check,modules)
    except c.CheckerResourceError:resource=1
    else:raise AssertionError('Deadline counted as semantic rejection')
    finally:c.DEADLINE=deadline
    report.update(actual_source_positive=actual_positive,restored_specification_positive=positive,
        first_norm_negative_cases=first_rejections,first_norm_resource_aborts=first_resources,
        first_norm_boolean_callback_rejections=callback_rejections,resource_abort_regressions=resource,
        scope='Actual first-norm source checked first; inherited root/shared mutations use explicitly restored specification view')
    a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','negative_count':109,'tangent_negative_count':12,'first_norm_negative_count':87,'resource_abort_regressions':resource+len(first_resources)}))
if __name__=='__main__':main()
