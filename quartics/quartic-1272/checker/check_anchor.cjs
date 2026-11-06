'use strict';
const fs=require('node:fs'),path=require('node:path');
const {Q,Poly,readIR,hashBytes}=require('./checker.cjs');
const fail=m=>{throw Error(m);};
const root=process.argv[2]?path.resolve(process.argv[2]):path.resolve(__dirname,'..');
const rawBytes=fs.readFileSync(path.join(root,'builder/raw-ir.json'));
const translatedBytes=fs.readFileSync(path.join(root,'builder/raw-translated-ir.json'));
const a=readIR(JSON.parse(rawBytes)),b=readIR(JSON.parse(translatedBytes));
const meta=a.data.anchor;
if(meta.rowId!==b.data.anchor.rowId||JSON.stringify(meta.privateCoordinateIds)!==JSON.stringify(b.data.anchor.privateCoordinateIds))fail('anchor metadata changed');
const ids=meta.privateCoordinateIds;if(ids.length!==3||new Set(ids).size!==3)fail('invalid private triple');
const [u,v,w]=ids.map(id=>Poly.coordinate(id));
const S=Poly.from([{monomial:[],sPower:1,coefficient:'1/1'}]);
const quarter=new Q(1n,4n);
const forward=new Map([[ids[0],S.add(u.sub(v.scale(new Q(3n))).add(w.scale(new Q(3n))).scale(quarter))],[ids[1],S.scale(new Q(1n,2n)).add(v.scale(quarter))],[ids[2],S.scale(new Q(3n,2n)).add(w.scale(quarter))]]);
const inverse=new Map([[ids[0],u.scale(new Q(4n)).add(v.scale(new Q(12n))).sub(w.scale(new Q(12n))).add(S.scale(new Q(8n)))],[ids[1],v.scale(new Q(4n)).sub(S.scale(new Q(2n)))],[ids[2],w.scale(new Q(4n)).sub(S.scale(new Q(6n)))]]);
function substitute(p,m){const r=new Poly();for(const t of p.terms.values()){let q=new Poly().put([],t.s,t.c);for(const id of t.m)q=q.mul(m.get(id)||Poly.coordinate(id));for(const z of q.terms.values())r.put(z.m,z.s,z.c);}return r;}
for(const id of ids){if(!substitute(forward.get(id),inverse).equals(Poly.coordinate(id)))fail('forward inverse composition fails');if(!substitute(inverse.get(id),forward).equals(Poly.coordinate(id)))fail('inverse forward composition fails');}
if(a.coordinates.size!==b.coordinates.size||a.residuals.size!==b.residuals.size)fail('anchor transformation changes census');
for(const[id,c]of a.coordinates)if(!b.coordinates.has(id)||(!ids.includes(id)&&b.coordinates.get(id).name!==c.name)||b.coordinates.get(id).kind!==c.kind)fail('nonprivate anchor coordinate identity changes');
let unchanged=0;for(const[id,p]of a.residuals){if(!b.residuals.has(id))fail('anchor residual missing');if(id===meta.rowId){if(!substitute(p,forward).scale(new Q(16n)).equals(b.residuals.get(id)))fail('anchor row is not 16 times transformed original');}else{for(const v of ids)if(p.uses(v))fail('private anchor coordinate occurs outside anchor row');if(!p.equals(b.residuals.get(id)))fail('nonanchor row changed');unchanged++;}}
const report={schema:'brox-independent-anchor-check-v1',status:'passed',inputHashes:{raw:hashBytes(rawBytes),translated:hashBytes(translatedBytes)},anchorResidualId:meta.rowId,privateCoordinateIds:ids,unchangedResiduals:unchanged,forward:Object.fromEntries([...forward].map(([v,p])=>[v,p.json()])),inverse:Object.fromEntries([...inverse].map(([v,p])=>[v,p.json()])),determinant:'1/64',inverseCompositionChecked:true,rowScale:'16/1',conclusion:'The rational common-zero sets are in bijection. The translated SOS is not asserted to equal the literal affine substitution into the old SOS, since the anchor residual is multiplied by 16.',scope:'Exact polynomial identities only; inherited arithmetic remains external.'};
fs.writeFileSync(path.join(__dirname,'ANCHOR_CHECK.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:'passed',anchorRow:meta.rowId,unchangedResiduals:unchanged,rowScale:16}));
