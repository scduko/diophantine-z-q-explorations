"""Exact pinned target-two source postprocessor for four direct tangents.

This is a new-source fragment. It does not authorize an old certificate edit.
"""
from copy import deepcopy
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
import json
from math import gcd,lcm

PARENT_ROOT_CANONICAL_SHA256='1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2'
ROLES=('A','S','T','Z')


def canonical(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode('ascii')
def v(i):return {(i,):Q(1)}
def c(n):return {():Q(n)} if n else {}
def add(*polys):
    out={}
    for p in polys:
        for m,a in p.items():out[m]=out.get(m,Q(0))+a
    return {m:a for m,a in out.items() if a}
def scale(p,a):return {m:x*a for m,x in p.items() if x*a}
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    out={}
    for m,a in p.items():
        for n,b in q.items():
            term=tuple(sorted(m+n));out[term]=out.get(term,Q(0))+a*b
    return {m:a for m,a in out.items() if a}
def field(ids):return tuple(v(i) for i in ids)
def fm(p,q):return add(mul(p[0],q[0]),scale(mul(p[1],q[1]),2)),add(mul(p[0],q[1]),mul(p[1],q[0]))
def fa(p,q):return tuple(add(x,y) for x,y in zip(p,q))
def fs(p,q):return tuple(sub(x,y) for x,y in zip(p,q))
def fc(p,a):return tuple(scale(x,a) for x in p)
def row(p):
    if not p:raise ValueError('Zero expected row')
    denominator=lcm(*(x.denominator for x in p.values()))
    terms={m:int(x*denominator) for m,x in p.items()}
    divisor=reduce(gcd,(abs(x) for x in terms.values()))
    if max(map(len,terms))>2:raise ValueError('Nonquadratic row')
    return [[x//divisor,list(m)] for m,x in sorted(terms.items())]
def variables(rows):return {v for r in rows for _,mon in r for v in mon}


def rewrite_root(original):
    if sha256(canonical(original)).hexdigest()!=PARENT_ROOT_CANONICAL_SHA256:
        raise ValueError('Unpinned general-root input')
    if (original['free'],original['locals'],len(original['residuals']))!=(1,218,203):
        raise ValueError('Unexpected root shape')
    if original['comparison_target_multiplier']!=2 or original['target_two_bindings']['first_doubling_only'] is not True:
        raise ValueError('Not the target-two source')
    work=deepcopy(original['residuals']);deleted=set();gone=set();labels={};records=[]
    D=(c(11),c(-6));one=(c(1),c(0))
    for role in ROLES:
        chart=original['general_root_charts'][role]
        if chart['kind']!='first_double_curve':raise ValueError('Missing curve chart')
        x,y=field(chart['x']),field(chart['y'])
        base=chart['square'][0];firstrow=chart['square_rows'][0]
        if chart['square']!=[base,base+1] or chart['square_rows']!=[firstrow,firstrow+1]:
            raise ValueError('Unexpected first square coordinates')
        expected_curve=[row(p) for p in fa(fs(fm(y,y),fm(x,field(chart['square']))),fm(D,x))]
        if [work[i] for i in chart['curve_rows']]!=expected_curve:
            raise ValueError('Wrong first curve equations')
        for step in range(1):
            start=base+10*step;at=firstrow+10*step
            q,inv,slope,slope2,yp=[field([start+2*k,start+2*k+1]) for k in range(5)]
            xx=fs(slope2,fc(x,2));yy=fs(yp,y)
            numerator=fs(fc(q,3),D)
            expected=[row(p) for pair in (
                fs(q,fm(x,x)),fs(fm(fc(y,2),inv),one),fs(slope,fm(numerator,inv)),
                fs(slope2,fm(slope,slope)),fs(yp,fm(slope,fs(x,xx)))) for p in pair]
            if work[at:at+10]!=expected:
                raise ValueError('Changed doubling equations '+role+' '+str(step+1))
            removed={start+2,start+3};allowed=set(range(at+2,at+6))
            if any(removed.intersection(variables([r])) for i,r in enumerate(work) if i not in allowed):
                raise ValueError('Reused doubling inverse')
            if any(removed.intersection(call['args']) for call in original['calls']):
                raise ValueError('Doubling inverse escapes in a call')
            for k,p in enumerate(fs(fm(fc(y,2),slope),numerator)):
                work[at+4+k]=row(p);labels[at+4+k]='direct tangent '+role+'.'+str(step+1)+'.'+str(k)
            deleted.update((at+2,at+3));gone.update(removed)
            records.append(dict(role=role,step=step+1,input_x=x,input_y=y,
                square=[start,start+1],slope=[start+4,start+5],square_rows=[at,at+1],
                tangent_rows=[at+4,at+5],slope_square_rows=[at+6,at+7],
                ordinate_product_rows=[at+8,at+9]))
            x,y=xx,yy
    if len(gone)!=8 or len(deleted)!=8:raise ValueError('Wrong doubling count')
    if any(gone.intersection(variables([r])) for i,r in enumerate(work) if i not in deleted):
        raise ValueError('Deleted inverse remains')
    ordered=sorted(gone)
    def vi(i):
        if type(i) is not int or i in gone:raise ValueError('Invalid live variable metadata')
        return i-sum(j<i for j in ordered) if i>=0 else i
    rowmap={i:j for j,i in enumerate(i for i in range(len(work)) if i not in deleted)}
    def encoded(poly):
        if any(a.denominator!=1 for a in poly.values()):raise ValueError('Unexpected affine denominator')
        return [[int(a),[vi(i) for i in mon]] for mon,a in sorted(poly.items())]
    result=deepcopy(original)
    result['locals']-=len(gone)
    result['residuals']=[[[a,[vi(i) for i in mon]] for a,mon in r] for j,r in enumerate(work) if j not in deleted]
    result['calls']=[dict(call,args=[vi(i) for i in call['args']]) for call in original['calls']]
    result['construction_log']=[]
    for kind,i,label in original['construction_log']:
        if kind=='variable' and i not in gone:result['construction_log'].append([kind,vi(i),label])
        elif kind=='equation' and i not in deleted:result['construction_log'].append([kind,rowmap[i],labels.get(i,label)])
    result['proxy_indices']=[vi(i) for i in original['proxy_indices']]
    result['point_coordinates']={name:[vi(i) for i in ids] for name,ids in original['point_coordinates'].items()}
    result['joint_chart_targets']=[{name:[vi(i) for i in ids] for name,ids in item.items()} for item in original['joint_chart_targets']]
    result['root_targets']=[{name:(value if name=='kind' else [vi(i) for i in value]) for name,value in item.items()} for item in original['root_targets']]
    result['general_root_charts']={name:{key:(value if key=='kind' else [rowmap[i] for i in value] if key.endswith('_rows') else [vi(i) for i in value])
                                      for key,value in item.items()} for name,item in original['general_root_charts'].items()}
    fixed=original['fixed_target_bindings']
    if set(fixed)!={'coordinates','rows','linear_coordinates','linear_rows'}:
        raise ValueError('Unexpected fixed-target metadata')
    result['fixed_target_bindings']={key:[rowmap[i] if key.endswith('rows') else vi(i) for i in values]
                                     for key,values in fixed.items()}
    targets=original['target_two_bindings']
    if set(targets)!={'rows','first_doubling_only'}:
        raise ValueError('Unexpected target-two metadata')
    result['target_two_bindings']=dict(rows=[rowmap[i] for i in targets['rows']],first_doubling_only=True)
    mapped=[]
    for item in records:
        mapped.append({key:([encoded(p) for p in value] if key in ('input_x','input_y')
                            else [rowmap[i] for i in value] if key.endswith('_rows')
                            else [vi(i) for i in value] if key in ('square','slope') else value)
                       for key,value in item.items()})
    result['direct_tangent_doublings']=mapped
    result['root_doubling_model']='direct tangent with retained square coordinates'
    receipt=dict(parent_root_canonical_sha256=PARENT_ROOT_CANONICAL_SHA256,
        parent_removed_variables=ordered,parent_removed_rows=sorted(deleted),
        historical_index_scope='parent_* IDs refer to the pre-tangent target-two root module',
        raw_variable_delta=-8,raw_row_delta=-8,doublings=4,
        nonzero_proof='y*[2*lambda*(3*q-2*D)-9*x*y]=2*D^2, D=11-6sqrt(2) nonzero',
        inverse_recovery='inverse(2*y)=[2*lambda*(3*q-2*D)-9*x*y]/(4*D^2)',
        source_pin_authorized=False)
    result['direct_tangent_rewrite']=deepcopy(receipt)
    if (result['locals'],len(result['residuals']))!=(210,195):raise ValueError('Wrong output count')
    # Older receipts deliberately retain their own historical index systems.
    for name in ('general_root_rewrite','lucas_proxy_removal'):
        if result[name]!=original[name]:raise ValueError('Historical receipt changed')
    return result,receipt
