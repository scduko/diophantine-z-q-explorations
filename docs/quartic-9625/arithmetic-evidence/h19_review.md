# Independent arithmetic review

Date: November 6, 2026.

**PASS for the stated arithmetic relation, relative to the exact inherited arithmetic inputs below.** The height-19, rational-target 37-contact, reciprocal-logarithm construction supports `(high,beta,anchor,scalar)=(40,12,25,32),(44,12,24,32),(48,12,23,32)`. I found no additional arithmetic hypothesis in their conjunction. This is permission to test these sources mathematically, not a certification of a generated source, a sub-10,000 count, or its coefficient bound.

The reviewed author proof is `../precision/PROOF.md`, SHA-256 `258d07739bed4bd114580a51bbbbeac07f6b5f6441024db2f7c19ed237b7818f`. The reference manuscript is `work/quartic-12504-release/public-repository/quartic_12504.tex`, SHA-256 `38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37`. I reopened the relevant released proof and primary literature interfaces, derived the changed inequalities, and checked the new proof itself. Earlier review verdicts were not premises.

Two wording ambiguities were corrected before this hash was frozen. The finite character whose image order divides `[L':Q]` is `epsilon^2`. The tail with valuation at least `(4m+1)r` is `log_E-L_e`; the corresponding `G-G_(m-1)` tail has valuation at least `4mr`. Neither correction changes a parameter or an equation.

## Height theorem and its published interfaces

The crucial premise is present in the released proof after its finite twist has been absorbed. The final primitive weight-two form realizes the same `r_l`, and on the normal field `L'` its double is the Tate representation of the quaternionic surface. Consequently `(det r_l)^2=chi_cyc^2` on `G_L'`. Released LR3 gives `[L':Q]<=2304R`, while the primitive level and its support satisfy `N<=210^300 R^2` and `rad(N)|R`. The proof does not substitute the smaller degree-576 field for `L'`.

In the Tate convention, `det r=epsilon*chi_cyc`. Therefore `epsilon^2` factors through the finite group `Gal(L'/Q)`. Its cyclic image order divides that group order. Squaring a finite cyclic image loses at most a factor two, so `ord(epsilon)<=4608R`. This requires no coefficient-field degree bound. A dual realization changes the finite character to its inverse only when the realization is dualized consistently. The published determinant and arithmetic-Frobenius convention are in [Diamond and Im, section 12.5, equations 12.5.1–12.5.2 and Remark 12.5.1](https://wstein.org/edu/Fall2003/252/references/diamond-im/Diamond-Im-Modular_forms_and_modular_curves.pdf). The indexed primary scan explicitly includes the epsilon factor; another OCR copy drops it, so that copy cannot be used as the formula's text.

For `H0=ker(epsilon)`, every element fixes the entire Galois-conjugate differential space of the newform quotient, not just one chosen eigenform. A homomorphism of characteristic-zero abelian varieties with zero differential has zero connected image. Thus `q<h>=q`, and `q e_H=q`. The newform quotient, its differential space, and the rational diamond convention are explicitly supplied by [Baker, Gonzalez-Jimenez, Gonzalez and Poonen, sections 3.1 and 3.2.1](https://math.mit.edu/~poonen/papers/finiteness.pdf).

The quotient and its Jacobian are over Q. In the push-pull identities one uses the image of H0 in the automorphism group, including removal of ineffective elements. Equal-sized fibers from H0 to this image make the two normalized averages equal. Hence the image of `e_H` is Q-isogenous to `J_H`, and `A_f` is a Q-isogeny factor. The Q-model and the characteristic-zero factor statement are corroborated by [Mascot, section 2.1 equation 2.1.8 and section 2.2 equation 2.2.1](https://link.springer.com/article/10.1007/s40993-022-00329-6). This argument does not use that paper's reversed subgroup quotient in equation 2.1.4 or its later mod-l kernel formula.

The existing Faltings-Hom and absolute-simplicity argument now gives an L'-isogeny `A times Z -> J_H`. It uses a shared constituent after scalar extension; it does not require all factors of `J_H` to be isogenous to A. Only `J_H` needs its Jacobian polarization. The released general isogeny estimate applies with that source. There is no new polarization-degree or descent assumption on A or Z, and the case `Z=0` satisfies the stated lower bound.

Evenness of epsilon puts `-I` in Gamma_H. Thus the map degree is exactly `N*ord(epsilon)*product(1+1/p)`, with no extra factor two. Since the product is at most `2R^(1/6)`, both the degree and genus are less than `T=2^14*210^300*R^(19/6)`. The estimate `h_F(J_H)<2^24 T^6` is the generic Belyi-degree-times-genus estimate, not the special J1 level estimate. I checked the published statements in local copies of Javanpeykar, Theorem 1.1.1 and section 2.3, and von Kanel, section 4 equations 4.1–4.2. They use the stable height of the Jacobian with the same original Faltings normalization. Their published locations are [Javanpeykar 2014](https://doi.org/10.2140/ant.2014.8.89) and [von Kanel 2021](https://doi.org/10.1017/fms.2021.29).

The transfer term is unchanged from released LT3. Substituting `g<T`, `log d'<8+log R`, and the bound on `h_F(J_H)` gives

```
V <=16T^4(2+log T)+2T^2(25+7log T)<=T^6.
```

Each final inequality follows at T=16 and has positive difference derivative thereafter. The Bost term is at most `3T/2`. Thus `h_F(A)<2^25 T^6=2^109*210^1800 R^19`. The unchanged CM bound is smaller. The unchanged metric comparison gives exactly `H19=2*(2^109*210^1800)*B_*^19+128`. With `B_*<2^109445`, its strict binary bound is 2093966. None of this proof uses a new unpublished external result.

## Rational targets, exceptional contacts, and completeness

Eight coefficients of the actual unscaled abscissas replace nine coefficients involving a source denominator. The source must retain `v!=0` and all 37 nonzero raw contacts. The ninth slope is the shared base slope. The existing parity-of-the-common-minimum argument uses rational valuations and unit differences between the four fixed branch points outside S_*. It therefore works without integral targets. It sends every normalized odd contact to an odd valuation of a retained raw contact, including contacts caused by negative valuations.

The new completeness denominator D0 is chosen after the eight rational targets are fixed. It is neither a source coordinate nor a polynomial coefficient. Multiplication by `V0*D0^2` makes every slope coefficient an integer divisible by W0. At a prime q dividing D0 outside the fixed small set, these coefficients vanish modulo q, and u and p0 can independently be 1. Their successors are then nonzero. At 31, 37 and 41 not dividing D0, the factor 47027 reduces the slope set to at most eight residues. At q>=43 there are at most 36 residues. Two missing residues exist in both cases. Reversing them avoids the one forbidden difference for p0+1. This proves the claimed value/successor admissibility.

Exact duplicate slopes are removed only in the analytic prime-pattern application. The remaining forms have independent linear parts. The fixed cutoff includes denominator and nonzero determinant primes. Both fiber equations remain affine with fixed integral coefficients; the auxiliary third coordinate and the cutoff-first, box-size-second argument are unchanged. The complexity decreases to at most 35. Constants may depend on D0 and the targets because they are fixed before the large-box limit. No uniform prime theorem in a growing denominator or modulus is being assumed.

For q dividing D0 outside S_*, the selected primes are larger than q. Hence u is a q-unit, `v_q(v)=2v_q(D0)` and `v_q(A_i v)>=v_q(D0)`. Both slopes have valuation `-2v_q(D0)`; their infinity depths are even, and their finite branch differences have the same even valuation. This rules out a new normalized odd contact. The raw infinity contact is `D0^2*p0`, with its unique odd valuation equal to one at p0. The other raw contacts are the selected positive primes.

The norm root is a unit at its assigned prime because the constant leaf lies on the all-left path and every other normalized leaf can be made integral there. Elsewhere a denominator in the norm root contributes an even valuation after squaring. Thus the parity argument has square reduced denominator even when a private point has a denominator at a prime dividing D0. Positivity and the Q2, Q3, Q17 square classes are also preserved by the square factor. Repeated prime occurrences can share their orientation while retaining independent private witnesses. No cross-prime coprimality of reduction orders is used.

The direct coefficient heights are sufficient: the two-slope identity gives `h(a_i)<2H|N|^(19/e)+14`; the two rational coefficients of an abscissa give `h(x(Q))<4H|N|^(19/e)+30<5H|N|^(19/e)`. The weaker coefficient 7 used downstream is therefore safe. No height bound for D0 is needed.

## Local logarithms, norm tests, and reconstruction

For `w=Df^2`, the exact curve identity and recurrence give `log_E(z)=zG(w)` as a formal identity. This does not identify the new finite polynomial with the old truncated polynomial. At a nonidentity formal-group point over a selected split prime p>76176, `v(f)=2r` and `v(w)=4r`, where r=v(z)>=1. The factorial bound on coefficient denominators covers the entire infinite tail, including terms beyond p. With m<=16, terms before the first possible denominator are integral; later terms have j>=19044 and `4jr-j>=4mr`. The valuations tend to infinity. Multiplication by z and the formal logarithm isometry give the required relative error modulo p^e. The word "formal" is necessary: positive v(z) alone would also allow the wrong branch near a two-torsion point.

For global nonvanishing, the ramified 2-adic valuation on Q(sqrt(2)) has half-integral value group, D is a unit, and every nonconstant recurrence coefficient has valuation one. For v(f)>=0 the constant term is uniquely least. For v(f)<0 the final term is uniquely least as soon as J>=2. Every permitted precision e>=10 has J>=2. This proves nonvanishing at arbitrary rational coordinate assignments, not just on a selected formal branch.

The compressed equations then force Lambda and every primary p_i to be nonzero. From `f_i p_i^2=v_i^2(1+d f_i)` they also force v_i nonzero. The reverse formulas `z=-1/p`, `y=xp`, `h=up`, `w=up/v`, together with `Lambda=-L_0` and `C_i=L_i/L_0`, restore the full charts and ratios. All denominators in this map have been justified. Forward substitution gives the stated compressed equations with the correct sign. The actual source checker must still verify privacy and every outside occurrence before removing coordinates.

For arbitrary odd raw-contact valuation R, the constant-left norm path bounds the root valuation by zero when R<0. The pole condition then excludes R<0. When R>0, descent yields `v_p(X)>(e-1)R>=e-1`, so the integer valuation is at least e. This is valid for every positive integer leaf order, not merely powers of two. The root test then forces splitting; theta is a unit and Hensel chooses rho with theta+rho a unit. The two rational tests imply the field test at rho through `theta-rho=(theta^2-2)/(theta+rho)`, even when its coefficient B has negative valuation.

All four index proxies must remain in every comparison. The alternate tests imply `(h-4)/j` has valuation at least K and `(m_i-4n_i)/j` at least e_i. Since j and the target indices are integers, h is a unit and `m_i/h` is integral with the required residue. Relative finite-logarithm errors preserve these residues. The scalar tests work at inert primes too: both coefficients are tested, the extension is unramified outside 2, and the formal logarithm compares `z(S)/z(J0)` to the rational ratio s/j0. Thus `M5(beta)^E_s|s` and `h(beta)<=H|s|^(19/E_s)`.

Completeness has the required order of choices. Choose scalar data and the anchored s first, then Lucas points, then their rational coefficients and prime pattern, then the common J and private points, and theta last. The condition `h_p=4 mod p^(K+v_p(j))` accounts for cross-prime factors in the lcm j. The only reduction-order coprimality invoked is at the same selected prime. Avoiding 0, 4 and -4 preserves the chart and difference guards. Arbitrarily deep finite choices are available; no circular dependence on D0 or on theta occurs.

## Strict inequalities and permitted parameters

For integers `39<=K<=64`, `10<=q<=K`, `20<=E_s<=38`, the proof requires the exact strict inequalities

```
(3/2)(2^(A-1)-1) > K*2093971/(2K-76),
(3/2)(2^(A-1)-1) > E_s*2093972/(E_s-19).
```

They imply `a>(24H)^(K/(2K-76))`, `a>(40H)^(E_s/(E_s-19))`, and a>40. The scalar inequality gives `h(beta)<a/40`. Since `E_s/(E_s-19)>=2`, the same cutoff and `40log(40H)<(40H)^2` give `log(40H)<a/40`.

If Delta is nonzero, every contact contributes the high-order divisibility even for the abscissa of nP_*. Then `B^2-6<7H|Delta|^(19/K)<16HB^(76/K)`, using `|Delta|<5B^4` and `7sqrt(5)<16`. Dividing gives `B^(2-76/K)<22H<24H`, contrary to B>=a. Thus Delta=0 and the unchanged Lucas bound gives `log B>a-3`.

If beta differs from n, its nonzero reduced numerator N satisfies `N<=2 exp(h(beta))B`. The beta congruence controls all four target abscissas, so `B^(2-19/q)<40H exp(19h(beta)/q)`. Taking logarithms yields a strict upper bound `((q+19)/(40(2q-19)))a`, at most `29a/40<a-3`. For q=12 the coefficient is exactly 31/200. Thus beta=n and rational X with X^2=beta-2 is integral.

The three proposed E_s=32 tuples satisfy both strict tests. K=39 is also arithmetically valid with A=26, but has the same ten G coefficients as K=40. Beta 10 has the same three G coefficients as beta 12. K<=38 and q<=9 do not yield these growth contradictions. Smaller E_s can be valid with an adequate anchor, but an arithmetic parameter change alone establishes no circuit saving. Parameters outside the displayed family require a separate proof, even where an extension may be possible.

## Inherited scope, files, and remaining finite work

The unchanged arithmetic inputs are identified in the released `degree8-original/arithmetic/current-proof.json` and `assumption-status.json`. The latter expressly retains the original restricted-converse and baseline arithmetic status. This review does not reprove that restricted converse, the cyclic generator/index-height statement, the seven-witness pole theorem, or the published prime-distribution inputs. In particular it retains the source-version conventions in the sieve ledger, the Pan/Calegari publication interface, and the author-attested Yuan translation qualification. The new quotient argument does not strengthen any of these statuses.

The following exact public files were rehashed, with paths relative to `work/quartic-12504-release/public-repository/`:

| File | SHA-256 |
| --- | --- |
| `degree8-original/arithmetic/current-proof.json` | `af4570f0f20c0e1895b3567f2c18a13d0cc40d939ac051047a757a3c145d753e` |
| `degree8-original/arithmetic/assumption-status.json` | `79ab37c5b822300ae0472ad391dcc02e2ff15e6020f21b4dad58986b08816101` |
| `degree8-original/arithmetic/sieve/applications.json` | `28b8f85d33be96b7148de22214dbe7fd39d221a99ab56c75534ad47edc18b062` |
| `degree8-original/arithmetic/sieve/source-ledger.json` | `e98599849e678182edac7c825a58ec9d86604198fbdd277e64faa128eae2b125` |
| `degree8-original/arithmetic/anchor/source-application-ledger.json` | `2f81ceea6b525913b1790c2695da9fb3cc3c9c8b63bfbe7e16bc26d0a227e5ef` |
| `degree8-original/arithmetic/parity/parity-justification.tex` | `df67c17520d942a4a5d8505b5ed1d97bf2bd3d18f8d13cbf514f758d7286075d` |
| `docs/theorem-application-audit/applications.json` | `1d53028414eefe1eeed85db566aae47b2b00d4206f3eaffeec8625f0e3c089bb` |

Sieve application records OP01–OP14 are the exact inherited prime-pattern inventory. OP02 gains deduplication, OP03 denominator-prime admissibility, OP04 the smaller form count, OP05/OP06/OP08 the fixed new coefficients, and OP13 the square-times-prime infinity case. OP14 requires a fresh source audit. The old height19 manuscript packet cites `lem:o8-rational37` without supplying its TeX lemma; the new author proof supplies the missing substantive argument in section 3. It must be included when any later manuscript is assembled. Historical packet text is not a ready standalone manuscript.

`verify_arithmetic_gate.py`, SHA-256 `afa76bacacb513ab5c80fadb8ab16bb857a25cde3ad279ef49b2a604b756f7f4`, independently checks the prime product, integer H19 envelope, strict rational cutoffs, mixed-order lists and coefficient counts. It includes nine invalid-parameter cases which must be rejected. It imports no source producer and has not been executed locally. Root can run it remotely with:

```sh
python3 -E -B work/quartic-sub10000-20261106/arithmetic-audit/verify_arithmetic_gate.py
```

The next acceptance boundary is finite and source-specific. Bind every regenerated original module, all direct rational target arguments, the 37 retained calls, all 41 tests per call, the exact G profiles and output consumers, scalar correction bits, anchor chain and terminal coordinate, all nonzero/difference guards, and full outside-use incidence. Then perform the independent lift/replay/mutation/collected-expansion checks. Neither this review nor a numerical PASS from the diagnostic substitutes for those operations.
