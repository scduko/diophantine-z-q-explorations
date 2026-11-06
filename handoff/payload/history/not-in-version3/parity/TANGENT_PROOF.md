# Exact tangent compression

This is an algebraic transformation of the accepted source. It introduces no
new arithmetic input, height assumption, contact condition or source theorem.

Write K = Q(rho), rho^2 = 2, d = 3-rho, and D = d^2 = 11-6rho.
Each element of K is represented by two rational coordinates. The old
tangent subcircuit, with x,y as retained input expressions, has three field
variables S,I,L and equations

```
S = x^2,
(2y) I = 1,
L = (3S-D) I.
```

It uses six rational coordinates and six quadratic scalar equations. The
replacement retains L and uses only the two scalar equations

```
(2y) L = 3x^2-D.
```

Thus it removes the four rational coordinates of S and I and four residuals.
Every input coordinate may be an affine rational expression. The replacement
then still has degree at most two after clearing constant denominators.

## The denominator cannot vanish

The equation 3x^2 = D has no solution in K. Indeed, d is nonzero because its
field norm is 7. If such an x existed, z=x/d would satisfy 3z^2=1. Write
z=a+b rho with a,b rational. The irrational coordinate gives 6ab=0, while
the rational coordinate gives 3a^2+6b^2=1. Either a^2=1/3 or b^2=1/6.
Both are impossible: the 3-adic valuation of a rational square is even,
whereas the valuation of 1/3 and of 1/6 is -1.

Consequently the new equation itself forces y nonzero. This argument does
not assume that x,y lie on the elliptic curve. It therefore applies to the
literal rational source equations, including every exceptional input.

## Both rational maps

Old to new: forget S and I. Multiplying the old slope equation by 2y gives
the replacement equation. All other coordinates remain unchanged.

New to old: retain every existing coordinate, and define

```
S = x^2,
I = (2y)^(-1).
```

The inverse is defined by the preceding argument. For y=c+e rho it has
rational coordinates

```
I = ( c/(2(c^2-2e^2)), -e/(2(c^2-2e^2)) ).
```

The denominator is nonzero because K is a field and y is nonzero. The new
equation multiplied by I recovers the old slope equation. These maps are
inverse on the retained variables, and the deleted coordinates have unique
reconstructions. There is no branch discarded at y=0: neither system admits
that branch. No division by x, a slope coordinate, or a curve coordinate
other than the proved nonzero y occurs.

The four deleted coordinates must be used only in these six old rows. The
rule checks their complete current incidence sets. It also rejects aliased
coordinates, cyclic inputs, non-affine inputs, wrong D, duplicate row IDs,
and any source row differing from the displayed equations up to nonzero
rational scaling. The slope and all subsequent double/quadruple outputs are
preserved literally.

## Root implementation and cost

The published source applies two doublings to each of A,S,T,Z and to its
fixed base point. Each doubling currently allocates ten rational
coordinates: S, I, L, L^2, and L(x-x_double). The replacement leaves the
last three field pairs, six rational coordinates per doubling.

The eight variable-point doublings therefore offer a raw reduction of 32
variables and 32 rows. Including the two fixed-base doublings offers a raw
reduction of 40 of each. This is not a measured reduction from the already
simplified 12,504-variable endpoint; some fixed-coordinate costs may already
have disappeared there. Do not add these raw counts to unrelated estimates.

The existing outputs are x_double=L^2-2x and
y_double=L(x-x_double)-y. They are unchanged. The second doubling's x,y
are affine expressions in those retained gate outputs and the original
inputs, so the same quadratic rule applies again. The source's small
constant double/quadruple circuit stays in use; no enormous fixed rational
coordinates are inserted.

For the root's eight variable-point cases, the displayed replacement rows
have integer coefficients of magnitude at most 24. For the two fixed-base
cases with x=(57/8,-7/2), y=(-165/8,417/32), clearing denominators gives
maximum absolute coefficient 14,275. The diagnostic reports the actual
primitive-row maximum. The exporter and independent replay still require
the complete sum-of-squares polynomial to have integer coefficients,
degree four and maximum absolute coefficient below 2^80.

`tangent_rule.py` is the independent matcher/reconstruction rule.
`produce_tangent.py` uses the published construction map and root indices to
locate the ten blocks in a pre-optimization candidate. It rejects changed or
nonunique rows. Its current source pin is the released reciprocal64/beta16
entry; porting the locator to another named source requires an explicit
audit, even though the mathematical rule itself is source-independent.
`verify_tangent.py` pins the complete published checker bytes, adds one
dispatch in memory, and runs every original check and the full expansion.
Its receipt records both extension file hashes as well as the frozen core
checker hash. No shared or published file is modified.

## Root-dispatched checks

Use the published package as PACKAGE and its recreated pre-optimization
`batch` stage as PARENT. The local raw wave13 batch stage is another possible
diagnostic input. Run the small tests first, then the diagnostic, then the
producer only if all intended blocks match.

```
python parity/test_tangent.py
python parity/produce_tangent.py --package PACKAGE --parent PARENT --output tangent-diagnostic.json --diagnostic-only
python parity/produce_tangent.py --package PACKAGE --parent PARENT --output TANGENT
python parity/verify_tangent.py --package PACKAGE TANGENT
python PACKAGE/reproducibility/tools/optimize.py --parent TANGENT --output SIMPLE --max-terms 96 --rounds 8 --rational --gaussian --row-combine --row-order reverse
python parity/verify_tangent.py --package PACKAGE SIMPLE
python PACKAGE/reproducibility/tools/merge_coordinates.py --parent SIMPLE --output COORDINATES
python parity/verify_tangent.py --package PACKAGE COORDINATES
```

The wrapper must be used for every descendant certificate containing the new
rule. The unextended published checker correctly rejects its unknown rule.
No test or full computation has been run in preparing this packet.
