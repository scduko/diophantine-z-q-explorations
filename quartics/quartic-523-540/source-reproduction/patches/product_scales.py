"""Replace nine height scales by three scales of the product abscissa.
Arithmetic equivalence requires the separate odd-root-label proof.
"""
def patch(s):
 old="let scales=[one];for(let n of ['A','S','T','Z']){scales.push(rsq(n+'.scale0',points[n].x[0]));scales.push(rsq(n+'.scale1',add(one,rsq(n+'.x1Square',points[n].x[1]))));}"
 new="""let productX=fc(1);
for(let n of ['A','S','T','Z'])productX=fmul('heightProduct.'+n,productX,points[n].x);
saveF('heightProduct',productX);
const scales=[one,rsq('heightProduct.scale0',productX[0]),rsq('heightProduct.scale1',add(one,rsq('heightProduct.x1Square',productX[1])))];"""
 assert s.count(old)==1
 s=s.replace(old,new)
 assert s.count('r<9;r++')==2
 s=s.replace('r<9;r++','r<3;r++')
 assert s.count("if(coords.length!==90)throw Error('base count '+coords.length);")==1
 s=s.replace("if(coords.length!==90)throw Error('base count '+coords.length);", "if(coords.length!==66)throw Error('base count '+coords.length);")
 if 'baseCoordinates:90' in s:
  s=s.replace('baseCoordinates:90',"baseCoordinates:coords.filter(c=>c.kind==='base'||c.kind==='input').length")
 else:
  assert "baseCoordinates:coords.filter(c=>c.kind==='base'||c.kind==='input').length" in s
 return s
if __name__=='__main__':
 from pathlib import Path
 import sys
 Path(sys.argv[2]).write_text(patch(Path(sys.argv[1]).read_text()))
