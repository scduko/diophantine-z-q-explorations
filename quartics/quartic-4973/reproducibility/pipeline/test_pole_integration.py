"""Three isolated batch specifications and semantic mutations, no full source."""
if not __debug__:raise RuntimeError('Assertions required')
import argparse,hashlib,importlib.util,json,time
from copy import deepcopy
from pathlib import Path
import audit_conic_pole as audit
import check_lucas_batch as old_audit
import conic_pole_kernel as kernel
import check_conic_pole as spec
HERE=Path(__file__).resolve().parent

def load(name,path,pin):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def reject(name,call):
    try:call()
    except (AssertionError,ValueError):return name
    raise AssertionError('Mutation accepted: '+name)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path);a=p.parse_args()
    b=load('tiny_pole_builder',HERE/'baseline/compiler/archive_build.py','c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912')
    e=load('tiny_joint_emitter',HERE/'conic_lucas.py','42fcb55ec95be9ee34e98c5d0b0e672062b7cce6c5f9f9d0e676edff72e5ed86')
    c=load('tiny_pole_audit_core',HERE/'core_audit.py','0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8')
    c.DEADLINE=time.monotonic()+90;b.write=lambda *args:None;b._private_conic_installed=True;kernel.install(b)
    passed=[];positive={}
    modes={'q_conic13':[1]*6+[12,40]+[40,12,40,40,40],
           'q_conic6':[1]*3+[12]*3,'q_conic10':[1]*5+[40]*5}
    for name,orders in modes.items():
        e.make_conic_batch(b,name,orders);m=b.MODULES[name]
        positive[name]=audit.check_batch(c,m,orders,old_audit.check_batch)
        for label in ('private conic square','private conic discriminant','conic evaluation','conic packed field norm','cubic norm node'):
            changed=deepcopy(m);i=next(i for k,i,t in changed['construction_log'] if k=='equation' and t==label)
            changed['residuals'][i][0][0]*=2
            passed.append(reject(name+' changed '+label,lambda:audit.check_batch(c,changed,orders,old_audit.check_batch)))
        for slot in range(3):
            changed=deepcopy(m);changed['calls'][0]['args'][slot]+=1
            passed.append(reject(name+' changed pole input '+str(slot),lambda:audit.check_batch(c,changed,orders,old_audit.check_batch)))
        for key in ('field_bindings','norm_tree'):
            changed=deepcopy(m);changed[key]=list(reversed(changed[key]))
            passed.append(reject(name+' changed '+key,lambda:audit.check_batch(c,changed,orders,old_audit.check_batch)))
        changed=deepcopy(m);changed['conic_private']['theta']=1
        passed.append(reject(name+' captured field coefficient',lambda:audit.check_batch(c,changed,orders,old_audit.check_batch)))
        changed=deepcopy(m);changed['calls'].append({'module':'q_primeparity','args':[0]})
        passed.append(reject(name+' extra call',lambda:audit.check_batch(c,changed,orders,old_audit.check_batch)))
    spec.check_pole(b.MODULES['q_conicpole'])
    c.Module(b.MODULES['q_conicpole'],26,arithmetic_labels=())
    for i in range(10):
        changed=deepcopy(b.MODULES['q_conicpole']);changed['residuals'][i][0][0]*=2
        passed.append(reject('changed literal pole row '+str(i),lambda:spec.check_pole(changed)))
    assert len(passed)==46
    result=dict(status='PASS',negative_count=len(passed),negative_cases=passed,positive=positive,
                scope='Three isolated batches and literal pole; no full source generation or replay')
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
