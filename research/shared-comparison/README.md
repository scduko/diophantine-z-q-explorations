# Shared comparison: a 4,151-variable quartic

**Status: research proposal.** Not accepted upstream, not refereed by a human, and not
formally verified. Base: Version 2, `quartics/quartic-12504/source` (source ID
`reciprocal64-beta16-compressed-s1-b5e836d77643`).

## The change

In Version 2, `Z_definition` calls `q_compare4` once for each of the 41 ordinary contacts.
These calls account for 11,685 of the 12,063 source witnesses (96.9%). They receive
identical arguments except the contact radical r_k, which feeds only the block's norm
batch `q_batch41`.

The variant keeps **one** comparison core (`q_compare4_core`: `q_compare4` without its
batch, exporting its 40 field tests). All 41 contacts share it, and each contact keeps only
its own 58-witness norm batch.

| | Version 2 | Shared variant |
|---|---:|---:|
| source witnesses | 12,063 | **2,983** |
| source residuals | 11,499 | 2,819 |
| quartic variables incl. X, plain quadratic lift | 14,431 | **4,151** |
| quartic monomials, plain quadratic lift | 120,910 | **19,910** |
| quartic variables incl. X, Version 2's optimisation pipeline | 12,504 | not yet run |

The largest absolute coefficient is unchanged, 685783949153203534233601 < 2^80.

The plain lift is a baseline: one product variable per needed pair. The Version 2 pipeline
(norm, chart, ordinate, parity and batch reductions, then optimisation and merging) takes
the pinned source from 14,431 to 12,504 variables. Its tools hard-code the `q_compare4`
layout, so they must be ported before the variant's optimised count is known.

## Why it still defines Z

**Solution ⇒ integer** needs no new argument. `build_shared_source.py` checks exactly
that the variant is the pinned source with every `q_compare4` instance's private witnesses
identified with the first instance's. A rational zero of the variant therefore gives a
rational zero of the pinned source with the same X, and Version 2's theorem applies. The
quadratic lift preserves the X-projection in both directions (`quadratic_lift.py` checks
this exactly).

**Integer ⇒ solution** needs one integer h satisfying `eq:old41-private-crt` at every
selected prime at once. By the Chinese remainder theorem this is **Lemma CPO**: a prime
pattern exists in which, after orientation, gcd(d_{p,1}, d_{p′,2}) = 4 and p′ ∤ d_{p,1}
for all distinct selected primes p, p′.

* Proof: [CPO_PROOF.md](CPO_PROOF.md). Its only external input is the unconditional
  Frei–Tinková theorem (arXiv:2408.17441, Theorem 1.4) on prime patterns with prescribed
  Artin symbols. That theorem's exact hypotheses and local-factor formula (1.15) still
  need to be confirmed against the paper.
* Review: [REVIEW_CPO_PROOF.md](REVIEW_CPO_PROOF.md).

## Experiments (heuristic, not part of the proof)

* `experiments/cross_prime_experiment.py` uses random primes near 10¹² with the pinned
  local conditions. A compatible 41-prime set essentially never occurs. Successes out of
  40 trials:

  | shift c | k=2 | k=3 | k=5 | k=9 | k=20 | k=41 |
  |---:|---:|---:|---:|---:|---:|---:|
  | 4 | 19 | 9 | 1 | 0 | 0 | 0 |
  | 12 | 17 | 7 | 1 | 0 | 0 | 0 |
  | 60 | 33 | 16 | 4 | 0 | 0 | 0 |
  | 16380 | 35 | 33 | 14 | 5 | 0 | 0 |

* `experiments/frobenius_mechanism.py` uses primes p ≡ c (mod W) that are L₀-good
  (ℓ ∤ d_{p,1}d_{p,2} for every odd ℓ ≤ L₀), oriented 2-adically. This is the mechanism
  of the proof:

  | L₀ | 30 | 200 | 2000 |
  |---|---:|---:|---:|
  | compatible 41-prime sets (of 20) | 0 | 3 | 18 |

## Reproduce

From this directory:

```sh
sh check.sh                      # regenerate source/ and quartic/ and compare with the committed files
python3 -I experiments/cross_prime_experiment.py 1 40
python3 -I experiments/frobenius_mechanism.py 2000 20 41
```

## Files

| Path | Contents |
|---|---|
| `build_shared_source.py` | Builds `source/` from the pinned source and runs the two exact equivalence checks. |
| `quadratic_lift.py` | Plain quadratic lift with an exact check; writes `quartic/`. |
| `source/` | Variant modules and flattened residuals (degree 8). |
| `quartic/` | Quadratic residuals, expanded coefficient table, `stats.json` (with SHA-256). |
| `CPO_PROOF.md`, `REVIEW_CPO_PROOF.md` | The completeness proof and its review. |
| `experiments/` | Heuristic numerics. |
| `check.sh` | Reproducibility check. |

## Next steps

1. Check Frei–Tinková Theorem 1.4 and (1.15) against CPO_PROOF.md §§3–5, then get a
   number-theory referee for the whole proof.
2. Port the Version 2 reduction tools to the core-plus-batches layout and replay with
   `verify_certificate.py` to get the optimised count.
3. Write the result up as a replacement for the private-shift paragraph of
   `subsec:o8-common-J-proof`.
4. Read Sun, *86 unknowns for Hilbert's tenth problem over the rationals*
   (arXiv:2610.20691). It builds on the same construction and may define Z far more
   compactly.
