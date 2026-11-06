"""Pinned root postprocessor for the separately reviewed target-two source.

This does not choose or authorize a whole-source parent. The caller must bind
its complete parent source independently. No frozen producer is imported.
"""
from copy import deepcopy
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
import json

PINS={
    'Z_definition':'5e96bf1b0de4e1694dcc7ff21a9a7b69b5e2cc61295c2fc2816696092c5dacde',
    'q_compare4':'924daadfdb5fb9f13b9e06fc7e457f224115d2e34801c070810d3ab5eef310c4',
    'q_compare_beta':'75189120b018c23bbf1573de56687103160872aca41d3d1d35138abb7b05203e',
    'q_compare_lucas':'a9157980855175cc0072f63c193c43f31c1350d850fdaeb3569d75e738229feb',
}
PROOF='ecdbfc9acd575a8ab194f8e76c356e7898544a506c705a40f169c6686c70a80e'
COMPOSITION='4e41f830938c3bdf8b5361b410a2fb639bd74299f0461fb356afe2efb012f2b7'
TARGET_TWO_PROOF='cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb'
TARGET_TWO_REVIEW='d5048cc8ac8944d26c8af6d9b8cfcdd672ddee1beed73efaf3d634a53b012155'
ROOT_KEYS={
    'name','free','locals','residuals','calls','construction_log','precision',
    'anchor_squarings','chart','prime_parity_witnesses','proxy_indices',
    'point_coordinates','coordinate_scalar_count','ordinary_contact_count',
    'contact_scale','contact_shift','contact_W','scalar_height_orders',
    'height_exponent','height_constant','scalar_rule','jacobi_targets',
    'beta_only_positions','lucas_only_positions','full_comparison_positions',
    'jacobi_mode_counts','jacobi_primary_pair_count','joint_chart_targets',
    'joint_chart_extra_target_coordinates','local_lucas_residual',
    'local_lucas_polynomial','retained_proxy_roles','lucas_proxy_removal',
}
PARTS=('u','v','w','z','f','h','x','y')
BLOCKS=('f=u^2','v2+df=1','w2+v2=2','h=vw','zh+u=0','xf=1','yz+x=0')
ROLES=('A','S','T','Z','height J','common comparison J')
SQUARES={'A':(112,113),'S':(132,133),'T':(152,153),'Z':(172,173)}
SQUARE_ROWS={'A':(100,101),'S':(120,121),'T':(140,141),'Z':(160,161)}
BINDINGS=((210,8,-57),(211,2,7),
          (287,1681,-456),(288,1681,-224),
          (285,41,87),(286,164,-129),
          (307,14637,55123),(308,58548,19301),
          (309,14161,-7624),(310,127449,39904))
BINDING_ROWS=(196,197,269,270,271,272,291,292,293,294)
FIXED_LINEAR_ROWS=(289,290,295,296)
SECOND_DOUBLING_VARIABLES=tuple(i for start in (122,142,162,182) for i in range(start,start+10))
SECOND_DOUBLING_ROWS=tuple(i for start in (110,130,150,170) for i in range(start,start+10))
TARGET_BINDING_ROWS=tuple(range(200,216))


def serialized(obj):return (json.dumps(obj,separators=(',',':'))+'\n').encode('utf-8')
def digest(obj):return sha256(serialized(obj)).hexdigest()
def pin(obj,name):
    if obj.get('name')!=name or digest(obj)!=PINS[name]:
        raise ValueError('Pinned input module mismatch: '+name)


def v(i):return {(i,):Q(1)}
def c(n):return {} if not n else {():Q(n)}
def plus(*polys):
    out={}
    for p in polys:
        for mon,n in p.items():out[mon]=out.get(mon,Q(0))+n
    return {m:n for m,n in out.items() if n}
def scale(p,n):return {m:a*n for m,a in p.items() if a*n}
def minus(a,b):return plus(a,scale(b,-1))
def times(a,b):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            mon=tuple(sorted(ma+mb));out[mon]=out.get(mon,Q(0))+ca*cb
    return {m:n for m,n in out.items() if n}
def field(ids):return tuple(v(i) for i in ids)
def fp(a,b):return plus(times(a[0],b[0]),scale(times(a[1],b[1]),2)),plus(times(a[0],b[1]),times(a[1],b[0]))
def fa(a,b):return tuple(plus(x,y) for x,y in zip(a,b))
def fs(a,b):return tuple(minus(x,y) for x,y in zip(a,b))
def row(p):
    if not p:raise ValueError('Unexpected zero replacement row')
    den=lcm(*(n.denominator for n in p.values()))
    ints={m:int(n*den) for m,n in p.items()};div=reduce(gcd,(abs(n) for n in ints.values()))
    if max(map(len,ints))>2:raise ValueError('New root row is not quadratic')
    return [[n//div,list(m)] for m,n in sorted(ints.items())]


def rewrite_root(original):
    """Return (new_root, provenance). All historical IDs remain historical."""
    pin(original,'Z_definition')
    if set(original)!=ROOT_KEYS or (original['free'],original['locals'],len(original['residuals']))!=(1,344,329):
        raise ValueError('Unexpected reference root structure')
    labels={};equations={}
    for kind,i,label in original['construction_log']:
        table=labels if kind=='variable' else equations if kind=='equation' else None
        if table is None:raise ValueError('Unexpected construction operation')
        table.setdefault(label,[]).append(i)
    def unique(table,label):
        values=table.get(label,[])
        if len(values)!=1:raise ValueError('Missing or ambiguous declaration '+label)
        return values[0]
    coords={name:{part:[unique(labels,name+'.'+part+'.'+str(k)) for k in range(2)]
                  for part in PARTS} for name in ROLES}
    oldrows={name:{part:[unique(equations,name+'.'+part+'.'+str(k)) for k in range(2)]
                    for part in BLOCKS} for name in ROLES}
    workrows=deepcopy(original['residuals']);ops=deepcopy(original['construction_log'])
    gone=set();deleted=set();patch_labels={};charts={};nextvar=345
    D=(c(11),c(-6))
    def append_field(poly,label):
        ids=[]
        for k,p in enumerate(poly):
            i=len(workrows);workrows.append(row(p));ops.append(['equation',i,label+'.'+str(k)]);ids.append(i)
        return ids
    for name in ROLES:
        keep={'x','y'} if name in ('A','T','Z') else {'x','y','f','z'} if name=='S' else {'f','z'}
        gone.update(i for part in PARTS if part not in keep for i in coords[name][part])
        retained_blocks={'xf=1','yz+x=0'} if name=='S' else set()
        deleted.update(i for part in BLOCKS if part not in retained_blocks for i in oldrows[name][part])
        if name in SQUARES:
            x,y=field(coords[name]['x']),field(coords[name]['y']);q=field(SQUARES[name])
            expected=[row(p) for p in fs(q,fp(x,x))]
            if [workrows[i] for i in SQUARE_ROWS[name]]!=expected:
                raise ValueError('First doubling square changed for '+name)
            newrows=append_field(fa(fs(fp(y,y),fp(x,q)),fp(D,x)),'general root '+name+' curve')
            charts[name]=dict(kind='first_double_curve',x=coords[name]['x'],y=coords[name]['y'],
                              square=list(SQUARES[name]),square_rows=list(SQUARE_ROWS[name]),curve_rows=newrows)
            if name=='S':charts[name].update(f=coords[name]['f'],z=coords[name]['z'])
        else:
            kids=[nextvar,nextvar+1];nextvar+=2
            for k,i in enumerate(kids):ops.append(['variable',i,'general root '+name+'.k.'+str(k)])
            f,z,k=field(coords[name]['f']),field(coords[name]['z']),field(kids)
            newrows=append_field(fs(k,fp(f,z)),'general root '+name+' k=fz')
            newrows+=append_field(fa(fs(f,fp(z,z)),fp(D,fp(k,k))),'general root '+name+' reciprocal curve')
            charts[name]=dict(kind='reciprocal_f_z',f=coords[name]['f'],z=coords[name]['z'],k=kids,curve_rows=newrows)

    gone.update(range(92,112));gone.update((212,213))
    deleted.update(range(80,100));deleted.update((198,199))
    gone.update(SECOND_DOUBLING_VARIABLES);deleted.update(SECOND_DOUBLING_ROWS)
    for position,(i,(variable,mult,constant)) in enumerate(zip(BINDING_ROWS,BINDINGS)):
        workrows[i]=row(plus(scale(v(variable),mult),c(constant)))
        patch_labels[i]='fixed Pstar '+('x','f','q','conjugate s','conjugate t')[position//2]+'.'+str(position%2)
    # The common J pair is 1/conj(z(Jroot)), not the root point itself.
    common=field((208,209))
    inverse_q=(c(Q(-232,357)),c(Q(86,357)))
    conjugate_s_over_q=(c(Q(291673,127449)),c(Q(-29440,42483)))
    for name,ids,multiplier,rids in (
            ('r',(305,306),inverse_q,(289,290)),
            ('u',(311,312),conjugate_s_over_q,(295,296))):
        for k,(rid,p) in enumerate(zip(rids,fs(field(ids),fp(common,multiplier)))):
            workrows[rid]=row(p);patch_labels[rid]='fixed Pstar '+name+'.'+str(k)
    for j,name in enumerate(('A','S','T','Z')):
        # The retained first doubling has x2=lambda^2-2x and y2=gate-y.
        x2=tuple(minus(v(118+20*j+k),scale(v(coords[name]['x'][k]),2)) for k in range(2))
        y2=tuple(minus(v(120+20*j+k),v(coords[name]['y'][k])) for k in range(2))
        target=original['jacobi_targets'][j+1]['original']
        for k,p in enumerate(fs(field(target[:2]),x2)+fs(field(target[2:]),y2)):
            rid=200+4*j+k;workrows[rid]=row(p)
            patch_labels[rid]='double target '+name+'.'+('x' if k<2 else 'y')+'.'+str(k%2)

    for i,r in enumerate(workrows):
        if i not in deleted and any(gone.intersection(mon) for coefficient,mon in r):
            raise ValueError('Deleted root coordinate remains in row '+str(i))
    for call in original['calls']:
        if gone.intersection(call['args']):raise ValueError('Deleted root coordinate remains in call')
    ordered=sorted(gone)
    def variable(i):
        if type(i) is not int:raise ValueError('Noninteger live coordinate')
        if i in gone:raise ValueError('Deleted root coordinate remains in metadata')
        return i-sum(j<i for j in ordered) if i>=0 else i
    rowmap={old:new for new,old in enumerate(i for i in range(len(workrows)) if i not in deleted)}
    result=deepcopy(original)
    result['locals']=nextvar-1-len(gone)
    result['residuals']=[[[a,[variable(i) for i in mon]] for a,mon in r]
                         for j,r in enumerate(workrows) if j not in deleted]
    result['calls']=[dict(call,args=[variable(i) for i in call['args']]) for call in original['calls']]
    result['construction_log']=[]
    for kind,i,label in ops:
        if kind=='variable' and i not in gone:result['construction_log'].append([kind,variable(i),label])
        elif kind=='equation' and i not in deleted:result['construction_log'].append([kind,rowmap[i],patch_labels.get(i,label)])
    result['proxy_indices']=[variable(i) for i in original['proxy_indices']]
    result['point_coordinates']={name:[variable(i) for i in ids] for name,ids in original['point_coordinates'].items()}
    result['joint_chart_targets']=[{key:[variable(i) for i in ids] for key,ids in entry.items()}
                                   for entry in original['joint_chart_targets']]
    targets=[]
    for j,entry in enumerate(original['jacobi_targets']):
        if set(entry)!={'original','p','f'}:raise ValueError('Unexpected old target metadata')
        item=dict(kind='fixed_Pstar' if j==0 else 'double',p=[variable(i) for i in entry['p']],f=[variable(i) for i in entry['f']])
        item['x' if j==0 else 'original']=[variable(i) for i in (entry['original'][:2] if j==0 else entry['original'])]
        targets.append(item)
    del result['jacobi_targets'];result['root_targets']=targets
    mapped_charts={}
    for name,entry in charts.items():
        mapped_charts[name]={key:(value if key=='kind' else [rowmap[i] for i in value] if key.endswith('_rows') else [variable(i) for i in value])
                             for key,value in entry.items()}
    result.update(chart='general_E_mixed',baseline_chart=10,general_root_charts=mapped_charts,
        root_carrier='nontorsion E(K)',root_index_semantics='2Q=n_Q Pstar, n_Q integer',
        comparison_base=dict(x=['1','1'],y=['0','2'],identity='2R=Pstar',fixed_target='2R=Pstar'),
        beta_comparison_scale=2,height_effective_multiplier=5,
        fixed_target_bindings=dict(coordinates=[variable(x[0]) for x in BINDINGS],rows=[rowmap[i] for i in BINDING_ROWS],
            linear_coordinates=[variable(i) for i in (305,306,311,312)],linear_rows=[rowmap[i] for i in FIXED_LINEAR_ROWS]),
        comparison_target_multiplier=2,
        target_two_bindings=dict(rows=[rowmap[i] for i in TARGET_BINDING_ROWS],
            first_doubling_only=True))
    provenance=dict(parent_root_sha256=PINS['Z_definition'],proof_sha256=PROOF,composition_contract_sha256=COMPOSITION,
        target_two_proof_sha256=TARGET_TWO_PROOF,target_two_review_sha256=TARGET_TWO_REVIEW,
        original_removed_variables=ordered,original_removed_rows=sorted(deleted),
        original_added_k_variables=list(range(345,349)),original_replaced_rows=sorted(BINDING_ROWS+FIXED_LINEAR_ROWS+TARGET_BINDING_ROWS),
        original_index_scope='all original_* fields are historical pre-rewrite IDs',
        raw_variable_delta=result['locals']-original['locals'],raw_row_delta=len(result['residuals'])-len(original['residuals']))
    result['general_root_rewrite']=deepcopy(provenance)
    if (result['locals'],len(result['residuals']),len(result['calls']))!=(218,203,39):
        raise ValueError('Unexpected root rewrite count')
    # The old proxy-removal receipt is historical and must not be reindexed.
    if result['lucas_proxy_removal']!=original['lucas_proxy_removal']:
        raise ValueError('Historical proxy provenance changed')
    return result,provenance


def rewrite_beta(original):
    name=original.get('name')
    if name not in ('q_compare4','q_compare_beta'):raise ValueError('Not a beta-bearing module')
    pin(original,name)
    result=deepcopy(original)
    ratio=[i for kind,i,label in original['construction_log'] if kind=='variable' and label=='retained logarithm ratio.0']
    if len(ratio)!=1:raise ValueError('Missing beta ratio coordinate')
    field_index=6 if name=='q_compare4' else 3
    target=original['conic_field_inputs'][field_index][0]
    matches=[i for i,r in enumerate(original['residuals']) if r==row(plus(v(target),v(0),scale(v(ratio[0]),-1)))]
    if len(matches)!=1:raise ValueError('Missing exact original beta coefficient row')
    rid=matches[0]
    result['residuals'][rid]=row(plus(v(target),scale(v(0),2),scale(v(ratio[0]),-1)))
    result['beta_comparison_scale']=2
    result['root_index_semantics']='2Q=n_Q Pstar, n_Q integer'
    result['beta_field_row']=rid
    result['beta_rewrite_parent_sha256']=PINS[name]
    return result


def postprocess_modules(modules):
    """Pure module-dictionary postprocessor. Caller writes and re-flattens."""
    result=deepcopy(modules)
    root,receipt=rewrite_root(modules['Z_definition']);result['Z_definition']=root
    for name in ('q_compare4','q_compare_beta'):result[name]=rewrite_beta(modules[name])
    pin(modules['q_compare_lucas'],'q_compare_lucas')
    for name in ('q_compare4','q_compare_beta','q_compare_lucas'):
        result[name]['comparison_fixed_target']='2R=Pstar'
        result[name]['comparison_target_multiplier']=2
        result[name]['root_index_semantics']='2Q=n_Q Pstar, n_Q integer'
        layout=result[name]['input_layout']
        if layout.count('Fq(P4)')!=1:raise ValueError('Unexpected legacy fixed-target label')
        result[name]['input_layout']=layout.replace('Fq(P4)','Fq(Pstar)')
    changed=[name for name in result if result[name]!=modules[name]]
    if set(changed)!={'Z_definition','q_compare4','q_compare_beta','q_compare_lucas'}:
        raise ValueError('Unexpected changed module set')
    return result,dict(root=receipt,changed_modules=sorted(changed),source_pin_authorized=False)
