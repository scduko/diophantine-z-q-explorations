# Independent review of private-conic field-test compression

Date: 2026-11-06. Arithmetic PASS for `precision/sub5000/ODD_DISCRIMINANT_PAIR_COMPRESSION.md`, SHA-256 `ef4de3f02fa3d17c18dc7c2af490960a62f35cc541eac8e4b80958d320fa8ab9`, subject to the exact contract below and the retained pole theorem. This is a new arithmetic source relation with the same input projection as the separately justified comparator source. It is not an algebraic equality with the old norm root or a rational transformation of every old witness tuple.

The argument works for arbitrary tested field elements. It therefore composes with the reviewed four-field rational difference source, which no longer makes primary f globally square. No new external arithmetic input is needed for the conic argument. Implementation, full source incidence, lifting, replay, and final counts remain separate obligations.

## Exact contract

For each raw occurrence r use its own rational coordinates theta,s,S and equations S=s^2 and theta^2-rS=2. Remove the old root-error test layer only after checking all its consumers. For each retained field test F=A+B sqrt(2), of positive integer order e, A and B must be independent of those conic coordinates. Set P=r^(2e) with a deterministic powering circuit, and impose

```
Y=A+theta B,
P W_F=2AY-A^2+2B^2.
```

The right side is identically Y^2-(theta^2-2)B^2. Preserve the approved field list, conjugations, orders, and raw-position assignment. Sort by order only with the specified stable ordering. Build the upper successive-pair tree on literal 1 followed by all W_F, using N_r(a,b)=a^2+r b^2, carrying an unpaired last node. The constant must stay on its all-left path. Apply the unchanged pole predicate to r times the square of the final root.

The scalar-height batch is excluded from this replacement. The proof does not turn its rational tests into field tests or modify its correction factors. Different raw occurrences must have independent conic triples. A common theta satisfying all conics is not supplied by this proof.

## Odd valuation and the constant path

Every rational conic solution has r,s,S nonzero. Either r=0 or s=0 would imply theta^2=2 over Q. Thus the rational nonsquareness of 2 justifies the nonzero facts; they do not rely on a genericity convention.

Fix p>76176 with R=v_p(r) odd, and abbreviate epsilon=theta^2-2. Its valuation E=R+2v_p(s) is odd. If v_p(theta)<0, E=2v_p(theta) is even. If v_p(theta)>0, E=0. If theta and epsilon are both units, E=0 again. Therefore theta is a unit and E is positive odd, even before R's sign is known. Hensel's lemma selects rho^2=2 with theta-rho divisible by p, and theta+rho is a unit. Hence v_p(theta-rho)=E.

At every upper norm node, the two nonzero summands have valuations of opposite parity. There is no cancellation. Consequently a zero node has two zero children. The literal constant path makes the final root nonzero. Its pole argument has odd valuation R+2v_p(root), so the unchanged pole theorem makes this valuation positive.

If R<0, ascent along the constant-left path gives v_p(root)<=0, contradicting that positivity. Thus R>0. Starting from v_p(root)>-R/2, descent at a node with bound v_p(N_r(a,b))>-cR, c<1, gives v_p(a)>-cR/2 and v_p(b)>-(c+1)R/2. Every finite descendant therefore has valuation greater than -R. In particular v_p(W_F)>-R.

This argument remains valid with zero field nodes. It uses the new literal constant rather than an old epsilon leaf and therefore justifies removal of that leaf in the specified tree.

## Recovering each field order

Since P=r^(2e), the field-node equation gives

```
v_p(Y^2-epsilon B^2)>(2e-1)R>=2e-1.
```

Integral valuations imply that the left side is at least 2e. The nonzero terms Y^2 and epsilon B^2 have even and odd valuations respectively, so each has valuation at least 2e. It follows that v_p(Y)>=e and E+2v_p(B)>=2e. Because E>0,

```
v_p((theta-rho)B)=E+v_p(B)>=e+E/2>e.
```

Subtracting this correction from Y proves v_p(A+rho B)>=e. If B=0 this follows directly; if a term vanishes the same minimum argument uses valuation infinity. No integrality of A or B was assumed in advance. No global squareness of F is used.

The lower bound above is at least 2e, not in general 2eR. The proof uses precisely the former bound. All downstream comparator arguments consume only the recovered field order e. Thus the same raw-contact soundness, four-field half-index argument, and two global contradictions apply after this replacement.

Soundness does not require different occurrences of the same rational prime to choose the same rho. At each occurrence the recovered primary tests hold at its selected place, and its already-conjugated common-J and alternate tests hold at the opposite place. The local group argument therefore yields the same rational proxy/index congruence modulo p^e whichever place was selected. These rational congruences, rather than a globally selected embedding, are what the radical and height arguments combine. If different occurrences select opposite roots, their common-J tests may force J to be formal at both places; any satisfying assignment then meets both local requirements. This creates no new soundness assumption. Completeness can and does choose the old common orientation at repeated primes.

## Rational conics and completeness

The inherited integral-input construction makes each raw contact r=d0^2 p>0, where d0 is a nonzero rational p-unit and p is a selected prime congruent to 1 modulo 8. The finite contacts have d0=1; the infinity contact carries the fixed denominator-clearing square. The selected p avoids the divisors of d0. A change of these raw-contact conditions would require a new completeness proof.

The proof's rational point construction is valid. The ring Z[sqrt(2)] is norm Euclidean: rounding both coefficients leaves a remainder with absolute norm at most 1/2. Since p splits, a generator of a prime ideal of norm p has norm p or -p, and multiplying by 1+sqrt(2) corrects the sign. This gives integers a,b with a^2-2b^2=p. Necessarily b != 0. Then theta0=a/b and s0=1/(d0*b) solve theta0^2-r*s0^2=2.

The displayed line parametrization is exact. With theta=theta0+t(s-s0), its second intersection is

```
delta=2(r*s0-theta0*t)/(t^2-r),
s=s0+delta, theta=theta0+t*delta.
```

Its rational denominator cannot vanish because r=d0^2 p is nonsquare. It has a rational inverse away from the usual exceptional point. Rational density in Q_p and continuity of these formulas therefore suffice for the asserted one-place approximation. No extra weak-approximation theorem is needed.

On either branch near rho, choose a local nonzero s with arbitrarily large valuation k. Hensel lifting gives a conic point with E=1+2k and v_p(theta-rho)=E. Approximation by rational parameter values sufficiently near it preserves those valuations. This constructs rational conic points with E arbitrarily large at the chosen orientation. Each occurrence may use the same orientation as the old completeness proof at a repeated prime while choosing its own conic point.

All primary and difference points, and hence A,B, are fixed before this approximation. Their old field conditions give v_p(A+rho B)>=e. Choose E so large that E+2v_p(B)>=2e for each nonzero B. Since E>0 this also makes v_p((theta-rho)B)>e, so v_p(Y)>=e and v_p(Y^2-epsilon B^2)>=2e. At the assigned prime R=1, W_F is then integral. Every upper node is integral; the leftmost constant path remains a unit, because every right square is multiplied by r of positive valuation. Hence the root is a unit.

The possibly negative real values of W_F cause no problem. Each upper norm is a sum of nonnegative terms because r>0, and the constant path makes the root positive. Its square times r is positive, has odd valuation exactly one at the selected p, and has even valuations elsewhere. Its reduced denominator is a square. Multiplication by the root square also preserves the required Q_2,Q_3,Q_17 square classes of r. These are exactly the inherited pole-completeness conditions. This proves completeness of the new layer.

## Implementation limits and combinations

The two conic equations and the two equations per field test are quadratic when r,A,B are affine in retained coordinates. A comparator with more complicated coefficients needs explicit product coordinates first. The upper norm formula itself is cubic and must use the existing checked quadratic implementation or a new audited lift. The proof does not by itself certify the final polynomial's degree or coefficient height.

The source checker must bind the per-occurrence conic, every raw r, every original field coefficient/order/conjugation, deterministic even powers, the literal constant, exact tree schedule including carries, and the final pole argument. It must reject conic sharing, theta dependence in A or B, missing fields, altered signs, altered exponents, and any lost constant path. It must account for all old theta/epsilon/paired-test/inverse consumers before removing their coordinates. Conic nonvanishing may justify a source-level removal of a raw inverse, but an unrelated old certificate rule does not automatically certify that removal.

For the actual measured minimal-Jacobi root module, SHA-256 `d9e529f1db230955d65518811354c5b99a1a76d6103b3611b5998c97764193be`, I also checked the old root-global coordinates directly. Theta and epsilon are local indices 69 and 70. Their only root residual is row 58, `2-theta^2+epsilon=0`. Their call consumers are exactly the 13 full calls at slots 28,29, the eight beta calls at slots 13,14, and the 16 Lucas calls at slots 23,24. The other two calls, anchor and scalar-height, do not consume them. The pinned combined builder shows the same separation. Thus removal has no scalar-height mathematical consumer in this baseline. The new source must repeat this complete incidence check after any other root transformation and update construction metadata and indices consistently; these old numeric locations are evidence, not a reusable unconditional deletion rule.

The frozen minimal-Jacobi lists contain 580 field tests. The newer four-field source contains 13*15+8*6+16*12=435. Its field count and tree must be recomputed from that approved source; the old nominal 508-coordinate estimate cannot be added to a separate chart estimate. Repeated fields, shared squares, source aliases, and later eliminations further affect the final count. No measured saving or threshold result follows from this arithmetic review.
