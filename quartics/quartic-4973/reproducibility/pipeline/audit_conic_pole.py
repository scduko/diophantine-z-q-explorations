"""Independent whole-batch specification through the pinned old conic audit.

No producer is imported. Restoration appends only the two removed tail gates.
The old checker accounts for every retained row, variable, call and field input.
The literal delta checker then verifies the entire proposed module unchanged
outside that deletion and the new call. The outer checker pins all three files.
"""
if not __debug__:raise RuntimeError('Assertions required')
from copy import deepcopy
import check_conic_pole as pole

OLD_SEMANTICS=('Private theta^2-r*s^2=2; packed eval_theta(F_i^2)/r^(2e_i); '
               'upper N_r tree on literal1 and packed nodes; Psi(r*root^2)')


def restore_batch(proposed):
    d=deepcopy(proposed)
    assert d['name'] in {'q_conic13','q_conic6','q_conic10'},'Wrong pole batch name'
    assert not {'norm_root_square','parity_argument'}&set(d),'Old tail metadata remains'
    assert {'pole_model','pole_inputs'}<=set(d),'Missing pole metadata'
    n=d['free']+d['locals'];nr=len(d['residuals']);W=d['norm_root']
    d['residuals'] += [[[-1,[W,W]],[1,[n]]],[[-1,[0,n]],[1,[n+1]]]]
    d['construction_log'] += [['variable',n,'batched square'],['equation',nr,'batched square'],
                              ['variable',n+1,'parity argument'],['equation',nr+1,'parity argument']]
    d['locals']+=2
    d['calls']=[{'module':'q_primeparity','args':[n+1]}]
    d.update(norm_root_square=n,parity_argument=n+1,parity_module='q_primeparity',semantics=OLD_SEMANTICS)
    del d['pole_model'];del d['pole_inputs']
    return d


def check_batch(c,proposed,orders,old_checker):
    restored=restore_batch(proposed)
    report=old_checker(c,restored,orders)
    delta=pole.check_batch(proposed,restored)
    return dict(old_batch=report,delta=delta,same_r_theta_root=True,
                free_coefficients_independent_of_private_conic=True)


def check_modules(c,modules,old,joint,conic,anchor):
    assert set(modules)==joint.MODULES|{'q_conicpole'},'Conic-pole module set'
    literal=pole.check_pole(modules['q_conicpole'])
    c.Module(modules['q_conicpole'],26,arithmetic_labels=())
    report=joint.check_modules(c,{n:m for n,m in modules.items() if n!='q_conicpole'},old,
        conic_batch_check=lambda c,m,o:check_batch(c,m,o,conic.check_batch),anchor_check=anchor.check_anchor)
    callers={n for n,m in modules.items() for call in m['calls'] if call['module']=='q_conicpole'}
    assert callers=={'q_conic13','q_conic6','q_conic10'},'Unexpected conic-pole caller'
    old_callers={n for n,m in modules.items() for call in m['calls'] if call['module']=='q_primeparity'}
    assert old_callers=={'q_height_batch'},'Unexpected legacy parity caller'
    report['conic_pole']=literal
    return report
