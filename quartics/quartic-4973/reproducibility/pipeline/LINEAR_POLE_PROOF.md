# A linear local unit in the ordinary pole

This is a new arithmetic source specialization. It does not assert an
algebraic equivalence to the old pole for arbitrary fixed conic witnesses.
It preserves the one-sided pole conclusion used in source soundness, and
proves integer completeness with the same inherited restricted-converse,
descent and forward-rank inputs. No rank condition is omitted.

Retain each private conic theta^2-r*s_c^2=2 and the existing packed fields
and constant-left norm tree W. All field coefficients must be fixed before
choosing this private conic. The statements below apply equally to the
reviewed normalized-Lucas fields when their separate arithmetic proof and
source audit establish that independence. No normalization theorem for
those fields is proved here.

## The local unit lemma

Put g=3-2*theta. Both r and s_c are nonzero over Q, since otherwise
theta^2=2. Let p be an odd prime with k=v_p(r) odd. Then
k+2*v_p(s_c) is odd. If it were negative, the right side of
theta^2=2+r*s_c^2 would have that odd valuation, impossible for a square.
It cannot be zero. Therefore it is positive, theta is p-integral, and

    (3-2*theta)(3+2*theta)=9-4*theta^2=1-4*r*s_c^2

is a p-unit. Each factor is integral, so both are units. In particular
v_p(g)=0. This holds for negative as well as positive odd k. We never
assume that an arbitrary soundness contact is a selected completeness
prime, or impose a congruence class on it.

## Eleven-variable direct form

With free inputs r,theta,W, use private variables
U,L,z,e,p,c,w,s,q,j,k and the nine quadratic equations

    U = r*(3-2*theta)
    L = W*U
    z = L^2
    c = r*e
    p^2-17*r-34*c+51*e*c = 0
    w = c*(17*r-z)
    j = s^2
    k = r*q
    j^2+34*j*w-867*w^2-17*q*k = 0.

Compared with the twelve-variable pole this deletes D and replaces its
first two equations by one equation. All coefficients are integers,
all degrees are at most two, and the maximum absolute coefficient is 867.

## Ten-variable normalized form, with W retained

An exact reversible scaling of that eleven-variable system, followed by
elimination of the now linear coordinate U/r, gives private variables
l,z,e,p,c,w,s,q,j,k and eight quadratic equations

    l = (3-2*theta)*W
    z = l^2
    c = r*e
    p^2-17*r-34*c+51*e*c = 0
    w = 17*e-c*z
    j = s^2
    k = r*q
    j^2+34*j*w-867*w^2-17*q*k = 0.

Subscripts 11 denote the direct form. From a normalized solution set

    U_11=r*g, L_11=r*l, z_11=r^2*z, w_11=r^2*w,
    s_11=r*s, q_11=r^2*q, j_11=r^2*j, k_11=r^2*k,

and keep e,p,c. Conversely divide by precisely those powers of r and
discard U_11, which its first row fixes. Every division is justified by
the retained conic's r!=0. The first-conic row is unchanged and the last
row is multiplied by r^4. The w row becomes
r^2*w=r*e*(17*r-r^2*z). This verifies every equation in both directions,
including all zero values of p,e,s,q,W. No pole witness is assumed nonzero.

## Complete replacement for the old negative-odd proof

It suffices to prove this for the normalized system. Let b=r*W^2. If W=0,
then b=0 and there is no nonzero pole-input conclusion to prove. Suppose
b!=0 and, toward a contradiction, v_p(b)<0 is odd for an odd prime
p outside {3,17}. Write a=v_p(r), t=v_p(W); then a is odd and
v_p(b)=a+2t. The local unit lemma gives v_p(l)=t.

The first conic is exactly

    p_witness^2=17*r*(1-e)*(1+3*e).

If e=0 its right side has odd valuation a, impossible. If v_p(e)>0,
the right side again has odd valuation a. If v_p(e)<0, both factors
have valuation v_p(e), so the right side has odd valuation
a+2*v_p(e). Therefore e!=0 and v_p(e)=0. This includes p_witness=0
and e=1 or -1/3, rather than excluding these branches.

Now w=e*(17-r*l^2). Since v_p(r*l^2)=a+2t=v_p(b)<0,
w is nonzero with the negative odd valuation v_p(b). The final equation is

    (s^2-17*w)*(s^2+51*w)=17*r*q^2.

If s!=0, the even valuation of s^2 differs from the odd valuation of w,
so both factors on the left have the same finite valuation and their
product has even valuation. If s=0, that product is -867*w^2, nonzero
with even valuation because p is outside {3,17}. The right side is
either zero, when q=0, or has odd valuation a+2*v_p(q). Both cases are
impossible. Hence v_p(b) is not negative odd for every p outside
{2,3,17}, precisely the assertion used by the existing norm argument.

This proof replaces the old Cayley/norm-identity step explicitly. It is
not a claim that the new witnesses satisfy the old Cayley equation.
Every downstream soundness use of Psi must consume only the stated
negative-odd exclusion. The ordinary norm soundness does so; the scalar
height module keeps its original Psi call unchanged.

## The generalized fixed-U completion statement

The proof of the manuscript's seven-witness completeness theorem gives
the following statement. Let b>0 have square reduced denominator and be
a square in Q_2,Q_3,Q_17. Put B=17*b. A prescribed rational U_o suffices
if

    U_o^2/B < 1 at infinity,
    v_2(U_o^2/B)>=3,
    v_3(U_o^2/B)>=1, v_17(U_o^2/B)>=1,

and v_p(U_o)=v_p(b) at each prime p outside {2,3,17} with v_p(b) odd.
Under these hypotheses there are e_o,p_o,h_o,s_o,q_o satisfying the
old first-conic, h and last-conic equations. No Cayley equation for U_o
is part of this statement.

For completeness, put V=B*(B-U_o^2). The inequalities make V positive
and a local square at 2,3,17. Let beta,eta be the positive squarefree
representatives of B,V. Then beta=17 mod24 and beta>1; eta=1 mod24
and 17 does not divide eta. At an odd-support prime of beta outside
the exceptional set, the square denominator makes v_p(b) positive.
The prescribed valuation equality gives v_p(U_o^2/B)=v_p(b)>0, so
1-U_o^2/B is a square unit. Thus eta is a square there, and the supports
are disjoint. At 17 this follows from the explicit smallness condition.
Conversely, odd valuation of V at an eta-support prime forces
v_p(B)=2*v_p(U_o) and strict cancellation in B-U_o^2; hence B/U_o^2
is a square unit. If U_o=0 then V=B^2 and eta=1, so this converse step
is unnecessary. These are exactly the mutual-square hypotheses of the
existing simultaneous-realization lemma. Its positive n,n*eta, rank-one
and Kummer realization argument, and all nonzero divisions in recovering
the three witnesses, are unchanged. No unpublished converse or altered
rank hypothesis is introduced.

## Integer completeness

Follow the current ordinary-contact completeness construction until
r=d0^2*p0, its private elliptic/ratio data and all field coefficients are
fixed. The selected p0 exceeds 76176. The raw r is positive and locally
square at 2,3,17. The existing conic has a rational point and weak
approximation. Choose its rational point simultaneously near the old
selected-prime target (sqrt(2),0), to the same required depth, and near

    (theta,s_c)=(3/2,1/(2*sqrt(r)))

at infinity, 2,3 and17. The latter points exist under precisely the
unchanged local-square hypotheses. Since each packed field and W is a
polynomial in theta after the field data are fixed,

    R(theta)=(r/17)*W(theta)^2*(3-2*theta)^2

is continuous and vanishes at theta=3/2 at all four places. It can meet
the four strict smallness/valuation conditions above. There is no
denominator near this target, including at2.

The old selected-prime argument still makes W a p0-unit. Its real
constant-left norm tree still gives W>=1 because r>0. Therefore
b=rW^2>0, has square reduced denominator and is a local square at2,3,17.
Set U_o=W^2*r*g. At every prime where v_p(b) is odd, v_p(r) is odd;
the local unit lemma gives v_p(U_o)=v_p(b). Moreover
U_o^2/(17*b)=R(theta). The generalized completion statement applies.

Recover the direct eleven-variable witnesses from the old three conics
using the nonzero W rescalings in PARITY_SCALE_PROOF.md, and set
U=r*g, L=WU. Equivalently use the exact r scaling above to obtain the
ten-variable form. Every old conic/field/root datum remains fixed, and
all rank/descent dependencies are those already stated. This establishes
integer completeness of the changed ordinary module.

## Zero branch and source obligations

For the normalized form W=0 has the explicit solution
l=z=p=q=k=0, e=1,c=r,w=17,s=17,j=289, for every retained rational conic.
For the direct form apply the exact r scaling. Thus W=0, zero parity
ordinates and the first conic's torsion endpoints have not been discarded.

Use this only for the37 ordinary private-conic calls. Require the exact
same r and theta, all existing conic/field/norm constraints, coefficient
independence, and the unchanged scalar-height module. Replace the
arithmetic assertion consumed by the ordinary batch with the explicitly
proved negative-odd exclusion. Bind any combined constant-path rewrite
separately by exact rational maps. The direct form saves one local
variable and row; the normalized W-retained form saves two of each
against the12-variable block. These are local counts, not measured
whole-artifact savings, and must not be added to overlapping path savings.
