# Shared comparison: a conditional 4,151-variable quartic

**Status: research proposal. Not accepted, not reviewed, not formally verified.**
The variant below is a mechanically checked restriction of the Version 2 source.
Its "solution ⇒ integer" direction follows from Version 2 with no new mathematics.
Its "integer ⇒ solution" direction depends on one new lemma (§3). That lemma is now proved
**conditionally on Hypothesis H**, a Green–Tao–Ziegler count for primes with prescribed
Gaussian residue classes: see [LEMMA_CPO.md](LEMMA_CPO.md). H is not proved here.

Base: Version 2, `quartics/quartic-12504/source` (source ID
`reciprocal64-beta16-compressed-s1-b5e836d77643`, 12,063 witnesses, 11,499 residuals).

## 1. Where the size comes from

`Z_definition` calls `q_compare4` once for each of the 41 ordinary contacts
(`eq:o8-contacts`). Each call has 285 witnesses: 227 of its own plus a 58-witness
`q_batch41`. Together the calls make up 11,685 of the 12,063 source witnesses (96.9%).
The 41 calls receive identical arguments except the last one, the contact radical r_k.
Inside `q_compare4`, r is used only as the first argument of its `q_batch41` call.

Everything else in a block depends only on the private multiplier h_p of
`eq:old41-private-crt`. That covers the points H = X_0, X_1..X_4, the charts Y_0..Y_4,
the logarithms, ratios, guards, and the 40 θ-split field tests. The common θ and J are
already shared.

## 2. The variant

Replace the 41 `q_compare4` calls by:

* one `q_compare4_core` call: `q_compare4` without its batch call, exporting its 40 bound
  field tests as outputs; and
* 41 `q_batch41` calls, the k-th with radical r_k, the common `root error` input, and the
  same 40 shared tests.

| | Version 2 | Shared variant |
|---|---:|---:|
| source witnesses | 12,063 | **2,983** |
| source residuals | 11,499 | 2,819 |
| source degree | 8 | 8 |
| plain quadratic lift: variables incl. X | 14,431 | **4,151** |
| plain quadratic lift: monomials | 120,910 | **19,910** |
| Version 2 optimised pipeline: variables incl. X | 12,504 | not yet run |

The "plain quadratic lift" (`naive_lift.py`) is a simple baseline: one product variable per
needed pair. It skips the Version 2 norm, chart, ordinate, parity, batch, optimisation and
merge reductions, which take the pinned source from 14,431 to 12,504 variables. A
comparable pass over the variant would likely land somewhere around 3,500–3,700 variables.
That figure is an estimate, not a computation: the pinned tools hard-code the `q_compare4`
layout and must be ported first.

The largest absolute coefficient is unchanged, 685783949153203534233601 < 2^80.

### Mechanical checks (`build_shared_source.py`, exact arithmetic)

1. The flattener reproduces the pinned `source/residuals.jsonl` row for row.
2. Let σ identify every local witness of the k-th `q_compare4` instance with the
   corresponding witness of the first instance. Then σ(pinned rows), as a set, equals the
   variant's rows under an injective renaming of variables. Every pinned variable is
   accounted for, and X = variable 0 is fixed.

`naive_lift.py` additionally checks exactly that every lifted row expands back to its
source row through the product definitions.

## 3. The argument

### Soundness (P(q, w) = 0 ⇒ q ∈ Z): no new mathematics

Let w′ be a rational zero of the variant. By check 2, setting w_g := w′_{τ⁻¹σ(g)}
defines a rational zero of the pinned source with the same X. Theorem
`thm:quartic-source-arithmetic` then gives X ∈ Z. The quadratic lift preserves the
X-projection in both directions. Hence the projection of the variant's quartic is contained
in Z, assuming exactly the same inputs as Version 2.

### Completeness (X ∈ Z ⇒ a zero exists): needs Lemma CPO

Follow the converse half of the proof of `thm:o8-conditional` unchanged, up to "choose J
and the private points". The only change is that **one** integer h must satisfy
`eq:old41-private-crt` at every distinct selected prime simultaneously:

  h ≡ 0 (mod d_{p,1}),  h ≡ 4 (mod d_{p,2}),  h ≡ 4 (mod p^{64+v_p(j)})  for all p ∈ 𝒫.

By CRT, solvability for every p ∈ 𝒫 is equivalent to pairwise compatibility. The
same-prime case is already proved in Version 2. Since p ∤ d_{p,1}d_{p,2} and
congruences to the same residue are always compatible, the cross-prime case reduces to:

> **Lemma CPO (cross-prime orientation).** For every integer target tuple **a** and every
> lower bound, there is a prime pattern with all properties of
> `subsec:o8-pattern-proof`, together with an orientation of the two places above each
> distinct selected prime, such that for all distinct selected p, p′:
> (X1) gcd(d_{p,1}, d_{p′,2}) divides 4, and (X2) p′ ∤ d_{p,1}.

Given h, put X_0 = [h]P_*, X_i = [h n_i]P_* and Y_i = [(h−4)n_i]P_* once. Each contact
batch then sees exactly the tests that the Version 2 completeness proof supplies at its own
prime. The radical r_k is the single prime p_k, so the batch imposes conditions only at
p_k. The remaining choices (avoiding h ∈ {0, ±4}, nonzero subtraction denominators,
L(z(X_0)) ≠ 0, and choosing θ last) carry over verbatim. **So Lemma CPO implies that the
variant defines Z.**

### Status of Lemma CPO

See [LEMMA_CPO.md](LEMMA_CPO.md). In summary:

* **2-adic part: proved.** Exactly one of d_{p,1}, d_{p,2} is ≡ 4 (mod 8), and this
  forces the orientation.
* **Small odd ℓ ≤ L₀:** handled by requiring each selected prime to be *L₀-good*
  (ℓ ∤ d_{p,1}d_{p,2}). This is a ray-class condition on the Gaussian prime above p. It is
  compatible with every residue condition of the manuscript, including the forced classes
  at 3 and 5 (Lemma 3).
* **Large ℓ > L₀ and (X2):** handled by unconditional upper bounds of the same shape as
  `eq:old41-bad`.
* **The one missing input is Hypothesis H**: GTZ for the manuscript's linear system with
  each prime's Gaussian factor in a prescribed class mod M. It reduces to orthogonality of
  Hecke-character-twisted Gaussian primes to polynomial nilsequences in the norm. It may
  follow from Kai (arXiv:2306.16983) or Green–Sawhney (arXiv:2410.04189); this is
  unverified.

### Numerical evidence (heuristic only)

`cross_prime_experiment.py` uses primes near 10¹² with the pinned local conditions and
solves the orientation constraints exactly. Each cell counts successful trials out of 40.
(The first version of this table used the even square in p = a² + b². The Frobenius trace
is twice the **odd** one; the numbers below are corrected.)

| shift c | k=2 | k=3 | k=5 | k=9 | k=20 | k=41 |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 19 | 9 | 1 | 0 | 0 | 0 |
| 12 | 17 | 7 | 1 | 0 | 0 | 0 |
| 60 | 33 | 16 | 4 | 0 | 0 | 0 |
| 16380 | 35 | 33 | 14 | 5 | 0 | 0 |

A random pattern essentially never works. `frobenius_mechanism.py` draws primes from the
pinned progression, requires them to be L₀-good, and tests 41-prime sets:

| L₀ | 30 | 200 | 2000 |
|---|---:|---:|---:|
| compatible 41-prime sets (of 20) | 0 | 3 | 18 |

This is the behaviour the conditional proof predicts.

### Partial sharing

Suppose the 41 contacts are split into g groups, each with its own core and with the
group fixed in the polynomial. Cross-prime compatibility is then needed only within each
group. With pairs, a random pair is compatible about 45–90% of the time, depending on c. The
cost is roughly ⌈41/g⌉·227 + 41·58 + 303 + 75. Any fixed g ≥ 2 still needs Hypothesis H, so partial sharing only reduces the cost.

## 4. Reproduce

```sh
python3 -I build_shared_source.py ../../quartics/quartic-12504/source source
python3 -I naive_lift.py source/residuals.jsonl quartic
python3 -I cross_prime_experiment.py 1 40
python3 -I frobenius_mechanism.py 2000 20 41
```

`quartic/polynomial.expanded.txt` (SHA-256 in `quartic/stats.json`) lists the conditional
quartic in the same format as Version 2's coefficient table.

## 5. Next steps

1. Get number-theory review of [LEMMA_CPO.md](LEMMA_CPO.md), above all Hypothesis H and
   the sieve bound (B1).
2. Port the Version 2 reduction tools to the `q_compare4_core` / batch layout and rerun
   `verify_certificate.py`-style replays to get the optimised count.
3. If H and Lemma CPO are accepted, write them up as a replacement for the private-shift paragraph
   of `subsec:o8-common-J-proof`.
