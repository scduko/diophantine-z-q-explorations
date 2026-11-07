# Audit of the odd product reduction

Date: November 7, 2026.

I found no mathematical gap in the new reduction. I accept its 554-variable construction and its additional 523-variable refinement **relative to the arithmetic inputs of the pinned source construction**. This audit does not independently establish every theorem in the 252-page Version 8 manuscript. The only reproduced defect is a Windows replay bug in the supplied verifier; a non-mutating fix is supplied and tested.

The submitted ZIP has SHA-256 `fcb169b0fe78b7d8c7badec083f23b543901ae0efa17f9bc38f3025511764141`. All 87 entries in its top-level hash manifest match. The main TeX has SHA-256 `5595a6cf5a5159ef1968296dbdd16c344c61652523cd342ce441841f6631d497`, matching its supplied article-review record. The original extraction is preserved under `input/`.

## Confirmed sizes

All counts include the rational input. Each polynomial has degree exactly four and primitive integer content one.

| Construction | Total variables | Existential witnesses | Quadratic residuals | Nonzero monomials | Maximum absolute coefficient |
| --- | ---: | ---: | ---: | ---: | --- |
| Odd product | 554 | 553 | 523 | 33,440 | `64 * 3^(2^27)` |
| Odd product, decimal coefficients | 571 | 570 | 540 | 33,490 | `3^2048 + 1005072314631333` |
| Odd product and asymmetric depth | 523 | 522 | 492 | 35,163 | `64 * 3^(2^27)` |
| Depth refinement, decimal coefficients | 540 | 539 | 509 | 35,213 | `3^2048 + 1005072314631333` |

The latter coefficient has 3,247 bits, so its magnitude is strictly below `2^3247`. The 523- and 554-variable tables use the fixed coefficient `S = 3^(2^26)`; S is not a variable. Their maximum is `64*S^2`. Every coordinate monomial has just one S-power term, so specializing S cannot cancel any reported monomial. The 17-coordinate chain has a unique rational solution and replaces S exactly. The 540-variable ordinary table occupies 4,309,114 bytes in its supplied JSON format.

## Arithmetic checks

### Exact height additivity

Main TeX, Lemma `lem:product`, lines 79 onward.

At a finite place with v(D)=0, E_1 is an open subgroup and E(K_v)/E_1 is finite. The image of T_0=(0,0) has order two: T_0 is not formal. The identity x(Q+T_0)=-D/x(Q) identifies positive x-valuation with the T_0 coset of E_1. If an odd multiple of P is formal, the order of P in the quotient divides an odd integer. Its cyclic subgroup cannot contain the nonzero element of order two. Consequently none of its multiples has positive x-valuation. If no odd multiple is formal, none of the odd multiples has negative x-valuation. This proves common weak signs at each such place, including the place over two. Minimality at two is not needed: the formal neighborhood for the integral equation is sufficient for this argument.

The only finite place with v(D)>0 is (3-sqrt(2)), above seven. P reduces to (1,6), a nonsingular point on y^2=x^3 over F_7. The nonsingular-reduction subgroup is closed under multiplication. Positive x-valuation would force positive y-valuation and reduction to the singular point (0,0), so it cannot occur on this orbit.

At both real embeddings every nonidentity double has x a nonzero square. The curve equation then forces x>3±sqrt(2)>1. Local positive-part logarithms therefore add at every place. The product is taken in K, not replaced by its rational norm. I found no cancellation omitted from the argument.

The three scales 1, C_0^2, (1+C_1^2)^2 are positive nonzero rational squares because both real values of C are positive. The stated estimates h(C_0)<=T, h(C_1)<=T/2 follow from the rational height identities. In particular, h(1+r^2)>=2h(r) follows by writing r in lowest terms. Thus h(C)<=3T/2+3log(2)/2, retaining the old 7H constant and the bound B^2-6<7H|N|^(19/k).

### Odd-coset chart and its predecessor

Main TeX, Proposition `prop:odd-chart`, lines 155 onward; predecessor note, Proposition `prop:chart`.

The x-squareclass homomorphism is justified by the line-intersection identity and the exceptional addition cases. From 2E(K)=ZP and P=2R_0, every point has a unique expression mR_0+T with T in E[2](K). The squareclasses of epsilon=1+sqrt(2), -1, and d=3-sqrt(2) are independent: their norms first force the epsilon and d exponents to be even, and the real signs exclude -1. The added equations therefore select exactly P+4E(K), not all square-abscissa points.

I checked the halfpoint curve equation, tangent slope, doubled abscissa and doubled ordinate as exact polynomial identities modulo t^2=2(h^2+j), with D=h^4-j^2. The converse chooses (2m+1)R_0 as a halfpoint. Nonzero denominators follow from D!=0 and the displayed identities. The chart can change the sign representation of h,j while preserving the represented point, which is the correct projection statement.

The earlier chart reduction also checks out. For V^2=U^3+4DU, odd valuations of U are impossible except possibly at the prime over seven; there the putative exceptional valuation would require -4 to be a square modulo seven, which it is not. At two, equality of the two summand valuations occurs only at the even valuation v(U)=2. All finite valuations of U are even, and U is positive at both real embeddings. The norm-Euclidean property of Z[sqrt(2)] and its unit signs then give that U is a square. This proves the predecessor chart equivalence without an extra rank assumption.

### Labels, scalar shift and bounds

Main TeX, Section 4, lines 202 onward.

For X=u/v in lowest terms, integrality of 2X^2+3 implies v^2 divides 2, hence v=1. For integral X this label is odd. The scalar contact 2401 would require X^2=1199; all other contacts are excluded by beta>=3. The required even negative valuations at odd primes are preserved.

The source changes the scalar and anchor point to S-P, while keeping S in the root product and comparisons. Its subtraction guard excludes a=±1. Completeness chooses a large positive scalar index s divisible by six and takes a=s+1, so this guard excludes no needed witness.

For c=|a-1| the smaller anchor S=3^(2^26) gives log_2(c)>25,165,823.5. Combined with log_2(H)<2,093,966, this implies c>(80H)^10 and H*c^(19/32)<c/80. Since |a|>=c/2, the two height contradictions retain their stated margins. I checked the powers and constants, including |F|<5B^4, the bound 24H in the first contradiction, and 31|a|/200<|a|-3 in the second.

For the Lucas construction, U_j=j modulo a-2 and the sequence modulo two has period 0,1,1. With a=1 modulo three and k=2(a-2), k=1 modulo three; U_k and U_(k+1) are odd. Thus b=U_k/(a-2) and t=U_(k+1) are odd integers and satisfy the required equation. The general argument, not just sample values, was checked; small exact examples are included in `IDENTITIES.json`.

### Asymmetric formal depth

Main TeX, Section 5, lines 303 onward.

The local order of reasoning is sound. Formal membership first gives that log(Q)/z(Q) is a unit, congruent to one to order 4v(z(Q)). Since one of h and h-1 is a p-unit, one full logarithm ratio is integral. The order-40 cross test transfers integrality to the other approximate ratio. Only then does integrality of z(U_i)/z(H), together with v(z(H))>=20, imply v(z(U_i))>=20. The primary relative error is now at least order 80, and the retained alternate truncations have order 40. Multiplying the resulting integral congruences by h and h-1 proves L_i=n_i modulo p^40. The same reasoning works at inert primes, where conjugation preserves the valuation.

The coefficient-tail estimate follows from the existing recurrence and factorial denominator bound. For large indices, (4j+1)/(p-1)<=j and 3jr>=4r. Thus the strengthened first-term estimate is legitimate; no high-precision conclusion is assumed before establishing integrality.

### Prime separation and completeness

Main TeX, Lemma `lem:separation`, lines 323 onward; Version 8, Proposition `prop:v5-artin-patterns` and subsection `subsec:v5-diagonal`.

I read the actual pinned Version 8 count and final order of limits. They supply a fixed positive proportion of NT after obstruction removal, with all root, scale, modulus and ray data fixed first. The extra condition tau(N)*N^(1/6)/(log N)^k -> infinity can be imposed in the same piecewise-constant diagonal choice. The weight of w<N^(1/3) is O(N^(4/3)(log N)^k)=o(NT), leaving an admissible pattern.

After repeated forms are merged, distinct prime values differ by at least c_*N^(2/3). Hasse's bound makes each opposite group order p_j+O(sqrt(N)); all selected primes are asymptotic to the same u. A selected prime dividing an opposite order would consequently equal it. Distinct indices contradict the separation bound. Equal indices contradict divisibility of the group order by four. This proves the additional coprimality, rather than assuming a stronger prime-pattern theorem.

The added factor Pi^19 is coprime to both M_+ and the continuity modulus L. The old compatibility gcd(M_-,L)=16 and 64|h_0 therefore suffice for the three congruences. Multiplication by the doubling-image order gives formal depth at least one, and p^19 adds nineteen. The real-progression argument still applies to the resulting fixed progression. All orders are fixed before selecting the prime pattern, so the existing detector completeness estimates apply.

## Source and finite verification

I fetched the exact contribution commit `772c4adf4a05e21255e4c1784e08e917fda4c68a` and verified its pinned inputs. The archive's compiler, independent checker, source TeX and direct-target proof note are byte-identical to those sources. `SOURCE_DIFF.txt` compares a freshly generated direct-target builder with the archive's base833 builder. Its changes are precisely the earlier chart replacement, cancellation of ordinate products, Laurent chain, scalar preparation and associated quotient changes explained in the predecessor note. The new patches then implement the odd charts, product scales, scalar shift and asymmetric tests described in the main article.

The submitted full source replay passed on a separate copy. It reproduced both precursors, checking 495 and 458 gate identities, then passed all four final package checks. The replay explicitly distinguishes the historical S=3^(2^27) generator metadata from the final specialization S=3^(2^26). That smaller specialization also has the required arithmetic anchor margin; it is not justified merely by relabelling metadata.

Separately, `independent_finite.py` imports no submitted code. It checks the archive hashes, seven and nine certified eliminations, unchanged input coordinate, normalized integer residuals, unique constant lifts, and every coefficient of all four sums of squares. It confirms exact degree, support, primitive content, and the maxima in the table above. `INDEPENDENT_FINITE.json`, `SOURCE_LINEAGE.json`, `IDENTITIES.json` and `replay-output/REPLAY.json` record the results.

## Reproduced defect and fix

Both copies of `verify_elimination.py`, lines 108-109, overwrite `integer-candidate-ir.json` and `verification.json`. These are hash-pinned inputs. On Windows the default newline conversion changes their bytes. After a successful first run, a second `verify_all.py` run fails with `AssertionError: symbolic523/integer-candidate-ir.json`.

`READONLY_VERIFIER.patch` replaces the writes by equality checks against the existing parsed JSON. `check_readonly_fix.py` tested the change in memory, with two consecutive successful full verification runs for each package and all input bytes unchanged. `READONLY_FIX_TEST.json` records the result. When applying the patch to a distributable archive, update each package's verifier hash and then the top-level manifest. Do not change historical evidence to make an old hash appear current.

This is a reproducibility defect, not a counterexample to any polynomial or arithmetic lemma. The immutable original input and both repository worktrees remain unchanged.

## Scope of acceptance

The new argument still consumes the source generator statement, effective five-contact height bound, scalar and anchor lemmas, pole-completeness results and the quantitative prime-pattern construction. In particular, it does not eliminate the original restricted-converse or analytic dependencies. The direct-target change also has a mathematical proof obligation; I checked its doubling-image CRT argument and shift-one logarithm identities against the exact source note, rather than treating its compiler output as an arithmetic proof.

No additional unproved external theorem was needed for the new steps. Hasse's bound and formal-group facts are already used in Version 8. Their new applications, the odd-product identity, odd-coset chart, shifted labels and asymmetric-depth argument should receive explicit entries in the theorem-application inventory if this improvement is integrated. This report is an internal model audit, not human peer review or a Lean formalization.
