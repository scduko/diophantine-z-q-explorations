# Independent count and optimization analysis

The reconstruction has 1,272 active coordinates and 1,229 quadratic residuals. It reaches the requested bound of at most 1,315 coordinates, subject to the separate source and transformation checks. These counts describe the reconstructed program. They do not recover Brox's missing original coefficient table.

The analysis here checks counts, arithmetic exponent identities, and the limits of further constant row combinations. It does not certify the external arithmetic theorems or replace the source review.

## Count comparison

The displayed source has 90 base coordinates and 47 structural residuals. Each arithmetic gate adds one coordinate and one residual. A coordinate elimination removes one of each. Constant row additions change neither number. Consequently the coordinate count minus the residual count stays equal to 43.

| Quantity | Brox's reported program | Reconstructed program |
| --- | ---: | ---: |
| Base coordinates | 90 | 90 |
| Structural residuals | 47 | 47 |
| Arithmetic gates | 1,285 | 1,214 |
| Coordinates before elimination | 1,375 | 1,304 |
| Residuals before elimination | 1,332 | 1,261 |
| Constant row additions | 11 | 0 |
| Coordinate eliminations | 60 | 32 |
| Final active coordinates | 1,315 | 1,272 |
| Final residuals | 1,272 | 1,229 |

The reconstructed program starts with 71 fewer gates and removes 28 fewer coordinates, giving a net saving of 43 coordinates. Gate counts depend on the arithmetic representation. A fused quadratic assignment can replace several multiplication gates, and homogeneous quadratic common subexpressions can be shared before the elimination stage. The original counts therefore do not determine an original gate list or its eleven row additions.

The reconstruction's gate census is independently reconciled as follows.

| Block | Gates |
| --- | ---: |
| Nine point modules | 72 |
| Fourfold root points | 64 |
| Five differences | 40 |
| Parameters and logarithms | 184 |
| Direct tests and shared symmetric coefficients | 125 |
| Fixed height scales | 12 |
| Detector with constant scale | 71 |
| Eight other detectors | 592 |
| Scalar block | 53 |
| Anchor | 1 |
| Total | 1,214 |

`verify_optimization.py` checks unique gate-coordinate and gate-row incidence, the 90 and 47 nongate inventories, the elimination counts, and occurrence of every surviving coordinate. It records the exact input hashes in `optimization-check.json`.

## Shared detector powers

Write `delta = A*lambda - 1`, `F = F5(A*lambda)`, and

```
e = (A*delta)^5/F
R = 1/(e*delta)
q1 = e/delta^3
q16 = q1*e^30
q52 = q1*e^102.
```

The exponent triples in `A, delta, F` are respectively

```
R   : (-5,  -6,    1)
q1  : ( 5,   2,   -1)
q16 : (155, 152,  -31)
q52 : (515, 512, -103).
```

They agree exactly with the displayed source formulas. The reconstruction retains inverses enforcing `F != 0`, `delta != 0`, and `e != 0`. This factorization removes no denominator condition.

Starting from `e`, the chain

```
2, 3, 6, 12, 24, 48, 96, 30 = 24+6, 102 = 96+6
```

uses nine multiplication gates. Multiplying the last two powers by `q1` gives the other two weights. The count is an upper bound, not a claim of optimality. For the scalar block, one inverse and five squarings supply `r^-1` through `r^-32`.

## Constant row combinations

`find_affine_dependencies.py` performs sparse Gaussian elimination with exact rational coefficients on the quadratic parts. On the raw system it finds four affine combinations, each involving three rows. They connect a root-point square to the two component squares used in the height scales. This is a concrete example of why pairwise proportional-row cancellation does not find every affine relation.

After the compiler's 32 substitutions, all 1,229 quadratic parts are linearly independent over the rationals. The exact rational search reaches this result without hitting its combination or fill limits.

`verify_optimization.py` checks the result a second way, using a separate elimination implementation modulo the prime 1,000,000,007. It verifies primality, checks that all 6,825 rational coefficient denominators are nonzero modulo that prime, and obtains rank 1,229. No quadratic coefficient contains the fixed parameter `S`. A nonzero full-row minor modulo this prime proves full row rank over the rationals for the actual quadratic coefficient matrix.

It follows that no nonzero rational constant combination of these final residuals is affine. This excludes further affine substitutions exposed solely by invertible constant row operations. It does not prove global minimality, and it does not exclude nonlinear identities, new arithmetic representations, or other changes of coordinates.

## Two optional scalar savings

These changes are not applied to the checked baseline.

If `l = t/r`, then `r*l^2 = t*l`. The inverse of `r` is already retained. Therefore the first scalar norm can be evaluated as

```
N_r(1,l1) = 1 + t1*l1,
```

and the next equal-order pair can be evaluated as

```
N_r(l2,l3) = l2^2 + t3*l3.
```

Each right-hand side is quadratic in existing affine coordinates and needs one assignment. The current evaluation separately assigns the square of the right leaf and then the norm. Replacing those two norm evaluations would save one gate apiece while preserving their exact rational values. A revised program and replayed certificates would be required before advertising any smaller final count.

## Reproduction

Run these scripts with a working Python interpreter from the repository root:

```
python optimization/verify_optimization.py
python optimization/find_affine_dependencies.py builder/raw-ir.json optimization/affine-dependencies-raw.json
python optimization/find_affine_dependencies.py compiler/direct/compiled-ir.json optimization/affine-dependencies-compiled.json
```

The scripts import neither the source builder nor the residual compiler. They never construct the decimal expansion of `S = 3^(2^27)`.
