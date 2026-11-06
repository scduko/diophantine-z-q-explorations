# Independent review of the direct local Lucas residual

Date: 2026-11-06. Verdict: PASS for the arithmetic replacement and the exact interface below. This is not acceptance of an emitted source, a finite replay, or an endpoint count. Version 3 is unchanged.

Reviewed proof: `precision/sub5000/LOCAL_LUCAS_RESIDUAL.md`, SHA-256 `2c4b1a1f24a485b021ff11561043a412a61186e243194ba244b6090124b83570`, relative to `work/quartic-sub10000-20261106/`. I read the proof and checked its inferential use against the existing joint arithmetic argument, SHA-256 `76d1ffafe8fcf1e79c462f269187ebfb168edd6f4cc3b339842dac217c9051f7`. The latter's frozen source contract is not implicitly changed by this review.

## The congruences do not depend on the global proxies

Use H19, high order K=40, beta order 12, anchor 25 and scalar order 32. Root indices n,s,t,z are ordinary integers. Each private point may have a half-integer index because it is only constrained to E(K), with [2]P=[2 alpha(P)]P_*. This distinction does not change integrality at an odd selected prime.

At any raw contact with odd valuation at p>76176, the retained norm layer supplies every retained formal and alternate order. The common denominator point has an order-40 alternate, so its private index h is 4 modulo p^40. Each Lucas numerator has an order-40 alternate, so its index m_i is 4n_i modulo p^40. These follow from v(alternate)=v((m_i-4n_i)/j), where the unchanged nonzero integer j has nonnegative p-adic valuation. Thus h is a unit, and m_i/h is integral and congruent to n_i modulo p^40.

The retained primary formal tests and reciprocal-G identities then give C_i=m_i/h modulo p^40. This conclusion uses neither a global proxy nor a primary error C_i-proxy. The logarithmic equality in the half-index case uses [4h]P_i=[4m_i]P_0, not an unproved equality before removing possible 2-torsion. The denominator logarithm is nonzero. These are precisely the premises already proved for the rational-difference source.

Therefore C_s,C_t,C_z are integral and congruent to s,t,z at this occurrence before any proposed replacement test is used.

## The one replacement test is sufficient

Put

```
F(X,Y,Z)=Y^2-X(X-2)YZ+(X-2)^2 Z^2-1.
V=(C_s-2)C_z,
D_eval=C_s C_t-V,
E_eval=C_t^2-V D_eval-1.
```

Direct substitution gives E_eval=F(C_s,C_t,C_z). There are three field pairs and six rational quadratic component equations. D_eval is not the fixed curve coefficient D. Since all arguments are integral at the selected place and F has integer coefficients, E_eval is congruent to the rational integer Delta=F(s,t,z) modulo p^40. An order-40 test for E_eval therefore proves p^40 divides Delta. It is not necessary to impose E_eval=0 as a field equation; doing so would create an unproved completeness requirement.

The retained Lucas-bearing positions are exactly the five shared positions and the eight positions for each of S,T,Z: 29 occurrences. All odd-valuation prime divisors needed by those three point-height bounds therefore divide Delta to the same order as before. Their proof is per occurrence; repeated primes and independently selected conjugate orientations cause no conflict because the conclusion concerns the same rational integer Delta.

For Delta nonzero, the existing radical and height argument is unchanged:

```
B_L=max(|s|,|t|,|z|),
B_L^2-6 < 7H |Delta|^(19/40),
|Delta| < 5 B_L^4,
B_L^(1/10) < 24H.
```

Here B_L>=|s| and the unchanged anchor gives |s|>(24H)^10. This is the same strict contradiction, now obtained directly from a local polynomial residual. Consequently Delta=0. The root Z is still nonzero, so z!=0; |s|>=7 is unchanged. The inherited Lucas growth conclusion |t|>exp(|s|-3) applies to these integer indices.

The second contradiction is unchanged: beta comparisons remain at all five shared positions, eight A positions and eight T positions. They control B_AT=max(|n|,|t|), and the growth of t supplies the same lower bound. No beta error, beta alternate, beta point, beta G circuit or height target is removed. There is no use of a global equality between a proxy and an index in this second argument.

## Completeness and choice order

For an integral input, retain the old scalar and anchor witnesses, integer Lucas solution, common J and independently chosen private points. Their quotient congruences give E_eval congruent to F(s,t,z)=0 modulo p^40. Assign V,D_eval,E_eval by the displayed polynomial formulas. Existing norm/pole completeness thus applies to exactly the new tested values.

For a private-conic norm layer, all three new field pairs and both rational coefficients of E_eval must be fixed before choosing that occurrence's conic theta. This lets the existing conic approximation absorb their denominators. The operation introduces no extra simultaneous-point or cross-prime congruence condition.

If the source retains unused global proxies and their old equation, xi=0,tau=1,zeta=0 satisfies that equation independently of the retained root points. If those coordinates or their equation are deleted, a complete incidence check must verify that no other consumer remains. Neither variant preserves an arbitrary old global-proxy witness tuple; the claimed equivalence is the final rational input projection.

## Exact emission gate

The source auditor must reconstruct the three polynomial definitions, bind their C_s,C_t,C_z to the original retained logarithm quotients, and pass exactly E_eval to the order-40 field test. It must preserve every primary formal test, common f(J) test, alternate and G equation. It must reject an E_eval=0 equation, omitted residual test, switched quotient, changed order or alternate, or an unrelated pair passed to the norm call.

The field lists and orders are:

| Mode | Ordered contents | Orders |
| --- | --- | --- |
| Full | five primary f, conjugate f(J), beta error, E_eval, five alternates | `[1]*6+[12,40]+[40,12,40,40,40]` |
| Beta-only | two primary f, conjugate f(J), beta error, two alternates | `[1]*3+[12]*3` |
| Lucas-only | four primary f, conjugate f(J), E_eval, four alternates | `[1]*5+[40]*5` |

With 13/8/16 occurrences, these contain 13*13+8*6+16*10=377 field tests and still 145 point/difference pairs. This arithmetic count is not a final variable count. The old conic/source contract with 435 fields must receive a separately named revision; it must not be reused unchanged. Compatibility with a new point chart requires that chart to recover the same f,p and alternate functions with all the nonvanishing premises used above. The new joint f,p,A,K chart is reviewed separately.

No new external theorem is used by this replacement. The height, integer carrier, formal logarithm, Lucas and prime-pattern inputs retain their prior source-version qualifications. This review did not run heavy computations or certify an implementation.
