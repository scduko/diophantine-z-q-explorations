# Opening the finite-contact black box

7 November 2026. This note turns the finite-contact lemma in
`PROOF_FROM_THE_BOOK.md` into five propositions. It is an exposition plan,
not an independent verification of the arithmetic proposal. Labels refer to
`manuscripts/quartic_v10.tex` at upstream commit
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6`.

The test of a good decomposition is that each proposition has one job, its
hypotheses are visible, and the two-gap proof uses only their conclusions.

## Proposition A: the integer carrier

There is a fixed elliptic curve $E/K$, $K=\mathbb Q(\sqrt2)$, and a point
$P$ such that

\[
                         2E(K)=\mathbb ZP.
\]

A finite quadratic chart selects four odd multiples

\[
 [n]P,\quad[a]P,\quad[t]P,\quad[b]P,
\]

and $b\ne0$. For odd labels, the product of their abscissae has exactly the
sum of their heights. Consequently three fixed rational-square scales control
all four label heights.

**Where it currently lives.** The group calculation and index-height bound
are listed in `subsec:v9-inputs`; the exact odd chart is
`v9:prop:odd-chart`; height additivity is `v9:lem:product`; the three-scale
consequence is `v9:cor:scales`.

**Proof burden.** Verify the Mordell--Weil calculation, the squareclass
description of the odd coset, and the local-sign argument behind exact
height additivity. No prime-pattern theorem is used here.

## Proposition B: finite contacts imply local congruences

For each of the three rational-square scales, one finite detector can force
one $K$-place at which all sixteen comparison tests have their assigned
depths. At such a place the elliptic formal logarithm gives

\[
 L_i\equiv n_i\pmod {\mathfrak p^{40}}
\]

for the Lucas labels, and the analogous order-$12$ input comparison. Hence
the corresponding contact radical to the fortieth power divides every
nonzero Lucas defect, while its twelfth power divides the numerator of every
nonzero input-label defect.

**Where it currently lives.** The pole obstruction and realization inputs
are `hyp:o8-pole`, `lem:original-seven-simultaneous-realization` and
`lem:v5-one-place`. Direct targets are treated in `lem:v9-bridge`; the final
formal-depth calculation is `subsec:v9-local-depth`.

**Proof burden.** State the permitted zero branches and every denominator
guard. Prove the one-place selection before applying logarithms. Separate
the pole obstruction used for soundness from its restricted converse used
for completeness.

## Proposition C: contact height transfer

There is an explicit constant $\mathcal H$ such that, whenever the $k$th
powers of the three selected contact radicals divide a nonzero integer $N$,

\[
                 B^2-6<7\mathcal H|N|^{19/k},           \tag{H}
\]

where $B$ is the largest absolute root label. In particular:

- with $N$ equal to the Lucas defect and $k=40$, the elementary bound
  $|N|<5B^4$ gives $B^{1/10}<24\mathcal H$;
- with $N=\lvert\operatorname{num}(n-\beta)\rvert$ and $k=12$, the bound
  $N\le2e^{h(\beta)}B$ gives
  \[
  \log B<\frac{12}{5}\log(40\mathcal H)
             +\frac{19}{5}h(\beta).
  \]

**Where it currently lives.** The exponent-$19$ theorem is
`thm:quartic-height19`; its translation is `lem:v5-height-transfer`; the
three-scale form (H) is `v9:eq:height-transfer`; the substitutions are in
`subsec:v9-soundness`.

**Proof burden.** This is the quantitative core of soundness. The constants,
height normalization and exponent must be replayed from the theorem actually
proved, rather than inferred from an earlier exponent-$24$ version.

## Proposition D: the anchor

The scalar block and one physical anchor force

\[
 |a|>(40\mathcal H)^{10},\qquad
 h(\beta)<|a|/40,\qquad
 \log(40\mathcal H)<|a|/40,                             \tag{A}
\]

where $\beta=2X^2+3$. For completeness, the scalar label may be chosen
positive, arbitrarily divisible, and congruent to $1$ modulo $6$ after the
shift used in the root chart.

**Where it currently lives.** `lem:v9-bridge` supplies the shifted scalar
statement; the explicit comparison with the fixed anchor is in
`subsec:v9-soundness`; the choice order is in `subsec:v9-completeness`.

**Proof burden.** Keep the shift $S-P=[a-1]P$ visible. The scalar estimate is
about $a-1$, while the Lucas equation is about $a$; the displayed constants
are what bridge them.

## Proposition E: simultaneous realization

For each integral input, after the four labels, three scales and continuity
modulus have been fixed, there are contact primes and one common elliptic
index realizing all source equations, all guards, all local depths, the
scalar block and the real anchor.

**Where it currently lives.** The analytic input is
`thm:v5-simultaneous-primes`; reduced-order compatibility is strengthened by
`v9:lem:separation`; the final CRT and formal-depth construction is
`subsec:v9-deep-completeness`.

**Proof burden.** Preserve the quantifier order:

1. fix the integral input and root labels;
2. fix scales and the small-prime continuity modulus;
3. choose the simultaneous primes beyond all fixed exceptional data;
4. solve the compatible index congruences;
5. choose a sufficiently large representative for the real conditions.

This is where the prime-pattern theorem is indispensable in the current
approach. Soundness does not use it.

## The assembly

Propositions A--D give clauses 1--3 of the finite-contact lemma. Proposition
E gives clause 4. The elementary amplifier then finishes the proof exactly
as follows:

1. (A) contradicts Proposition C unless the Lucas defect is zero.
2. The amplifier gives $\log B>|a|-3$.
3. (A) and the second consequence of Proposition C give
   $\log B<(31/200)|a|<|a|-3$ unless $n=\beta$.
4. Thus $n=\beta\in\mathbb Z$, and the reduced denominator of
   $\beta=2X^2+3$ forces $X\in\mathbb Z$.
5. Proposition E proves the converse; quadratic graphing and a sum of
   squares give one quartic.

This decomposition is not merely a rename of the full manuscript. It
separates the proof into an algebraic carrier, a local detector, one height
transfer, one anchor and one global realization theorem. It also locates the
main independent-review priorities: Proposition C for soundness and
Proposition E for completeness.
