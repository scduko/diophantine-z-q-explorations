"""Local Lucas residuals on the joint-chart source; no source authorization.

Install after joint_chart and before this packet's conic_lucas hook. The
root edit is a checked source revision, not an old-certificate rewrite.
"""
from collections import Counter
from copy import deepcopy

PROOF_SHA256 = '2c4b1a1f24a485b021ff11561043a412a61186e243194ba244b6090124b83570'
REVIEW_SHA256 = '818c51743e55536c0b10da8c4153d82f45ee5ab64d6f2cb68abb6d5482c9f715'
MODEL = 'joint f,p,A,K curve and complete z graph; no difference formal tests'
EXTRA_LAYOUT = ';target_F_slots_are_J_over_conj_q;extra_targets[s,t,u]'
POLYNOMIAL = 'T^2-S*(S-2)*T*Z+(S-2)^2*Z^2-1'
COUNTS = {'q_compare4': 13, 'q_compare_beta': 8, 'q_compare_lucas': 16}
MODES = {
    'q_compare4': dict(n=4, old_free=61, free=58, legacy=28, proxy_count=1,
        remove_slots=[1,2,3], batch='q_batch31', g=[40,12,40,40,40],
        orders=[1]*6+[12,40]+[40,12,40,40,40],
        layout='beta;Fq(P4);Fq(A4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_beta': dict(n=1, old_free=28, free=28, legacy=16, proxy_count=1,
        remove_slots=[], batch='q_batch13', g=[12,12],
        orders=[1]*3+[12]*3,
        layout='beta;Fq(P4);Fq(A4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_lucas': dict(n=3, old_free=50, free=47, legacy=23, proxy_count=0,
        remove_slots=[0,1,2], batch='q_batch25', g=[40]*4,
        orders=[1]*5+[40]*5,
        layout='Fq(P4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
}
ROOT_KEYS = {
    'name','free','locals','residuals','calls','construction_log','precision',
    'anchor_squarings','chart','prime_parity_witnesses','proxy_indices',
    'point_coordinates','coordinate_scalar_count','ordinary_contact_count',
    'contact_scale','contact_shift','contact_W','scalar_height_orders',
    'height_exponent','height_constant','scalar_rule','pell_equation',
    'jacobi_targets','beta_only_positions','lucas_only_positions',
    'full_comparison_positions','jacobi_mode_counts','jacobi_primary_pair_count',
    'joint_chart_targets','joint_chart_extra_target_coordinates',
}


def remove_root_proxies(b, original):
    """Audit every deleted variable use, then return the reindexed root."""
    if set(original) != ROOT_KEYS or original['name'] != 'Z_definition' or original['free'] != 1:
        raise ValueError('Unexpected joint root schema')
    labels = ['index proxy s', 'index proxy t', 'index proxy z']
    removed = []
    for label in labels:
        ids = [i for kind,i,text in original['construction_log'] if kind=='variable' and text==label]
        if len(ids) != 1:
            raise ValueError('Missing or duplicate root proxy variable')
        removed.extend(ids)
    rows = [i for kind,i,text in original['construction_log']
            if kind=='equation' and text=='Lucas norm proxy certificate']
    if len(rows) != 1 or len(set(removed)) != 3:
        raise ValueError('Missing or duplicate proxy equation')
    row_id = rows[0]
    if len(original['proxy_indices']) != 4 or original['proxy_indices'][1:] != removed:
        raise ValueError('Root proxy metadata does not match its declarations')
    S,T,Z = [b.P.v(i) for i in removed]
    expected = (T*T-S*(S-2)*T*Z+(S-2)**2*Z*Z-1).row()
    if original['residuals'][row_id] != expected:
        raise ValueError('Root proxy equation changed')
    gone = set(removed)
    for i,row in enumerate(original['residuals']):
        if i != row_id and any(gone.intersection(mon) for coefficient,mon in row):
            raise ValueError('A deleted proxy has an outside equation use')

    counts = Counter()
    for call in original['calls']:
        name,args = call['module'],call['args']
        if name in MODES:
            spec = MODES[name];counts[name] += 1
            if len(args) != spec['old_free']:
                raise ValueError('Unexpected old joint comparison arity')
            slots = spec['remove_slots']
            if slots and [args[i] for i in slots] != removed:
                raise ValueError('Comparison proxy slots changed')
            if any(value in gone for i,value in enumerate(args) if i not in slots):
                raise ValueError('A deleted proxy has an outside comparison use')
        elif gone.intersection(args):
            raise ValueError('A deleted proxy is used by another module')
    if dict(counts) != COUNTS:
        raise ValueError('Wrong root comparison multiplicities')

    ordered = sorted(gone)
    def variable(value):
        if type(value) is not int:
            raise ValueError('Noninteger variable index')
        if value in gone:
            raise ValueError('A deleted proxy remains in retained metadata')
        return value-sum(i<value for i in ordered) if value>=0 else value
    result = deepcopy(original)
    result['residuals'] = [[[coefficient,[variable(v) for v in mon]] for coefficient,mon in row]
                           for i,row in enumerate(original['residuals']) if i!=row_id]
    result['calls'] = []
    for call in original['calls']:
        revised = deepcopy(call)
        slots = MODES[call['module']]['remove_slots'] if call['module'] in MODES else []
        revised['args'] = [variable(v) for i,v in enumerate(call['args']) if i not in slots]
        result['calls'].append(revised)
    result['construction_log'] = []
    for kind,index,label in original['construction_log']:
        if kind=='variable':
            if index not in gone:
                result['construction_log'].append([kind,variable(index),label])
        elif kind=='equation':
            if index!=row_id:
                result['construction_log'].append([kind,index-(index>row_id),label])
        else:
            raise ValueError('Unexpected construction-log operation')
    result['locals'] -= 3
    result['proxy_indices'] = [variable(original['proxy_indices'][0])]
    result['point_coordinates'] = {name:[variable(v) for v in values]
                                  for name,values in original['point_coordinates'].items()}
    for key,fields in [('jacobi_targets',{'original','p','f'}),
                       ('joint_chart_targets',{'q','r','s','t','u'})]:
        entries = []
        for entry in original[key]:
            if set(entry)!=fields:
                raise ValueError('Unexpected target metadata schema')
            entries.append({name:[variable(v) for v in values] for name,values in entry.items()})
        result[key] = entries
    del result['pell_equation']
    result['local_lucas_residual'] = True
    result['local_lucas_polynomial'] = POLYNOMIAL
    result['retained_proxy_roles'] = ['beta']
    result['lucas_proxy_removal'] = dict(
        original_variables=removed, original_row=row_id,
        removed_input_slots={name:spec['remove_slots'][:] for name,spec in MODES.items()},
        variable_reindex='subtract number of removed original indices strictly below the index',
    )
    return result


def install(b, rational, low, base_make_batch):
    """Install after joint_chart, before conic_lucas, on a fresh builder."""
    if not getattr(b,'_joint_chart_installed',False) or not getattr(b,'_rational_difference_installed',False):
        raise ValueError('The pinned joint chart must be installed first')
    if getattr(b,'_local_lucas_installed',False) or getattr(b,'_private_conic_installed',False):
        raise ValueError('Wrong local-Lucas installation order')
    if b.MODULES or rational.COUNTS != COUNTS:
        raise ValueError('Expected fresh three-mode builder')
    if getattr(base_make_batch,'__name__',None)!='make_batch' or base_make_batch.__globals__.get('M') is not b.M:
        raise ValueError('Expected original archive batch constructor')
    b._local_lucas_installed = True

    def point(field,name):
        f,p=[b.fvar(field.m,name+'.'+key) for key in ('f','p')]
        return dict(f=f,p=p)

    def difference(field,P,r,q,s,t,u,jz):
        m=field.m;f=field.conj(P['f']);p=field.conj(P['p']);D=field.conj(field.D)
        A,K=[b.fvar(m,'joint chart.'+name) for name in ('A','K')]
        b.feq(m,b.fs(K,b.raw_fmul(b.fs(A,r),p)),'joint chart K=(A-r)p')
        DtA=b.raw_fmul(D,b.raw_fmul(t,A))
        first=b.fs(b.fa(b.raw_fmul(K,p),b.raw_fmul(u,p)),
                   b.fa(b.scale(b.raw_fmul(D,b.raw_fmul(r,f)),2),b.scale(DtA,4)))
        b.feq(m,first,'joint chart first relation')
        second=b.fa(b.scale(b.raw_fmul(D,b.raw_fmul(b.fa(A,r),f)),2),
                    b.fa(b.raw_fmul(s,K),b.fa(b.scale(DtA,4),b.raw_fmul(jz,field.conj(q)))))
        b.feq(m,second,'joint chart second relation')
        return A

    def comparison():
        for name,spec in MODES.items():
            n=spec['n'];base=spec['legacy'];first_j=base-7;start=spec['proxy_count']
            if name!='q_compare4':
                orders=[1]+[e for order in spec['orders'] for e in (order,order)]
                base_make_batch(spec['batch'],orders,'q_primeparity')
            m=b.M(name,spec['free']);field=b.Field(m)
            pair=lambda i:(b.P.v(i),b.P.v(i+1))
            fj=pair(first_j);jz=pair(first_j+2)
            theta=b.P.v(first_j+4);error=b.P.v(first_j+5);raw=first_j+6
            points=[point(field,label) for label in ['H']+['X'+str(i) for i in range(n)]]
            alternate=[difference(field,P,pair(start+4*j),pair(start+4*j+2),
                                  pair(base+6*j),pair(base+6*j+2),pair(base+6*j+4),jz)
                       for j,P in enumerate(points)]
            def g(P,e):
                profile=rational.LOW if e==12 else rational.HIGH
                return low.emit_g(b,field,P['f'],e,bind_output=False,hscale=1,
                                  scheme=profile['scheme'],normalization=profile['normalization'])
            lam=b.fvar(m,'common negative logarithm')
            b.feq(m,b.fs(b.raw_fmul(lam,points[0]['p']),g(points[0],spec['g'][0])),'H pH=GH')
            ratios=[]
            for j,P in enumerate(points[1:]):
                ratio=b.fvar(m,'retained logarithm ratio');aux=b.fvar(m,'ratio times p')
                b.feq(m,b.fs(aux,b.raw_fmul(ratio,P['p'])),'A=C p')
                b.feq(m,b.fs(b.raw_fmul(aux,lam),g(P,spec['g'][j+1])),'A H=G')
                ratios.append(ratio)
            primary=[];evaluation=None
            if name!='q_compare_lucas':
                primary.append(b.fs(ratios[0],(b.P.v(0),b.P())))
            if name!='q_compare_beta':
                Cs,Ct,Cz=ratios[1:] if name=='q_compare4' else ratios
                V,Dv,E=[b.fvar(m,'local Lucas.'+label) for label in ('V','D','E')]
                b.feq(m,b.fs(V,b.raw_fmul(b.fs(Cs,(b.P(2),b.P())),Cz)),'local Lucas V=(Cs-2)Cz')
                b.feq(m,b.fa(b.fs(Dv,b.raw_fmul(Cs,Ct)),V),'local Lucas D=CsCt-V')
                b.feq(m,b.fa(b.fa(b.fs(E,b.raw_fmul(Ct,Ct)),b.raw_fmul(V,Dv)),(b.P(1),b.P())),
                      'local Lucas E=Ct2-VD-1')
                primary.append(E)
                evaluation=dict(ratios=[[m.bind(v) for v in ratio] for ratio in (Cs,Ct,Cz)],
                                V=[m.bind(v) for v in V],D=[m.bind(v) for v in Dv],E=[m.bind(v) for v in E],
                                order=40)
            fields=[P['f'] for P in points]+[fj]+primary+alternate
            if len(fields)!=len(spec['orders']):
                raise ValueError('Unexpected local-Lucas field count')
            tests=b.field_tests(m,theta,error,fields)
            if len(tests)!=1+2*len(fields):
                raise ValueError('Unexpected field-test boundary')
            m.call(spec['batch'],[raw]+tests)
            m.save(precision=spec['g'][0],label_precision=spec['g'][1],modeled_points=n,
                   field_inequality_orders=spec['orders'][:],logarithm_coordinate='reciprocal f=1/x',
                   compressed_primary_charts=True,high_log_profile=deepcopy(rational.LOW if spec['g'][0]==12 else rational.HIGH),
                   beta_log_profile=deepcopy(rational.LOW if spec['g'][1]==12 else rational.HIGH),
                   input_layout=spec['layout']+EXTRA_LAYOUT,difference_model=MODEL,
                   primary_square_transfer=False,x_squareclass_membership=False,
                   private_index_group='(1/2)Z via doubling',difference_formal_tests=False,
                   rational_difference_four_fields=False,joint_primary_difference_chart=True,
                   extra_target_start=base,local_lucas_residual=(name!='q_compare_beta'),
                   local_lucas_evaluation=evaluation,global_lucas_proxy_inputs=False)
    b.make_multi_comparison=comparison
    previous_root=b.make_root
    def root():
        previous_root()
        revised=remove_root_proxies(b,b.MODULES['Z_definition'])
        b.MODULES['Z_definition']=revised
        b.write('modules/Z_definition.json',revised)
    b.make_root=root
    return dict(local_lucas_residual=True,proof_sha256=PROOF_SHA256,review_sha256=REVIEW_SHA256,
                global_lucas_proxies_removed=True,field_count=377,source_pin_authorized=False,
                modes=deepcopy(MODES))
