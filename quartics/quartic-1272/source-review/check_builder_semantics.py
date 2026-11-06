"""Independent exact finite-field evaluation of the reconstructed source.

Evaluates every IR gate, checks every gate equation, and compares all 47
structural equations plus semantic outputs with independently written formulas.
This supplements the mathematical review; finite samples do not prove identities.
"""
from fractions import Fraction
from pathlib import Path
import hashlib,json,random

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'builder/raw-ir.json'
TRANS=HERE.parent/'builder/raw-translated-ir.json'
data=json.loads(PATH.read_text())
trans=json.loads(TRANS.read_text())
reports=[]

def run(p,seed):
    rng=random.Random(seed); values={}; checks=0
    S=pow(3,2**27,p)
    def inverse(a):
        if a%p==0:raise ZeroDivisionError('vanished finite-field denominator')
        return pow(a%p,-1,p)
    def rational(text):
        q=Fraction(text);return q.numerator*inverse(q.denominator)%p
    def poly(terms):
        result=0
        for t in terms:
            val=rational(t['coefficient'])*pow(S,t.get('sPower',0),p)%p
            for v in t['monomial']:val=val*values[v]%p
            result=(result+val)%p
        return result
    def fa(a,b):return ((a[0]+b[0])%p,(a[1]+b[1])%p)
    def fn(a):return (-a[0]%p,-a[1]%p)
    def fs(a,b):return fa(a,fn(b))
    def fm(a,b):return ((a[0]*b[0]+2*a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)
    def fc(a,k):return (a[0]*k%p,a[1]*k%p)
    def fi(a):return fc((a[0],-a[1]%p),inverse(a[0]*a[0]-2*a[1]*a[1]))
    def fd(a,b):return fm(a,fi(b))
    def fq(a):return (a[0],-a[1]%p)
    def fp(a,n):
        v=(1,0)
        while n:
            if n&1:v=fm(v,a)
            a=fm(a,a);n//=2
        return v
    byname={c['name']:c['id']for c in data['coordinates']}
    for c in data['coordinates']:
        if c['kind'] in ('base','input'):values[c['id']]=rng.randrange(1,p)
    for g in data['gates']:
        if g['operation']=='quadratic_assignment':v=poly(g['expression'])
        elif g['operation']=='rational_quotient':v=poly(g['numerator'])*inverse(poly(g['denominator']))%p
        elif g['operation']=='field_quotient_component':
            a=tuple(poly(z)for z in g['numerator']);b=tuple(poly(z)for z in g['denominator'])
            v=fd(a,b)[g['component']]
        else:raise AssertionError(g['operation'])
        values[g['coordinateId']]=v
    assert len(values)==len(data['coordinates'])
    for row in data['residuals']:
        if row['kind']=='gate':assert poly(row['terms'])==0,row['name']
    def val(name):return values[byname[name]]
    def same(name,v):
        nonlocal checks
        assert poly(data['values'][name]['terms'])==v%p,(name,poly(data['values'][name]['terms']),v%p)
        checks+=1
    def samef(name,v):same(name+'.0',v[0]);same(name+'.1',v[1])
    expected_rows={}
    D=(11,-6%p)
    def double(P):
        x,y=P;m=fd(fs(fc(fp(x,2),3),D),fc(y,2))
        outx=fs(fp(m,2),fc(x,2));outy=fs(fm(m,fs(x,outx)),y)
        return outx,outy
    def subtract(P,Q):
        x,y=P;a,b=Q;m=fd(fa(y,b),fs(x,a))
        outx=fs(fs(fp(m,2),x),a);outy=fs(fm(m,fs(x,outx)),y)
        return outx,outy
    names=['A','S','T','Z','H','UA','US','UT','UZ'];points={}
    for n in names:
        x=(val(n+'.half.x0'),val(n+'.half.x1'));y=(val(n+'.half.y0'),val(n+'.half.y1'))
        curve=fa(fs(fp(y,2),fp(x,3)),fm(D,x))
        for j in range(2):expected_rows[n+'.curve.'+str(j)]=curve[j]
        points[n]=double((x,y));samef(n+'.x',points[n][0]);samef(n+'.y',points[n][1])
    P=((rational('57/8'),rational('-7/2')),(rational('-165/8'),rational('417/32')))
    roots=[P]+[points[n]for n in ['A','S','T','Z']]
    four=[double(double(x))for x in roots]
    U=[points[n]for n in ['H','UA','US','UT','UZ']]
    V=[subtract(x,y)for x,y in zip(U,four)]
    for i,v in enumerate(V):samef('V'+str(i)+'.x',v[0]);samef('V'+str(i)+'.y',v[1])
    def params(P):return fi(P[0]),fd(fn(P[0]),P[1])
    PU=list(map(params,U));PV=list(map(params,V));PS=params(points['S'])
    coeff=[Fraction(1),Fraction(-2,5)]
    for j in range(2,13):coeff.append(coeff[-1]*Fraction(4*j-5,4*j+1))
    def logarithm(fz,e):
        f,z=fz;w=fm(D,fp(f,2));out=(0,0)
        for j,c in enumerate(coeff[:e//4]):out=fa(out,fc(fp(w,j),rational(str(c))))
        return fm(z,out)
    LU=[logarithm(x,16 if i==1 else 52)for i,x in enumerate(PU)]
    LV=[logarithm(x,16 if i==1 else 52)for i,x in enumerate(PV)]
    for i in range(5):samef('logU'+str(i),LU[i]);samef('logV'+str(i),LV[i])
    L=[fd(LU[i],LU[0])for i in range(1,5)]
    LP=[fq(fd(LV[i],LV[0]))for i in range(1,5)]
    for i in range(1,5):samef('L'+str(i),L[i-1]);samef('LP'+str(i),fq(LP[i-1]))
    beta=(val('input')**2+2)%p;same('beta',beta)
    a,t,b=L[1:]
    lucas=fa(fs(fp(t,2),fm(fm(fm(a,fs(a,(2,0))),t),b)),fs(fp(fm(fs(a,(2,0)),b),2),(1,0)))
    tests=[x[0]for x in PU]+[fq(x[0])for x in PV]+[fs(x,y)for x,y in zip(L,LP)]+[fs(L[0],(beta,0)),lucas]
    orders=[1]*10+[16,52,52,52,16,52]
    for i,t in enumerate(tests):samef('test'+str(i),t)
    scales=[1]
    for n in ['A','S','T','Z']:scales += [points[n][0][0]**2%p,(1+points[n][0][1]**2)**2%p]
    contacts=[0,rational('-1/2'),p-1,rational('1/2399'),rational('-32/407')]
    def pole_expected(name,b,with_prep):
        e,s,pp,qq=[val(name+'.'+z)for z in ['e','s','p','q']]
        B=17*b%p;u=b
        if with_prep:
            prep=val('scalar.preparation');v=b*prep*prep%p
            u=b*(1-v)*inverse(1+v)%p;same('scalar.U',u)
        h=e*(B-u*u)%p
        expected_rows[name+'.firstConic']=(pp*pp-B*(1-e)*(1+3*e))%p
        expected_rows[name+'.secondConic']=(B*qq*qq-(s*s-B*h)*(s*s+3*B*h))%p
    for i,A in enumerate(scales):
        t=A*val('lambda')%p;delta=(t-1)%p;F=1
        for c in contacts:F=F*(t-c)%p
        R=F*inverse(pow(A,5,p)*pow(delta,6,p))%p
        w=(1,0)
        for test,m in zip(tests,orders):
            # Direct original product, independently of the builder's E_m reuse.
            q=pow(A,10*m-5,p)*pow(delta,10*m-8,p)*inverse(pow(F,2*m-1,p))%p
            w=fm(w,fa((1,0),fc(fp(test,2),q)))
        norm=(w[0]**2-2*w[1]**2)%p;b=R*norm*norm*inverse(4*w[0]*w[0])%p
        same('detector'+str(i)+'.R',R);samef('detector'+str(i)+'.W',w);same('detector'+str(i)+'.Bsemantic',b)
        pole_expected('detector'+str(i),b,False)
    rr=beta*(beta-1)*(beta-2401)*(32*beta+343)*(2*beta-1)%p
    same('scalar.r',rr)
    zr=fd(PS[1],PU[0][1]);samef('scalar.zRatio',zr)
    scalar_tests=[*PU[0][0],*PS[0],*zr]
    leaves=[x*inverse(pow(rr,1 if i<4 else 32,p))%p for i,x in enumerate(scalar_tests)]
    def norm(a,b):return (a*a+rr*b*b)%p
    n0=norm(1,leaves[0]);n1=norm(leaves[1],leaves[2]);n3=norm(leaves[4],leaves[5]);W=norm(norm(n0,n1),norm(leaves[3],n3))
    same('scalar.W',W)
    correction=(1-2*val('correction.sign'))%p
    for j,prime in enumerate([2,3,5,7,11,13,17]):
        bit=val('correction.'+str(prime));correction=correction*(1+(prime-1)*bit)%p
        expected_rows['correction.boolean'+str(j)]=(bit*bit-bit)%p
    bit=val('correction.sign');expected_rows['correction.boolean7']=(bit*bit-bit)%p
    b=correction*rr*W*W%p;same('scalar.b',b);pole_expected('scalar',b,True)
    A=(PS[0][0]**2+PS[0][0]*PS[0][1]-PS[0][1]**2)%p;same('anchor.physicalA',A)
    u,v,w=[val('anchor.'+n)for n in['u','v','w']]
    expected_rows['anchor.equation']=(u*u+6*v*v-2*w*w-3*A*A+2*S*S)%p
    structural=[r for r in data['residuals']if r['kind']=='structural']
    assert set(expected_rows)=={r['name']for r in structural}
    for row in structural:assert poly(row['terms'])==expected_rows[row['name']],row['name']
    trow=trans['residuals'][data['anchor']['rowId']]
    assert poly(trow['terms'])==(-48*A*A+u*u-6*u*v+6*u*w+15*v*v-18*v*w+7*w*w+8*S*u)%p
    return {'prime':p,'seed':seed,'semantic_values_compared':checks,'gate_equations_checked':len(data['gates']),'structural_equations_checked':len(structural),'translated_anchor_checked':True}

for p in [1000003,1000033,1000037]:
    for seed in [1315,2718,3141]:reports.append(run(p,seed))
output={'source_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),'translated_sha256':hashlib.sha256(TRANS.read_bytes()).hexdigest(),'sample_count':len(reports),'samples':reports,'scope':'Independent exact finite-field checks of formulas and all equations. This is supplementary evidence, not a proof of rational equivalence or source arithmetic.'}
(HERE/'builder_semantic_checks.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'samples':len(reports),'checks_per_sample':reports[0]},indent=2))
