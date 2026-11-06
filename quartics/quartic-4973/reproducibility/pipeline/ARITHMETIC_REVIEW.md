# Independent review of the rational difference reform

Date: 2026-11-06. Arithmetic PASS for `charts/sub5000/RATIONAL_DIFFERENCE.md`, SHA-256 `8558cbfdb09bfaf12054caa2907900bc30b6de91fd6ab43c14ddc294f1cd7e9d`, under the inherited curve, group, formal-logarithm, and source hypotheses stated below. This is a new arithmetic source theorem. It does not assert equivalence of all private witness tuples to the minimal-Jacobi source. A generated source, exact equation/call audit, and complete finite replay are still required.

I read the complete proof and `test_rational_difference.py`, including its cleared chord identity and its torsion-translated examples. No test or source generator was executed here. The polynomial identities are useful finite checks; the half-index and local arithmetic arguments are verified separately below.

## Algebra and exact domain

The base field and curve are K=Q(sqrt(2)), d=3-sqrt(2), D=d^2, and E: y^2=x^3-Dx. Both embeddings of D are positive. The target Q=(a,b) is a retained nonidentity point in G=2E(K)=Z P_*, and F=1/a, q=b/a. In particular a,b,F,q are nonzero. A primary point retains xf=1 and p^2=x-Df, and has y=xp. The unchanged nonvanishing G equations force p != 0. Thus the primary point is an affine non-two-torsion point, but it need not lie in G.

With jz=1/conjugate(z(J)) nonzero, the proposed four field equations are

```
t=fF,
M(1+Dt)=p,
T=2x-pq+2M(q-p),
A*conjugate(T)+conjugate(q-p)*jz=0.
```

Each rational component is quadratic. Put B=1+DfF and k=q-p. Since MB=p and p is nonzero, B is nonzero. Therefore M=p/B and the first three equations determine t,M,T. If T were zero, the fourth equation and jz != 0 would imply k=0. The primary and target curve relations then imply (x-a)B=0, so P=Q. At P=Q, however, T=x+D/x=(x^2+D)/x is nonzero by positivity of D. Hence T never vanishes on a solution, and A is exactly conjugate(Z)*jz for Z=-k/T.

An independently useful numerator identity is

```
B*T = pq*(1-D/(xa)) + 2D*(1/x+1/a).
```

For x != a, substitution in the chord formula for P-Q gives T*X=k*Y, with X,Y its affine coordinates. Thus Z=-X/Y wherever that quotient is defined. The identity extends as a rational function, and the exceptional points can also be checked explicitly.

At P=Q, Z=A=0 and the difference is O. At P=-Q, the formula is the duplication formula, and 2P belongs to torsion-free G, so it cannot be a nonzero two-torsion point. The locus P-Q=(0,0) gives x=-D/a and B=0, so it is deliberately excluded by MB=p.

For P-Q=(s,0), s=d or -d, the translation formulas give x=s(a+s)/(a-s), y=-2Db/(a-s)^2, pq=-2s and ax=s(x+a+s). These denominators are nonzero because Q is not two-torsion. The numerator identity gives BT=2[-s+D(x+a+s)/(ax)]=0. On B != 0 this would force T=0, already impossible. Thus the two poles of z are also excluded. These cases establish the exact open subset used by the source; the proof does not assume a total rational chart for every pair of points in E(K).

## Why the difference formal tests can be removed

At a selected split prime p>76176, the unchanged paired tests for conjugate(f(J)) put the nonzero J in the formal group at the conjugate place. Consequently v(z(J))>0. Decoding the retained paired order-e test for A gives v(A)>=e, and hence

```
v(Z)=v(A)+v(z(J)) >= e+v(z(J)) > 0.
```

Zero is allowed and has infinite valuation. This implication uses no integrality assumption on the rational coefficients before their paired tests are decoded. All alternate orders are 12 or 40, although positivity here only needs e>=1.

For a nontorsion affine R=(X,Y), the exact identity z(R)^2=X/(X^2-D) proves the local dichotomy. If v(X)=0, its right side has nonpositive valuation because D is a unit, contradicting v(z)>0. If v(X)<0, R is in the formal group. If v(X)>0, translation by T0=(0,0) gives

```
X'=-D/X,   Y'=D*Y/X^2,   z(R+T0)=-z(R),
```

so R+T0 is formal and has the same parameter valuation. In either case 2R is formal, and v(log(2R))=v(z(R)), since multiplication by 2 is a unit on this odd-prime formal group. For R=O the equality is interpreted with both sides infinite. The other torsion cases were excluded algebraically above.

It is essential to use the doubled point in this argument. Positive v(z(R)) by itself does not imply R is formal, and no logarithm is taken at a nonformal R. Its possible reduction at T0 is explicitly accounted for.

## Half-integer indices suffice

Every P in E(K) has a unique alpha(P) in (1/2)Z defined by 2P=[2alpha(P)]P_*. This follows directly from the inherited equality 2E(K)=Z P_* and the infinite order of P_*. It does not require the single-x descent lemma, and it does not assert the existence of a half of arbitrary P. All these alpha values are p-integral at the selected odd primes.

Write alpha(P0)=h and alpha(Pi)=m_i. For the root target Q_i=[4n_i]P_* one has alpha(Q_i)=4n_i. For R_i=P_i-Q_i and J=[j]P_*, the exact integer-multiple relation is

```
[j](2R_i) = [2(m_i-4n_i)]J.
```

Both sides are multiples of formal points. Taking the formal logarithm and the preceding valuation equality gives

```
v(Z(R_i)/z(J)) = v((m_i-4n_i)/j).
```

If R_i=O, its doubled index difference is zero, so this also holds with infinite valuations. Because j is the unchanged nonzero integer, v(j)>=0. Thus the alternate tests give h=4 modulo p^e0 and m_i=4n_i modulo p^ei. In particular h is a p-adic unit.

At the primary place, each primary point is already formal by its retained f test. The exact identity [4h]P_i=[4m_i]P0 has integer coefficients and follows from the defining doubled-point relations. Applying the formal logarithm gives log(P_i)/log(P0)=m_i/h. The denominator is nonzero by the formal-logarithm isometry and p != 0. Using [2h]P_i=[2m_i]P0 without accounting for a possible two-torsion discrepancy would have been unjustified; the proof now uses the safe doubled relation explicitly.

The unchanged reciprocal G approximation and ratios therefore imply the same local congruences between the rational proxies and the integer root indices n_i. The private indices need only be integral at this odd prime. No global-height argument measures h or m_i: the first argument measures the unchanged root indices s,t,z and the second measures n,t. Their integrality, height lower bounds, scalar bound, and Lucas equation all remain intact. Thus the full, beta-only, and Lucas-only soundness proofs apply without replacing an integer root index by a half-integer.

## Raw contacts, reduced batches, and completeness

The root-error test remains. The constant-left path remains in every norm tree. At any raw contact with odd valuation, the old norm/pole proof therefore still excludes negative valuation and decodes each retained test at its assigned positive integer order. Removing difference-formal leaves does not remove a premise of this argument. The resulting rational batch sizes are 31, 13, and 25 for the full, beta-only, and Lucas-only modes.

For integral input, use exactly the old private points in G and the old target points. Their reciprocal abscissas are positive in both real embeddings, making B>0. The old private-index choices avoid the affine subtraction exceptions and give differences in torsion-free G; hence no excluded pole or T0 occurs and T is nonzero. The displayed rational formulas supply t,M,T,A, with A equal to the old alternate ratio. All retained tests keep their old valuations. Choose theta only after the actual new coefficients are fixed. The same finite approximation, norm-root unit, positivity, square denominator and local-square arguments then supply the remaining witnesses.

This is equality of input projections with the old source, proved by soundness and completeness. It does not require the enlarged private points to reconstruct old G-chart witnesses. Conversely, the old completeness witnesses do lie inside the new open domain.

## Exact source obligations and interactions

The future checker must verify every primary inverse and curve row, every G evaluation and ratio equation that forces p nonzero, the unchanged nonzero common-J inverse, the four equations above with the indicated conjugations, and each mode's complete ordered retained tests. It must confirm that only the difference-formal leaves were removed and that all 37 position assignments, original affine height targets, scalar source, anchor, and root data persist.

The old minimal-Jacobi source had six field pairs per site when its alternate ratio was included; the new presentation has four. The raw allocation difference is 580 rational coordinates across 145 sites. This is an estimate before later optimization, not a measured saving or a claim of a total below 5,000.

This source drops global squareness of primary f. A proposed conic shortcut that works only for globally square field tests cannot be applied to those f values without another proof. A conic shortcut proved for arbitrary field tests would be a separate compatible candidate after review. Shared primary points across contacts are also separate: this proof retains independently chosen private points and does not resolve cross-prime reduction-order CRT obstructions.
