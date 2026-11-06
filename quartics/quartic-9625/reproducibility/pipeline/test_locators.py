"""Tiny synthetic mixed-module locator tests and pinned adapter syntax check.

No source generation, polynomial expansion, or candidate replay is performed.
The full independent certificate checker remains mandatory for every candidate.
"""
import argparse
import ast
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path

from adapt_absorb import adapt_mixed_absorb
from source_layout import MODULES, derive_layout, norm_row

BASE_ADAPTER='cabb72d21f1308925513003a7375d8b87f766328485d0dd554597dad32e77ed5'
BASE_PRODUCER='ba9f073a9b9628e9848ee54b7f6d4421785246ed711d9c117993de035d47c588'


def blank(name,free=1,locals=0,rows=0):
    return dict(name=name,free=free,locals=locals,residuals=[[] for _ in range(rows)],
                construction_log=[],calls=[])


def fixture():
    modules={name:blank(name) for name in MODULES}
    root=modules['Z_definition'];root['residuals']=[[[1,[0]]]]
    root['construction_log']=[['equation',0,'root error']]
    modules['q_primeparity']=blank('q_primeparity',1,7,4)
    for name,free,pairs in [('q_batch41',42,20),('q_batch17',18,8)]:
        m=blank(name,free,0,pairs);modules[name]=m
        m['norm_tree']=[dict(type='pair',tests=[2+2*i,3+2*i],order=1) for i in range(pairs)]
        m['construction_log']=[['equation',i,'fused normalized pair'] for i in range(pairs)]
    for name,batch,free,points in [('q_compare4','q_batch41',31,5),('q_compare_beta','q_batch17',16,2)]:
        m=blank(name,free,3*points,points);modules[name]=m
        m['calls']=[dict(module=batch,args=[0]*modules[batch]['free'])]
        for j in range(points):
            x,y,inverse=free+3*j,free+3*j+1,free+3*j+2
            m['construction_log'] += [['variable',x,f'P{j}.x.0'],['variable',y,f'P{j}.x.1'],
                ['variable',inverse,'distinct abscissae guard'],['equation',j,'distinct abscissae guard']]
            m['residuals'][j]=[[c,list(mon)] for mon,c in norm_row(inverse,(x,y),(4+4*j,5+4*j))]
    visits=[];next_local=100;next_row=0
    inventory=[('Z_definition',1),('q_anchor',1),('q_height_batch',1),('q_primeparity',38),
               ('q_compare4',29),('q_batch41',29),('q_compare_beta',8),('q_batch17',8)]
    for name,count in inventory:
        m=modules[name]
        for j in range(count):
            visits.append(dict(path=f'{name}/{j}',module=name,arguments=list(range(m['free'])),
                first_local=next_local,local_count=m['locals'],first_residual=next_row,
                residual_count=len(m['residuals'])))
            next_local+=m['locals'];next_row+=len(m['residuals'])
    return modules,visits


def reject(name,mutate,wanted):
    modules,visits=fixture();mutate(modules,visits)
    try:
        derive_layout(modules,visits)
    except AssertionError as error:
        reason=error.args[0] if error.args else None
        assert wanted(reason),(name,'wrong rejection',reason)
        return name
    raise AssertionError((name,'accepted malformed locator'))


def main():
    if not __debug__:raise RuntimeError('Assertions required')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base-adapter',type=Path,required=True)
    p.add_argument('--producer',type=Path,required=True)
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    for path in here.glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    assert hashlib.sha256(a.base_adapter.read_bytes()).hexdigest()==BASE_ADAPTER
    assert hashlib.sha256(a.producer.read_bytes()).hexdigest()==BASE_PRODUCER
    spec=importlib.util.spec_from_file_location('pinned_base_adapter',a.base_adapter)
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    adapted=adapt_mixed_absorb(base.adapt_producer('absorb_batch_error.py',a.producer.read_text()))
    tree=ast.parse(adapted)
    # Preserve the actual current-alias recursion and all incidence-closure code.
    before=base.adapt_producer('absorb_batch_error.py',a.producer.read_text())
    for start,end in [('    alias_values = {}; alias_order = []; alias_visiting = set()\n',
                      '    specs = []; pair_records = []; first = []; lows = {}; odds = {}; squares = {}\n'),
                     ('    # Delete only the largest closed private subset.',
                      "    event = {'kind': 'batch_absorb'")]:
        old=before[before.index(start):before.index(end)]
        new=adapted[adapted.index(start):adapted.index(end)]
        assert old==new,('Changed protected algebraic logic',start)
    assert sum(isinstance(node,ast.For) for node in ast.walk(tree))>10
    modules,visits=fixture();layout=derive_layout(modules,visits)
    assert layout['counts']==dict(comparisons=37,norm_guards=161,uncompressed_charts=0,
                                  parity=38,batches=37,batch_pairs=644)
    assert {b['module'] for b in layout['batches']}=={'q_batch41','q_batch17'}
    passed=[]
    def wrong_norm(m,v):m['q_compare_beta']['residuals'][0][0][0]*=-1
    passed.append(reject('altered beta norm',wrong_norm,lambda r:isinstance(r,tuple) and r[0]=='ambiguous norm locator'))
    def wrong_call(m,v):m['q_compare_beta']['calls'][0]['module']='q_batch41'
    passed.append(reject('wrong beta callee',wrong_call,lambda r:r is None))
    def missing_pair(m,v):m['q_batch17']['norm_tree'].pop()
    passed.append(reject('missing beta pair',missing_pair,lambda r:r is None))
    def wrong_free(m,v):m['q_batch17']['free']+=1
    passed.append(reject('wrong beta arity',wrong_free,lambda r:r is None))
    def duplicate_path(m,v):v[-1]['path']=v[-2]['path']
    passed.append(reject('duplicate path',duplicate_path,lambda r:r is None))
    def overlap(m,v):
        nonempty=[x for x in v if x['local_count']];nonempty[-1]['first_local']=nonempty[-2]['first_local']
    passed.append(reject('overlapping locals',overlap,lambda r:r=='overlapping instantiations'))
    def wrong_count(m,v):v[-1]['residual_count']+=1
    passed.append(reject('wrong row count',wrong_count,lambda r:r is None))
    print(json.dumps(dict(status='PASS',synthetic_counts=layout['counts'],malformed_cases=passed,
                         scope='Small locator/template checks; full source and certificate replay required')))


if __name__=='__main__':main()
