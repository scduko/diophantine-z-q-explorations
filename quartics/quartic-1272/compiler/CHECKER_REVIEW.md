# Review of the independent algebra checker

I reviewed `checker/checker.cjs`, its mutation tests, and the reported test outcomes. I wrote the Python compiler being checked, so this is a review of the independently implemented verifier, not a third independent reconstruction or an independent proof of every arithmetic input.

The checker imports no compiler or builder implementation. It uses its own normalized rational arithmetic, sparse polynomial operations, substitution, sum-of-squares expansion, and fixed-parameter coefficient analysis. I found no defect affecting the frozen baseline construction.

## Defects found during review

The initial verifier checked quartic coordinate ids and input kinds but did not compare their names against the coordinate map. Changing only a table coordinate name could pass. I reported this metadata gap; the checker now compares the names too. My local probe confirms that the renamed-coordinate mutation is rejected.

I also found a generic exactness gap outside the baseline's small parameter exponents. The parser required safe-integer exponents, but multiplication did not check that their sum remained a safe integer. Multiplying `S^9007199254740991` by `S^2` produced exponent `9007199254740992`, rather than the exact exponent `9007199254740993`. I reported a fail-closed check in the common polynomial insertion method. The checker now applies that check, and my overflow probe confirms rejection. The baseline uses exponents at most four and was unaffected.

The final reviewed checker SHA-256 is `50f9924557f0594a0ddb2664260d2e382d80762a0d607d87203fb7ddfb4e1cb1`. Both reported defects are repaired in that version. There is no unresolved finding affecting the baseline.

## Accepted reasoning

For every raw coordinate marked as a gate, the checker requires a recognized defining equation. It recomputes the equation from the operation's expressions, verifies the exact dependency set, and requires every dependency to precede the output id. For paired field quotients it requires a unique complementary component with matching numerator, denominator, and output pair. These checks establish the recorded polynomial identities and their dependency order.

The fixed parameter is bound explicitly in both the raw and compiled IR to `S = 3^(2^27)`, with `coordinate: false`. The sparse table must declare the same fixed parameter. Coefficient degree is therefore separate from coordinate degree.

The elimination replay checks a nonzero rational constant pivot coefficient, removes that term, and rejects any remaining occurrence of the eliminated coordinate in the pivot. It recomputes the replacement exactly, checks the complete affected-row list, substitutes into every other row, and rejects any residual of coordinate degree greater than two. Input coordinate zero cannot be eliminated. Row additions retain their source rows, and row scalings must be nonzero. The resulting residuals and coordinate ids are compared with the supplied compiled IR.

The coordinate map is injective in both directions, has contiguous output ids, preserves input id zero, and agrees with the source coordinate names. An omitted coordinate must occur in no final residual. The sum-of-squares table is independently expanded, mapped, and compared term by term, with any overall nonzero rational scalar explicit.

The fixed-parameter support and height argument is valid. For a nonzero coefficient polynomial, the checker bounds the sum of the absolute lower coefficients divided by the leading coefficient. Its numerator bit length gives an upper bound below `2^(2^27)`, while the fixed `S` is larger than that number. The leading term therefore determines the sign. Applying the same argument to differences of absolute coefficient polynomials certifies the maximum and ensures no formal support term disappears after specialization.

The integrality check uses exact modular exponentiation to test whether the specialized numerator is divisible by its common denominator. The content calculation starts with the gcd of nonzero parameter-independent coefficients and successively takes gcds with the other specialized coefficients modulo the current bound. This yields the exact content whenever a nonzero parameter-independent coefficient exists. It reports content as unverified if no such bound is available. The baseline's input fourth-power coefficient is one.

## Tests and limits

The final mutation report records 36 rejected adversarial mutations with its baseline passing. The suite covers parser failures, fixed-parameter changes, missing and corrupted gates, incorrect dependencies, invalid eliminations, table corruption, mapping failures, and incorrect specialization claims. The separate review probes in `review_checker.cjs` exercise a valid paired field quotient and rejection of a missing mate, wrong component, omitted dependency, degree-growing elimination, changed coordinate name, and parameter exponent overflow. All seven observations have the expected result. Their results are in `checker-review-probes.json` and bind the final checker hash above.

Gate-domain strings remain mathematical proof obligations. A quotient equation alone does not establish a nonzero denominator. The checker states this limitation in its report. It also does not prove that the raw system contains every required source constraint, that a base coordinate has been assigned the correct role, or that an inherited arithmetic theorem is true. Those are responsibilities of the source-system and domain audits. The checker does not automatically prove that the direct and translated raw systems are related by the asserted affine substitution.

The mutation suite accepts any thrown error as rejection. Together with a passing baseline this is useful fail-closed evidence, but it is not an exhaustive proof that each intended validation branch is correct. The direct code review and the separately recorded probes supplement those tests.

No frozen builder, compiler output, coefficient table, or certificate was changed during this review.
