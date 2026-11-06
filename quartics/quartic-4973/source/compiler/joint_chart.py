"""Joint f,p,A,K curve/difference graph after the rational-difference installer.

This changes only the difference representation and shared target interface.
All tested field expressions and their orders remain unchanged.
"""
from copy import deepcopy

MODEL='joint f,p,A,K curve and complete z graph; no difference formal tests'
EXTRA_LAYOUT=';target_F_slots_are_J_over_conj_q;extra_targets[s,t,u]'
TARGET_INDICES={'q_compare4':[0,1,2,3,4],
                'q_compare_beta':[0,1],
                'q_compare_lucas':[0,2,3,4]}


def install(b,rational,low,base_make_batch):
    """Install after rational_difference.install, before any source generation."""
    if not getattr(b,'_rational_difference_installed',False):
        raise ValueError('The frozen rational-difference installer must run first')
    if getattr(b,'_joint_chart_installed',False) or getattr(b,'_two_denominator_installed',False):raise ValueError('Already installed')
    if rational.COUNTS!={'q_compare4':13,'q_compare_beta':8,'q_compare_lucas':16}:
        raise ValueError('Unexpected source modes')
    if getattr(base_make_batch,'__name__',None)!='make_batch' or base_make_batch.__globals__.get('M') is not b.M:
        raise ValueError('Expected the original archive batch constructor')
    b._joint_chart_installed=True

    def point(field,name):
        m=field.m;f,p=[b.fvar(m,name+'.'+s) for s in ('f','p')]
        return dict(f=f,p=p)

    def difference(field,P,r,q,s,t,u,jz):
        m=field.m;f=field.conj(P['f']);p=field.conj(P['p']);D=field.conj(field.D)
        A,K=[b.fvar(m,'joint chart.'+name) for name in ('A','K')]
        b.feq(m,b.fs(K,b.raw_fmul(b.fs(A,r),p)),'joint chart K=(A-r)p')
        DtA=b.raw_fmul(D,b.raw_fmul(t,A))
        e=b.fs(b.fa(b.raw_fmul(K,p),b.raw_fmul(u,p)),
               b.fa(b.scale(b.raw_fmul(D,b.raw_fmul(r,f)),2),b.scale(DtA,4)))
        b.feq(m,e,'joint chart first relation')
        e=b.fa(b.scale(b.raw_fmul(D,b.raw_fmul(b.fa(A,r),f)),2),
               b.fa(b.raw_fmul(s,K),b.fa(b.scale(DtA,4),b.raw_fmul(jz,field.conj(q)))))
        b.feq(m,e,'joint chart second relation')
        return A

    # The batch dispatcher belongs to the preceding frozen installer.
    # The supplied archive constructor emits just the two small batches;
    # no discarded old comparison body is generated.
    if not hasattr(rational,'rational_orders'):raise ValueError('Unexpected rational helper')

    def comparison():
        for name,spec in rational.MODES.items():
            n=spec['n'];base=5*n+11;at=5*n+4
            if name!='q_compare4':base_make_batch(spec['batch'],rational.rational_orders(spec),'q_primeparity')
            m=b.M(name,base+6*(n+1));field=b.Field(m)
            pair=lambda i:(b.P.v(i),b.P.v(i+1))
            fj=pair(at);jz=pair(at+2);theta=b.P.v(at+4);error=b.P.v(at+5);raw=at+6
            points=[point(field,s) for s in ['H']+['X'+str(i) for i in range(n)]]
            alternate=[difference(field,P,pair(n+4*j),pair(n+4*j+2),
                                  pair(base+6*j),pair(base+6*j+2),pair(base+6*j+4),jz)
                       for j,P in enumerate(points)]
            def g(P,e):
                profile=rational.LOW if e==12 else rational.HIGH
                return low.emit_g(b,field,P['f'],e,bind_output=False,hscale=1,
                                  scheme=profile['scheme'],normalization=profile['normalization'])
            lam=b.fvar(m,'common negative logarithm')
            b.feq(m,b.fs(b.raw_fmul(lam,points[0]['p']),g(points[0],spec['g'][0])),'H pH=GH')
            primary=[]
            for j,P in enumerate(points[1:]):
                ratio=b.fvar(m,'retained logarithm ratio');aux=b.fvar(m,'ratio times p')
                b.feq(m,b.fs(aux,b.raw_fmul(ratio,P['p'])),'A=C p')
                b.feq(m,b.fs(b.raw_fmul(aux,lam),g(P,spec['g'][j+1])),'A H=G')
                primary.append(b.fs(ratio,(b.P.v(j),b.P())))
            tests=b.field_tests(m,theta,error,[P['f'] for P in points]+[fj]+primary+alternate)
            if len(tests)!=6*n+7:raise ValueError('Unexpected retained test count')
            m.call(spec['batch'],[raw]+tests)
            m.save(precision=spec['g'][0],label_precision=spec['g'][1],modeled_points=n,
                   field_inequality_orders=rational.field_orders(spec),logarithm_coordinate='reciprocal f=1/x',
                   compressed_primary_charts=True,high_log_profile=deepcopy(rational.LOW if spec['g'][0]==12 else rational.HIGH),
                   beta_log_profile=deepcopy(rational.LOW if spec['g'][1]==12 else rational.HIGH),
                   input_layout=rational.LAYOUTS[name]+EXTRA_LAYOUT,difference_model=MODEL,
                   primary_square_transfer=False,x_squareclass_membership=False,
                   private_index_group='(1/2)Z via doubling',difference_formal_tests=False,
                   rational_difference_four_fields=False,joint_primary_difference_chart=True,
                   extra_target_start=base)
    b.make_multi_comparison=comparison

    # Expand root arguments only AFTER the existing 13/8/16 selector has run.
    # Its old 31/16/26 layouts must never be silently reinterpreted.
    captured={};old_save=b.M.save
    def save(m,**metadata):
        if m.name=='Z_definition':
            if 'root' in captured and captured['root'] is not m:raise ValueError('Multiple root objects')
            captured['root']=m
        return old_save(m,**metadata)
    b.M.save=save
    old_root=b.make_root
    def root():
        old_root();obj=b.MODULES['Z_definition'];m=captured['root']
        calls=[c for c in obj['calls'] if c['module'] in rational.MODES]
        if len(calls)!=37 or len(obj['jacobi_targets'])!=5:raise ValueError('Unexpected old root')
        full=next(c for c in calls if c['module']=='q_compare4');jzi=full['args'][26:28]
        jz=tuple(b.P.v(i) for i in jzi);D=tuple(b.P(i) for i in b.CURVE_D2)
        entries=[]
        for j,target in enumerate(obj['jacobi_targets']):
            ai=target['original'][:2];a=tuple(b.P.v(i) for i in ai)
            q=tuple(b.P.v(i) for i in target['p']);F=tuple(b.P.v(i) for i in target['f'])
            r,s,t,u=[b.fvar(m,'joint chart target '+str(j)+'.'+name) for name in ('r','s','t','u')]
            conj=lambda v:(v[0],-v[1])
            b.feq(m,b.fs(b.raw_fmul(r,conj(q)),jz),'shared joint coefficient r')
            b.feq(m,b.fs(b.raw_fmul(s,conj(q)),conj(b.fa(a,b.raw_fmul(D,F)))),'shared joint coefficient s')
            b.feq(m,b.fs(b.raw_fmul(t,conj(b.fs(a,b.raw_fmul(D,F)))),(b.P(1),b.P())),
                  'shared joint coefficient t')
            b.feq(m,b.fs(u,b.raw_fmul(r,s)),'shared joint coefficient u')
            entries.append(dict(q=target['p'],r=[m.bind(i) for i in r],s=[m.bind(i) for i in s],
                                t=[m.bind(i) for i in t],u=[m.bind(i) for i in u]))
        for call in calls:
            name=call['module'];n=rational.MODES[name]['n'];args=call['args'];base=5*n+11
            if len(args)!=base or args[5*n+6:5*n+8]!=jzi:raise ValueError('Unexpected selected boundary')
            chosen=TARGET_INDICES[name]
            expected=[i for j in chosen for key in ('f','p') for i in obj['jacobi_targets'][j][key]]
            if args[n:n+4*(n+1)]!=expected:raise ValueError('Selected target mapping changed')
            call['args'][n:n+4*(n+1)]=[i for j in chosen for key in ('r','q') for i in entries[j][key]]
            call['args']+= [i for j in chosen for key in ('s','t','u') for i in entries[j][key]]
        structural={'name','free','locals','residuals','calls','construction_log'}
        metadata={k:v for k,v in obj.items() if k not in structural}
        metadata['joint_chart_targets']=entries
        metadata['joint_chart_extra_target_coordinates']=40
        old_save(m,**metadata)
    b.make_root=root
