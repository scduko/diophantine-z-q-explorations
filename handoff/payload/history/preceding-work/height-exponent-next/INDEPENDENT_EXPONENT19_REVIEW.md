# Independent review of the exponent-19 height proposal

Reviewed 2026-11-05. Scope: the new height-transfer argument in
`PROVISIONAL_EXPONENT19.md`, compared with the current manuscript's LR3,
LR5 and LT1--LT7 arguments and the published sources specified below. This
review does not reprove the inherited geometric construction, modularity,
conductor bounds, CM estimate or metric comparison. It does not certify a
changed arithmetic source, revised downstream precision parameters or a
new polynomial. No heavy computation or shared-file edits were performed.

I found no remaining mathematical obstruction to the proposed bound

    h(a) <= H_19 M_5(a)^19,
    H_19 = 2 A_19 B_*^19 + 128,
    A_19 = 2^109 * 210^1800,
    log_2 H_19 < 2093966,

under the exact inherited inputs. The smaller modular Jacobian contains the
needed constituent over the required field, and the complete isogeny-height
transfer fits the stated constant. One initially incorrect quotient identity
was reported and corrected during review. The corrected proof uses the
effective diamond group.

## Inherited assumptions and character order

The current manuscript supplies a normal field `L'/Q` with
`d'=[L':Q]<=2304R`, an absolutely simple non-CM surface `A`, a modular
two-dimensional representation `r`, and on `G_L'` the identities
`V_l(A)=r+r` and `(det r)^2=chi_cyc^2`. It also supplies
`N<=210^300 R^2` and `rad(N)|R`. The proposal must retain the latter support
condition, not merely the numerical level bound.

Put `delta=det r/chi_cyc` in the manuscript's Tate convention. Then
`delta^2` factors through the finite group `Gal(L'/Q)`. If its image has
order `s`, then `s|d'` and every value of `delta` is a `2s`-th root of unity.
Thus `ord(delta)<=2d'`. This reasoning does not require the coefficient
field to have bounded degree. A faithful coefficient-field embedding preserves
the order and the kernel of the character.

For the primitive weight-two form after the finite twist has already been
absorbed, the finite determinant character is its nebentypus, up to the
inverse in the opposite convention. An inverse changes neither order nor
kernel. The argument must use that final form, not the auxiliary sign-splitting
character that appeared earlier. Weight two gives `epsilon(-1)=1`. Hence
`t=ord(epsilon)<=4608R`, and `-I` belongs to `Gamma_H` for
`H=ker(epsilon)`.

This is a consequence of the accepted compatible representation and modular
determinant identities. It does not assert a new bounded-degree coefficient
field, a bounded-degree rational model of every newform factor, or a bounded
full scalar-splitting field.

## Quotient field and the required newform factor

There is no cyclotomic field-degree penalty for `X_H`. Mascot's published
Section 2.1 describes `X_H`, its diamond operators and its rational model,
including the lower-right-entry convention in (2.1.8). The moduli model is
over `Q`, even though full-level `X(N)` initially has a cyclotomic model.
Thus both the quotient and its Jacobian are defined over `Q`.
See [Mascot, Research in Number Theory 8 (2022), 48, equations
(2.1.5)--(2.1.8)](https://link.springer.com/article/10.1007/s40993-022-00329-6).

The following version makes the factor argument precise. Let
`q:J_1(N)->A_f` be the standard newform quotient. Its pulled-back
differentials are spanned by the Galois conjugates of `f`. Each diamond
`<h>`, `h in H`, fixes those differentials, because the eigenvalues are
the conjugates of `epsilon(h)=1`. Therefore `q o <h>=q`: in characteristic
zero a homomorphism of abelian varieties with zero differential is zero.
Consequently `q e_H=q` for the rational averaging projector `e_H`. These
newform and diamond conventions are explicit in [Baker, González-Jiménez,
González and Poonen, Sections 3.1 and 3.2.1](https://math.mit.edu/~poonen/papers/finiteness.pdf),
especially author-PDF pages 9 and 11. Shimura's original Theorem 1 also
constructs the rational quotient and its differential space for intermediate
level groups: [J. Math. Soc. Japan 25 (1973), pp. 525--526](https://www.jstage.jst.go.jp/article/jmath1948/25/3/25_3_523/_article).

Let `H_eff` be the image of `H` in `Aut(X_1(N))`, and `pi` the quotient
map. Then

    pi^* pi_* = sum_{h in H_eff} h,
    pi_* pi^* = [|H_eff|].

The images of `pi^*` and `e_H` agree up to isogeny, since the normalized
averages over `H` and `H_eff` agree. The restriction of `q` to this image
is surjective. Hence `A_f` is a `Q`-isogeny factor of `J_H`.

The first draft instead summed over all of `H` while using the effective
quotient map. That formula had an extra factor from the trivial action of
`-1`. For `N>2` the factor is two. The author replaced it with the effective
formulas above. The corrected version was read back and is sound.

This proof uses the whole Galois orbit, so it does not confuse one complex
eigenspace with a rational abelian subvariety. It also avoids asserting that
an arbitrary factor of `J_1(N)` survives every diamond quotient. Only the
factor annihilated by this particular `H` is used.

## Transfer to the quaternionic surface

The accepted realization of `r` in `V_l(A_f)` now places it in
`V_l(J_H)`. Over `L'` it is a constituent of `V_l(A)`. A nonzero Hom space
after scalar extension remains nonzero before scalar extension; semisimplicity
and Faltings' Hom theorem yield a nonzero `L'`-homomorphism `A->J_H`.
Absolute simplicity gives finite kernel. Poincare reducibility over `L'`
then gives `A x Z` isogenous to `J_H`, with `g=dim J_H>=2`.

No assertion is needed that all geometric factors of `A_f` or `J_H` are
isogenous to `A`. The complement and the surface need not be principally
polarized. A polarization of the Jacobian suffices for reducibility, and the
subsequent general isogeny theorem has no assumed polarization-degree bound.

For the height estimate, the base field in Gaudron--Remond is `L'`, the
source is `J_H`, and the target is `A x Z`, all defined over that field.
The published Theorem 1.9(1) gives both isogeny directions with degree at
most `Xi(J_H)^2`, where the definition of `Xi` has exponent `2g^2`.
Taking half a logarithm gives exactly the proposal's `V`, including its
factor `2g^2`. Section 1.5 explicitly uses the original stable Faltings
normalization. I checked the published pages 7--8, not only an earlier
author version. See [Gaudron--Remond, Mémoires SMF 176 (2023)](https://smf.emath.fr/system/files/filepdf/smf_mem_176_0.pdf).

## Index, Belyi degree and height constants

The lower-right-entry map from `Gamma_0(N)` onto `(Z/NZ)^*` has
`Gamma_H` as the inverse image of `H`. Therefore its index contribution is
exactly `t`. Since `-I` is in `Gamma_H`, the degree of the coarse map to
`X(1)` is the full `SL_2` index, with no additional factor of two:

    d_H = N t product_{p|N}(1+1/p).

This calculation uses the group definition directly. It does not use
Mascot's displayed (2.1.4), whose HTML subgroup quotient is reversed:
`Gamma_H/Gamma_1` corresponds to `H`, while the quotient by `H` corresponds
to `Gamma_0/Gamma_H`. The geometric rational-model statements cited above
do not require that typographical formula.

For every prime `p>=5`, `(1+1/p)^6<=p`; the two possible factors at 2 and
3 multiply to at most 2. Using `rad(N)|R`, this proves
`d_H<=9216 C R^(19/6)<T`, where `C=210^300` and
`T=2^14 C R^(19/6)`. The genus bound `g<=1+d_H/12`, together with `g>=2`,
implies `g<=d_H<T`.

The applicable published modular-curve bound is the generic
`h_F(J(Gamma))<=13,000,000 d_Gamma^5 g_Gamma`, not a formula restricted to
squarefree `X_0(N)` or to trivial nebentypus. The coarse-degree convention
and the stable-height normalization are both explicit in [von Känel,
Forum of Mathematics, Sigma 9 (2021), equations (4.1)--(4.2), p. 8](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/5DA2DC5985591DFBC9A26C20BA22F49B/S2050509421000293a.pdf/the-effective-shafarevich-conjecture-for-abelian-varieties-of-dollartext-gl2dollar-type.pdf).
The underlying [Javanpeykar Theorem 1.1.1 and Section 2.3](https://msp.org/ant/2014/8-1/ant-v8-n1-p04-s.pdf)
apply to a smooth projective geometrically connected curve over `Qbar`;
Section 2.3 identifies its height with the stable height of its Jacobian.
Thus a change from `X_1(N)` to `X_H` introduces no field-of-definition term.

The remaining estimates are elementary and were checked independently.
With `u=log T`, `d'<=2304R` implies

    V <= 16 T^4(2+u) + 2 T^2(25+7u).

For `T>=16`, the two displayed inequalities in the proposal imply that each
summand is at most `T^6/2`. The inequalities hold at 16, and their differences
have positive derivatives on that range. Consequently `V<=T^6`.
The Bost lower bound in the same original metric gives
`h_F(Z)>-3g/2`. The zero-dimensional complement causes no exception.
It follows that

    h_F(A) < (2^24+1) T^6 + 3T/2 < 2^25 T^6
           = 2^109 * 210^1800 * R^19.

The CM estimate `854R` is smaller for all `R>=1`. Finally `M_5(a)>=1`
allows the additive 128 in the geometric comparison to be absorbed into
`H_19 M_5(a)^19`. The numerical exponent is correct:

    2 + 109 + 1800*8 + 19*109445 = 2093966.

The inequalities used here are strict because `210<2^8`,
`B_*<2^109445`, and `A_19 B_*^19>64`.

## What this review establishes and leaves to integration

The new height theorem follows from the stated inherited inputs and the
corrected quotient argument. No unsupported descent, character-order,
polarization or coefficient-field assumption was found. The initial
ineffective-group error has a local correction and does not alter the
constant or exponent.

The theorem is a new proved consequence of the existing arithmetic setup;
it is not an equal-output rewrite of the old polynomial. Every downstream
use of exponent 24 or the old height constant must be revisited explicitly
before changing source precisions, the scalar batch, or the anchor. This
review does not certify those future choices. In particular, the scalar
order 48 would now directly yield the exponent `19/48` in the scalar
height estimate, and a weaker square-root bound may still be used if useful.
Any lower order requires its own divisibility and growth check.

No new quartic count or coefficient pass is implied. The inherited
arithmetic theorem and this height improvement remain mathematical inputs
to the finite source, circuit and expansion checks; those finite checks
do not independently prove the arithmetic inputs.

The corrected substantive draft read for this report had SHA256
`5a91081349010dafd1a0f3f5813639e26436da20ec51e8da7bdf7883675393a8`.
The author is adding the exact published references and the differential
formulation described above. Those additions should preserve this argument;
the final integrated manuscript and source still need their own content pins.
