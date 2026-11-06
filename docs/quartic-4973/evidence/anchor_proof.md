# Four-witness homogeneous anchor

This proposal replaces only `q_anchor` in the current three-mode minimal-Jacobi source. Let `C=3^(2^25)` be its existing shared nonzero anchor constant. Let `f0,f1` be the two rational input coefficients of `f(S)`. The old anchor requires both `f0/C` and `f1/C` to belong to `R=Z_(2) intersect Z_(3)`. The replacement has four private rational variables and two integer quadratic equations. All coordinates and predicates outside this module remain unchanged.

## Published trace facts

Use the quaternion algebra with `i^2=2`, `j^2=3`, `ij=-ji`. Its reduced norm is `x0^2-2u^2-3v^2+6w^2` and its reduced trace is `2x0`. Consequently its rational norm-one trace set is

```text
S = {h in Q : exists u,v,w in Q,
                 h^2-8u^2-12v^2+24w^2=4}.
```

The source is Jochen Koenigsmann, *Defining Z in Q*, Annals of Mathematics 183 (2016), pp. 73-93, [publisher PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v183-n1-p02-p.pdf). Definition 4 is on printed p. 75. Observation 5 and the Hilbert-symbol computation give ramification exactly at 2 and 3. On printed p. 77, the proof of Proposition 6 supplies:

* Fact (b): at a ramified finite prime, `S(Q_p)` is contained in `Z_p` and contains every integral trace whose residue belongs to `U_p`.
* The same page gives `U_2={1}` and `U_3={0}`.
* Fact (e): the rational trace set is the intersection of the local trace conditions at ramified places.

Facts (a) and (c) show no additional restriction at the split finite places or the real place. Both quaternion parameters are positive. These are additional explicit uses of the published trace facts; the old bare equality `T=S+S=R` alone does not prove the new assertion. The local square constructions below are proved here.

The archived publisher PDF is `work/private-15671-20261105/anchor/primary/koenigsmann-annals-2016.pdf`, SHA256 `f26c2e155d025978045a0c68073505631677624ef4d6f9b461640c6fbe1d3c93`.

## Exact trace criterion for two inputs

For every pair `a,b in Q`, set `n=a^2+b^2` and `h=9+3n`. Then

```text
a,b in R  if and only if  h in S.
```

First suppose `h in S`. Fact (b) makes `h` integral at 2 and 3. We show that neither input has negative valuation at either prime. Use valuation infinity for zero.

At 3, if at least one input is nonzero, let `m=min(v_3(a),v_3(b))`. If their valuations differ, the summands in `n` have different valuations, so `v_3(n)=2m`. If their valuations agree, divide both inputs by `3^m`; both resulting units have square residue 1, whose sum is 2 modulo 3. Again `v_3(n)=2m`. This includes the case where exactly one input is zero through the unequal-valuation case. If `m<0`, then `v_3(3n)=1+2m<0`, strictly below `v_3(9)=2`, contradicting integrality of `h`.

At 2, use the same minimum `m` for the 2-adic valuations. If the valuations differ, including exactly one zero input, `v_2(n)=2m`. If they agree and are finite, both scaled inputs are 2-adic units. Their squares are 1 modulo 8, so their sum is 2 modulo 8 and `v_2(n)=2m+1`. If `m<0`, either value is negative. Since 3 is a unit, `v_2(3n)<0=v_2(9)`, again contradicting integrality of `h`. If both inputs are zero, both are already integral. Thus all zero and unequal-valuation cases are included.

Conversely suppose `a,b in R`. At 3, `h` is integral and zero modulo 3, so Fact (b) with `U_3={0}` gives `h in S(Q_3)`.

At 2, if `a,b` have the same residue parity, `n` is even and `h` is odd. Fact (b) with `U_2={1}` applies. If their parities differ, the odd square is 1 modulo 4 and the even square is 0 modulo 4. Thus `n=1 mod 4` and `h=0 mod 4`. We now prove directly that every `h in 4Z_2` belongs to `S(Q_2)`.

Put `x0=h/2 in 2Z_2`.

* If `x0=2 mod 4`, then `(x0^2-1)/3=1 mod 8`. Choose `v in Z_2` with `v^2=(x0^2-1)/3`, and set `u=w=0`. The norm is `x0^2-3v^2=1`.
* If `x0=0 mod 4`, then `x0^2/6 in 8Z_2`, so `1-x0^2/6=1 mod 8`. Choose `w in Z_2` with `w^2=1-x0^2/6`, and set `u=v=1`. The norm is `x0^2-2-3+6w^2=1`.

We used the elementary 2-adic square criterion: every unit congruent to 1 modulo 8 is a square in `Q_2`. Both cases have reduced trace `2x0=h`; together they cover all of `4Z_2`, including zero. We therefore have both required local trace conditions. Fact (e) supplies a rational norm-one quaternion of trace `h`. This proves the criterion.

## Homogeneous source replacement and both directions

Introduce only `H,U,V,W` and impose

```text
C*H - 9*C^2 - 3*f0^2 - 3*f1^2 = 0,
H^2 - 8*U^2 - 12*V^2 + 24*W^2 - 4*C^2 = 0.
```

Since `C` is nonzero, division by `C^2` identifies `H/C=9+3((f0/C)^2+(f1/C)^2)` and gives its norm-one trace equation with witnesses `U/C,V/C,W/C`. Thus every solution of the new anchor has `f0/C,f1/C in R`. The original characterization `T=R` supplies the two old seven-witness `T` tuples and the old quotient variables. Every coordinate outside the old anchor is retained.

Conversely, any old solution has `a=f0/C,b=f1/C in R`. The criterion supplies rational `u,v,w` of trace `h=9+3(a^2+b^2)`. Taking `H=C*h`, `U=C*u`, `V=C*v`, `W=C*w` solves both new equations, with the same external coordinates.

These are exact existential projections for every rational input pair. They do not assert a rational formula that converts one quaternion witness tuple into another. This is an arithmetic source replacement, not a purely algebraic circuit-elimination rule. The only division by a source quantity is by the already nonzero `C`; the independent source audit must retain the shared chain generating it.

## Cost and completeness

The old module has 16 private variables and six residuals. This module has four private variables and two residuals, with all coefficients integral, maximum absolute coefficient 24, and total degree two. No separate variable for `C^2` is needed. The exact module-level saving is 12 variables and four rows. These numbers do not claim a measured saving in the final quartic; that requires the complete source audit, lift and replay.

The integer completeness construction already makes both coefficients `f_i(S)/C` belong to `R`. The new criterion therefore supplies its four witnesses without any new restriction on points, indices, primes or the common `J`. Conversely every new solution extends to the old anchor, so the old anchor bound and the pole and ordinary-prime soundness arguments apply unchanged. This includes `f0=0`, `f1=0`, and both zero. No nonzero condition is imposed on either input coefficient. The root/comparator variable maps, degree bounds and source bindings remain separate obligations for integration.
