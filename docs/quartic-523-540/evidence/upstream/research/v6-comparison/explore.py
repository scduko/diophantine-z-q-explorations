"""Additive Version 6 experiments; see README.md for arithmetic scope."""
import argparse, importlib.util, json, shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/combined-comparison'))
# This module has the same basename; load the historical helpers explicitly.
spec=importlib.util.spec_from_file_location('historical_explore',ROOT/'research/combined-comparison/explore.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
PACKAGE=ROOT/'quartics/quartic-962'
def variant(s,level):
 if level>=1:
  s=h.replace_once(s,"let four={P:double('P4',double('P2',P))};for(let n of ['A','S','T','Z'])four[n]=double(n+'4',double(n+'2',points[n]));","let four={P:double('P2',P)};for(let n of ['A','S','T','Z'])four[n]=double(n+'2',points[n]);")
  s=h.replace_once(s,"start('fourfold_roots',[2394,2399]);","start('doubled_targets',[2394,2399]);")
 if level>=2:
  s=h.replace_once(s,"let di=inv('detector'+r+'.deltaInverse',delta),Ad=","let Ad=")
  s=h.replace_once(s,"let q1=rquot('detector'+r+'.q1',mul(ep,rsq('detector'+r+'.deltaInverse2',di)),delta,'retained_deltaInverse');","let delta2=rsq('detector'+r+'.delta2',delta),delta3=rm('detector'+r+'.delta3',delta2,delta),q1=rquot('detector'+r+'.q1',ep,delta3,'norm_equation_forces_nonzero_delta');")
  s=h.replace_once(s,"bv=rm('detector'+r+'.B',nw,rquot('detector'+r+'.Rnorm',mul(di,nw),ep,'positive_scale_weight_enforces_nonzero_ep'));","eDelta=rm('detector'+r+'.eDelta',ep,delta),bv=rquot('detector'+r+'.B',sq(nw),eDelta,'retained_w0_inverse_and_nonsquare_two_force_nonzero_norm');")
  s=s.replace('positive_scale_and_deltaInverse_make_numerator_nonzero','positive_scale_and_norm_equation_make_numerator_nonzero')
 if level>=3:
  # Keep the high-order log polynomial; reduce only the low-order tests to 12.
  s=s.replace('i===1?16:52','i===1?12:52').replace('order:16},{value:FF','order:12},{value:FF').replace('[1,16,52]','[1,12,52]')
  s=h.replace_once(s,"let w2=fsq(name+'.wPower2',w),rawout=rawPolynomial6(aCoeffs.slice(0,4),[fc(1),w,w2,rawFmul(w2,w)]);","let rawout=fadd(fadd(fc(aCoeffs[0]),fscale(w,aCoeffs[1])),fscale(rawFmul(w,w),aCoeffs[2]));")
  start=s.index(" let e2=rsq('detector'+r+'.e2'");end=s.index(" let wi=inv('detector'+r+'.w0Inverse'",start)
  # Joint chain for e^22,e^102 with shared e^6; eleven multiplications including weights.
  s=s[:start]+""" let e2=rsq('detector'+r+'.e2',ep),e4=rsq('detector'+r+'.e4',e2),e6=rm('detector'+r+'.e6',e4,e2),e8=rsq('detector'+r+'.e8',e4),e16=rsq('detector'+r+'.e16',e8),e32=rsq('detector'+r+'.e32',e16),e48=rm('detector'+r+'.e48',e32,e16),e96=rsq('detector'+r+'.e96',e48);
 let common=rm('detector'+r+'.q1e6',q1,e6),q12=rm('detector'+r+'.q12',common,e16),q52=rm('detector'+r+'.q52',common,e96);
 let w=fmul('detector'+r+'.W',fmul('detector'+r+'.Wfirst',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E12',coeffs[12],q12)),evalSym('detector'+r+'.E52',coeffs[52],q52));
"""+s[end:]
 if level>=4:
  a=s.index('let squareQ=');b=s.index('function log(',a);s=s[:a]+s[b:]
  s=s.replace('j<=12;j++','j<=9;j++').replace('// Exact degree-12 square completion, requiring four field assignments.','// Field polynomial helpers for the degree-nine block circuit.')
  s=s.replace('i===1?12:52','i===1?12:40').replace('order:52','order:40').replace('[1,12,52]','[1,12,40]')
  start=s.index(' if(e===52){');end=s.index(' let rawout=fadd(fadd(fc(aCoeffs[0])',start)
  s=s[:start]+""" if(e===40){
  let w2=fsq(name+'.wPower2',w),w3=fmul(name+'.wPower3',w2,w);
  let basis=[fc(1),w,w2];
  function block(k){let out=fc(0);for(let j=0;j<3;j++)out=fadd(out,fscale(basis[j],aCoeffs[k+j]));return out;}
  let inner=fadd(block(6),fscale(w3,aCoeffs[9]));
  let midraw=fadd(block(3),rawFmul(w3,inner)),mid=midraw.map((v,j)=>assign(name+'.middle.'+j,v));
  let outraw=fadd(block(0),rawFmul(w3,mid)),out=outraw.map((v,j)=>assign(name+'.polynomial.'+j,v));
  return p.z?fmul(name,p.z,out):fquot(name,[scale(add(mul(p.point.x[0],out[0]),scale(mul(p.point.x[1],out[1]),2)),-1),scale(add(mul(p.point.x[0],out[1]),mul(p.point.x[1],out[0])),-1)],p.point.y,'finite_double_or_difference_nonzero_y_Brox4311_4348');
 }
"""+s[end:]
  start=s.index(" let e2=rsq('detector'+r+'.e2'");end=s.index(" let wi=inv('detector'+r+'.w0Inverse'",start)
  s=s[:start]+""" let e2=rsq('detector'+r+'.e2',ep),e4=rsq('detector'+r+'.e4',e2),e8=rsq('detector'+r+'.e8',e4),e16=rsq('detector'+r+'.e16',e8),e24=rm('detector'+r+'.e24',e16,e8),e40=rm('detector'+r+'.e40',e24,e16),e80=rsq('detector'+r+'.e80',e40);
 let q12=rquot('detector'+r+'.q12',mul(q1,e24),e2,'norm_equation_forces_nonzero_weight'),q40=rquot('detector'+r+'.q40',mul(q1,e80),e2,'norm_equation_forces_nonzero_weight');
 let w=fmul('detector'+r+'.W',fmul('detector'+r+'.Wfirst',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E12',coeffs[12],q12)),evalSym('detector'+r+'.E40',coeffs[40],q40));
"""+s[end:]
 return s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',type=int);a=ap.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 pins=json.loads((Path(__file__).parent/'INPUTS.json').read_text())
 for path,sha in pins['sha256'].items():
  if h.digest(ROOT/path)!=sha:raise ValueError('Pinned input changed: '+path)
 spec=importlib.util.spec_from_file_location('compiler',PACKAGE/'compiler/compile_ir.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
 summary={'upstreamCommit':'f87226569fa7ceeae0c783c3e4d1241ac727733a','variants':{}}
 for level,name in enumerate(['ordinary','target_two','quotient','low_precision','precision40_quotients']):
  if a.only is not None and level!=a.only:continue
  d=out/name;d.mkdir();(d/'sources').mkdir();shutil.copyfile(PACKAGE/'sources/diophantine_optimization_20261106_v3.tex',d/'sources/diophantine_optimization_20261106_v3.tex')
  script=d/'build_source.cjs';script.write_text(variant((PACKAGE/'build_source.cjs').read_text(),level));h.call(['node',script],d/'builder.log')
  raw=json.loads((d/'raw-translated-ir.json').read_text());raw['source']['historicalUpstreamRefinements']=raw['source'].pop('refinements');raw['variant']={'name':name,'status':'arithmetic proposal; mathematical review pending','anchorPower':26}
  (d/'parameter-source-ir.json').write_text(json.dumps(raw,indent=2)+'\n');ordinary=d/'source-ir.json';ordinary.write_text(json.dumps(h.chain_lift(raw,last_power=26),indent=2)+'\n')
  compiled=d/'compiled';r=c.run(ordinary,compiled)
  h.call(['node',PACKAGE/'checker/checker.cjs','--input',ordinary,'--compiled',compiled/'compiled-ir.json','--certificate',compiled/'reduction-certificate.json','--coordinate-map',compiled/'coordinate-map.json','--quartic',compiled/'polynomial.json','--report',d/'independent-check.json'],d/'checker.log')
  t=json.loads((compiled/'polynomial.json').read_text());assert all(x['sPower']==0 for x in t['terms']);bits=max(abs(int(x['coefficient'])).bit_length() for x in t['terms']);t['schema']='ordinary-integer-quartic-v1';t['fixedParameter']=None;t['terms']=[{'monomial':x['monomial'],'coefficient':x['coefficient']} for x in t['terms']];export=compiled/'ordinary-polynomial.json';export.write_text(json.dumps(t,indent=2)+'\n')
  summary['variants'][name]={**r['final'],'maximumCoefficientBits':bits,'ordinaryExportSha256':h.digest(export),'builderSha256':h.digest(script)};(out/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n');print(name,json.dumps(summary['variants'][name]),flush=True)
if __name__=='__main__':main()
