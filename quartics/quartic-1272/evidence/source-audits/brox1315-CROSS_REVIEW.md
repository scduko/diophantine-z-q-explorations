# Cross-review of the unramified logarithm supplement

Reviewed `brox41/reciprocal_unramified_repair.tex`, lines 1-103, against the frozen upstream `common/upstream-quartic-12504-28e87b1.tex`, lines 8753-8843, and Brox v3, lines 2401-2411, 2641-2670, and 4181-4209. I did not edit the supplement.

Verdict: the proof is correct for its intended rational primes greater than 76176, at both split and inert places of `Q(sqrt(2))`, and for precisions 16, 52, and 64. It closes a statement-scope omission in the inherited split-prime lemma. It does not introduce a new arithmetic hypothesis. Before making it a standalone inserted statement, I recommend the two scope edits below.

## Scope edits before insertion

1. At line 7, write “Let `p>76176` be a rational prime.” Primality is implicit in the existing use of places above `p`, but should be stated.

2. At lines 76-78, explicitly restrict the denominator precision to the proved set. For example, choose `k_i,d_i` in `{16,52,64}` with `d_i>=k_i`, and write

   `L_i=L_{k_i}(U_i)/L_{d_i}(H)` and `L'_i=sigma(L_{k_i}(V_i)/L_{d_i}(V_0))`.

   The phrase “a denominator precision at least `k_i`” is broader than the lemma if read without the surrounding manuscript. Arbitrarily long truncations need not have their nominal precision once denominators divisible by `p` enter the coefficients. The intended denominators 52 and 64 satisfy the proposed restriction. This is a scope correction; it changes no Brox formula or bound.

The inherited notation otherwise supplies the integer labels, conjugation, nonidentity points, and nonzero denominator guards. In a standalone version, say explicitly that the corollary uses the same `K,E,p,mathfrak p` as the lemma.

## Checks

The discriminant of the displayed curve is `64D^3`. The element `D` is integral and has rational norm 49, so every prime under consideration is a prime of good reduction with `D` a unit. The extension is unramified because the quadratic field has discriminant 8. Consequently positive formal depth is an integer `r>=1`, including at inert primes. Nonidentity formal points have nonzero abscissa and ordinate, so `f` and `z` are defined.

The parameter identities and differential equation at lines 36-46 match the frozen upstream proof. The branch of the square root has constant term one; the antiderivative `zG(w)` has zero constant term. Thus it is the normalized formal logarithm in characteristic zero.

For `j>=1`, the denominator bound at lines 48-52 is valid. For `4j+1<p`, the coefficient is integral. Otherwise `j>=19044`. Since `p-1>=76176`, `(4j+1)/(p-1)<=j`; since `r>=1`, `4jr-j>=3jr`; and since `m` is 4, 13, or 16, `3j>=4m`. All inequalities in lines 54-60 follow. For large `j`, the lower bound `3jr` tends to infinity, so this controls the whole tail rather than merely finitely many coefficients. Multiplication by `z` gives `(4m+1)r=(e+1)r`.

Every nonconstant term of `G(w)` has positive valuation by the same two cases. Therefore the leading term `z` is uniquely least and the full logarithm has valuation `r`; no nonvanishing assumption is hidden in dividing by it. The relative error has valuation at least `er>=e`. A quotient of two elements of `1+p^e O` has the claimed precision. The truncated logarithm is nonzero locally as a consequence.

For the corollary, the retained guards give `h!=0,4`. The logarithm homomorphism implies the exact rational ratios `u_i/h` and `(u_i-4n_i)/(h-4)`, even if `P` itself is not formal: apply it to the equal formal multiples `[h]U_i=[u_i]H`, and to their alternate counterparts. Since `p` is odd, at least one of `h,h-4` is a unit. The difference test then makes both truncated ratios integral, and valuation equality makes both exact ratios integral. Relative precision becomes absolute precision. Multiplying the two congruences by `h` and `h-4` yields `4L_i=4n_i` modulo `p^{k_i}`, and division by four is valid. At an inert prime, conjugation acts continuously within the same completion and preserves valuation, so no step changes.

## Limits

This is a local lemma for the specified characteristic-zero quadratic field and large rational primes. It does not assert the estimate at ramified primes, at primes 2 or 7, at all good primes without the displayed cutoff, for arbitrary number fields, or for arbitrary truncation orders. It does not replace the separate global nonvanishing lemma for points that are not formal at a chosen place. That global argument at upstream lines 8818-8843 covers all required truncation degrees `3,12,15` because each is at least 2.

Brox lines 4206-4207 already explicitly cover the unramified split/inert distinction for order 52. The supplement makes the shared use of orders 16 and 64 equally explicit. It establishes no missing gate list, coefficient table, or external arithmetic theorem.
