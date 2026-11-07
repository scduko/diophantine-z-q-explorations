# Integrated three-detector construction

Two source variants have been built and checked.

| Variant | Raw coordinates | After upstream compiler | After certified eliminations | Final residuals |
|---|---:|---:|---:|---:|
| Three detectors, original logarithms | 577 | 561 | 554 | 523 |
| Three detectors, asymmetric depth | 540 | 532 | 523 | 492 |

All counts include the rational input. All residuals are quadratic; their sum of squares has degree four. The first variant reduces833 to554 variables. The second reduces833 to523 and also uses the additional asymmetric-depth completeness argument.

The fixed coefficient parameter S remains formal in these counts and is not a coordinate. The established ordinary-coefficient constant-chain construction adds17 coordinates when specializing at S=3^(2^26), giving571 and540 respectively, subject to the accompanying scalar/anchor proof. Those ordinary versions are assembled separately.

## Reproducible composition

`build_integrated.py` reads the frozen full-log source at `circuit/laurent_noy_scalar` and applies, in order:

1. `architecture/odd_chart/patch.py`: four odd-root coset charts, sixteen extra rational witnesses and sixteen quadratic residuals.
2. `patch_product_scales.py`: computes the product of the four root abscissae and retains only the three scales1, X0², (1+X1²)²; allocates only three pole-witness groups and detector blocks.
3. `architecture/integer_encoding/odd_scalar_patch.py`: replaces beta by2X²+3 and uses S-P* only in the scalar preparation and anchor.

The root point S itself remains the point of odd integer label a. The shifted scalar point has label a-1. All direct comparisons and height products use the unshifted root.

Run `python build_integrated.py` for the first source, or `python build_integrated.py asymmetric` for the second. The latter starts from `architecture/logarithms/candidate`; the same three patches are then applied. The output directories are `integrated/` and `integrated_asymmetric/`.

## Verification and proof boundaries

The independent upstream checker passed the full source/compiler/polynomial checks for both precursors:495 gates for the561-coordinate version,458 gates for the532-coordinate version. Reports are in each source directory as `independent-check.json`.

The inherited exact elimination machinery produces `eliminated/` and `eliminated_asymmetric/`, with seven and nine eliminations respectively. Their `verification.json` files record exact polynomial identities, reversible substitutions and degree checks. The additional arithmetic reasoning is separate from these finite checks:

* `PRODUCT_HEIGHT.md` proves the explicit inequality h(x(Qi))<=h(product x(Qj))+3log7 for odd labels, including bad places. The independent stronger proof in `architecture/scales/odd_product_height.tex` gives exact height additivity on this particular orbit. Either estimate preserves the existing7H constant.
* `architecture/odd_chart/` proves that the new root witnesses characterize exactly P*+4E(K).
* `architecture/integer_encoding/ODD_ROOT_COMPLETENESS.md` proves compatibility with the shifted scalar anchor, odd Pell witnesses and beta=2X²+3.
* The optional version additionally uses `architecture/logarithms/PROOF.md`, including the prime-pattern thinning and p^19 CRT refinement.

These are arithmetic refinements of the inherited construction. Their correctness does not follow merely from the algebra checker's success. All original arithmetic assumptions and source qualifications remain inherited.
