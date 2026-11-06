# Exact residual compiler

For this release, use `python reproduce.py --out ../quartic1272-replay` from the package root. It copies the package and runs the low-level commands below there. Run those commands only inside that copied directory, because they write generated artifacts and would otherwise invalidate the package manifest.

`compile_ir.py` reads the builder's sparse quadratic IR. It treats `S = 3^(2^27)` as a fixed integer coefficient parameter and never constructs that integer. Its only Python dependencies are standard-library modules.

The builder owns arithmetic expression construction, common-expression reuse, and domain guards. This compiler does not treat source tags or domain-justification strings as proofs of those assertions. It checks the polynomial operations after construction.

Run from the copied package root with Python 3.10 or later:

```text
python compiler/compile_ir.py --self-test
python compiler/compile_ir.py builder/raw-ir.json compiler/direct
python compiler/compile_ir.py builder/raw-translated-ir.json compiler/translated
```

The small self-tests exercise successful quadratic elimination, rejection of degree growth, exact rational normalization, and a row addition exposing an affine elimination.

## Files

- `compiled-ir.json` contains the final quadratic residuals with stable source coordinate ids. `sourceGates` contains historical raw-gate metadata, not live final definitions.
- `reduction-certificate.json` records every accepted row addition, coordinate elimination, and nonzero rational row scaling. The certificate pins the exact raw IR bytes by SHA-256.
- `coordinate-map.json` gives a bijection from retained source ids to the contiguous final ids, preserving input id zero. A coordinate omitted as free must occur in no residual. Its recorded reconstruction value is zero.
- `polynomial.json` contains the exact sparse sum of the final residual squares, using the compact ids. `sosMultiplier` is one; the compiler applies no further polynomial normalization.
- `specialization-certificate.json` identifies the maximum absolute coefficient after fixing `S`, using an explicit leading-term dominance bound.
- `compiler-report.json` records counts, integer-coefficient checks, the gcd of parameter-independent coefficients, and artifact hashes.

## Why the transformations preserve rational solutions

For a row addition, replacing `q_i` by `q_i + c*q_j` while retaining `q_j` has inverse `q_i = (q_i + c*q_j) - c*q_j`. The compiler requires distinct rows and a nonzero rational scalar.

For an elimination, the pivot is `a*v + q`, where `a` is a nonzero rational constant and `q` does not contain `v`. Every solution has the unique value `v = -q/a`. Substitution into all other rows therefore gives a bijection between their rational solutions and those of the original system. The compiler checks that every substituted residual still has total coordinate degree at most two. Powers of `S` contribute zero to coordinate degree. Protected coordinates, including the input and the private anchor coordinates, cannot be eliminated.

The greedy candidate search is a heuristic for finding these operations. It does not affect their acceptance criteria. In particular, the compiler rejects a quadratic replacement when the variable occurs in a quadratic monomial elsewhere, and performs the exact degree check after every accepted substitution.

Clearing denominators and dividing by the gcd of scalar integer coefficients multiplies a row by a nonzero rational number. This gives a primitive row over `Z[S]` and preserves its rational zeros. It does not by itself claim that the specialized row is primitive over `Z`.

The final polynomial is the sum of the squares of the normalized rows. Over the rationals, that sum is zero exactly when every row is zero. Thus the final quartic has the same rational input projection as the raw quadratic system. This argument does not assert the corresponding sum-of-squares equivalence over arbitrary fields.

## Fixed-parameter arithmetic

Evaluation at an integer `S` is a ring homomorphism from `Z[S]` to `Z`. Every exact polynomial identity checked symbolically remains an identity at the specified `S = 3^(2^27)`. All displayed integer scalar coefficients therefore specialize to integers.

For a coefficient polynomial `a_d*S^d + ... + a_0`, its leading term determines its sign whenever `S > 1 + sum_{i<d}|a_i/a_d|`. The compiler applies this test to every coefficient and every comparison with the running maximum absolute coefficient. Each required bound is weakened to `S > 2^b`. The fixed parameter satisfies `S > 2^(2^27)`, so checking `b <= 2^27` proves all comparisons without expanding `S`.

The gcd of the coefficients of monomials whose coefficients are independent of `S` bounds the content of the specialized polynomial. A gcd of one proves specialized primitiveness. A coefficient of exactly one is an even shorter witness when present.

These files reconstruct a new explicit polynomial. Their counts and coefficients must not be described as recovered copies of the author's missing gate program or sparse table. Equivalence to the displayed source arithmetic system requires the separate builder and domain audit; the compiler alone cannot establish those inputs.
