"""Small exact tests for the pinned tangent postprocessor; no whole source build."""
if not __debug__:
    raise RuntimeError('Assertions required')
import argparse
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

import compress_doublings as producer

HELPER='fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799'
ZERO=(Q(0),Q(0));ONE=(Q(1),Q(0));D=(Q(11),Q(-6))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def scale(a,n):return (a[0]*n,a[1]*n)
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def inverse(a):
    norm=a[0]*a[0]-2*a[1]*a[1]
    assert norm
    return (a[0]/norm,-a[1]/norm)
def curve(x,y):return sub(mul(y,y),sub(mul(mul(x,x),x),mul(D,x)))
def double(point):
    x,y=point;slope=mul(sub(scale(mul(x,x),3),D),inverse(scale(y,2)))
    X=sub(mul(slope,slope),scale(x,2));Y=sub(mul(slope,sub(x,X)),y)
    assert curve(X,Y)==ZERO
    return X,Y


def preservation_identity():
    # Independent sparse integer arithmetic in x,y,L,D,X,Y.
    def plus(*ps):
        out={}
        for p in ps:
            for m,c in p.items():out[m]=out.get(m,0)+c
        return {m:c for m,c in out.items() if c}
    def times(p,q):
        out={}
        for m,c in p.items():
            for n,d in q.items():
                v=tuple(a+b for a,b in zip(m,n));out[v]=out.get(v,0)+c*d
        return {m:c for m,c in out.items() if c}
    def sc(p,n):return {m:c*n for m,c in p.items() if c*n}
    def square(p):return times(p,p)
    xs=[]
    for i in range(6):
        mon=[0]*6;mon[i]=1;xs.append({tuple(mon):1})
    x,y,L,d,X,Y=xs;t=plus(X,sc(x,-1));Y0=plus(sc(y,-1),sc(times(L,t),-1))
    left=plus(square(Y),sc(times(square(X),X),-1),times(d,X))
    old=plus(square(y),sc(times(square(x),x),-1),times(d,x))
    tangent=plus(sc(times(y,L),2),sc(square(x),-3),d)
    output=plus(square(L),sc(X,-1),sc(x,-2))
    right=plus(old,times(t,tangent),times(square(t),output),times(plus(Y,sc(Y0,-1)),plus(Y,Y0)))
    assert left==right
    # Bezout identity after q=x^2 and f=x^3-D*x, independently expanded.
    q=square(x);f=plus(times(q,x),sc(times(d,x),-1))
    n=plus(sc(q,3),sc(d,-1));cofactor=plus(sc(q,3),sc(d,-2))
    assert plus(times(n,cofactor),sc(times(x,f),-9))==sc(square(d),2)


def evaluate(row,values):
    total=Q(0)
    for c,mon in row:
        value=Q(c)
        for v in mon:value*=values[v]
        total+=value
    return total


def preservation_checks(old,new,receipt):
    gone=receipt['parent_removed_variables'];deleted=receipt['parent_removed_rows']
    assert gone==[38,39,48,49,58,59,68,69]
    assert deleted==[16,17,26,27,36,37,46,47]
    vi=lambda v:v-sum(x<v for x in gone)
    ri=lambda r:r-sum(x<r for x in deleted)
    changed={18,19,28,29,38,39,48,49}
    count=0
    for i,row in enumerate(old['residuals']):
        if i in changed or i in deleted:continue
        assert new['residuals'][ri(i)]==[[c,[vi(v) for v in mon]] for c,mon in row]
        count+=1
    assert new['calls']==[dict(call,args=[vi(v) for v in call['args']]) for call in old['calls']]
    variable_fields=('proxy_indices',)
    for key in variable_fields:assert new[key]==list(map(vi,old[key]))
    assert new['point_coordinates']=={key:list(map(vi,val)) for key,val in old['point_coordinates'].items()}
    assert new['joint_chart_targets']==[{key:list(map(vi,val)) for key,val in item.items()} for item in old['joint_chart_targets']]
    assert new['root_targets']==[{key:val if key=='kind' else list(map(vi,val)) for key,val in item.items()} for item in old['root_targets']]
    for name,chart in old['general_root_charts'].items():
        for key,values in chart.items():
            assert new['general_root_charts'][name][key]==(values if key=='kind' else list(map(ri if key.endswith('_rows') else vi,values)))
    for key,values in old['fixed_target_bindings'].items():
        assert new['fixed_target_bindings'][key]==list(map(ri if key.endswith('rows') else vi,values))
    assert new['target_two_bindings']==dict(rows=list(map(ri,old['target_two_bindings']['rows'])),first_doubling_only=True)
    transformed={'locals','residuals','calls','construction_log','proxy_indices','point_coordinates',
        'joint_chart_targets','root_targets','general_root_charts','fixed_target_bindings','target_two_bindings'}
    for key in old:
        if key not in transformed:assert new[key]==old[key],key
    assert set(new)-set(old)=={'direct_tangent_doublings','root_doubling_model','direct_tangent_rewrite'}
    expected=[]
    for kind,i,label in old['construction_log']:
        if kind=='variable' and i not in gone:expected.append([kind,vi(i),label])
        elif kind=='equation' and i not in deleted:
            if i in changed:
                role=('A','S','T','Z')[(i-18)//10];label='direct tangent '+role+'.1.'+str((i-18)%10)
            expected.append([kind,ri(i),label])
    assert new['construction_log']==expected
    return count


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parent-root',type=Path,required=True)
    p.add_argument('--root-helper',type=Path,required=True)
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    assert hashlib.sha256(a.root_helper.read_bytes()).hexdigest()==HELPER
    spec=importlib.util.spec_from_file_location('frozen_general_root',a.root_helper)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    old,unused=helper.rewrite_root(json.loads(a.parent_root.read_bytes()))
    before=deepcopy(old);new,receipt=producer.rewrite_root(old);assert before==old
    untouched_rows=preservation_checks(old,new,receipt)
    assert (new['locals'],len(new['residuals']))==(210,195)
    assert {i for kind,i,label in new['construction_log'] if kind=='variable'}==set(range(1,211))
    assert {i for kind,i,label in new['construction_log'] if kind=='equation'}==set(range(195))
    assert producer.variables(new['residuals'])==set(range(211))
    assert max(len(mon) for row in new['residuals'] for _,mon in row)<=2
    gone=receipt['parent_removed_variables']
    transform=lambda i:i-sum(j<i for j in gone)
    point=((Q(1),Q(1)),(Q(0),Q(2)))
    old_checks=new_checks=0
    for role in producer.ROLES:
        assert curve(*point)==ZERO
        chart=old['general_root_charts'][role];x,y=point;values={}
        for ids,pair in ((chart['x'],x),(chart['y'],y)):
            values.update(zip(ids,pair))
        for step in range(1):
            start=chart['square'][0]+10*step;at=chart['square_rows'][0]+10*step
            square=mul(x,x);inv=inverse(scale(y,2));slope=mul(sub(scale(square,3),D),inv)
            slope2=mul(slope,slope);X=sub(slope2,scale(x,2));yp=mul(slope,sub(x,X))
            for k,pair in enumerate((square,inv,slope,slope2,yp)):
                values.update(zip((start+2*k,start+2*k+1),pair))
            assert all(evaluate(row,values)==0 for row in old['residuals'][at:at+10]);old_checks+=10
            mapped={transform(i):v for i,v in values.items() if i not in gone}
            record=next(r for r in new['direct_tangent_doublings'] if r['role']==role and r['step']==step+1)
            for key in ('square_rows','tangent_rows','slope_square_rows','ordinate_product_rows'):
                assert all(evaluate(new['residuals'][i],mapped)==0 for i in record[key]);new_checks+=2
            reconstructed_y=tuple(evaluate(poly,mapped) for poly in record['input_y'])
            assert inverse(scale(reconstructed_y,2))==inv
            numerator=sub(scale(mul(slope,sub(scale(square,3),scale(D,2))),2),scale(mul(x,y),9))
            assert mul(numerator,inverse(scale(mul(D,D),4)))==inv
            x,y=X,sub(yp,y);assert curve(x,y)==ZERO
        point=double(point)
    preservation_identity()
    d=(Q(3),Q(-1))
    for x in (ZERO,d,neg(d)):
        assert curve(x,ZERO)==ZERO
        assert sub(scale(mul(x,x),3),D)!=ZERO
    rejected=[]
    for label,edit in (
            ('row coefficient',lambda r:r['residuals'][14][0].__setitem__(0,99)),
            ('outside inverse row',lambda r:r['residuals'].append([[1,[38]]])),
            ('outside inverse call',lambda r:r['calls'][0]['args'].__setitem__(0,38)),
            ('wrong curve metadata',lambda r:r['general_root_charts']['A']['x'].__setitem__(0,38)),
            ('wrong historical receipt',lambda r:r['general_root_rewrite'].__setitem__('raw_variable_delta',0)),
            ('wrong target-two metadata',lambda r:r['target_two_bindings']['rows'].__setitem__(0,16)),
            ('wrong fixed linear metadata',lambda r:r['fixed_target_bindings']['linear_coordinates'].__setitem__(0,38)),
            ('wrong target multiplier',lambda r:r.__setitem__('comparison_target_multiplier',4)),
            ('changed free input',lambda r:r.__setitem__('free',2))):
        bad=deepcopy(old);edit(bad)
        try:producer.rewrite_root(bad)
        except ValueError as exc:
            assert str(exc)=='Unpinned general-root input';rejected.append(label)
        else:raise AssertionError('Accepted '+label)
    result=dict(status='PASS: tiny source-fragment and exact algebra tests',source_locals=[218,210],source_rows=[203,195],
        old_component_checks=old_checks,new_component_checks=new_checks,denominator_reconstructions=4,
        symbolic_curve_preservation=True,symbolic_bezout_identity=True,
        polynomial_inverse_reconstructions=4,excluded_two_torsion_points=3,pin_rejections=rejected,
        unchanged_rows_verified=untouched_rows,complete_metadata_remapping=True,
        producer_sha256=hashlib.sha256(Path(producer.__file__).read_bytes()).hexdigest(),
        output_root_canonical_sha256=hashlib.sha256(producer.canonical(new)).hexdigest(),
        whole_source_built=False,quartic_expanded=False)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.report:a.report.write_text(text)
    print(text,end='')


if __name__=='__main__':main()
