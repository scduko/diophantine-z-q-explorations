"""Independent joint f,p,A,K plus conic module audit; no producer imports.

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
EXTRA_LAYOUT=';target_F_slots_are_J_over_conj_q;extra_targets[s,t,u]'


def field_orders(spec):
    return [1]*(spec['n']+2)+spec['g'][1:]+spec['g']


def rational_orders(spec):
    return [1]+[e for order in field_orders(spec) for e in (order,order)]


def check_comparison(c,obj):
    assert obj['name'] in MODES,'Unknown comparison module'
    spec=MODES[obj['name']];n=spec['n'];first_j=5*n+4
    m=c.Module(obj,arithmetic_labels=('arithmetic','conic field coefficient'));expected=defaultdict(list)
    base=5*n+11
    assert m.free==11*n+17 and obj['modeled_points']==n,'Mode dimensions'
    assert obj['precision']==spec['high'] and obj['label_precision']==spec['label'],'Mode precisions'
    assert obj['input_layout']==spec['layout']+EXTRA_LAYOUT,'Mode boundary layout'
    assert obj['high_log_profile']==(LOW if spec['high']==12 else HIGH),'High G profile'
    assert obj['beta_log_profile']==(LOW if spec['label']==12 else HIGH),'Numerator G profile'
    assert obj['field_inequality_orders']==field_orders(spec),'Field orders'
    assert obj['compressed_primary_charts'] is True,'Primary chart metadata'
    assert obj['primary_square_transfer'] is False,'Square-transfer metadata'
    assert obj['x_squareclass_membership'] is False,'Membership metadata'
    assert obj['private_index_group']=='(1/2)Z via doubling','Index-group metadata'
    assert obj['difference_formal_tests'] is False,'Difference-test metadata'
    assert obj['rational_difference_four_fields'] is False,'Difference-chart metadata'
    assert obj['joint_primary_difference_chart'] is True,'Joint-chart metadata'
    assert obj['extra_target_start']==base,'Extra-target metadata'
    assert obj['logarithm_coordinate']=='reciprocal f=1/x'
    assert obj['difference_model']=='joint f,p,A,K curve and complete z graph; no difference formal tests','Difference-model metadata'
    assert obj['comparison_norm']=='private conic field norm v1','Comparison norm metadata'
    assert obj['conic_batch']==spec['batch'],'Conic batch metadata'
    assert obj['conic_legacy_input_count']==base,'Conic legacy input count'
    assert obj['ignored_shared_root_inputs']==[first_j+4,first_j+5],'Ignored root inputs'
    def feq(tag,pair):
        for j,p in enumerate(pair):assert p;expected[tag+'.'+str(j)].append(p)
    points=[]
    for name in ['H']+['X'+str(i) for i in range(n)]:
        f,p=[m.pair(name+'.'+s) for s in ('f','p')]
        points.append(dict(f=f,p=p))
    alternate=[]
    zji=(c.v(first_j+2),c.v(first_j+3))
    for j,point in enumerate(points):
        at=n+4*j;r=(c.v(at),c.v(at+1));q=(c.v(at+2),c.v(at+3))
        s=(c.v(base+6*j),c.v(base+6*j+1));t=(c.v(base+6*j+2),c.v(base+6*j+3))
        u=(c.v(base+6*j+4),c.v(base+6*j+5))
        A,K=[m.pair('joint chart.'+key,j,n+1) for key in ('A','K')]
        f=c.conj(point['f']);p=c.conj(point['p']);D=c.conj(c.D)
        feq('joint chart K=(A-r)p',c.fs(K,c.fm(c.fs(A,r),p)))
        feq('joint chart first relation',c.fs(c.fa(c.fm(K,p),c.fm(u,p)),
                                             c.fa(c.fc(c.fm(D,c.fm(r,f)),2),c.fc(c.fm(D,c.fm(t,A)),4))))
        feq('joint chart second relation',c.fa(c.fc(c.fm(D,c.fm(c.fa(A,r),f)),2),
                                              c.fa(c.fm(s,K),c.fa(c.fc(c.fm(D,c.fm(t,A)),4),c.fm(zji,c.conj(q))))))
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
    assert all(len(mon)<=1 for i in m.equations['conic field coefficient'] for mon in m.rows[i]),'Nonaffine field coefficient binding'
    old_roots={first_j+4,first_j+5}
    assert all(not (c.variables(value)&old_roots) for i,value in m.env.items() if i in m.definitions),'Old root dependency in comparison'
    assert all(not (c.variables(row)&old_roots) for row in m.rows),'Old root input in comparison row'
    for tag,polys in expected.items():
        ids=m.equations[tag];assert len(ids)==len(polys),('Core multiplicity',tag)
        for i,p in zip(ids,polys):
            assert c.normal(c.subst(m.rows[i],m.env))==c.normal(p),('Core equation',tag,i)
    assert len(obj['calls'])==1,'Comparison call count'
    call=obj['calls'][0]
    assert call['module']==spec['batch'] and len(call['args'])==len(tests)+1,'Comparison batch call'
    assert not set(call['args'])&old_roots,'Old root input in conic call'
    assert obj['conic_field_inputs']==[call['args'][i:i+2] for i in range(1,len(call['args']),2)],'Conic field input metadata'
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
    jzi=calls[0]['args'][26:28]
    assert len(jzi)==2 and all(call['args'][26:28]==jzi for call in calls),'Baseline shared inverse'
    jz=tuple(c.v(i) for i in jzi);extra=[]
    for j,target in enumerate(targets):
        ai=target['original'][:2];a=tuple(c.v(i) for i in ai)
        q=tuple(c.v(i) for i in target['p']);F=tuple(c.v(i) for i in target['f'])
        ri,r=allocate('joint chart target '+str(j)+'.r')
        si,s=allocate('joint chart target '+str(j)+'.s')
        ti,t=allocate('joint chart target '+str(j)+'.t')
        ui,u=allocate('joint chart target '+str(j)+'.u')
        feq('shared joint coefficient r',c.fs(c.fm(r,c.conj(q)),jz))
        feq('shared joint coefficient s',c.fs(c.fm(s,c.conj(q)),c.conj(c.fa(a,c.fm(c.D,F)))))
        feq('shared joint coefficient t',c.fs(c.fm(t,c.conj(c.fs(a,c.fm(c.D,F)))),c.ONE))
        feq('shared joint coefficient u',c.fs(u,c.fm(r,s)))
        extra.append(dict(q=target['p'],r=ri,s=si,t=ti,u=ui))
    position=0
    for call in expected['calls']:
        if call['module']!='q_compare4':continue
        call['args']=call['args'][:4]+new_boundary+call['args'][24:]
        if position in BETA_POSITIONS:
            call['module']='q_compare_beta';call['args']=[call['args'][i] for i in BETA_SELECTION]
        elif position in LUCAS_POSITIONS:
            call['module']='q_compare_lucas';call['args']=[call['args'][i] for i in LUCAS_SELECTION]
        chosen=([0,1] if position in BETA_POSITIONS else
                [0,2,3,4] if position in LUCAS_POSITIONS else list(range(5)))
        n=MODES[call['module']]['n']
        call['args'][n:n+4*(n+1)]=[i for j in chosen for key in ('r','q') for i in extra[j][key]]
        call['args'] += [i for j in chosen for key in ('s','t','u') for i in extra[j][key]]
        position+=1
    assert position==37
    expected.update(locals=at-old['free'],jacobi_targets=targets,
        beta_only_positions=BETA_POSITIONS,lucas_only_positions=LUCAS_POSITIONS,
        full_comparison_positions=FULL_POSITIONS,jacobi_mode_counts=COUNTS,jacobi_primary_pair_count=145,
        joint_chart_targets=extra,joint_chart_extra_target_coordinates=40)
    assert set(obj)==set(expected),'Root metadata fields'
    for key,value in expected.items():
        if key!='residuals':assert obj[key]==value,('Root field',key)
    assert len(obj['residuals'])==len(expected['residuals']),'Root row count'
    for i,(actual,wanted) in enumerate(zip(obj['residuals'],expected['residuals'])):
        assert c.normal(c.decode(actual,at,26))==c.normal(c.decode(wanted,at,26)),('Root equation',i)
    c.Module(obj,26,arithmetic_labels=())
    counts=Counter(call['module'] for call in obj['calls'] if call['module'] in MODES)
    assert counts==COUNTS and sum(counts[name]*(MODES[name]['n']+1) for name in counts)==145
    return dict(shared_target_coordinates=60,shared_target_rows=60,mode_counts=dict(counts),primary_pairs=145)


def check_modules(c,modules,old_modules,*,conic_batch_check,anchor_check=None):
    # Both callbacks must be independent checkers whose exact bytes are pinned
    # by the outer source auditor. No producer callback is permitted.
    assert callable(conic_batch_check),'Missing independent conic checker'
    assert set(modules)==MODULES,'Module set'
    assert set(old_modules)=={'Z_definition','q_anchor','q_height_batch','q_primeparity','q_compare4','q_batch41'},'Baseline module set'
    for name in ('q_height_batch','q_primeparity'):
        assert modules[name]==old_modules[name],('Changed retained module',name)
    if anchor_check is None:
        assert modules['q_anchor']==old_modules['q_anchor'],('Changed retained module','q_anchor')
        anchor_report={'status':'UNCHANGED PINNED ANCHOR'}
    else:
        assert callable(anchor_check),'Missing independent anchor checker'
        anchor_report=anchor_check(modules['q_anchor'])
    root=check_root(c,modules['Z_definition'],old_modules['Z_definition'])
    reports={name:check_comparison(c,modules[name]) for name in MODES}
    for name,spec in MODES.items():
        batch=deepcopy(modules[spec['batch']]);assert batch['name']==spec['batch']
        conic_batch_check(c,batch,field_orders(spec))
    for name in ('q_anchor','q_height_batch','q_primeparity'):c.Module(modules[name],26,arithmetic_labels=())
    return dict(root=root,comparisons=reports,anchor=anchor_report,arithmetic_acceptance=False,
                scope='All module equations and calls; caller must separately verify pins, contract and flattening')
