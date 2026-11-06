"""Eight-pair normalized Lucas blocks after the local-Lucas source hook.

The root, scalar, anchor, beta comparator and conic batches are unchanged.
This is a new arithmetic source, not an old private-witness equivalence.
"""
from copy import deepcopy

PROOF_SHA256='e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811'
MODEL='joint f,p,A,K curve and complete z graph; no difference formal tests'
EXTRA_LAYOUT=';target_F_slots_are_J_over_conj_q;extra_targets[s,t,u]'
NORMALIZATION='F(C_s,C_t,C_z)/C_s^2'
MODES={
    'q_compare4':dict(n=4,free=58,legacy=28,proxy_count=1,batch='q_batch31',
        g=[40,12,40,40,40],orders=[1]*6+[12,40]+[40,12,40,40,40],
        layout='beta;Fq(P4);Fq(A4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_beta':dict(n=1,free=28,legacy=16,proxy_count=1,batch='q_batch13',
        g=[12,12],orders=[1]*3+[12]*3,
        layout='beta;Fq(P4);Fq(A4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_lucas':dict(n=3,free=47,legacy=23,proxy_count=0,batch='q_batch25',
        g=[40]*4,orders=[1]*5+[40]*5,
        layout='Fq(P4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
}


def install(b,rational,low,base_make_batch):
    """Install after local_lucas, before unchanged conic_lucas.install(b)."""
    if not getattr(b,'_local_lucas_installed',False) or not getattr(b,'_joint_chart_installed',False):
        raise ValueError('Install pinned local-Lucas and joint-chart hooks first')
    if getattr(b,'_normalized_lucas_installed',False) or getattr(b,'_private_conic_installed',False):
        raise ValueError('Wrong normalized-Lucas installation order')
    if b.MODULES or (b.PELL_PRECISION,b.ANCHOR_SQUARINGS,b.CURVE_DROOT,b.CURVE_D2)!=(40,25,(3,-1),(11,-6)):
        raise ValueError('Expected fresh H19/high40/beta12/anchor25 builder')
    if getattr(base_make_batch,'__name__',None)!='make_batch' or base_make_batch.__globals__.get('M') is not b.M:
        raise ValueError('Expected original archive batch constructor')
    b._normalized_lucas_installed=True

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
            primary=[];Bs={};ps={};evaluation=None
            for j,Pnt in enumerate(points[1:]):
                if name!='q_compare_lucas' and j==0:
                    ratio=b.fvar(m,'retained logarithm ratio');aux=b.fvar(m,'ratio times p')
                    b.feq(m,b.fs(aux,b.raw_fmul(ratio,Pnt['p'])),'A=C p')
                    b.feq(m,b.fs(b.raw_fmul(aux,lam),g(Pnt,spec['g'][j+1])),'A H=G')
                    primary.append(b.fs(ratio,(b.P.v(0),b.P())))
                else:
                    role=('s','t','z')[j-1 if name=='q_compare4' else j]
                    Bs[role]=b.fvar(m,'normalized Lucas.B_'+role)
                    ps[role]=Pnt['p']
                    b.feq(m,b.fs(b.raw_fmul(Bs[role],lam),g(Pnt,spec['g'][j+1])),
                          'normalized Lucas B_'+role+' Lambda=G_'+role)
            if name!='q_compare_beta':
                Pn,U,V,Kc,E=[b.fvar(m,'normalized Lucas.'+label) for label in ('P','U','V','K','E')]
                one_minus_two_P=b.fs((b.P(1),b.P()),b.scale(Pn,2))
                b.feq(m,b.fs(b.raw_fmul(Pn,Bs['s']),ps['s']),'normalized Lucas P Bs=ps')
                b.feq(m,b.fs(b.raw_fmul(b.fa(U,V),ps['t']),b.raw_fmul(Pn,Bs['t'])),
                      'normalized Lucas (U+V)pt=P Bt')
                b.feq(m,b.fs(b.raw_fmul(Kc,ps['t']),b.raw_fmul(one_minus_two_P,Bs['t'])),
                      'normalized Lucas K pt=(1-2P)Bt')
                b.feq(m,b.fs(b.raw_fmul(V,ps['z']),b.raw_fmul(one_minus_two_P,Bs['z'])),
                      'normalized Lucas V pz=(1-2P)Bz')
                b.feq(m,b.fa(b.fa(b.fs(E,b.raw_fmul(U,U)),b.raw_fmul(Kc,V)),b.raw_fmul(Pn,Pn)),
                      'normalized Lucas E=U2-KV-P2')
                primary.append(E)
                evaluation=dict(B={role:[m.bind(x) for x in Bs[role]] for role in ('s','t','z')},
                    P=[m.bind(x) for x in Pn],U=[m.bind(x) for x in U],V=[m.bind(x) for x in V],
                    K=[m.bind(x) for x in Kc],E=[m.bind(x) for x in E],order=40,normalization=NORMALIZATION)
            fields=[Pnt['f'] for Pnt in points]+[fj]+primary+alternate
            if len(fields)!=len(spec['orders']):raise ValueError('Unexpected normalized field count')
            tests=b.field_tests(m,theta,error,fields)
            if len(tests)!=1+2*len(fields):raise ValueError('Unexpected field-test boundary')
            m.call(spec['batch'],[raw]+tests)
            metadata=dict(precision=spec['g'][0],label_precision=spec['g'][1],modeled_points=n,
                field_inequality_orders=spec['orders'][:],logarithm_coordinate='reciprocal f=1/x',
                compressed_primary_charts=True,high_log_profile=deepcopy(rational.LOW if spec['g'][0]==12 else rational.HIGH),
                beta_log_profile=deepcopy(rational.LOW if spec['g'][1]==12 else rational.HIGH),
                input_layout=spec['layout']+EXTRA_LAYOUT,difference_model=MODEL,
                primary_square_transfer=False,x_squareclass_membership=False,
                private_index_group='(1/2)Z via doubling',difference_formal_tests=False,
                rational_difference_four_fields=False,joint_primary_difference_chart=True,
                extra_target_start=base,local_lucas_residual=(name!='q_compare_beta'))
            if name=='q_compare_beta':
                metadata['local_lucas_evaluation']=None
            else:
                metadata.update(normalized_lucas_residual=True,normalized_lucas_evaluation=evaluation,
                                global_numerator_p_nonzero=False)
            metadata['global_lucas_proxy_inputs']=False
            m.save(**metadata)
    b.make_multi_comparison=comparison
    return dict(normalized_lucas_residual=True,proof_sha256=PROOF_SHA256,
                normalization=NORMALIZATION,source_pin_authorized=False,
                root_and_conic_unchanged=True,raw_coordinate_delta=-58,raw_residual_delta=-58)
