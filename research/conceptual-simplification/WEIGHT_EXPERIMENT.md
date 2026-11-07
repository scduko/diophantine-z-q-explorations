# Direct high-order weight experiment

The asymmetric Version 10 detector requires only the order-one weight
\(q_1\) and the high-order weight
\[
q_{40}=q_1e^{78}.
\]
The upstream eight-coordinate circuit computes six negative powers,
then an intermediate \(q_{12}\), then \(q_{40}\).

I tested the equally short positive-power circuit
\[
e^2,e^4,e^8,e^{16},e^{32},e^{64},e^{80},
\qquad e^2q_{40}=q_1e^{80}.
\]
The sole quotient denominator is \(e^2\). The unchanged detector norm
equations force \(e\ne0\), so this introduces no new domain obligation.
The equations uniquely give the same \(q_{40}\) in both directions.

The experiment passed the unchanged compiler, precursor reduction
certificate, independent gate checker and complete precursor polynomial
expansion. It has the same 532 active coordinates, 501 compiled residuals
and degree four as upstream, but 34,251 precursor monomials rather than
34,248. It is therefore rejected: it is three monomials worse and offers
no variable saving.

The final nine-coordinate elimination certificate was not applied. It is
specific to the upstream source rows. No 540-variable polynomial is claimed
for this experiment.

Reproduce with:

    python3 -B research/conceptual-simplification/weight_experiment.py \
      --out /tmp/q40-direct

This closes the simplest remove-\(q_{12}\) substitution. A useful next
search must find a seven-coordinate monomial circuit or share a coordinate
with the \(q_1,\delta\), or norm block. Merely changing signs in an
eight-coordinate exponent chain is unlikely to improve the expanded
quartic.
