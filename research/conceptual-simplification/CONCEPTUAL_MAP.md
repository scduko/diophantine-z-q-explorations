# The proof on a blackboard

This map identifies where a genuinely shorter proof would have to change
the mathematics.

## Six moves

### 1. Obtain integers without quantifying over integers

The fixed elliptic curve has
\[
2E(\mathbb Q(\sqrt2))=\mathbb ZP.
\]
Thus every rationally quantified nonidentity point in \(2E(K)\) has a
hidden integer label. The equations quantify coordinates; the group
theorem supplies the integer.

### 2. Compare the input with a hidden label

Set \(\beta=2X^2+3\). If \(\beta\) equals a label \(n\), then a
reduced-fraction argument forces \(X\in\mathbb Z\). Two observations at
a good prime compare
\[
\frac{u}{h},\qquad \frac{u-n}{h-1}.
\]
If both are congruent to one local approximation \(L\), subtraction
gives \(L\equiv n\). One of the consecutive denominators is a unit.

### 3. Turn contacts into many local tests

A detector makes every sufficiently large prime occurring oddly in a
fixed contact product enforce a comparison. Three scales control the
height of the product of four odd elliptic abscissae. Oddness prevents
local cancellation, so the product height is the sum of the four heights.

### 4. Convert divisibility into equality

If a nonzero defect \(N\) is divisible by the \(k\)th powers of all
contact radicals, the height theorem gives schematically
\[
B^2\ll H|N|^{19/k}.
\]
For the degree-four Lucas residual, \(k=40\) makes the exponent on \(B\)
strictly smaller than two. The anchor makes \(B\) too large, so the
residual vanishes.

### 5. Amplify the remaining equality

The Lucas equation forces
\[
\log B>|a|-3.
\]
The scalar block keeps \(h(\beta)\) sublinear in \(|a|\). A second
height comparison then contradicts Lucas growth unless \(\beta=n\).

### 6. Construct one common witness

For an integral input, the proof fixes labels and scales, selects a
simultaneous pattern of contact primes, and solves compatible congruences
for one index \(h\). A separation lemma permits extra primary depth;
continuity preserves scalar conditions; a real-progression argument
avoids poles.

## Source map

| Blackboard step | Version 9/10 source |
| --- | --- |
| Hidden labels | subsec:v9-inputs and inherited point-source lemmas |
| Two observations | lem:v9-bridge |
| Odd product and three scales | v9:lem:product and v9:cor:scales |
| Odd-label chart | v9:prop:odd-chart |
| First contradiction | subsec:v9-soundness |
| Lucas amplification | lem:o8-lucas and v9:sec:labels |
| Asymmetric depth | subsec:v9-local-depth |
| Prime separation | v9:lem:separation |
| Common witness | subsec:v9-deep-completeness |
| Single quartic | subsec:v9-finite |

## The bottleneck

For a nonintegral rational number, some prime sees its denominator.
An existential formula cannot say “for every prime.” It must arrange a
finite witness whose algebraic consequences expose enough primes to make
a nonzero defect impossible. The current proof uses contact radicals and
height. A new short proof needs another finite existential substitute for
that missing universal quantifier. A prettier final polynomial does not
address this bottleneck.
