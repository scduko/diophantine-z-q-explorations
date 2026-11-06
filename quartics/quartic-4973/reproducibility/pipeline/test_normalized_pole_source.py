"""Combined acceptance, then normalized mutations on an explicit tail view.

Actual pole/tail mutations run separately through test_linear_integration.py.
No restored view substitutes for accepting the actual eleven modules first.
"""
import argparse,importlib.util,json,time
from pathlib import Path
import check_source as outer
import test_normalized_lucas as tests
HERE=Path(__file__).resolve().parent
def load(c,name,pin):
    path=HERE/name;assert c.file_sha256(path)==pin,('Test dependency',name)
    spec=importlib.util.spec_from_file_location('combined_'+path.stem,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('core','source','baseline','report','anchor-checker'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    c=outer.core();assert c.file_sha256(a.core)==outer.CORE_SHA;c.DEADLINE=time.monotonic()+a.seconds
    assert c.file_sha256(Path(tests.__file__))=='b862d6d0959eb4b357d4a999228f6fb70f4ded5562e39542b8c65c593314c54c'
    pins,old=outer.baseline(c,a.baseline)
    normalized=load(c,'audit_normalized_lucas.py',outer.JACOBI_AUDIT_SHA)
    conic=load(c,'check_lucas_batch.py',outer.CONIC_AUDIT_SHA)
    anchor=load(c,'check_anchor_four.py',outer.ANCHOR_AUDIT_SHA)
    assert c.file_sha256(a.anchor_checker)==outer.ANCHOR_AUDIT_SHA
    for name,pin in outer.POLE_HELPERS.items():assert c.file_sha256(HERE/name)==pin
    pole=load(c,'audit_linear_pole.py',outer.POLE_HELPERS['audit_linear_pole.py'])
    assert {f.stem for f in (a.source/'modules').glob('*.json')}==set(outer.MODULES)
    modules={name:c.load(a.source/'modules'/(name+'.json')) for name in outer.MODULES}
    positive=pole.check_modules(c,modules,old,normalized,conic,anchor)
    deadline=c.DEADLINE;c.DEADLINE=0
    try:tests.reject('deadline regression',c.tick,'not a resource failure')
    except c.CheckerResourceError:resource_regressions=1
    else:raise RuntimeError('Resource abort became a semantic rejection')
    finally:c.DEADLINE=deadline
    passed=tests.root_cases(c,modules['Z_definition'],old['Z_definition'])
    for name,spec in normalized.MODES.items():
        passed+=tests.comparison_cases(c,modules[name])
        restored=pole.restore_batch(modules[spec['batch']])
        conic.check_batch(c,restored,normalized.field_orders(spec))
        passed+=tests.batch_cases(c,restored,normalized.field_orders(spec))
    assert len(passed)==len(set(passed))==208;c.tick()
    report=dict(status='PASS',negative_count=208,negative_cases=passed,resource_abort_regressions=resource_regressions,
                actual_composite_positive=positive,tail_view='Only two old tail coordinates/rows and old parity call restored',
                scope='Actual combined positive first; normalized208 suite on retained modules and explicit old tail view; actual new pole mutations are a separate stage')
    a.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status='PASS',negative_count=208,resource_abort_regressions=1)))
if __name__=='__main__':main()
