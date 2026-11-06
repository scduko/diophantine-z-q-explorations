# Independent review of the linear ordinary pole

Date: 2026-11-06. Verdict: PASS for the arithmetic replacement in the exact proof below. This does not accept an emitted module, a later constant-path fusion or a whole-source count.

Reviewed proof: `parity/sub5000/linear-pole-next/PROOF.md`, SHA-256 `0b52a6ac4840636be12f455bf0e8b07ba02bb2308493d937afd840ea19bdb510`. The proposal removes the old rational Cayley value and uses g=3-2theta. Its soundness is a new direct negative-odd-valuation theorem, not an algebraic map to the full old parity predicate.

## Local unit and exact normalization

The retained rational conic theta^2-r*s_c^2=2 forces r,s_c nonzero. At an odd prime with odd v(r), the valuation v(r*s_c^2) is odd. It cannot be negative, because the right side of theta^2=2+r*s_c^2 would then have odd valuation; it cannot be zero. Thus it is positive and theta is integral. The product

```
(3-2theta)*(3+2theta)=1-4r*s_c^2
```

is a unit. Both factors are integral, so g is a unit. This conclusion applies to positive and negative odd v(r) and requires no ordinary-prime residue class.

I checked the scaling between the direct eleven-local form and the normalized ten-local form. The direct variables U=r*g, L=r*l, z_direct=r^2*z, w_direct=r^2*w, s_direct=r*s, q_direct=r^2*q, j_direct=r^2*j and k_direct=r^2*k give precisely the displayed direct equations. In particular

```
c*(17r-z_direct)=r*e*(17r-r^2*z)=r^2*(17e-c*z).
```

The last conic is multiplied by r^4; the first conic is unchanged. The inverse scaling divides only by powers of the known nonzero r. It remains valid when any of the pole ordinates, e, l or W is zero. This is an exact equivalence of these two new local forms, not of either form with the old fixed-Cayley block.

## Negative-odd soundness, including zeros

Let b=rW^2!=0 have negative odd valuation at a prime outside2,3,17. Put a=v(r), t=v(W). Then a is odd, l=gW has valuation t, and a+2t=v(b)<0. The first conic is

```
p_witness^2=17r*(1-e)*(1+3e).
```

If e=0, v(e)>0 or v(e)<0, its right side is nonzero with respectively odd valuation a, a, or a+2v(e), impossible for a square. Hence e is a unit. The remaining first-conic zero cases e=1 and e=-1/3 are allowed; they do not affect this conclusion.

Now w=e*(17-r*l^2) is nonzero with valuation a+2t, negative and odd. The last relation factors as

```
(s^2-17w)*(s^2+51w)=17r*q^2.
```

For s!=0, the valuations of s^2 and w have opposite parity, so each factor on the left has the same finite valuation and their product has even valuation. For s=0, the left side is -867w^2, again nonzero with even valuation. The right side is zero when q=0 and otherwise has odd valuation a+2v(q). Both are impossible. Therefore b has no negative odd valuation outside2,3,17.

When W=0, b=0 and this nonzero-input assertion is vacuous. The explicit normalized witnesses l=z=p=q=k=0, e=1, c=r, w=17, s=17 and j=289 satisfy every row; the final conic has its first factor zero. Thus the proof does not hide a nonzero-W or nonzero-ordinate condition.

This is the only ordinary pole assertion consumed by the current norm argument: constant-left noncancellation excludes negative odd raw valuations, and the same inequality bounds then descend to every packed field. No downstream step needs the old global Cayley norm identity. The scalar-height module must keep its original predicate and call.

## Generalized fixed-U completeness

For complete b>0 with square reduced denominator and exceptional local squares, write B=17b and V=B(B-U_o^2). The four stated smallness conditions make V positive and a square at2,3,17. The squarefree positive representatives beta of B and eta of V therefore have the same congruence properties as in the inherited simultaneous-realization proof: beta=17 modulo24 and eta=1 modulo24, with17 absent from eta.

At a beta-support prime outside the exceptional set, v(b) is positive odd because the denominator is a square. The new explicit hypothesis v(U_o)=v(b) gives positive valuation of U_o^2/B, so 1-U_o^2/B is a square unit. Hence eta is a square there and its support is disjoint from beta. At an eta-support prime, unequal valuations of B and U_o^2 would make v(V) even. Equality and strict cancellation are therefore necessary, and B/U_o^2 is a square unit. This gives the reverse mutual-square condition. If U_o=0, V=B^2 and eta=1, so the reverse step is unnecessary. At17 the prescribed smallness condition gives the same conclusion directly.

These are precisely the squareclass inputs to the existing simultaneous-realization, rank-one and restricted-converse argument. The proof retains those inherited hypotheses and conclusions; it does not replace them by a new general converse or omit a rank condition. The old first/h/last-conic witness construction consequently applies without a Cayley equation for U_o.

## Complete source composition

Fix root/contact data and all elliptic/G/ratio field coefficients before choosing private theta. This includes normalized-Lucas coefficients if that independently reviewed source is used. With fixed data, all packed fields and W(theta) remain polynomials in theta. The quantity

```
(r/17)*W(theta)^2*(3-2theta)^2
```

is continuous and zero at theta=3/2 in the real,2,3,17 completions. The same rational conic has local points there because complete r is an exceptional local square. Weak approximation can simultaneously satisfy these neighborhoods and the selected-prime depth. The latter makes W a unit at its assigned prime; the real constant-left path gives W>=1.

Thus b=rW^2 has the original positivity, denominator and exceptional squareclass properties. Set U_o=W^2*r*g. At every odd-support prime of b outside2,3,17, the unit lemma gives v(U_o)=2v(W)+v(r)=v(b). Its smallness quotient is exactly the displayed continuous expression. The generalized fixed-U theorem supplies the remaining witnesses. Nonzero W scaling gives the direct new block and then the exact r scaling gives the normalized block.

This proves integer completeness with all existing root, contact and field data fixed before theta, followed by pole witnesses. The local unit lemma also holds at any other odd-support prime introduced by denominators. No new exceptional prime or prime-pattern condition is needed. The future source must retain the same r/theta conic, complete constant-left norm tree and coefficient independence, and must state the new one-sided negative-odd theorem as its ordinary pole interface. Exact source equations, any W/path elimination, full flattening and polynomial replay remain unreviewed until supplied separately.
