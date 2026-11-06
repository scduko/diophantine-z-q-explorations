# Audit of Sun's simultaneous prime theorem

Audit date: 2026-11-06. Target: Zhi-Wei Sun, arXiv:2610.20691v2, Theorem 4.1, Sections 4–6 and Appendix A.

## Result and scope

I found one minor hypothesis omission and repaired it. Appendix A's definition of a good prime must explicitly exclude 2 to match the cited lattice-cover lemma. `LOCAL_REPAIR.tex` makes this change by including the divisors of 2κ in the fixed exceptional set. It changes no hypothesis or conclusion of Theorem 4.1 and no exponent or stated constant dependence in its proof.

With that local repair, I found no surviving mathematical gap in this proof chain. The local counts, primitive quadric normalization, two sieve ranges, fixed-field transference, ray-class density calculation, and final diagonal choice fit together. This conclusion treats the cited external theorems as inputs after checking their exact statements and hypotheses. It is not an independent proof of those external theorems, nor an audit of the separate OpenAI arithmetic inputs.

There is one citation issue. Sun uses the theorem numbering of the Tao–Ziegler arXiv preprint while the bibliography names the published paper, whose numbering differs. The cited results exist with the required hypotheses. `CITATION_REPAIR.tex` supplies a version clarification. It changes no mathematics.

All line references below are one-based physical lines of the preserved TeX source, not HTML display lines. `P103q.tex` is the unmodified source extracted from the pinned Sun archive. The numbered copies facilitate review. `SOURCES.json` records URLs, versions, byte counts, and SHA-256 hashes. `STATUS.json` and `DEPENDENCIES.json` distinguish checked applications from accepted external inputs.

The Sun TeX SHA-256 and every downloaded payload hash are in `SOURCES.json`. The original HTML and source archive are retained. Two arXiv source responses are gzip-compressed single TeX files despite their local `.tar` suffixes; their correctly decompressed `source.tex` files are the reviewed texts.

## What Theorem 4.1 supplies

Source: `P103q.tex:514–532` and the conclusion at `1020–1042`.

The quantifiers needed downstream are present. The coefficient list is any fixed finite list of distinct integers with at least two entries. The prescribed divisor of the positive parameter w, the odd squarefree avoidance modulus prime to 7, and the two positive lower bounds are fixed before counting. The theorem supplies every cross-sign gcd equal to 4, including equal positions. It also supplies the stronger absence of odd common factors between any two orders at distinct positions.

The dilation argument is valid. Apply the proof to coefficients q²c_j and then put w=qv. To obtain the requested bound u/w²>H, choose the pre-dilation ratio greater than q²H, or use its divergence. No uniformity in q is needed. Negative coefficients cause no problem: choose the fixed initial upper bound on w/√N small enough that every u+c_jw² lies between positive fixed multiples of N.

Writing a=9+16A and b=16B gives

\[
(a+1)^2+b^2\equiv4\pmod8,\qquad
(a-1)^2+b^2\equiv64\pmod{128}.
\]

Thus the two valuations are exactly 2 and 6. Removing all odd common factors makes the cross-sign gcd exactly 4, not merely a bounded power of 2. At a prime dividing the avoidance modulus, a+bi≡i gives both order norms congruent to 2. At 7, the chosen residue gives the two norms 6 and 2. These facts match the requested order orientation and avoidance.

## Exact external inputs

| Input | Preserved source location | Check |
|---|---|---|
| Browning–Loughran, arXiv:1705.01999v2, Theorem 4.1 | `browning-loughran-1705.01999v2/source.tex:1278–1326` | A nonsingular isotropic quadratic form in n≥5 variables; smooth compact support away from the singular point; modulus coprime to 2Δ; arbitrary nonzero solution residue subsets. Error B^(n/2+ε)m^(n/2+ε), uniform in modulus and subsets. |
| Browning–Heath-Brown, arXiv:2003.09593v1, Lemma 2.1 | `browning-heath-brown-2003.09593v1/source.tex:559–599` | Polynomials have no common factor in Z[X], including constant prime factors; coefficient height enters only logarithmically; rectangular boxes allowed. |
| Same paper, Lemma 4.1 | `browning-heath-brown-2003.09593v1/source.tex:949–983` | Rank at least 3 and squarefree good modulus. For rank 3: O(9^ω(q)q) covering lattices, determinant q²; O(9^ω(q)q³T^-3) with largest minimum above T. |
| Frei–Tinková, arXiv:2408.17441v3, Theorem 1.4 and formula 1.15 | `frei-tinkova-2408.17441v3/linear_equations_in_artin_primes.tex:330–408` | Unconditional fixed finite Galois fields, conjugacy classes, finite-complexity affine-linear systems of bounded normalized size, and convex regions. The error is uniform in the systems and regions with these bounds. |
| Tao–Ziegler, arXiv:1603.07817v1, Theorems 2.5, 3.1, 4.1 and Corollary 3.9 | `tao-ziegler-1603.07817v1.tex:462–475,627–676,965–973,1022–1031` | Bounded-function concatenation, an arbitrary-function dense model, simultaneous global/local norm approximation, and the polynomial generalized von Neumann theorem. |
| Milne, Class Field Theory v4.03 | `milne-CFT-v4.03.pdf`, Chapter V, Theorem 1.7, pp.150–151; Section 3 | Ray-class exact sequence and Artin reciprocity. The Gaussian specialization and finite-group calculations are replayed below. |

The Browning–Loughran condition is n≥5. PDF text extraction can display it as n>5; the preserved TeX resolves the ambiguity. The five-variable application is permitted.

Frei–Tinková's primitive-root result is Theorem 1.2 and assumes HRH. That result is not the one used here. Their separate Artin-symbol result, Theorem 1.4, is unconditional. A finite Gaussian ray-class field is legitimate input to the latter theorem. The audit found no hidden GRH assumption at this step.

## Local counting and the intermediate sieve

Source: `P103q.tex:536–680`.

For p away from the fixed bad set, the rank-five affine cone has p⁴ points, including its origin. With χ the quadratic character of -1, let ν₀=p+(p-1)χ be the number of representations of 0 by two squares. A nonzero norm has p-χ representations. Splitting on w=0 and w≠0 gives exactly the numerator in equation 4.8. Distinct coefficient differences prevent intersections away from w=0. Removing the common origin gives the stated denominator p⁴-1.

The collision count is also correct. At split primes, the two shifted norm-zero conditions each have two linear branches. The remaining equation is linear in one coordinate with a nonzero coefficient, giving at most 4p² points. At inert primes, both shifted pairs are forced, and the quadric then forces w=0, giving one point.

An initially suspected k=2 positivity defect was withdrawn. It confused the union of the two norm-zero loci with their intersection. At an inert prime, equation 4.8 gives g(p)=2/(p²+1)>0. Therefore no finite-set enlargement or sieve repair is required. This failed candidate is recorded to prevent its reuse as a purported counterexample.

The quadric is isotropic over Q, for example at (1,0,1,0,0), and has nonzero discriminant when κ≠0. Thus Browning–Loughran applies. Möbius inversion for primitive vectors is valid even though the imposed collision residues are not homogeneous: at a scaling divisor h prime to the modulus, the subsets become h^-1Ω_p and retain their cardinalities; if p divides h there is no contribution. The error sums absolutely. The unrestricted p-adic density is

\[
\sigma_p=(1-p^{-4})/(1-p^{-3}).
\]

After primitive inversion the local factor is 1-p^-4. Prescribing Ω_p changes it by exactly |Ω_p|/(p⁴-1). This verifies the normalization of equation 4.9.

The Selberg denominator has order at least (log z)^k. The χ(p)/p contribution has a bounded sum, while the k/p part supplies k log log z. Removing one prime changes the Euler product by a bounded factor. The Rankin/Markov truncation argument retains a fixed positive portion of the product mass.

For z=B^0.01 and obstruction primes at most B^0.01, the summed remainder exponent is

\[
2.5+\varepsilon+0.01(7+4\varepsilon)+0.01(3.5+\varepsilon).
\]

At ε=0.001 this is 2.60605<2.7. Fixed logarithmic weights fit within B^2.8. The self-gcd lattice sieve is less demanding. On prime vectors the two prime norms force primitivity, and all sieved values exceed z. No omitted prime condition is needed to achieve the log-power saving.

The archimedean density is O(τ) with a constant independent of τ. Polar coordinates eliminate the second radial factor through the delta constraint, leaving an interval of length O(τ) in w. Derivative-dependent constants occur only in the error. This distinction is sufficient for the later diagonal choice.

## The large-prime estimate is actually proved on the needed affine expressions

Source: `P103q.tex:1437–1552`.

The proof does not apply the homogeneous-auxiliary-form version of the Browning–Heath-Brown quadric theorem to nonhomogeneous forms. It uses their two smaller lemmas after an explicit change of coordinates. This avoids the proposed homogenization objection.

Set x₀=a+c, x₁=a-c, x=b-d, z=b+d. Then x₀x₁=R=κw²-xz. Ignoring the parity restrictions only enlarges the set in an upper bound.

For a large common divisor of x₀ and x₁, R is divisible by its square. At each fixed value of R, divisor counting gives O(B^(1+ε)) triples x,z,w. The zero value has the stated O(B^(2+ε)) contribution after including x₀,x₁. This handles the points absent from the two invertible charts.

In the chart t=a-c≠0, set

\[
P=\kappa w^2+2t,\quad T=(t^2+x^2)(t^2+z^2),\quad
K=(\kappa w^2-xz+t^2+2t)^2+t^2(x+z)^2.
\]

The identity K-T=P(P+2t²-2xz) is exact. For a prime not dividing 2t, the original obstruction forces both P and T to vanish. They are coprime over Q because they involve disjoint variable sets and t≠0; the coefficient of x²z² in T is 1, so there is no common constant prime.

In the chart t=a+c≠0, the pair is P′=κ(t+2)w²-2xz and the same K. If t≠-2, P′ is a rank-three homogeneous quadratic form and therefore irreducible, while K has the nonzero constant t²(t+2)². It cannot divide K. If t=-2, the possible factors x,z do not divide K. The coefficient -2 excludes common odd content.

There is a local hypothesis omission at `P103q.tex:1455`. Browning–Heath-Brown explicitly defines an R-good prime to be odd, with rank-preserving reduction, at `browning-heath-brown-2003.09593v1/source.tex:949–955`. Sun's sentence mentions only rank. The later assertion that the obstruction prime is not 2 does not fix this: the auxiliary lattice modulus q is built from divisors of t, not from obstruction primes, and could still include 2 under the incomplete definition.

The repair is to require good primes to be odd and take S_R to contain every prime dividing 2κ before defining q at `P103q.tex:1503`. For R=κw²-xz, all primes outside this fixed set have rank three. This restores every hypothesis of the lattice-cover lemma. Primes in the enlarged fixed set remain in the allowed support of t/q in the Rankin estimate. Its constant already depends on κ and ε, so the repair changes neither its order nor any later exponent. `LOCAL_REPAIR.tex` gives exact replacement text for both locations.

With that convention, for each fixed squarefree good radical q of t, the stated O(B^ε) bound on the number of t is valid. Rankin's bound contributes (B/q)^ε times a product over prime factors of q and a fixed set. The latter product is O(q^ε) with constant depending on ε and the fixed form.

The lattice-cover theorem gives determinant q² and successive minima at most q because each lattice contains qZ³. Large last minima cost O(B^(5+ε)T^-3). On the other lattices a short basis gives a coordinate box of volume O(B³/q²) and smallest side at least a constant times B/T. Substitution preserves rational coprimality. Any common constant prime introduced by the basis determinant divides q, hence t, and can be removed because those primes are excluded in the chart.

The rectangular box sieve then costs O(B^(3+ε)/(L log L)+B^(2+ε)T). Summing 9^ω(q)/q loses only B^ε. Taking T=B^(3/4) gives the claimed exponent 11/4+ε. At L=B^0.01, small ε and fixed logarithmic weights yield O(B^(3-1/200)). The self-gcd tail follows directly from the coprime polynomials a and b²+1. This proves the power-saving input used in Proposition 4.3 relative to the two cited sieve lemmas.

## Fixed Artin fields and polynomial transference

Source: `P103q.tex:682–907`.

The conditional weight μ_j is correctly normalized. If D contains the conductor of the maximal abelian subfield, then K∩Q(ζ_D)=K^ab, and φ(D)η_{K,C}(b,D) is the fraction of the commutator coset in the desired class. Summing over conjugacy classes gives the displayed μ_j∈[0,1]. No factor 1/[K:Q] is missing.

Lemma 5.2 expands genuine difference-multiset norms. Its variables h_i,h′_i are independent. The affine prime forms have the same nonzero x coefficient, and different vertices have different step coefficients, so no pair of their linear parts is proportional. The finite-complexity hypothesis is met.

At each fixed v, W, q and the normalized coefficients are bounded. The wraparound cells are convex. Frei–Tinková therefore gives an error o_v(n^(2a+1)); since J is a fixed-v positive fraction of n, this is o_v(nJ^(2a)). Moving endpoints and n-dependent constant terms are allowed by the bounded normalized-size hypothesis. The prime-power contribution is negligible by fixing the steps and counting the O_v(√n log n) exceptional x values.

Outside W, the pairwise hyperplane intersections have density p^-2 when p does not divide q. At p dividing q the weaker O(1/p) local error suffices. There are O(v/log v) prime divisors of q above v because log q=O(v). Thus the total remaining factor is 1+O(1/log v). This error is not falsely discarded at fixed v; v grows only after the fixed-v limit.

The ordinary prime majorants dominate the Artin weights, so no Artin-specific polynomial-forms majorant is assumed. The fixed conductor multiplier E_D in W=E_DW₀ is harmless: prime divisors of W are excluded from all sieve divisors, and E_D is invertible at every other prime. It changes only fixed coefficient bounds and constants in the divisor-sum proof.

The two majorant scales solve a genuine compatibility issue. With the source's exponent B>C+2 and ρ*=ρ/B, the coefficient parameter for dense modeling is Acal=A^B. The function supported above n^ρ is dominated by the ordinary weight supported above n^ρ*. Thus the arbitrary-function dense-model theorem applies with all local polynomial coefficients at most Acal.

Its common bounded model controls both required kinds of norms. With a the global norm order, the required progression length is J=floor(A^(-2Ba)M²). The bounds in the source imply

\[
nA^{-2Ba-7}\le J\le nA^{-2Ba},\qquad q\le A^{Ba}.
\]

These are precisely the ranges of Lemma 5.2 with exponents Ba,2Ba,2Ba+7. Concatenation's smallness threshold is independent of Acal. First increasing v and then n is consequently sufficient; there is no circular rate requirement. The local norm polynomials have degree exactly one because d=d₀=2. The generalized von Neumann theorem applies to R_j-R_h, whose leading coefficient is (c_j-c_h)W≠0.

Finally the residue recombination has bounded total normalized admissible mass. Its Euler factor outside the fixed coefficient differences is

\[
\left(\frac p{p-1}\right)^k\frac{(p-1)(p-k+1)}{p^2}=1+O_k(p^{-2}).
\]

This is obtained by counting the admissible u separately at w=0 and w≠0. It prevents the number of residue classes from amplifying a uniform error. The endpoint losses use domination by ordinary prime weights, and T²=o(N). Taking one slow diagonal cutoff across the finitely many required estimates proves the asserted threshold statement. Applying it at N and N/2 with enlarged thresholds gives the interval version.

## Ray fibres and final limits

Source: `P103q.tex:909–1042`.

The Gaussian class number is one. The ray group is (A₀×B)/U with U the four units. Since U injects into A₀, a fixed base class has a unique normalized representative with base residue r. The kernel over the base ray field is the full product B, not B/U. This removes a possible erroneous factor of four.

At an added prime ℓ, the map b↦b/bar(b) maps onto the norm-one subgroup, of size ℓ-χ(ℓ). These subgroups lie in the commutator subgroup of the full Galois group. Quotienting by their product leaves G₀ times the independent norm groups F_ℓ*. Hence the asserted maximal abelian subfield and commutator-group size are correct.

On a nonzero norm fibre s, either order condition fixes the real coordinate a and allows at most two imaginary coordinates. At most four residues are forbidden. The normalized condition is invariant under conjugation and therefore defines an allowed set of rational Artin symbols. The two base classes really differ: equality modulo a unit forces that unit to be 1 modulo 16, which then contradicts the distinct residues modulo 7.

The conditional good-fibre density is bounded below by a fixed positive number times the product of 1-4/(ℓ-1). Raising to k and using Mertens gives (log L)^(-4k). No growing ray-field degree remains as an additional denominator. Keeping all admissible norm residues at the new primes retains the ordinary convergent Euler product. The one retained base residue pair u=b₀,w=0 has fixed positive weight, independent of L.

The final choice fixes L so that C/(L log L) is smaller than c/[32(log L)^(4k)]. This is possible for every fixed k. The field K_L is then fixed. A decreasing sequence of positive constants τ_j and increasing thresholds N_j makes the τ-dependent sieve remainder small relative to τ_jB³, while also meeting the polynomial-counting threshold. Floors lose at most a factor of two. The inequalities in `1033–1040` leave a positive weighted remainder.

Thus no theorem uniform in the degree of K_L, and no quantitative rate in the Artin theorem, is required. The resulting u/w² diverges and all prime values diverge. This completes the checked implication to every conclusion of Theorem 4.1.

## Citation clarification and reproducible checks

| Number used by Sun, from arXiv:1603.07817v1 | Number in the 2018 publication | Published page; extracted text lines |
|---|---|---|
| Theorem 1.4 | Theorem 4 | p.4; `tao-ziegler-published-2018.txt:149–162` |
| Theorem 2.5 | Theorem 9 | p.21; `tao-ziegler-published-2018.txt:945–963` |
| Theorem 3.1 | Theorem 11 | p.28; `tao-ziegler-published-2018.txt:1273–1283` |
| Corollary 3.9 | Corollary 3 | p.38; `tao-ziegler-published-2018.txt:1769–1778` |
| Theorem 4.1 | Theorem 13 | p.41; `tao-ziegler-published-2018.txt:1888–1904` |
| Equation 3.5 | Equation 36 | p.29; `tao-ziegler-published-2018.txt:1322–1335` |
| Equation 4.1 | Equation 57 | p.41; `tao-ziegler-published-2018.txt:1900–1902` |

The publication contains the same applicable statement for each item. The proposed TeX insertion makes the version convention explicit, rather than replacing a valid proof input. The text copy was extracted from the preserved published PDF using pypdf, with a one-based PAGE marker prepended to each page. Mathematical glyphs in extracted PDF text can be imperfect; the preserved PDF and original TeX take precedence.

Run `node check_sun41.cjs` in this directory to reproduce two exact polynomial-identity checks, the norm-fibre and commutator-image counts for all 24 odd primes through 97, and 64 residue checks for the 2-adic orientation. All pass. These checks corroborate the algebra and finite-field arguments; they do not establish the asymptotic theorems. The root audit also records 22 independent quadric/local-count cases in `../common/check_local_counts.json`.

The local good-prime repair closes the identified hypothesis omission. It does not weaken Theorem 4.1, add a theorem assumption, or change any exponent or stated constant dependence. The separate citation correction has no mathematical effect. An independent reproof of all the cited external theorems remains outside this audit's scope.
