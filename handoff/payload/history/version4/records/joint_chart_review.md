# Independent review of the four-field joint chart

Date: 2026-11-06. Verdict: PASS for the stated arithmetic graph and its soundness/completeness interface. This review does not accept an emitted source, a finite replay, or an endpoint count. Version 3 and the prior frozen source contracts remain unchanged.

Paths below are relative to `work/quartic-sub10000-20261106/`.

| Reviewed argument | SHA-256 |
| --- | --- |
| `charts/sub5000/next-interface/joint-chart/PROOF.md` | `947b505969ee3b6f1c8677e452703454adac6933c2bb01bbb54ab4b27b5e7451` |
| `charts/sub5000/next-interface/TWO_DENOMINATOR.md` | `d4f43b3fef411179f8c1afe7a9029fc5a3e67d42399376761e965281c79b8dc2` |
| `charts/sub5000/RATIONAL_DIFFERENCE.md` | `8558cbfdb09bfaf12054caa2907900bc30b6de91fd6ab43c14ddc294f1cd7e9d` |

I checked the eliminant and transformations directly, read the exceptional-point and local-index arguments, and inspected `joint_chart.py` for its conjugation and boundary conventions. Complete independent source reconstruction, full incidence, flattening and replay remain required. No test run or author-reported count substitutes for the following argument.

## Fixed target and nonzero premises

Work in K=Q(sqrt(2)), d=3-sqrt(2), D=d^2 and E:y^2=x^3-Dx. The target Q=(a,aq) is a retained nonzero quadruple of a root point in the torsion-free group G=2E(K). Hence a,q are nonzero. Retain F=1/a and q^2=a-DF. With c=a+DF,

```
c^2-q^4=4D.
```

Let J=1/z(J_common), where J_common is the original nonzero point in G. Thus J!=0. The notation J in the equations is a field value, not the integer index of the common point. The four shared values are uniquely forced by

```
r q=J,  s q=c,  t(a-DF)=1,  u=r s.
```

They are r=J/q, s=c/q, t=1/q^2 and u=rs. No integrality of q,J or these coefficients at a selected prime is needed. Their denominators must be accounted for by the existing final approximation choice.

## Recovery uses no inverse of the alternate

The private variables are f,p,A,K, constrained by

```
K=(A-r)p,
E0 := Kp+up-2Drf-4DtA=0,
E2 := 2D(A+r)f+sK+4DtA+Jq=0.
```

Every term is quadratic or linear when D is the fixed field constant. Define x=p^2+Df and L=Ap=K+rp. Substitution gives

```
E1 := 2E0+E2 = 2(A-r)x+sL-4DtA+up+Jq,
E2 = 2D(A+r)f+sL+4DtA-up+Jq.
```

Adding and multiplying by q/2 gives A U=J H2; subtracting and multiplying by q^2/2 gives A V=J H1, where

```
U=q(x+Df)+cp,       H2=x-Df-q^2,
V=q^2(x-Df)-4D,     H1=q(x+Df)-cp.
```

These manipulations are reversible because q and 2 are nonzero. With Z=A/J, they say ZU=H2 and ZV=H1. In particular H2 V-H1 U=0 even when A=0.

The missing curve equation follows from the exact expansion

```
H2 V-H1 U
 = (p^2-q^2)(q^2 p^2-4D)
   -[q^2(p^2+2Df)^2-c^2 p^2]
 = p^2(c^2-q^4-4D)+4Dq^2(1-fp^2-Df^2)
 = -4Dq^2(fp^2+Df^2-1).
```

Thus fp^2+Df^2=1, since Dq!=0. Consequently xf=1 and p^2=x-Df. Both x and f are nonzero, and P=(x,xp) is an actual point of E. No inverse of A, K, U, V, p, an index difference, or a logarithm difference was used in this recovery.

The unchanged G equations are essential: their previously proved global nonvanishing forces p!=0, so P is not a two-torsion point. That proof applies to arbitrary f in K and does not assume that f is a square. The inherited statement that E(K) has only its four two-torsion points as torsion then makes P nontorsion. Deleting or altering those G equations would invalidate this interface.

## The graph has no extra component

For a recovered curve point, the two graph identities are identities for z(P-Q), where z=-x/y extends to zero at O and T0=(0,0). To check uniqueness at exceptional denominators, suppose U=V=0. Then p=-2v/q for v=d or -d, and

```
x=v(c+2v)/q^2=v(a+v)/(a-v).
```

Together with the value of p, these are exactly the two points P=Q+(v,0), where the difference is an actual pole of z. At each, H2=(4D-q^4)/q^2. This is nonzero: q^4=4D would imply q^2=2d or -2d and hence N(q)^2=28, impossible for rational N(q). Thus these poles cannot solve ZU=H2. At every other P, at least one of U,V is nonzero, so the two equations determine a unique Z.

On the ordinary chord domain, the identities H U=N H2 and H V=N H1, with H=(p-q)(1+DfF) and N=pq(1-DfF)+2D(f+F), identify that Z with z(P-Q). These rational-function identities hold on E, and the unique value extends them at every point where z is regular. This uses only ordinary characteristic-zero curve algebra, not a new group-membership theorem.

The four relevant special cases are retained. At P=Q and P=Q+T0, H1=H2=0 and V=q^4-4D!=0, so Z=A=0. At P=-Q and P=-Q+T0, U=H2=0 but V is again nonzero and determines the correct nonzero value. In particular admitting P-Q=T0 introduces a genuine elliptic difference, not an extraneous component. The two differences (d,0) and (-d,0) remain excluded as actual poles.

Conversely, for any nontorsion affine P whose difference is not a pole, set f=1/x, p=y/x, A=J z(P-Q), K=(A-r)p. The curve identity gives x=p^2+Df, the graph gives E1=E2=0, and E0=(E1-E2)/2=0. This is the exact rational forward map on the stated domain. Its inverse recovers P and the same alternate A. It need not recover a witness of the narrower old B!=0 difference presentation for every new point.

## Local arithmetic, conjugation and completeness

In the actual source A is conjugate(z(P-Q))*jz, with jz=1/conjugate(z(J_common)). Accordingly f,p,D,q and c are conjugated in these graph equations and J is replaced by jz. The inspected emitter follows that convention. It is a field automorphism of the proof above; reconstruct the unbarred primary x as p^2+Df. Mixing the unbarred q or D into the barred equations would be a different, unsupported chart.

All tested values are unchanged: primary f, logarithm quotients obtained from f,p, common conjugate f(J_common), and the alternate A. For arbitrary odd raw contacts, the same norm argument decodes their orders. The alternate makes z(P-Q) small at the conjugate place. A nontorsion difference with small z is formal after translating by O or T0; multiplication by 2 removes this possible T0. The half-index comparison therefore remains

```
v(z(P-Q)/z(J_common))=v((alpha(P)-4n)/j).
```

The new case P-Q=T0 has A=0, [2](P-Q)=O and alpha(P)-4n=0. Both sides have infinite valuation. This explicitly closes the additional case not admitted by the previous B!=0 chart. No logarithm of a nonformal point is asserted. Private indices remain half-integers; the root indices and j remain ordinary integers. Integrality of the private indices at odd primes is all that the subsequent congruence argument needs.

Each raw-contact occurrence may select its own orientation of sqrt(2). Every conclusion used globally is a congruence for the same rational root indices at the rational prime, so no shared orientation is required for soundness. The first and second height contradictions, their strict cutoffs, and the root height targets are unchanged.

For completeness use the previous points in G, which already avoid the old difference-chart exceptions, and assign the four new shared values for each target. The explicit forward map gives all new private witnesses. Assign any local Lucas-residual evaluation coordinates if that separate replacement is included. Only after every tested field coefficient is fixed choose the global theta or each private conic theta, according to the selected norm layer. This order accounts for denominators in the new shared coefficients, A and K. No new simultaneous choice of numerator points or CRT condition is needed.

## Exact source gate and scope

An integrating checker must independently reconstruct the four shared equations for each of the five targets and the three private equations at each of the 145 sites. It must verify the actual target map and conjugations, retained nonzero common-point boundary, original root/doubling/height coordinates, unchanged G and scalar equations, and complete incidence of the deleted x coordinates. In the inspected emitter, the old target-F interface slots are deliberately retyped to r=J/conjugate(q), while q remains the target q and three new pairs s,t,u are appended. This requires an explicit new boundary contract; the old F,q contract cannot be reused under the old meaning.

The proposal replaces seven private field pairs f,x,p,t_den,M,T_den,A by four f,p,A,K and adds four shared pairs for each of five targets. The raw difference is 145*6-40=830 rational coordinates. This is an allocation calculation, not a measured final saving.

The chart can compose with private-conic compression because it recovers exactly the same tested field values and the conic theorem permits arbitrary coefficients. It can also compose with the separately reviewed direct Lucas residual because the retained quotient congruences are unchanged. Such combinations need new, explicit source contracts and full independent reconstruction; the earlier 435-field contract is not automatically extended. No new published or unpublished arithmetic input is introduced by the chart itself.
