# Provisional reduction of the five-contact exponent to 19

Status: proposed proof for independent adversarial review. No source change,
new polynomial, or exponent improvement is accepted by this note alone.
The argument retains the accepted H5 geometry, compatible representations,
modularity, level bound and CM branch. It changes the modular curve used
for the non-CM height transfer from X_1(N) to the quotient determined by the
nebentypus kernel.

## Accepted input and conventions

Let a be a rational parameter outside the same five contacts. Put
R=B_* M_5(a), with B_* the product of primes at most 76176. The accepted
proof constructs the non-CM quaternionic abelian surface A/L and a normal
field L'/Q with

    [L:Q] <= 576,  d'=[L':Q] <= 2304R,
    N <= C R^2,   C=210^300,

where N is the primitive level of a weight-two newform f whose compatible
two-dimensional representation r restricts over L' to a multiplicity
factor of V_l(A). More precisely, on G_L',

    V_l(A) = r + r,   (det r)^2 = chi_cyc^2.

The proof uses coefficient prime five and transfers to three to control
the conductor at five. No new local conductor bound is proposed here.
The level may contain prime squares and arbitrary nebentypus.

The coefficient field of f is allowed to vary and is not bounded. Every
representation comparison can be made over an algebraic closure of the
chosen l-adic coefficient field. The determinant character and its order
are independent of a coefficient-field embedding.

All h_F below are original stable Faltings heights. The accepted metric
comparison is

    h(a) <= 2 max(0,h_F(A)) + 128,

where h is the absolute logarithmic Weil height. The accepted CM argument
already gives h_F(A)<854R. Neither statement is altered.

## The nebentypus has order at most 4608R

Let epsilon be the nebentypus of the primitive newform after absorbing
the finite twist in the accepted modularity argument. Use the Tate-module
convention of the accepted comparison, with cyclotomic character taking
the value p on arithmetic Frobenius at p. The modular representation has
det r=epsilon*chi_cyc. Diamond--Im, Section 12.5, equations (12.5.1)-(12.5.2)
and Remark 12.5.1, state this convention: the Frobenius polynomial is
X^2-theta(T_p)X+p theta(S_p), and theta(S_p)=p^(k-2)epsilon(p).
Here k=2. These determinant identities extend from good Frobenius elements
to G_Q by continuity and Chebotarev. In a contragredient convention one
must first dualize the accepted realization consistently; the resulting
finite character is epsilon^-1 and has the same kernel and order. We do
not apply a norm twist to the accepted realization.

Set delta=det r/chi_cyc in the accepted convention. On G_L', delta^2=1.
Consequently delta^2 factors through Gal(L'/Q). Its image is cyclic and
has order dividing d'. Therefore delta has order at most 2d', and

    t=ord(epsilon) <= 2d' <= 4608R.               (1)

This does not bound the degree of the coefficient field. It uses only the
finite determinant character, not a bound on the scalar splitting field.
Because f has weight two, epsilon(-1)=1.

## The smaller modular Jacobian contains the needed factor

Put H=ker(epsilon) in (Z/NZ)^*, and define

    Gamma_H={gamma in Gamma_0(N): lower-right(gamma) mod N lies in H}.

Let X_H=X_1(N)/H, with the standard diamond action, and J_H=Jac(X_H).
The diamond action and quotient are defined over Q, and -1 acts trivially.
The subgroup Gamma_H contains -I because epsilon is even.

Write q:J_1(N)->A_f for the standard newform quotient. Baker--Gonzalez-
Jimenez--Gonzalez--Poonen, Section 3.1, identifies q^*H^0(A_f,Omega) with
the span of the Galois conjugates of f. Their Section 3.2.1 states that
<h> acts on f by epsilon(h). For h in H it therefore acts identically on
that entire span, because every conjugate character also takes the value
one on h. Consequently q composed with <h> and q have the same map on
differentials. Homomorphisms of abelian varieties in characteristic zero
are determined by their differentials: a homomorphism with zero
differential has zero-dimensional connected image and is zero. Hence
q composed with <h> equals q over Q. This avoids assuming in advance
that a selected representative of the quotient carries diamond operators.

Put e_H=|H|^-1 sum_{h in H}<h> in End^0_Q(J_1(N)). Then q e_H=q.
Thus q restricts to a surjection from the image of e_H onto A_f.
Here the image of a rational idempotent means the connected image of any
nonzero integer multiple that is an actual endomorphism; its isogeny
class is independent of this choice. Let H_eff be
the image of H in Aut(X_1(N)); in particular the trivial diamond action
of -1 is removed. For the quotient map pi, the Jacobian maps satisfy
pi^* pi_*=sum_{h in H_eff}h and pi_* pi^*=[|H_eff|]. The normalized
averages over H and H_eff agree, since every effective element has the
same number of preimages in H. Thus the image of the idempotent is
Q-isogenous to J_H. Hence A_f is a Q-isogeny factor of J_H by Poincare
reducibility over Q.

The accepted realization of r in A_f therefore puts r in V_l(J_H).
Over L', it shares a constituent with V_l(A). Faltings' Hom theorem and
scalar extension give a nonzero L'-homomorphism A -> J_H. Absolute
simplicity of the non-CM surface then gives an embedding up to finite
kernel. Poincare reducibility supplies Z/L' and an L'-isogeny

    A x Z -> J_H.                                (2)

In particular g=dim J_H>=2. The quotient Jacobian has its canonical
principal polarization. No principal polarization on the factor A or
the complement Z, and no bounded polarization degree for either, is
assumed. The same general isogeny theorem as in the accepted transfer
is applied with source J_H over L'.

## Belyi degree and genus

The index formula gives the degree of the natural map to X(1):

    d_H=[SL_2(Z):Gamma_H]
       =N t product_{p|N}(1+1/p).

This map is unramified outside the elliptic points and the cusp, so after
normalizing their images its Belyi degree is at most d_H. Its genus obeys
g<=1+d_H/12, and g>=2 implies d_H>=2 and hence g<=d_H.

The accepted conductor support gives rad(N)|R. For p>=5,

    (1+1/p)^6 <= p.

Indeed the left side decreases with p and at p=5 it is
46656/15625<5. The factors at two and three multiply to at most two.
Consequently

    product_{p|N}(1+1/p) <= 2 R^(1/6).

Combining this with (1), define B=2^14 C and T=B R^(19/6). Then

    d_H <= 9216 C R^(19/6) < T,   g<=T,   T>=2^14. (3)

The published generic congruence-curve inequality, von Kanel (2021),
Section 4, equations (4.1)-(4.2), follows from Javanpeykar (2014),
Theorem 1.1.1, with the original stable Faltings normalization. It gives

    h_F(J_H) <= 13,000,000 d_H^5 g < 2^24 T^6.   (4)

No squarefree-level or trivial-character assumption is used.

## Every transfer term

Use exactly the accepted Gaudron-Remond (2023), Theorem 1.9(1),
half-logarithmic isogeny-height variation, and Bost lower bound. From (2),

    h_F(A)+h_F(Z) <= h_F(J_H)+V,
    V=2g^2[8g^2 log(7g)+log d'
                 +log max(1,log d',h_F(J_H))],
    h_F(Z)>-(3/2)g.

Put u=log T. Then log R<=u, log d'<8+log R,
log(7g)<2+u. The upper bound 2^24 T^6 is at least each of
1, log d', and h_F(J_H), so the last logarithm is at most
24 log2+6u<17+6u. Hence

    V <= 16T^4(2+u)+2T^2(25+7u).

For T>=16 the elementary inequalities

    2+log T <= T^2/32,
    25+7log T <= T^4/4

hold, as checked at T=16 and then by differentiating the differences.
Thus V<=T^6. Combining with (4) and -(3/2)g gives

    h_F(A) < (2^24+1)T^6+(3/2)T < 2^25 T^6
           = A_19 R^19,
    A_19=2^109 * 210^1800.                       (5)

The accepted CM bound 854R is also less than A_19 R^19 for R>=1.
The geometric comparison therefore gives the proposed uniform bound

    h(a) <= H_19 M_5(a)^19,
    H_19=2 A_19 B_*^19+128.                      (6)

The existing integer estimate B_*<2^109445 and 210<2^8 imply

    H_19<4 A_19 B_*^19<2^2093966.                (7)

The strict first inequality uses A_19 B_*^19>64.

## Published source locations and review gaps

Already accepted H5 dependencies: manuscript labels LR3, LR5, LT1,
the determinant calculation in the modularity paragraph, the Faltings
Hom/Poincare step in LT1-LT3, the general isogeny variation LT3, the
CM bound, and the metric comparison G. The historical accepted-h5
level-transfer.tex uses an older padded C=210^4000; the current accepted
manuscript and final acceptance receipt use C=210^300.

Published source locations:

- Rafael von Kanel, Forum of Mathematics, Sigma 9 (2021), e39,
  Section 4, equations (4.1)-(4.2), printed p.8, and Section 5.2.1 for
  the newform quotient A_f of J_1(N).
  https://doi.org/10.1017/fms.2021.29
- Ariyan Javanpeykar, Algebra & Number Theory 8 (2014), 89-140,
  Theorem 1.1.1, via the exact congruence-curve formulation above.
  https://doi.org/10.2140/ant.2014.8.89
- Gaudron-Remond, Memoires SMF 176 (2023), Theorem 1.9(1),
  pp.7-8, retained at the exact accepted H5 use and normalization.
  https://doi.org/10.24033/msmf.484
- Baker, Gonzalez-Jimenez, Gonzalez and Poonen, American Journal of
  Mathematics 127 (2005), 1325-1387, Sections 3.1 and 3.2.1. The author
  copy has the newform quotient at PDF p.9 and diamonds at PDF p.11.
  It explicitly identifies itself as the published article.
  https://math.mit.edu/~poonen/papers/finiteness.pdf
- Mascot, Research in Number Theory 8 (2022), article 48, Section 2.1,
  gives the Q-model of X_H and its Q-rational diamond action.
  https://doi.org/10.1007/s40993-022-00329-6
  Its HTML equation (2.1.4) appears to interchange a subgroup and a
  quotient. We do not use that equation. Directly from the definition,
  Gamma_H/Gamma_1 is H and Gamma_0/Gamma_H is (Z/NZ)^*/H.
- Diamond and Im, "Modular forms and modular curves", in Seminar on
  Fermat's Last Theorem, CMS Conference Proceedings 17 (1995), 39-133,
  Section 12.5, pp.119-120, equations (12.5.1)-(12.5.2), Remark 12.5.1.
  The indexed primary scan gives the compatible representation and
  arithmetic Frobenius convention. Direct web rendering is limited by
  its file size; the characteristic polynomial and theta(S_p) formula
  were checked from the indexed chapter text.
  https://wstein.org/msri06/stein/Diamond-Im-Modular_forms_and_modular_curves.pdf
  A second indexed copy explicitly preserves the epsilon factor in the
  printed determinant formula, which some OCR copies omit:
  https://wstein.org/msri06/refs/Diamond-Im-Modular_forms_and_modular_curves.pdf

The new ingredient is the quotient/idempotent argument and determinant
order bound above. Independent review must approve these with the exact
accepted realization or identify a missing premise. No arithmetic source
may be repinned before that review and the full downstream
soundness/completeness revision.
