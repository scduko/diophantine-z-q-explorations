# Two equations for the difference parameter

This is a new research extension of the frozen rational-difference packet.
It does not alter Version 3 or the frozen packet. All primary f,x,p charts,
G polynomials, primary ratios, contact assignments, scalar and anchor
constraints remain. The alternate field value is exactly unchanged.

## Exact graph

Use K=Q(sqrt(2)), d=3-sqrt(2), D=d^2 and E: y^2=x^3-Dx.
Let P=(x,xp), Q=(a,aq) satisfy the retained primary/target constraints

    xf=1, p^2=x-Df, aF=1, q^2=a-DF.

The surrounding G equations make p nonzero. The target is still a retained
nonzero quadruple in G=2E(K), so a,F,q are nonzero. Put

    c=a+DF,
    U=q(x+Df)+cp,             H2=x-Df-q^2,
    V=q^2(x-Df)-4D,           H1=q(x+Df)-cp.              (1)

Then the graph of Z=z(P-Q), where z=-x/y and z(O)=z((0,0))=0, is

    ZU=H2,                   ZV=H1.                    (2)

The only excluded differences are the genuine poles (d,0) and (-d,0).
There is no additional denominator exception. In particular P=Q,
P=-Q, P=Q+(0,0), and P=-Q+(0,0) are all covered.

To verify the identities, write B=1+DfF, k=q-p and

    N=pq(1-DfF)+2D(f+F),       H=(p-q)(1+DfF).

On the open set B*N nonzero the preceding rational chart gives Z=H/N.
Direct reduction using p^2=x-D/x and q^2=a-D/a gives

    HU=NH2,                  HV=NH1.                   (3)

These polynomial identities can also be checked from the chord law.
They imply (2) wherever z(P-Q) is defined by continuity of rational maps.
The following common-zero calculation proves that (2) has exactly that
graph, including all points omitted by the preceding open chart.

First q^4 cannot equal 4D. Such equality would give q^2=2d or q^2=-2d,
and taking K/Q norms would give N(q)^2=28, impossible for rational N(q).
Also c=(a^2+D)/a is nonzero by total positivity of D.

Suppose U=V=0. From V=0 we have p=-2s/q for one s in {d,-d}.
The U equation gives x+Df=2sc/q^2, while x-Df=p^2=4D/q^2.
Adding the two identities gives

    x=s(c+2s)/q^2=s(a+s)/(a-s).

The denominators a-s and a+s are nonzero because Q is not two-torsion.
Together with p=-2s/q, this is exactly the addition formula for
P=Q+(s,0). Conversely those two points give U=V=0. At either point,

    H2=(4D-q^4)/q^2 != 0.

Thus (2) has no solution at either genuine pole. At every other primary
point at least one of U,V is nonzero. Equations (2) then determine Z
uniquely, and (3) identifies it with the actual difference parameter.

The special values are explicit. At P=Q and P=Q+(0,0), H1=H2=0 and
V=q^4-4D is nonzero, so Z=0. At P=-Q and P=-Q+(0,0), U=H2=0 but
V=q^4-4D remains nonzero, and H1 is respectively 2qc and -2qc.
Therefore the equations still determine the correct unique value.

## Three private field pairs

Let jz=1/conj(z(J)) be the same nonzero shared boundary value as in the
frozen packet, and let A=conj(Z)*jz be the existing alternate test.
Precompute once for each of the five targets

    Bq=jz*conj(q),           Bc=jz*conj(a+DF).           (4)

The root already retains a,F,q and jz. Equations (4) use two additional
field pairs per target. Pass the existing a and the two new pairs along
with the old F,q boundary. No root point or height target changes.

At each comparison site allocate just U,V,A and impose

    U=q(x+Df)+(a+DF)p,
    V=(a-DF)(x-Df)-4D,
    A*conj(U)=jz*conj(x-Df-a+DF),
    A*conj(V)=Bq*conj(x+Df)-Bc*conj(p).                 (5)

Every component equation has degree at most two, because D is a fixed
constant and every other factor in (5) is linear in the displayed source
coordinates. The shared products in (4) prevent cubic coefficients in
the last equation. The first right-hand side uses q^2=a-DF; it does not
need a separately allocated q^2.

Forward: take the actual Z, set A=conj(Z)*jz, and use (1) for U,V.
Reverse: jz is nonzero, so recover Z=conj(A/jz). The first two equations
give U,V and the last two give exactly (2). The common-zero argument
therefore recovers the unique actual difference. This establishes exact
projection equivalence onto all retained primary/target data and A on
the stated genuine-pole domain. It introduces no inverse of U, V, A,
an index difference or a difference logarithm.

Relative to the previous four-field open chart, the new equations also
admit P=-Q+(0,0) and P=Q+(0,0). They are actual elliptic differences, not
extra components. Thus the claim is not a bijection of every old private
witness tuple with every new one.

## Arithmetic interface

The alternate test A, its order and every other tested field value are
unchanged. The frozen half-index argument applies to every non-torsion
difference and to O. The additional possibility P-Q=(0,0) has Z=A=0;
translation by (0,0) gives O, its double is O, and its half-index
difference is zero. Both sides of the logarithmic valuation identity
are therefore infinite. The other two nonzero two-torsion differences
remain excluded as actual poles by (5).

Consequently the same odd-prime local congruences, integer root-index
height arguments and input soundness theorem follow. Completeness uses
the old chosen points, which already avoid the old open-chart exceptions,
and the explicit forward construction above. The shared coefficients
are fixed before theta is chosen. The old theta-last CRT and norm/pole
completeness argument is unchanged. No retained pole or integrality guard
has been weakened.

The independent tiny test checks both identities (3), their connection to
the earlier chord identity, 34 valid exact K-point cases and both genuine
pole rejections. It includes all four special cases described above.
Direct rational-component expansion of the primary and new graph rows
has degree two and maximum absolute coefficient 386. The new shared-root
products are also quadratic. A final expanded quartic coefficient bound
still requires the full source lift and replay.

## Incidence and expected size

The three-field presentation replaces only the private difference block.
Its output A is the same field expression consumed by the old alternate
tests or by the proposed conic field tests. U and V have no outside users.
An integrating auditor must reconstruct both equations of (4), every
equation of (5), exact mode boundaries and every ordered test/call, in
addition to the existing full source/map checks.

There are still 145 sites. Dropping one private field pair saves 290 raw
rational coordinates, while the ten shared field pairs add 20. The net
allocation estimate is 270, before any downstream elimination. Passing
already allocated root a coordinates adds no root variables. No measured
endpoint count or additive final saving is asserted.
