"""Mutation runner for a complete proposed source and independent check callback.

run_cases(modules, check) checks the valid source first. Its check callback must
include the entire independent source audit, including the restored parent.
Runtime/resource/deadline exceptions propagate; they never count as rejection.
"""
from copy import deepcopy

MODES={'q_compare4':('q_conic13',5,21),'q_compare_beta':('q_conic6',2,9),
       'q_compare_lucas':('q_conic10',4,16)}


def must_reject(name,check,modules):
    try:check(modules)
    except (AssertionError,ValueError):return name
    raise RuntimeError('Malformed source accepted: '+name)


def run_cases(modules,check):
    check(modules)
    passed=[]
    def test(name,mutator):
        bad=deepcopy(modules);mutator(bad);passed.append(must_reject(name,check,bad))
    root=modules['Z_definition'];C,D=root['shared_square_root']['square_pair']
    for row_offset in (-2,-1):
        test('root definition '+str(row_offset),lambda x,i=row_offset:x['Z_definition']['residuals'][i][0].__setitem__(0,7))
    test('root missing definition',lambda x:x['Z_definition']['residuals'].pop())
    test('root changed old row',lambda x:x['Z_definition']['residuals'][0][0].__setitem__(0,7))
    test('root hidden square use',lambda x:x['Z_definition']['residuals'][0].append([1,[C]]))
    test('root false occurrence count',lambda x:x['Z_definition']['shared_square_root'].__setitem__('occurrences',36))
    test('root swapped recorded square pair',lambda x:x['Z_definition']['shared_square_root']['square_pair'].reverse())
    test('root false equation record',lambda x:x['Z_definition']['shared_square_root']['equations'].__setitem__(0,0))
    test('root original-pair metadata only',lambda x:x['Z_definition']['shared_square_root']['original_pair'].__setitem__(0,0))
    test('root wrong log',lambda x:x['Z_definition']['construction_log'][-1].__setitem__(2,'wrong square'))
    test('root extra marker key',lambda x:x['Z_definition']['shared_square_root'].__setitem__('unchecked',1))
    test('root noninteger original coordinate',lambda x:x['Z_definition']['shared_square_root']['original_pair'].__setitem__(0,False))
    # Coherently change the proposed original field. Only the delegated parent
    # audit can establish that this is not the original conjugate fJ channel.
    def false_original(x):
        d=x['Z_definition'];A,B=d['shared_square_root']['original_pair'];A=0
        d['shared_square_root']['original_pair']=[A,B]
        rr=lambda terms:sorted(terms,key=lambda v:tuple(v[1]))
        d['residuals'][-2]=rr([[1,[C]],[-1,[A,A]],[-2,[B,B]]])
        d['residuals'][-1]=rr([[1,[D]],[-2,sorted([A,B])]])
    test('root coherent false original field',false_original)
    for comp,(batch,index,slot) in MODES.items():
        def wrong_call(x,name=comp,k=slot):
            call=next(c for c in x['Z_definition']['calls'] if c['module']==name)
            call['args'][k]=0
        test(comp+' one changed root call',wrong_call)
        def duplicate_use(x,name=comp,k=slot):
            call=next(c for c in x['Z_definition']['calls'] if c['module']==name)
            call['args'][0]=C
        test(comp+' repeated square call use',duplicate_use)
        test(comp+' old layout',lambda x,n=comp:x[n].__setitem__('input_layout',x[n]['input_layout'].replace('square_conj_fJ','conj_fJ')))
        test(comp+' residual slot capture',lambda x,n=comp,k=slot:x[n]['residuals'][0].append([1,[k]]))
        for key,value in [('field','wrong'),('field_index',index+1),('order',2),('input_type','ordinary field'),('input_slots',[0,1])]:
            test(comp+' marker '+key,lambda x,n=comp,k=key,v=value:x[n]['shared_square_input'].__setitem__(k,v))
        test(comp+' extra marker key',lambda x,n=comp:x[n]['shared_square_input'].__setitem__('unchecked',1))
        test(comp+' changed old core row',lambda x,n=comp:x[n]['residuals'][0][0].__setitem__(0,7))
        test(comp+' extra call',lambda x,n=comp,b=batch:x[n]['calls'].append({'module':b,'args':[0]}))
        m=modules[batch];ri=m['shared_square_input']['removed_equation']
        for key,value in [('field','wrong'),('field_index',index+1),('order',2),('input_type','ordinary field'),('input_slots',[0,1]),
                          ('removed_evaluation',0),('removed_equation',0)]:
            test(batch+' marker '+key,lambda x,n=batch,k=key,v=value:x[n]['shared_square_input'].__setitem__(k,v))
        test(batch+' noninteger deleted coordinate',lambda x,n=batch:x[n]['shared_square_input'].__setitem__('removed_evaluation',False))
        test(batch+' changed square row',lambda x,n=batch,i=ri:x[n]['residuals'][i][0].__setitem__(0,7))
        test(batch+' wrong theta',lambda x,n=batch:x[n]['conic_private'].__setitem__('theta',0))
        test(batch+' missing conic row',lambda x,n=batch:x[n]['residuals'].pop(0))
        test(batch+' extra row',lambda x,n=batch:x[n]['residuals'].append([[1,[0]]]))
        test(batch+' extra call',lambda x,n=batch:x[n]['calls'].append({'module':'q_primeparity','args':[0]}))
        test(batch+' changed old field row',lambda x,n=batch:x[n]['residuals'][2][0].__setitem__(0,7))
        test(batch+' changed local count',lambda x,n=batch:x[n].__setitem__('locals',x[n]['locals']+1))
        for collection in ('field_bindings','norm_tree'):
            def change_record(x,n=batch,col=collection,k=index):
                rec=next(r for r in x[n][col] if r.get('field')==k);rec['evaluation']=0
            test(batch+' restored-Y marker '+collection,change_record)
            def wrong_type(x,n=batch,col=collection,k=index):
                rec=next(r for r in x[n][col] if r.get('field')==k);rec['input_type']='ordinary field'
            test(batch+' wrong type '+collection,wrong_type)
        def coherent_wrong_power(x,n=batch,k=index,i=ri):
            d=x[n];rec=next(r for r in d['field_bindings'] if r['field']==k)
            oldp=rec['power'];rec['power']=0
            next(r for r in d['norm_tree'] if r.get('field')==k)['power']=0
            for term in d['residuals'][i]:term[1]=sorted(0 if v==oldp else v for v in term[1])
        test(batch+' coherent wrong power',coherent_wrong_power)
    return dict(status='PASS: full-source shared-square mutations',negative_count=len(passed),cases=passed)
