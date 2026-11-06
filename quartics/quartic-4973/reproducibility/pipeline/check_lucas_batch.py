"""Independent conic batch specification for local-Lucas orders.

Only the finite name registry changes from frozen conic checker 0358e595.
No producer import. The caller pins this file and the bounded core parser.
"""

def check_batch(c,obj,orders):
    """Reconstruct the conic, all powers, every leaf, and the literal-one tree."""
    orders=list(orders);count=len(orders)
    expected_names={13:'q_conic13',6:'q_conic6',10:'q_conic10'}
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
