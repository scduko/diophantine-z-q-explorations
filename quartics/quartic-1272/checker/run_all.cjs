'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const {run,hashBytes}=require('./checker.cjs');
const root=process.argv[2]?path.resolve(process.argv[2]):path.resolve(__dirname,'..');
const out=path.join(root,'checker');
const results=[];
for(const stage of ['direct','translated']){
 const d=path.join(root,'compiler',stage);
 const options={input:path.join(root,'builder',stage==='direct'?'raw-ir.json':'raw-translated-ir.json'),compiled:path.join(d,'compiled-ir.json'),certificate:path.join(d,'reduction-certificate.json'),coordinateMap:path.join(d,'coordinate-map.json'),quartic:path.join(d,'polynomial.json'),report:path.join(out,stage+'-check.json'),emitQuartic:path.join(out,stage+'-quartic.json')};
 const r=run(options);results.push({stage,status:r.status,rawHash:r.inputSha256,coordinates:r.coordinateCount,residuals:r.residualCount,gates:r.gateIdentities.checked,degree:r.statistics.degree,monomials:r.statistics.monomials,activeCoordinateCount:r.statistics.activeCoordinateCount,primitiveContent:r.statistics.primitiveContent,maximum:r.statistics.maximumAbsoluteCoefficient,artifactHashes:r.artifactHashes});
}
for(const script of ['mutation_tests.cjs','check_anchor.cjs']){const args=[path.join(__dirname,script)];if(script==='check_anchor.cjs')args.push(root);const p=cp.spawnSync(process.execPath,args,{encoding:'utf8'});if(p.status!==0)throw Error(p.stderr||p.stdout||'subcheck failed');process.stdout.write(p.stdout);}
const files=['checker.cjs','mutation_tests.cjs','check_anchor.cjs','run_all.cjs'];
const report={schema:'brox-checker-final-v1',status:'passed_exact_algebra_checks',checkedAtUTC:new Date().toISOString(),sourceSemanticStatus:'See separate source review and oracle; this checker does not turn numerical tests into arithmetic proofs.',results,mutations:JSON.parse(fs.readFileSync(path.join(__dirname,'MUTATION_TESTS.json'))),anchor:JSON.parse(fs.readFileSync(path.join(__dirname,'ANCHOR_CHECK.json'))),checkerSources:files.map(file=>({file,sha256:hashBytes(fs.readFileSync(path.join(__dirname,file)))}))};
fs.writeFileSync(path.join(out,'FINAL_CHECK.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,results:results.map(({stage,coordinates,residuals,gates,degree,monomials,primitiveContent,maximum})=>({stage,coordinates,residuals,gates,degree,monomials,primitiveContent,maximum})),checkerSources:report.checkerSources}));
