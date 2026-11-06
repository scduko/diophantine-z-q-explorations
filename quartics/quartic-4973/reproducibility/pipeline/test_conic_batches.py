"""Repeat the frozen conic batch negatives against the joint-chart source."""
import argparse,hashlib,importlib.util,json,time
from copy import deepcopy
from pathlib import Path
import frozen_conic_tests as tests
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('core','source','report','anchor-checker'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    assert sha(HERE/'frozen_conic_tests.py')=='e022d97f11399d12fdbf0c2e70b90f4a29d386c2b0f007faea5f50bbed5ec0c8'
    assert sha(HERE/'audit_conic_source.py')=='0358e595147d8e840093b5f1a73e01c710f7c8bc0a7235f2d94611792c0b2baa'
    c=tests.load_code(a.core,'joint_conic_test_core',tests.CORE_SHA);c.DEADLINE=time.monotonic()+a.seconds
    deadline=c.DEADLINE;c.DEADLINE=0
    try:tests.reject('resource regression',c.tick,'not a resource failure')
    except c.CheckerResourceError:resource_regressions=1
    else:raise RuntimeError('Resource abort became a semantic rejection')
    finally:c.DEADLINE=deadline
    passed=[];positive={}
    for name,orders in [('q_conic15',[1]*6+[12,40,40,40]+[40,12,40,40,40]),
                        ('q_conic6',[1]*3+[12]*3),('q_conic12',[1]*5+[40]*7)]:
        module=c.load(a.source/'modules'/(name+'.json'))
        positive[name]=tests.audit.check_batch(c,module,orders)
        passed.extend(tests.batch_cases(c,module,orders))
    anchor=tests.load_code(a.anchor_checker,'joint_anchor_test',tests.ANCHOR_SHA).check_anchor
    module=c.load(a.source/'modules/q_anchor.json');anchor(module)
    changed=deepcopy(module);changed['residuals'][0][0][0]*=-1
    try:anchor(changed)
    except ValueError as error:
        assert str(error)=='Anchor differs from the independent four-witness specification'
        passed.append('changed independent anchor')
    else:raise AssertionError('Changed anchor accepted')
    assert len(passed)==len(set(passed))==61;c.tick()
    report=dict(status='PASS',negative_count=61,negative_cases=passed,positive=positive,
                resource_regressions=resource_regressions,core_sha256=tests.CORE_SHA,
                frozen_test_sha256=sha(HERE/'frozen_conic_tests.py'),test_sha256=sha(Path(__file__)),
                scope='Conic batch and anchor semantics; joint module and full outer audits run separately')
    a.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',negative_count=61,resource_regressions=1)))
if __name__=='__main__':main()
