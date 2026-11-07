# Proposed PR #4 title

Integrate Version 10 and preserve quartic research with a verified 540-variable baseline

# Proposed PR #4 description

## Current baseline

The branch now integrates upstream Version 10 at `ba7a3e0a0c171b7cd2ce75976addba57fad8a5dd`. Its Version 9 construction supersedes our earlier 933-, 924- and 900-variable variants as the smallest ordinary-coefficient research baseline. Those variants and their evidence remain preserved.

The **540-variable ordinary quartic has 509 quadratic residuals and 35,213 monomials**, degree four, primitive content one, and maximum coefficient length 3,247 bits. The accompanying 523-variable table uses a fixed symbolic coefficient. These upstream reductions are credited to Gabriel Conant with ChatGPT; this PR does not present them as new fork discoveries.

## Research contribution and review path

Start with `research/v10-integration-20261107/README.md`. It compares the current baseline with the preserved fork work and records the integration and verification scope. `BLACKBOARD.md` explains why odd indices prevent local height cancellation, why a product permits three detectors instead of nine, and how asymmetric formal depth replaces five logarithm polynomials. It maps every step to the full proof.

Earlier research retains the direct-target argument, exact mixed-weight circuit, parameterized height comparison lemma, elementary Lucas exposition and rejected experiments. A new diameter argument extends the restricted eight-gate lower bound to negative pure powers. It is not a general circuit minimality theorem.

## Fresh verification

- Rebuilt both upstream precursors from the pinned patch composition.
- Replayed each final package twice, including elimination certificates and complete coefficient tables.
- Confirmed pinned inputs were unchanged and decimal downloads match the JSON tables.
- Passed Version 9 dependency bindings, Version 10 document bindings and the bounded valuation regression.
- Replayed the frozen 933-variable package after integration.

The ordinary 540 JSON polynomial hash is `b14e76dda63ea4bb8b012a89a4f052c73e19877b451633df6ee9c198b8d83571`.

```sh
python3 -B scripts/check_odd_product.py --out /tmp/v10-replay
python3 -B docs/quartic-523-540/inventory.py validate
python3 -B docs/manuscript-revisions/version10/check.py
```

## Scope and next direction

No new polynomial smaller than upstream's 540-variable construction is proposed in this checkpoint. The asymmetric source now needs only orders 1 and 40, so further weight optimization should target q40 alone instead of preserving q12 as an output. The current eight-gate fork circuit cannot simply be substituted to save another gate.

Finite algebraic and document checks do not prove the inherited arithmetic characterization of the integers. The odd-product and deeper-common-witness arguments were inspected with AI assistance, not independently human-refereed. The elliptic group, height theorem, prime-pattern input, source-version qualifications and incomplete formalization remain explicit dependencies.

All historical evidence and upstream attribution are preserved. No upstream merge is requested or performed by this checkpoint; this description is saved locally in the fork because upstream metadata writes were previously blocked.
