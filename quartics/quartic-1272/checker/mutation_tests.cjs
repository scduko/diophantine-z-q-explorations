'use strict';
const fs=require('node:fs'),path=require('node:path');
const {Q,Poly,readIR,checkGates,replay,compareIR,checkCoordinateMap,checkQuartic,coefficientStats,scalarSign,hashBytes}=require('./checker.cjs');
const clone=x=>JSON.parse(JSON.stringify(x));
const t=(monomial,coefficient='1/1',sPower=0)=>({monomial,coefficient,sPower});
const data={fixedParameter:{name:'S',value:'3^(2^27)',coordinate:false},coordinates:[0,1,2,3].map(id=>({id,name:['input','x','square','sum'][id],kind:id===0?'input':id===1?'free':'gate'})),residuals:[
 {id:'p',terms:[t([2]),t([1,1],'-1/1')]},
 {id:'q',terms:[t([3]),t([2],'-1/1'),t([0],'-1/1')]},
 {id:'r',terms:[t([3]),t([1],'-1/1')]}
],gates:[{coordinateId:2,definitionResidualId:'p',operation:'quadratic_assignment',expression:[t([1,1])],dependencies:[1]},{coordinateId:3,definitionResidualId:'q',operation:'quadratic_assignment',expression:[t([2]),t([0])],dependencies:[0,2]}]};
const sha=hashBytes(Buffer.from(JSON.stringify(data)));
const cert={schema:'brox-reduction-v1',inputSha256:sha,operations:[
 {kind:'row_add',target:'r',source:'q',factor:'-1/1'},
 {kind:'eliminate',coordinate:3,pivot:'q',coefficient:'1/1',replacement:[t([2]),t([0])],affected:[]},
 {kind:'eliminate',coordinate:2,pivot:'p',coefficient:'1/1',replacement:[t([1,1])],affected:['r']},
 {kind:'normalize',residual:'r',multiplier:'2/1'}
]};
const compiled={fixedParameter:data.fixedParameter,coordinates:data.coordinates.slice(0,2),residuals:[{id:'r',terms:[t([1,1],'2/1'),t([0],'2/1'),t([1],'-2/1')]}]};
const raw=readIR(data),ir=readIR(compiled);checkGates(raw);compareIR(ir,replay(raw,cert,sha));
const map={schema:'brox-coordinate-map-v1',mapping:[{sourceId:0,compactId:0,name:'input'},{sourceId:1,compactId:1,name:'x'}],omittedFreeCoordinates:[]};
const cm=checkCoordinateMap(ir,map),polynomial=checkQuartic(ir,null,cm);
const table={schema:'brox-sparse-polynomial-v1',fixedParameter:'S = 3^(2^27)',sosMultiplier:'1/1',coordinates:compiled.coordinates,terms:polynomial.json()};
checkQuartic(ir,table,cm);const stats=coefficientStats(polynomial);if(stats.degree!==4||stats.monomials!==6||stats.primitiveContent!=='4')throw Error('baseline statistics wrong');
const tests=[];function rejects(name,fn){let caught=false,error=null;try{fn();}catch(e){caught=true;error=e.message;}if(!caught)throw Error('mutation accepted: '+name);tests.push({name,status:'rejected',error});}
function changeData(fn){const x=clone(data);fn(x);return()=>readIR(x);}
function changeCert(fn){const x=clone(cert);fn(x);return()=>replay(raw,x,sha);}
rejects('residual degree three',changeData(x=>x.residuals[0].terms.push(t([1,1,1]))));
rejects('unknown coordinate',changeData(x=>x.residuals[0].terms.push(t([99]))));
rejects('unsorted monomial',changeData(x=>x.residuals[0].terms.push(t([2,1]))));
rejects('zero denominator',changeData(x=>x.residuals[0].terms[0].coefficient='1/0'));
rejects('duplicate coordinate',changeData(x=>x.coordinates.push(clone(x.coordinates[0]))));
rejects('missing input coordinate',changeData(x=>x.coordinates=x.coordinates.slice(1)));
rejects('wrong fixed parameter',changeData(x=>x.fixedParameter.value='3^(2^26)'));
rejects('wrong input kind',changeData(x=>x.coordinates[0].kind='gate'));
rejects('missing gate definition',()=>{const x=clone(data);x.gates.pop();checkGates(readIR(x));});
rejects('unknown gate operation',()=>{const x=clone(data);x.gates[0].operation='trust_me';checkGates(readIR(x));});
rejects('forward gate dependency',()=>{const x=clone(data);x.gates[0].dependencies.push(3);checkGates(readIR(x));});
rejects('gate sign corruption',()=>{const x=clone(data);x.gates[0].expression[0].coefficient='-1/1';checkGates(readIR(x));});
rejects('gate dependency omission',()=>{const x=clone(data);x.gates[1].dependencies=[0];checkGates(readIR(x));});
rejects('wrong input hash',changeCert(x=>x.inputSha256='00'));
rejects('self row addition',changeCert(x=>x.operations[0].source='r'));
rejects('wrong pivot coefficient',changeCert(x=>x.operations[2].coefficient='2/1'));
rejects('wrong replacement',changeCert(x=>x.operations[2].replacement=[t([1])])) ;
rejects('omitted affected residual',changeCert(x=>x.operations[2].affected=[]));
rejects('zero normalization',changeCert(x=>x.operations[3].multiplier='0/1'));
rejects('self-dependent replacement',changeCert(x=>x.operations[2].replacement=[t([2])])) ;
rejects('compiled residual corruption',()=>{const x=clone(compiled);x.residuals[0].terms[0].coefficient='3/1';compareIR(readIR(x),replay(raw,cert,sha));});
rejects('quartic missing monomial',()=>{const x=clone(table);x.terms.pop();checkQuartic(ir,x,cm);});
rejects('quartic changed coefficient',()=>{const x=clone(table);x.terms[0].coefficient='99/1';checkQuartic(ir,x,cm);});
rejects('quartic coordinate name change',()=>{const x=clone(table);x.coordinates[1].name='wrong';checkQuartic(ir,x,cm);});
rejects('zero quartic scalar',()=>{const x=clone(table);x.sosMultiplier='0/1';checkQuartic(ir,x,cm);});
rejects('bad compact coordinate map',()=>{const x=clone(map);x.mapping[1].compactId=0;checkCoordinateMap(ir,x);});
rejects('omit used coordinate',()=>{const x=clone(map);x.mapping.pop();x.omittedFreeCoordinates=[1];checkCoordinateMap(ir,x);});
rejects('false height bound',()=>coefficientStats(polynomial,[t([],'7/1')]));
rejects('nonintegral specialized coefficient',()=>coefficientStats(Poly.from([t([0],'1/2')])));
rejects('negative final S power',()=>coefficientStats(Poly.from([t([0],'1/1',-1)])));
rejects('S exponent arithmetic overflow',()=>Poly.from([t([],'1/1',Number.MAX_SAFE_INTEGER)]).square());
// Specialization is not formal content: both S+1 and S+3 are even.
const even=Poly.from([t([0],'1/1',1),t([0]),t([1],'1/1',1),t([1],'3/1'),t([],'2/1')]);
if(coefficientStats(even).primitiveContent!=='2')throw Error('specialized content test failed');
const integralAtS=Poly.from([t([0],'1/2',1),t([0],'1/2')]);
if(!coefficientStats(integralAtS).integerCoefficients)throw Error('specialized integrality test failed');
const field={fixedParameter:data.fixedParameter,coordinates:data.coordinates.map(c=>({...c,kind:c.id===0?'input':c.id===1?'base':'gate'})),residuals:[{id:'f0',terms:[t([2]),t([1,3],'2/1'),t([0],'-1/1')]},{id:'f1',terms:[t([3]),t([1,2]),t([],'-1/1')]}],gates:[0,1].map(component=>({coordinateId:2+component,definitionResidualId:'f'+component,operation:'field_quotient_component',component,numerator:[[t([0])],[t([])]],denominator:[[t([])],[t([1])]],output:[[t([2])],[t([3])]],dependencies:[0,1]}))};
checkGates(readIR(field));
rejects('field quotient missing mate',()=>{const x=clone(field);x.gates.pop();checkGates(readIR(x));});
rejects('field quotient wrong component',()=>{const x=clone(field);x.gates[0].component=1;checkGates(readIR(x));});
rejects('field quotient omitted dependency',()=>{const x=clone(field);x.gates[0].dependencies=[0];checkGates(readIR(x));});
rejects('field quotient wrong sqrt2 norm',()=>{const x=clone(field);x.residuals[0].terms[1].coefficient='1/1';checkGates(readIR(x));});
const growing={fixedParameter:data.fixedParameter,coordinates:data.coordinates.slice(0,3),residuals:[{id:'p',terms:[t([2]),t([1,1],'-1/1')]},{id:'r',terms:[t([0,2])]}]};
rejects('elimination raises degree to three',()=>replay(readIR(growing),{schema:'brox-reduction-v1',operations:[{kind:'eliminate',coordinate:2,pivot:'p',coefficient:'1/1',replacement:[t([1,1])],affected:['r']}]}));
const report={schema:'brox-checker-mutation-tests-v1',testedAtUTC:new Date().toISOString(),baseline:'passed',adversarialMutations:tests.length,allRejected:true,tests,positiveSpecializationTests:['gcd(S+1,S+3,2)=2','(S+1)/2 integral for odd S'],scope:'Tests exercise the independent checker; they are not inherited arithmetic proofs.'};
fs.writeFileSync(path.join(__dirname,'MUTATION_TESTS.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({baseline:'passed',adversarialMutations:tests.length,allRejected:true}));
