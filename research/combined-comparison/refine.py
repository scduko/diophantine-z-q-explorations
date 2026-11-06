"""Further source refinements; preserves all earlier artifacts. See REFINEMENTS.md."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from explore import ROOT, PACKAGE, builder_variant, replace_once, chain_lift, call, digest

def refine(s, level):
    s=replace_once(s,"let ep=rm('detector'+r+'.eWeight',rp('detector'+r+'.Adelta5',Ad,5),fi),ei=inv('detector'+r+'.eWeightInverse',ep),Rv=rm('detector'+r+'.R',ei,di);",
                   "let ep=rm('detector'+r+'.eWeight',rp('detector'+r+'.Adelta5',Ad,5),fi);")
    s=replace_once(s,",bv=rm('detector'+r+'.B',Rv,rsq('detector'+r+'.normOver2w0Square',nw));",
                   "; let eDelta=rm('detector'+r+'.eDelta',ep,delta),bv=rquot('detector'+r+'.B',sq(nw),eDelta,'nonzero_norm_and_w0_guard_force_nonzero_denominator');")
    s=replace_once(s,'function pole(name,b,p,prep){',"""function pole(name,b,p,prep){
 if(!prep){
  const B=scale(b,17),eb=rm(name+'.eb',p.e,b);
  residual(name+'.firstConic',add(sq(p.p),scale(b,-17),scale(eb,-34),scale(mul(eb,p.e),51)));
  let h=assign(name+'.h',sub(scale(eb,17),mul(eb,b))),Bh=rm(name+'.Bh',B,h),ss=rsq(name+'.s2',p.s),qq=rsq(name+'.q2',p.q);
  residual(name+'.secondConic',sub(mul(B,qq),mul(sub(ss,Bh),add(ss,scale(Bh,3)))));
  return;
 }
""")
    if level>=2:
        s=replace_once(s,",di=inv('detector'+r+'.deltaInverse',delta),Ad=",",Ad=")
        s=replace_once(s,"let q1=rm('detector'+r+'.q1',ep,rp('detector'+r+'.deltaInverse3',di,3));",
                       "let q1=rquot('detector'+r+'.q1',ep,rp('detector'+r+'.delta3',delta,3),'eDelta_equation_forces_delta_nonzero');")
    if level>=3:
        s=replace_once(s,"let fi=inv('detector'+r+'.FInverse',Fv),Ad=","let Ad=")
        s=replace_once(s,"let ep=rm('detector'+r+'.eWeight',rp('detector'+r+'.Adelta5',Ad,5),fi);",
                       "let ep=rquot('detector'+r+'.eWeight',rp('detector'+r+'.Adelta5',Ad,5),Fv,'positive_scale_and_nonzero_delta_force_F_nonzero');")
    if level>=4:
        s=replace_once(s,"let four={P:double('P4',double('P2',P))};for(let n of ['A','S','T','Z'])four[n]=double(n+'4',double(n+'2',points[n]));",
                       "let four={P:double('P2',P)};for(let n of ['A','S','T','Z'])four[n]=double(n+'2',points[n]);")
        s=replace_once(s,"start('fourfold_roots',[2394,2399]);","start('doubled_targets',[2394,2399]);")
    return s

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    pins=json.loads((Path(__file__).parent/'INPUTS.json').read_text())
    for p,h in pins['sha256'].items():assert digest(ROOT/p)==h,p
    spec=importlib.util.spec_from_file_location('compiler',PACKAGE/'compiler/compile_ir.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    base=builder_variant((PACKAGE/'builder/build_source.cjs').read_text(),'h19',32)
    summary={'baseCommit':pins['baseCommit'],'variants':{}}
    for level,name in enumerate(['detector_fusions','delta_quotient','scale_quotient','target_two'],1):
        dest=out/name;build=dest/'builder';build.mkdir(parents=True);sources=dest/'sources';sources.mkdir()
        shutil.copyfile(PACKAGE/'sources/diophantine_optimization_20261106_v3.tex',sources/'diophantine_optimization_20261106_v3.tex')
        script=build/'build_source.cjs';script.write_text(refine(base,level))
        call(['node',script],dest/'builder.log')
        raw=json.loads((build/'raw-translated-ir.json').read_text())
        raw['source']['historicalUpstreamRefinements']=raw['source'].pop('refinements')
        raw['source']['variant']={'name':name,'comparisonOrders':[12,40,40,40],'scalarOrder':32,'targetMultiplier':2 if level>=4 else 4,'status':'arithmetic proposal; see REFINEMENTS.md'}
        (dest/'parameter-source-ir.json').write_text(json.dumps(raw,indent=2)+'\n')
        ordinary=dest/'source-ir.json';ordinary.write_text(json.dumps(chain_lift(raw,last_power=26),indent=2)+'\n')
        compiled=dest/'compiled';r=compiler.run(ordinary,compiled)
        call(['node',PACKAGE/'checker/checker.cjs','--input',ordinary,'--compiled',compiled/'compiled-ir.json','--certificate',compiled/'reduction-certificate.json','--coordinate-map',compiled/'coordinate-map.json','--quartic',compiled/'polynomial.json','--report',dest/'independent-check.json'],dest/'checker.log')
        t=json.loads((compiled/'polynomial.json').read_text());assert all(x['sPower']==0 for x in t['terms'])
        bits=max(abs(int(x['coefficient'])).bit_length() for x in t['terms'])
        t['schema']='ordinary-integer-quartic-v1';t['fixedParameter']=None
        t['terms']=[{'monomial':x['monomial'],'coefficient':x['coefficient']} for x in t['terms']]
        export=compiled/'ordinary-polynomial.json';export.write_text(json.dumps(t,indent=2)+'\n')
        item={**r['final'],'maximumCoefficientBits':bits,'ordinaryExportSha256':digest(export),'builderSha256':digest(script)}
        summary['variants'][name]=item;(out/'REFINEMENT_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
        print(name,json.dumps(item),flush=True)

if __name__=='__main__':main()
