# Independent checker for the reconstructed quartics

For this release, use `python reproduce.py --out ../quartic1272-replay` from the package root. The commands below describe the checker inside the isolated copy. They write receipts and should not be run against the shipped package, whose bytes are pinned by its manifest.

The frozen direct and translated artifacts pass the exact algebra checks. The translated construction has 1,272 active coordinates, 1,229 quadratic residuals, 48,001 ordinary monomials, primitive integer coefficients, and exact coefficient height

\[
64S^2=64\cdot3^{2^{28}},\qquad S=3^{2^{27}}.
\]

The direct construction has the same coordinate and residual counts and 47,984 ordinary monomials. Its exact maximum coefficient is the scalar polynomial recorded in `direct-check.json`. Neither result claims to reproduce the missing 1,315-coordinate, 29,021-monomial table. They certify the supplied independent reconstruction.

## Reproduce

Requires Node.js with BigInt support and no third-party packages. From the reconstruction directory, run:

```text
node checker/run_all.cjs
```

An explicit reconstruction root can be supplied as the next argument. Run the copied checker inside that copied layout when reproducing an archive. The command reads `builder/` and `compiler/{direct,translated}/`, writes receipts and independent tables under `checker/`, checks the anchor conversion, and runs the mutation tests.

To check one stage directly:

```text
node checker/checker.cjs --input builder/raw-translated-ir.json --compiled compiler/translated/compiled-ir.json --certificate compiler/translated/reduction-certificate.json --coordinate-map compiler/translated/coordinate-map.json --quartic compiler/translated/polynomial.json --report checker/translated-check.json --emit-quartic checker/translated-quartic.json
```

`FINAL_CHECK.json` contains the source hashes of all four checker programs and the frozen hashes of each input artifact. Its component receipts are `direct-check.json`, `translated-check.json`, `ANCHOR_CHECK.json`, and `MUTATION_TESTS.json`.

## What is checked

The checker implements rational arithmetic with BigInt numerator and denominator pairs, and sparse polynomial arithmetic in the rational coordinates and a formal positive parameter S. It does not import the builder's or compiler's arithmetic code.

- Every raw residual has degree at most two in rational coordinates.
- S has the declared fixed value and is not a coordinate. Coordinate 0 remains the sole input coordinate.
- All 1,214 raw gate coordinates have exactly one recognized defining gate. Every listed dependency precedes its output. Assignment equations, rational quotients, and paired Q(sqrt(2)) quotient equations agree exactly with the residuals. Each field quotient has a unique matching component.
- The reduction certificate is bound to the raw file's SHA-256. Row additions, nonzero rational row scalings, and constant-linear elimination are replayed exactly. Every elimination's replacement and complete affected-row list are checked. Any operation that produces a residual of degree above two is rejected.
- The resulting residuals and coordinate names agree with the compiled IR. The compact coordinate map is a bijection onto consecutive coordinate IDs, preserves input 0, and can omit only genuinely unused coordinates.
- The checker expands every residual square and adds all terms. The supplied quartic table agrees exactly, including its stated overall rational multiplier and coordinate names.
- All formal nonzero coefficient polynomials remain nonzero after specialization. The exact maximum absolute coefficient is certified by leading-term domination, using S greater than 2^(2^27). No gigantic integer S is constructed.
- Integrality is checked by evaluating a common-denominator numerator modulo that denominator. The exact specialized coefficient content is determined from the gcd of the S-free coefficients and modular evaluation of the other coefficients. Formal primitivity in Z[S] is not substituted for primitivity at the fixed integer S.

The translated table's maximum is attained at the monomial with coordinate IDs `[79,79]`. Its coefficient is exactly `64*S^2`. Both specialized coefficient contents are 1.

## Anchor conversion

`check_anchor.cjs` reads both raw files and checks the actual row and coordinate IDs. It verifies the forward and inverse affine substitutions by symbolic composition. All 1,260 nonanchor rows are unchanged and omit the three private anchor coordinates.

The translated anchor row equals 16 times the old anchor row after the affine substitution. Thus their rational common-zero sets are in bijection. The translated sum of squares is not claimed to be the literal affine substitution into the old sum of squares: its anchor summand has an additional factor of 256.

## Adversarial tests and limits

All 36 deliberate corruptions are rejected. The cases include wrong gates, missing field mates, wrong field components, omitted dependencies, forward dependencies, missing gate definitions, changed fixed parameters, nonintegral coefficients, wrong hashes, bad pivot replacements, incomplete affected-row lists, degree-increasing elimination, incorrect coordinate maps, changed table names or coefficients, false height bounds, and exponent overflow.

Positive tests also distinguish formal from specialized content and verify an integer-valued rational coefficient at the fixed odd S. These tests exercise the checker; they are not proofs of the inherited Diophantine arithmetic.

Field quotients and noninverse rational quotients have source-level domain obligations. The receipts list them instead of treating metadata labels as proofs. Source formula coverage, local arithmetic, Sun's simultaneous prime theorem, and the source restricted converse belong to the separate semantic review. Numerical source-oracle samples are supplementary to that review.

All checker code and final receipts are frozen after the successful run recorded in `FINAL_CHECK.json`.
