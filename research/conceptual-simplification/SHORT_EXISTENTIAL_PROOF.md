# A short existential presentation of the theorem

Status: proof architecture based on Version 10 at commit
036cebe4f1a4aa7ca89820a9b48f3629b4c364d6. This note separates a
short presentation of the theorem from a shorter proof of its arithmetic
engine. The former is available now; the latter would require new ideas.
The analysis is AI-assisted and has not received independent human review.

## The right notion of explicitness

An expanded coefficient table is evidence, not the mathematical idea.
For a Diophantine definition it is enough to specify a finite list of
polynomial equations. Over the rationals, a finite conjunction

\[
 F_1(X,\mathbf Y)=\cdots=F_m(X,\mathbf Y)=0
\]

is equivalent to the single equation

\[
 P(X,\mathbf Y):=\sum_{j=1}^m F_j(X,\mathbf Y)^2=0.
\]

This uses only that \(\mathbb Q\) is formally real. If every \(F_j\)
is quadratic, then \(P\) is a quartic. Nonzero conditions introduce
inverse witnesses through \(UV-1=0\); rational operations introduce
one output variable and a quadratic graph equation. Thus a finite
rational straight-line construction automatically gives one quartic.

This is arguably the most elegant polynomial attached to the proof:
it is the squared norm of the vector of source equations. Expanding it
is useful for reproducibility and size records, but irrelevant to the
logical implication.

## A master arithmetic proposition

The current proof can be organized around the following proposition.
It repackages the Version 9/10 arithmetic source rather than supplying
a new independent theorem.

**Master proposition.** There is a finite system
\(\mathcal S(X,\mathbf Y)=0\) of rational quadratic equations, specified
by the following fixed data, whose rational projection to \(X\) is
exactly \(\mathbb Z\):

1. the curve
   \[
   E:y^2=x^3-(11-6\sqrt2)x
   \]
   over \(K=\mathbb Q(\sqrt2)\), with the fixed point \(P\) for which
   \(2E(K)=\mathbb ZP\);
2. four odd elliptic labels \(n,a,t,b\), with \(n=2X^2+3\) forced
   locally and
   \[
   t^2-a(a-2)tb+(a-2)^2b^2=1;
   \]
3. the scalar-height anchor on \((a-1)P\);
4. three contact detectors attached to the product of the four
   abscissae;
5. two local observations of every label, using a common index \(h\)
   and the shifts \(h\) and \(h-1\).

Every rational operation and domain condition is replaced by its
quadratic graph.

- **Soundness.** Contact divisibility and the exponent-19 height bound
  force the Lucas residual to vanish. Lucas growth then conflicts with
  the scalar height bound unless \(n=2X^2+3\). Hence \(X\in\mathbb Z\).
- **Completeness.** For \(X\in\mathbb Z\), choose odd Lucas labels,
  the scalar anchor and three product-height scales. The simultaneous
  prime argument and its separation refinement provide one common index
  meeting the primary, opposite, continuity and real conditions.

The deep content is all in this proposition. Its map to the current
manuscript is given in CONCEPTUAL_MAP.md.

## The short proof

**Theorem.** The ordinary integers are Diophantine over the rationals.
Indeed, they are the projection of the zero set of an integer quartic.

**Proof.** Take the finite quadratic system of the master proposition
and clear the fixed rational denominators in each row, obtaining integer
quadratics \(F_1,\ldots,F_m\). Put
\[
 P=F_1^2+\cdots+F_m^2.
\]
For rational arguments, \(P=0\) if and only if every \(F_j=0\).
The master proposition therefore gives
\[
 X\in\mathbb Z
 \quad\Longleftrightarrow\quad
 \exists\mathbf Y\in\mathbb Q^N\;P(X,\mathbf Y)=0.
\]
The degree is at most four, and is exactly four after retaining a
genuinely quadratic source row. \(\square\)

This proof does not need the expanded 540-variable table, its monomial
count, or an elimination certificate. Those objects establish a sharper
finite record: a particular small polynomial, not the existential theorem.

## The honest limitation

Calling the preceding paragraph a new short proof of the whole result
would be misleading: the master proposition contains the hard arithmetic.
A compact paper could prove it through a small number of named lemmas and
omit all expanded coefficients, historical inventories and optimization
details. A fully self-contained proof still has to establish the elliptic
Mordell--Weil calculation, contact-to-height theorem, simultaneous-prime
construction, local comparison, scalar anchor and Lucas contradiction.

The shortest honest paper should separate its theorem layer, arithmetic
engine and reproducibility supplement.

## Why the sum of squares is conceptually hard to improve

A field norm can also package several equations, but its degree grows with
the extension degree. The sum of squares packages arbitrarily many
quadratic equations into degree four because \(\mathbb Q\) has no
nontrivial zero of a positive definite rational quadratic form. Since the
manuscript separately proves that a single defining polynomial cannot have
degree below four, this already has optimal degree.

One may write it compactly as
\[
 P(X,\mathbf Y)=\|\Phi(X,\mathbf Y)\|^2,
\]
where \(\Phi\) is the quadratic source map. Further elegance must come
from simplifying \(\Phi\), not expanding or cosmetically refactoring \(P\).
