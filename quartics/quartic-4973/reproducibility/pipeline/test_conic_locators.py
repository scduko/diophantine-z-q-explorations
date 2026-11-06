"""Tiny conic locator fixtures; no source generation or certificate replay."""
if not __debug__:raise RuntimeError('Assertions required')
from source_layout import MODULES,COMPARISONS,BOUNDARIES,derive_layout


def blank(name,free=1,locals=0,rows=0):
    return dict(name=name,free=free,locals=locals,residuals=[[] for _ in range(rows)],
                construction_log=[],calls=[])


def fixture():
    modules={name:blank(name) for name in MODULES}
    modules['Z_definition']=blank('Z_definition',rows=1)
    modules['Z_definition']['construction_log']=[['equation',0,'root error']]
    modules['Z_definition'].update(chart='general_E_mixed',baseline_chart=10,comparison_target_multiplier=2,root_carrier='nontorsion E(K)',root_index_semantics='2Q=n_Q Pstar, n_Q integer',beta_comparison_scale=2,shared_square_root=dict(occurrences=37))
    modules['Z_definition'].update(root_doubling_model='direct tangent with retained square coordinates',direct_tangent_doublings=[dict(role=role) for role in ('A','S','T','Z')],direct_tangent_rewrite=dict(doublings=4,raw_variable_delta=-8,raw_row_delta=-8))
    modules['q_primeparity']=blank('q_primeparity',1,7,4)
    modules['q_linearnormalpole']=blank('q_linearnormalpole',3,10,8)
    for name,count in [('q_conic13',13),('q_conic6',6),('q_conic10',10)]:
        free=1+2*count;m=blank(name,free,3+2*count,3+count);modules[name]=m
        m.update(comparison_norm='private conic field norm v1',conic_equations=[0,1],
                 conic_private=dict(theta=free,s=free+1,square=free+2))
        m.update(norm_root=free+2+2*count,pole_inputs=[0,free,free+2+2*count])
        m['calls']=[dict(module='q_linearnormalpole',args=list(m['pole_inputs']))]
        m['norm_tree']=[dict(type='literal',value=1)]
        special={'q_conic13':5,'q_conic6':2,'q_conic10':4}[name]
        m['shared_square_input']=dict(field_index=special,order=1,input_type='pre-squared shared field')
        for i in range(count):
            m['norm_tree'].append(dict(type='conic_field',inputs=[1+2*i,2+2*i],
                                      evaluation=None if i==special else free+3+2*i,norm=free+4+2*i,order=1,field=i))
            if i==special:m['norm_tree'][-1]['input_type']='pre-squared shared field'
            m['construction_log'].append(['equation',2+i,'conic packed field norm'])
        first=m['norm_tree'][1];numerator=first['norm']
        first.update(type='conic_first_numerator',norm=None,numerator=numerator,power=0,virtual_denominator_exponent=1)
        m['first_norm_fusion']=dict(field=0,role='H.f',order=1,numerator=numerator,first_node=m['norm_root'],
            numerator_row=2,first_node_row=2+count,original_power=free+2,virtual_denominator=0,virtual_denominator_exponent=1)
        m['construction_log'][0][2]='first conic field numerator'
        m['construction_log'].append(['equation',2+count,'fused first norm node'])
    for name,(free,legacy) in BOUNDARIES.items():
        m=blank(name,free);modules[name]=m
        index,slot={'q_compare4':(5,21),'q_compare_beta':(2,9),'q_compare_lucas':(4,16)}[name]
        m.update(shared_square_input=dict(field='conj_fJ',input_slots=[slot,slot+1],field_index=index,order=1,input_type='pre-squared shared field'),root_index_semantics='2Q=n_Q Pstar, n_Q integer',comparison_target_multiplier=2,comparison_fixed_target='2R=Pstar')
        m.update(local_lucas_residual=name!='q_compare_beta',global_lucas_proxy_inputs=False)
        if name!='q_compare_beta':m.update(normalized_lucas_residual=True,global_numerator_p_nonzero=False)
        m.update(difference_model='joint f,p,A,K curve and complete z graph; no difference formal tests',
                 primary_square_transfer=False,x_squareclass_membership=False,difference_formal_tests=False,
                 rational_difference_four_fields=False,joint_primary_difference_chart=True,
                 conic_legacy_input_count=legacy,extra_target_start=legacy,private_index_group='(1/2)Z via doubling',
                 comparison_norm='private conic field norm v1',ignored_shared_root_inputs=[legacy-3,legacy-2])
        m['calls']=[dict(module=COMPARISONS[name],args=[legacy-1]+[0]*(modules[COMPARISONS[name]]['free']-1))]
    visits=[];local=100;row=0
    counts={'Z_definition':1,'q_anchor':1,'q_height_batch':1,'q_primeparity':1,'q_linearnormalpole':37,
            'q_compare4':13,'q_compare_beta':8,'q_compare_lucas':16,'q_conic13':13,'q_conic6':8,'q_conic10':16}
    for name in MODULES:
        m=modules[name]
        for i in range(counts[name]):
            visits.append(dict(path=name+'/'+str(i),module=name,arguments=list(range(m['free'])),
                               first_local=local,local_count=m['locals'],first_residual=row,
                               residual_count=len(m['residuals'])))
            local+=m['locals'];row+=len(m['residuals'])
    batches=[v for v in visits if v['module'] in COMPARISONS.values()]
    poles=[v for v in visits if v['module']=='q_linearnormalpole']
    for batch,pole in zip(batches,poles):
        m=modules[batch['module']]
        pole['arguments']=[0,batch['first_local'],batch['first_local']+m['norm_root']-m['free']]
    return modules,visits


def reject(name,mutation,message):
    modules,visits=fixture();mutation(modules,visits)
    try:derive_layout(modules,visits)
    except AssertionError as error:
        assert error.args==(message,),(name,error.args,message)
        return name
    raise AssertionError((name,'Mutation accepted'))


def main():
    modules,visits=fixture();counts=derive_layout(modules,visits)['counts']
    assert counts==dict(comparisons=37,norm_guards=0,uncompressed_charts=0,parity=1,
                        batches=37,batch_pairs=0,conic_fields=377,private_conics=37,conic_poles=37,conic_evaluations=340,conic_first_numerators=37,conic_norm_fields=340)
    cases=[]
    for name in COMPARISONS:
        for field in ('primary_square_transfer','x_squareclass_membership','difference_formal_tests',
                      'rational_difference_four_fields','joint_primary_difference_chart','private_index_group'):
            cases.append(reject(name+' missing '+field,lambda m,v,n=name,f=field:m[n].pop(f),
                                'Incomplete joint chart flags'))
        cases.append(reject(name+' wrong Lucas flag',lambda m,v,n=name:m[n].update(local_lucas_residual=n=='q_compare_beta'), 'Wrong local Lucas flag'))
        cases.append(reject(name+' old proxy inputs',lambda m,v,n=name:m[n].update(global_lucas_proxy_inputs=True), 'Old global Lucas proxy inputs'))
        if name=='q_compare_beta':
            cases.append(reject(name+' added normalized metadata',lambda m,v,n=name:m[n].update(normalized_lucas_residual=False), 'Changed beta normalization metadata'))
        else:
            cases.append(reject(name+' missing normalization',lambda m,v,n=name:m[n].pop('normalized_lucas_residual'), 'Missing normalized Lucas flag'))
            cases.append(reject(name+' false global numerator premise',lambda m,v,n=name:m[n].update(global_numerator_p_nonzero=True), 'Wrong global numerator scope'))
        cases.append(reject(name+' wrong model',lambda m,v,n=name:m[n].pop('comparison_norm'),
                            'Wrong conic comparison model'))
        def old_input(m,v,n=name):m[n]['calls'][0]['args'][1]=BOUNDARIES[n][1]-3
        cases.append(reject(name+' legacy root argument',old_input,'Legacy root input reaches conic batch'))
        def bad_arity(m,v,n=name):
            m[n]['free']+=1
            for inst in v:
                if inst['module']==n:inst['arguments'].append(0)
        cases.append(reject(name+' wrong enlarged arity',bad_arity,'Wrong joint comparison arity'))
        cases.append(reject(name+' wrong legacy count',lambda m,v,n=name:m[n].update(conic_legacy_input_count=m[n]['free']),
                            'Wrong joint legacy count'))
        cases.append(reject(name+' wrong extra target start',lambda m,v,n=name:m[n].update(extra_target_start=m[n]['free']),
                            'Wrong joint legacy count'))
        cases.append(reject(name+' enlarged-free ignored slots',lambda m,v,n=name:m[n].update(ignored_shared_root_inputs=[m[n]['free']-3,m[n]['free']-2]),
                            'Wrong ignored root slots'))
        def bad_raw(m,v,n=name):m[n]['calls'][0]['args'][0]=m[n]['free']-1
        cases.append(reject(name+' enlarged-free raw slot',bad_raw,'Wrong joint raw contact slot'))
    for name in COMPARISONS.values():
        cases.append(reject(name+' wrong model',lambda m,v,n=name:m[n].pop('comparison_norm'),
                            'Wrong conic batch model'))
        cases.append(reject(name+' missing literal',lambda m,v,n=name:m[n]['norm_tree'][0].update(value=0),
                            'Missing literal-one leaf'))
        cases.append(reject(name+' old pair node',lambda m,v,n=name:m[n]['norm_tree'][1].update(type='pair'),
                            'Wrong conic field nodes'))
        def alias(m,v,n=name):m[n]['conic_private']['s']=m[n]['conic_private']['theta']
        cases.append(reject(name+' private alias',alias,'Conic private coordinate alias'))
        def old_inverse(m,v,n=name):m[n]['construction_log'].append(['variable',m[n]['free'],'nonzero contact factor'])
        cases.append(reject(name+' old inverse',old_inverse,'Old inverse or error leaf in conic batch'))
    for name in COMPARISONS.values():
        for slot in range(3):
            def wrong(m,v,n=name,k=slot):m[n]['calls'][0]['args'][k]+=1
            cases.append(reject(name+' wrong pole slot '+str(slot),wrong,'Wrong conic pole boundary'))
    def wrong_visit(m,v):
        next(i for i in v if i['module']=='q_linearnormalpole')['arguments'][1]+=1
    cases.append(reject('wrong instantiated pole',wrong_visit,'Wrong instantiated pole inputs'))
    for label,key,value,message in [
        ('old root chart','chart',10,'Wrong general root chart'),
        ('old root carrier','root_carrier','2E(K)','Wrong root carrier'),
        ('old root index','root_index_semantics','old','Wrong root index semantics'),
        ('noninteger beta scale','beta_comparison_scale',2.0,'Wrong root beta scale'),
        ('missing root square','shared_square_root',{},'Missing shared root square')]:
        cases.append(reject(label,lambda m,v,k=key,x=value:m['Z_definition'].__setitem__(k,x),message))
    for name in COMPARISONS:
        cases.append(reject(name+' old root index',lambda m,v,n=name:m[n].update(root_index_semantics='old'),'Wrong comparison root index'))
        cases.append(reject(name+' old fixed target',lambda m,v,n=name:m[n].update(comparison_fixed_target='4Pstar'),'Wrong fixed target'))
        cases.append(reject(name+' boolean field order',lambda m,v,n=name:m[n]['shared_square_input'].update(order=True),'Wrong comparison square channel'))
    for name in COMPARISONS.values():
        cases.append(reject(name+' doubled shared order',lambda m,v,n=name:m[n]['shared_square_input'].update(order=2),'Wrong batch square channel'))
        cases.append(reject(name+' boolean shared order',lambda m,v,n=name:m[n]['shared_square_input'].update(order=True),'Wrong batch square channel'))
        def restored_eval(m,v,n=name):
            item=next(p for p in m[n]['norm_tree'] if p.get('input_type')=='pre-squared shared field');item['evaluation']=0
        cases.append(reject(name+' ordinary shared evaluation',restored_eval,'Wrong pre-squared field record'))
    cases.append(reject('old root target multiplier',lambda m,v:m['Z_definition'].update(comparison_target_multiplier=4),'Wrong root target multiplier'))
    for name in COMPARISONS:
        cases.append(reject(name+' old target multiplier',lambda m,v,n=name:m[n].update(comparison_target_multiplier=4),'Wrong comparison target multiplier'))
    cases.append(reject('missing tangent model',lambda m,v:m['Z_definition'].pop('root_doubling_model'),'Wrong direct tangent model'))
    cases.append(reject('missing tangent site',lambda m,v:m['Z_definition']['direct_tangent_doublings'].pop(),'Wrong direct tangent sites'))
    for key,value in [('doublings',3),('raw_variable_delta',-7),('raw_row_delta',-7),('doublings',4.0)]:
        cases.append(reject('wrong tangent '+key,lambda m,v,k=key,x=value:m['Z_definition']['direct_tangent_rewrite'].update({k:x}),'Wrong direct tangent rewrite'))
    for name in COMPARISONS.values():
        for key,value,message in [
            ('field',1,'Wrong first-norm meaning'),('role','other','Wrong first-norm meaning'),
            ('order',2,'Wrong first-norm meaning'),('order',True,'Wrong first-norm metadata'),
            ('virtual_denominator',1,'Wrong first-norm meaning'),
            ('virtual_denominator_exponent',2,'Wrong first-norm meaning'),
            ('first_node',0,'Wrong first-norm coordinates'),('numerator_row',-1,'Wrong first-norm rows')]:
            cases.append(reject(name+' bad first '+key,lambda m,v,n=name,k=key,x=value:m[n]['first_norm_fusion'].update({k:x}),message))
        for key,value in [('norm',0),('power',1),('order',2),('numerator',0),('virtual_denominator_exponent',2)]:
            cases.append(reject(name+' bad numerator '+key,lambda m,v,n=name,k=key,x=value:m[n]['norm_tree'][1].update({k:x}),'Wrong first numerator record'))
        cases.append(reject(name+' old first field type',lambda m,v,n=name:m[n]['norm_tree'][1].update(type='conic_field'),'Wrong conic field nodes'))
        cases.append(reject(name+' old first label',lambda m,v,n=name:m[n]['construction_log'][0].__setitem__(2,'conic packed field norm'),'Wrong first-norm labels'))
    assert len(cases)==153
    print(dict(status='PASS',counts=counts,negative_cases=cases))


if __name__=='__main__':main()
