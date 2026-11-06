"""Independent rational-difference/conic module audit; no producer imports.

The caller must pin the core auditor and the old high40 six-module source,
then check the contract, files, complete flattening and construction map.
This helper certifies only the exact module-level change described here.
"""
from collections import Counter,defaultdict
from copy import deepcopy

BETA_POSITIONS=list(range(5,13))
LUCAS_POSITIONS=list(range(13,21))+list(range(29,37))
FULL_POSITIONS=list(range(5))+list(range(21,29))
BETA_SELECTION=[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30]
LUCAS_SELECTION=[1,2,3,4,5,6,7]+list(range(12,31))
COUNTS={'q_compare4':13,'q_compare_beta':8,'q_compare_lucas':16}
HIGH=dict(precision=40,scheme='block3',normalization='a6',hscale=1,bound_output=False)
LOW=dict(precision=12,scheme='direct',normalization='unit',hscale=1,bound_output=False)
MODES={
    'q_compare4':dict(n=4,high=40,label=12,batch='q_conic15',g=[40,12,40,40,40],
        layout='beta,s,t,z;Fq(P4);Fq(A4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_beta':dict(n=1,high=12,label=12,batch='q_conic6',g=[12,12],
        layout='beta;Fq(P4);Fq(A4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_lucas':dict(n=3,high=40,label=40,batch='q_conic12',g=[40]*4,
        layout='s,t,z;Fq(P4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
}
MODULES={'Z_definition','q_anchor','q_height_batch','q_primeparity',*MODES,
         'q_conic15','q_conic6','q_conic12'}


def field_orders(spec):
    return [1]*(spec['n']+2)+spec['g'][1:]+spec['g']


def rational_orders(spec):
    return [1]+[e for order in field_orders(spec) for e in (order,order)]


def check_comparison(c,obj):
    assert obj['name'] in MODES,'Unknown comparison module'
    spec=MODES[obj['name']];n=spec['n'];first_j=5*n+4
    m=c.Module(obj,arithmetic_labels=('arithmetic','conic field coefficient'));expected=defaultdict(list)
    assert m.free==5*n+11 and obj['modeled_points']==n,'Mode dimensions'
    assert obj['precision']==spec['high'] and obj['label_precision']==spec['label'],'Mode precisions'
    assert obj['input_layout']==spec['layout'],'Mode boundary layout'
    assert obj['high_log_profile']==(LOW if spec['high']==12 else HIGH),'High G profile'
    assert obj['beta_log_profile']==(LOW if spec['label']==12 else HIGH),'Numerator G profile'
    assert obj['field_inequality_orders']==field_orders(spec),'Field orders'
    assert obj['compressed_primary_charts'] is True,'Primary chart metadata'
    assert obj['primary_square_transfer'] is False,'Square-transfer metadata'
    assert obj['x_squareclass_membership'] is False,'Membership metadata'
    assert obj['private_index_group']=='(1/2)Z via doubling','Index-group metadata'
    assert obj['difference_formal_tests'] is False,'Difference-test metadata'
    assert obj['rational_difference_four_fields'] is True,'Difference-chart metadata'
    assert obj['logarithm_coordinate']=='reciprocal f=1/x'
    assert obj['difference_model']=='rational difference on B*T!=0; fused alternate; no difference formal tests','Difference-model metadata'
    assert obj['comparison_norm']=='private conic field norm v1','Comparison norm metadata'
    assert obj['conic_batch']==spec['batch'],'Conic batch metadata'
    assert obj['ignored_shared_root_inputs']==[m.free-3,m.free-2],'Ignored root inputs'
    def feq(tag,pair):
        for j,p in enumerate(pair):assert p;expected[tag+'.'+str(j)].append(p)
    points=[]
    for name in ['H']+['X'+str(i) for i in range(n)]:
        f,x,p=[m.pair(name+'.'+s) for s in ('f','x','p')]
        feq(name+'.p2=x-Df',c.fs(c.fm(p,p),c.fs(x,c.fm(c.D,f))))
        feq(name+'.xf=1',c.fs(c.fm(x,f),c.ONE))
        points.append(dict(f=f,x=x,p=p))
    alternate=[]
    zji=(c.v(first_j+2),c.v(first_j+3))
    for j,point in enumerate(points):
        at=n+4*j;FQ=(c.v(at),c.v(at+1));q=(c.v(at+2),c.v(at+3))
        t,M,T,A=[m.pair('rational difference.'+s,j,n+1) for s in ('t','M','T','A')]
        k=c.fs(q,point['p'])
        feq('rational denominator product',c.fs(t,c.fm(point['f'],FQ)))
        feq('rational denominator quotient',c.fs(c.fm(M,c.fa(c.ONE,c.fm(c.D,t))),point['p']))
        rhs=c.fa(c.fs(c.fc(point['x'],2),c.fm(point['p'],q)),c.fc(c.fm(M,k),2))
        feq('rational T numerator',c.fs(T,rhs))
        feq('rational fused alternate',c.fa(c.fm(A,c.conj(T)),c.fm(c.conj(k),zji)))
        alternate.append(A)
    gs=[c.expected_g(point['f'],e) for point,e in zip(points,spec['g'])]
    lam=m.pair('common negative logarithm')
    feq('H pH=GH',c.fs(c.fm(lam,points[0]['p']),gs[0]))
    primary=[]
    for j in range(n):
        ratio=m.pair('retained logarithm ratio',j,n);aux=m.pair('ratio times p',j,n)
        feq('A=C p',c.fs(aux,c.fm(ratio,points[j+1]['p'])))
        feq('A H=G',c.fs(c.fm(aux,lam),gs[j+1]))
        primary.append(c.fs(ratio,(c.v(j),{})))
    formal=[point['f'] for point in points]+[(c.v(first_j),c.v(first_j+1))]
    fields=formal+primary+alternate;factor=first_j+6
    tests=[part for pair in fields for part in pair]
    assert len(fields)==3*n+3 and set(m.equations)-{'arithmetic','conic field coefficient'}==set(expected),'Core row labels'
    assert all(len(mon)<=1 for i in m.equations['conic field coefficient'] for mon in m.rows[i]), 'Nonaffine field coefficient binding'
    old_roots={first_j+4,first_j+5}
    assert all(not (c.variables(value)&old_roots) for i,value in m.env.items() if i in m.definitions), 'Old root dependency in comparison'
    assert all(not (c.variables(row)&old_roots) for row in m.rows), 'Old root input in comparison row'
    for tag,polys in expected.items():
        ids=m.equations[tag];assert len(ids)==len(polys),('Core multiplicity',tag)
        for i,p in zip(ids,polys):
            assert c.normal(c.subst(m.rows[i],m.env))==c.normal(p),('Core equation',tag,i)
    assert len(obj['calls'])==1,'Comparison call count'
    call=obj['calls'][0]
    assert call['module']==spec['batch'] and len(call['args'])==len(tests)+1,'Comparison batch call'
    assert not set(call['args'])&old_roots,'Old root input in conic call'
    assert obj['conic_field_inputs']==[call['args'][i:i+2] for i in range(1,len(call['args']),2)], 'Conic field input metadata'
    for i,(actual,wanted) in enumerate(zip(call['args'],[c.v(factor)]+tests)):
        assert m.env[actual]==wanted,('Ordered argument',i)
    assert m.core|set(m.definitions)==set(range(m.free,m.total)),'Unaccounted local coordinates'
    assert not m.core&set(m.definitions),'Coordinate role collision'
    used=set().union(*(c.variables(row) for row in m.rows))
    assert set(range(m.free,m.total))<=used,'Unused local coordinates'
    return dict(primary_points=n+1,differences=n+1,free=m.free,locals=obj['locals'],
                ordered_tests=len(tests),core_rows=sum(map(len,expected.values())))


def check_root(c,obj,old):
    # old must be the hash-pinned high40 root with37 full comparison calls.
    expected=deepcopy(old);at=old['free']+old['locals'];targets=[]
    calls=[call for call in old['calls'] if call['module']=='q_compare4']
    assert len(calls)==37 and old['free']==1,'Baseline root shape'
    assert not any(call['module'] in ('q_compare_beta','q_compare_lucas') for call in old['calls'])
    boundary=calls[0]['args'][4:24]
    assert len(boundary)==20 and all(len(call['args'])==31 and call['args'][4:24]==boundary for call in calls),'Baseline shared target boundary'
    def allocate(label):
        nonlocal at
        ids=[at,at+1]
        for j,i in enumerate(ids):expected['construction_log'].append(['variable',i,label+'.'+str(j)])
        at+=2
        return ids,tuple(c.v(i) for i in ids)
    def feq(label,pair):
        for j,p in enumerate(pair):
            assert p
            expected['construction_log'].append(['equation',len(expected['residuals']),label+'.'+str(j)])
            expected['residuals'].append([[a,list(mon)] for mon,a in c.normal(p)])
    for j in range(5):
        ids=boundary[4*j:4*j+4];x=tuple(c.v(i) for i in ids[:2]);y=tuple(c.v(i) for i in ids[2:])
        qi,q=allocate('jacobi target '+str(j)+'.p');fi,f=allocate('jacobi target '+str(j)+'.f')
        feq('jacobi target reciprocal',c.fs(c.fm(x,f),c.ONE))
        feq('jacobi target ordinate ratio',c.fs(c.fm(q,x),y))
        targets.append(dict(original=ids,p=qi,f=fi))
    new_boundary=[i for t in targets for key in ('f','p') for i in t[key]]
    position=0
    for call in expected['calls']:
        if call['module']!='q_compare4':continue
        call['args']=call['args'][:4]+new_boundary+call['args'][24:]
        if position in BETA_POSITIONS:
            call['module']='q_compare_beta';call['args']=[call['args'][i] for i in BETA_SELECTION]
        elif position in LUCAS_POSITIONS:
            call['module']='q_compare_lucas';call['args']=[call['args'][i] for i in LUCAS_SELECTION]
        position+=1
    assert position==37
    expected.update(locals=at-old['free'],jacobi_targets=targets,
        beta_only_positions=BETA_POSITIONS,lucas_only_positions=LUCAS_POSITIONS,
        full_comparison_positions=FULL_POSITIONS,jacobi_mode_counts=COUNTS,jacobi_primary_pair_count=145)
    assert set(obj)==set(expected),'Root metadata fields'
    for key,value in expected.items():
        if key!='residuals':assert obj[key]==value,('Root field',key)
    assert len(obj['residuals'])==len(expected['residuals']),'Root row count'
    for i,(actual,wanted) in enumerate(zip(obj['residuals'],expected['residuals'])):
        assert c.normal(c.decode(actual,at,26))==c.normal(c.decode(wanted,at,26)),('Root equation',i)
    c.Module(obj,26,arithmetic_labels=())
    counts=Counter(call['module'] for call in obj['calls'] if call['module'] in MODES)
    assert counts==COUNTS and sum(counts[name]*(MODES[name]['n']+1) for name in counts)==145
    return dict(shared_target_coordinates=20,shared_target_rows=20,mode_counts=dict(counts),primary_pairs=145)


def check_modules(c,modules,old_modules,anchor_check=None):
    assert set(modules)==MODULES,'Module set'
    assert set(old_modules)=={'Z_definition','q_anchor','q_height_batch','q_primeparity','q_compare4','q_batch41'},'Baseline module set'
    for name in ('q_height_batch','q_primeparity'):
        assert modules[name]==old_modules[name],('Changed retained module',name)
    if anchor_check is None:
        assert modules['q_anchor']==old_modules['q_anchor'],('Changed retained module','q_anchor')
        anchor_report={'status':'UNCHANGED PINNED ANCHOR'}
    else:
        # The outer wrapper must pin this independent checker and record its
        # digest. No altered anchor is substituted into the old-module map.
        assert callable(anchor_check),'Anchor checker must be callable'
        anchor_report=anchor_check(modules['q_anchor'])
    root=check_root(c,modules['Z_definition'],old_modules['Z_definition'])
    reports={name:check_comparison(c,modules[name]) for name in MODES}
    for name,spec in MODES.items():
        batch=deepcopy(modules[spec['batch']]);assert batch['name']==spec['batch']
        check_batch(c,batch,field_orders(spec))
    for name in ('q_anchor','q_height_batch','q_primeparity'):c.Module(modules[name],26,arithmetic_labels=())
    return dict(root=root,comparisons=reports,anchor=anchor_report,arithmetic_acceptance=False,
                scope='All module equations and calls; caller must separately verify pins, contract and flattening')


def check_batch(c,obj,orders):
    """Reconstruct the conic, all powers, every leaf, and the literal-one tree."""
    orders=list(orders);count=len(orders)
    expected_names={15:'q_conic15',6:'q_conic6',12:'q_conic12'}
    assert count in expected_names and obj['name']==expected_names[count], 'Conic batch name'
    assert all(type(e) is int and 0<e<=40 for e in orders), 'Conic field orders'
    m=c.Module(obj,arithmetic_labels=('shared conic contact power',))
    assert m.free==1+2*count,'Conic input count'
    R=c.v(0);consumed=set(m.arithmetic)
    def coordinate(poly):
        assert len(poly)==1
        mon,coefficient=next(iter(poly.items()))
        assert coefficient==1 and len(mon)==1
        return mon[0]
    def check(tag,polys,maximum_degree):
        ids=m.equations[tag]
        assert len(ids)==len(polys),('Conic row multiplicity',tag)
        for i,p in zip(ids,polys):
            assert all(len(mon)<=maximum_degree for mon in m.rows[i]),('Conic row degree',tag,i)
            assert c.normal(c.subst(m.rows[i],m.env))==c.normal(p),('Conic equation',tag,i)
            consumed.add(i)
    theta=m.scalar('private conic theta');s=m.scalar('private conic s');S=m.scalar('private conic S')
    assert [coordinate(p) for p in (theta,s,S)]==[m.free,m.free+1,m.free+2], 'Private conic allocation'
    check('private conic square',[c.subst(c.add((1,S),(-1,c.mul(s,s))),m.env)],2)
    check('private conic discriminant',[c.add((1,c.mul(theta,theta)),(-1,c.mul(R,S)),(-2,c.const(1)))],2)
    assert m.equations['private conic square']==[0] and m.equations['private conic discriminant']==[1], 'Private conic row positions'

    # The cache and even-power targets are reconstructed from the schedule.
    # Intermediate square-then-multiply definitions are checked literally,
    # even when two emitted coordinates represent the same power.
    power_ids=m.labels['shared conic contact power'];power_number=0;power_cache={}
    powers={0:c.const(1),1:R}
    def allocate_power(rhs):
        nonlocal power_number
        key=tuple(sorted(rhs.items()))
        if key in power_cache:
            return power_cache[key]
        assert power_number<len(power_ids),'Missing conic power'
        target=c.v(power_ids[power_number]);power_number+=1
        i=m.definitions[coordinate(target)]
        assert all(len(mon)<=2 for mon in m.rows[i]),'Conic power degree'
        assert c.normal(m.rows[i])==c.normal(c.add((1,target),(-1,rhs))),('Conic power schedule',i)
        power_cache[key]=target
        return target
    def rp(exponent):
        if exponent not in powers:
            half=rp(exponent//2)
            powers[exponent]=allocate_power(c.mul(half,half))
            if exponent%2:
                powers[exponent]=allocate_power(c.mul(powers[exponent],R))
        return powers[exponent]

    indices=sorted(range(count),key=lambda i:(orders[i],i))
    nodes=[c.const(1)];plan=[dict(type='literal',value=1)];bindings=[]
    evaluations=[];norms=[]
    for number,index in enumerate(indices):
        a_id,b_id=1+2*index,2+2*index;A,B=c.v(a_id),c.v(b_id)
        Y=m.scalar('conic evaluation',number,count)
        W=m.scalar('conic packed field norm',number,count)
        assert coordinate(Y)<coordinate(W),'Conic field allocation'
        P=rp(2*orders[index])
        assert m.env[coordinate(P)]==c.power(R,2*orders[index]),'Conic even power'
        evaluations.append(c.add((1,Y),(-1,A),(-1,c.mul(theta,B))))
        norms.append(c.add((1,c.mul(c.power(R,2*orders[index]),W)),(-2,c.mul(A,Y)),
                           (1,c.mul(A,A)),(-2,c.mul(B,B))))
        record=dict(type='conic_field',field=index,order=orders[index],inputs=[a_id,b_id],
                    evaluation=coordinate(Y),norm=coordinate(W),power=coordinate(P))
        plan.append(record);bindings.append(dict(record));nodes.append(W)
    assert power_number==len(power_ids),'Extra conic power'
    assert all(len(value)==1 and next(iter(value.values()))==1 and set(next(iter(value)))<={0}
               for i,value in m.env.items() if i in m.definitions), 'Nonpower arithmetic in conic batch'
    check('conic evaluation',evaluations,2)
    check('conic packed field norm',norms,2)

    upper=[];levels=[];number=0
    while len(nodes)>1:
        levels.append(len(nodes));next_nodes=[]
        for i in range(0,len(nodes),2):
            if i+1==len(nodes):
                next_nodes.append(nodes[i]);continue
            left,right=nodes[i:i+2]
            out=m.scalar('cubic norm node',number,count);number+=1
            upper.append(c.add((1,out),(-1,c.mul(left,left)),(-1,c.mul(R,c.mul(right,right)))))
            next_nodes.append(out)
        nodes=next_nodes
    assert number==count,'Conic upper node count'
    check('cubic norm node',upper,3)
    square=m.scalar('batched square');argument=m.scalar('parity argument')
    check('batched square',[c.add((1,square),(-1,c.mul(nodes[0],nodes[0])))],2)
    check('parity argument',[c.add((1,argument),(-1,c.mul(R,square)))],2)
    assert obj['calls']==[{'module':'q_primeparity','args':[coordinate(argument)]}], 'Conic parity call'
    assert consumed==set(range(len(m.rows))),'Unconsumed conic rows'
    assert m.core|set(m.definitions)==set(range(m.free,m.total)),'Unaccounted conic coordinates'
    assert not m.core&set(m.definitions),'Conic coordinate role collision'

    expected=dict(orders=orders,field_inequality_orders=orders,norm_tree=plan,norm_level_sizes=levels,
        parity_module='q_primeparity',squareclass_correction=False,input_layout='r;A0;B0;A1;B1;...',
        comparison_norm='private conic field norm v1',
        conic_private=dict(theta=coordinate(theta),s=coordinate(s),square=coordinate(S)),conic_equations=[0,1],
        field_input_order=[[1+2*i,2+2*i] for i in range(count)],sorted_field_indices=indices,
        field_bindings=sorted(bindings,key=lambda item:item['field']),
        contact_powers=[dict(exponent=e,variable=coordinate(value)) for e,value in sorted(powers.items()) if e],
        norm_root=coordinate(nodes[0]),norm_root_square=coordinate(square),parity_argument=coordinate(argument),
        semantics='Private theta^2-r*s^2=2; packed eval_theta(F_i^2)/r^(2e_i); '
                  'upper N_r tree on literal1 and packed nodes; Psi(r*root^2)')
    core_keys={'name','free','locals','residuals','calls','construction_log'}
    assert set(obj)==set(expected)|core_keys,'Conic metadata keys'
    for key,value in expected.items():
        assert type(obj[key]) is type(value) and obj[key]==value,('Conic metadata',key)
    return dict(status='PASS: CONIC MODULE SPECIFICATION',fields=count,private_coordinates=3,
                powers=power_number,upper_nodes=number,root_error_leaf=False,contact_inverse=False)
