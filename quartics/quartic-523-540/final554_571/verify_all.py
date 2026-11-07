"""Independent exact checks of elimination, constant lift, and both full tables.

Only the Python standard library is required. This checks algebraic identities
and projection-preserving changes; it does not prove the source arithmetic.
"""
from pathlib import Path
import json,hashlib,importlib.util,math,functools
from fractions import Fraction as Q
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('V',HERE/'verify_elimination.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(p):
 den=functools.reduce(math.lcm,(c.denominator for c in p.values()),1)
 num=functools.reduce(math.gcd,(abs(c.numerator*(den//c.denominator)) for c in p.values()),0)
 mul=Q(den,num)
 if p[min(p,key=lambda k:(k[1],k[0]))]<0:mul=-mul
 return {k:c*mul for k,c in p.items()}
def check_table(directory):
 source=read(directory/'polynomial/compiled-ir.json');table=read(directory/'polynomial/polynomial.json')
 coords={c['id']:c for c in source['coordinates']}
 poly={};active=set()
 for row in source['residuals']:
  p=V.readpoly(row['terms']);assert V.degree(p)<=2
  assert p==normalize(p)
  active |= V.variables(p);poly=V.add(poly,V.mul(p,p))
 assert active==set(coords) and 0 in active
 mapping={c['sourceId']:c['id'] for c in table['coordinates']}
 assert list(mapping)==sorted(active)
 assert list(mapping.values())==list(range(len(mapping))) and mapping[0]==0
 expected={(s,tuple(mapping[i] for i in m)):c for (s,m),c in poly.items()}
 actual=V.readpoly(table['terms']);assert actual==expected
 assert V.degree(actual)==4 and all(c.denominator==1 for c in actual.values())
 content=functools.reduce(math.gcd,(abs(c.numerator) for (s,m),c in actual.items() if s==0),0)
 assert content==1
 return {'coordinates':len(coords),'residuals':len(source['residuals']),'degree':4,'monomials':len({m for s,m in actual}),'polynomialSha256':sha(directory/'polynomial/polynomial.json'),'maximumIntegerCoefficientBits':max(abs(c.numerator).bit_length() for c in actual.values()) if all(s==0 for s,m in actual) else None}
def check_lift():
 small=read(HERE/'symbolic554/integer-candidate-ir.json');large=read(HERE/'ordinary571/lifted-ir.json')
 sc={c['id']:c for c in small['coordinates']};lc={c['id']:c for c in large['coordinates']}
 chain=large['constantChain']['coordinates'];assert len(chain)==17
 assert not set(chain)&set(sc) and set(lc)==set(sc)|set(chain)
 assert all(lc[v]['protected'] for v in chain)
 assert all(lc[v]==c for v,c in sc.items())
 rows={r['id']:V.readpoly(r['terms']) for r in large['residuals']}
 for r in small['residuals']:
  p=V.readpoly(r['terms']);expected={}
  for (s,m),a in p.items():
   assert s in (0,1) and (s==0 or len(m)<=1)
   k=(0,tuple(sorted(m+((chain[-1],) if s else ()))))
   expected[k]=expected.get(k,Q(0))+a
  assert rows.pop(r['id'])==expected
 for k,v in enumerate(chain):
  expected={(0,(v,)):Q(1)}
  expected[(0,()) if k==0 else (0,(chain[k-1],chain[k-1]))]=Q(-3**1024) if k==0 else Q(-1)
  assert rows.pop(f'constant-chain-{k}')==expected
 assert not rows
 # Induction: c_0=3^(2^10), c_i=c_(i-1)^2 gives c_16=3^(2^26).
 return {'constant':'3^(2^26)','additionalCoordinates':17,'uniqueExtension':True}
def check_compile_relation(directory,sourcefile):
 src=read(sourcefile);out=read(directory/'polynomial/compiled-ir.json')
 assert src['coordinates']==out['coordinates']
 before={r['id']:normalize(V.readpoly(r['terms'])) for r in src['residuals']}
 after={r['id']:V.readpoly(r['terms']) for r in out['residuals']}
 assert before==after

def main():
 manifest=read(HERE/'MANIFEST.json')
 for name,h in manifest['sha256'].items():assert sha(HERE/name)==h,name
 V.SOURCE=HERE/'source561.json';V.HERE=HERE/'symbolic554';V.verify()
 check_compile_relation(HERE/'symbolic554',HERE/'symbolic554/integer-candidate-ir.json')
 check_compile_relation(HERE/'ordinary571',HERE/'ordinary571/lifted-ir.json')
 result={'eliminationVerified':True,'constantLift':check_lift(),'symbolic554':check_table(HERE/'symbolic554'),'ordinary571':check_table(HERE/'ordinary571')}
 assert result['symbolic554']['coordinates']==554 and result['ordinary571']['coordinates']==571
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
