'use strict';
// Review probes only. This file does not import or modify compiler code.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const checkerPath = path.resolve(__dirname, '../checker/checker.cjs');
const {Poly, readIR, checkGates, replay, checkCoordinateMap, checkQuartic} = require(checkerPath);
const clone = x => JSON.parse(JSON.stringify(x));
const term = (monomial, coefficient='1', sPower=0) => ({monomial, coefficient, sPower});
const coordinates = count => Array.from({length:count}, (_,id)=>({id,name:`x${id}`,kind:id===0?'input':'base'}));
const fixedParameter = {name:'S',value:'3^(2^27)',coordinate:false};
const observations = [];
function probe(name, expectedReject, fn) {
  let rejected=false, error=null;
  try { fn(); } catch(e) { rejected=true; error=e.message; }
  observations.push({name, expectedReject, rejected, matchesExpectation:rejected===expectedReject,error});
}

// A quadratic pivot substituted in a nonlinear occurrence makes a cubic.
const data = {fixedParameter,coordinates:coordinates(4),residuals:[
  {id:'pivot',terms:[term([3]),term([1,2],'-1')]},
  {id:'other',terms:[term([1,3]),term([], '-1')]}
]};
probe('degree-growing elimination is rejected',true,()=>replay(readIR(data),{
  schema:'brox-reduction-v1',operations:[{kind:'eliminate',coordinate:3,pivot:'pivot',coefficient:'1',replacement:[term([1,2])],affected:['other']}]
}));

const field = {fixedParameter,coordinates:coordinates(5),residuals:[
  {id:'real',terms:[term([1,3]),term([2,4],'2'),term([0],'-1')]},
  {id:'imag',terms:[term([1,4]),term([2,3])]}
]};
field.coordinates[3].kind='gate';field.coordinates[4].kind='gate';
const shared = {operation:'field_quotient_component',numerator:[[term([0])],[]],denominator:[[term([1])],[term([2])]],output:[[term([3])],[term([4])]],dependencies:[0,1,2],domain:'externally proved nonzero'};
field.gates=[{...shared,coordinateId:3,definitionResidualId:'real',component:0},{...shared,coordinateId:4,definitionResidualId:'imag',component:1}];
probe('valid paired field quotient is accepted',false,()=>checkGates(readIR(field)));
probe('missing field quotient mate is rejected',true,()=>{const x=clone(field);x.gates.pop();checkGates(readIR(x));});
probe('wrong field quotient component is rejected',true,()=>{const x=clone(field);x.gates[1].component=0;checkGates(readIR(x));});
probe('field quotient omitted dependency is rejected',true,()=>{const x=clone(field);x.gates[0].dependencies=[0,1];checkGates(readIR(x));});

const one = readIR({fixedParameter,coordinates:coordinates(1),residuals:[{id:'input',terms:[term([0])]}]});
const coordinateMap=checkCoordinateMap(one,{schema:'brox-coordinate-map-v1',mapping:[{sourceId:0,compactId:0,name:'x0'}],omittedFreeCoordinates:[]});
const table={schema:'brox-sparse-polynomial-v1',fixedParameter:'S = 3^(2^27)',sosMultiplier:'1',coordinates:[{id:0,name:'wrong name',kind:'input'}],terms:[term([0,0])]};
// At initial review this metadata mutation passed. Report its current behavior
// without asserting whether the checker has already been repaired.
let nameRejected=false;
try { checkQuartic(one,table,coordinateMap); } catch(e) { nameRejected=true; }
observations.push({name:'renamed quartic coordinate metadata',rejected:nameRejected,algebraUnaffected:true});
probe('parameter exponent overflow is rejected',true,()=>{
  Poly.from([term([], '1', Number.MAX_SAFE_INTEGER)]).mul(Poly.from([term([], '1', 2)]));
});
const report={checkerSha256:crypto.createHash('sha256').update(fs.readFileSync(checkerPath)).digest('hex'),observations};
fs.writeFileSync(path.join(__dirname,'checker-review-probes.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
