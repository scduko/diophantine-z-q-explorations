# Lemma CPO: a proof conditional on one analytic hypothesis

**Status.** This is a proof attempt written in this session and not reviewed by anyone else.
Everything below is proved, or proved to the level of detail of `subsec:o8-pattern-proof`,
**except Hypothesis H (§4)**. H is a Green–Tao–Ziegler (GTZ) count for prime patterns whose
Gaussian factors lie in prescribed residue classes. I believe it is within reach of known
methods, but it is not established here. So the shared-comparison quartic defines Z
**conditionally on H**. The "solution ⇒ integer" direction remains unconditional (NOTE.md §3).

Notation follows `subsec:o8-pattern-proof`. E: y² = x³ − Dx over K = Q(√2), with
D = (3 − √2)². Selected primes p are the values of the m ≤ 41 forms; they are positive,
p ≡ c (mod W) with c = 18484837801 and W = 25878772920 = 4·∏_{q≤29} q, and they satisfy
the paper's value and successor conditions. For such p, the manuscript shows that
Frobenius is a + bi ∈ Z[i] with a² + b² = p, and d_{1,2} = p + 1 ∓ 2a. Since 4 | d_i,
**a is the odd one of the two squares** (if a were even, (a − 1)² + b² ≡ 2 mod 4).

## 1. The statement

**Lemma CPO.** For every integer target tuple **a** and every lower bound there is a prime
pattern as in `subsec:o8-pattern-proof`, together with an orientation of the two places
above each distinct selected prime, such that for all distinct selected p, p′:

* (X1) gcd(d_{p,1}, d_{p′,2}) = 4, and
* (X2) p′ ∤ d_{p,1}.

**Proposition 1 (CRT reduction).** Assume (X1) and (X2), together with the same-prime facts
gcd(d_{p,1}, d_{p,2}) = 4 and p ∤ d_{p,1}d_{p,2}. Then one integer h satisfies
`eq:old41-private-crt` for every selected p at once.

*Proof.* A finite system h ≡ r_i (mod n_i) is solvable iff r_i ≡ r_j (mod gcd(n_i, n_j))
for all i, j. The moduli are d_{p,1} (residue 0), d_{p,2} (residue 4) and
p^{64+v_p(j)} (residue 4). Pairs with equal residues are always compatible. The remaining
pairs are:

* d_{p,1} with d_{p′,2}: needs gcd | 4. For p = p′ this is the manuscript's fact; for
  p ≠ p′ it is (X1).
* d_{p,1} with p′^{e}: needs gcd | 4, i.e. p′ ∤ d_{p,1}. For p = p′ this is the
  manuscript's fact; otherwise it is (X2).

By CRT the solutions form a residue class modulo the lcm, so one can also avoid
h ∈ {0, ±4}. ∎

With this h, the private points of `subsec:o8-common-J-proof` become common to all contacts,
which is exactly the completeness input the shared variant needs (NOTE.md §3).

## 2. Two elementary lemmas

**Lemma 2 (2-adic orientation).** For each selected p, exactly one of d_{p,1}, d_{p,2} is
≡ 4 (mod 8). Orient every prime so that this one is d_{p,2}. Then for all p, p′ the 2-part
of gcd(d_{p,1}, d_{p′,2}) is exactly 4.

*Proof.* p ≡ c ≡ 1 (mod 8) gives d_1 + d_2 = 2(p + 1) ≡ 4 (mod 16), and 4 | d_i.
If both had v₂ ≥ 3, the sum would be ≡ 0 (mod 8). If both had v₂ = 2, write d_i = 4u_i with
u_i odd; then the sum 4(u_1 + u_2) ≡ 0 (mod 8). Both cases are impossible, so exactly one
d_i has v₂ = 2. After the stated orientation, v₂(d_{p,2}) = 2 for every p, so
v₂(gcd(d_{p,1}, d_{p′,2})) = 2. ∎

Call p **ℓ-good** for an odd prime ℓ if ℓ ∤ d_{p,1}d_{p,2} = (p + 1)² − 4a². Call p
**L₀-good** if it is ℓ-good for every odd ℓ ≤ L₀. The condition depends only on the ideal
(a + bi) ⊂ Z[i]: changing the generator by a unit or by conjugation changes a only by a
sign, because a is always the odd coordinate. So it is a condition on the class of
a + bi in (Z[i]/M)^×/⟨i⟩ for M = 4∏_{ℓ≤L₀} ℓ, i.e. on the ray class of the prime above p.

**Lemma 3 (good classes are compatible with every allowed residue).** Let ℓ be an odd
prime and t ∈ F_ℓ. Suppose t is a residue the manuscript's conditions allow for a selected
prime at ℓ (so t ≠ 0, t ≠ −1 when ℓ ≤ L, and t ≡ c when ℓ | W). Then some (a, b) ∈ F_ℓ²
satisfies a² + b² = t and (t + 1)² ≠ 4a².

*Proof.* If ℓ ≥ 7: the conic a² + b² = t (t ≠ 0) has ℓ − (−1/ℓ) ≥ ℓ − 1 ≥ 6 points, and the
excluded values a = ±(t + 1)/2 remove at most 4 of them. If ℓ ∈ {3, 5}: these divide W, and
c ≡ 1 (mod 3) and c ≡ 1 (mod 5); take (a, b) = (0, 1), for which (t + 1)² − 4a² = 4 ≠ 0. ∎

So L₀-goodness is a nonempty Chebotarev-type condition, imposed independently on each
selected prime, that **puts no restriction on the residues of p themselves**. It does not
interfere with any condition in the manuscript. Because of Lemma 2, condition (X1) can now
fail only through odd primes ℓ > L₀ that divide both d_{p,1} and d_{p′,2}.

## 3. Bad events above L₀ and for (X2): unconditional upper bounds

Use the coordinates (x, y, z) and box X·Ω of `subsec:o8-pattern-proof`. There are m forms
Ψ_ν with pairwise independent linear parts, and good patterns are counted without von
Mangoldt weights.

**(B1) Cross events, L₀ < ℓ ≤ X^η.** Fix two distinct forms k ≠ k′ and write
p = Ψ_k = a² + b², p′ = Ψ_{k′} = a′² + b′² (a, a′ odd). Because the linear parts are
independent, (x, y) is an affine function of (p, p′), and integrality is a congruence
condition on (a, b, a′, b′). Every other form becomes an irreducible quadratic polynomial
Q_ν(a, b, a′, b′) = α_ν(a² + b²) + β_ν(a′² + b′²) + γ_ν. The conditions ℓ | (a − 1)² + b²
and ℓ | (a′ + 1)² + b′² are residue conditions modulo ℓ of joint density at most 16/ℓ².

Apply Selberg's upper-bound sieve to (a, b, a′, b′) in a box of side ≍ √X, sifting all m
values by primes below X^{η′}. The level of distribution is supplied by lattice-point
counting, as for `eq:old41-upper`. This gives

  #{patterns with this cross event at ℓ} ≪_{m, **a**} X³ / (ℓ² (log X)^m),

uniformly for ℓ ≤ X^η. The factor X comes from the unused coordinate z.

**(B2) Cross events, ℓ > X^η.** For fixed (a, b), at most 1/η primes ℓ > X^η divide
(a − 1)² + b² ≤ 3X. For each such ℓ, the number of (a′, b′) with ℓ | (a′ + 1)² + b′² is
≪ X/ℓ + √X·X^ε. The total is therefore
≪ X · η⁻¹ · (X^{1−η} + X^{1/2+ε}) · X = o(X³ / (log X)^m).

**(B3) Events (X2).** Since p′ ≥ αX and d_{p,1} ≤ 2βX + 2, any event p′ | d_{p,1} has
d_{p,1} = j p′ with 1 ≤ j ≤ J = O(1). Subtracting (a − 1)² + b² = jΨ_{k′} from
a² + b² = Ψ_k gives 2a − 1 = Ψ_k − jΨ_{k′}. So (x, y) lies on one of the O(√X) lines
Ψ_k − jΨ_{k′} = 2a − 1 with |a| ≤ √X. On each line, Ψ_k is a nonconstant affine function
of the line parameter, because the linear parts are independent. It equals a² + b² for
at most O(√X) parameter values. Altogether there are O(X) choices of (x, y) for each
(k, k′, j), hence O(X²) patterns after including z. This is negligible.

**(B4) Same-prime events, ℓ > L.** These are the manuscript's `eq:old41-bad`, unchanged.

## 4. The analytic input

**Hypothesis H.** Let Ψ_1, …, Ψ_m: Z³ → Z be the affine forms above, let M = 4∏_{ℓ≤L₀} ℓ,
and for each ν let S_ν ⊂ (Z[i]/M)^× be a set stable under multiplication by i and under
conjugation. Put Λ_S(n) = log p if n = p is prime and the generator of a prime of Z[i] above
p lies in S modulo M, and Λ_S(n) = 0 otherwise. Then, in the setting of
`subsec:o8-pattern-proof` (including its residue conditions modulo q ≤ L),

  Σ_{n ∈ Z³ ∩ XΩ} ∏_ν Λ_{S_ν}(Ψ_ν(n)) = (𝔖 · ∏_{ℓ | M} γ_ℓ + o(1)) · vol(Ω) X³.

Here 𝔖 is the manuscript's singular series. The factor γ_ℓ is the probability that each
value lies in its class, assuming the Gaussian classes of the values are independent given
their residues. For L₀-goodness, Lemma 3 gives γ_ℓ ≥ (1 − 4/(ℓ − 1))^m for ℓ ≥ 7 and
γ₃, γ₅ ≥ 2^{−2m}. In particular, the main term is positive.

*How H reduces to a standard-shaped statement.* Expand 1_S over the characters χ of
(Z[i]/M)^×/⟨i⟩. The trivial character and characters of the form φ∘N (Dirichlet
characters) are exactly what GTZ with the W-trick already handles. Each remaining term
involves Λ_χ(n) = Σ_{N(π)=n} χ(π) log n, which satisfies |Λ_χ| ≤ 2Λ and so is majorised
by the GTZ pseudorandom measure. By the generalised von Neumann theorem and the GTZ inverse
theorem, H follows from the non-correlation estimate

  Σ_{π ∈ Z[i] prime, N(π) ≤ N} χ(π) log N(π) · F(g(N(π))Γ) = o(N),

uniformly over nilsequences of bounded complexity. Equivalently, the Gaussian primes,
restricted to a residue class mod M, are orthogonal to the polynomial nilsequences
(x, y) ↦ F(g(x² + y²)Γ) on Z². This is a "Möbius–nilsequence" statement for Z[i] with
polynomial (not linear) phases.

*Literature.* W. Kai, *Linear patterns of prime elements in number fields*
(arXiv:2306.16983) proves the number-field analogue of GTZ, so it must contain an
orthogonality theorem for prime elements of O_K against nilsequences on O_K ≅ Zⁿ. If that
theorem covers filtered polynomial sequences of arbitrary degree and residue-class
restrictions (the Green–Tao MN theorem over Z does), H follows. Green–Sawhney, *Primes of
the form p² + nq²* (arXiv:2410.04189), controls Gowers norms of primes along norm forms
and is also relevant. **I could not read either paper from this environment (arXiv is
blocked), so this applicability is unverified.**

## 5. Proof of Lemma CPO assuming H

Fix **a** and the lower bound. Choose L exactly as in `subsec:o8-pattern-proof`. Then
choose L₀ ≥ L, and impose L₀-goodness on every form, which is possible by Lemma 3. By H,
the number of good patterns in XΩ is

  G ≥ c(**a**, L) · (log L₀)^{−4m} · X³ / (log X)^m

for large X. The factor (log L₀)^{−4m} lower-bounds ∏ γ_ℓ, and c does not depend on L₀.
By (B1)–(B4), the number of these patterns violating (X1), (X2) or the manuscript's own
same-prime conditions is at most

  C(**a**, L) · ( Σ_{ℓ>L₀} ℓ⁻² ) · X³ / (log X)^m + (manuscript bad term) + o(X³ / (log X)^m)
  ≤ (C(**a**, L) / L₀) · X³ / (log X)^m + ….

The upper-bound sieves do not impose goodness, so C is independent of L₀. Since
(log L₀)^{4m}/L₀ → 0, one can choose L₀ so that C/L₀ is less than half of
c·(log L₀)^{−4m}, and then X large. A pattern survives. Orient its primes as in Lemma 2.

For p ≠ p′, the odd part of gcd(d_{p,1}, d_{p′,2}) has no prime ℓ ≤ L₀ (goodness) and none
above L₀ (the survival), and (X2) holds by (B3). Repeated targets reuse the same prime, and
its orientation is forced by Lemma 2. ∎

## 6. Numerical sanity checks (`frobenius_mechanism.py`)

Primes are drawn from the pinned progression p ≡ c (mod W), filtered to be L₀-good,
oriented as in Lemma 2, and tested exactly for (X1) and (X2) in sets of 41.

| L₀ | 30 | 200 | 2000 |
|---|---:|---:|---:|
| compatible 41-prime sets (of 20) | 0 | 3 | 18 |

Without goodness, compatible 41-sets essentially never occur (`cross_prime_experiment.py`).
This matches the proof: goodness removes small ℓ, and the tail Σ_{ℓ>L₀} ℓ⁻² removes the
rest. Lemma 2's assertion was also checked on every sampled prime.

## 7. What a referee should check first

1. **Hypothesis H** (§4): whether Kai's or Green–Sawhney's theorems already give it.
2. **The Selberg-sieve bound (B1)** in the four variables (a, b, a′, b′): uniformity in
   ℓ ≤ X^η and the level of distribution.
3. **Lemma 3 and the claim that goodness is a well-defined ray-class condition** that is
   independent of the orientation and of the sign of Frobenius in the curve's normalisation.
