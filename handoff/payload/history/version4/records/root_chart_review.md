# Smaller half-generator root charts

Verdict: PASS for the equations and source-consumer plan in
`precision/sub5000/root-doubled-indices/CHART_APPENDIX.md`, SHA-256
`9a126a387cd376f988964e76193ac9ca712e363f501cd26f4f55c543c8e1011e`.
This review assumes the separately reviewed half-generator arithmetic
proposal. It does not accept an implementation or a whole-source saving.

For A,T,Z, the existing first-doubling square q=x^2 together with
y^2=xq-Dx is exactly the affine curve equation. The retained inverse of
2y makes y nonzero, and hence x nonzero. If a later independent rule
replaces that inverse by 2y*lambda=3q-D, the same domain follows: y=0
would give x=0,d,-d, whose right sides are -D,2D,2D. All are nonzero.
Thus the chart has precisely the required nontorsion point image. The
inverse maps f=1/x, z=-x/y and p=y/x are well-defined; those values need
not be allocated when they have no outside consumers.

S retains f and z with xf=1 and yz+x=0. Consequently its scalar and
anchor outputs are exactly the old functions. The four first-doubling
square pairs must actually be reused. Adding fresh duplicate squares
would preserve mathematics but would invalidate the stated allocation
count.

For J0 and J, the equations k=fz and f=z^2-Dk^2 require the retained
inverse of z or its conjugate. Then f=0 would imply k=0 and z=0, a
contradiction. With x=1/f, p=-1/z and y=xp, division of the second
equation by z^2 gives fp^2=1-Df^2. This is exactly the same curve and
reciprocal functions. Conversely each nontorsion point gives a unique
k=fz. There is no square-root choice or lost sign. Deleting the z
inverse would admit the all-zero solution and is not authorized by
this replacement.

I inspected the archive Field.double/Field.f/Field.z interfaces and
the actual normalized5512 root module, SHA-256
`5e96bf1b0de4e1694dcc7ff21a9a7b69b5e2cc61295c2fc2816696092c5dacde`.
The actual residuals and calls confirm the stated outside uses: only
x,y for A/T/Z, x,y,f,z for S, and only f,z for J0/J. Their outside z
inverses occur at row pairs 72/73 and 194/195; the first four root
square pairs occur at 100/101, 120/121, 140/141 and 160/161. These are
observations about the pinned old source, not fixed row numbers for a
new source. Cached affine aliases and all variable-bearing metadata
must be reconstructed in the new audit.

The exact proposed local allocation is 32 rational chart coordinates
and 20 rational chart rows, with four pre-existing square pairs and
all other doubling/inverse rows outside this count. Comparing this
number to surviving endpoint coordinates does not prove a net saving.
The producer has not yet been measured. The review therefore accepts
the allocation formula but no final variable count.

`CHART_INTERFACE.md`, SHA-256
`aa54740637c939c98fa3d99c0d444422b412aa1bdeacafee69dbe73f35886a12`,
records a concrete first-doubling hook and independent-checker duties.
It also separates live variable IDs from historical proxy-removal
metadata. No source or frozen packet was changed during this review.

The tiny independent `test_chart_appendix.py`, SHA-256
`a8b738ec0b826706c28e41363d1ac262acd127bcbd77e4a88e4305e2fefe62cd`,
passed eight nontorsion torsion-translate examples, the exact forward
and inverse maps, tangent equations and all three excluded affine
two-torsion cases. No full local source generation was performed.

The optional direct fixed-target constants are a separate compiler
idea. `FIXED_TARGET.json`, SHA-256
`03d5ffae826a5183d1c1470594c113bc62c285ca12a09702c26f1fb0e69c1409`,
contains their exact values and isolated four-row coefficient squares.
It does not certify the full polynomial coefficient bound. Direct
constants for s and t exceed the target, so only the partial x/q plan
is worth a future source measurement.
