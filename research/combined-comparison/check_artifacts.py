"""Replay the selected 1267-variable artifact without regenerating all variants."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from verify_variants import check_chain, budgets, require

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    manifest=json.loads((HERE/'ARTIFACTS.json').read_text())
    pins=json.loads((HERE/'INPUTS.json').read_text())
    checker='quartics/quartic-1272/checker/checker.cjs'
    require(hashlib.sha256((ROOT/checker).read_bytes()).hexdigest()==pins['sha256'][checker], 'checker hash changed')
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)
        for name,entry in manifest['files'].items():
            z=(HERE/'artifacts'/(name+'.gz')).read_bytes()
            require(hashlib.sha256(z).hexdigest()==entry['gzipSha256'],'compressed hash mismatch')
            data=gzip.decompress(z)
            require(hashlib.sha256(data).hexdigest()==entry['sha256'],'uncompressed hash mismatch')
            (tmp/name).write_bytes(data)
        load=lambda name:json.loads((tmp/name).read_text())
        check_chain(load('parameter-source-ir.json'),load('source-ir.json'),26)
        budgets()
        table=load('ordinary-polynomial.json')
        require(table['schema']=='ordinary-integer-quartic-v1' and table['fixedParameter'] is None,'ordinary format mismatch')
        require(all(isinstance(t['coefficient'],str) and str(int(t['coefficient']))==t['coefficient'] for t in table['terms']),'noninteger coefficient')
        # Adapt metadata only to the unchanged upstream checker's input schema.
        table['schema']='brox-sparse-polynomial-v1'
        table['fixedParameter']='S = 3^(2^27)'
        for t in table['terms']:t['sPower']=0
        (tmp/'checker-table.json').write_text(json.dumps(table))
        r=subprocess.run(['node',str(ROOT/checker),'--input',str(tmp/'source-ir.json'),
            '--compiled',str(tmp/'compiled-ir.json'),'--certificate',str(tmp/'reduction-certificate.json'),
            '--coordinate-map',str(tmp/'coordinate-map.json'),'--quartic',str(tmp/'checker-table.json')],capture_output=True,text=True)
        require(r.returncode==0,r.stderr)
        result=json.loads(r.stdout)
        require(result['coordinates']==1267 and result['residuals']==1224 and result['monomials']==45480,'unexpected counts')
        require(result['degree']==4 and result['content']=='1','degree or content mismatch')
        bits=max(abs(int(t['coefficient'])).bit_length() for t in table['terms'])
        require(bits==4059,'coefficient bound mismatch')
        print(json.dumps({'status':'passed','coordinates':1267,'residuals':1224,'monomials':45480,
                          'degree':4,'primitiveContent':1,'maximumCoefficientBits':bits,
                          'chainProjectionCheck':'passed','independentChecker':result['status']}))

if __name__=='__main__':main()
