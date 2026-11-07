"""Compare the upstream Laurent q40 circuit with a direct positive-power one.

This checks the 532-coordinate precursor only. The final nine-coordinate
elimination certificate is source-specific and is deliberately not reused.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'quartics/quartic-523-540/source-reproduction'
SOURCE=PKG/'builders/odd-product-asymmetric-source.cjs'
OLD=""" let em1=rquot('detector'+r+'.eMinus1',one,ep,'weight_nonzero'),
 em3=rquot('detector'+r+'.eMinus3',sq(em1),ep,'weight_nonzero'),
 em7=rquot('detector'+r+'.eMinus7',sq(em3),ep,'weight_nonzero'),
 em14=rsq('detector'+r+'.eMinus14',em7),
 em29=rquot('detector'+r+'.eMinus29',sq(em14),ep,'weight_nonzero'),
 em55=rquot('detector'+r+'.eMinus55',sq(em29),em3,'inverse_weight_power_nonzero');
 let q12=rquot('detector'+r+'.q12',mul(q1,em7),em29,'inverse_weight_power_nonzero'),
 q40=rquot('detector'+r+'.q40',mul(q12,ep),em55,'inverse_weight_power_nonzero');"""
NEW=""" let e2=rsq('detector'+r+'.e2',ep),
 e4=rsq('detector'+r+'.e4',e2),
 e8=rsq('detector'+r+'.e8',e4),
 e16=rsq('detector'+r+'.e16',e8),
 e32=rsq('detector'+r+'.e32',e16),
 e64=rsq('detector'+r+'.e64',e32),
 e80=rm('detector'+r+'.e80',e64,e16);
 let q40=rquot('detector'+r+'.q40',mul(q1,e80),e2,'norm_equation_forces_nonzero_weight');"""

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def run(out):
    out.mkdir(parents=True,exist_ok=False)
    source=SOURCE.read_text()
    if source.count(OLD)!=1: raise ValueError('upstream weight block changed')
    source=source.replace(OLD,NEW)
    builder=out/'build_source.cjs';builder.write_text(source)
    shutil.copytree(PKG/'sources',out/'sources')
    with (out/'builder.log').open('w') as log:
        subprocess.run(['node',str(builder)],check=True,stdout=log,stderr=subprocess.STDOUT)
    compiled=out/'compiled'
    with (out/'compiler.log').open('w') as log:
        subprocess.run([sys.executable,'-B',str(PKG/'tools/compile_ir.py'),
                        str(out/'raw-translated-ir.json'),str(compiled)],
                       check=True,stdout=log,stderr=subprocess.STDOUT)
    with (out/'checker.log').open('w') as log:
        subprocess.run(['node',str(PKG/'tools/checker.cjs'),
            '--input',str(out/'raw-translated-ir.json'),
            '--compiled',str(compiled/'compiled-ir.json'),
            '--certificate',str(compiled/'reduction-certificate.json'),
            '--coordinate-map',str(compiled/'coordinate-map.json'),
            '--quartic',str(compiled/'polynomial.json'),
            '--report',str(out/'independent-check.json')],
            check=True,stdout=log,stderr=subprocess.STDOUT)
    check=json.loads((out/'independent-check.json').read_text())
    compiled_ir=json.loads((compiled/'compiled-ir.json').read_text())
    result={'status':check['status'],
      'scope':'532-coordinate precursor; no final elimination claimed',
      'coordinates':check['statistics']['activeCoordinateCount'],
      'residuals':len(compiled_ir['residuals']),
      'monomials':check['statistics']['monomials'],
      'degree':check['statistics']['degree'],
      'builderSha256':sha(builder),
      'polynomialSha256':sha(compiled/'polynomial.json')}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();print(json.dumps(run(args.out.resolve()),indent=2))
