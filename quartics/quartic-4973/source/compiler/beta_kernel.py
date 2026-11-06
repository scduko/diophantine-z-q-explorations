"""Three-mode comparison source proposal; no arithmetic approval."""
POSITIONS=list(range(5,13))
SELECTION=[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30]
ORDERS=[1]*11+[12]*6
LUCAS_POSITIONS=list(range(13,21))+list(range(29,37))
LUCAS_SELECTION=[1,2,3,4,5,6,7]+list(range(12,31))
LUCAS_ORDERS=[1]*19+[40]*14
FULL_POSITIONS=list(range(5))+list(range(21,29))

def install(b,combined,low):
    make_batch=b.make_batch
    config=combined.install(b,low.emit_g,high=40,label=12)
    original_comparison=b.make_multi_comparison;original_root=b.make_root
    # Capture the underlying original batch constructor, before the combined
    # dispatch wrapper: its algebra is generic in an explicit order list.
    def comparison():
        original_comparison()
        make_batch('q_batch17',ORDERS,'q_primeparity')
        m=b.M('q_compare_beta',16);field=b.Field(m)
        target=lambda at:{'x':(b.P.v(at),b.P.v(at+1)),'y':(b.P.v(at+2),b.P.v(at+3))}
        points=[combined.comparison_point(b,field,s) for s in ('H','X0')]
        differences=[field.difference(point,target(at)) for point,at in zip(points,(1,5))]
        fj=(b.P.v(9),b.P.v(10));zji=(b.P.v(11),b.P.v(12));theta=b.P.v(13);error=b.P.v(14)
        formal=[field.f(point) for point in points]+[fj]+[field.conj(field.f(point)) for point in differences]
        G=lambda point:low.emit_g(b,field,point['f'],12,bind_output=False,hscale=1,scheme='direct',normalization='unit')
        lam=b.fvar(m,'common negative logarithm')
        b.feq(m,b.fs(b.raw_fmul(lam,points[0]['p']),G(points[0])),'H pH=GH')
        ratio=b.fvar(m,'retained logarithm ratio');aux=b.fvar(m,'ratio times p')
        b.feq(m,b.fs(aux,b.raw_fmul(ratio,points[1]['p'])),'A=C p')
        b.feq(m,b.fs(b.raw_fmul(aux,lam),G(points[1])),'A H=G')
        primary=[b.fs(ratio,(b.P.v(0),b.P()))]
        alternate=[field.mul(field.conj(field.z(point)),zji) for point in differences]
        tests=b.field_tests(m,theta,error,formal+primary+alternate)
        assert len(tests)==17
        m.call('q_batch17',[15]+tests)
        m.save(precision=12,label_precision=12,modeled_points=1,
               field_inequality_orders=[1]*5+[12]*3,logarithm_coordinate='reciprocal f=1/x',
               compressed_primary_charts=True,high_log_profile=dict(config['beta_log_profile']),
               beta_log_profile=dict(config['beta_log_profile']),
               input_layout='beta;4P;4A;conj_fJ;inv_conj_zJ;root;root_error;r')
        make_batch('q_batch33',LUCAS_ORDERS,'q_primeparity')
        m=b.M('q_compare_lucas',26);field=b.Field(m)
        points=[combined.comparison_point(b,field,s) for s in ('H','X0','X1','X2')]
        differences=[field.difference(point,target(at)) for point,at in zip(points,(3,7,11,15))]
        fj=(b.P.v(19),b.P.v(20));zji=(b.P.v(21),b.P.v(22));theta=b.P.v(23);error=b.P.v(24)
        formal=[field.f(point) for point in points]+[fj]+[field.conj(field.f(point)) for point in differences]
        G=lambda point:low.emit_g(b,field,point['f'],40,bind_output=False,hscale=1,scheme='block3',normalization='a6')
        lam=b.fvar(m,'common negative logarithm')
        b.feq(m,b.fs(b.raw_fmul(lam,points[0]['p']),G(points[0])),'H pH=GH')
        primary=[]
        for j in range(3):
            ratio=b.fvar(m,'retained logarithm ratio');aux=b.fvar(m,'ratio times p')
            b.feq(m,b.fs(aux,b.raw_fmul(ratio,points[j+1]['p'])),'A=C p')
            b.feq(m,b.fs(b.raw_fmul(aux,lam),G(points[j+1])),'A H=G')
            primary.append(b.fs(ratio,(b.P.v(j),b.P())))
        alternate=[field.mul(field.conj(field.z(point)),zji) for point in differences]
        tests=b.field_tests(m,theta,error,formal+primary+alternate);assert len(tests)==33
        m.call('q_batch33',[25]+tests)
        m.save(precision=40,label_precision=40,modeled_points=3,
               field_inequality_orders=[1]*9+[40]*7,logarithm_coordinate='reciprocal f=1/x',
               compressed_primary_charts=True,high_log_profile=dict(config['high_log_profile']),
               beta_log_profile=dict(config['high_log_profile']),
               input_layout='s,t,z;4P;4S;4T;4Z;conj_fJ;inv_conj_zJ;root;root_error;r')
    def root():
        original_root();module=b.MODULES['Z_definition'];position=0
        for call in module['calls']:
            if call['module']!='q_compare4':continue
            if position in POSITIONS:
                old=call['args'];assert len(old)==31
                call['module']='q_compare_beta';call['args']=[old[i] for i in SELECTION]
            elif position in LUCAS_POSITIONS:
                old=call['args'];assert len(old)==31
                call['module']='q_compare_lucas';call['args']=[old[i] for i in LUCAS_SELECTION]
            position+=1
        assert position==37
        module['beta_only_positions']=POSITIONS[:]
        module['lucas_only_positions']=LUCAS_POSITIONS[:]
        module['full_comparison_positions']=FULL_POSITIONS[:]
        b.write('modules/Z_definition.json',module)
    b.make_multi_comparison=comparison;b.make_root=root
    return config
