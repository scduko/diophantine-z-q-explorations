from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'circuit/laurent_noy_scalar'
s=(BASE/'build_source.cjs').read_text()
def edit(old,new):
 global s
 assert s.count(old)==1,(old,s.count(old))
 s=s.replace(old,new)
edit("z:(name==='U0'||name==='V0')?null:","z:(name==='V0')?null:")
edit("const LU=PU.map((p,i)=>log('logU'+i,p,i===1?12:40)),LV=PV.map((p,i)=>log('logV'+i,p,i===1?12:40));", "const LU=PU.map((p,i)=>saveF('logU'+i,p.z)),LV=PV.map((p,i)=>log('logV'+i,p,40));")
edit("const tests=[...PU.map(p=>({value:p.f,order:1})),...PV.map(p=>({value:fconj(p.f),order:1}))];", "const tests=[...PU.map((p,i)=>({value:p.f,order:i===0?40:1})),...PV.map(p=>({value:fconj(p.f),order:1}))];")
edit("for(let i=1;i<=4;i++)tests.push({value:fsub(L[i],LP[i]),order:i===1?12:40});", "for(let i=1;i<=4;i++)tests.push({value:fsub(L[i],LP[i]),order:40});")
edit("tests.push({value:fsub(L[1],[beta,zero]),order:12},{value:FF,order:40});", "tests.push({value:fsub(L[1],[beta,zero]),order:40},{value:FF,order:40});")
edit("for(let m of [1,12,40])coeffs[m]", "for(let m of [1,40])coeffs[m]")
a=s.index('function evalSym(');b=s.index('function pole(',a)
s=s[:a]+'''function evalSym(name,co,q){
 const n=co.length-1,split=n===9?5:n===7?4:null;
 if(split===null)throw Error('Unexpected grouped detector degree '+n);
 const powers=[one,q];for(let k=2;k<=split;k++)powers[k]=rm(name+'.power'+k,powers[Math.floor(k/2)],powers[Math.ceil(k/2)]);
 const high=[zero,zero];
 for(let k=split;k<=n;k++)for(let j=0;j<2;j++)high[j]=add(high[j],mul(co[k][j],powers[k-split]));
 const block=[assign(name+'.high.0',high[0]),assign(name+'.high.1',high[1])];
 const out=[mul(powers[split],block[0]),mul(powers[split],block[1])];
 for(let k=0;k<split;k++)for(let j=0;j<2;j++)out[j]=add(out[j],mul(co[k][j],powers[k]));
 return saveF(name,[assign(name+'.sum.0',out[0]),assign(name+'.sum.1',out[1])]);
}
'''+s[b:]
edit("let w=fmul('detector'+r+'.W',fmul('detector'+r+'.Wfirst',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E12',coeffs[12],q12)),evalSym('detector'+r+'.E40',coeffs[40],q40));", "let w=fmul('detector'+r+'.W',evalSym('detector'+r+'.E1',coeffs[1],q1),evalSym('detector'+r+'.E40',coeffs[40],q40));")
out=HERE/'candidate';out.mkdir(exist_ok=True);shutil.copytree(BASE/'sources',out/'sources',dirs_exist_ok=True)
(out/'build_source.cjs').write_text(s)
print(out)
