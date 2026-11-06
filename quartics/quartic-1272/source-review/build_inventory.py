"""Emit a complete, independent semantic inventory, not a gate compiler.

Expression nodes are JSON arrays with the operator first. Atomic strings
refer to named definitions or coordinates. Ratios ["rat",a,b] are constants.
Field values are pairs over Q with sqrt(2)^2=2. Point helpers are expanded
in the helpers dictionary. All indices are explicitly enumerated.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BROX=ROOT/'sources/diophantine_optimization_20261106_v3.tex'
UPSTREAM=ROOT/'sources/upstream-quartic-12504-28e87b1.tex'
def op(name,*args):return [name,*args]
def add(*xs):return op('add',*xs)
def mul(*xs):return op('mul',*xs)
def sub(a,b):return op('sub',a,b)
def div(a,b):return op('div',a,b)
def pw(a,b):return op('pow',a,b)
def rat(a,b):return op('rat',a,b)
def comp(a,i):return op('component',a,i)
def pair(a,b):return op('field',a,b)
defs=[]; constraints=[];guards=[];variables=[]
def define(name,expr,lines,**kw):defs.append(dict(name=name,expression=expr,brox_lines=lines,**kw));return name
def var(name,role):variables.append(dict(name=name,domain='Q',role=role));return name
def eq(name,expr,lines,**kw):constraints.append(dict(name=name,residual=expr,equals=0,brox_lines=lines,**kw))
def guard(name,expr,kind,reason,lines):guards.append(dict(name=name,nonzero=expr,enforcement=kind,justification=reason,brox_lines=lines))
def norm(a):return sub(pw(comp(a,0),2),mul(2,pw(comp(a,1),2)))

var('X','input');var('lambda','common rational slope')
define('D',pair(11,-6),[2367,2374]);define('d',pair(3,-1),[2367,2374])
define('P',op('point',pair(rat(57,8),rat(-7,2)),pair(rat(-165,8),rat(417,32))),[2367,2374])
define('beta',add(pw('X',2),2),[3800,3800])
point_names=['A','S','T','Z','H','U_A','U_S','U_T','U_Z']
for name in point_names:
    for c in ['a0','a1','b0','b1']:var(f'half.{name}.{c}',f'affine halfpoint for {name}')
    a=define(f'half.{name}.a',pair(f'half.{name}.a0',f'half.{name}.a1'),[4451,4456])
    b=define(f'half.{name}.b',pair(f'half.{name}.b0',f'half.{name}.b1'),[4451,4456])
    res=op('ksub',op('kpow',b,2),op('ksub',op('kpow',a,3),op('kmul','D',a)))
    for i in range(2):eq(f'curve.{name}.{i}',comp(res,i),[4311,4348])
    define(f'half.{name}',op('point',a,b),[4451,4456])
    define(name,op('point_double',f'half.{name}'),[4311,4348])
    guard(f'doubling.{name}.denominator',b,'implied_by_equations',
          'On the halfpoint curve, (2b)m=3a^2-D cannot hold if b=0.',[4311,4325])
    for coordinate in ['x','y']:
        guard(f'point.{name}.{coordinate}',op('point_component',name,coordinate),'proved_automatic',
              'Every finite double has nonzero x and y over Q(sqrt(2)); x is a nonzero square and +/-d have nonsquare rational norm seven.',[4327,4337])
for name in ['P','A','S','T','Z']:
    define(f'twice.{name}',op('point_double',name),[2395,2399],note='For P all coordinates may be precomputed fixed rational constants.')
    define(f'four.{name}',op('point_double',f'twice.{name}'),[2395,2399])

U=['H','U_A','U_S','U_T','U_Z'];Q=['P','A','S','T','Z']
for i,(u,q) in enumerate(zip(U,Q)):
    denominator=op('ksub',op('point_component',u,'x'),op('point_component',f'four.{q}','x'))
    guard(f'subtraction.{i}',denominator,'explicit_field_inverse',
          'Must retain: equal abscissas can make an unguarded quotient equation 0=0.',[2395,2399,4362,4364])
    define(f'V{i}',op('point_subtract',u,f'four.{q}'),[2395,2399,4340,4348])

for name in U+[f'V{i}' for i in range(5)]+['S']:
    define(f'f.{name}',op('kinv',op('point_component',name,'x')),[2376,2378,4350,4360])
    define(f'z.{name}',op('kdiv',op('kneg',op('point_component',name,'x')),op('point_component',name,'y')),[2376,2378,4350,4360])
    guard(f'z.{name}.denominator',op('point_component',name,'y'),'proved_automatic',
          'Nonzero ordinate of a finite point in 2E(K). A direct quotient is valid.',[4334,4337,4350,4352])

coefficients=[Fraction(1),Fraction(-2,5)]
for j in range(2,13):coefficients.append(coefficients[-1]*Fraction(4*j-5,4*j+1))
for name,e in [(U[i],52 if i==0 else [16,52,52,52][i-1])for i in range(5)]+[(f'V{i}',52 if i==0 else [16,52,52,52][i-1])for i in range(5)]:
    w=define(f'log_argument.{name}',op('kmul','D',op('kpow',f'f.{name}',2)),[4181,4209])
    g=op('kadd',*[op('kscale',rat(c.numerator,c.denominator),op('kpow',w,j))for j,c in enumerate(coefficients[:e//4])])
    define(f'ell.{name}',op('kmul',f'z.{name}',g),[4181,4209],precision=e,degree=e//4-1)
for i in range(1,5):
    define(f'L{i}',op('kdiv',f'ell.{U[i]}','ell.H'),[2408,2412,4162,4165])
    define(f'Lprime{i}',op('conjugate',op('kdiv',f'ell.V{i}','ell.V0')),[2408,2412,4162,4165])
for name in ['H','V0']:
    guard(f'log_denominator.{name}',f'ell.{name}','proved_automatic',
          'z is nonzero and G_J(Df^2) is globally nonzero for J>=2 by the 2-adic unique-minimum argument.',[4350,4360])

tests=[]
def test(name,expr,order,lines):
    define(name,expr,lines);tests.append(dict(name=name,order=order,field='Q(sqrt(2))',brox_lines=lines))
for i,name in enumerate(U):test(f'test.formal.U{i}',f'f.{name}',1,[3810,3822])
for i in range(5):test(f'test.formal.V{i}',op('conjugate',f'f.V{i}'),1,[3810,3822])
for i,k in enumerate([16,52,52,52],1):test(f'test.cross.{i}',op('ksub',f'L{i}',f'Lprime{i}'),k,[4575,4604])
test('test.beta',op('ksub','L1',pair('beta',0)),16,[4575,4604])
test('test.Lucas',op('kadd',op('kpow','L3',2),op('kneg',op('kmul','L2',op('ksub','L2',pair(2,0)),'L3','L4')),op('kpow',op('kmul',op('ksub','L2',pair(2,0)),'L4'),2),pair(-1,0)),52,[4575,4604])
for m in [1,16,52]:
    define(f'E{m}',op('formal_product','T',*[op('kadd',pair(1,0),op('kscale','T',op('kpow',t['name'],2)))for t in tests if t['order']==m]),[4423,4437,4597,4604],note='Polynomial over K. Compute coefficients once; evaluate independently at all nine detector weights.')

theta=[rat(0,1),rat(-1,2),rat(-1,1),rat(1,2399),rat(-32,407)]
scales=[1]
for name in ['A','S','T','Z']:
    x=op('point_component',name,'x')
    scales += [pw(comp(x,0),2),pw(add(1,pw(comp(x,1),2)),2)]
for i,A in enumerate(scales):
    define(f'scale.{i}',A,[3352,3405])
    guard(f'scale.{i}',f'scale.{i}','proved_automatic','For even-coordinate scale, 1+x1^2>0; for odd scale x0>0 by positivity of doubled x at both real embeddings; scale zero is one.',[3366,3376])
    t=define(f'detector.{i}.t',mul(f'scale.{i}','lambda'),[2424,2444,3352,3405])
    delta=define(f'detector.{i}.delta',sub(t,1),[2424,2444])
    f=define(f'detector.{i}.F',mul(*[sub(t,c)for c in theta]),[2424,2444])
    for s in [delta,f]:guard(s,s,'explicit_rational_inverse','Required contact and pole exclusion. Inverse may be combined with other guards if the exact product is recorded.',[2430,2444])
    R=define(f'detector.{i}.R',div(f,mul(pw(f'scale.{i}',5),pw(delta,6))),[2430,2444])
    for m in [1,16,52]:
        define(f'detector.{i}.q{m}',div(mul(pw(f'scale.{i}',10*m-5),pw(delta,10*m-8)),pw(f,2*m-1)),[4272,4279])
    w=define(f'detector.{i}.W',op('kmul',*[op('evaluate_field_polynomial',f'E{m}',f'detector.{i}.q{m}')for m in [1,16,52]]),[4423,4437,4597,4604])
    w0=comp(w,0)
    guard(f'detector.{i}.trace',w0,'explicit_rational_inverse','w0!=0 implies W!=0 and norm(W)!=0 over Q(sqrt(2)); Tr(W^-1)=2w0/norm(W).',[4439,4447])
    b=define(f'pole.{i}.b',div(mul(R,pw(norm(w),2)),mul(4,pw(w0,2))),[4439,4447])
    B=define(f'pole.{i}.B',mul(17,b),[2446,2454])
    for c in ['e','s','p','q']:var(f'pole.{i}.{c}',f'coordinate pole {i}')
    h=define(f'pole.{i}.h',mul(f'pole.{i}.e',sub(B,pw(b,2))),[2446,2454])
    eq(f'pole.{i}.first',sub(pw(f'pole.{i}.p',2),mul(B,sub(1,f'pole.{i}.e'),add(1,mul(3,f'pole.{i}.e')))),[2446,2454])
    eq(f'pole.{i}.second',sub(mul(B,pw(f'pole.{i}.q',2)),mul(sub(pw(f'pole.{i}.s',2),mul(B,h)),add(pw(f'pole.{i}.s',2),mul(3,B,h)))),[2446,2454])
    guard(f'pole.{i}.B',B,'proved_automatic','R is nonzero and w0 inverse enforces nonzero trace; B=17*R/Tr(W^-1)^2.',[4439,4447])

primes=[2,3,5,7,11,13,17]
for c in ['minus']+list(map(str,primes)):
    v=var(f'epsilon.{c}','scalar signed squareclass correction bit')
    eq(f'boolean.{c}',sub(pw(v,2),v),[4458,4469])
define('scalar.c',mul(sub(1,mul(2,'epsilon.minus')),*[add(1,mul(p-1,f'epsilon.{p}'))for p in primes]),[4458,4469])
r=define('scalar.r',mul('beta',sub('beta',1),sub('beta',2401),add(mul(32,'beta'),343),sub(mul(2,'beta'),1)),[2468,2487])
guard('scalar.r',r,'proved_automatic_and_inverse_for_evaluation','For rational X, beta=X^2+2 is >=2 and cannot equal2401 since2399 is not a rational square. Other roots are below2.',[2468,2477,3064,3065])
ratio=define('scalar.ratio',op('kdiv','z.S','z.H'),[2473,2477,2946,2958])
scalar_test_expressions=[comp('f.H',0),comp('f.H',1),comp('f.S',0),comp('f.S',1),comp(ratio,0),comp(ratio,1)]
scalar_tests=[]
for i,(expr,m) in enumerate(zip(scalar_test_expressions,[1,1,1,1,32,32]),1):
    name=define(f'scalar.X{i}',expr,[2473,2477,4285,4305]);scalar_tests.append(dict(name=name,order=m))
    define(f'scalar.leaf{i}',div(name,pw(r,m)),[2473,2477,4285,4305],upstream_lines=[8082,8090])
def N(a,b):return add(pw(a,2),mul(r,pw(b,2)))
define('scalar.n0',N(1,'scalar.leaf1'),[2473,2477],upstream_lines=[8082,8090])
define('scalar.n1',N('scalar.leaf2','scalar.leaf3'),[2473,2477],upstream_lines=[8082,8090])
define('scalar.n3',N('scalar.leaf5','scalar.leaf6'),[2473,2477],upstream_lines=[8082,8090])
define('scalar.m0',N('scalar.n0','scalar.n1'),[2473,2477],upstream_lines=[8082,8090])
define('scalar.m1',N('scalar.leaf4','scalar.n3'),[2473,2477],upstream_lines=[8082,8090])
W=define('scalar.W',N('scalar.m0','scalar.m1'),[2473,2477],upstream_lines=[8082,8090])
b=define('scalar.b',mul('scalar.c',r,pw(W,2)),[2473,2487])
B=define('scalar.B',mul(17,b),[2473,2487])
guard('scalar.b',b,'explicit_rational_inverse_or_equivalent_W_inverse','Retained by Brox2483 and4165. W need not be globally nonzero merely by its rational formula; dropping this guard requires a separate arithmetic-only argument.',[2483,2490,4162,4165])
for c in ['t','e','s','p','q']:var(f'scalar.{c}','scalar pole and preparation')
define('scalar.prep_factor',mul(b,pw('scalar.t',2)),[2478,2487])
prepden=add(1,'scalar.prep_factor')
prep=define('scalar.U',div(mul(b,sub(1,'scalar.prep_factor')),prepden),[2478,2487])
guard('scalar.preparation',prepden,'implied_by_direct_quotient_equation','If1+b*t^2=0 then b!=0 and the numerator is2b!=0. Thus U(1+b*t^2)=b(1-b*t^2) already forces the denominator nonzero.',[2478,2487],)
h=define('scalar.h',mul('scalar.e',sub(B,pw(prep,2))),[2478,2487])
eq('scalar.pole.first',sub(pw('scalar.p',2),mul(B,sub(1,'scalar.e'),add(1,mul(3,'scalar.e')))),[2483,2487])
eq('scalar.pole.second',sub(mul(B,pw('scalar.q',2)),mul(sub(pw('scalar.s',2),mul(B,h)),add(pw('scalar.s',2),mul(3,B,h)))),[2483,2487])

for c in ['u','v','w']:var(f'anchor.{c}','private semilocal anchor witness')
define('anchor.A',sub(add(pw(comp('f.S',0),2),mul(comp('f.S',0),comp('f.S',1))),pw(comp('f.S',1),2)),[4167,4175])
eq('anchor',add(pw('anchor.u',2),mul(6,pw('anchor.v',2)),mul(-2,pw('anchor.w',2)),mul(-3,pw('anchor.A',2)),mul(2,'kappa')),[4167,4175,4272,4283])

helpers={
 'field':["a0+a1*sqrt(2)","sqrt(2)^2=2"],
 'kadd':{'components':['sum(a_i0)','sum(a_i1)']},
 'ksub':{'components':['a0-b0','a1-b1']},
 'kneg':{'components':['-a0','-a1']},
 'kmul':{'binary_components':['a0*b0+2*a1*b1','a0*b1+a1*b0'],'more_than_two_arguments':'Associative product, in the displayed order.'},
 'kscale':{'components':['r*a0','r*a1']},
 'kinv':{'components':['a0/(a0^2-2*a1^2)','-a1/(a0^2-2*a1^2)'],'domain':'a!=0'},
 'kdiv':{'definition':'kmul(a,kinv(b))','direct_equations':['b0*z0+2*b1*z1-a0=0','b0*z1+b1*z0-a1=0'],'domain':'b!=0'},
 'kpow':{'definition':'Repeated product, nonnegative integer exponent; exponent0 gives field(1,0).'},
 'conjugate':{'components':['a0','-a1']},
 'point':{'components':['x','y']},
 'point_double':{'input':['a','b'],'slope':'kdiv(ksub(kscale(3,kpow(a,2)),D),kscale(2,b))','x':'ksub(kpow(slope,2),kscale(2,a))','y':'ksub(kmul(slope,ksub(a,x)),b)','domain':'b!=0; forced by the slope equation and curve equation'},
 'point_subtract':{'inputs':['Q=(x,y)','R=(a,b)'],'slope':'kdiv(kadd(y,b),ksub(x,a))','x':'ksub(ksub(kpow(slope,2),x),a)','y':'ksub(kmul(slope,ksub(old_x,new_x)),y)','domain':'x-a!=0; explicit inverse retained'},
 'formal_product':{'definition':'The second argument names a formal indeterminate; subsequent arguments are field-polynomial factors. It adds no quantified variable.'},
 'evaluate_field_polynomial':{'definition':'Ordinary polynomial substitution at the displayed rational value. A field polynomial remains field-valued.'}
}
assert len(variables)==90,len(variables)
assert len(constraints)==47,len(constraints)
assert len(tests)==16
assert {m:sum(t['order']==m for t in tests)for m in[1,16,52]}=={1:10,16:2,52:4}
report={
 'status':'Independent complete semantic reconstruction. Gate ordering and original unpublished row/elimination choices are not specified by the manuscript.',
 'sources':{'brox':{'path':BROX.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(BROX.read_bytes()).hexdigest()},'upstream':{'path':UPSTREAM.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(UPSTREAM.read_bytes()).hexdigest()}},
 'constants':{'kappa':{'value':'3^(2^28)','quantified':False},'s':{'value':'3^(2^27)','quantified':False,'use':'Only for optional private-anchor affine translation'},'coefficient_field':'Q','field_extension':'K=Q(sqrt(2))','log_coefficients':[str(c)for c in coefficients],'contacts':theta},
 'expression_format':{'atoms':'Integers are scalar constants; strings reference definitions or coordinates. Expressions are prefix JSON arrays.','operators':list(helpers)+['add','sub','mul','div','pow','rat','component','point_component']},
 'helpers':helpers,'base_variables':variables,'base_variable_count':len(variables),'definitions':defs,'structural_constraints':constraints,'structural_constraint_count':len(constraints),'field_tests':tests,'scalar_tests':scalar_tests,'guards':guards,
 'forbidden_additional_guards':['No nonzero guard on coordinate or scalar e,s,p,q,h, or scalar preparation t,U.', 'No nonzero guard on individual rational components of a halfpoint; this quartic uses all four halfpoint coordinates, not the one-ordinate chart.', 'No approximate sqrt(2) coordinate.', 'No Lucas proxy coordinates or exact proxy Lucas equation.', 'No conic parametrization or finite conic selector in this quartic.', 'No normalized scalar R_beta, delta(beta), or enlarged 2^14 correction set; use original r_beta and 256 Boolean corrections.', 'No finite-algebra determinant witness or fixed elliptic exclusion product; use three-witness semilocal anchor.'],
 'optional_anchor_translation':{'source_lines':[4674,4708],'map':{'anchor.u':'s+(U-3V+3W)/4','anchor.v':'s/2+V/4','anchor.w':'3s/2+W/4'},'inverse':{'U':'4u+12v-12w+8s','V':'4v-2s','W':'4w-6s'},'raw_translated_residual_times_16':'-48*anchor.A^2+U^2-6UV+6UW+15V^2-18VW+7W^2+8sU','warning':'The published -3*A_num^2 form has A_num=4*anchor.A. Match actual compiled affine scaling before claiming coefficient-table identity.'},
 'arithmetic_dependencies':['Pinned source cyclic group and index-height inequality','Pinned source five-contact height theorem with stated constant','Pinned source pole completeness and restricted-converse inputs','Sun simultaneous prime-pattern Theorem4.1','Unramified reciprocal-logarithm lemma for precisions16,52','Elementary Lucas growth'],
 'reported_unpublished_compilation':{'raw_base_variables':90,'raw_structural_equations':47,'arithmetic_gate_coordinates':1285,'claimed_eliminations':60,'claimed_row_additions':11,'claimed_final_variables':1315,'claimed_final_residuals':1272,'identity_reconstructed':False}
}
(HERE/'source_inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'definitions':len(defs),'base_variables':len(variables),'structural_constraints':len(constraints),'guards':len(guards),'field_tests':len(tests)}))
