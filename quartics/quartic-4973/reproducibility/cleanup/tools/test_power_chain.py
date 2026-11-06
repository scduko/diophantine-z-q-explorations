"""Tiny full-certificate test of the seven-node power replacement."""
if not __debug__:
    raise RuntimeError('Assertions required')

import argparse
import ast
from copy import deepcopy
import gzip
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

import binding
import power_chain
import probe_localized as poly


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--tools',type=Path,required=True)
    a=p.parse_args()
    binding.registry(a.checker)
    sys.path.insert(0,str(a.tools.resolve()))
    from export_artifact import export
    old_chain=[(2,1,1),(3,2,1),(6,3,3),(12,6,6),(24,12,12),
               (4,2,2),(5,4,1),(10,5,5),(20,10,10),(40,20,20),(80,40,40)]
    powers={1:0};rows=[]
    for target,(exponent,left,right) in enumerate(old_chain,1):
        rows.append(poly.primitive({(target,):1,tuple(sorted((powers[left],powers[right]))):-1}))
        powers[exponent]=target
    event,patches,nextvar=power_chain.plan(rows,list(range(11)),list(range(1,12)),powers,0,12)
    assert nextvar==16
    newrows=deepcopy(rows)
    for i,row in patches.items():newrows[i]=row
    with tempfile.TemporaryDirectory(prefix='tiny-power-') as tmp:
        root=Path(tmp)
        header=dict(witnesses=11,residuals=11,degree=4)
        source=binding.canonical(header)+b'\n'+b''.join(binding.canonical(poly.enc(r))+b'\n' for r in rows)
        source_path=root/'source.jsonl.gz';source_path.write_bytes(gzip.compress(source,mtime=0))
        entry=dict(source_id='synthetic-power-chain',source_sha256=binding.sha(source_path),
            source_variables=12,source_rows=11,source_header=header,
            uncompressed_sha256=binding.hashlib.sha256(source).hexdigest())
        text=a.checker.read_text();lines=text.splitlines(keepends=True)
        node,=[n for n in ast.parse(text).body if isinstance(n,ast.Assign)
            and any(isinstance(t,ast.Name) and t.id=='SOURCE_ENTRIES' for t in n.targets)]
        entries={'original64':binding.ORIGINAL64,entry['source_id']:entry}
        text=''.join(lines[:node.lineno-1]+['SOURCE_ENTRIES = '+repr(entries)+'\n']+lines[node.end_lineno:])
        checker=root/'checker.py';checker.write_text(text,newline='\n')
        spec=importlib.util.spec_from_file_location('tiny_power_checker',checker)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        initial=dict(kind='initial',source_id=entry['source_id'],
            source_entry_sha256=binding.hashlib.sha256(binding.canonical(entry)+b'\n').hexdigest(),
            source_sha256=entry['source_sha256'],source_variables=12,source_rows=11,
            reuse=[],gates=[],rows=[poly.enc(r) for r in rows])
        export(root/'baseline',source_path,rows,[initial],12,{})
        old=module.verify(root/'baseline',False)
        export(root/'candidate',source_path,newrows,[initial,event],nextvar,{})
        new=module.verify(root/'candidate',False)
        assert (old['variables'],new['variables'])==(12,8)
        certificate=root/'candidate/certificate.jsonl.gz'
        records=[json.loads(line) for line in gzip.decompress(certificate.read_bytes()).splitlines()]
        mutations=[]
        def add(name,fn):
            rr=deepcopy(records);fn(rr[1]);mutations.append((name,rr))
        add('wrong product',lambda e:e['patches'][3][1][0].__setitem__(0,2))
        add('missing output',lambda e:e['data']['outputs'].pop())
        add('duplicate old row',lambda e:e['data']['old_rows'].__setitem__(0,e['data']['old_rows'][1]))
        add('unfresh new coordinate',lambda e:e['data']['new_targets'].__setitem__(1,11))
        rejected=[]
        for name,rr in mutations:
            certificate.write_bytes(gzip.compress(b''.join(binding.canonical(r)+b'\n' for r in rr),mtime=0))
            try:module.verify(root/'candidate',False)
            except AssertionError:rejected.append(name)
            else:raise AssertionError('Accepted '+name)
        outside=deepcopy(rows)+[{(powers[3],):1,(0,):1}]
        try:power_chain.plan(outside,list(range(11)),list(range(1,12)),powers,0,12)
        except AssertionError:rejected.append('outside consumer')
        else:raise AssertionError('Outside consumer accepted')
        print(json.dumps(dict(status='PASS',old_variables=old['variables'],new_variables=new['variables'],
            full_checker_replays=2,malformed_rejected=len(rejected),cases=rejected,
            base_checker_sha256=binding.sha(a.checker))))


if __name__=='__main__':main()
