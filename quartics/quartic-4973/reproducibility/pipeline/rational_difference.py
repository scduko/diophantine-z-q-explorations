"""Four-field rational differences after the fixed three-mode installer.

New arithmetic source. Its acceptance requires the half-index proof, not
only a finite module audit. No frozen or published source is modified.
"""
from collections import Counter
from copy import deepcopy

COUNTS={'q_compare4':13,'q_compare_beta':8,'q_compare_lucas':16}
LAYOUTS={
    'q_compare4':'beta,s,t,z;Fq(P4);Fq(A4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r',
    'q_compare_beta':'beta;Fq(P4);Fq(A4);conj_fJ;inv_conj_zJ;root;root_error;r',
    'q_compare_lucas':'s,t,z;Fq(P4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r',
}
HIGH=dict(precision=40,scheme='block3',normalization='a6',hscale=1,bound_output=False)
LOW=dict(precision=12,scheme='direct',normalization='unit',hscale=1,bound_output=False)
MODES={
    'q_compare4':dict(n=4,batch='q_batch31',g=[40,12,40,40,40]),
    'q_compare_beta':dict(n=1,batch='q_batch13',g=[12,12]),
    'q_compare_lucas':dict(n=3,batch='q_batch25',g=[40]*4),
}
MODEL='rational difference on B*T!=0; fused alternate; no difference formal tests'


def field_orders(spec):return [1]*(spec['n']+2)+spec['g'][1:]+spec['g']
def rational_orders(spec):return [1]+[x for e in field_orders(spec) for x in (e,e)]


def install(b,combined,low,base_make_batch):
    """Call after beta_kernel.install, never after minimal_jacobi.install.

    base_make_batch is captured from the fresh archive builder BEFORE the
    combined/three-mode installer replaces b.make_batch.
    """
    if (b.PELL_PRECISION,b.ANCHOR_SQUARINGS,b.CURVE_DROOT,b.CURVE_D2)!=(40,25,(3,-1),(11,-6)):
        raise ValueError('Expected installed H19/root37/high40 three-mode source')
    if getattr(b,'_minimal_jacobi_installed',False) or getattr(b,'_rational_difference_installed',False):
        raise ValueError('Chart installer already applied')
    if getattr(base_make_batch,'__name__',None)!='make_batch' or base_make_batch.__globals__.get('M') is not b.M:
        raise ValueError('Expected the original archive batch constructor')
    b._rational_difference_installed=True
    previous_batch=b.make_batch

    def batch(name,orders,parity):
        if name=='q_batch41':
            if parity!='q_primeparity':raise ValueError('Unexpected parity module')
            base_make_batch('q_batch31',rational_orders(MODES['q_compare4']),parity)
        elif name=='q_height_batch':previous_batch(name,orders,parity)
        else:raise ValueError('Unexpected top-level batch')
    b.make_batch=batch

    def point(field,name):
        m=field.m
        f,x,p=[b.fvar(m,name+'.'+s) for s in ('f','x','p')]
        b.feq(m,b.fs(b.raw_fmul(p,p),b.fs(x,b.raw_fmul(field.D,f))),name+'.p2=x-Df')
        b.feq(m,b.fs(b.raw_fmul(x,f),(b.P(1),b.P())),name+'.xf=1')
        return dict(f=f,x=x,p=p)

    def difference(field,P,target,zji):
        m=field.m;F,q=target;f,p,x=P['f'],P['p'],P['x']
        t,M,T,A=[b.fvar(m,'rational difference.'+s) for s in ('t','M','T','A')]
        k=b.fs(q,p)
        b.feq(m,b.fs(t,b.raw_fmul(f,F)),'rational denominator product')
        B=b.fa((b.P(1),b.P()),b.raw_fmul(field.D,t))
        b.feq(m,b.fs(b.raw_fmul(M,B),p),'rational denominator quotient')
        rhs=b.fa(b.fs(b.scale(x,2),b.raw_fmul(p,q)),b.scale(b.raw_fmul(M,k),2))
        b.feq(m,b.fs(T,rhs),'rational T numerator')
        b.feq(m,b.fa(b.raw_fmul(A,field.conj(T)),b.raw_fmul(field.conj(k),zji)),
              'rational fused alternate')
        return A

    def comparison():
        for name,spec in MODES.items():
            n=spec['n'];at=5*n+4
            if name!='q_compare4':base_make_batch(spec['batch'],rational_orders(spec),'q_primeparity')
            m=b.M(name,5*n+11);field=b.Field(m)
            fj=(b.P.v(at),b.P.v(at+1));zji=(b.P.v(at+2),b.P.v(at+3))
            theta,error=b.P.v(at+4),b.P.v(at+5);raw=at+6
            points=[point(field,s) for s in ['H']+['X'+str(i) for i in range(n)]]
            targets=[((b.P.v(n+4*j),b.P.v(n+4*j+1)),
                      (b.P.v(n+4*j+2),b.P.v(n+4*j+3))) for j in range(n+1)]
            alternate=[difference(field,P,Q,zji) for P,Q in zip(points,targets)]
            def g(P,e):
                profile=LOW if e==12 else HIGH
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
            formal=[P['f'] for P in points]+[fj]
            tests=b.field_tests(m,theta,error,formal+primary+alternate)
            if len(tests)!=6*n+7:raise ValueError('Unexpected reduced test count')
            m.call(spec['batch'],[raw]+tests)
            m.save(precision=spec['g'][0],label_precision=spec['g'][1],modeled_points=n,
                   field_inequality_orders=field_orders(spec),logarithm_coordinate='reciprocal f=1/x',
                   compressed_primary_charts=True,high_log_profile=deepcopy(LOW if spec['g'][0]==12 else HIGH),
                   beta_log_profile=deepcopy(LOW if spec['g'][1]==12 else HIGH),input_layout=LAYOUTS[name],
                   difference_model=MODEL,primary_square_transfer=False,x_squareclass_membership=False,
                   private_index_group='(1/2)Z via doubling',difference_formal_tests=False,
                   rational_difference_four_fields=True)
    b.make_multi_comparison=comparison

    def forbidden_difference(*args,**kwargs):raise ValueError('Old difference constructor is forbidden')
    b.Field.difference=forbidden_difference

    # Keep the root construction byte-for-byte equivalent to minimal Jacobi.
    # Only the shared reciprocal/ordinate boundary is added to the old root.
    old_call=b.M.call
    def call(m,name,args,label=None):
        if name in ('q_compare_beta','q_compare_lucas'):
            raise ValueError('Root must select modes after recording all full calls')
        if name=='q_compare4':
            if m.name!='Z_definition' or len(args)!=31:raise ValueError('Unexpected root boundary')
            boundary=tuple(args[4:24])
            if not hasattr(m,'jacobi_targets'):
                m.jacobi_old_boundary=boundary;m.jacobi_targets=[];m.jacobi_call_count=0
                for j in range(5):
                    ids=boundary[4*j:4*j+4]
                    x=tuple(b.P.v(i) for i in ids[:2]);y=tuple(b.P.v(i) for i in ids[2:])
                    q,f=[b.fvar(m,'jacobi target '+str(j)+'.'+s) for s in ('p','f')]
                    b.feq(m,b.fs(b.raw_fmul(x,f),(b.P(1),b.P())),'jacobi target reciprocal')
                    b.feq(m,b.fs(b.raw_fmul(q,x),y),'jacobi target ordinate ratio')
                    m.jacobi_targets.append(dict(original=list(ids),p=[m.bind(a) for a in q],f=[m.bind(a) for a in f]))
            if boundary!=m.jacobi_old_boundary:raise ValueError('Root target boundary changed')
            m.jacobi_call_count+=1
            args=list(args[:4])+[i for t in m.jacobi_targets for key in ('f','p') for i in t[key]]+list(args[24:])
        return old_call(m,name,args,label)
    b.M.call=call
    old_save=b.M.save
    def save(m,**metadata):
        if m.name=='Z_definition':
            if m.jacobi_call_count!=37:raise ValueError('Expected exactly 37 contacts')
            metadata['jacobi_targets']=m.jacobi_targets
        return old_save(m,**metadata)
    b.M.save=save
    old_root=b.make_root
    def root():
        old_root();obj=b.MODULES['Z_definition']
        counts=Counter(call['module'] for call in obj['calls'] if call['module'] in MODES)
        if counts!=COUNTS:raise ValueError('Wrong three-mode dispatch counts')
        obj['jacobi_mode_counts']=dict(COUNTS);obj['jacobi_primary_pair_count']=145
        b.write('modules/Z_definition.json',obj)
    b.make_root=root
