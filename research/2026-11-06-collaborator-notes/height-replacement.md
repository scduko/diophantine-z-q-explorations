# A five-contact replacement for the von Känel–Kret input

Date: November 6, 2026.

The existing five-contact height argument in `quartic_4973.tex`, Theorem `hyp:o8-height`, supplies the exact kind of input required by the two collaborator notes. It also replaces the height subsection of `two-proofs-reduced-inputs-v3.tex`. This is a substitution into those arguments, relative to the existing height proof and its recorded qualifications. It is not a new independent verification of every theorem used by that proof.

The adapted arguments do not invoke von Känel–Kret, Propositions 7.13 or 7.14. References to those results remain only in the unchanged supplied originals. The replacement continues to use the separate, published 2021 article by von Känel for standard modular-genus and lower-height estimates; that article is not the excluded joint preprint.

## Exact input

Use the fixed contact set

\[
\mathcal C=\{\infty,0,1,2401,-343/32\}
\]

with primitive integral forms

\[
L_0(U,V)=V,\quad L_1(U,V)=U,\quad L_2(U,V)=U-V,
\quad L_3(U,V)=U-2401V,\quad L_4(U,V)=32U+343V.
\]

Set \(S_* = \{p:p\le76176\}\), \(B_* = \prod_{p\in S_*}p\), and

\[
H_*=2(4608^{165888}+6^{100})B_*^{24}+128.
\]

For \(s=(u:v)\notin\mathcal C\), let \(M_{S_*}(s)\) be the product of primes outside \(S_*\) at which at least one of

\[
v_p(L_i(u,v))-\min\{v_p(u),v_p(v)\}\qquad(0\le i\le4)
\]

is odd. The existing theorem is

\[
h(s)\le H_*M_{S_*}(s)^{24},\qquad \log_2H_*<4783227.
\]

Here \(h\) is the absolute logarithmic Weil height. The normalized valuations do not depend on the homogeneous coordinates. They are nonnegative integers: scale locally to integral coordinates with one a unit, and use integral forms. Thus the notes' phrase "odd order" and the existing theorem's "positive odd contact order" agree. At primes outside \(S_*\), replacing \(u+343v/32\) by the primitive form \(32u+343v\) changes no valuation. The contact infinity, and hence odd denominator valuations, are included.

## Why this removes the joint-preprint dependency

The relevant proof is already present in Version 4. Its non-CM branch proceeds through a modular level, rather than a general effective Shafarevich estimate over number fields. For a fixed parameter put \(R=B_*M_{S_*}(s)\). The established geometry and representation construction supply:

\[
[L:\mathbb Q]\le576,\qquad [L':\mathbb Q]\le2304R,
\qquad N\le210^{300}R^2.
\]

The non-CM quaternionic surface \(A/L\) has a weight-two modular constituent that also occurs in \(J_1(N)\) over \(L'\). The scalar character order and the coefficient-field degree are allowed to vary. Faltings' Hom theorem and Poincaré reducibility give an \(L'\)-isogeny

\[
A\times Z\longrightarrow J_1(N).
\]

The bound on \([L':\mathbb Q]\) is radical-dependent. It is not the rejected claim of a uniform bound on the scalar splitting field or the newform coefficient field. A match of Frobenius traces at good primes is also not used by itself as a bound on the conductor at five: the construction passes between coefficient primes five and three and applies local compatibility away from the coefficient prime.

Write \(C=210^{300}\) and \(g=\dim J_1(N)\). The genus and Belyi-degree estimates, followed by Javanpeykar's published theorem, give

\[
g\le C^2R^4/24,\qquad h_F(J_1(N))\le13000000C^{12}R^{24}.
\]

All Faltings heights here use the original stable normalization. Applying Gaudron–Rémond's published Theorem 1.9(1) with the modular Jacobian as source gives the variation term

\[
V=2g^2\left(8g^2\log(7g)+\log[L':\mathbb Q]
+\log\max\{1,\log[L':\mathbb Q],h_F(J_1(N))\}\right).
\]

The existing proof bounds \(V<C^{12}R^{24}\); it uses the lower bound \(h_F(Z)>-3g/2\), not nonnegativity of the complement's height. Consequently

\[
h_F(A)<2^{24}210^{3600}R^{24}<4608^{165888}R^{24}.
\]

The separate CM argument gives \(h_F(A)<854R\). It uses the field of definition of CM elliptic factors, the class-number estimate, and an isogeny-height bound, and does not call the excluded Proposition 7.14. Since \(854<6^{100}\) and \(R\ge1\), both branches fit inside

\[
h_F(A)<(4608^{165888}+6^{100})R^{24}.
\]

Finally the geometric metric comparison is

\[
h(s)\le2\max\{0,h_F(A)\}+128.
\]

Since \(M_{S_*}(s)\ge1\), these inequalities give exactly the stated coefficient \(H_*\). The elementary budget uses \(B_*<2^{109445}\), \(4608<2^{13}\), and

\[
3+13\cdot165888+24\cdot109445=4783227.
\]

The complete geometric, local and CM arguments are in the pinned manuscript, not inferred from this numerical budget. The included source and review map identifies them individually.

## Substitution into the collaborator's equivalence argument

In `paper_equivalence.pdf`, Section 2, instantiate Input H with the forms above, \(S_0=S_*\), \(H_0=H_*\), and \(c_0=24\). In `proof_optimization.pdf`, replace Section 4 as the source of Input H by the existing Version 4 proof just identified. The printed Section 4 remains in the original PDF only as provenance.

The notes' prime-pattern argument is formulated for an arbitrary fixed configuration of five distinct rational points, including infinity. These forms are primitive, and their pairwise determinants are nonzero. Their prime divisors lie in \(\{2,3,5,7\}\). Thus the same thirteen-form construction applies; no sixth contact or additional prime-pattern slot is introduced. This checks compatibility of the input, rather than re-proving the notes' sieve theorem.

Fix the predicate \(\Phi\) and its exceptional set \(S_\Phi\), then the finite multiplier catalogue \(\mathcal K\) as prescribed in the notes. Choose \(c=24\), enlarge \(S_*\) to the fixed set \(S\) required by their Section 2.1, and put

\[
D_S=\prod_{p\in S\setminus S_*}p,\qquad H'=H_*D_S^{24}.
\]

For each rational parameter, \(M_{S_*}(s)\mid D_SM_S(s)\); therefore

\[
h(s)\le H'M_S(s)^{24}.
\]

The value \(H'\) is a positive integer, chosen once. It does not depend on the represented integer, the rational scalar under test, or the later fixed multiplication parameter. It is a formula for the constant, not a new numerical bound on the yet-uninstantiated catalogue and \(S_\Phi\).

The formal-logarithm truncation still has degree 24. The coordinate amplification parameter can be any positive integer satisfying the notes' inequality

\[
L^2>18a_*H'+a_*^2+8a_*.
\]

It is a fixed integer, and can be implemented by fixed elliptic group operations before variable-index multiplication is defined. All subsequent multiplication and scalar-evaluation arguments use precisely this instantiated height statement.

## Substitution into the reduced-precision Lucas argument

Replace the von Känel–Kret height subsection in `two-proofs-reduced-inputs-v3.tex` by the same five-contact theorem. Set its \(H=H_*\) and \(S_0=S_*\). Its definition

\[
H_d=\max\{1,H_*(\prod_{p\in S\setminus S_*}p)^{24}\}
\]

and \(K=24\) are unchanged. Its later enlargement of a generator from \(P_0\) to \(NP_0\) leaves \(H_d\) fixed. Thus the quadratic-Lucas and small-constant estimates have the same hypotheses. This substitution does not instantiate the generator multiple, excluded finite range, all predicate witnesses, or a compiled polynomial, so it establishes no improved variable or coefficient count.

## Dependency and review boundary

No new external theorem application is needed: this substitution consumes the existing five-contact theorem on exactly its declared domain. The principal existing inputs are the published discriminant-210 quotient models, the integral/metric comparison for the quaternionic family, Faltings, semistable reduction and local ramification theory, two-dimensional modularity, local modular compatibility/newform theory, Javanpeykar's bound and Gaudron–Rémond's isogeny theorem. The CM branch has its own existing source chain. Their exact locations and qualifications are listed in [DEPENDENCIES.json](DEPENDENCIES.json).

The existing H5 acceptance explicitly distinguishes Calegari's published formulation of Pan's theorem from the detailed author version inspected, and Yuan's author-identified English translation from the original Chinese typesetting. This update preserves those inspection limits. An old comment reading "pending" in a historical fragment is not a new decision; the final acceptance and current source are separately pinned.

The collaborator's parity assertion P remains an input of that standalone argument. The equivalence P with integer definability is not a proof of either assertion. Our manuscript's restricted-converse argument is a separate proposed justification; this height substitution neither replaces nor newly certifies it. In particular no finiteness of the two-primary Tate–Shafarevich group is inferred merely from a Selmer dimension calculation.
