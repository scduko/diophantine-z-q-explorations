# Integration notes for new1272.tex

Insert the three bridge lemmas from `../bridge-review/arithmetic_bridges.tex` before `new1272.tex`. The new section cites `v5:scalar32-bridge`, `v5:preparation-zero-bridge`, and `v5:real-progression-bridge`. The Sun appendix supplies `thm:v5-simultaneous-primes`; its proof is not duplicated in this section.

The section presents one new polynomial, `P_1272`. The 1304-coordinate object is described only as the initial residual system, not as a fourth presented polynomial. The preceding Version 4 quartic and the original large polynomial are untouched.

The current coefficient-table path is `quartics/quartic-1272/polynomial.json`. Its required SHA-256 is `02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586`. The section avoids guessing additional final-package filenames. It describes the included certificate, coordinate map, source program, and residual table generically.

The release packager confirmed these canonical paths beneath `quartics/quartic-1272/`: `compiler/translated/compiled-ir.json`, `compiler/translated/reduction-certificate.json`, `compiler/translated/coordinate-map.json`, and `builder/build_source.cjs`. The top-level `polynomial.json` is an exact-byte alias of `compiler/translated/polynomial.json`. The portable check is `python scripts/check_quartic1272.py`.

Add the following bibliography entry, with the exact `Brox2026` key used in the section:

```tex
\bibitem{Brox2026} J. Brox,
\emph{Conditional polynomial constructions, lower bounds, and number-field
obstructions for rational Diophantine integrality}, working version 3,
6 November 2026. Public source at Git revision
\nolinkurl{f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6}.
\url{https://github.com/JoseBrox/diophantine-z-q_improvements/blob/f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6/paper/diophantine_optimization_20261106_v3.tex}.
```

The existing `voight2021` entry is cited at Proposition 14.6.7 for the quaternion quadratic-embedding criterion. Its existing bibliography text currently emphasizes Chapter 43. It may be useful to broaden that entry to identify the full book without removing the Chapter 43 information needed by earlier text.

## Arithmetic scope

The new section explicitly uses the original `hyp:o8-height`, with exponent 24 and constant `H_*<2^4783227`. It does not substitute Version 4's sharper exponent-19 result or its smaller constant. It inherits `prop:generator` through the normalized curve change, `eq:o8-indexheight`, `hyp:o8-pole`, the restricted-converse and simultaneous-realization prerequisites of that pole lemma, `lem:o8-lucas`, and `lem:quartic-reciprocal-nonzero`.

The new local logarithm lemma covers rational primes greater than 76176 at both split and inert places, and only precisions 16, 52, and 64. It closes the inherited split-prime scope explicitly without changing the earlier Version 4 statement.

The simultaneous-prime theorem is genuinely additional to the old fixed-prime pattern. Its cross-prime order gcd is used in the three simultaneous congruences for the single comparison-point index. The new section does not infer this from single-prime order information.

The new `lem:v5-two-reductions` supplies the link between the Gaussian norms and the two reduced elliptic group cardinalities. It uses the existing CM calculation in `subsec:o8-pattern-proof`, then full rational two-torsion and parity to identify the Frobenius Gaussian integer with the selected generator up to sign and conjugation. The cardinalities are used as annihilators; no claim is made that the reduced point has exactly that order.

## Checked finite statistics

- 90 initial coordinates, 47 structural residuals.
- 1214 arithmetic coordinates and defining equations.
- 32 exact eliminations; no row additions or free-coordinate omissions.
- 1272 active final coordinates, 1229 final quadratic residuals.
- 48001 coordinate monomials: 47993 with fixed integer coefficients, seven with a nonzero coefficient times the fixed integer `S`, one with coefficient `64*S^2`.
- The largest `S`-independent coefficient has bit length 5339. The largest multiplier of `S` is 768.
- The input fourth-power coefficient is 1. The maximum coefficient is at monomial `X_79^2` and equals `64*S^2`.

The manuscript uses these actual reconstruction values, not the smaller fixed-coefficient bound or linear coefficient bound of the unavailable original Brox table.

## Review status

The complete source implementation received independent semantic review and exact certificate/table verification in the reconstruction campaign. The new exposition has also been accepted by the independent bridge and oracle reviewers. No PDF build is performed in this lane; the root integration owns typesetting and layout checks.

The bridge reviewer accepted the full new section after the explicit CM and contact-denominator additions. The accepted TeX has SHA-256 `506675ede05bb3d369d9882945958c86d2d39c8fbe4d6e1e393c6a4e17f00000`. Static validation checks 82 balanced environment tokens and 31 distinct labels. Every reference resolves against the existing manuscript and bridge fragment except the expected Sun theorem supplied by its appendix. The independent oracle reviewer then accepted this same TeX hash and independently recomputed all reported coefficient statistics from the 1229 actual residuals. The separate Sun appendix and full release still have their own integration checks.
