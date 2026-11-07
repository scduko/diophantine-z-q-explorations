# Historical excerpt: kato

Origin in the research workspace: `work/quartic-version6-release/repository/docs/theorem-application-audit/evidence/applications.md`

Full origin SHA-256: `a8368a8ee209a53ca8d0ba424ef9727dfea3f0ba3155867d30e194e81b978038`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 1 to 5

```text
1: # External-theorem applicability audit of the restricted-converse argument
2:
3: This is a targeted adversarial follow-up by the author of the earlier RC composition report, not independent reviewer credit for that report. It checks the strongest Kato and normalized-theta applications by returning to the original statements and the actual current consumers. No previously assigned verdict is used as evidence. The mathematical target examined here is frozen review-v4e, with the already specified branch/activation/coordinate clarifications distinguished from its bytes. This note neither validates the ordinary-integer theorem nor supplies Lean verification.
4:
5: The earlier report is `work/astra-final-rc-unconditional-closure-audit-001/REPORT.md`, SHA256 `da18bc014ea500ed842950e31898cdf50ff7f9efcba68a0c66c7505e16255f72`. It must be read with `RC_REPORT_CORRECTION_001.md` in this directory, SHA256 `9e089adb4eb8d996bcb93d631ca131078a0c39acbd954d3d9fa7cfd9e59b6389`. Its old Section 12 formula for the Euler correction was a transcription error. The manuscript and the raw producer have the correct formula. Section 8 below also records the needed regular-functional justification explicitly; generic nonzero rank would not suffice.
```

## Original lines 26 to 60

```text
26: ## 2. Kato 13.4(2): every hypothesis on the actual object
27:
28: The target is the fixed non-CM curve E_ell, not an arbitrary elliptic curve. Its j-invariant is 35152/9, hence is not an algebraic integer and cannot be a CM j-invariant. All quadratic twists remain non-CM. The representation is the actual rank-two Tate module, after the one fixed comparison from the original modular form. The representation is not replaced by its reduction modulo two.
29:
30: | Hypothesis or conclusion | Direct check and actual consumer |
31: |---|---|
32: | Finite extension L/Q_2; finite free integral representation, unramified outside a finite set | T_2(E) has rank two, and a quadratic character has finite conductor. The finite set contains 2, bad primes, twist primes, and smoothing primes. K 5160–5169; E 8–49. |
33: | An actual Euler system satisfying 13.1.1 | Original classes use 8.1.3 and 8.12. Pushforward on the group basis is integral. At a constituent it is the literal transfer of the class tensored with the character line; transitivity gives E.1. Newly added primes, and only those, give the Euler factors. This checks the norm relation itself rather than postulating a class with the desired L-value. |
34: | Nonzero at every height-zero component | A fixed integral sum of modular symbols has nonzero projections on both period lines: two proper rational kernels do not cover the rational symbol space, and denominators can be cleared once. Kato 13.6 gives the span. For a fixed finite twist, 13.5(2) leaves only finitely many zero critical values among characters supported on its fixed finite conductor set. Each parity component contains infinitely many cyclotomic finite characters. The fixed smoothing multipliers are nonzero at these specializations. The same argument as 13.7 gives a nonzero generic class in each component. K 5257–5283; E 9–16,94–103. |
35: | Each real eigenspace has rank one | Elliptic complex conjugation is odd with eigenvalues +1 and −1 over Q_2. Twisting can exchange the two eigenspaces but cannot change either dimension. This is rational rank, not semisimplicity over F_2. |
36: | Purity | Printed p.226 uses **inverse** arithmetic Frobenius. For the Tate module its two inverse eigenvalues have complex absolute value q^(−1/2), so w=−1. A quadratic sign does not change the absolute value. The previously proposed w=+1 correction would be wrong in this convention. |
37: | Rational irreducibility | Non-CM open image contains an open SL_2 subgroup after restricting to any fixed quadratic kernel. The natural two-dimensional Q_2 representation of such a subgroup has no invariant line. This remains true when E[2] is completely trivial. |
38: | An element of the cyclotomic kernel with one-dimensional fixed space | The determinant is cyclotomic. The open SL_2 subgroup, intersected with the quadratic kernel, contains a matrix [[1,2^r],[0,1]] for some finite r. It is nonidentity and has exactly one-dimensional fixed space. The stronger abelian-kernel version in Kato 1999 Example 0.6.2 also follows by using the open commutator image; the 2004 theorem needs only the cyclotomic-kernel statement. |
39: | Height-one prime away from two | This is the precise domain of 13.4(2). On each rational character component it bounds the localization of H^2_0 by the ideal of the actual class's coordinates. The integral estimate at the prime (2) comes later from the separately constructed positive complex, not from this theorem. |
40: | Controlled module | It is H^2_0=ker(H^2→H^2_loc), not all of H^2. E 105–125 accounts for the difference. Ignoring this distinction would leave a real gap. |
41:
42: The original printed p.226 places residual irreducibility, an integral rank-one cokernel, and p≠2 only in part (3). They are not hypotheses of part (2). Kato 1999 0.8 makes the same away-p distinction; its 0.7 ideal is generated by all linear evaluations of the actual class. Sections 11.6–11.9 prove the divisibility by obtaining one factor outside the chosen height-one prime and taking the finite-level limit. This is the right coordinate ideal for the determinant application; it is not a theorem about a differently normalized primitive generator.
43:
44: The original 1999 proof also displays its dyadic adjustment: Lemma 12.7, printed p.364, uses an extra factor two at levels m≤2 when p=2. It explicitly notes that two is outside the localized prime. Thus the small-level factor is invertible in the away-two application. It cannot be silently discarded in an integral assertion at (2), which this application does not make.
45:
46: An explicit failed alternative is useful here: for the actual E_ell, E[2] is rational. Part (3)'s residual irreducibility is false. Any proof which invokes that part for this curve fails. The present part-(2)-plus-integral-positive-complex route does not make that invocation.
47:
48: ## 3. Fixed normalization, ramified characters, and exceptional Euler zeros
49:
50: The smoothing and character conventions are checked on the printed formulas, not inferred from an L-value slogan. At k=2 and r=r'=1, both alternatives of 4.2.4 give (u,v)=(1,1). The retained version of 6.6 is a sum over all residues, with no division by the number of residues. It uses f* and the inverse character on the analytic side. For the fixed rational newform f*=f; auxiliary cyclotomic characters still retain their inverse. Theorem 9.7 sends the very same smoothed etale class to this modular-form expression. See printed pp.143,163,189, and E 18–49,77–91.
51:
52: The smoothing integers are odd and congruent to 1 modulo the odd support and to 1+2^e modulo 2^(e+1), for fixed e≥max(3,v_2N). They are therefore prime to 6 and the class conductor, and satisfy the original congruence modulo N. At the quadratic central constituent their character values are 1, so each factor c^2−c has valuation e. Their product has valuation 2e even if their numerical sizes increase with the support. Nothing is divided by a vanishing smoothing factor. For a finite-order nonquadratic character, c−chi(c) cannot be zero for c>1, because chi(c) is a root of unity; this also checks the generic-nonvanishing application.
53:
54: For an odd signed squarefree h with discriminant Delta_h=4h, omitting the dyadic character would change the representation. The actual basis map E.2 includes both character factors at every sufficiently high cyclotomic level. If a quadratic character is nontrivial on Gamma, the action is changed by t↦−2−t. The comparison with the full-conductor transfer is cofinal: introducing more powers of a prime already in the level has no Euler factor in 8.12. Thus the comparison is an equality of the retained classes, not an equality of just their central L-values. For odd h the ramified dyadic possibilities are a finite list; in fact the quadratic character of conductor four is on the real-sign factor, while the displayed Gamma automorphism also covers the allowed conductor-eight enlargement. The signed Gauss relation is tau(chi_h)^2=Delta_h. Replacing its right side by chi_h(−1)Delta_h would double-count the sign.
55:
56: At the old support the local types of a quadratic twist form a finite set. Local Tate duality identifies H^2(Q_v,V_h) with the dual of rational Tate invariants, which vanish because local elliptic torsion is finite. Local Iwasawa control therefore excludes t from the finite local clearing factor. Taking the product over those finite types gives one F_E with F_E(0)≠0. This is the justification for using F_E; nonzero generic rank alone would not show its central value nonzero.
57:
58: At a new active odd prime, inertia acts through the nontrivial quadratic sign; over Q_2 its invariants and the relevant rational inertia cohomology vanish. At an unused prime, the rational j_*-to-full cone is the two-term Frobenius complex on H^1(I_q,V_h), in degrees one and two. Its differential is generically invertible, hence injective over the one-variable domain even when its determinant has a zero at a height-one prime. Its degree-two length is precisely the order of that determinant. The same Euler factor occurs in the transferred class E.1, so it pays this length. At bad primes H^1(I_q,V_h) must be used; replacing it indiscriminately by V_h^{I_q}(−1) is not justified.
59:
60: This addresses exceptional characters: a specialization may make an unused Euler factor zero, and a central analytic value may vanish. Neither is discarded as an exceptional set in the divisibility proof. The generic identity is cleared before specialization. The numerical central identity E.7–E.9 is used only where Selmer corank is zero; its finite nonzero valuation form additionally assumes the central L-value is nonzero. A rank-one curve with finite Sha would be a counterexample to treating finite Sha alone as that corank-zero hypothesis. The actual unknown base has full corank one and does not enter this central Kato calculation. Known nonzero central values get the required corank-zero conclusion from the separate forward theorem.
```
