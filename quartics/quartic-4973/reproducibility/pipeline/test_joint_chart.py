"""Small exact joint-chart checks, independent of every source producer.

The earlier open-chart helper checks are retained for the comparison identity.
"""
from fractions import Fraction as F
import json


def add(*terms):
    out={}
    for c,p in terms:
        for m,a in p.items():out[m]=out.get(m,0)+c*a
    return {m:a for m,a in out.items() if a}


def mul(p,q):
    assert len(p)*len(q)<100000,'Tiny-test size bound'
    out={}
    for m,a in p.items():
        for n,b in q.items():
            k=tuple(x+y for x,y in zip(m,n));out[k]=out.get(k,0)+a*b
    return {m:a for m,a in out.items() if a}


def power(p,n):
    out={(0,)*5:1}
    for _ in range(n):out=mul(out,p)
    return out


def var(i):
    m=[0]*5;m[i]=1
    return {tuple(m):1}


def reduce_curve(poly):
    # Laurent variables x,a,p,q,D; only x,a can acquire negative exponents.
    out={};pending=list(poly.items())
    while pending:
        m,c=pending.pop()
        i=2 if m[2]>=2 else 3 if m[3]>=2 else None
        if i is None:
            out[m]=out.get(m,0)+c;continue
        n=list(m);n[i]-=2;n[i-2]+=1;pending.append((tuple(n),c))
        n[i-2]-=2;n[4]+=1;pending.append((tuple(n),-c))
    return {m:c for m,c in out.items() if c}


def symbolic_checks():
    x,a,p,q,D=[var(i) for i in range(5)]
    d=add((1,x),(-1,a));k=add((1,q),(-1,p))
    b=add((1,mul(x,a)),(1,D))
    ln=add((1,mul(x,p)),(1,mul(a,q)))
    xn=add((1,power(ln,2)),(-1,mul(add((1,x),(1,a)),power(d,2))))
    yn=add((-1,mul(mul(x,p),power(d,3))),
           (1,mul(mul(ln,x),power(d,2))),(-1,mul(ln,xn)))
    tn=add((1,mul(b,add((2,x),(-1,mul(p,q))))),
           (2,mul(mul(mul(p,k),x),a)))
    assert not reduce_curve(add((1,mul(mul(xn,tn),d)),(-1,mul(mul(k,yn),b))))
    # This is also the old lifted Jacobi numerator with its square roots removed.
    rhs=add((1,mul(mul(p,q),add((1,mul(x,a)),(-1,D)))),
            (2,mul(D,add((1,x),(1,a)))))
    assert not reduce_curve(add((1,tn),(-1,rhs)))
    return ['cleared chord z identity','root-free T numerator']


Z=(F(0),F(0));O=(F(1),F(0));D=(F(11),F(-6));d=(F(3),F(-1))
def fa(a,b):return a[0]+b[0],a[1]+b[1]
def fs(a,b):return a[0]-b[0],a[1]-b[1]
def fm(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def sc(a,n):return a[0]*n,a[1]*n
def inv(a):
    n=a[0]*a[0]-2*a[1]*a[1]
    assert n
    return a[0]/n,-a[1]/n
def div(a,b):return fm(a,inv(b))
def neg(P):return None if P is None else (P[0],sc(P[1],-1))
def oncurve(P):
    if P is not None:
        x,y=P
        assert fm(y,y)==fs(fm(fm(x,x),x),fm(D,x))
def plus(P,Q):
    oncurve(P);oncurve(Q)
    if P is None:return Q
    if Q is None:return P
    x,y=P;a,b=Q
    if x==a:
        if y==sc(b,-1):return None
        assert y==b and y!=Z
        slope=div(fs(sc(fm(x,x),3),D),sc(y,2))
    else:slope=div(fs(b,y),fs(a,x))
    xx=fs(fs(fm(slope,slope),x),a)
    yy=fs(fm(slope,fs(x,xx)),y)
    R=(xx,yy);oncurve(R);return R
def times(n,P):
    if n<0:return times(-n,neg(P))
    out=None
    for _ in range(n):out=plus(out,P)
    return out
def z(P):
    if P is None or P==(Z,Z):return Z
    return sc(div(P[0],P[1]),-1)


def field_cases():
    # A half-generator need not belong to 2E(K); its translates test all torsion classes.
    half=((F(1),F(1)),(F(0),F(2)))
    torsions=[None,(Z,Z),(d,Z),(sc(d,-1),Z)]
    oncurve(half)
    for T0 in torsions:oncurve(T0)
    Q=times(4,half);a,b=Q;q=div(b,a);FQ=inv(a)
    checked=0;excluded_b=0;excluded_t=0;identity=0;opposite=0
    for n in (-4,-3,-2,-1,1,2,3,4,5):
        for tor in torsions:
            P=plus(times(n,half),tor);x,y=P
            assert x!=Z and y!=Z
            f=inv(x);p=div(y,x)
            B=fa(O,fm(D,fm(f,FQ)));k=fs(q,p)
            R=plus(P,neg(Q))
            if B==Z:
                # The proposed open chart deliberately has no witness here.
                assert fm(x,a)==sc(D,-1)
                excluded_b+=1;continue
            M=div(p,B);T=fa(fs(sc(x,2),fm(p,q)),sc(fm(M,k),2))
            if T==Z:
                assert k!=Z and R in torsions[2:]
                excluded_t+=1;continue
            zz=sc(div(k,T),-1)
            assert zz==z(R)
            assert R not in torsions[1:]
            if P==Q:assert zz==Z;identity+=1
            if P==neg(Q):assert R==times(2,P);opposite+=1
            if R is not None:
                RT=plus(R,torsions[1])
                assert RT is not None and z(RT)==sc(zz,-1)
                assert RT[0]==sc(div(D,R[0]),-1)
                assert RT[1]==div(fm(D,R[1]),fm(R[0],R[0]))
            # Fusion A*conj(T)+conj(k)*jz=0 for an arbitrary nonzero shared jz.
            conj=lambda v:(v[0],-v[1])
            jz=(F(2),F(3));AA=fm(conj(zz),jz)
            assert fa(fm(AA,conj(T)),fm(conj(k),jz))==Z
            checked+=1
    assert identity==1 and opposite==1 and excluded_b>=1 and excluded_t==2
    return dict(valid_cases=checked,B_zero_excluded=excluded_b,T_zero_poles_excluded=excluded_t,
                identity_cases=identity,opposite_cases=opposite)


def quadratic_rows():
    # Independent component expansion of the six field equations, with both
    # target coordinates and the shared inverse treated as variable inputs.
    def pp(i):return {(i,):1}
    def pa(a,b):
        out=dict(a)
        for k,v in b.items():out[k]=out.get(k,0)+v
        return {k:v for k,v in out.items() if v}
    def pc(a,c):return {k:v*c for k,v in a.items() if v*c}
    def pm(a,b):
        out={}
        for i,x in a.items():
            for j,y in b.items():
                k=tuple(sorted(i+j));out[k]=out.get(k,0)+x*y
        return {k:v for k,v in out.items() if v}
    def plus(a,b):return pa(a[0],b[0]),pa(a[1],b[1])
    def times(a,b):return pa(pm(a[0],b[0]),pc(pm(a[1],b[1]),2)),pa(pm(a[0],b[1]),pm(a[1],b[0]))
    def scale(a,c):return pc(a[0],c),pc(a[1],c)
    def sub(a,b):return plus(a,scale(b,-1))
    def conj(a):return a[0],pc(a[1],-1)
    f,p,A,K,r,s,t,u,jz,q=[(pp(2*i),pp(2*i+1)) for i in range(10)]
    dd=({():11},{():6});f=conj(f);p=conj(p)
    rows=[*sub(K,times(sub(A,r),p)),
          *sub(plus(times(K,p),times(u,p)),plus(scale(times(dd,times(r,f)),2),scale(times(dd,times(t,A)),4))),
          *plus(scale(times(dd,times(plus(A,r),f)),2),plus(times(s,K),plus(scale(times(dd,times(t,A)),4),times(jz,conj(q)))))]
    degree=max(len(k) for row in rows for k in row)
    bound=max(abs(v) for row in rows for v in row.values())
    assert len(rows)==6 and all(rows) and degree==2 and bound==88
    return dict(rational_rows=len(rows),degree=degree,max_absolute_component_coefficient=bound)


def two_denominator_identities():
    x,a,p,q,D=[var(i) for i in range(5)]
    f={(-1,0,0,0,0):1};FQ={(0,-1,0,0,0):1};one=power(x,0)
    B=add((1,one),(1,mul(D,mul(f,FQ))))
    H=mul(add((1,p),(-1,q)),B)
    N=add((1,mul(mul(p,q),add((1,one),(-1,mul(D,mul(f,FQ)))))),
          (2,mul(D,add((1,f),(1,FQ)))))
    c=add((1,a),(1,mul(D,FQ)))
    xp=add((1,x),(1,mul(D,f)));xm=add((1,x),(-1,mul(D,f)))
    U=add((1,mul(q,xp)),(1,mul(c,p)))
    V=add((1,mul(power(q,2),xm)),(-4,D))
    H1=add((1,mul(q,xp)),(-1,mul(c,p)))
    H2=add((1,xm),(-1,power(q,2)))
    assert not reduce_curve(add((1,mul(H,U)),(-1,mul(N,H2))))
    assert not reduce_curve(add((1,mul(H,V)),(-1,mul(N,H1))))
    return ['H*U=N*H2','H*V=N*H1']


def two_denominator_cases():
    half=((F(1),F(1)),(F(0),F(2)));torsions=[None,(Z,Z),(d,Z),(sc(d,-1),Z)]
    Q=times(4,half);a,b=Q;q=div(b,a);FQ=inv(a);q2=fm(q,q);c=fa(a,fm(D,FQ))
    checked=0;poles=0;special=set()
    assert fm(q2,q2)!=sc(D,4)
    for n in (-4,-3,-2,-1,1,2,3,4,5):
        for tor in torsions:
            P=plus(times(n,half),tor);x,y=P;p=div(y,x);f=inv(x)
            xp=fa(x,fm(D,f));xm=fs(x,fm(D,f))
            U=fa(fm(q,xp),fm(c,p));V=fs(fm(q2,xm),sc(D,4))
            H1=fs(fm(q,xp),fm(c,p));H2=fs(xm,q2);R=plus(P,neg(Q))
            if R in torsions[2:]:
                assert U==V==Z and H2!=Z
                poles+=1;continue
            assert U!=Z or V!=Z
            zz=z(R)
            assert fm(zz,U)==H2 and fm(zz,V)==H1
            assert zz==(div(H2,U) if U!=Z else div(H1,V))
            for label,point in [('Q',Q),('-Q',neg(Q)),('Q+T0',plus(Q,torsions[1])),
                                ('-Q+T0',plus(neg(Q),torsions[1]))]:
                if P==point:special.add(label)
            jz=(F(2),F(3));conj=lambda v:(v[0],-v[1]);A=fm(conj(zz),jz)
            Bq=fm(jz,conj(q));Bc=fm(jz,conj(c))
            assert fm(A,conj(U))==fm(jz,conj(H2))
            assert fm(A,conj(V))==fs(fm(Bq,conj(xp)),fm(Bc,conj(p)))
            r=div(jz,conj(q));s=div(conj(c),conj(q));t=inv(conj(q2));u=fm(r,s)
            pp=conj(p);ff=conj(f);dd=conj(D);K=fm(fs(A,r),pp)
            assert fs(fa(fm(K,pp),fm(u,pp)),fa(sc(fm(dd,fm(r,ff)),2),sc(fm(dd,fm(t,A)),4)))==Z
            assert fa(sc(fm(dd,fm(fa(A,r),ff)),2),fa(fm(s,K),fa(sc(fm(dd,fm(t,A)),4),fm(jz,conj(q)))))==Z
            checked+=1
    assert checked==34 and poles==2 and len(special)==4
    return dict(valid_cases=checked,actual_poles_rejected=poles,special_cases=sorted(special))


def joint_identities():
    # Independent Laurent-polynomial verification, variables f,p,A,q,c,J,D.
    one={(0,)*7:1}
    def variable(i,e=1):
        key=[0]*7;key[i]=e
        return {tuple(key):1}
    def pw(x,n):
        z=one
        for _ in range(n):z=mul(z,x)
        return z
    f,p,A,q,c,J,D=[variable(i) for i in range(7)];qi=variable(3,-1)
    r=mul(J,qi);s=mul(c,qi);t=pw(qi,2);u=mul(r,s)
    K=mul(add((1,A),(-1,r)),p);x=add((1,pw(p,2)),(1,mul(D,f)))
    E=add((1,mul(K,p)),(1,mul(u,p)),(-2,mul(D,mul(r,f))),(-4,mul(D,mul(t,A))))
    E2=add((2,mul(D,mul(add((1,A),(1,r)),f))),(1,mul(s,K)),
           (4,mul(D,mul(t,A))),(1,mul(J,q)))
    E1=add((2,E),(1,E2));xp=add((1,x),(1,mul(D,f)));xm=add((1,x),(-1,mul(D,f)))
    U=add((1,mul(q,xp)),(1,mul(c,p)));V=add((1,mul(pw(q,2),xm)),(-4,D))
    H1=add((1,mul(q,xp)),(-1,mul(c,p)));H2=add((1,xm),(-1,pw(q,2)))
    R1=add((1,mul(A,U)),(-1,mul(J,H2)));R2=add((1,mul(A,V)),(-1,mul(J,H1)))
    assert not add((F(1,2),mul(q,add((1,E1),(1,E2)))),(-1,R1))
    assert not add((F(1,2),mul(pw(q,2),add((1,E1),(-1,E2)))),(-1,R2))
    curve=add((1,mul(f,pw(p,2))),(1,mul(D,pw(f,2))),(-1,one))
    expression=add((1,mul(H2,V)),(-1,mul(H1,U)),(4,mul(D,mul(pw(q,2),curve))))
    # Only the target relation c²=q⁴+4D is used for this eliminant.
    out={};pending=list(expression.items())
    while pending:
        mon,coefficient=pending.pop()
        if mon[4]<2:
            out[mon]=out.get(mon,0)+coefficient;continue
        key=list(mon);key[4]-=2;key[3]+=4;pending.append((tuple(key),coefficient))
        key[3]-=4;key[6]+=1;pending.append((tuple(key),4*coefficient))
    assert not {mon:value for mon,value in out.items() if value}
    return ['q*(E1+E2)/2=first graph equation',
            'q²*(E1-E2)/2=second graph equation',
            'graph eliminant forces f*p²+D*f²=1']


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions are required')
    print(json.dumps(dict(status='PASS',open_chart_identities=symbolic_checks(),
                         new_identities=two_denominator_identities(),examples=two_denominator_cases(),
                         joint_identities=joint_identities(),
                         quadratic_rows=quadratic_rows(),
                         scope='Tiny exact identities, not source or arithmetic acceptance')))
