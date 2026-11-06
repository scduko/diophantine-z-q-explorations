"""Bounded semantic mutations of a generated selective-beta source."""
import argparse,copy,json,time
from pathlib import Path
import check_source as audit

def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','baseline','report'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--seconds',type=int,default=180);a=p.parse_args();assert 1<=a.seconds<=600
    c=audit.core();c.DEADLINE=time.monotonic()+a.seconds
    valid,visits=audit.check(c,a.source,a.baseline)
    obj=c.load(a.source/'modules/q_compare_beta.json');batch=c.load(a.source/'modules/q_batch17.json')
    root=c.load(a.source/'modules/Z_definition.json');old=c.load(a.baseline/'modules/Z_definition.json')
    rejected=[]
    def reject(name,fn):
        try:fn()
        except c.CheckerResourceError:raise
        except (AssertionError,KeyError,ValueError,IndexError,TypeError):rejected.append(name);return
        raise AssertionError('Accepted malformed source: '+name)
    def mutate(name,change):
        bad=copy.deepcopy(obj);change(bad);reject(name,lambda:audit.check_beta(c,bad))
    def change_row(m,label):
        i=next(op[1] for op in m['construction_log'] if op[0]=='equation' and op[2]==label)
        m['residuals'][i][0][0]*=-1
    for label in ('arithmetic','H.xf=1.0','X0.xf=1.1','H pH=GH.0','A=C p.0','A H=G.1',
                  'difference line at first point.0','difference line at negated second point.1',
                  'difference reciprocal abscissa.0','difference formal parameter.1','distinct abscissae guard'):
        mutate('changed '+label,lambda m,label=label:change_row(m,label))
    mutate('wrong denominator precision',lambda m:m.update(precision=40))
    mutate('wrong field order',lambda m:m['field_inequality_orders'].__setitem__(5,40))
    mutate('wrong G profile',lambda m:m['high_log_profile'].update(precision=40))
    mutate('missing ordered test',lambda m:m['calls'][0]['args'].pop())
    mutate('wrong contact input',lambda m:m['calls'][0]['args'].__setitem__(0,14))
    mutate('wrong batch module',lambda m:m['calls'][0].update(module='q_batch41'))
    mutate('wrong beta proxy',lambda m:m['calls'][0]['args'].__setitem__(12,m['calls'][0]['args'][14]))
    for name,change in [
        ('wrong selected contact',lambda m:m['calls'][7].update(module='q_compare4')),
        ('wrong selected free argument',lambda m:m['calls'][7]['args'].__setitem__(0,0)),
        ('wrong retained full call',lambda m:m['calls'][2]['args'].__setitem__(0,0)),
        ('changed root equation',lambda m:m['residuals'][0][0].__setitem__(0,123)),
        ('changed root selection metadata',lambda m:m['beta_only_positions'].pop())]:
        bad=copy.deepcopy(root);change(bad);reject(name,lambda bad=bad:audit.check_root(bad,old))
    for name,change in [('wrong batch order',lambda m:m['orders'].__setitem__(11,40)),
                        ('wrong constant leaf',lambda m:change_row(m,'fused constant leaf norm')),
                        ('wrong batch power',lambda m:change_row(m,'shared contact power')),
                        ('wrong parity input',lambda m:m['calls'][0]['args'].__setitem__(0,0))]:
        bad=copy.deepcopy(batch);change(bad);bad['name']='q_batch41';reject(name,lambda bad=bad:c.check_batch(bad,audit.ORDERS))
    saved=c.DEADLINE;c.DEADLINE=time.monotonic()-1
    try:
        try:reject('resource abort must not pass',c.tick)
        except c.CheckerResourceError:pass
        else:raise AssertionError('Resource abort counted as semantic rejection')
    finally:c.DEADLINE=saved
    result={'status':'PASS','malformed_sources_rejected':len(rejected),'cases':rejected,
            'resource_abort_propagation':'PASS','valid_source_status':valid['status'],
            'scope':'New module and exact root retargeting; inherited modules are byte-pinned and full flattening independently checked'}
    a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()
