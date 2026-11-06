# Independent primary-membership review

PASS for `charts/DESCENT_MEMBERSHIP.md`, SHA-256 `97d4af4394f5629bf5b9e199e7f2adfb1ed54ec584a5c9452b6283a7e09a0814`, relative to the exact released generator/descent result and the square-transfer source reviewed here. This is a theorem-dependent existential source equivalence. It is not a polynomial-identity elimination or a rational choice of a half point.

I inspected the actual released `quartic_12504.tex`, SHA-256 `38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37`, at the proof of `prop:generator`, lines 282 onward. It explicitly calls the first map the x-squareclass map in the two-isogeny descent, proves its image has order eight, and separately states `[E(K):2E(K)]=8`. These are not the cardinalities of the full two-descent pair or triple. The normalized curve multiplies x by epsilon^4, a square, so the same single-map statement transports to D=(3-sqrt(2))^2.

The exact map is delta(O)=1, delta((0,0))=[-D], and delta(P)=[x(P)] otherwise. The author's chord-product proof gives the homomorphism on all cases: a nonvertical line has intersection-abscissa product c^2; a line through (0,0) has the remaining product -D; tangencies are counted with multiplicity; reflection preserves x; vertical chords and O give the neutral case. The explicit translation formula for (0,0) handles its special input. Thus every double is in the kernel.

The image has order eight, so the kernel has index eight. Since 2E is contained in it and has the same finite index, equality follows. This comparison uses two exact equalities. An image upper bound, or the rank statement without its torsion/index conclusion, would not justify it.

For another check on the map identification, the four torsion images are 1,-1,d,-d and the point with x=1+sqrt(2) supplies the third generator. Their square classes are independent: the sign vectors of -1 and 1+sqrt(2) are independent, d is positive in both embeddings, and its norm is 7. This is precisely the single abscissa map used in the released paragraph.

Now the retained target is a double with F_Q=U^2 and U nonzero. The transferred equation r^2=f F_Q and xf=1 give u=r/U, u^2=f, and x a nonzero square. The retained p^2=x-Df gives the curve point P=(x,xp). It has trivial delta and therefore belongs to G=2E(K). As an affine point it is not O; the released theorem makes G torsion-free, so y and p cannot vanish. No new guard or new group assumption is needed.

To restore a deleted v, choose a half V=(a,b) with 2V=P. It exists by the kernel equality. Since P is nonidentity, b is nonzero. The exact duplication identity gives

```
x(P)-d = (((a-d)^2-2D)/(2b))^2.
```

Multiplication by u gives the proposed `v=u*((a-d)^2-2D)/(2b)` and v^2=1-df. The restored v is nonzero: if v=0, then x=d, which would be a nonzero two-torsion point and could not lie in torsion-free G. Equivalently the retained p equation would force p=0. All other coordinates and all rational test values stay fixed. Choosing V is an existential use of the inherited group theorem, not a globally defined rational function of the retained P.

The previously checked Jacobi identities, identity-difference case, G nonvanishing, and scalar/height arguments therefore remain valid after reconstruction. The three comparator modes are also compatible: each retained private point has its own transferred-square r and exactly one deleted v. No denominator, order-one w test, alternate Z ratio, or common-J value changes.

The combined checker must bind the field to Q(sqrt(2)), the exact normalized curve, the retained target-doubling chains and their nonzero inverse data, every xf and p equation, every transferred-square equation, and all outside uses of the deleted v. This proof does not support applying a generic local v-elimination rule to an unrelated curve. The source must explicitly cite the released generator/descent result in its arithmetic dependency record.

The source note's 370-coordinate estimate assumes 37 full five-point comparisons. A three-mode source has 145 private points, so this deletion has 290 private rational coordinates at that allocation level. Neither number is an optimized endpoint saving. A generated source, full replay and collected coefficient check remain necessary. No local computation was performed for this review.
