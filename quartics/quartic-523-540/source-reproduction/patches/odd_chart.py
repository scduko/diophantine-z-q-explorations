"""Add an exact P+4E(K) chart to selected square-abscissa root points."""
from pathlib import Path
import re,sys
ALLOC="""
// Odd-index root witnesses: Q in P+4E(K), with P=2R0, R0=(1+sqrt(2),2sqrt(2)).
const oddChartWitnesses={};for(let n of ['A','S','T','Z'])oddChartWitnesses[n]={
 t:[fresh(n+'.odd.t0','base'),fresh(n+'.odd.t1','base')],
 r:[fresh(n+'.odd.r0','base'),fresh(n+'.odd.r1','base')]};
"""
EQUATIONS="""
 if(oddChartWitnesses[n]){
  const t=oddChartWitnesses[n].t,r=oddChartWitnesses[n].r;
  const tt=fsub(rawFmul(t,t),fscale(fadd(x,j),2));
  const aa=fsub(fadd(rawFmul(t,h),fadd(x,j)),rawFmul(fc(1,1),rawFmul(r,r)));
  for(let k=0;k<2;k++){
   residual(n+'.odd.halfParameter.'+k,tt[k]);
   residual(n+'.odd.halfAbscissaClass.'+k,aa[k]);
  }
 }
"""
def patch(source):
 if 'oddChartWitnesses' in source:raise ValueError('already patched')
 # The earlier count assertion still audits the unaugmented allocation.
 needle="const D=fc(11,-6), P="
 assert source.count(needle)==1
 source=source.replace(needle,ALLOC+'\n'+needle)
 needle=" const y=rawFmul(h,j);\n points[n]="
 assert source.count(needle)==1
 source=source.replace(needle,EQUATIONS+needle)
 source,n=re.subn(r'baseCoordinates:\d+',"baseCoordinates:coords.filter(c=>c.kind==='base'||c.kind==='input').length",source)
 assert n==1,n
 return source
if __name__=='__main__':
 src,dst=map(Path,sys.argv[1:]);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(patch(src.read_text()))
