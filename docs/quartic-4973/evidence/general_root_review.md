# Independent half-generator root review

Date: 2026-11-06. Verdict: PASS for the conservative mathematical proposal and the separate smaller-chart algebra, with the source obligations below. No source implementation or coordinate saving is accepted by this review.

Reviewed files under `precision/sub5000/root-doubled-indices/`:

| File | SHA-256 |
|---|---|
| `PROOF.md` | `ecdbfc9acd575a8ab194f8e76c356e7898544a506c705a40f169c6686c70a80e` |
| `CHART_APPENDIX.md` | `9a126a387cd376f988964e76193ac9ca712e363f501cd26f4f55c543c8e1011e` |
| `PROPOSED_CONTRACT.json` | `8be093a118346296ea4aa681617b0b47336d2e1aa7d3609ad1d546ada37621af` |
| `test_exact.py` | `e792b2f13224efc7581a8cd7b3772768d767c9c5f6f680a9f6154234b2fb69bc` |

I compared the actual group, height, anchor, scalar and common-J arguments in released `quartic_9625.tex`, SHA-256 `dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552`, including its generator proof, equation `eq:o8-indexheight`, the explicit 3-adic calculation, and the shared auxiliary point construction. I also compared the current joint chart and normalized-Lucas proof. This is an independent check of the changed interfaces; the inherited arithmetic inputs retain their existing qualifications.

## Group, local indices and exceptional branches

The displayed R lies on the current normalized curve and satisfies 2R=P*. The inherited assertions `2E(K)=Z P*` and `E(K)_tors=E[2](K)` imply that every Q has a unique integer n with 2Q=nP*, and Q=nR+tau. In particular n is nonzero exactly for nontorsion Q. This does not confuse the full group with its torsion-free subgroup.

The conservative four equations force x,f,y,z,p nonzero, y=xp and pz=-1, and give the curve equation. Their converse is unique for every nontorsion point. They exclude the identity and all three finite torsion points. All old external coordinate meanings are therefore retained.

For arbitrary source solutions, the exact relations are `2(Xi-4Qi)=(mi-4ni)P*` and `2(X0-4R)=(h-4)P*`. The retained alternate tests give their quotient valuations against `2J=jP*`. The existing O/T0 difference argument applies before doubling, including the zero-difference branch. Doubling is a local unit, so these are precisely the valuations of `(mi-4ni)/j` and `(h-4)/j`. Since the nonzero integer j is locally integral, h is congruent to 4 and mi to 4ni to the required orders. Thus h is a unit.

The primary positive-f tests still select the O formal group. The identity `[2h]Xi=[2mi]X0` is valid even when the private points have torsion components. Applying the formal logarithm gives mi/h without taking a logarithm of a nonformal generator. Reciprocal approximation then yields Ci congruent to ni with orders 12 or 40. The beta field must be `C_A-2beta`; changing the root carrier alone would be wrong.

The target points 4R and 4Qi are nonzero multiples in 2E(K). All joint-chart target denominators remain nonzero. Normalized-Lucas primary p_s/p_z zero branches retain their existing treatment: they may occur globally, but the positive-f tests exclude them at every consumed prime. Independent private conic orientations do not change these conclusions, which are local at each selected place.

The scalar identity is `[2j0]S=[2s]J0`. It gives the same s/j0 formal ratio at every relevant place, including inert odd primes. The scalar polynomial still uses beta, and all six old coefficient orders remain `(1,1,1,1,32,32)`. Replacing that polynomial by its value at 2beta would not implement this proof.

## Heights and strict inequalities

Applying the old index-height bound to 2Q=nP* and the old duplication upper bound to Q gives

```
n^2-6 <= 4h(x(Q))+log(676),
h(x(Q)) > n^2/4-4.
```

These bounds are uniform in the torsion translate. The same eight original rational coefficients of x(A),x(S),x(T),x(Z) are still the height targets. Combining their unchanged H19 estimate with this lower bound gives `n^2-6 < 7H_eff N^alpha`, with `H_eff=5H19`. Indeed `log(676)<7` and `H19*N^alpha>=1`, so `28H19*N^alpha+log(676)<35H19*N^alpha`. No new height theorem is assumed.

The full anchor still imposes integrality of both coefficients of f(S)/C at 2 and 3, with C=3^(2^25). At 3 this places S in the formal group. Doubling preserves the valuation, and the explicit calculation for 2S=sP* gives s even and `v3(s)>=2^24-1`. The 2-adic condition remains a source condition, although it is not needed for this lower bound.

The resulting `log2|s|>50331645/2` exceeds `10*2093974=20939740` and `(32/13)*2093975=5154400`. Thus the high40 and scalar32 cutoffs survive enlargement to H_eff. The scalar estimate `h(2beta)<=h(beta)+log2 < H_eff*|s|^(19/32)` follows from the unchanged estimate for beta. All uses of `h(beta')<|s|/40` and `log(40H_eff)<|s|/40` are justified.

The first contradiction uses the same 29 Lucas-bearing positions, the three indices s,t,z and `B_L=max(|s|,|t|,|z|)`. The inequality `|Delta|<5B_L^4` and the restored height format give `B_L^(1/10)<24H_eff`, contradicting the cutoff. The second uses the 21 A/T beta-bearing positions, beta'=2beta and `B_AT=max(|n|,|t|)`. Its numerator estimate and height bound give `log B_AT<31|s|/200<|s|-3`, contradicting Lucas growth. Finally, `2X^2+4` integral forces X integral by the reduced denominator argument `b^2|2`. The weakened final beta conclusion is sufficient.

## Completeness in the required order

Choose A=beta P*, and choose both scalar J0 and S together in the old subgroup by the existing scalar construction. Their new indices both double, so the scalar ratio is unchanged. Additional divisibility remains available before applying Lucas existence to the new integer s. Set T=tR and Z=zR. These nontorsion points are permitted in the enlarged carrier.

Fix these points and all eight coefficient targets before the rational37 prime pattern. Impose the normalized-Lucas finite avoidance of primes dividing s at this stage. Then choose j as the lcm of the opposite group cardinalities and set J=jR. The same-prime CRT has compatible moduli because their gcd is 4 and the selected prime divides neither group cardinality. Each resulting h is divisible by four. Hence Xi=hQi and X0=hR have the required formal reductions, and h kills every root torsion component. The additional p-power modulus accounts for all valuations of j; no cross-prime coprimality claim is made.

The existing G and normalized ratio coordinates can now be assigned. Only afterward are the private conics, norm roots and ordinary pole witnesses chosen. This preserves coefficient independence and every previously reviewed completeness approximation. No new external arithmetic input is required.

## Smaller-chart appendix

For A,T,Z the reused first-doubling q=x^2 and row `y^2=xq-Dx` give the curve equation. The retained inverse of 2y, or the exact tangent row `2y*lambda=3q-D`, excludes y=0: the latter case would give x in {0,d,-d} and a nonzero right side. It also excludes x=0. Thus every admitted point is nontorsion, and every nontorsion point has the required doubling extension. The added S equations `xf=1` and `yz+x=0` preserve exactly the scalar and anchor outputs.

For each of J0,J, the equations `k=fz` and `f=z^2-Dk^2`, together with the actually retained inverse of z, force f nonzero. Substitution of `x=1/f`, `p=-1/z`, `y=xp` gives `fp^2+Df^2=1` and the curve equation. Conversely every nontorsion point extends uniquely. This proof divides only by the explicitly nonzero z and the consequent nonzero f. It introduces no unwanted component or omitted torsion case.

The appendix's algebra therefore passes. Its claims about available q coordinates and absent external uses of deleted coordinates remain concrete source-incidence obligations. I have not accepted them merely from names or prior allocation counts.

## Verification boundary

The bounded exact fixture passed: the base duplication, 20 points covering five multiples and all four torsion translates, both proposed chart forms, the two rational cutoff comparisons and 1295 reduced input-denominator cases. No full source was generated or replayed.

A new source audit must bind the actual six root charts, retained auxiliary inverses, reused doubling squares, all outside uses of deleted coordinates, fixed R and its quadruple, each variable target 4Qi, both beta-mode expressions `C_A-2beta`, the unchanged scalar beta polynomial and six orders, full anchor, unchanged rational37 targets, and H_eff metadata. Existing square-membership rewrite rules cannot be applied to the new rows by label. Fresh lifting, reduction replay, coefficient checking and an actual endpoint measurement remain required. The 24-, 47- and 64-coordinate figures are allocation comparisons only.
