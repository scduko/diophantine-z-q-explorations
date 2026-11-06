# Shared comparison: a 4,151-variable quartic

**Status: proposal.** Not accepted by the Version 2 authors, not refereed by a human, and
not formally verified. This proposes a **size reduction**, not a correction: nothing here
asserts an error in Version 2, and no existing file is modified.

**Base.** Version 2 at commit `28e87b1b62af0effd954605af7f70b2699dd5672`, source
`quartics/quartic-12504/source` (ID `reciprocal64-beta16-compressed-s1-b5e836d77643`,
`residuals.jsonl` SHA-256 `b5e836d7764363fcbfdafbacefe80a5f53e0979eba73af990827942b0fa9351d`).
The pinned input hashes in [SHA256SUMS](SHA256SUMS) agree with
`quartics/quartic-12504/source-entry.json`. [PROPOSAL.json](PROPOSAL.json) is the
machine-readable record of this proposal.

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

* Current proof: [CPO_PROOF_V2.md](CPO_PROOF_V2.md), with expanded conditional-density
  and uniform sieve calculations. Its external prime-pattern input is the unconditional
  Frei–Tinková theorem (arXiv:2408.17441v3, Theorem 1.4).
* [SHARED_COMPLETENESS.md](SHARED_COMPLETENESS.md) constructs the common points,
  chart witnesses and root approximation, and explains why each contact retains its
  own norm-batch witnesses. The precision is chosen after the primes and auxiliary
  index j, before applying CRT for h.
* [Follow-up verification](VERIFICATION_2026-11-06.md) checks the theorem's hypotheses
  and local-factor normalization against the full paper. This is AI author self-review,
  not independent mathematical review.
* Historical records: [CPO_PROOF.md](CPO_PROOF.md) and
  [REVIEW_CPO_PROOF.md](REVIEW_CPO_PROOF.md), preserved unchanged.

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

From the repository root (Python 3, standard library only; tested with CPython 3.13.18 on
Linux):

```sh
sh research/shared-comparison/check.sh
python3 -I -B research/shared-comparison/experiments/cross_prime_experiment.py 1 40
python3 -I -B research/shared-comparison/experiments/frobenius_mechanism.py 2000 20 41
```

`check.sh` verifies the pinned Version 2 inputs and this directory's scripts and outputs
against [SHA256SUMS](SHA256SUMS). It then regenerates `source/` and `quartic/`, rerunning
both exact equivalence checks, and compares them byte for byte with the committed files.
The scripts refuse to run under `python -O`, because their checks are assertions.

**How the result was found and how it was checked.** The construction was designed by hand
from the module structure; there was no search. It is checked by exact rational arithmetic
in `build_shared_source.py` and `quadratic_lift.py`. Neither the Version 2 certificate
checker (`verify_certificate.py`) nor its source auditor has been run on the variant. Both
are hard-wired to the Version 2 module layout.

## AI contribution and verification

* **Claude Code (Anthropic):**
  * the cost analysis and the shared-comparison construction;
  * every script and experiment in this directory;
  * the problem statement for Lemma CPO, and an earlier conditional proof (superseded; in
    the branch history);
  * the review in [REVIEW_CPO_PROOF.md](REVIEW_CPO_PROOF.md). That reviewer is not
    independent of the proposal.
* **An external AI reasoning model**, supplied by the repository owner, wrote
  [CPO_PROOF.md](CPO_PROOF.md). It is preserved verbatim apart from math delimiters; see
  its provenance header.
* **Subsequent AI author self-review:** the revised proof, completeness bridge,
  source-application record, and strengthened product-definition checks. This review
  is not independent of the original CPO proof.
* **Verification performed:**
  * exact algebraic checks, reproducible with `check.sh`;
  * a step-by-step AI read of the proof;
  * a direct check of Frei–Tinková Theorem 1.4 and its local-factor formula;
  * an independent expansion of the committed quadratic residuals;
  * heuristic numerics.
* **Not performed:**
  * human refereeing;
  * a Version 2 certificate replay of the variant;
  * Lean formalisation.

## Files

| Path | Contents |
|---|---|
| `build_shared_source.py` | Builds `source/` from the pinned source and runs the two exact equivalence checks. |
| `quadratic_lift.py` | Plain quadratic lift with an exact check; writes `quartic/`. |
| `source/` | Variant modules and flattened residuals (degree 8). |
| `quartic/` | Quadratic residuals, expanded coefficient table, `stats.json` (with SHA-256). |
| `CPO_PROOF_V2.md`, `SHARED_COMPLETENESS.md` | Current CPO proof and its application to the shared circuit. |
| `VERIFICATION_2026-11-06.md` | Follow-up source check, checker explanation, and verification scope. |
| `CPO_PROOF.md`, `REVIEW_CPO_PROOF.md` | Preserved original proof and earlier review. |
| `experiments/` | Heuristic numerics. |
| `check.sh` | Reproducibility check. |
| `PROPOSAL.json` | Machine-readable record: base, change, counts, checks, inputs, AI contribution, what is not claimed. |
| `SHA256SUMS` | Hashes of the pinned inputs, scripts, the proof and all generated files. |
| `.gitattributes` | Marks this directory `-text`, so byte comparisons survive any checkout. |

## Next steps

1. Obtain independent number-theory review of the revised proof and its completeness
   bridge, especially the uniform estimates in §§5–9.
2. Port the Version 2 reduction tools to the core-plus-batches layout and replay with
   `verify_certificate.py` to get the optimised count.
3. After review, integrate `SHARED_COMPLETENESS.md` into the manuscript's private-shift
   and reciprocal-comparison completeness arguments.
4. Read Sun, *86 unknowns for Hilbert's tenth problem over the rationals*
   (arXiv:2610.20691). It builds on the same construction and may define Z far more
   compactly.
