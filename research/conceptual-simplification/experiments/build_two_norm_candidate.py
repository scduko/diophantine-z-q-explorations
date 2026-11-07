"""Generate the isolated dense Gaussian-period two-norm source candidate."""

from pathlib import Path
import json, shutil
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args()
root=Path(__file__).resolve().parents[3]
base=root/'quartics/quartic-523-540/source-reproduction'
src=(base/'builders/odd-product-asymmetric-source.cjs').read_text()
out=a.out.resolve()
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True); shutil.copytree(base/'sources',out/'sources')

def table(d):
 p=127;g=3;h=126//d; cos=[];idx={}
 for j in range(d):
  C=sorted({pow(g,j+d*t,p) for t in range(h)});cos.append(C)
  for a in C:idx[a]=j
 T=[]
 for i in range(d):
  row=[]
  for j in range(d):
   c0=0;tot=[0]*d
   for a in cos[i]:
    for b in cos[j]:
     s=(a+b)%p
     if s==0:c0+=1
     else:tot[idx[s]]+=1
   row.append([x//h-c0 for x in tot])
  T.append(row)
 return T
T3,T7,T9=table(3),table(7),table(9)
start=src.index('function polyProduct(name, ys) {')
end=src.index("start('fixed_height_scales'",start)
block=f'''const periodTable3={json.dumps(T3,separators=(',',':'))};
const periodTable7={json.dumps(T7,separators=(',',':'))};
const periodTable9={json.dumps(T9,separators=(',',':'))};
function extShift(a,s){{const d=a.length;return a.map((_,k)=>a[(k-s+d)%d]);}}
function extMul(name,a,b,table,selected=null){{
 const d=a.length, which=selected===null?[...Array(d).keys()]:selected, out=[];
 for(const k of which){{let c=[zero,zero];for(let i=0;i<d;i++)for(let j=0;j<d;j++)if(table[i][j][k]){{let u=rawFmul(a[i],b[j]);c[0]=add(c[0],scale(u[0],table[i][j][k]));c[1]=add(c[1],scale(u[1],table[i][j][k]));}}out.push([assign(name+'.'+k+'.0',c[0]),assign(name+'.'+k+'.1',c[1])]);}}
 return out;
}}
function norm9(name,x){{
 const y=extMul(name+'.relative9.first',x,extShift(x,3),periodTable9);
 const z=extMul(name+'.relative9.second',y,extShift(x,6),periodTable9,[0,1,2]);
 const q=extMul(name+'.relative3.first',z,extShift(z,1),periodTable3);
 const c=extMul(name+'.relative3.second',q,extShift(z,2),periodTable3,[0])[0];
 return saveF(name,[scale(c[0],-1),scale(c[1],-1)]);
}}
function norm7(name,x){{
 const a0=extMul(name+'.pair0',x,extShift(x,1),periodTable7);
 const a1=extMul(name+'.pair1',extShift(x,2),extShift(x,3),periodTable7);
 const a2=extMul(name+'.pair2',extShift(x,4),extShift(x,5),periodTable7);
 const b0=extMul(name+'.block0',a0,a1,periodTable7);
 const b1=extMul(name+'.block1',a2,extShift(x,6),periodTable7);
 const c=extMul(name+'.final',b0,b1,periodTable7,[0])[0];
 return saveF(name,[scale(c[0],-1),scale(c[1],-1)]);
}}
const packedNorm1=norm9('packedNorm.order1',tests.filter(t=>t.order===1).map(t=>t.value));
const packedNorm40=norm7('packedNorm.order40',tests.filter(t=>t.order===40).map(t=>t.value));
const packedNormSquare1=fsq('packedNorm.square1',packedNorm1);
const packedNormSquare40=fsq('packedNorm.square40',packedNorm40);
'''
src=src[:start]+block+src[end:]
old="let w=fmul('detector'+r+'.W',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E40',coeffs[40],q40));\n let wi=inv('detector'+r+'.w0Inverse',w[0]),nw=rquot('detector'+r+'.normOver2w0',scale(sub(sq(w[0]),scale(sq(w[1]),2)),Q(1,2)),w[0],'retained_w0Inverse'),eDelta=rm('detector'+r+'.eDelta',ep,delta),bv=rquot('detector'+r+'.B',sq(nw),eDelta,'retained_w0_inverse_and_nonsquare_two_force_nonzero_norm');"
new="""let eDelta=rm('detector'+r+'.eDelta',ep,delta);
 let qe1=rm('detector'+r+'.packedWeight1.base',q1,eDelta),qe1_2=rsq('detector'+r+'.packedWeight1.square2',qe1),qe1_4=rsq('detector'+r+'.packedWeight1.square4',qe1_2),qe1_8=rsq('detector'+r+'.packedWeight1.square8',qe1_4),packedWeight1=rm('detector'+r+'.packedWeight1.final',q1,qe1_8);
 let qe40=rm('detector'+r+'.packedWeight40.base',q40,eDelta),qe40_2=rsq('detector'+r+'.packedWeight40.square2',qe40),qe40_3=rm('detector'+r+'.packedWeight40.power3',qe40_2,qe40),qe40_6=rsq('detector'+r+'.packedWeight40.power6',qe40_3),packedWeight40=rm('detector'+r+'.packedWeight40.final',q40,qe40_6);
 let factor1=saveF('detector'+r+'.packedFactor1',[assign('detector'+r+'.packedFactor1.0',add(one,mul(packedWeight1,packedNormSquare1[0]))),assign('detector'+r+'.packedFactor1.1',mul(packedWeight1,packedNormSquare1[1]))]);
 let factor40=saveF('detector'+r+'.packedFactor40',[assign('detector'+r+'.packedFactor40.0',add(one,mul(packedWeight40,packedNormSquare40[0]))),assign('detector'+r+'.packedFactor40.1',mul(packedWeight40,packedNormSquare40[1]))]);
 let w=fmul('detector'+r+'.W',factor1,factor40);
 let wi=inv('detector'+r+'.w0Inverse',w[0]),nw=rquot('detector'+r+'.normOver2w0',scale(sub(sq(w[0]),scale(sq(w[1]),2)),Q(1,2)),w[0],'retained_w0Inverse'),bv=rquot('detector'+r+'.B',sq(nw),eDelta,'retained_w0_inverse_and_nonsquare_two_force_nonzero_norm');"""
if old not in src: raise SystemExit('detector block not found')
src=src.replace(old,new)
(out/'build_source.cjs').write_text(src)
print(out/'build_source.cjs')
