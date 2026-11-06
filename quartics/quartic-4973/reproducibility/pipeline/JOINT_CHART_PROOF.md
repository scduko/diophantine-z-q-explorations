# A joint four-field primary and difference chart

This research packet is separate from every frozen source and Version 3.
It combines the primary curve equation with the two-denominator difference
graph. It leaves the functions tested by the arithmetic source unchanged.

## Shared target coefficients

Work in K=Q(sqrt(2)), with d=3-sqrt(2), D=d^2, and E: y^2=x^3-Dx.
Let the retained target Q=(a,aq) be nonidentity and non-two-torsion, and put

    F=1/a, c=a+DF, J=1/z(J_common),
    r=J/q, s=c/q, t=1/q^2, u=r*s.                       (1)

Here J is the reciprocal parameter of the unchanged common nonzero point;
it is not the name of an index. Both J and q are nonzero. The target is
still an actual quadruple of a retained nonzero root point in G=2E(K).
In particular q^2=a-DF and

    c^2-q^4=4D.                                        (2)

Four shared field pairs per target suffice for r,s,t,u. They are specified
quadratically and uniquely by

    rq=J, sq=c, t(a-DF)=1, u=rs.                       (3)

There are five targets, so this adds 40 rational root coordinates. The
old F,q values and original affine target coordinates are retained.

## Three equations in four private field variables

Use only f,p,A,K for each primary/difference pair and impose

    K=(A-r)p,
    Kp+up-2Drf-4DtA=0,
    2D(A+r)f+sK+4DtA+Jq=0.                             (4)

All three equations are quadratic. No separate primary x variable or
primary curve equation is imposed. The original G equations use f and p
exactly as before, and the alternate test is A exactly as before.

The formulas in this proof use un-conjugated coordinates for readability.
The source alternate is A=conj(z(P-Q))*jz, where jz=1/conj(z(J_common)).
Accordingly its three equations use conj(f), conj(p), conj(D), conj(q),
and the shared coefficients obtained by replacing q,c,J in (3) with
conj(q),conj(c),jz. These are literal field conjugations, so every argument
below applies verbatim.

## Recovery of the curve and the graph

For any solution of (4), define

    x=p^2+Df, L=Ap=K+rp, Z=A/J.                        (5)

Writing the second equation of (4) as E and the third as E2, put E1=2E+E2.
Then (4) gives

    E1 = 2(A-r)x+sL-4DtA+up+Jq = 0,
    E2 = 2D(A+r)f+sL+4DtA-up+Jq = 0.                  (6)

Using (1), multiplying the sum of (6) by q/2 gives

    A[q(x+Df)+cp] = J[x-Df-q^2].                      (7)

Multiplying their difference by q^2/2 gives

    A[q^2(x-Df)-4D] = J[q(x+Df)-cp].                  (8)

The multipliers 2,q,q^2 are nonzero, so these operations are reversible.
Let

    U=q(x+Df)+cp, V=q^2(x-Df)-4D,
    H1=q(x+Df)-cp, H2=x-Df-q^2.

Equations (7),(8) give ZU=H2 and ZV=H1. Their eliminant is

    H2*V-H1*U = -4Dq^2*(fp^2+Df^2-1),                (9)

after the substitution x=p^2+Df and the target identity (2). The left
side vanishes because ZU=H2 and ZV=H1. Since Dq is nonzero, (9) forces

    fp^2+Df^2=1, hence xf=1.                          (10)

Thus f and x are nonzero and P=(x,xp) lies on E. The unchanged G equations
force p nonzero by the same global nonvanishing argument as in the frozen
rational-difference proof. No extra real or squareclass assumption enters.

For completeness, the exact two-denominator graph has no hidden component.
If U=V=0, then p=-2v/q for v=d or v=-d, and

    x=v(c+2v)/q^2=v(a+v)/(a-v).

These are exactly P=Q+(v,0), the two actual poles of z(P-Q). At those
points H2=(4D-q^4)/q^2 is nonzero. Indeed q^4=4D would force q^2=2d or
-2d, and taking norms would give N(q)^2=28, impossible over Q.
Consequently neither pole can solve (7). At every other P, U or V is
nonzero, so Z is uniquely determined. The identities

    H*U=N*H2, H*V=N*H1,
    H=(p-q)(1+DfF), N=pq(1-DfF)+2D(f+F)

identify Z with z(P-Q) on the ordinary chord domain and hence everywhere
the function is regular. The independent two-denominator proof in the
parent folder gives the same calculation in full.

Conversely, take a nonidentity, non-two-torsion P on E for which P-Q is
not one of the two actual poles. Put f=1/x, p=y/x, Z=z(P-Q), A=JZ and
K=(A-r)p. The two graph identities hold. Reversing (6)--(8) yields (4),
using x=p^2+Df. This gives exact rational forward and reverse maps on the
stated domain, fixing P, Q and the alternate value A.

No inverse of A, K, U, V, an index difference or a difference logarithm
was taken. At P=Q and P=Q+(0,0), Z=A=0 is allowed. At P=-Q and
P=-Q+(0,0), U=H2=0 but V=q^4-4D is nonzero and gives the correct unique
value. The source therefore handles identity, opposition and every
removable denominator case explicitly.

## Arithmetic and source incidence

The primary functions f,p and the alternate A are exactly those of the
reviewed rational-difference source. The same half-index proof therefore
gives all odd-prime local conclusions. The additional difference (0,0)
has A=0, double O and zero index difference, so its logarithmic valuation
is infinite on both sides. The other two nonzero two-torsion differences
are excluded as actual poles by (7),(8).

Every old complete witness gives the new witnesses by the forward map.
All target coefficients are fixed before choosing theta. No retained
norm/pole or integrality guard changes. The literal tested values also
allow composition with the separately reviewed conic field-test layer.

The removed x coordinate had only two consumers in the exact comparison
module: its primary curve equations and the replaced difference block.
All G polynomials, log-ratio equations, field tests and calls use f,p,A.
An independent module reconstruction must check this full incidence,
the exact shared target coefficients, every ordered mode boundary and
the unchanged test list. Outer source hashes, full flattening and finite
replay remain separate obligations.

The tiny independent test verifies both normalization identities (7),(8)
and the exact eliminant (9) symbolically. It checks the source's conjugated
equations at 34 valid K-points, including all four listed exceptional
configurations, and rejects the two genuine poles. Expanding the six
rational component equations gives degree two and maximum absolute
coefficient 88. This does not replace the final expanded-quartic bound,
which must be checked after the complete lift and elimination.

The four-field rational source used seven private field pairs per site:
f,x,p,t,M,T,A. The joint chart uses four: f,p,A,K. For 145 sites this
removes 870 raw rational coordinates, while (3) adds 40 shared ones.
The net allocation estimate is 830, not a measured final reduction and
not additive to another independently measured endpoint.
