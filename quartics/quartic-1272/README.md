# The 1272-variable quartic

This package contains a complete explicit integer quartic with 1272 variables, including one input, and 48001 nonzero monomials. Its exact coefficient height is `64*3^(2^28)`. The coefficient of the input's fourth power is one, so the polynomial has degree four and primitive integer coefficients.

The polynomial is an independent reconstruction from José Brox's public formulas. It is not a recovered copy of the unavailable 1315-variable polynomial. The complete table is [polynomial.json](polynomial.json), with SHA-256

```text
02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586
```

The conclusion that this polynomial defines the integers in the rationals uses the arithmetic inputs named in the pinned manuscripts, including the restricted converse, pole completeness, the five-contact height theorem, and Sun's simultaneous prime-pattern theorem. This package checks the finite construction and provides source and domain reviews. It does not supply a Lean proof or reprove every external arithmetic theorem.

## Read the coefficient table

Set the fixed integer `S = 3^(2^27)`. An entry

```json
{"monomial": [0, 0, 1], "sPower": 2, "coefficient": "7"}
```

means `7*S^2*X_0^2*X_1`. Sum every entry to obtain the polynomial. Repeated coordinate indices denote powers. The table lists every coordinate monomial; it is not merely a circuit or a list of equations. `S` is a fixed coefficient parameter, not another variable or a quantified witness. The exact power encoding avoids writing roughly 128 million decimal digits for each largest coefficient.

This table complements the earlier ordinary-coefficient artifacts. It does not replace Version 4 or alter the existing 4973-variable package.

The top-level table is an exact-byte copy of the compiler output at [compiler/translated/polynomial.json](compiler/translated/polynomial.json). The integrity check requires both copies to have the pinned hash.

Serialization is explicit across operating systems. Generated JSON uses UTF-8 and LF line endings, except the direct and translated polynomial tables, whose published CRLF bytes are preserved on every platform. The compiler requests those line endings explicitly. The integrity and reproduction checks validate this policy in addition to comparing exact bytes; they never normalize files before a hash comparison.

## Reproduce and check

Requirements are Python 3.10 or later and Node.js 18 or later, both on `PATH`. All programs use standard libraries. No package installation, network access, Lean installation, or expansion of the giant integer is needed.

From the repository root, run:

```text
python scripts/check_quartic1272.py
```

This checks every shipped file against [MANIFEST.json](MANIFEST.json), rebuilds in a temporary directory, runs the source evaluators and independent certificate checker, and compares the rebuilt coefficient table byte for byte. It leaves the repository unchanged. To retain the rebuilt files, logs, and `REPRODUCTION.json`, supply a new empty directory outside this package:

```text
python scripts/check_quartic1272.py --out quartic1272-replay
```

The package also works outside this repository:

```text
python reproduce.py --out ../quartic1272-replay
```

For an integrity-only check, run `python integrity.py` from this directory. It verifies the complete file inventory, pinned source bytes, and the hard-coded polynomial hash. The full check is required to replay the mathematics of the finite construction; a matching hash alone is not that replay.

## What is checked

The source builder starts with 90 base coordinates and 47 structural equations and adds 1214 arithmetic coordinates with defining equations. The compiler records 32 degree-preserving eliminations, yielding 1272 active coordinates and 1229 quadratic residuals. The final polynomial is their exact sum of squares.

The independent checker imports neither the builder nor the compiler. It verifies the gate equations and dependency order, replays every elimination and normalization, validates the coordinate map, expands all residual squares, and compares all coefficients. Its fixed-integer calculations certify support, integrality, primitive content, and maximum coefficient without materializing `S`. The check includes 36 deliberately corrupted examples and a separate review probe suite.

The source review covers all 90 base coordinates, 47 structural equations, 259 named expressions, 16 field tests, and 93 explicit or derived domain conditions. Two independent evaluators compare the source expressions with the generated program. These sampled checks supplement the written source review; they do not prove the external number theory.

The exact anchor check verifies the invertible affine change and the identity `translated row = 16 * original row after substitution`. It therefore preserves the common zero set. The two differently normalized raw sums of squares are not asserted to be literally the same polynomial after substitution.

## Contents and provenance

- [builder](builder/) contains the source program, both complete raw systems, and their gate traces.
- [compiler](compiler/) contains the exact compiler, final residuals, elimination certificates, coordinate maps, direct and translated tables, and coefficient certificates.
- [checker](checker/) contains the independent verifier, mutation tests, anchor checker, and regenerated receipts.
- [source-review](source-review/), [oracle](oracle/), and [identity](identity/) contain the source inventory, domain review, independently implemented evaluators, and fixed-parameter checks.
- [sources](sources/) contains the pinned Brox and upstream manuscripts, Sun's source, and local proof supplements. [sources/SOURCES.json](sources/SOURCES.json) records their hashes.
- [evidence](evidence/) preserves the prior source audits and historical reconstruction receipts.

[PROVENANCE.json](PROVENANCE.json) records the portable path and serialization changes. The two raw systems differ from the originally reviewed files only in `source.path`; every other JSON field is identical. The arithmetic of the builder, compiler, and checker is unchanged. Code adaptations concern source and report paths and explicit line endings. Both polynomial tables are byte-identical to the original reconstruction. Historical review hashes remain historical; the package manifest and regenerated receipts bind the portable files.

The mathematics is attributed to the authors named in the pinned sources. The independent implementation and reviews were prepared by Astra agents under Elliot Glazer's direction. This package makes no claim of authorship over those source manuscripts.
