# Complete Jacobi difference charts

This is a proposed change to the arithmetic source. It is not a local
certificate rule for the released affine subtraction chart. The released
chart excludes equal abscissas; the chart below permits both equal and
opposite points. The integer projection needs the arithmetic argument in
this note as well as the finite source checker.

The base is the released 12,504-variable construction. Its manuscript is
`work/quartic-12504-release/public-repository/quartic_12504.tex`, SHA-256
`38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37`.
In particular, the accepted inputs remain the curve/group identification,
formal-group facts, mixed 64/16 reciprocal estimates, norm/pole theorem,
41-contact pattern, height exponent 24, anchor 24 and scalar order 48.
No smaller arithmetic constants are asserted here.

## The two-point chart

Work in K=Q(sqrt(2)), with d=3-sqrt(2), D=d^2=11-6sqrt(2) and
E: y^2=x^3-Dx. Both real embeddings of d and D are positive. N(d)=7.
Let P=(x,y) and Q=(a,b) be nonidentity points with coordinates in K and
choose nonzero u,U in K such that u^2=1/x and U^2=1/a. Put

    p=y/x, q=b/a, h=u p, H=U q.

Then h^2=1-Du^4 and H^2=1-DU^4. The primary compressed chart supplies u,p,x.
The shared target chart described below supplies U,q.

Introduce five field variables r,v,w,T,Z and impose

    r = u U,
    w = r v,
    v + D r w = q-p,
    T = 2x-pq+2pv,
    Z T + q-p = 0.                                      (J)

Every component is a polynomial of degree at most two in rational
coordinates. These equations determine all five variables uniquely.
For the proof write

    k=q-p, B=1+D r^2,
    N=uH-Uh=rk,
    C=hH(1-Du^2U^2)+2D uU(u^2+U^2).

B is strictly positive in both real embeddings, so B is nonzero. The exact
forward formulas are

    r=uU, v=k/B, w=N/B, T=C/(rB), Z=-k/T,
    h_R=Tr/B=C/B^2.

The identity

    C^2 + D N^4 = B^4                                  (1)

follows on substituting h^2=1-Du^4 and H^2=1-DU^4. Thus
h_R^2=1-Dw^4. The element h_R cannot vanish. Otherwise D w^4=1, and taking
norms after d w^2=1 or -1 would give 7 N(w)^2=1, impossible for rational
N(w). Therefore T is nonzero as well. This proves that every denominator
in the forward formulas is nonzero, even when k or w is zero.

Conversely, any solution of (J) first gives r=uU and
Bv=k, hence v=k/B and w=N/B. Substitution in the T equation gives
TrB=C, and its last equation gives Z=-k/T. Thus no additional component
or choice is hidden by the quadratic presentation. This gives exact
two-way rational maps between (J) and the complete two-point graph with
the two chosen input lifts. It fixes all primary and target inputs.

For w nonzero define

    R=(1/w^2, h_R/w^3).

Equation (1) puts R on E and Z=-x(R)/y(R)=-w/h_R. For w=0 define R=O and
Z=0. The identities agree with P-Q. One direct verification away from
x=a uses the line of slope (y+b)/(x-a). The cleared abscissa and ordinate
identities are checked independently by `test_jacobi.py`. This equality
of rational maps extends to the remaining points. Its explicit cases are
as follows.

* If P=Q, either input square-root sign is allowed. Then k=w=Z=0 and
  h_R is 1 or -1. Both lifts represent O.
* If P=-Q, the formula represents 2P. There is no equal-abscissa division.
  Since the input lies in the torsion-free group G=2E(K), P=-Q cannot
  simultaneously mean P=Q for these nonidentity inputs.
* More generally w=0 implies k=0. The relation p^2=x-D/x is injective in
  x on these K-points: equality for x,a gives
  (x-a)(1+D/(xa))=0, and 1+D/(xa)=B is nonzero. Thus x=a,y=b.
* Changing either chosen square-root lift changes w,h_R by a common
  sign, so R and Z are unchanged. All equations and order-one w tests
  tolerate this sign choice.

For normalization, on the Jacobi quartic dx/(2y)=-du/h. With U,H fixed,
implicit differentiation gives

    h dw/du = h_R.

At u=0,h=1 the formula has w=-U,h_R=H and represents -Q. This fixes the
translation sign and invariant differential. The derivative, (1), both
cleared chord identities and TrB=C are five separate exact polynomial
reductions in `test_jacobi.py`. Six exact K-examples also check P=Q with
both lifts, P=-Q, Q=2P and Q=4P with both lifts. The inputs in these
examples have nonzero x,y,u and lie on the curve.

## Shared target square roots

The five targets are [4]P_* and [4]A,[4]S,[4]T,[4]Z. The existing root
module retains their affine x,y coordinates and the two doubling chains.
For each target add U,q,F_Q and the three field equations

    a F_Q=1, U^2=F_Q, q a=b.                            (S)

The targets are nonidentity because the original root inputs lie in the
torsion-free group G and are nonidentity. Their coordinates are nonzero.
These equations have K-solutions. If Q=[2]V and V=(x_V,y_V), choose

    U = 2 y_V/(x_V^2+D), F_Q=U^2, q=b/a.

The denominator is nonzero by positivity, y_V is nonzero, and the standard
doubling formula gives U^2 a=1. Conversely (S) retains the original target
point and supplies exactly the required lift. The root module adds 30
rational coordinates and 30 rational equations once, shared by all 41
comparison calls. Only the four slots of each comparison target change
from a,b to U,q. All root affine coordinates, denominator-cleared height
targets, root formal parameters and both common auxiliary points remain.

In any future root-37 composition, the height targets must still be the
eight coefficients of the original x(A),x(S),x(T),x(Z), not U or q. This
packet's checker is deliberately bound to the released 41-contact root.

## Arithmetic consumption

In the comparison module change only the five conjugate order-one tests
for f(P-Q) to conjugate(w). Keep the eleven-test ordering, the five
conjugate Z/z(J) tests, all primary tests, the common J with its inverse,
all G polynomials and ratios, and every assigned order. In particular,
there is no inversion of the difference logarithm or of w or Z.

At any split good prime used by the released soundness proof, if w is
nonzero then f(R)=w^2. Thus v(w)>0 is equivalent to v(f(R))>0 and puts R
in the formal group. If w=0, R=O is already in that group. In the nonzero
case h_R^2=1-Dw^4 gives v(h_R)=0 and v(Z)=v(w). Set log(O)=Z(O)=0.
The formal logarithm is a homomorphism, so for J=[j]P_* nonidentity and
R=[m]P_* in this formal group,

    v(Z(R)/Z(J)) = v(m/j),

with both sides infinite when m=0. The denominator log(J) remains
nonzero by the unchanged guarded point and formal logarithm isometry.
Consequently the five alternate tests imply exactly the same congruences
h=4 mod p^64 and m_i=4n_i mod p^e_i as in the released theorem. The
possibility of equality or opposition between the input points creates
no additional integer indices outside those congruences. The original
primary nonvanishing proof, ratio interpretation, radical divisibilities,
height bounds, Lucas argument and beta=n conclusion then apply unchanged.

For completeness use the same released choices of private indices h_p,
including avoidance of 0,4,-4, and the same target and primary points.
The shared target lifts exist by (S), and (J) has the stated rational
values. Each required difference was formal in the old construction, so
v(w)=v(Z) is at least one, and can be made as deep as needed by the same
private congruence. The five alternate tests are literally unchanged.
Choose the common approximation theta last, now including the finitely
many new coefficients of conjugate(w), to satisfy both rational tests
epsilon B and A+theta B. This is the same finite CRT argument.

The norm batch is then rebuilt for these new rational leaves. Every raw
contact in this direction is the same positive prime r with the required
local squareclasses. At r the normalized leaves are integral and the
all-left constant leaf makes the norm root a unit. The real norm root is
positive, and r times its square has square reduced denominator and is a
local square at 2,3,17. These facts do not require w to be integral at those
three primes. Hence the original pole-completeness input still supplies
the witnesses. The scalar batch has not changed.

This proves the integer projection under exactly the arithmetic inputs
of the released theorem. It does not give a rational reverse map into
the old guarded difference chart at P=Q or P=-Q. Such a claim would be
false. Finite source checking and later quadratic-lift checking establish
different parts of the construction and must be reported separately.

## Source incidence and coefficient effects

`build_jacobi_source.py` first regenerates and compares all six released
modules using pinned released compiler bytes. It installs the change in
a fresh builder. Every q_compare4 call must have the same old 20-coordinate
target boundary; unexpected callers, lengths or differing targets fail.
Only that boundary is replaced. `check_jacobi_source.py` imports no
producer. It reconstructs the entire new root from the pinned old root,
checks every new comparison core row after expanding only acyclic
arithmetic definitions, checks all ordered call arguments, checks the
four unchanged modules and reconstructs every flattened row and map.

The old local slope, intercept, output x,y,f,z and abscissa guard have no
outside consumer except the replaced formal/alternate tests. Exact module
and call reconstruction is the outside-use guard; this packet does not
permit applying (J) to arbitrary unexamined local incidence. Root x,y and
z coordinates are retained. All rational component coefficients in (J)
have absolute value at most 22 before primitive normalization. All new
root equations have coefficients at most 2 and degree at most two. This
does not by itself bound the final expanded quartic, which needs a fresh
lift and coefficient check.

Per comparison, the five old differences have 13 rational coordinates
each, while the five new differences have 10 each. The source allocation
estimate is therefore 41*15-30=585 fewer coordinates. Relative to the
released optimized endpoint, which already eliminated old intermediates,
the tentative structural estimate is 41*5*2-30=380. Neither estimate is a
measured final variable count. Neither may be added to another proposal
without one combined construction and exact replay.
