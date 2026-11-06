"""Small exact rational-chart checks, independent of every source producer."""
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
    f,x,p,FQ,q,t,M,T,A,jz=[(pp(2*i),pp(2*i+1)) for i in range(10)]
    dd=({():11},{():-6});one=({():1},{})
    k=sub(q,p);B=plus(one,times(dd,t))
    rows=[*sub(times(x,f),one),*sub(times(p,p),sub(x,times(dd,f))),
          *sub(t,times(f,FQ)),*sub(times(M,B),p),
          *sub(T,plus(sub(scale(x,2),times(p,q)),scale(times(M,k),2))),
          *plus(times(A,conj(T)),times(conj(k),jz))]
    degree=max(len(k) for row in rows for k in row)
    bound=max(abs(v) for row in rows for v in row.values())
    assert len(rows)==12 and all(rows) and degree==2 and bound==22
    return dict(rational_rows=12,degree=degree,max_absolute_component_coefficient=bound)


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Assertions are required')
    print(json.dumps(dict(status='PASS',identities=symbolic_checks(),examples=field_cases(),
                         quadratic_rows=quadratic_rows(),
                         scope='Tiny exact identities, not source or arithmetic acceptance')))
