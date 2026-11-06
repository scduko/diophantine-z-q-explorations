"""Bounded guard tests for source proxy removal; not an independent source audit."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

from local_lucas import remove_root_proxies, MODES


def load(path):
    spec=importlib.util.spec_from_file_location('proxy_removal_archive',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run(b, original):
    result=remove_root_proxies(b,original)
    assert result['locals']==original['locals']-3
    assert len(result['residuals'])==len(original['residuals'])-1
    assert result['proxy_indices']==[original['proxy_indices'][0]]
    assert 'pell_equation' not in result
    assert all(len(call['args'])==MODES[call['module']]['free']
               for call in result['calls'] if call['module'] in MODES)
    proxies=original['proxy_indices'][1:]
    equation=next(i for kind,i,label in original['construction_log']
                  if kind=='equation' and label=='Lucas norm proxy certificate')
    cases=[]
    def add(name,edit):
        value=deepcopy(original);edit(value);cases.append((name,value))
    add('unexpected-root-metadata',lambda m:m.update(unaccounted_variable_metadata=[proxies[0]]))
    add('wrong-proxy-equation',lambda m:m['residuals'][equation][0].__setitem__(0,99))
    add('outside-root-row-use',lambda m:m['residuals'].append([[1,[proxies[0]]]]))
    add('duplicate-proxy-variable',lambda m:m['construction_log'].append(['variable',proxies[0],'index proxy s']))
    add('duplicate-proxy-equation',lambda m:m['construction_log'].append(['equation',equation,'Lucas norm proxy certificate']))
    add('wrong-proxy-metadata',lambda m:m['proxy_indices'].__setitem__(1,0))
    add('retained-target-proxy-use',lambda m:m['joint_chart_targets'][0]['r'].__setitem__(0,proxies[0]))
    add('unknown-target-key',lambda m:m['jacobi_targets'][0].update(extra=[proxies[0]]))
    def auxiliary(m):
        call=next(c for c in m['calls'] if c['module']=='q_anchor');call['args'][0]=proxies[0]
    add('outside-call-use',auxiliary)
    def wrongslot(m):
        call=next(c for c in m['calls'] if c['module']=='q_compare4');call['args'][1]=0
    add('wrong-comparison-proxy-slot',wrongslot)
    def leaked(m):
        call=next(c for c in m['calls'] if c['module']=='q_compare4');call['args'][-1]=proxies[0]
    add('outside-comparison-slot-use',leaked)
    def count(m):
        at=next(i for i,c in enumerate(m['calls']) if c['module']=='q_compare4');m['calls'].pop(at)
    add('wrong-comparison-count',count)
    rejected=[]
    for name,value in cases:
        try:remove_root_proxies(b,value)
        except ValueError:rejected.append(name)
        else:raise AssertionError('Guard accepted '+name)
    assert len(rejected)==12 and len(set(rejected))==12
    return dict(status='PASS: PRODUCER GUARDS ONLY',count=12,rejected=rejected,
                removed_variables=proxies,removed_row=equation)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--builder',type=Path,required=True)
    p.add_argument('--joint-root',type=Path,required=True)
    p.add_argument('--out',type=Path)
    a=p.parse_args();report=run(load(a.builder),json.loads(a.joint_root.read_bytes()))
    text=json.dumps(report,sort_keys=True,indent=2)+'\n'
    if a.out:a.out.write_text(text,encoding='utf-8')
    print(text,end='')


if __name__=='__main__':main()
