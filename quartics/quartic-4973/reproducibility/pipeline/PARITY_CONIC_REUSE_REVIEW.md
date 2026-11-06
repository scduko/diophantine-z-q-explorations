# Independent review of private-conic reuse in the parity predicate

Date: 2026-11-06. Arithmetic verdict: PASS for the stated new source and its exact premises. No implementation or measured endpoint is accepted by this note. The reverse direction is integer-input completeness with a newly chosen private conic parameter; it is not a bijection with every old fixed-conic witness tuple.

Reviewed proposal: `parity/sub5000/PARITY_CONIC_REUSE_PROOF.md`, SHA-256 `a7d2712ce511aca30f5c8e94e0e2ce93c6ee64e21074e2bff91f412fe5a1cb5c`, relative to `work/quartic-sub10000-20261106/`. I compared its fixed-U claim with the actual `lem:original-seven-parity-completeness` proof and preceding simultaneous-realization lemma in the Version 3 manuscript, rather than relying on a summary of their conclusions.

The previously reviewed scaling argument is `PARITY_SCALE_PROOF.md`, SHA-256 `5d36002ff1b144135c5c27735c909553e1b469774cb227ae5cf36f55ebde63c4`. The private-conic theorem is `ODD_DISCRIMINANT_PAIR_COMPRESSION.md`, SHA-256 `ef4de3f02fa3d17c18dc7c2af490960a62f35cc541eac8e4b80958d320fa8ab9`.

## Exact extension to the old predicate

Keep the existing rational conic theta^2-r*s_c^2=2. It forces r and s_c nonzero. The new two equations are

```
D=4*theta^2-7,
D*(U+r)=2*r.
```

Here D is a new rational parity coordinate, not the fixed elliptic-curve coefficient. It never vanishes over Q: D=0 would make 7=(2theta)^2 a rational square. These equations give

```
D=1+4*r*s_c^2,
U=r*(2-D)/D=r*(1-r*(2*s_c)^2)/(1+r*(2*s_c)^2).
```

Thus t=2*s_c is a legitimate Cayley parameter. With v=4*r*s_c/D and a=r*v,

```
U^2+r*v^2
=r^2*((2-D)^2+4*(D-1))/D^2
=r^2.
```

Adding these v,a to the remaining new equations gives exactly the thirteen-variable scaled parity template. Its proved map then gives the old pole predicate at b=r*W^2. This implication preserves the actual conic and all surrounding field/norm values, including arbitrary signs and exceptional raw contacts. No real or local approximation hypothesis is used in soundness.

At W=0, retain the forced D,U and choose L=z=p=q=k=0, e=1, c=r, w=17r^2, s_p=17r and j=289r^2. The p equation has coefficient -17-34+51=0; the last equation vanishes because j=17w and 289+578-867=0. This explicitly covers a potentially zero norm root in an arbitrary rational source solution. The map to the old predicate at b=0 requires no division by W. For W!=0 the earlier scaling maps use only permitted powers of W. No inverse of U, e, w, a difference parameter or a parity witness is assumed.

Consequently all prior odd-contact soundness arguments still apply: the new block implies the original pole predicate, and the conic/norm argument then excludes a negative odd raw valuation and recovers the field orders. In particular a zero W cannot evade that argument at an odd raw valuation, because norm noncancellation and the literal-one path already make W nonzero there.

## What the inherited completeness proof actually needs

Let b>0 have square reduced denominator and be a square in Q_2,Q_3,Q_17. Put B=17b. For fixed rational Cayley witnesses t_o,U_o, it is enough that

```
U_o^2/B < 1 in R,
v_2(U_o^2/B)>=3,
v_3(U_o^2/B)>=1,
v_17(U_o^2/B)>=1.
```

These make V=B(B-U_o^2)=B^2(1-U_o^2/B) positive and square at the three finite places. The original proof uses the freedom to choose t_o only to obtain precisely these inequalities. Its subsequent argument works for the fixed choice:

* At an odd-support prime of the positive squarefree representative beta of B outside 2,3,17, the square denominator of b makes v(b) positive odd. The Cayley quotient gives v(U_o)=v(b), for every rational t_o, including t_o=0. Hence 1-U_o^2/B is a square unit and V is locally square there.
* At a prime of the squarefree representative eta of V, v(B) is even. An odd v(V) forces equality of the valuations of B and U_o^2 and strict cancellation. Hence B/U_o^2 is a square unit. This is the other mutual-square condition. If U_o=0, eta=1 and this step is unnecessary.
* The exceptional local conditions give beta congruent to 17 modulo 24, eta congruent to 1 modulo 24, disjoint supports, and 17 not dividing eta. The same simultaneous-realization and rescaling proof supplies the remaining witnesses.

No later step requires another adjustment of t_o or U_o. The proposal therefore extracts a valid fixed-U lemma. Its inherited restricted-converse, descent and forward-rank dependencies remain exactly those of the old lemma; this review does not strengthen their status or introduce a new simultaneous-realization theorem.

## One private conic meets all completeness conditions

Follow the accepted integer-input construction through the root data, contact primes and private elliptic points. At each ordinary occurrence, r=d0^2*p>0, with p>76176 the sole prime of odd valuation, p congruent to 1 modulo 8, v_p(d0)=0, and r square in Q_2,Q_3,Q_17. All field coefficients A_i,B_i and orders are fixed before choosing the conic point.

For this fixed data,

```
W_i(theta)=(A_i^2+2*A_i*B_i*theta+2*B_i^2)/r^(2e_i)
```

is a polynomial in theta with rational coefficients. Every upper node is obtained by polynomial operations, so its root W(theta) is also a polynomial. No denominator depending on theta has been hidden here; the only field-node denominator is a fixed nonzero power of r. Large coefficients or negative coefficient valuations affect the necessary approximation depth but not its existence.

At the selected prime, use a nonzero local s_c of sufficiently large valuation and the Hensel branch near the chosen rho^2=2. This gives a positive odd error valuation 1+2v_p(s_c), as large as needed for all field nodes. A sufficiently close rational conic point preserves these strict finite valuation bounds. Then every W_i is p-integral, and the all-left literal-one path makes W a p-unit. Approaching (rho,0) is shorthand for this construction; an actual rational solution cannot have s_c=0.

At the real place and at 2,3,17, use the local conic point

```
theta=3/2,  s_c=1/(2*sqrt(r)).
```

It exists by the stated positive/local-square conditions. At this point D=2!=0 and g(theta)=(9-4theta^2)/(4theta^2-7)=0. Therefore

```
R(theta)=(r/17)*W(theta)^2*g(theta)^2
```

is continuous and zero there. In particular it can satisfy R<1 over R and valuations at least 3,1,1 at 2,3,17. D=2 being a nonunit at 2 is harmless: it is nonzero, so its inverse is continuous in a sufficiently small 2-adic neighborhood. The factor 1/17 likewise changes only the required 17-adic depth. If W vanishes at a local target, continuity still holds and makes the condition easier, not harder.

These requirements are at five distinct places. The rational conic has a rational point by the already proved norm-Euclidean construction. Its line parametrization identifies an open subset with an open subset of the rational line. Each desired local neighborhood contains a point in that open subset; avoid the finitely many excluded parameter values. Rational weak approximation for that finite set of places then gives one rational parameter meeting all neighborhoods. This elementary approximation can be obtained from finite CRT conditions on a numerator with a sufficiently large denominator prime to the finite places, leaving real mesh arbitrarily small. No uniform quantitative bound is needed. Thus no new distribution-of-primes or simultaneous-elliptic-points input is being assumed.

For the resulting rational point, r>0 and the constant-left norm path give W>=1 over R, so W!=0 and b=rW^2>0. The selected-prime unit property gives v_p(b)=1. At every other prime v(r) is even, so v(b) is even; the reduced denominator is a square. Local squareness of b at 2,3,17 follows from that of r and W!=0. Set

```
t_o=2*s_c/W,  U_o=W^2*U.
```

They satisfy the old Cayley equation at b, and U_o^2/(17b)=R(theta). The fixed-U lemma supplies the remaining old witnesses. Their scaling map gives the new twelve-variable block. The selected-prime field conditions, root choices and elliptic points have all remained intact.

Repeated primes across contacts do not create a conflict: each occurrence still has its own conic. Soundness does not require their orientations to agree. Completeness can retain each previously chosen orientation while making the additional exceptional-place approximations.

## Mandatory source boundary

The new block is allowed only at ordinary comparison occurrences whose exact raw r, private theta and norm root W are passed together. Its coefficients A_i,B_i must remain independent of that conic's theta,s_c,S_c. A dependence introduced through an alias or another call would break the polynomial-in-theta completeness argument and must be rejected by a complete incidence check.

The source must retain the exact field orders, powers r^(2e_i), constant-left norm tree and original root/height targets. It must replace only the two old b,W^2 argument gates and the matching old parity occurrence. The old scalar-height batch remains outside the proposal. New private variables must be fresh, the block must have exactly the displayed twelve locals and ten rows, and all deleted gates must have no unaccounted outside use. D and s_p need names distinct from the curve constant and conic coordinate.

The four-field rational chart and the newer joint chart are both compatible at the proof level because their actual field coefficients are fixed before the conic choice. A direct local Lucas residual would also need its evaluation coordinates fixed first. Each combined emitted source still needs its own typed boundary, independent full source reconstruction, arithmetic binding and finite replay.

The expected local count is twelve variables and ten quadratic rows, compared with fourteen/eleven before square-factor fusion and thirteen/ten after it. This is not a final measured saving. No implementation was run or accepted by this review.
