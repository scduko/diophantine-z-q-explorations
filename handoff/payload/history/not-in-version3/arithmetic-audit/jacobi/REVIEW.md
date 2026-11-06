# Jacobi arithmetic checkpoint

The complete-difference equations pass the arithmetic interface review. They can replace the guarded affine differences in the reviewed H19/root37/high40/beta12 construction, subject to a new source identity and a combined source audit. The same reasoning applies to the separately reviewed H18 parameters. This is not a rational bijection with the old source: identity differences become allowed.

This checkpoint reads `charts/PROOF.md`, SHA-256 `c07709254a482696dea7e71c7e7380af51bc2fb36f94371e8db64781e48468f5`, the source files below, `test_jacobi.py`, the released compiler's complete list of difference consumers, and `batching/JACOBI_REVIEW.md`. The latter's SHA-256 is `98691769d8e27818e775cd95103eb829d44bd987447f202c293b2a191d0e468f`. No compiler, test, or heavy calculation was run locally.

| File in `charts/` | SHA-256 read |
| --- | --- |
| `jacobi_kernel.py` | `69b2e0a46d7358a8d16e339fde141cb24a819c3878b940250cdc1695dc5996c0` |
| `build_jacobi_source.py` | `85d3075bb686009dca664fba172149b63e29b3d5bfc7cef0b84db52c8d13bd55` |
| `check_jacobi_source.py` | `9bdf726f8dc00f1451d97bbd6feae86b6b0175e7b73d6dd7dbfb04cb1b50f646` |

## Exact point and parameter interface

Use K=Q(sqrt(2)), d=3-sqrt(2), D=d^2. A primary point has x=u^-2 and p=y/x. A shared target has a=U^-2 and q=b/a. Set h=up, H=Uq, r=uU, k=q-p, B=1+Dr^2. Both u and U are nonzero. The equations are

```
r=uU, w=rv, v+Drw=k,
T=2x-pq+2pv, ZT+k=0.
```

B is positive in each real embedding and therefore nonzero. Writing N=uH-Uh and C=hH(1-Du^2U^2)+2DuU(u^2+U^2), the equations imply

```
v=k/B, w=N/B, TrB=C,
h_R=Tr/B=C/B^2, h_R^2=1-Dw^4, Z=-w/h_R.
```

I checked the T identity independently by substituting p=h/u and q=H/U: `TrB=2U(B-h^2)/u+hH(2-B)=C`. The quartic and chord identities in the batching review and independent test give the actual group difference P-Q. No division by w, k, or x-a is used by the source.

The denominator h_R cannot vanish. Otherwise `(dw^2)^2=1`, whence `7 Norm(w)^2=1`, impossible with rational Norm(w). Consequently T is nonzero too. For w nonzero, the difference coordinates are `x_R=w^-2`, `y_R=h_R/w^3`, and its parameter is exactly `-x_R/y_R=Z`.

At P=Q, k=w=Z=0 and h_R is 1 or -1 according to the chosen lifts. Both represent the identity. Conversely w=0 forces p=q, then `(x-a)(1+D/(xa))=0`; its second factor is B, so P=Q. At x=a with P different from Q, Q=-P and the formulas give 2P by the tangent formula. Primary p is nonzero, so this tangent denominator is permitted. Changing the sign of either square-root lift changes w and h_R together and leaves the represented point and Z unchanged.

Every new target square root exists without an extra arithmetic hypothesis. The target is a second ordinary double. For its preceding point `(x2,y2)`, take `U=2y2/(x2^2+D)`. The old doubling inverse makes y2 nonzero, and positivity makes x2^2+D nonzero. The doubling formula gives U^2=1/x4. Then q=y4/x4 and f=1/x4 satisfy all added shared equations. Thus the target extension imposes no new condition on a former root assignment.

## Soundness at arbitrary raw contacts

The root37 coverage proof and all raw nonzero guards remain in force. At any p>76176 with odd raw valuation, the same constant-left norm/pole argument first excludes a negative valuation, then gives the required integer orders for all rational tests. The root-error test selects a split root rho. Applied to the two rational tests of conjugate(w), the existing identity `theta-rho=(theta^2-2)/(theta+rho)` gives positive valuation of w at the opposite place. This does not assume ordinariness in soundness or integrality of the rational coefficients of w.

If w is nonzero, `h_R^2=1-Dw^4` makes h_R a unit there, and `v(Z)=v(w)>0`. The actual group difference is in the formal group. If w=0, it is the identity, also in the formal group, and Z=0. Replacing the old order-one test on f_R=w^2 by one on w therefore gives exactly the formal membership needed downstream. At a split prime the valuation is integral; positive valuation of w^2 is equivalent to positive valuation of w.

The released compiler consumes a difference only through this formal-membership test and its alternate parameter ratio Z/z(J). It does not invert the difference's parameter or its logarithm. The common J is still a nonzero chart point, so z(J) and log(J) are nonzero. For a nonidentity formal difference R, formal logarithm isometry gives

```
v(Z/z(J))=v(log(R)/log(J))
         =v((m_i-4n_i)/j),
```

and similarly `(h-4)/j` for the common private point. For the identity the numerator on both sides is zero and the valuation is infinite: the target index difference is exactly zero because the retained generator has infinite order. Thus allowing identities does not weaken any index congruence. In particular h=4 is harmless, although h=0 remains excluded by the primary chart.

All primary points, primary formal tests, reciprocal G polynomials, and primary ratios stay unchanged. The reviewed global G nonvanishing still forces their p_i and Lambda denominators to be nonzero. There is no new inverse-log condition. The high-order and beta-order alternate tests therefore produce exactly the old congruences. Both global contradictions are unchanged.

The direct rational height targets in root37 must remain the eight coefficients of the original unscaled x(A), x(S), x(T), x(Z). The U,q coordinates belong only to the comparison-target interface. They must not replace those height targets.

## Completeness and the common root

Use the existing integer-input construction, which already chooses private indices away from 0, 4 and -4. It gives noncoincident differences and so lies in the old affine open subset. Extend the shared targets by the rational square roots above and evaluate the Jacobi equations. The computed Z equals the old formal parameter, so every alternate ratio keeps its required valuation. Since the difference is formal, the computed w has positive integral valuation and meets its order-one condition. The construction would also handle an identity difference with zero leaves, but it does not need one.

Choose theta only after all these new rational coordinates are fixed. At each selected prime there are finitely many expressions A+B sqrt(2). Choose the approximation deep enough both for `v((theta^2-2)B)>=e` and `v(A+B theta)>=e`. A negative valuation of B merely raises this finite requested depth. The old f_R coefficient bounds cannot be reused for w. Repeated raw positions assigned the same prime retain a common orientation, so their finitely many demands can be maximized before the CRT choice. This creates no circular dependence: the private points and Jacobi coordinates do not depend on theta.

The normalized norm leaves are then integral at their assigned primes, with the root-error constant-left branch retained. Zero identity leaves are allowed. The norm root is a unit at the selected prime; multiplying its square by the raw contact leaves even valuations elsewhere. The root37 factor D0^2 at infinity is still a square. Positivity and the required Q2, Q3 and Q17 square classes are unchanged even if a new coordinate has a denominator at one of those places. The same pole witnesses consequently exist.

## Remaining source obligations

The current charts producer and checker explicitly target the released 64/16, 41-contact, anchor24, scalar48 source. Their finite validation cannot certify the H19/root37/high40 composition. That combined source must separately reconstruct its 37 calls, exact parameter lists and G outputs, retain the same common/root data, and route U,q only into the changed comparison slots. It must check that every removed affine-difference coordinate and guard has no remaining consumer. Shared target overhead must be counted once.

The independent algebra tests include generic chord identities, sign lifts, P=Q and P=-Q. The independent source mutation tests target the five equations, target equations, boundary slots, formal w arguments and unchanged alternate Z arguments. Execution and collected coefficient expansion are still required. No count or coefficient bound is asserted by this checkpoint.
