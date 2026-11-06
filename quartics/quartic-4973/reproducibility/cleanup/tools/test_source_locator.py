"""Tiny exact fixtures for the explicit full-conic module selector."""
if not __debug__:
    raise RuntimeError('Assertions required')

from copy import deepcopy
import json
from pathlib import Path
import tempfile

import binding
import power_chain
import probe_localized as poly


def main():
    chain=[(2,1,1),(3,2,1),(6,3,3),(12,6,6),(24,12,12),
           (4,2,2),(5,4,1),(10,5,5),(20,10,10),(40,20,20),(80,40,40)]
    powers={1:0};rows=[]
    for target,(exponent,left,right) in enumerate(chain,1):
        rows.append(poly.primitive({(target,):1,tuple(sorted((powers[left],powers[right]))):-1}))
        powers[exponent]=target
    rows += [{(powers[exponent],):1} for exponent in (2,24,80)]
    module=dict(free=1,orders=[1,12,40],construction_log=[
        ['variable',target,'shared conic contact power'] for target in range(1,12)])
    positives=[];rejected=[]
    with tempfile.TemporaryDirectory(prefix='tiny-conic-locator-') as tmp:
        root=Path(tmp);(root/'source/modules').mkdir(parents=True)
        for name in ('q_conic13','q_conic15'):
            relative='modules/'+name+'.json'
            path=root/'source'/relative
            path.write_bytes(binding.canonical(module)+b'\n')
            visits=dict(instantiations=[dict(module=name,arguments=[0],first_local=1,path='fixture')])
            mapfile=root/'construction-map.json';mapfile.write_bytes(binding.canonical(visits)+b'\n')
            entry=dict(construction_map_sha256=binding.sha(mapfile),
                       inspected_files_sha256={relative:binding.sha(path)})
            plans,reasons=power_chain.source_plans(root,entry,rows,12,name)
            assert len(plans)==1 and not reasons
            assert plans[0][0]['data']['outputs']==[powers[e] for e in (2,24,80)]
            positives.append(name)
            for label,change in (
                    ('module hash',lambda e:e['inspected_files_sha256'].__setitem__(relative,'0'*64)),
                    ('map hash',lambda e:e.__setitem__('construction_map_sha256','0'*64))):
                bad=deepcopy(entry);change(bad)
                try:power_chain.source_plans(root,bad,rows,12,name)
                except AssertionError:rejected.append(name+' '+label)
                else:raise AssertionError('Accepted '+label)
            other='q_conic15' if name=='q_conic13' else 'q_conic13'
            try:power_chain.source_plans(root,entry,rows,12,other)
            except AssertionError:rejected.append(name+' unpinned selection')
            else:raise AssertionError('Accepted unpinned selection')
            outside=deepcopy(rows)+[{(powers[3],):1}]
            plans,reasons=power_chain.source_plans(root,entry,outside,12,name)
            assert not plans and reasons=={'outside_outputs_changed':1}
            rejected.append(name+' outside consumer')
        try:power_chain.source_plans(root,entry,rows,12,'../q_conic13')
        except AssertionError:rejected.append('unsupported selector')
        else:raise AssertionError('Accepted unsupported selector')
    print(json.dumps(dict(status='PASS',positive_modules=positives,
                          malformed_rejected=len(rejected),cases=rejected)))


if __name__=='__main__':main()
