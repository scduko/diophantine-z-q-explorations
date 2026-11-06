# Publication-readiness proof inventory, version 2

This new snapshot leaves publication-readiness/ and every published file
unchanged. It is a preparation record, not publication approval. Full hashes
and byte counts are in [PROOF_PINS.json](PROOF_PINS.json). The executable
freeze_pins.py checks artifact bytes only. Proof scopes and dependencies are
recorded below and in LEMMAS.json and CURRENT_CONSUMPTION.json.

The immutable Version 3 manuscript is `quartic_9625.tex`, SHA-256
`dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552`.
Its theorem/source boundary remains the reference for inherited inputs.

The line being prepared is Version 3 -> normalized-ten pole -> general-root
and shared-square -> target-two -> direct tangents -> first-norm fusion.
This notation records construction dependencies, not equal acceptance
status. J0/scalar inverse fusion remains a separate optional branch.

## Current evidence snapshot

| Stage | Exact evidence and current scope |
|---|---|
| Normalized-ten parent | `linear_source_review` binds source ending `0f54051d0d14`; `linear_endpoint_record` records its finite cleanup. |
| General-root/shared, target four | `root_shared_source_review` binds source ending `1644d0b9193b`; `root_shared_endpoint_record` records **5,070 total variables**, including the input, on that same source. This is the best measured result in this snapshot. |
| Target two/shared | `target_two_source_review` binds source ending `e318d3a9d26b`; `target_two_endpoint_record` records **5,218 total variables**. Its further cleanup is pending; the 5,070 result belongs to the target-four source. |
| Target two/direct tangent/shared | `tangent_review` and `tangent_outer_review` accept exact module and pre-run integration scopes. No emitted-source or finite endpoint acceptance is recorded here. |
| First-norm extension | `first_norm_parity_review`, `first_norm_arithmetic_review`, `first_norm_helper_review`, `first_norm_locator_review` and `first_norm_outer_review` accept arithmetic, helper and pre-run integration scopes. Emitted-source and finite checks remain pending in this snapshot. |
| Optional J0/scalar inverse fusion | `scalar_inverse_review` accepts an exact target-two root-module change. It is not integrated into the selected tangent or first-norm line. |

SOURCE_STATUS.json binds the exact source IDs, source hashes, certificate and
expanded-polynomial hashes supplied by the two current finite records. No
pending saving is added to a measured count, and no sub-5,000 claim is made.

## Inherited statements and qualifications

Retain the Version 3 field and curve conventions

    K=Q(sqrt(2)), d=3-sqrt(2), D=d^2=11-6sqrt(2),
    E: y^2=x^3-Dx, z(P)=-x(P)/y(P), f(P)=1/x(P).

Retain the exact constant

    H19 = 2*(2^109 * 210^1800)*B_star^19 + 128,
    B_star = product of the primes at most 76176,
    log2(H19) < 2093966.

Retain the same 37 raw contacts, the eight original
abscissa coefficients of A,S,T,Z, high order 40, beta order 12, scalar orders
(1,1,1,1,32,32), and C=3^(2^25). No H18 assertion or changed prime-order
hypothesis is needed. Changes to the distribution of the 37 comparisons and
to the interpretation of point indices are specified below.

The mathematical inputs in the published inventory's groups I_H5, I_GEN, I_FORMAL, I_SIEVE,
I_ANCHOR, I_POLE, I_NORM, I_CRT, I_LUCAS and I_RECIPROCAL remain dependencies
only where currently consumed. Old construction conventions are not automatically
inherited; CURRENT_CONSUMPTION.json records the replacements. Preserve all five `source_version_requirements` in
`v3_inventory`. In particular, keep the restricted-converse/rank and original
arithmetic proof-status qualifications; the corrected-author-v5/erratum
prime-pattern convention; the stated Pan/Calegari source boundary; the
author-attested Yuan translation boundary; and the metric, twist and
arithmetic-Frobenius conventions. Neither finite replay nor these new lemmas
upgrades any inherited input's status.

The additional published trace application needed for the new anchor is
Koenigsmann, *Defining Z in Q*, Annals 183 (2016), Definition 4, Observation 5 and the proof of Proposition 6, Facts
(a),(b),(c),(e), printed pages 75 and 77. Its pinned author proof identifies the
archived publisher PDF hash and the exact ramification/residue facts. Add a
new version-qualified application for these facts; the old bare equality
T=Z_(2) intersect Z_(3) does not by itself prove the new anchor criterion.

## Required new mathematical lemmas

Suggested labels below are planning labels, not declarations already present
in a public manuscript. Each paragraph names its author proof and independent
review through the exact IDs in PROOF_PINS.json.

**N1. Three-mode height coverage** (`lem:quartic-three-mode-coverage`).
Replace the Version 3 partition of 29 full and 8 beta-only occurrences by
13 full, 8 beta-only and 16 Lucas-only occurrences. Positions 0..4 and 21..28
are full; 5..12 are beta-only; 13..20 and 29..36 are Lucas-only. All 29 contacts
covering S,T,Z retain Lucas information; all 21 contacts covering A,T retain
beta information. No raw position is removed, even when slopes or primes
coincide. With

    F(s,t,z)=t^2-s(s-2)tz+(s-2)^2z^2-1,

the first contradiction forces F=0. The inherited stronger conclusion
|t|>exp(|s|-3) then supplies the second contradiction using only A,T heights.
For H19 and q=12 its coefficient is 31/200. Dependencies: Version 3 height,
scalar/anchor and prime coverage, plus I_LUCAS. Proof `three_mode_proof`;
review `three_mode_review`. This is an arithmetic source change, not a
fixed-witness equivalence to the 29/8 source.

**N2. General private points and doubled formal comparisons**
(`lem:quartic-doubled-private-comparison`). Retained primary f-tests place
the primary points in the formal group at the consumed place. A high-order
alternate z(P-Q)/z(J), together with the retained opposite-place f(J)-test,
gives positive valuation of z(P-Q). The difference is formal after possible
translation by (0,0); doubling removes that two-torsion ambiguity. Thus

    v(log_E([2](P-Q)))=v(z(P-Q)).

Use actual doubled group identities before taking logarithms. Private points
need not lie in 2E(K); their coefficient of Pstar modulo torsion can be in
(1/2)Z. Separate difference-f tests and primary square-membership witnesses
are therefore unnecessary. The reciprocal G2/G9 nonvanishing and approximation
lemmas are the retained ones, applied on their proved full field domain.
Proof `private_comparison_proof`; review `private_comparison_review`.
Dependencies: I_GEN including the full rational two-torsion computation,
I_FORMAL, I_RECIPROCAL and N1. This is an arithmetic source extension, not
deletion of a guard justified by a local algebraic identity alone.

**N3. Joint primary/difference graph** (`lem:quartic-joint-chart`).
For target Q=(a,aq), F_Q=1/a, c=a+D F_Q and Jinv=1/z(J), set

    r=Jinv/q, s=c/q, t=1/q^2, u=rs.

The four private field values f,p,A,K satisfy

    K=(A-r)p,
    Kp+up-2Drf-4DtA=0,
    2D(A+r)f+sK+4DtA+Jinv*q=0.

The source applies the stated conjugations to f,p,D,q and the common inverse.
Recover x=p^2+Df and A=Jinv*z(P-Q). The two-denominator eliminant is

    H2*V-H1*U=-4Dq^2*(fp^2+Df^2-1),

which forces xf=1. The genuine z-poles are excluded because their graph
equations are inconsistent. The norm obstruction q^4!=4D excludes the
exceptional simultaneous-denominator-zero/basepoint cases; it does not say
that the geometric poles do not exist. A=0 is permitted at differences O and (0,0); opposition and removable
denominators are covered. No inverse of A,K,U,V is imposed. Proofs
`joint_chart_proof`, `two_denominator_proof`; review `joint_chart_review`;
exact source interface `joint_chart_contract`. Dependencies: N2 and the
nonzero target/common-inverse premises. The later N7 explicitly extends the
source interpretation at the allowed p_s=0 or p_z=0 branches; do not retain
the earlier blanket p!=0 conclusion for every normalized numerator.

**N4. One conic norm node per field** (`lem:quartic-private-conic-packing`).
For each raw contact r, introduce its own rational theta,s_c,S with

    S=s_c^2, theta^2-rS=2.

For each original field F_i=A_i+B_i sqrt(2) of order e_i, use

    Y_i=A_i+theta B_i,
    r^(2e_i) W_i=2A_iY_i-A_i^2+2B_i^2
                  =Y_i^2-(theta^2-2)B_i^2.

The upper tree is the exact successive-pair N_r(a,b)=a^2+rb^2 tree on
literal 1 followed by the sorted W_i, with odd carries. At a prime p>76176
where r has odd valuation, the conic makes v(theta^2-2) positive and odd.
It selects one split place. The norm and pole argument makes v(r)>0 and gives
v(r^(2e_i)W_i)>=2e_i, hence the original field order at that one place.
Do not replace the proved lower bound by 2e_i*v(r). Coefficients may have
negative valuations; no global squareness of F_i is assumed.

Completeness uses the elementary norm-Euclidean proof of a rational conic
point for r=d0^2*p, followed by its rational parametrization and approximation
after the original fields are fixed. Negative real leaves and zero leaves
are allowed. The scalar-height batch is not converted. Proof `conic_proof`;
review `conic_review`; composition `joint_arithmetic_proof` and
`joint_arithmetic_contract`. Dependencies: I_NORM, the applicable pole theorem,
the retained contact construction and N1/N2. This changes the auxiliary source;
it does not claim a rational map from every old private witness tuple.

**N5. Four-witness homogeneous anchor** (`lem:quartic-anchor-four`).
For a,b in Q, both are integral at 2 and 3 exactly when h=9+3(a^2+b^2)
is a norm-one trace for the quaternion algebra (2,3). Local valuation
arguments include equal valuations, unequal valuations and zero inputs;
the 2-adic h in 4Z_2 branch is proved explicitly. With a=f0/C,b=f1/C, use

    C H-9C^2-3f0^2-3f1^2=0,
    H^2-8U^2-12V^2+24W^2-4C^2=0.

The exact existential projection equals the old anchor for every rational
input pair. Division is only by the retained nonzero C. Proof `anchor_proof`;
review `anchor_review`. Dependencies: the new explicit Koenigsmann trace
application and I_ANCHOR. Retain both places; a consequence at 3 is not a
replacement definition of the anchor.

**N6. A local Lucas residual** (`lem:quartic-local-lucas`).
Before the old proxy comparisons are used, the retained primary/alternate
argument already gives p-integral C_s,C_t,C_z congruent to integer s,t,z.
Consequently the one order 40 test E=F(C_s,C_t,C_z) yields p^40|F(s,t,z).
Evaluate it quadratically by

    V=(C_s-2)C_z, D_eval=C_s C_t-V, E=C_t^2-V D_eval-1.

Delete only the three global proxy variables, their single Lucas equation
and their proved exclusive call uses. Do not impose E=0 as a field equation.
The full/beta/Lucas field lists now have 13/6/10 entries respectively, with
all primary formal and alternate tests retained. Proof `local_lucas_proof`;
review `local_lucas_review`; contract `local_lucas_contract`.
Dependencies: N1,N2,N3,N4 and I_LUCAS. Global input-projection equivalence uses
the two height contradictions and completeness, not fixed proxy witnesses.

**N7. Normalized local Lucas evaluation** (`lem:quartic-normalized-lucas`).
Replace the three quotient/evaluation blocks by B_s,B_t,B_z,P,U,V,K_c,E:

    B_i Lambda=G_i, P B_s=p_s,
    (U+V)p_t=P B_t, K_c p_t=(1-2P)B_t,
    V p_z=(1-2P)B_z, E=U^2-K_c V-P^2.

At consumed primes, C_i=B_i/p_i and E=F(C_s,C_t,C_z)/C_s^2. Soundness uses
F=C_s^2 E with C_s integral, without assuming it is a unit. Completeness
chooses the nonzero integer s before the prime pattern and excludes its
prime divisors, making C_s a unit there. Preserve all prior finite exclusions.
Global nonvanishing applies to Lambda,p_H,B_s,B_t,B_z,p_t. It does not apply
to p_s,p_z,P or 1-2P. The p_s=0 and p_z=0 branches are covered by the joint
graph's x=+/-d extension, with nonzero graph coefficient 2qx; positive-f tests
exclude them only at consumed places. Proof `normalized_proof`; review
`normalized_review`; contract `normalized_contract`. Dependencies: N6,
I_RECIPROCAL and the fixed-system finite-exclusion version of I_SIEVE.

**N8. Linear-unit one-sided ordinary pole** (`lem:quartic-linear-pole`).
Put g=3-2theta. At each odd prime where r has odd valuation, the private
conic implies theta is integral and (3-2theta)(3+2theta)=1-4r*s_c^2 is a unit. Thus g is a unit.
The ten-variable ordinary pole is

    l=gW, z=l^2, c=re,
    p^2-17r-34c+51ec=0,
    w=17e-cz, j=s_p^2, k=rq,
    j^2+34jw-867w^2-17qk=0.

It excludes negative odd valuation of nonzero rW^2 outside 2, 3, 17. This is
the one-sided conclusion consumed by N4. It is not equivalence to the old
full Psi predicate, and the original scalar-height Psi call is unchanged.
The proof includes W=0 and zero-ordinate branches. Its direct eleven-variable/normalized ten-variable
coordinate conversion divides only by r, nonzero by the private conic.

Completeness needs the generalized fixed-U realization lemma, with the same
inherited restricted-converse, rank and simultaneous-realization hypotheses.
Fix the fields first; choose theta near the selected sqrt(2) branch and near
3/2 at infinity,2,3,17. Then (r/17)W(theta)^2g(theta)^2 is small as required.
The exact witness scaling is in `parity_scale_proof`; its review is
`parity_scale_review`. The full new proof/review/contract are
`linear_pole_proof`, `linear_pole_review`, `linear_pole_contract`.
The actual normalized ten-variable source is bound by `linear_source_review`.

## General-root and shared-square lemmas

N9--N12 now have an emitted target-four source binding in
`root_shared_source_review`, and a same-source finite cleanup record in
`root_shared_endpoint_record`. N11 is historical in the target-two line: its
fixed constants are superseded by N13. The other general-root statements
remain, with the mandatory mixed-mode correction below.

**N9. Integer doubled root indices** (`lem:quartic-doubled-indices` and
`thm:quartic-general-root-source`). Set R=(1+sqrt(2),2sqrt(2)), so 2R=Pstar.
By the inherited generator and full two-torsion facts, every nontorsion root
Q has a unique nonzero integer n_Q with 2Q=n_Q Pstar. Replace the old 2E root
carrier by nontorsion E(K). The private `(1/2)Z via doubling` metadata still
describes a coefficient of Pstar; it is not this integer doubled root index.

Against targets 4R, 4Q_i the local identities are

    2(X0-4R)=(h-4)Pstar,
    2(Xi-4Q_i)=(m_i-4n_i)Pstar.

The denominator congruence has order e0=12 in beta-only mode and e0=40
in full and Lucas-only modes. Each numerator has its original order e_i,
with e_i<=e0. This yields the same integral primary quotients. The uniform
order-40 denominator statement in the frozen author notes and early reviews
is superseded by `mixed_mode_clarification`, not silently treated as true. Change both beta-bearing field tests
to C_A-2beta. Keep beta=X^2+2 and the scalar polynomial in beta unchanged.
From h(x(2Q))<=4h(x(Q))+log(676), use H_eff=5H19 in the index-height estimates.
The original high 40, beta 12, scalar 32 and anchor 25 cutoffs still suffice.
The full anchor remains at 2 and 3; its 3-adic implication is
s in 2*3^(2^24-1)Z. Both global contradictions now prove 2beta is an integer.
For X=a/b in lowest terms, b^2|2 then implies b=1.

Completeness chooses A=beta Pstar, J0,S in the old subgroup with extra
divisibility, T=tR,Z=zR, then the old finite prime pattern and private
same-prime CRT data. No cross-prime coprimality is added. Proof
`general_root_proof`; review `general_root_review`; typed composition
`general_root_composition`. This carrier/base/beta/height change must be
implemented as one source theorem.

**N10. General-root charts** (`lem:quartic-general-root-charts`).
For A,T,Z retain x,y and reuse the actual first-doubling q=x^2 pair:
y^2=xq-Dx. Retain the existing inverse of 2y. For S also keep xf=1 and
yz+x=0, preserving its scalar and anchor outputs. For J0,J use
k=fz and f=z^2-Dk^2, retaining their actual scalar/common z inverses.
Then recover x=1/f,p=-1/z,y=xp. These charts describe the required nontorsion
root points. Every deleted coordinate needs a full residual/call/alias/live
metadata incidence check. Proof `root_chart_proof`; review `root_chart_review`;
implementation review `root_implementation_review`. Dependencies: N9 and
the explicit retained nonzero gates. The target-four source and target-two source retain those inverse gates.
N14 is the separately reviewed exact tangent replacement.

**N11. Exact fixed target 4R** (`lem:quartic-fixed-target`).
Replace only the fixed-base doubling construction by the four primitive rows

    2285245536*a0-8226963211=0,
    1713934152*a1+1063929023=0,
    143614994586*q0-70757419981=0,
    574459978344*q1-344600359813=0.

They bind a=x(4R),q=y(4R)/a. Retain aF_Q=1 and the joint r,s,t,u equations;
q^2=a-D F_Q holds for these exact constants. Do not substitute the large
fractions into all later rows or invent a live fixed-target ordinate.
Proof `fixed_target_proof`, exact values `fixed_target_values`, independent
review `fixed_target_review`. The isolated four-row coefficient calculation
is not a global coefficient certificate.

**N12. Shared common-field square** (`lem:quartic-shared-field-square`).
Retain F=conj(f(J))=A+B sqrt(2); append C=A^2+2B^2,D_s=2AB at the root.
At exactly one designated field in every batch, replace

    Y=A+theta B, P W=2AY-A^2+2B^2

by P W=C+theta D_s, where P is the same r^2 coordinate. This uses explicitly
pre-squared coefficients of the original order-one F test. It is not an
order-one test of F^2. Restore Y=A+theta B; no division is used and W is
identical, including zero branches. Proof `shared_square_proof`, contract
`shared_square_contract`, mathematical review `shared_square_review`,
implementation review `shared_square_implementation_review`. Dependencies:
the exact packed-field definition N4 and the separately checked shared
root/comparator/batch incidences. Conjugation gives D_s=-2 f(J)_0 f(J)_1.

The general-root/shared outer review (`root_shared_outer_review`) binds the
current general-root contract 505b3a74... and both exact postprocessors. The
older `root_integration_review_historical_contract` binds contract ab4e98b7...
and must remain described that way. The later contract added the explicit
private-index versus doubled-root-index distinction; the later outer review
provides its current binding. Do not silently retarget the older review.

## Target-two, tangent and first-norm extensions

**C1. Mandatory mode-dependent denominator correction.** For target multiplier
c=4 or c=2, write 2X0=h Pstar, 2Xi=m_i Pstar and 2J=j_d Pstar. The exact
source implies

    v((h-c)/j_d)>=e0,  v((m_i-c*n_i)/j_d)>=e_i,
    e0=12 in beta-only mode, e0=40 in full and Lucas-only modes,
    e_i<=e0 in every mode.

The integer j_d is locally integral, and c is a unit at consumed primes.
Thus h is a unit, and

    m_i/h-n_i = ((m_i-c*n_i)-n_i*(h-c))/h

has valuation at least e_i. This is the required conclusion, without a
uniform order-40 denominator claim. Completeness may choose its stronger
order-40 congruence, but that choice proves no stronger statement about
arbitrary source witnesses. `mixed_mode_clarification` supersedes precisely
the incorrect phrases in the pinned general-root/target-two notes and early
reviews. It changes no source, order, hypothesis or finite artifact.

**N13. Target-two comparison construction** (`lem:quartic-target-two`).
Replace targets 4R,4Q_i by Pstar=2R,2Q_i. Retain integer doubled root indices,
the C_A-2beta field test, the scalar polynomial in beta and effective height
5H19. Apply C1 with c=2. In completeness, let N_1,N_2 be the full orders
of E(F_p) at the two selected places. Full rational two-torsion gives

    |2E(F_p)|=N_i/4,  gcd(N_1/4,N_2/4)=1.

Use image-group orders M_i=N_i/4. Let J=j_c Pstar with
j_c=lcm_p M_(p,2), so its doubled index is 2j_c. For each occurrence choose

    k=0 mod M_1,  k=1 mod M_2,
    k=1 mod p^(40+v_p(j_c)),  k not in {0,1,-1},
    X0=k Pstar,  Xi=k*(2Q_i).

These are same-prime congruences; no cyclicity, reduction surjectivity or
cross-prime coprimality is assumed. The fixed target values include

    x(Pstar)=57/8-(7/2)*sqrt(2),
    1/x(Pstar)=456/1681+(224/1681)*sqrt(2),
    y(Pstar)/x(Pstar)=-87/41+(129/164)*sqrt(2).

All fixed target denominator primes lie in {2,3,7,17,41}, below the ordinary
cutoff. The four variable-target first doublings remain; only their second
doublings disappear. N11's target-four constants and completeness multipliers
are superseded, while the unchanged group, height, chart and scalar facts are
retained. Proof `target_two_proof`; author contracts `target_two_author_contract`
and `target_two_machine_contract`; reviews `target_two_review`,
`target_two_implementation_review`, `target_two_outer_review`; controlling
composition `target_two_composition` together with C1; actual source binding
`target_two_source_review`. This is an arithmetic source change, not a map
between arbitrary target-four and target-two private witnesses.

**N14. Direct tangent equations** (`lem:quartic-tangent-fusion`).
In each of the four retained variable-target first doublings, retain
q=x^2 and y^2=x^3-Dx, and replace the inverse/slope pair by

    2*y*lambda=3*q-D.

The exact identity

    (3q-D)(3q-2D)-9x(x^3-Dx)=2D^2

gives y*[2lambda(3q-2D)-9xy]=2D^2. Since N(D)=49, D is nonzero; hence y
is nonzero and the old inverse is restored by

    h=(2lambda(3q-2D)-9xy)/(4D^2).

Forgetting h and this reverse formula give exact rational projection maps
preserving every other doubling output. The three affine two-torsion cases
are excluded by the retained equations, not by an added assumption. The
proof adds no external theorem, integrality condition or precision change.
The exact current transition deletes only the four private inverse pairs
after target-two and before shared-square. Full row/call/live-metadata
incidence and coordinate remapping are part of its source contract.
Proof `tangent_proof`; contract `tangent_contract`; independent literal review
`tangent_review`; composition review `tangent_outer_review`. The latter is
pre-run acceptance only in this snapshot.

**N15. First packed numerator and constant-node fusion**
(`lem:quartic-first-norm-fusion`). In each ordinary comparison batch the
first field remains H.f, original field index 0 and order 1. Retain
S=s_c^2 and theta^2-rS=2, so r is nonzero over Q. Let

    Y=A+theta*B,
    T=2AY-A^2+2B^2=Y^2-(theta^2-2)B^2.

At an odd contact valuation R, the conic gives delta=v(theta^2-2)>0 odd.
The two summands have different valuation parity. The sharper implication

    v(T)>=2e-1  implies  v(A+rho B)>=e

holds for all rational coefficients: v(Y)>=e and
delta+v(B)>=e+(delta-1)/2>=e. Zero coefficients are covered by valuation
infinity. Change only this first virtual leaf from T/r^2 to W=T/r. The
unchanged virtual tree and one-sided pole first exclude R<0, then give
v(W)>-R, so v(T)>0 and the original order-one field conclusion follows.

Compile the first constant node N=1+rW^2 directly by

    T-2AY+A^2-2B^2=0,  rN-r-T^2=0.

The fusion is exact after the denominator change: forward T=rW, reverse
W=T/r, preserving N and every higher node/pole coordinate. It allows T=0,
W=0 and N=0. The isolated r=0 row would allow extraneous N; only the
unchanged rational conic excludes it. The denominator change itself uses
soundness and integer completeness, not a fixed-witness equivalence to the
old denominator-r^2 source. In completeness the old depth-two approximation
still makes W integral; for fixed r and fields it is polynomial in theta,
so the same theta-last approximation and linear-pole realization apply.

The first old W ID now denotes a numerator T. Both field_bindings and
norm_tree must record `conic_first_numerator`, norm=null, the numerator ID
and denominator exponent 1. Only its numerator and first-node rows may use
it. All other denominators, powers, field orders, shared-square typing and
higher node consumers remain exact. The ordinary normalized-W reduction
rules do not apply to this typed entry. Proof `first_norm_proof`; contract
`first_norm_contract`; independent arithmetic reviews
`first_norm_parity_review` and `first_norm_arithmetic_review`; implementation
review `first_norm_helper_review`; locator and pre-run integration reviews
`first_norm_locator_review` and `first_norm_outer_review`. The exact pre-run
packet manifest is 7654b06f450db87a3181dd5e16fe23949cb4e57d22751aef3681fed80a1fcf26.
Fresh emitted-source and finite acceptance remain separate gates.

## Optional J0/scalar branch

**O1. Scalar inverse fusion** (`lem:quartic-scalar-inverse-fusion`).
The target-two root has z0*i=1 and lambda=z_S*i. Retained S equations
x_S*f_S=1 and y_S*z_S+x_S=0 give z_S*(-y_S*f_S)=1. Thus replacing the old
pair by lambda*z0=z_S introduces no zero-factor branch. Restore
i=-lambda*y_S*f_S; exact polynomial identities prove both old equations.
This is a quadratic source replacement with a polynomial reverse witness
map, and it adds no arithmetic hypothesis. Proof `scalar_inverse_proof`,
contract `scalar_inverse_contract`, independent review `scalar_inverse_review`.

This change is optional and unintegrated. Its reviewed input is the pinned
target-two root before tangents/shared-square. It renumbers subsequent
coordinates and changes the root hash; the frozen tangent helper must reject
that output until a separate composition is rebound and reviewed. No saving
from O1 belongs to the selected current line or to a measured endpoint here.

## Classification of inputs and proof changes

The new elementary/local construction arguments are N1--N4, N6--N15, C1
and optional O1, with their explicitly listed inherited inputs. Elementary
norm-Euclidean arithmetic, valuation parity, Hensel/weak approximation,
finite-group image counting, and exact curve identities used in these proofs
must be proved or cited within those notes in their stated scopes. They are
not new deep external theorem applications. N5 has an elementary local
criterion and an additional published trace application.

The additional published application is exactly Koenigsmann's trace set for
the quaternion algebra (2,3): Definition 4, Observation 5 and the proof of
Proposition 6, Facts (a),(b),(c),(e), including U_2={1}, U_3={0}, ramification
at 2 and 3, absence of split-finite/real restrictions, and local-to-global
trace membership. PUBLISHED_APPLICATIONS.json records it separately from
the elementary criterion and from the inherited equality T=Z_(2) intersect
Z_(3). This does not add any unpublished comparison input.

The unchanged external inputs remain the qualified Version 3 height/group,
formal-group, prime-pattern, Lucas, reciprocal-log and pole-realization
theorems. CURRENT_CONSUMPTION.json records what is still consumed and which
old construction conventions are superseded. Retain all five published
source-version qualifications. Never transfer an old review to a changed
manuscript excerpt without a new exact binding.

## Choice order and publication gate

Fix the integer input and beta; choose A, scalar J0/S and the full anchor;
choose Lucas integers t,z and root T/Z; fix root abscissas and denominators;
choose the finite contact-prime pattern avoiding the fixed nonzero s and all
earlier finite exclusions; choose the common comparison J and separate
private points for each occurrence; fix joint-chart, G, normalized-Lucas and
shared-square field values; finally choose each private conic approximation
and its norm/pole witnesses. Optional O1 changes equations for existing
values, not this choice order. Repeated contacts remain separate occurrences.

The apparent conic/pole dependency is not circular: first prove the conic
valuation and abstract binary-tree lemmas; then prove the one-sided pole
conclusion from the conic equation; then decode field orders. N15 uses this
same order with a different first virtual leaf. The formal-group arguments
consume the corrected mode-dependent orders in C1.

Before release, choose one exact source family and bind all selected lemmas
and superseding clarifications to its emitted modules and complete flattened
map. Require the actual source mutation tests, fresh lift, independent full
certificate replay and complete degree/coefficient verification. Verify the
total-variable threshold including the input. A pre-run source review or a
different variant's smaller count cannot substitute for these gates.

Precision's standalone draft is under precision/sub5000/publication-draft/.
The draft is still under review and may change. Its observed labels and
then-current content digest are recorded in DRAFT_LABELS.json for coordination
only, outside the normative proof pins. LEMMAS.json uses those suggested
labels. The selected, finally reviewed public TeX bytes need their own
source/excerpt binding. The independent inventory scope review is
`inventory_delta_review`.
