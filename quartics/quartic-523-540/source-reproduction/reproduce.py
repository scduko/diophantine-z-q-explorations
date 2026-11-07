#!/usr/bin/env python3
"""Offline source replay for the 554/571 and 523/540 quartic packages."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def replay(work,node,packages=None):
 manifest=read(HERE/'MANIFEST.json')
 for rel,expected in manifest['sha256'].items():
  if sha(HERE/rel)!=expected:raise ValueError('Frozen bundle file changed: '+rel)
 odd=load('odd_chart_patch',HERE/'patches/odd_chart.py')
 product=load('product_patch',HERE/'patches/product_scales.py')
 scalar=load('scalar_patch',HERE/'patches/odd_scalar.py')
 asym=load('asymmetric_patch',HERE/'patches/asymmetric_depth.py')
 receipt={'status':'passed','offline':True,'variants':{}}
 variants=[('primary',False,'odd-product-source.cjs',561,'final554_571'),('asymmetric',True,'odd-product-asymmetric-source.cjs',532,'final523_540')]
 for name,is_asymmetric,frozen_builder,count,package in variants:
  d=work/name;d.mkdir(parents=True,exist_ok=True)
  source=(HERE/'builders/base833-source.cjs').read_text()
  if is_asymmetric:source=asym.patch(source)
  source=scalar.patch(product.patch(odd.patch(source)))
  if source.encode()!=(HERE/'builders'/frozen_builder).read_bytes():raise ValueError(name+': patch composition differs from frozen builder')
  (d/'build_source.cjs').write_text(source)
  shutil.copytree(HERE/'sources',d/'sources',dirs_exist_ok=True)
  with (d/'builder.log').open('w') as log:
   subprocess.run([node,str(d/'build_source.cjs')],check=True,stdout=log)
  with (d/'compiler.log').open('w') as log:
   subprocess.run([sys.executable,str(HERE/'tools/compile_ir.py'),str(d/'raw-translated-ir.json'),str(d/'compiled')],check=True,stdout=log)
  with (d/'checker.log').open('w') as log:
   subprocess.run([node,str(HERE/'tools/checker.cjs'),'--input',str(d/'raw-translated-ir.json'),'--compiled',str(d/'compiled/compiled-ir.json'),'--certificate',str(d/'compiled/reduction-certificate.json'),'--coordinate-map',str(d/'compiled/coordinate-map.json'),'--quartic',str(d/'compiled/polynomial.json'),'--report',str(d/'independent-check.json')],check=True,stdout=log)
  fresh=read(d/'compiled/compiled-ir.json');frozen=read(HERE/'expected'/f'source{count}.json')
  if set(fresh)!=set(frozen):raise ValueError(name+': compiled schema changed')
  for key in fresh:
   if key!='fixedParameter' and fresh[key]!=frozen[key]:raise ValueError(name+': compiled field changed: '+key)
  if fresh['fixedParameter']!={'name':'S','value':'3^(2^27)','coordinate':False}:raise ValueError('Unexpected historical parameter declaration')
  if frozen['fixedParameter']!={'name':'S','value':'3^(2^26)','coordinate':False}:raise ValueError('Unexpected final parameter declaration')
  if len(fresh['coordinates'])!=count:raise ValueError('Wrong coordinate count')
  check=read(d/'independent-check.json')
  result={'patchCompositionByteExact':True,'compiledFieldsMatchExceptDocumentedParameterMetadata':True,'coordinates':count,'residuals':len(fresh['residuals']),'gateIdentitiesChecked':check['gateIdentities']['checked'],'degree':check['statistics']['degree'],'monomials':check['statistics']['monomials'],'builderSha256':sha(d/'build_source.cjs'),'compiledPrecursorSha256':sha(d/'compiled/compiled-ir.json')}
  if packages is not None:
   final=packages/package
   if not (final/'verify_all.py').is_file():raise ValueError('Final package not found: '+str(final))
   if read(final/f'source{count}.json')!=frozen:raise ValueError('Sibling package source differs from pinned precursor')
   with (d/'final-package-verification.json').open('w') as log:
    subprocess.run([sys.executable,str(final/'verify_all.py')],check=True,cwd=final,stdout=log)
   result['finalPackageVerification']='passed'
  receipt['variants'][name]=result
  print(f'{name}: byte-exact patch composition; {count}-coordinate precursor; independent algebra checks passed.',flush=True)
 receipt['finalPackageVerification']='passed' if packages is not None else 'not requested; run with --packages PARENT_DIRECTORY for all four final quartics'
 (work/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
 return receipt

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--work',type=Path,help='Keep rebuilt artifacts in this directory; otherwise use a temporary directory.')
 ap.add_argument('--node',default=shutil.which('node'),help='Node executable (default: node on PATH).')
 ap.add_argument('--packages',type=Path,help='Parent directory containing final554_571 and final523_540; additionally verify all four final tables.')
 a=ap.parse_args()
 if not a.node:ap.error('Node is required; use --node PATH')
 packages=a.packages.resolve() if a.packages else None
 if a.work:
  work=a.work.resolve();work.mkdir(parents=True,exist_ok=True);replay(work,a.node,packages)
 else:
  with tempfile.TemporaryDirectory(prefix='h10-odd-product-replay-') as td:replay(Path(td),a.node,packages)
if __name__=='__main__':main()
