# Audit of the public 41-variable construction

The public proof supports a conditional construction with 41 total rational coordinates and 40 existential witnesses. I found no counterexample to its shared-point argument, scalar normalization, conic elimination, direct Lucas substitution, or guarded finite-algebra theorem. There is a small gap in the scope of a cited local lemma: the upstream reciprocal-logarithm statement assumes a split prime, while the new soundness argument allows an inert prime. The supplied additive lemma proves the needed unramified version. It changes no formula, guard, variable count, or bound.

The exact reported bounds `degree <= 2^9566673` and `height <= 2^(2^86098382)` are not independently certified by this audit. The generic bounding method and the fixed elliptic coefficient estimate check out, but their substitution into the 6018-node coefficient specification is not reproducible from the public files. This is an evidence limitation, not a counterexample to either bound. No change of those bounds is established.

This audit treats the pinned source's restricted converse, pole-completeness arithmetic, and five-contact height theorem with its stated constant as inputs. It does not establish the arithmetic theorem unconditionally. Sun's Theorem 4.1 is also an input here; its separate dedicated audit is in `../sun41/`. I checked that Brox's application matches its statement.

The audited manuscript is `diophantine_optimization_20261106_v3.tex` at JoseBrox repository commit `f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6`, SHA-256 `fc8bc7b8fae727e24f934ddd7de0a7cff8a005e89c3d0cac1ea14e5191b910ca`. All unqualified line numbers below refer to that exact local file in `../../josebrox-claims-audit-20261106/`. “Upstream” means `../common/upstream-quartic-12504-28e87b1.tex`, recovered from commit `28e87b1b62af0effd954605af7f70b2699dd5672`, SHA-256 `38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37`.

1. **Fixed curve, integer labels, and chart coverage.** Lines 2367–2411, 2504–2557, 3531–3548.

   The point belongs to `y^2=x^3-(11-6sqrt(2))x`; the exact check is included in `check_brox41.py`. The norm of `3-sqrt(2)` is seven, as required for the conjugate reduction-order argument. The identity `2E(K)=ZP` is inherited from upstream 279–359 and transported at upstream 7808–7818. I reviewed that dependency and independently replayed its bounded square search: 7004 primitive quadratic polynomials, their 14008 roots, and 111 rational candidates yield exactly the seven abscissas in upstream 342–343. This does not replace the surrounding two-descent and height arguments.

   The ordinate chart is exact. Writing `a^3-Da=A+B sqrt(2)`, the quartic `C^4-AC^2+B^2/2=0` and `C!=0` give `b=C+B sqrt(2)/(2C)` with the correct square. If a chosen halfpoint has zero rational ordinate component, translation by `(0,0)` provides one with nonzero rational component. Otherwise the proof forces `d^3` to lie in either `Q` or `sqrt(2)Q`; the actual value is `45-29sqrt(2)`, which lies in neither. The guard `A^2-2B^2!=0` holds at every nonzero rational halfpoint ordinate and makes the permitted quartic root simple. After `Y=2C`, the relation is the integral monic quartic `Y^4-4AY^2+8B^2=0`. No second ordinate chart or retained ordinate coordinate is needed.

2. **One place for all tests and the two-anchor comparison.** Lines 2572–2671, 3810–3850.

   The parity calculation in the reciprocal-trace detector is valid for both split and inert primes. If `alpha=v_p(R)` is odd, every nonconstant summand in a factor of `W` has odd valuation, so cancellation with one is impossible. Let `lambda` be the largest place-valuation of `W`. The inequality `v_p(T)>=-lambda`, combined with the pole obstruction, forces `alpha>0` and `lambda>-alpha/2`. At a place attaining that maximum, every test satisfies `v(D_j)>(m_j-3/4)alpha`, hence `v(D_j)>=m_j`. Vanishing tests cause no exception.

   The exact ratios are `u_i/h` and `(u_i-4n_i)/(h-4)`. Since `p!=2`, one denominator is a unit. Its ratio is integral, the difference test transfers integrality to the other ratio, and then the relative approximation bounds become absolute. The identity `h r_i-(h-4)r'_i=4n_i` proves the claimed congruence.

   Upstream 8753–8816 states the reciprocal-logarithm approximation only for a split prime. Brox 2669–2670 invokes it at an inert prime without separately stating the extension. `reciprocal_unramified_repair.tex` supplies that extension, including precisions 16, 52, and 64. At an unramified completion, valuations are integral, `D` is a unit, `v(f)=2v(z)`, and the same factorial denominator estimate controls the entire infinite tail. Thus this is a local proof clarification with no effect on the construction. The precision-52 section also explicitly treats both splitting types at 4206–4207.

3. **The fixed preparation-zero pole.** Lines 2446–2460 and 2574–2602; upstream 7523–7752.

   This is the old seven-witness predicate specialized to preparation parameter zero and `U=b`. The one-sided parity obstruction still applies, including the degenerate values `e=0`, `p=0`, `s=0`, or `h=0`. No new guard on those witnesses is needed.

   For completeness, `V=17^2 b^2(1-b/17)`. The conditions `0<b<17`, `v_2(b)>=3`, `v_3(b)>=1`, and `v_17(b)>=2` make `V` positive and square at the three indicated completions. These are precisely sufficient for the preparatory step in upstream 7712–7717. The remaining disjoint-support and mutual-squareness argument in upstream 7720–7735 applies with `U=b`. The resulting simultaneous two-twist existence remains dependent on the inherited restricted-converse and descent inputs. Brox has not silently replaced that arithmetic input with an elementary conic argument.

4. **Height transfer and the size anchor.** Lines 2673–2763, 3352–3405, 2038–2115, and 2121–2349.

   The contact transformation `phi(t)=2+1/t` sends the five displayed finite contacts to `infinity,0,1,2401,-343/32`. Its matrix and inverse are integral of determinant minus one. I reproduced the exceptional-prime list, including all contact differences and differences from one: `2,3,5,7,11,37,109,439,2399`. Thus these transformations introduce no prime above the existing cutoff.

   The scale `A_0=x_0^2` is nonzero because the doubled abscissa is positive at both real embeddings, hence `x_0>0`. For the other component, `A_1=(1+x_1^2)^2` has height at least `4h(x_1)`. The unchanged constant `7H` in the point-height bound follows from the displayed inequalities. No independent height parameter has been lost by sharing the slope.

   The fixed exclusion is exact over rational base points: `u^2-2v^2=0` implies `u=v=0`. Hence it excludes `S=+/-jP` for all `1<=j<=M`. With `M=2^9566463` and `H<2^4783227`, it implies `|a|>M>(20H)^2`. Completeness allows indices larger than this fixed number while meeting finitely many congruence and real open conditions.

   The fixed-coefficient height argument is valid. The elementary common-denominator estimates imply `H_0(nP)<=17n^8` through the binary recurrence `H'+7<=180(H+7)`. The norm bound `||M_E||<=2^((2b+38)M^9)` then follows by multiplying factor bounds. It does not require expansion of the exclusion product.

5. **Shared completeness and the generalized CRT.** Lines 2765–2921 and 2946–3045.

   Once the four root labels are fixed, all positive square scales are fixed. Choosing `D_0` clears the contact denominators, giving integer coefficients in the forms `u+c_j w^2`. At least the five contacts of one detector remain distinct after duplicate removal. Sun's theorem allows these coefficients, arbitrary fixed divisibility of `w`, a lower bound on `u/w^2`, and a lower bound on the primes.

   The avoidance modulus is allowed: it is the odd squarefree product of the required factors of `3*17*L`, excluding seven. The Gaussian condition modulo seven gives order residues six and two, so seven is avoided separately. The condition modulo sixteen gives exactly `v_2(d_+)=2` and `v_2(d_-)=6`. These finite calculations were reproduced. Sun's all-pairs cross-gcd assertion gives `gcd(U,V)=4`; avoidance gives `gcd(U,L)=64` and `gcd(V,L)=4` when `64|L`. The residues `0,4,h_0` are compatible because `64|h_0`. No unjustified pairwise coprimality assumption occurs here.

   For the curve actually used, the two conjugate twisting parameters have product seven. At the selected primes, `p=1 mod 8` and `p=3 mod 7`, so seven is nonsquare and the reductions have the two opposite CM orders in Sun's statement. One can choose the place with order `d_-`; the conjugate place has order `d_+`. The resulting multiples enter the required formal groups without requiring a prescribed order for `P` itself.

   The real compact-group argument also works. The closure of the cyclic orbit is a compact abelian Lie group with finitely many components. Its identity component projects onto each real elliptic identity circle, since each projected orbit is infinite. A finite union of inverse images of poles has empty interior there. After local congruences are fixed, the final progression is dense in the relevant component and has arbitrarily large positive representatives. Bounds for the comparison functions can therefore be chosen before the later prime-pattern moduli.

   In the pole construction each selected contact prime is excluded from `v` and from all fixed scale and difference denominators. Exactly one contact factor contributes valuation one in a given detector. At the successful place `W_r^{-1}` has residue one; at the other place its residue is zero or one. Consequently `T_r` has residue one or two and is a unit. The reduced denominator of `B_r` is square, and the Gaussian congruences make its squareclass trivial at two, three, and seventeen. The real and small-prime asymptotics in 2887–2918 then give all preparatory inequalities simultaneously.

6. **Scalar normalization with the same shared point.** Lines 3049–3340.

   The normalizer `delta(T)=T^2+T+23` has no real zero and no root at the seven primes in the displayed local basis. The contact evaluations in 3136–3143 are correct. I recomputed every row of the local-squareclass matrix, its rank seven, the six possible common-divisor primes, the correction product `518513917206770054130`, and the strict inequality `2^16*Cmax*204^2<23^24`.

   The two finite prime sets are disjoint. The first adjusts parity at every possible denominator/contact collision; the second adjusts the three local squareclasses without changing those parities. Thus `cR_beta` has square reduced denominator. The real bound gives `0<cR_beta<1` and the fixed factor `204^2` gives the stated small-prime valuations.

   Soundness uses only the original finite contacts. For `beta=X^2+2`, every negative valuation is even; outside the old exceptional set the quadratic normalizer is a unit at each relevant finite contact. Replacing `r_beta` by `R_beta` therefore preserves the odd-contact norm argument and `M_5(beta)^48|a`. The original height input gives the same `h(beta)<=H sqrt(|a|)`.

   Completeness imposes local unit conditions for `W` at the finite support of `cR_beta` and makes all six real tests small. The first choice of `H_*` can lie in a small real open subset of the identity component while satisfying the finite local subgroup conditions. Then `S` can satisfy its divisibility and size requirements and approach the real identity. This makes `W` close to one uniformly for `H` in the chosen open set. The final CRT progression preserves the local conditions and is dense in that same real identity component. Hence `0<b=cR_beta W^2<4` and the preparation-zero pole is complete. This order of choices avoids a circular requirement on the later common index.

7. **Conic elimination and direct Lucas substitution.** Lines 3407–3452 and 3720–3915.

   The conic formulas include both `e=1,p=0` and `e=-1/3,p=0`. The first is the fixed chart `sigma=1,t=0`; the second belongs to `sigma=0,t=0`. For `e!=1`, the inverse parameter is `t=p/(e-1)`, and its denominator is nonzero because `t^2+3B=-4B/(e-1)`. Thus one finite square root per pole is genuinely removable; no forbidden nonzero condition on `p` or `t` appears.

   Polynomial evaluation preserves the congruences once the two-anchor argument has proved integrality of the ratios. The new order-64 field test gives `p^64 | Delta` for the same integer Lucas residual. It does not claim exact equality between approximate ratios and labels. The inequalities `|Delta|<5B^4` and `B^2-6<7H|Delta|^(3/8)` contradict `B>=(20H)^2` unless `Delta=0`. The inherited Lucas growth lemma and scalar estimate then force `beta=n`. Conversely, exact integer Lucas labels give the required local congruence of the approximate test. Its real values and small-prime valuations remain controlled because it is a fixed polynomial in the previously controlled ratios.

8. **Finite algebra, exceptional fibers, and integer clearing.** Lines 1386–1519, 3531–3614, and 4090–4110.

   The triangular monic presentation is free on the standard monomials. A rational equation `q^2=N/D` is converted by `Z=Dq` to `Z^2=ND`, retaining the denominator guard. The zero-radicand branch uses the relation `Z=0` and a separate closed residual for the coefficient, rather than quotienting by the latter and destroying freeness. The other branch guards `Z!=0`. Together with the simple quartics, this gives local length one at every guarded geometric point, not just generically.

   In the determinant construction, a bad component with `G=0` contributes only the factor one to `det(I-VM)`, even if that component is nonreduced. There are at most `m*n*(n+1)/2` bad separating integers: each individual zero and each pairwise collision is the root of a nonzero polynomial of degree at most `m`. The stated inclusive integer range therefore contains a good choice.

   The degree cases enforce every higher coefficient to vanish. The resultant and leading-coefficient guard make the selected characteristic root simple. A rational kernel line of `I-VM`, preserved by every multiplication matrix, gives rational values for every algebra generator. At that root `J=Tr(adj(I-VM))=-V H'(V)!=0`, so the reversed trace residuals enforce exactly the closed equations. The reciprocal residual is one whenever its clearing factor or `U` vanishes; no extraneous root enters at a cleared denominator. This is a global fiber argument and needs no unperformed exceptional-stratum decomposition.

   The independent small interpreter exercises a nilpotent component killed by the guard, a degree drop, a surviving trace residual, a separating collision rejected by the resultant, an empty guard, and the linear zero-quadratic branch. These finite checks support the audit of the proof; they are not substituted for that proof.

9. **Count and quantitative certification boundary.** Lines 3894–3923 and 4054–4128.

   The retained count is `1+18+1+18+2=40`. The nineteen formal generators consist of nine quartics and ten quadratics, with maximum rank `4^9*2^10=2^28`. The determinant construction adds exactly one retained rational coordinate. Fixed correction choices, conic charts, quadratic masks, separating integers, and degree cases are finite product indices, not witnesses. This proves the stated 41 total coordinates structurally.

   With the literal displayed product ranges, there are `2^14*2^10=2^24` original parameter choices, `2^10` quadratic masks, and

   `2^24 [4^9*3^10 + (19/2)((4^9)^3*9^10 + (4^9)^2*5^10)]`

   final factors, equal to `10011251370231759899441399242686464`. This count was independently recomputed without forming a matrix or product.

   The generic weighted-degree, matrix-norm, determinant, Sylvester-resultant, reversal, and outer-product estimates in 1526–1643 are valid. The common-denominator elliptic coefficient estimate in 2121–2349 is also valid. But the 41-variable instance needs the actual recursive generator weights, matrix-norm majorants, guard list, residual list, and integer clearing choices. Lines 4104–4108 refer to these data and an independent receipt; the public repository does not supply them. I therefore do not mark the specific 6018-node artifact, its hash, or the numerical degree and height exponents verified. Publishing the source DAG and receipt would make those claims reviewable; no mathematical failure follows merely from their absence.

`check_brox41.py` uses only Python's standard library and writes `checks.json`. It completes in a few seconds and uses no large matrix, expanded exclusion product, or network resource. It now contains nine groups of exact checks. The source hashes bind the checks to the audited version. The only proposed mathematical edit is the additive unramified logarithm lemma in `reciprocal_unramified_repair.tex`. The pinned manuscript is unchanged.
