# Independent review of normalized local Lucas ratios

Date: 2026-11-06. Verdict: PASS for the arithmetic replacement and the typed producer interface below. No generated normalized source or finite endpoint is accepted by this review.

The reviewed proof is `precision/sub5000/normalized-lucas/NORMALIZED_LUCAS.md`, SHA-256 `e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811`. I read that proof, the frozen joint-chart proof and the actual Version 3 rational-contact completeness argument. I also read the entire new emitter `normalized_lucas.py`, SHA-256 `3e1e420306de2fbe51c17aeb8f24169e23a9d74f47601262d3333360e7c7d921`, and its source contract, SHA-256 `b038a32f4b22de7a43680857dc693d5614d25c6d0f432841bbafd2a8577898d6`. No published arithmetic input is added.

## Identity and permitted divisions

Retain Lambda*p_H=G_H. The proposed eight field pairs B_s,B_t,B_z,P,U,V,K_c,E satisfy

```
B_i*Lambda=G_i                 (i=s,t,z),
P*B_s=p_s,
(U+V)*p_t=P*B_t,
K_c*p_t=(1-2P)*B_t,
V*p_z=(1-2P)*B_z,
E=U^2-K_c*V-P^2.
```

The retained reciprocal polynomials G_9(D*f^2) and G_2(D*f^2) never vanish over Q(sqrt(2)). The established dyadic argument applies here without a change of polynomial: D is a dyadic unit, the nonconstant G coefficients have valuation1, and the truncation degree in D*f^2 is at least2. When v_2(f)<0, the highest term has uniquely smaller valuation than the constant and all other terms, including when v_2(f) is a negative half-integer. When v_2(f)>=0, the constant is uniquely least. Thus Lambda,p_H and every B_i are globally nonzero.

If p_t=0, the second displayed normalized relation gives P=0, and the third then gives B_t=0. This contradiction proves p_t is globally nonzero. This argument does not prove p_s or p_z nonzero, and neither is required globally. In particular, one must not reuse the old global division by all p_i after deleting their old quotient equations.

At a consumed prime p>76176, every retained primary f test has positive valuation. The unchanged joint-chart eliminant gives

```
f*p^2+D*f^2=1.
```

Here D is a unit. It follows that each primary p is nonzero, v(f)+2v(p)=0, and the associated point is formal. Only at this stage define C_i=B_i/p_i for the local soundness argument. They are exactly the old finite-logarithm quotients. The retained alternates, nonzero common denominator logarithm and half-index doubled identities give C_i integral and C_i congruent to i modulo p^40.

Since B_s and p_s are now nonzero, P=1/C_s. Substitution yields

```
V=(1-2P)*C_z,
U=P*C_t-V,
K_c=(1-2P)*C_t,
E=P^2*F(C_s,C_t,C_z),
F(S,T,Z)=T^2-S*(S-2)*T*Z+(S-2)^2*Z^2-1.
```

For example, expanding (P*C_t-V)^2-K_c*V uses 2P*C_t+K_c=C_t, leaving P^2*C_t^2-C_t*V+V^2-P^2, which is the claimed expression. The tested E is F/C_s^2. Soundness multiplies by the integral C_s^2 to obtain F=C_s^2*E; it does not divide by a possibly nonunit C_s. Thus an order40 E test is sufficient even when C_s has positive valuation. There is no missing factor2 or sign in this identity. The case C_s=2 gives V=K_c=0, U=C_t/2 and E=(C_t^2-1)/4, without division by 1-2P.

The rest of soundness is unchanged: the same 29 positions imply p^40 divides the rational integer Delta=F(s,t,z), the same H19/high40/anchor25 contradiction forces Delta=0, and the same 21 beta-bearing positions and Lucas growth give beta=n. Different private conic orientations at a repeated rational prime still imply divisibility of this same rational integer. No relation between those local orientations is needed.

## The newly permitted zero-ordinate branches

The old joint-chart proof invoked old G/ratio equations to conclude every numerator p was globally nonzero. That sentence is not inherited for p_s,p_z in this new source. Its eliminant and curve reconstruction, however, contain no division by a primary p. They still prove f!=0, x=p^2+D*f=1/f and the curve equation.

If a primary p vanishes, then D*f^2=1 and x is d or -d. In the complete two-denominator graph,

```
U_graph=q*(x+D*f)+c*p=2*q*x != 0,
H2=x-D*f-q^2=-q^2.
```

It therefore determines z(P-Q)=-q/(2*x). This is the ordinary regular value at the nonzero two-torsion primary, not a new free component. The retained target Q is a nonzero point of the torsion-free root group; subtracting it from a torsion primary cannot give a torsion pole. The same polynomial graph identities thus extend the chart correctly. At every consumed prime these branches are excluded because f is a unit, contradicting its retained positive-valuation test. Nothing requires a private point to be nontorsion at occurrences where no odd contact is consumed.

These facts close the only new global chart-domain obligation. They do not supply a global inverse of p_s or p_z and should not be described as doing so.

## Completeness and finite prime avoidance

Normalization is stronger at a prime where C_s is not a unit. Consequently this is an arithmetic source change, not an algebraic equivalence for every old witness tuple. The proof correctly changes the existential witness construction.

Fix the integral input, scalar/anchor data, the nonzero integer root index s, its integer Lucas companions t,z and all rational height-target coefficients before choosing the contact pattern. The actual Version 3 rational37 proof states that the coefficients, positive cone, denominator D_0 and initial cutoff are fixed before the box grows. Increasing that fixed cutoff beyond |s| and every prior excluded prime is therefore permitted by the same fixed-system prime-pattern theorem. It neither requires uniformity in a growing denominator nor changes a same-prime elliptic-order condition. The fixed forms are positive and grow in the chosen cone. Thus all assigned primes can avoid s, even if |s| is very large; exact duplicate positions are restored afterward as before.

Choose common J and the private points only after these primes. For the old complete witnesses all C_i exist and are nonzero, with C_s congruent to s. Hence C_s is a unit at every assigned Lucas prime. The old congruence F(C_s,C_t,C_z)=0 modulo p^40 now implies the same order for E=F/C_s^2. Assign the eight new coordinates by the displayed formulas, fixing all their rational coefficients before choosing each private conic theta. Existing conic/pole completeness then applies. The global beta quotient, scalar-height data, four-witness anchor and all root height targets remain untouched.

This quantifier order avoids a circular choice of s from later primes. It uses no assumption that a common set of private elliptic points can serve different contacts; those points remain independent.

## Producer/interface review and remaining source gate

The emitter explicitly requires the old local-Lucas and joint hooks, a fresh H19/high40/beta12/anchor25 builder, and installation before the retained conic hook. It reconstructs the same joint chart, common G equation and beta quotient, then uses exactly the eight-pair equations above at the three correct numerator roles. All G precisions and their unbound output expressions are retained. The conic hook still intercepts the temporary old field-test interface and passes only the same affine field coefficients to q_conic13/q_conic6/q_conic10. It cannot retain an old theta/error leaf through that interface.

The root, beta-only comparator, all three conic batches, anchor, scalar-height and old parity modules are required to be byte-identical to the frozen local-Lucas source. Comparison arities remain58/28/47, legacy prefixes28/16/23 and theta/error/raw slots25/26/27,13/14/15,20/21/22. The exact field lists and orders are unchanged; only the Lucas E value is normalized. The new metadata states `global_numerator_p_nonzero=false`, which is necessary. There are eight field coordinates and eight field equations replacing nine of each at 29 occurrences; the raw difference is58 rational coordinates and58 rational rows, not an accepted final polynomial saving.

The final source auditor must independently reconstruct all these equations and bind roles, signs, factors and output E. It must preserve primary formal tests, every alternate and the beta quotient, reject any extra denominator/nonzero restriction, bind the new global/local zero-ordinate convention, and complete flattening and a fresh named-source replay. I have not accepted an uninspected normalized source or its eventual count. The typed addition accompanying this review records these exact obligations and excludes the separately proposed conic-pole change.
