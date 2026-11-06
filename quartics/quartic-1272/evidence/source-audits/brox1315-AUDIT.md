# Audit of the 1315-variable quartic

The displayed arithmetic modifications and the affine anchor transformation survive this audit. I found no invalid identity, omitted domain condition, or counterexample to the rational input projection in the parts of the construction that the public manuscript specifies. This does not certify the complete 1315-variable polynomial. Its 1285-gate program, 60 eliminations, final residuals, and coefficient tables are absent from the available public files. The exact finite implementation claims remain unverified.

The conclusion that the polynomial defines the integers is conditional on the named source arithmetic results and Sun's Theorem 4.1. This audit does not prove the restricted converse, the five-contact height theorem, the cyclic-group calculation, or Sun's theorem. It is not a proof that those results fail.

## Source and scope

The source is Jose Brox's `diophantine_optimization_20261106_v3.tex`, from repository revision `f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6`. The SHA-256 is `fc8bc7b8fae727e24f934ddd7de0a7cff8a005e89c3d0cac1ea14e5191b910ca`. All line numbers below refer to that frozen file, locally at `sources/diophantine_optimization_20261106_v3.tex`.

The main audit covers lines 4135-4758. It traces the necessary earlier arguments through lines 2354-3044, 3344-3405, and 3734-3891. It also checks the local three-adic calculation printed at lines 7057-7073. The subsequent ordinary-coefficient variants are not the target of this report.

`check_local.cjs` is a new independent exact-arithmetic checker. It imports no author code. Run it with `node work/josebrox-deep-audit-20261106/brox1315/check_local.cjs`. Its generated `local-checks.json` records the checks. It represents the huge fixed integer symbolically and never constructs its decimal expansion.

## Actual findings and repair status

There is no mathematical correction to apply on the evidence checked. Creating a purported repaired 1315-variable table without the original residual program would substitute an unaudited object for the claimed polynomial. No original manuscript or coefficient file was modified.

The concrete missing evidence is the complete program and certificate archive. Lines 4626-4638 and 4746-4757 make claims about that archive, rather than supplying a reproducible gate list in the manuscript. The README explicitly says that the full archive is not uploaded. The root audit also checked the public tree and releases. Until the files are supplied, an audit report must call the exact count, full expansion, coefficient maximum, and guard incidence *reported*, rather than independently replayed.

`local-proof-supplement.tex` makes two implicit calculations explicit: the derivation of the size bound from the displayed three-adic point data, and the 34-monomial increase of the translated anchor under the stated overlap information. It is supplementary proof text, not a correction of a false theorem.

## Arithmetic changes

### Precision 52 and scalar order 32

Lines 4183-4209 correctly control the entire infinite formal-logarithm tail, including coefficients whose denominators are divisible by the local prime. With `v(z)=r>=1`, the omitted term indexed by `j>=13` has valuation at least `53r` after multiplication by `z`. The factorial denominator bound is sufficient. At unramified places over primes greater than 76176, the normalized valuation is integral. Dividing by the formal logarithm gives relative precision at least 52.

The nonvanishing needed for direct logarithm quotients is also valid for the new truncation. As explained at lines 9219-9225, at the place over 2 all nonconstant coefficients have valuation 1, and `v(D)=0`. If `v(f)>=0`, the constant coefficient is uniquely least. If `v(f)<0`, the final term is uniquely least when the truncation degree is at least 2. Degree 12 meets this condition. There is no numerical approximation in this argument.

The companion 41-variable audit identified a scope clarification for the inherited reciprocal-logarithm lemma: the upstream statement names split primes, whereas the shared construction also uses inert primes. Its proof extends to unramified completions. Lines 4206-4207 already make that extension explicit for precision 52. The companion audit supplies a common all-unramified statement covering 16, 52, and 64; this changes no quartic count or bound.

From the conditional height inequalities at lines 4215-4223, a nonzero Lucas residual gives

`B^(2/13) < (7*5^(6/13)+6)*H < 21*H`.

The exact integer inequality `5^6*7^13 < 15^13` checks the last step. The manuscript also correctly warns that 14 would be too small. The anchor threshold `|a|>(21H)^(13/2)` rules out a nonzero residual.

For scalar order 32, the inherited scalar estimate becomes `h(beta)<=H*|a|^(3/4)`. The new threshold implies `|a|>(20H)^4`, since `21^13>20^8` and `H>=1`. Hence `h(beta)<|a|/20`, which is exactly the bound used in the last contradiction. The logarithmic bound and `|a|/4<|a|-3` hold with ample margin under this threshold. The checker verifies the integer comparisons in these reductions.

### The enlarged semilocal anchor

Lines 586-681 justify replacing membership of both `f_0/C` and `f_1/C` in `Z_(2) intersection Z_(3)` by the three-witness equation. The binary form `a^2+ab-b^2` has no nontrivial zero over either residue field; its valuation is twice the minimum component valuation. The quaternion proof includes the exceptional input zero, so it does not silently exclude it.

For `C=3^(2^26)`, the anchor forces both rational components of `f(S)` to have three-adic valuation at least `2^26`. The prime 3 is inert and unramified in `Q(sqrt(2))`, so this is the valuation of `f(S)` in the quadratic local field. The displayed point reduces to the nonzero two-torsion point `(sqrt(2),0)`, so a formal multiple `[a]P` has even `a`. Exact arithmetic reproduces the displayed value of `z(2P)` and shows its valuation is 1. Multiplication by a three-adic unit preserves depth and multiplication by 3 increases depth by one. Thus

`v_3(f([a]P)) = 2*(1+v_3(a/2))` for nonzero even `a`.

It follows that `a` is a nonzero multiple of `2*3^(2^25-1)`, as used at lines 4249-4257. The anchor therefore gives `log_2|a|>50331647.5`, whereas the required threshold has logarithm less than 31091008. This calculation uses the inherited assertion that every allowed point has an integer label in `ZP`; it does not establish the cyclic-group assertion itself.

### Shared point, fixed scales, and direct Lucas test

The scalar-sharing proof at lines 2946-3044 preserves the needed local conditions by continuity before imposing the final common-index congruences. The scalar witnesses are then chosen for the final index. At primes dividing the integer `r_beta`, the constant-left-path norm tree remains a unit. At primes dividing the squareclass correction but not `r_beta`, the nonconstant leaves are divisible and the tree is again a unit. This justifies the square reduced denominator and nonzero scalar guard. The quartic retains the scalar preparation coordinate, as lines 4138-4147 and 4567-4570 explicitly state. It does not depend on the later normalized scalar-pole construction.

The CRT step needs the full cross-prime order condition in Sun's Theorem 4.1. A condition only at each individual prime would be insufficient. Given the claimed theorem, lines 3007-3019 correctly give `gcd(U,V)=4`, `gcd(U,L)=64`, and `gcd(V,L)=4`; the prescribed residues are compatible. This audit treats Sun's theorem as an external dependency and does not infer it from the individual-prime condition.

The fixed scales `x_0^2` and `(1+x_1^2)^2` are positive rational squares. The first is nonzero because the abscissa of a nonidentity double is positive at both real embeddings. The rational height computation at lines 3385-3397 preserves the bound with constant `7H`.

The direct Lucas replacement at lines 4575-4590 is legitimate. The two-anchor argument already forces the approximate ratios to be integral and congruent to their integer labels using the ten formal-point tests and four cross comparisons. It does not need the deleted proxy comparisons. Polynomial congruence then transfers the order-52 condition on `F(L_2,L_3,L_4)` to the integer Lucas residual. In completeness, this new polynomial remains bounded on the same neighborhoods avoiding the old denominators. The detector order inventory is ten of order 1, two of order 16, and four of order 52.

## Divisions and the compiler

The doubling-slope equation at lines 4311-4337 cannot have a solution with ordinate zero. On the curve, such a point has abscissa 0 or a root of `x^2=D`, and the slope numerator is respectively `-D` or `2D`. Both are nonzero.

For a finite double, `x(2R)=((x(R)^2+D)/(2y(R)))^2` is a nonzero square. The real embedding makes its numerator nonzero. A point with zero ordinate has abscissa `0,d,-d`, and neither `d` nor `-d` is a square in the quadratic field because its rational norm is 7. Thus every finite double has nonzero abscissa and ordinate. The same conclusion holds for a finite difference of doubles.

These facts justify the direct quotient equations for doubling slopes, local parameters, scalar local-parameter ratios, and nonvanishing logarithm ratios. The subtraction slope still requires the explicit abscissa-difference guard. Lines 4362-4364 and 4402-4405 correctly retain it. The field quotient matrix has determinant `b_0^2-2b_1^2`, nonzero for a nonzero element of `Q(sqrt(2))`. This assertion is about the rational coefficient field; it is not asserted as a norm anisotropy statement over arbitrary scalar extensions.

The detector simplification is correct. Substituting `R=A^-5*F/(A*lambda-1)^6` into `R^(1-2m)*(A*lambda-1)^(-2m-2)` yields the weights at lines 4272-4279. The checker verifies all three exponent triples. For `W=w_0+w_1*sqrt(2)`, the inverse of `w_0` enforces nonzero trace. It also forces `W` nonzero; its norm is then nonzero over the rationals. With the retained nonzero `R`, the resulting `B` is nonzero, so an extra inverse of `B` is redundant.

The compiler transformations at lines 4473-4497 are sound as general rules. A row addition is invertible if the other row is retained. A defining equation with a nonzero rational constant coefficient gives a unique eliminated coordinate. The compiler must check the degree after substitution into every residual. Merely occurring linearly is not sufficient to preserve degree, but the manuscript explicitly states the stronger complete degree check. Squaring and summing residuals recovers their common zero set over the rationals.

These arguments validate the rules. They cannot establish that an unavailable program applied those rules correctly, preserved every guard, or eliminated only the stated coordinates.

## What can be checked about 1315 and 1272

The displayed uncompiled system has the following coordinate inventory.

| Block | Coordinates | Structural residuals |
| --- | ---: | ---: |
| Input | 1 | 0 |
| Nine halfpoints, four rational components each | 36 | 18 |
| Common slope | 1 | 0 |
| Nine coordinate poles, four witnesses each | 36 | 18 |
| Scalar pole including preparation | 5 | 2 |
| Private semilocal anchor | 3 | 1 |
| Boolean squareclass and sign choices | 8 | 8 |
| Total | 90 | 47 |

Each rational arithmetic gate adds one coordinate and one equation under the conventions at lines 4367-4405. The reported 1285 gates and 60 eliminations therefore give

`90+1285-60=1315`, and `47+1285-60=1272`.

The eleven row additions change neither count. The count is structurally consistent and includes all eight Boolean selectors. The full 1285 gate count and all sixty actual eliminations still require their missing certificates. Exact active-variable incidence also remains unverified. The claim of exactly 1314 existential witnesses follows once the full 1315 active-coordinate claim is established, because the input contributes one coordinate.

## Translated anchor

The affine map at lines 4691-4699 is invertible, with determinant `1/64`. Direct symbolic expansion verifies both the map and its inverse. Since the three affected coordinates occur only in the anchor, substitution turns the whole literal polynomial into the claimed new polynomial. This argument works over every characteristic-zero field and does not use positivity. The absence of other occurrences is a table-incidence assertion, presently taken from lines 4685-4688.

The exact local expansion produces the following facts.

| Quantity | Original anchor square | Translated anchor square |
| --- | ---: | ---: |
| Ordinary coordinate monomials | 49 | 79 |
| Monomials involving a private anchor coordinate | 27 | 64 |

Of the seven shared lower-degree monomials lost in the translation, the constant and three square monomials already occur in the remainder according to lines 4633-4636. The other three disappear. The global increase is therefore `64-27-3=34`, consistent with `28987+34=29021`. This checks the *change* in support conditional on the stated remainder overlaps; it does not check the base support 28987 or those overlaps against the missing table.

The translated anchor square has exactly one coefficient involving `s^2`, namely `64s^2` at `U^2`. Its coefficients involving `s` have absolute value at most `288s`. The fixed coefficients in this anchor square have absolute value at most 540. No monomial in that square receives two different powers of `s`. Those are exact independent checks.

Given the manuscript's unavailable-table assertions that every other coefficient is less than `2^1020` and the input fourth-power coefficient is 1, the claimed primitive height follows: `64s^2=64*3^(2^28)`. The bound `log_2 H<429496736` follows from `3^5<2^8`. The fixed integer `s` is not an existential coordinate and contributes no polynomial degree. The full coefficient bound and content-one claim are not independently certified here.

## Dependencies and remaining obligations

The arithmetic inputs are more than the bare equality of the original source's input projection with the integers. The new source uses its cyclic-group calculation, formal logarithm behavior, index-height estimate, Lucas growth and existence, pole completeness through the restricted converse, and the exact five-contact bound `H<2^4783227`. Sun's simultaneous theorem is an additional input. Lines 131-139, 2357-2364, and 9282-9358 distinguish these dependencies correctly.

An implementation audit can be completed when the following files are available: the direct source/gate program, the 1285-gate trace, eleven row additions, sixty eliminations, final residual list with a coordinate map, the direct and translated sparse tables, and the transformation certificate. The verifier should replay every operation with exact arithmetic, compare every final coefficient, check all 1315 coordinates occur, and check that each retained domain guard has a justified implementation. In particular it should confirm the three private anchor coordinates have no other incidence and verify the three reported `1-192*kappa` overlaps and constant overlap.

The manuscript identifies these relevant paths at lines 4653-4659, 4865-4881, and 9594-9620. None is present in the supplied public checkout:

- `research/phase3/quartic/build_direct_quartic.py`
- `research/phase2/quartic/verify_shared_quartic.py`
- `research/phase3/quartic/quartic-direct/polynomial.json.gz`, together with its residual list, gate trace, coordinate maps, and construction/verification reports
- `research/phase3/quartic/transform_direct_quartics.py`
- `research/phase3/quartic/verify_final_transforms_independent.py`
- `research/phase3/quartic/quartic-direct-translated/`, with the full transformed table, residual list, parent hash, and transformation certificate
- `research/phase3/compression/check_fixed_coefficient_support.py`

The published material does not identify every internal filename or the imports these programs require. Those should come from the actual archive manifest, not an invented reconstruction. The user has instructed the team to finish with public information, so the absent archive is a stated limit of this completed audit rather than a pending request.

The standalone local checks passed. No claim is made that the missing implementation or the external arithmetic inputs passed an independent audit.
