# Conceptual-simplification checkpoint

## Later integration pass on 7 November 2026

The conceptual work was subsequently integrated into the refreshed
combined-comparison research line. Upstream through `036cebe4` was merged;
its two post-Version-10 commits add audit provenance and exact finite-case
documentation, while leaving the 540/509/35,213 polynomial baseline
unchanged.

`CURRENT_PASS.md` records a new restricted lower bound: seven gates are
impossible when pure Laurent powers are prepared first and one final mixed
quotient must produce `q40=q1*e^78`. Six pure gates have exponent diameter
at most 64. This does not establish unrestricted eight-gate optimality for
circuits with earlier mixed intermediates.

7 November 2026. The fork main branch was fast-forwarded from
fef5fb2d7fc73798aeaca1017a3b3453253e1380 to upstream
036cebe4f1a4aa7ca89820a9b48f3629b4c364d6. The existing
combined-comparison branch and upstream PR #4 were left untouched at
4145131edb579440607cdeb1c3b0de5cee2fe19d. No further work is being
added to that pull. This work begins from a clean upstream baseline on
the separate conceptual-simplification branch.

The two new upstream commits add audit-history evidence and Issue 3
serialization documentation. They do not change the 523/540 polynomial
data. AGENTS.md and CONTRIBUTING.md were read. This research does not
reclassify a historical audit item.

## Main conclusion

A very short proof of the final existential theorem is already available
at the correct abstraction level: specify the finite quadratic source and
take the sum of squares of its rows. The expanded polynomial is unnecessary
for the proof, and the sum of squares is a canonical degree-four choice.

This does not shorten the arithmetic master proposition. The core
complexity comes from replacing a universal condition over denominator
primes by finitely many existential equations. The current mechanism is
elliptic labels, contact radicals, a height contradiction, Lucas
amplification and a simultaneous common witness.

SHORT_EXISTENTIAL_PROOF.md gives the compact theorem proof;
CONCEPTUAL_MAP.md explains the six moves; ALTERNATIVE_ROUTES.md evaluates
possible replacements without treating hidden assumptions as simplifications.

## Best next directions

The most promising different route is to replace simultaneous contact
primes by primitive divisors of one elliptic divisibility sequence. It
needs a uniform radical-height and prime-separation lemma, not merely a
primitive-divisor theorem.

The second target is a single global defect on a fiber product of the
label and comparison varieties. The high-confidence expository project
is a short paper that proves one master proposition and relegates expansion
and certificates to a supplement.

## Parallel finite experiment

The asymmetric source needs only \(q_1\) and \(q_{40}=q_1e^{78}\).
A direct positive-power circuit was compiled and replayed against the
532-coordinate precursor. It passed exact algebraic checks and has the
same 532 active coordinates, 501 compiled residuals and degree four.
It has 34,251 precursor monomials, three more than upstream's 34,248,
so it is rejected. The final source-specific nine-coordinate elimination
was not reused and no new 540-variable polynomial is claimed.

Further finite work should search for a seven-coordinate mixed circuit
or share a coordinate with the \(q_1,\delta\), or norm block. Replacing
the signed chain by an equally long positive chain is now recorded as
unproductive.

No independent human review is claimed. No pull request, upstream message,
merge or metadata edit was made from this branch.
