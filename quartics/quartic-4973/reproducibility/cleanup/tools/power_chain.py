"""Replace the full conic's 11-node power chain by seven exact products.

With no --output this only checks current rows/incidence and reports plans.
An exporting run expands the SOS and belongs on the bounded remote worker.
"""
if not __debug__:
    raise RuntimeError('Assertions required')

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

import binding
import probe_localized as poly

CHAIN = [(2,1,1),(4,2,2),(8,4,4),(16,8,8),(24,16,8),(40,24,16),(80,40,40)]
TOOLS = {'export_artifact.py':'791c8e503407b2b58cbdb788785a952e2d6bc2720f34802ece2b0958cb07ccb4',
         'polynomial_ops.py':'fe325ee902ed3226da28277e4a70fd924a9628e40d5bea39451bba6c52a2b5c5'}


def plan(rows, old_ids, old_targets, powers, root, allocated):
    """Return an ordinary circuit event after checking every current use."""
    outputs = [powers[e] for e in (2,24,80)]
    selected=set(old_ids)
    assert len(old_ids)==len(old_targets)>7
    assert len(selected)==len(old_ids) and len(set(old_targets))==len(old_targets)
    for i,row in enumerate(rows):
        if i not in selected:
            assert not (poly.variables(row)&(set(old_targets)-set(outputs))), 'outside_use'
    env={1:root}; new_targets=[]; new_rows=[]; nextvar=allocated
    for exponent,left,right in CHAIN:
        target=powers[exponent] if exponent in (2,24,80) else nextvar
        if exponent not in (2,24,80):nextvar+=1
        product=tuple(sorted((env[left],env[right])))
        new_rows.append(poly.primitive({(target,):1,product:-1}))
        new_targets.append(target);env[exponent]=target
    patches={i:(new_rows[k] if k<len(new_rows) else {}) for k,i in enumerate(old_ids)}
    event=dict(kind='circuit',data=dict(old_rows=old_ids,old_targets=old_targets,
        outputs=outputs,new_targets=new_targets),patches=[[i,poly.enc(row)] for i,row in patches.items()])
    return event,patches,nextvar


def source_plans(adapter,entry,rows,allocated,conic_module):
    assert conic_module in ('q_conic13','q_conic15'), 'Unsupported full conic module'
    raw=(adapter/'construction-map.json').read_bytes()
    assert binding.hashlib.sha256(raw).hexdigest()==entry['construction_map_sha256']
    visits=json.loads(raw)['instantiations']
    relative='modules/'+conic_module+'.json'
    assert relative in entry['inspected_files_sha256'], 'Selected module is not source-pinned'
    binding.pinned(adapter/'source'/relative,entry['inspected_files_sha256'][relative])
    module=json.loads((adapter/'source'/relative).read_bytes())
    assert set(module['orders'])=={1,12,40}
    # The exponent metadata omits temporary even powers when rp(odd)
    # overwrites its dictionary entry. Include every labelled allocation,
    # then derive exponents again from the actual current definitions.
    local_targets={v for kind,v,label in module['construction_log']
                   if kind=='variable' and label=='shared conic contact power'}
    incidence=defaultdict(set); definitions=defaultdict(list)
    for i,row in enumerate(rows):
        for v in poly.variables(row):incidence[v].add(i)
        if len(row)!=2:continue
        for mon,c in row.items():
            if len(mon)!=1:continue
            target=mon[0]; other=next(m for m in row if m!=mon)
            if len(other)==2 and target not in other and row[other]==-c:
                definitions[target].append((i,other))
    plans=[];reasons=Counter()
    for visit in visits:
        if visit['module']!=conic_module:continue
        def gv(v):
            return visit['arguments'][v] if v<module['free'] else visit['first_local']+v-module['free']
        targets={gv(v) for v in local_targets if incidence[gv(v)]}
        if any(len(definitions[v])!=1 for v in targets):
            reasons['definition_changed']+=1;continue
        remaining=set(targets); exponents={gv(0):1}; old_ids=[];old_targets=[]
        while remaining:
            ready=sorted(v for v in remaining if set(definitions[v][0][1])<=exponents.keys())
            if not ready:break
            for v in ready:
                i,product=definitions[v][0]
                exponents[v]=sum(exponents[w] for w in product)
                old_ids.append(i);old_targets.append(v);remaining.remove(v)
        if remaining:
            reasons['nonpower_or_cyclic_definition']+=1;continue
        outputs={v for v in targets if incidence[v]-set(old_ids)}
        if len(outputs)!=3 or {exponents[v] for v in outputs}!={2,24,80}:
            reasons['outside_outputs_changed']+=1;continue
        powers={exponents[v]:v for v in outputs}
        if len(old_ids)<=7:
            reasons['already_short']+=1;continue
        try:event,patches,nextvar=plan(rows,old_ids,old_targets,powers,gv(0),allocated)
        except AssertionError as exc:
            reasons[str(exc)]+=1;continue
        plans.append((event,patches,nextvar,visit['path']))
        allocated=nextvar
    return plans,dict(reasons)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--artifact',type=Path,required=True)
    p.add_argument('--adapter',type=Path,required=True)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--expect-source-entry',required=True)
    p.add_argument('--expect-checker',required=True)
    p.add_argument('--expect-certificate',required=True)
    p.add_argument('--conic-module',required=True,choices=('q_conic13','q_conic15'))
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--output',type=Path)
    p.add_argument('--tools',type=Path)
    a=p.parse_args()
    entry,counts,verification=binding.inspect_inputs(a.artifact,a.adapter/'source-entry.json',a.checker,
        a.expect_source_entry,a.expect_checker,a.expect_certificate)
    assert verification['checker_sha256']==a.expect_checker, 'Use an endpoint replayed by this base checker'
    rows=[poly.dec(r) for r in json.loads(binding.ungzip(a.artifact/'candidate-rows.json.gz'))]
    records=[json.loads(line) for line in binding.ungzip(a.artifact/'certificate.jsonl.gz').splitlines()]
    allocated=records[-1]['allocated_variables']
    plans,reasons=source_plans(a.adapter,entry,rows,allocated,a.conic_module)
    report=dict(status='STRUCTURAL PLANS ONLY; no transformation or coefficient claim',
        conic_module=a.conic_module,
        source_id=entry['source_id'],baseline=counts,eligible=len(plans),
        potential_removals=sum(len(event['data']['old_targets'])-7 for event,_,_,_ in plans),
        reasons=reasons,paths=[path for _,_,_,path in plans])
    if a.output:
        assert a.tools and not a.output.exists()
        for name,expected in TOOLS.items():binding.pinned(a.tools/name,expected)
        sys.path.insert(0,str(a.tools.resolve()))
        from export_artifact import export
        import shutil
        total={}
        for row in rows:poly.add_to(total,poly.mul(row,row))
        assert max(map(abs,total.values()))<2**80
        accepted=[]; coefficient_rejections=0
        for event,patches,nextvar,path in plans:
            # Plans allocate consecutively. If one fails its coefficient
            # check, stop rather than leave a gap in fresh variable IDs.
            delta={}
            for i,row in patches.items():
                poly.add_to(delta,poly.mul(rows[i],rows[i]),-1)
                poly.add_to(delta,poly.mul(row,row))
            if any(abs(total.get(mon,0)+c)>=2**80 for mon,c in delta.items()):
                coefficient_rejections+=1;break
            poly.add_to(total,delta)
            for i,row in patches.items():rows[i]=row
            accepted.append(event);allocated=nextvar
        retained=[r for r in records if r['kind'] not in ('weights','final')]
        report['export']=export(a.output,a.artifact/'source-residuals.jsonl.gz',rows,
            retained+accepted,allocated,dict(conic_power_circuits=len(accepted)))
        shutil.copyfile(a.adapter/'source-entry.json',a.output/'source-entry.json')
        report.update(status='EXPORTED CANDIDATE; full independent replay required',
                      accepted=len(accepted),coefficient_rejections=coefficient_rejections)
    a.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
