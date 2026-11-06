# Shared comparison: a conditional 4,151-variable quartic

**Status: research proposal. Not accepted, not reviewed, not formally verified.**
The variant below is a mechanically checked restriction of the Version 2 source.
Its "solution ⇒ integer" direction follows from Version 2 with no new mathematics.
Its "integer ⇒ solution" direction depends on one new lemma (§3), which is **open**.

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

### What is known about Lemma CPO

Write Frobenius at p as π = a + bi, so d_{p,1} = N(π − 1) and d_{p,2} = N(π + 1).

* **2-adic part: solved.** p ≡ 1 (mod 8) gives d_{p,1} + d_{p,2} = 2(p+1) ≡ 4 (mod 16).
  So exactly one of d_{p,1}, d_{p,2} is ≡ 4 (mod 8). Choosing it as d_{p,2} for every p
  makes the 2-part of every cross gcd divide 4. This fixes the orientation completely, so
  the odd part has no orientation freedom left.
* **Inert ℓ ≡ 3 (mod 4), ℓ ≥ 7: controllable by a linear condition.** If ℓ | N(π ∓ 1),
  then π ≡ ±1 in the field Z[i]/ℓ, so p = N(π) ≡ 1 (mod ℓ). Adding p ≢ 1 (mod ℓ) to the
  local conditions excludes it. For ℓ = 11, 19, 23 this requires changing the residue
  class c mod ℓ, which appears only in the existence proof, not in the polynomial. The sieve
  density changes from ∏(1 − 2m/q) to ∏(1 − 3m/q).
* **ℓ = 3: not controllable this way.** The conditions p ≢ 0, −1 (mod 3) force p ≡ 1, and
  3 | d_{p,i} then depends on whether π ≡ ±1 or ±i (mod 3).
* **Split ℓ ≡ 1 (mod 4): not controllable this way.** Whether ℓ | N(π − 1) depends on π
  modulo a prime above ℓ, which is not determined by p mod ℓ. Over Q, this is a Chebotarev
  condition in a non-abelian extension (ray class fields of Q(i)).
* **Large ℓ > L: plausibly handled by the existing upper-bound sieve method.** The cross
  event ℓ | d_{p,1}, ℓ | d_{p′,2} has two-fibre density about ℓ⁻². Its contribution
  C_𝐚X³/(L(log X)^m) has the same form as `eq:old41-bad`. This needs a careful write-up.
* **A fixed larger shift does not close the gap.** Replacing 4 by c = 4M (cost: about
  log₂ M point operations per shifted point) absorbs ℓ | M. But L depends on 𝐚, so no
  fixed M covers all small ℓ.

### Numerical evidence (`cross_prime_experiment.py`; heuristic only)

Primes near 10¹² with the pinned local conditions. Each cell counts trials (out of 40) in
which an orientation satisfying (X1) and (X2) exists, solved exactly by 2-SAT.

| shift c | k=2 | k=3 | k=5 | k=9 | k=20 | k=41 |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 30 | 20 | 5 | 0 | 0 | 0 |
| 12 | 30 | 14 | 5 | 0 | 0 | 0 |
| 60 | 35 | 29 | 16 | 0 | 0 | 0 |
| 16380 | 38 | 35 | 26 | 13 | 1 | 0 |

A random 41-prime pattern essentially never satisfies Lemma CPO. That is not a
counterexample: the lemma asks for **some** pattern among infinitely many. If the
Frobenius classes of the selected primes behave independently, the good patterns have
positive (though tiny) relative density, so the lemma is heuristically true. Proving it
seems to need a lower bound for prime patterns with prescribed Frobenius conditions modulo
small primes, which is a Green–Tao–Ziegler theorem with Chebotarev conditions. I don't
know whether a usable version exists in the literature. This is the question to put to
number theorists.

### Partial sharing

Suppose the 41 contacts are split into g groups, each with its own core and with the
group fixed in the polynomial. Cross-prime compatibility is then needed only within each
group. With pairs, a random pair is compatible 75–95% of the time, depending on c. The
cost is roughly ⌈41/g⌉·227 + 41·58 + 303 + 75. Any fixed g ≥ 2 still needs the same kind
of Frobenius control, so partial sharing reduces the cost but not the difficulty.

## 4. Reproduce

```sh
python3 -I build_shared_source.py ../../quartics/quartic-12504/source source
python3 -I naive_lift.py source/residuals.jsonl quartic
python3 -I cross_prime_experiment.py 1 40
```

`quartic/polynomial.expanded.txt` (SHA-256 in `quartic/stats.json`) lists the conditional
quartic in the same format as Version 2's coefficient table.

## 5. Next steps

1. Get number-theory input on Lemma CPO, in particular the small-ℓ Frobenius control.
2. Port the Version 2 reduction tools to the `q_compare4_core` / batch layout and rerun
   `verify_certificate.py`-style replays to get the optimised count.
3. If Lemma CPO is accepted, write it up as a replacement for the private-shift paragraph
   of `subsec:o8-common-J-proof`.
