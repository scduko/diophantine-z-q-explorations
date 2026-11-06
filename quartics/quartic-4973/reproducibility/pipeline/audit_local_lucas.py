"""Independent local-Lucas, joint-chart and conic module specification.

The caller must pin the core auditor and the old high40 six-module source,
then check the contract, files, complete flattening and construction map.
This helper certifies only the exact module-level change described here.
"""
from collections import Counter,defaultdict
from copy import deepcopy

BETA_POSITIONS=list(range(5,13))
LUCAS_POSITIONS=list(range(13,21))+list(range(29,37))
FULL_POSITIONS=list(range(5))+list(range(21,29))
COUNTS={'q_compare4':13,'q_compare_beta':8,'q_compare_lucas':16}
HIGH=dict(precision=40,scheme='block3',normalization='a6',hscale=1,bound_output=False)
LOW=dict(precision=12,scheme='direct',normalization='unit',hscale=1,bound_output=False)
MODES={
    'q_compare4':dict(n=4,high=40,label=12,batch='q_conic13',g=[40,12,40,40,40],proxy_count=1,
        orders=[1]*6+[12,40]+[40,12,40,40,40],
        layout='beta;Fq(P4);Fq(A4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_beta':dict(n=1,high=12,label=12,batch='q_conic6',g=[12,12],proxy_count=1,
        orders=[1]*3+[12]*3,
        layout='beta;Fq(P4);Fq(A4);conj_fJ;inv_conj_zJ;root;root_error;r'),
    'q_compare_lucas':dict(n=3,high=40,label=40,batch='q_conic10',g=[40]*4,proxy_count=0,
        orders=[1]*5+[40]*5,
        layout='Fq(P4);Fq(S4);Fq(T4);Fq(Z4);conj_fJ;inv_conj_zJ;root;root_error;r'),
}
MODULES={'Z_definition','q_anchor','q_height_batch','q_primeparity',*MODES,
         'q_conic13','q_conic6','q_conic10'}
EXTRA_LAYOUT=';target_F_slots_are_J_over_conj_q;extra_targets[s,t,u]'
POLYNOMIAL='T^2-S*(S-2)*T*Z+(S-2)^2*Z^2-1'


def field_orders(spec):
    return list(spec['orders'])


def rational_orders(spec):
    return [1]+[e for order in field_orders(spec) for e in (order,order)]


def check_comparison(c,obj):
    assert obj['name'] in MODES,'Unknown comparison module'
    spec=MODES[obj['name']];n=spec['n'];start=spec['proxy_count'];first_j=start+4*(n+1)
    m=c.Module(obj,arithmetic_labels=('arithmetic','conic field coefficient'));expected=defaultdict(list)
    base=first_j+7
    assert m.free==base+6*(n+1) and obj['modeled_points']==n,'Mode dimensions'
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
    lucas=obj['name']!='q_compare_beta'
    assert obj['local_lucas_residual'] is lucas,'Local Lucas metadata'
    assert obj['global_lucas_proxy_inputs'] is False,'Global proxy metadata'
    def feq(tag,pair):
        for j,p in enumerate(pair):assert p;expected[tag+'.'+str(j)].append(p)
    points=[]
    for name in ['H']+['X'+str(i) for i in range(n)]:
        f,p=[m.pair(name+'.'+s) for s in ('f','p')]
        points.append(dict(f=f,p=p))
    alternate=[]
    zji=(c.v(first_j+2),c.v(first_j+3))
    for j,point in enumerate(points):
        at=start+4*j;r=(c.v(at),c.v(at+1));q=(c.v(at+2),c.v(at+3))
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
    ratios=[]
    for j in range(n):
        ratio=m.pair('retained logarithm ratio',j,n);aux=m.pair('ratio times p',j,n)
        feq('A=C p',c.fs(aux,c.fm(ratio,points[j+1]['p'])))
        feq('A H=G',c.fs(c.fm(aux,lam),gs[j+1]))
        ratios.append(ratio)
    primary=[];evaluation=None
    if start:
        primary.append(c.fs(ratios[0],(c.v(0),{})))
    if lucas:
        Cs,Ct,Cz=ratios[-3:]
        V,Dv,E=[m.pair('local Lucas.'+key) for key in ('V','D','E')]
        feq('local Lucas V=(Cs-2)Cz',c.fs(V,c.fm(c.fs(Cs,c.fc(c.ONE,2)),Cz)))
        feq('local Lucas D=CsCt-V',c.fa(c.fs(Dv,c.fm(Cs,Ct)),V))
        feq('local Lucas E=Ct2-VD-1',c.fa(c.fa(c.fs(E,c.fm(Ct,Ct)),c.fm(V,Dv)),c.ONE))
        primary.append(E)
        def pair_ids(pair):
            result=[]
            for value in pair:
                assert len(value)==1,'Evaluation coordinate shape'
                mon,coefficient=next(iter(value.items()))
                assert coefficient==1 and len(mon)==1,'Evaluation coordinate shape'
                result.append(mon[0])
            return result
        evaluation=dict(ratios=[pair_ids(pair) for pair in (Cs,Ct,Cz)],
                        V=pair_ids(V),D=pair_ids(Dv),E=pair_ids(E),order=40)
    assert obj['local_lucas_evaluation']==evaluation,'Local Lucas evaluation metadata'
    formal=[point['f'] for point in points]+[(c.v(first_j),c.v(first_j+1))]
    fields=formal+primary+alternate;factor=first_j+6
    tests=[part for pair in fields for part in pair]
    assert len(fields)==len(field_orders(spec)) and set(m.equations)-{'arithmetic','conic field coefficient'}==set(expected),'Core row labels'
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
                ordered_tests=len(tests),core_rows=sum(map(len,expected.values())),
                local_lucas_evaluation=lucas,global_proxy_inputs=start)


def check_root(c,obj,old):
    # Independently delete the old proxy layer FIRST, then construct the new
    # shared target layer and each final mode boundary directly. The producer
    # instead edits an already generated joint root and reindexes it afterward.
    calls=[call for call in old['calls'] if call['module']=='q_compare4']
    assert len(calls)==37 and old['free']==1,'Baseline root shape'
    assert not any(call['module'] in ('q_compare_beta','q_compare_lucas') for call in old['calls'])
    removed=[]
    for label in ('index proxy s','index proxy t','index proxy z'):
        ids=[i for kind,i,text in old['construction_log'] if kind=='variable' and text==label]
        assert len(ids)==1,'Baseline proxy declarations'
        removed.extend(ids)
    ids=[i for kind,i,label in old['construction_log']
         if kind=='equation' and label=='Lucas norm proxy certificate']
    assert len(ids)==1 and len(set(removed))==3,'Baseline proxy equation'
    deleted_row=ids[0];gone=set(removed);old_total=old['free']+old['locals']
    assert len(old['proxy_indices'])==4 and old['proxy_indices'][1:]==removed,'Baseline proxy metadata'
    S,T,Z=map(c.v,removed);two_less=c.add((1,S),(-2,c.const(1)))
    pell=c.add((1,c.power(T,2)),(-1,c.mul(c.mul(S,two_less),c.mul(T,Z))),
               (1,c.mul(c.power(two_less,2),c.power(Z,2))),(-1,c.const(1)))
    assert c.normal(c.decode(old['residuals'][deleted_row],old_total,26))==c.normal(pell),'Baseline proxy polynomial'
    for i,row in enumerate(old['residuals']):
        if i!=deleted_row:
            assert all(not gone.intersection(mon) for coefficient,mon in row),'Baseline proxy outside row'
    for call in old['calls']:
        if call['module']=='q_compare4':
            assert len(call['args'])==31 and call['args'][1:4]==removed,'Baseline proxy call slots'
            assert not gone.intersection(call['args'][:1]+call['args'][4:]),'Baseline proxy outside call'
        else:
            assert not gone.intersection(call['args']),'Baseline proxy outside call'
    def reindex(i):
        assert type(i) is int and i not in gone,'Deleted variable in retained content'
        return i-sum(j<i for j in removed) if i>=0 else i
    expected=deepcopy(old)
    expected['residuals']=[[[coefficient,[reindex(v) for v in mon]] for coefficient,mon in row]
                           for i,row in enumerate(old['residuals']) if i!=deleted_row]
    expected['construction_log']=[]
    for kind,i,label in old['construction_log']:
        assert kind in ('variable','equation'),'Baseline construction operation'
        if kind=='variable' and i not in gone:
            expected['construction_log'].append([kind,reindex(i),label])
        if kind=='equation' and i!=deleted_row:
            expected['construction_log'].append([kind,i-int(i>deleted_row),label])
    expected['proxy_indices']=[reindex(old['proxy_indices'][0])]
    expected['point_coordinates']={key:[reindex(i) for i in value] for key,value in old['point_coordinates'].items()}
    del expected['pell_equation']
    boundary=calls[0]['args'][4:24]
    assert len(boundary)==20 and all(call['args'][4:24]==boundary for call in calls),'Baseline shared target boundary'
    boundary=[reindex(i) for i in boundary]
    at=old_total-3;targets=[]
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
    jzi=calls[0]['args'][26:28]
    assert len(jzi)==2 and all(call['args'][26:28]==jzi for call in calls),'Baseline shared inverse'
    jzi=[reindex(i) for i in jzi]
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
    position=0;expected['calls']=[]
    for original in old['calls']:
        call=deepcopy(original)
        if call['module']!='q_compare4':
            call['args']=[reindex(i) for i in call['args']]
            expected['calls'].append(call)
            continue
        if position in BETA_POSITIONS:
            call['module']='q_compare_beta';chosen=[0,1]
        elif position in LUCAS_POSITIONS:
            call['module']='q_compare_lucas';chosen=[0,2,3,4]
        else:
            chosen=list(range(5))
        prefix=[reindex(original['args'][0])] if MODES[call['module']]['proxy_count'] else []
        call['args']=(prefix+[i for j in chosen for key in ('r','q') for i in extra[j][key]]
                      +[reindex(i) for i in original['args'][24:]]
                      +[i for j in chosen for key in ('s','t','u') for i in extra[j][key]])
        expected['calls'].append(call)
        position+=1
    assert position==37
    expected.update(locals=at-old['free'],jacobi_targets=targets,
        beta_only_positions=BETA_POSITIONS,lucas_only_positions=LUCAS_POSITIONS,
        full_comparison_positions=FULL_POSITIONS,jacobi_mode_counts=COUNTS,jacobi_primary_pair_count=145,
        joint_chart_targets=extra,joint_chart_extra_target_coordinates=40,
        local_lucas_residual=True,local_lucas_polynomial=POLYNOMIAL,
        retained_proxy_roles=['beta'],lucas_proxy_removal=dict(
            original_variables=removed,original_row=deleted_row,
            removed_input_slots={'q_compare4':[1,2,3],'q_compare_beta':[],'q_compare_lucas':[0,1,2]},
            variable_reindex='subtract number of removed original indices strictly below the index'))
    assert set(obj)==set(expected),'Root metadata fields'
    for key,value in expected.items():
        if key!='residuals':assert obj[key]==value,('Root field',key)
    assert len(obj['residuals'])==len(expected['residuals']),'Root row count'
    for i,(actual,wanted) in enumerate(zip(obj['residuals'],expected['residuals'])):
        assert c.normal(c.decode(actual,at,26))==c.normal(c.decode(wanted,at,26)),('Root equation',i)
    c.Module(obj,26,arithmetic_labels=())
    counts=Counter(call['module'] for call in obj['calls'] if call['module'] in MODES)
    assert counts==COUNTS and sum(counts[name]*(MODES[name]['n']+1) for name in counts)==145
    return dict(shared_target_coordinates=60,shared_target_rows=60,mode_counts=dict(counts),primary_pairs=145,
                removed_proxy_coordinates=removed,removed_proxy_row=deleted_row,field_tests=377,lucas_evaluations=29)


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
