# Review of CPO_PROOF.md

**Reviewer:** Claude (AI), in the session that produced the shared-comparison variant.
This is a careful read, not an independent human referee report.

## Verdict

The argument is correct as far as I can check without reading the external theorem. It
replaces the earlier conditional write-up (an unproved "Hypothesis H", in this branch's
history) with an unconditional published theorem,
**Frei–Tinková, *Linear constellations in primes with arithmetic restrictions*,
arXiv:2408.17441, Theorem 1.4** (GTZ asymptotics with prescribed Artin symbols in fixed
Galois extensions). A web search confirms that the paper exists and that its Artin-symbol
result is unconditional. It is also cited as Theorem 1.4 by later work. I could not open
the paper, because arXiv is blocked from this environment.

## Checked steps

* **§4, Lemma 4.1 (abelian part of the ray class field).**
  * The isomorphism (Z[i]/2R)^×/⟨i⟩ ≅ (Z[i]/R)^×/{±1} is right: (Z[i]/(2))^× = {1, i} is
    the image of the units, with kernel {±1}.
  * The commutator subgroup of A ⋊ ⟨σ⟩ is {u/ū}, the norm-one elements (Hilbert 90
    modulo each ℓ), and it contains −1 = i/(−i).
  * So G^ab ≅ (Z/R)^× × C₂, which matches [Q(i, ζ_R) : Q]. Correct.
* **§5, goodness.**
  * Goodness is invariant under sign and conjugation, so it is a union of conjugacy
    classes.
  * The fibre bounds g_ℓ ≥ 1 − 4/(ℓ − 1) and g₃(1) = g₅(1) = 1/2 are correct.
    Enumeration mod 3: the norm-1 classes are (±1, 0) and (0, ±1); only (0, ±1) is good.
  * The point that densities must be **conditional on the abelian (norm) data** is
    right. My Hypothesis H glossed over this.
* **§7, medium primes.**
  * The substitution z = ε + αu leaves every local density at q ≠ ℓ unchanged.
  * Box-counting remainders are O((T/d + 1)³), independent of the coefficients, so the
    sieve constant is independent of ℓ and of L₀. That is the uniformity my sketch lacked.
  * The densities give sieve dimension m: two norm forms at (1 + χ₋₄(q))/q and m − 2
    rank-4 mixed quadratics at 1/q.
  * The error T³Z^{2+o(1)} is negligible because T ≫ X^{9/20} and Z = X^{1/100}.
* **§8, large primes.** The lattice count without primality gives O(X²/ℓ²) for each ℓ,
  and summing over ℓ > X^{1/10} gives O(X^{2−η}). Correct, and simpler than my divisor
  argument.
* **§9, same-prime collisions.** These are re-proved directly using a = ℓr,
  b = b₀ + ℓs. So the manuscript's L-dependent same-prime argument is not needed for the
  new family.
* **§10, (X2).** z determines both p and p′, hence n, which gives O(X) points. Correct,
  and simpler than my line-counting.
* **§12, orientation and CRT.** These agree with my Lemma 2 and Proposition 1.

## Points to confirm against the source

1. **[FT] Theorem 1.4, its hypotheses, and the local-factor formula (1.15).** Confirm that
   it applies to affine forms Z² → Z (plus the unused z) with pairwise independent linear
   parts, restricted to residue classes modulo a fixed modulus. Confirm also that its
   leading constant is the ordinary singular series times the conditional class densities
   used in (5.3)–(5.5).
2. **"Constant independent of L₀" in (5.5).** This follows from the product form of the
   local factors and the uniform fibre bound (5.4). It should be stated explicitly as a
   consequence of (1.15).
3. **Inputs from the manuscript.** Admissibility, the positivity cone, and the
   progression p ≡ c (mod W) are taken from `subsec:o8-pattern-proof`. The new proof
   replaces that subsection's sieve for this family, and it no longer needs the
   L-dependent successor conditions.

## Consequence

If item 1 checks out, the shared-comparison variant (2,983 source witnesses; 4,151
variables after a plain quadratic lift, against 12,504) defines Z in Q under exactly the
same arithmetic inputs as Version 2, with no new hypothesis.
