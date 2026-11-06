# Projection argument for the reconstructed system

The system in `raw-ir.json` is a new compilation of the displayed Brox source. The argument below concerns its rational solutions. It does not assert that its residuals match an unavailable author table.

Every quadratic-assignment gate has one equation `v=q`, where `q` is a quadratic polynomial in earlier coordinates. The compiler writes a desired quadratic expression as `c*q+l`, where `c` is a nonzero rational scalar, `l` is affine, and the normalized homogeneous quadratic part `q` is either already assigned or receives this gate. Substitution and reinsertion are inverse operations on rational solutions. Reusing a gate for the identical normalized polynomial imposes no extra condition.

A rational quotient gate is `b*v=a`. Its value is unique when `b` is nonzero. An inverse gate sets `a=1` and thereby enforces nonzero `b`. A field quotient has the two equations for `(b0+b1*sqrt(2))*(z0+z1*sqrt(2))=a0+a1*sqrt(2)`. For rational coordinates its matrix determinant is `b0^2-2*b1^2`, nonzero exactly when the field denominator is nonzero. A field inverse has numerator one and enforces that domain. Paired field quotient outputs form one simultaneous step; the two component equations should not be mistaken for successive scalar divisions.

The non-inverse divisions have the required domains for the following reasons.

- Each affine halfpoint satisfies the curve equation. Its doubling-slope equation rules out zero ordinate, since the numerator would be `-D` or `2D`. A finite double has nonzero abscissa and ordinate on this curve, by the real-place and norm argument at Brox lines 4311-4337. This justifies subsequent doubling slopes and the local-parameter quotients.
- Every subtraction retains an explicit inverse of the abscissa difference. It therefore gives a finite difference of points in `2E(K)`, with the same nonvanishing coordinates. Its slope is `(y(U)+y(Q))/(x(U)-x(Q))`, the slope for subtracting `Q` from `U`.
- The reciprocal logarithm denominators are nonzero globally for truncation degrees 3 and 12 by the source's two-adic argument. The source pole and formal logarithm hypotheses justify the arithmetic use of those ratios.
- The scalar preparation equation is `(1+b*t^2)*U=b*(1-b*t^2)`. If its denominator vanished, the right side would be `2b`, and `b*t^2=-1` would force `b!=0`. This is impossible over the rationals. A separate inverse of that denominator is unnecessary. The explicit source guard `b!=0` is retained independently.

The weight factorization introduces inverses of `F`, `delta`, and `e=(A*delta)^5/F`. On the original source domain, the fixed scale `A` is nonzero, the five-contact guard gives `F!=0`, and the extra contact guard gives `delta!=0`. Therefore `e!=0`; its inverse excludes no source solution. Conversely the equations themselves enforce `F!=0`, `delta!=0`, and `e!=0`, so the factorization yields the original weights and `R` exactly. No numerical exponentiation or approximation occurs.

For each detector, the symmetric-coefficient recurrence computes exactly the product of its prescribed factors. The three polynomial evaluations thus give the source `W`. Inverting its rational component `w0` enforces nonzero trace. Over `Q(sqrt(2))`, this also makes `W` and its norm nonzero. The formula `B=R*(Norm(W)/(2*w0))^2` is precisely the reciprocal-trace formula. The preparation-zero pole equations then match the source.

The scalar block uses the stated integer correction choices, the exact seven-leaf tree, and order 32 for its last two leaves. Its pole keeps the original preparation coordinate. Each Boolean satisfies `epsilon^2-epsilon=0`, so the product ranges over exactly the signed squarefree corrections in the source.

All 47 nongate residuals are the original nine pairs of curve equations, nine pairs of coordinate-pole equations, the scalar pair, the eight Boolean equations, and the semilocal anchor. Thus, with all gate equations, their rational input projection agrees with the selected shared-point source, subject to the source equivalence proof for the stated precision and direct Lucas changes.

The translated file changes only the anchor and renames its three private coordinates. Its row is sixteen times the old row after the specified invertible affine substitution. The multiplier sixteen is nonzero and all three coordinates occur nowhere else. Hence the two rational input projections agree.

Finally, clearing rational denominators of each row and dividing by its nonzero integer content preserves its rational zero set. The sum of the squares of the resulting integer rows vanishes over the rationals exactly when every row vanishes. It is a polynomial of degree at most four. In the raw system the input occurs only in its square-definition row, which is `v-X^2=0` up to sign. This row gives a nonzero fourth-degree term, so the sum of squares has degree four. The fixed parameter `S=3^(2^27)` is an integer coefficient, not a quantified variable.

The resulting definition of the integers remains conditional on the same cyclic-group, pole-completeness, height, Lucas, and simultaneous-prime inputs as the public Brox source. The reconstruction makes the finite polynomial compilation available for verification; it does not prove those external arithmetic results.

## Named-value convention for the alternate logarithm ratios

The IR aliases `LP1` through `LP4` name the un-conjugated field quotient `ell(V_i)/ell(V_0)`, which is the output of each paired quotient gate. The JavaScript `LP[i]` value then applies conjugation before forming the source cross test. Thus the manuscript's alternate ratio is `(values[LPi.0], -values[LPi.1])`. The stored `test10` through `test13` aliases already include that conjugation. This is an alias convention, not a different equation.
