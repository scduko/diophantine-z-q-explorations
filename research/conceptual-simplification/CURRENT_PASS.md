# Current pass: audit integration and a sharper separation of tasks

Date: 7 November 2026. This pass starts from upstream commit
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6` and the fork's verified
Version 10 integration. It is an AI-assisted research note, not an
independent human mathematical review.

## Upstream comparison

The two upstream commits after Version 10 do not change the finite source,
the 540-variable ordinary polynomial, or the 523-variable symbolic table.
They add an audit-integration protocol and exact historical records for
Issues 2 and 3. In particular, Issue 3 now states the finite test ranges
and serialization conventions that the original checkers used. Those
records improve reproducibility; they do not prove the arithmetic theorem.

The current ordinary baseline therefore remains:

| quantity | value |
| --- | ---: |
| variables, including input | 540 |
| quadratic residuals | 509 |
| monomials | 35,213 |
| maximum coefficient bit length | 3,247 |
| polynomial JSON SHA-256 | `b14e76dda63ea4bb8b012a89a4f052c73e19877b451633df6ee9c198b8d83571` |

## The genuinely short theorem layer

Let \(\Phi=(F_1,\ldots,F_m)\) be the integer quadratic source map whose
rational zero set projects to \(\mathbb Z\). Then

\[
       P=\langle\Phi,\Phi\rangle=\sum_{i=1}^m F_i^2
\]

is a single quartic with the same projection. This is not merely shorthand
for a hidden expansion: it is a complete finite prescription of the
polynomial. Over \(\mathbb Q\), positive definiteness gives
\(P=0\Longleftrightarrow\Phi=0\). A nonzero quadratic leading part gives
degree exactly four, since a sum of rational squares of homogeneous
quadratics cannot cancel identically.

The manuscript's separate degree-obstruction theorem says that no single
polynomial of total degree at most three can have rational projection
exactly \(\mathbb Z\). Subject to that theorem's cited Hilbert
irreducibility and cubic-unirationality inputs, the norm-square construction
is therefore degree-optimal. The expanded table is valuable as a small,
replayable record, but it is not logically required for existence.

This gives a short **presentation** of the result. It does not shorten the
arithmetic source theorem. Any claim of a genuinely shorter proof must
replace at least one of the following interfaces:

1. integer labels inside the elliptic Mordell--Weil group;
2. a finite existential surrogate for testing all denominator primes;
3. the height contradiction that turns local divisibility into equality;
4. the common-witness prime construction used for completeness.

The second and fourth interfaces are the main conceptual bottleneck. A
primitive-divisor argument is useful only if it supplies enough radical
growth **and** separates the shifted denominator needed for the second
observation. Ordinary elliptic Zsigmondy existence alone does neither.

## A restricted optimality result for the remaining weight circuit

The asymmetric source requires only
\(q_{40}=q_1e^{78}\). Upstream computes it with six pure Laurent-power
coordinates and two mixed coordinates:

\[
 e^{-1},e^{-3},e^{-7},e^{-14},e^{-29},e^{-55},
 \quad q_{12}=q_1e^{22},\quad q_{40}=q_1e^{78}.
\]

There is a simple lower bound for circuits that prepare pure powers first
and use one final mixed quotient. If the available pure exponents have
minimum \(m\), maximum \(M\), and diameter \(D=M-m\), one quadratic
monomial quotient adjoins an exponent \(a+b-c\), so the new diameter is at
most \(2D\). Starting from exponents \(0,1\), six pure gates give diameter
at most \(64\). A final relation

\[
 q_{40} e^c=q_1 e^a
\]

can shift the exponent of \(q_1\) by only \(a-c\), whose magnitude is at
most \(64\), not \(78\). Thus a seven-gate circuit of this restricted form
is impossible, and upstream's eight gates are optimal in that class.

This does not exclude seven gates with earlier mixed intermediates or
quadratic relations involving two mixed monomials. The exact positive-power
candidate tested in `weight_experiment.py` remains rejected: it passes the
532-coordinate algebra checker but increases the precursor monomial count
from 34,248 to 34,251 and supplies no variable reduction.

## Verification status

- Exact algebra: the saved weight experiment passes the compiler and
  source checker in its stated 532-coordinate scope.
- Repository bindings: the upstream audit-history checker passes after the
  two documentation commits are integrated.
- Arithmetic proof: the master proposition is a reorganization of the
  Version 10 proof, not an independent re-proof of its inherited estimates.
- Human review: still required for the arithmetic proposition and the
  degree-obstruction theorem's source applications.

The next best conceptual direction is to formulate the precise
primitive-divisor-and-separation lemma that would replace the simultaneous
prime construction, then test each clause against known elliptic divisibility
sequence theorems. The next finite direction is an exhaustive search over
seven-gate mixed Laurent circuits, with every proposed denominator tied to
an existing nonvanishing proof before compilation.
