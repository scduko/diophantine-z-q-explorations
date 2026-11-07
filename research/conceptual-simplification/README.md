# Conceptual simplification program

This directory starts a new research line from upstream Version 10 at
commit 036cebe4f1a4aa7ca89820a9b48f3629b4c364d6. It is deliberately
separate from the preserved combined-comparison pull-request branch.

## Current conclusions

1. The expanded polynomial is unnecessary for a proof of existence.
   A finite quadratic source map \(\Phi\) gives the canonical quartic
   \(P=\|\Phi\|^2\).
2. This yields a genuinely short final theorem proof, but not by itself
   a short proof of the arithmetic source-projection theorem.
3. The main conceptual problem is replacing a universal condition over
   denominator primes by finitely many existential equations.
4. The strongest alternative directions are a primitive-divisor version
   of the common-prime step and a single global defect replacing the
   contact detectors.
5. The simplest direct \(q_{40}\) circuit substitution was checked and
   rejected: it adds three precursor monomials with no variable saving.

Read:

- SHORT_EXISTENTIAL_PROOF.md for the compact theorem architecture;
- CONCEPTUAL_MAP.md for a blackboard explanation of the current proof;
- ALTERNATIVE_ROUTES.md for new proof directions and their obstacles;
- WEIGHT_EXPERIMENT.md for the parallel finite optimization;
- CURRENT_PASS.md for the latest upstream comparison and restricted circuit
  lower bound;
- CONTINUATION.md for repository state and next steps.

All mathematical assessment in this directory is AI-assisted research
and has not received independent human mathematical review.
