"""Independent full-source delta for the normalized linear-unit pole.

The old pole is restored only as a specification view for inherited source
rows. This does not assert projection equivalence of the pole predicates.
The new arithmetic proof establishes the consumed negative-odd conclusion.
"""
if not __debug__:raise RuntimeError('Assertions required')
from copy import deepcopy
import audit_conic_pole as previous
import check_conic_pole as previous_literal
import spec_linear

BATCHES={'q_conic13','q_conic6','q_conic10'}
NEW='q_linearnormalpole';OLD='q_conicpole'
MODEL='linear unit 3-2*theta'
SEMANTICS='Private theta^2-r*s_c^2=2; original packed fields and upper tree; linear-unit negative-odd exclusion at (r,theta,root)'
OLD_SEMANTICS='Private theta^2-r*s_c^2=2; original packed fields and upper tree; conic-conditioned pole at (r,theta,root)'

def previous_batch(proposed):
    assert proposed['name'] in BATCHES,'Wrong linear-pole batch name'
    args=[0,proposed['conic_private']['theta'],proposed['norm_root']]
    assert previous_literal.equal(proposed['calls'],[{'module':NEW,'args':args}]),'Wrong linear-pole caller inputs'
    assert previous_literal.equal(proposed.get('pole_inputs'),args),'Wrong linear-pole input metadata'
    assert proposed.get('parity_module')==NEW,'Wrong linear-pole module metadata'
    assert proposed.get('pole_model')==MODEL,'Wrong linear-pole model'
    assert proposed.get('semantics')==SEMANTICS,'Wrong linear-pole semantics'
    d=deepcopy(proposed)
    d['calls']=[{'module':OLD,'args':args}]
    d.update(parity_module=OLD,pole_model='private conic Cayley parameter 2*s_c',semantics=OLD_SEMANTICS)
    return d

def restore_batch(proposed):
    return previous.restore_batch(previous_batch(proposed))

def check_batch(c,proposed,orders,old_checker):
    return previous.check_batch(c,previous_batch(proposed),orders,old_checker)

def check_modules(c,modules,old,joint,conic,anchor):
    assert set(modules)==joint.MODULES|{NEW},'Linear-pole module set'
    literal=spec_linear.check(modules[NEW],normalized=True)
    c.Module(modules[NEW],26,arithmetic_labels=())
    restored={name:previous_batch(obj) if name in BATCHES else deepcopy(obj)
              for name,obj in modules.items() if name!=NEW}
    restored[OLD]=previous_literal.expected_pole()
    inherited=previous.check_modules(c,restored,old,joint,conic,anchor)
    callers={name for name,obj in modules.items() for call in obj['calls'] if call['module']==NEW}
    assert callers==BATCHES,'Unexpected linear-pole caller'
    assert not any(call['module']==OLD for obj in modules.values() for call in obj['calls']),'Old pole caller remains'
    inherited.pop('conic_pole')
    inherited['linear_pole']=literal
    inherited['pole_specification_view_only']=True
    return inherited
