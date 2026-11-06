# Independent quadratic source reconstruction

For this release, run `python reproduce.py --out ../quartic1272-replay` from the package root. The low-level command below is intended for the isolated copy, where it may write regenerated files without changing the shipped package manifest.

`build_source.cjs` reconstructs the complete displayed rational arithmetic system in the public Brox v3 manuscript. It imports no unpublished gate program or table. Run it with Node.js:

```text
node builder/build_source.cjs
```

The current raw system has 90 base coordinates, 1214 arithmetic coordinates, 47 structural residuals, and 1214 defining residuals. This gives 1304 total coordinates and 1261 quadratic residuals before elimination. Independent semantic and algebraic checks are handled by the adjacent review, oracle, checker, and compiler directories. The existence of these files alone is not a statement that those checks passed.

`raw-ir.json` uses the original physical anchor. `raw-translated-ir.json` uses an equivalent affine translation of its three private witnesses. `census.json` records the count by block. Both IR files contain every coordinate, gate, residual, named intermediate value, and denominator guard. Coefficients are exact rational strings. A term stores a sorted coordinate list, an exponent of the fixed symbol `S`, and its rational coefficient. The symbol means `3^(2^27)` and is never counted as a coordinate.

The base-coordinate order is the input, nine affine halfpoints with four rational components each, the common slope, four witnesses for each of nine coordinate poles, five scalar-pole witnesses, three anchor witnesses, and eight Boolean correction witnesses. The initial allocation has exactly 90 coordinates. Curve equations contribute 18 structural residuals, coordinate poles 18, the scalar pole two, the anchor one, and the Boolean choices eight.

The arithmetic compiler keeps affine expressions without assigning additional coordinates. To assign a quadratic expression, it separates its affine part, normalizes the remaining homogeneous quadratic part by a nonzero rational scalar, and reuses a previously assigned identical quadratic part when available. This is an exact change of representation. Each new homogeneous quadratic value has a defining equation. Divisions use explicit scalar or paired field quotient equations, with the domain justification recorded in the gate. Field arithmetic uses the basis `1,sqrt(2)`.

The following source changes distinguish the selected system from the earlier proxy source:

| Operation | Frozen Brox source lines |
| --- | --- |
| Basic point, detector, and scalar equations | 2366-2489 |
| Shared scalar-height point | 2946-3044 |
| Fixed nonzero height scales | 3352-3405 |
| Precision 52 and scalar order 32 | 4160-4306 |
| Direct field quotients and their domains | 4311-4405 |
| Shared polynomial and symmetric-product evaluations | 4407-4447 |
| Eight Boolean scalar corrections | 4458-4469 |
| Direct Lucas test | 4575-4605 |
| Private-anchor translation | 4674-4736 |

The scalar norm-tree topology is the one specified by the frozen upstream manuscript at lines 8082-8090. With normalized leaves `x1,...,x6` in source order, the tree is

```text
n0 = N_r(1,x1)
n1 = N_r(x2,x3)
n3 = N_r(x5,x6)
W  = N_r(N_r(n0,n1), N_r(x4,n3))
```

The detector weights use an exact algebraic factorization. Put `delta=A*lambda-1`, `F=F5(A*lambda)`, and `e=(A*delta)^5/F`. Then

```text
R   = 1/(e*delta)
q1  = e/delta^3
q16 = q1*e^30
q52 = q1*e^102
```

These are respectively `A^5*delta^2/F`, `A^155*delta^152/F^31`, and `A^515*delta^512/F^103`, the source formulas. The power chain computes `e^2,e^3,e^6,e^12,e^24,e^48,e^96`, followed by the needed products. Inverses of `F`, `delta`, and `e` explicitly enforce the domains. The fixed height scales are nonzero on the point domain, so these equations preserve the source rational solutions.

The scalar block retains its preparation coordinate and the explicit inverse of its nonzero pole argument. The preparation denominator does not have a separate inverse because its quotient equation forces it nonzero: if `1+b*t^2=0`, its other side is `2b`, inconsistent with `b*t^2=-1` in characteristic zero. The subtraction slopes retain explicit paired inverses of the abscissa differences.

For the anchor, the named value `anchor.physicalA` is exactly `T=f0^2+f0*f1-f1^2`. The original residual is

```text
u^2+6v^2-2w^2-3T^2+2S^2.
```

The translated residual is

```text
-48T^2+U^2-6UV+6UW+15V^2-18VW+7W^2+8S*U.
```

It equals sixteen times the old residual after the specified invertible affine change. Its different scaling is recorded explicitly. We do not identify `T` with the manuscript's later normalized table coordinate `A`, which was four times the physical value.

The generated source system is a complete independently specified object. Its count and eventual coefficient table must be distinguished from the absent original 1315-coordinate table. Its arithmetic interpretation remains conditional on the same named external source results and Sun's simultaneous theorem.
