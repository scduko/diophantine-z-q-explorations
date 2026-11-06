# Independent source review of the reconstructed quartic program

Portable release note: the hashes quoted in this historical review identify the original reviewed files. `../PROVENANCE.json` proves that the packaged raw systems change only `source.path`, while the two final polynomial tables are byte-identical. The packaged `review_verdict.json` records both original and portable hashes. Run the release checks through `python reproduce.py` from the package root.

The frozen builder implements the public rational source correctly. I found no omitted equation, incorrect test, lost domain condition, or unauthorized arithmetic modification. The program is an independent reconstruction, not a recovery of the unpublished author's gate ordering or coefficient table. Its raw count is 1304 coordinates and 1261 equations, including 1214 arithmetic gate coordinates and their equations. A separate compiler may reduce these counts while preserving the rational projection.

This conclusion concerns the algebraic source and the stated domain proofs. Identifying its rational input projection with the integers still depends on the arithmetic inputs named in the manuscript, including the five-contact height theorem, pole completeness and its restricted-converse input, and Sun's simultaneous prime-pattern theorem. This review does not certify those inputs anew.

The exact reviewed files are `../builder/build_source.cjs`, `../builder/raw-ir.json`, and `../builder/raw-translated-ir.json`. The frozen raw IR has SHA-256 `d71ded4f434476cdc4bdd1ac309a19f57cb706ed3e714439c6ed32fd1f0b1731`; the translated IR has SHA-256 `301e3d110d5618ecd172ca0eca45f71058d9177348c379256819f69bd89b3425`. The source is Brox v3 at commit `f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6`, with source hash recorded in `source_inventory.json`.

`build_inventory.py` generates `source_inventory.json`. It independently lists all 90 initial rational coordinates, 47 structural equations, 259 named source expressions, 16 field tests, the six ordered scalar tests, and 93 explicit or derived nonzero conditions. The prefix expression format includes complete definitions of field arithmetic, point doubling, point subtraction, the logarithms, detector products, scalar norm tree, both kinds of poles, and the anchor. It gives source lines for each formula. Its coordinate order is a semantic inventory, not a claim about the unpublished original order.

The 90 initial coordinates are one input, 36 halfpoint coordinates for nine points over `Q(sqrt(2))`, one common slope, 36 coordinate-pole witnesses, five scalar-pole and preparation witnesses, three private anchor witnesses, and eight Boolean correction witnesses. The 47 structural equations are 18 halfpoint curve components, 18 coordinate-pole equations, two scalar-pole equations, eight Boolean equations, and one anchor equation. There is no approximate square root of two, Lucas proxy, normalized scalar contact parameter, finite-algebra witness, or conic-chart selector in this quartic source.

| Builder lines | Source block | Review result |
|---|---|---|
| 34–42 | Homogeneous quadratic reuse | Correct. If a quadratic expression is `c*h+l`, where `h` is a normalized homogeneous quadratic and `l` is affine, the code stores one coordinate for `h` and returns `c*v+l`. Reusing the same normalized `h` preserves its exact value. This is stronger reuse than simple identical-expression matching and can explain a count different from the unpublished implementation. |
| 44–69 | Rational and quadratic-field quotients | Correct. Rational inverses enforce a nonzero denominator. Field inverses impose both component equations. Direct quotients are used only in the domain cases proved below. Constant field inverses use the correct norm formula. |
| 71–80 | Initial variables | Correct 90-coordinate inventory. All nine point occurrences use four unrestricted rational halfpoint components. The three anchor coordinates are private. The scalar correction is precisely the original eight-bit, 256-choice correction. |
| 81–96 | Curve equations and doublings | Correct. Both components of `b^2=a^3-Da` are imposed, with `D=11-6sqrt(2)`. The slope is `(3a^2-D)/(2b)`, and the standard doubled coordinates follow. Both later doublings for each fourth multiple are valid. The fixed fourth multiple of `P` is computed as constants. |
| 98–101 | Five subtractions | Correct subtraction sign. For `U-Q`, the slope is `(y(U)+y(Q))/(x(U)-x(Q))`. The explicit inverse of the abscissa difference is retained. The formulas `x'=m^2-x(U)-x(Q)` and `y'=m(x(U)-x')-y(U)` are correct. |
| 103–113 | Parameters and logarithms | Correct. There are eight order-52 logarithms and two order-16 logarithms. The coefficient recurrence is exact. The block evaluation gives `G_12` with block length three and `G_3` with block length four. The alternate ratio is conjugated after division. |
| 115–122 | Direct Lucas test and shared coefficients | Correct. The direct polynomial is evaluated using `A=U(U-2)`, `B=VW`, and `C=(U-2)W`, then `V^2-AB+C^2-1`. The 16 tests have counts 10, 2, and 4 at orders 1, 16, and 52. The elementary-symmetric recurrence is exactly multiplication by each factor `1+T*D_j^2`; no test is omitted or counted twice. |
| 124–146 | Scales, weights, detector traces, coordinate poles | Correct. The scales are `1`, then `x0^2` and `(1+x1^2)^2` for each root point. With `e=(A*delta)^5/F`, the identities `R=1/(e*delta)`, `q1=e/delta^3`, `q16=q1*e^30`, and `q52=q1*e^102` reproduce the source weights exactly. The trace formula produces `b=R*norm(W)^2/(4*w0^2)`. Both pole equations and `h=e_pole*(17b-b^2)` are correct. |
| 147–157 | Scalar block | Correct original scalar contact polynomial, Boolean correction, order list, tree order, and preparation formula. The strict source guard `b!=0` is retained by an inverse. No scalar normalization from the 41-variable construction has been imported. |
| 159–160 | Semilocal anchor | Correct physical source anchor, with `A=f0^2+f0*f1-f1^2` and `kappa=S^2=3^(2^28)`. |
| 167–172 | Private affine anchor change | Correct. The replacement is 16 times the raw anchor after the invertible displayed affine substitution. This gives the same common zero set and preserves the rational input projection. |

The scalar tree order deserves an explicit check because a generic balanced-tree implementation need not reproduce it. Upstream 8082–8090 first pairs the constant one with the first order-one test, then groups the remaining tests by order. With `X1=f(H)_0`, `X2=f(H)_1`, `X3=f(S)_0`, `X4=f(S)_1`, `X5=(z(S)/z(H))_0`, and `X6=(z(S)/z(H))_1`, define `li=Xi/r^mi` with orders `1,1,1,1,32,32`. Then

```
n0 = N_r(1,l1)
n1 = N_r(l2,l3)
n3 = N_r(l5,l6)
W  = N_r(N_r(n0,n1), N_r(l4,n3))
N_r(a,b) = a^2+r*b^2
```

The builder uses exactly this tree. There is no padding leaf.

The domain review is part of the algebraic conclusion. It cannot be replaced by coefficient expansion alone.

- A halfpoint ordinate cannot vanish in a solution of the curve and doubling-slope equations. If `b=0`, then `a=0` or `a^2=D`, while the slope numerator is respectively `-D` or `2D`. Both are nonzero. This justifies the direct slope quotient.
- Every represented point and finite difference lies in `2E(Q(sqrt(2)))`. Its abscissa is a nonzero square because the two real embeddings make the doubling numerator positive. Its ordinate is nonzero because `0,d,-d` cannot be the abscissa of such a finite double; the latter two have nonsquare rational norm seven. This justifies the direct `z=-x/y` quotients.
- Every logarithm denominator is nonzero by the source's global nonvanishing argument for `G_J`, with `J=3` or `12`. The scalar denominator `z(H)` is nonzero by the preceding point argument.
- The five subtraction denominators are explicitly inverted. They cannot be omitted: equal abscissas can make an unguarded slope equation admit spurious values.
- Every detector explicitly inverts its five-contact product `F`, its `delta=A*lambda-1`, and the rational component `w0` of `W`. It also inverts the weight `e`; this adds no restriction because `A`, `delta`, and `F` are already nonzero. Over the quadratic field, `w0!=0` implies `norm(W)!=0`, hence a nonzero trace. Thus no separate inverse of the pole input `b` is required for coordinate detectors.
- The scalar contact polynomial is inverted, and the scalar pole input `b=c*r*W^2` is explicitly inverted. The latter is a guard in the strict shared source. It was not silently removed using the weaker, arithmetic-only unguarded norm argument.
- The preparation equation itself forces `1+b*t^2!=0`: otherwise `b*t^2=-1`, so `b!=0`, while the right side of `U(1+b*t^2)=b(1-b*t^2)` is `2b!=0`. A separate inverse coordinate is redundant here.
- There are no extra nonzero requirements on the pole witnesses `e,s,p,q,h` or the preparation values `t,U`, and no nonzero requirement on an individual rational component of a halfpoint. These exclusions would be unauthorized.

The private affine change requires a normalization qualification. The published later anchor has the form `-3*A_num^2+16u^2+96v^2-32w^2+32*kappa`, where the arithmetic representation has `A_num=4*A_physical`. This reconstruction starts from the physical source anchor. Its translated residual is therefore

```
-48*A_physical^2 + U^2-6UV+6UW+15V^2-18VW+7W^2+8*S*U.
```

It equals 16 times the original raw residual after substitution. Consequently the new system has the same rational projection. Before any primitive row normalization, one must not claim that the entire new sum of squares literally equals the old sum of squares composed with the affine map. That stronger polynomial identity depends on matching the residual normalization.

`check_builder_semantics.py` provides independent supplementary evidence. It evaluates the IR using only standard-library rational parsing and modular arithmetic, then separately evaluates the public source formulas. In particular, the second evaluation computes each detector as a direct product of all 16 factors instead of reusing the builder's symmetric-coefficient program. For each of nine samples over three prime fields it verifies 168 named semantic values, all 1214 gate equations, all 47 structural equations, and the translated anchor. Every check passes. These samples do not prove rational identities; the code and mathematical review above justify the identities and domain implications. The results and exact artifact hashes are in `builder_semantic_checks.json`.

The original gate program is underdetermined by the public description. The manuscript does not list the eleven row additions, sixty eliminated coordinates, every reuse decision, or the affine representation chosen at each gate. Therefore different faithful programs can have different counts and coefficient tables. This reconstruction contains all source equations and guards and uses more aggressive valid quadratic reuse. Its smaller raw count is not evidence that an equation was omitted, and it does not authenticate the reported unpublished 1315-variable table.

No builder file was edited during this review. I suggested only a correction to the preparation-domain source citation and additional precision references in the metadata. The lead builder made those metadata changes, froze the files, and the independent checks were rerun against the final hashes above. Compiler elimination and coefficient-table verification remain the responsibility of the separate independent compiler review.
