# A proof-from-the-book architecture

7 November 2026. This is a conceptual reorganization of the verified
Version 9/10 argument at upstream
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6`. It is AI-assisted and has
not received independent human mathematical review. The purpose is to
expose the shortest honest proof, not to claim that the deep arithmetic
inputs have become elementary.

## The target theorem in one sentence

The proposal aims to construct a finite quadratic map
$\Phi(X,\mathbf Y)$ over $\mathbb Q$ such
that

\[
 X\in\mathbb Z
 \quad\Longleftrightarrow\quad
 \Phi(X,\mathbf Y)=0\text{ for some }\mathbf Y\in\mathbb Q^N.
\]

Once the arithmetic projection claim is fully verified,

\[
             P(X,\mathbf Y)=\|\Phi(X,\mathbf Y)\|^2
\]

is a quartic defining the integers over the rationals. The expanded
polynomial is a certificate of size, not part of the proof.

The arithmetic reason such a map exists is a two-gap argument. A norm-one
equation makes one hidden integer label exponentially large. Finite local
contacts make every possible nonzero error grow only polynomially, first
for the norm equation and then for the input comparison. Exponential and
polynomial growth cannot coexist.

## 1. Integer labels from one elliptic curve

Fix $K=\mathbb Q(\sqrt2)$ and the curve and point used in the source. The
Mordell--Weil calculation gives

\[
                   2E(K)=\mathbb ZP.
\]

Thus a rationally quantified point of $2E(K)$ carries a unique hidden
integer label. The formula never quantifies over the integers: it
quantifies the point coordinates, and the group theorem supplies the
integer.

Write four labelled points as

\[
 A=[n]P,qquad S=[a]P,qquad T=[t]P,qquad Z=[b]P.
\]

For the rational input $X$, put

\[
                         \beta=2X^2+3.
\]

If a local comparison eventually proves $n=\beta$, then $X$ is integral:
writing $X=u/v$ in lowest terms shows $v^2\mid2$, and hence $v=1$.

## 2. The elementary amplifier

The conceptual heart is the following Pell--Lucas observation.

**Amplifier lemma.** Let $a,t,b\in\mathbb Z$, $|a|\ge7$, and $b\ne0$.
If

\[
        t^2-a(a-2)tb+(a-2)^2b^2=1,                       \tag{1}
\]

then

\[
                         \log|t|>|a|-3.                  \tag{2}
\]

Conversely, each such $a$ admits positive integral $t,b$ satisfying (1).
If $a>0$ and $a\equiv1\pmod6$, they may be chosen odd as required by the
completeness argument.

**Proof.** Write $A=|a|$, put

\[
 w=\operatorname {sgn}(a)(a-2)b,
 \qquad \rho=\frac{A+\sqrt{A^2-4}}2.
\]

Equation (1) is the norm-one equation

\[
                         t^2-Atw+w^2=1.                 \tag{N}
\]

Every positive norm-one unit of $\mathbb Z[\rho]$ is a power of $\rho$.
Here is the short proof. Multiply such a unit by a power of $\rho$ until
it lies in $[1,\rho)$. Write the result as $v=C+D\rho$. Then

\[
 D=\frac{v-v^{-1}}{\rho-\rho^{-1}}\in[0,1)\cap\mathbb Z,
\]

so $D=0$ and $v=1$. Thus the integral solutions of (7) are described by
the Lucas sequence

\[
 U_0=0,qquad U_1=1,qquad U_{k+1}=|a|U_k-U_{k-1}.
\]

Namely, $|w|=U_k$ and $|t|\in\{U_{k-1},U_{k+1}\}$ for some $k\ge1$.
The recurrence gives the two congruences

\[
 U_k\equiv k\pmod {A-2},\qquad
 U_k\equiv(-1)^{k-1}k\pmod {A+2}.                       \tag{C}
\]

If $a>0$, then $A-2=|a-2|$ divides $w$, and (C) gives $k\ge A-2$.
If $a<0$, then $A+2=|a-2|$ divides $w$, and (C) gives $k\ge A+2$.
Induction gives $U_k\ge(A-1)^{k-1}$, and therefore in either case

\[
 |t|\ge(A-1)^{A-4}>e^{A-3}.
\]

The last inequality needs no numerical approximation: $A-1\ge6$,
$6^3>3^4$, multiplication by $6>3$ advances the inequality from $A$
to $A+1$, and $3>e$.

For bare existence, take $k=A-2$ and $b=U_k/(a-2)$ when $a>0$; when
$a<0$, take $k=A+2$ and $b=U_k/(A+2)$. In both cases put
$t=U_{k+1}$. The completeness construction needs positive odd labels,
so it chooses $a>0$, $a\equiv1\pmod6$ and $k=2(a-2)$. Then (C) makes
$b$ integral, while the period $0,1,1$ modulo $2$ makes $t$ and $b$ odd.
$\square$

The factor $a-2$ is the amplifier. Without it, the norm-one equation could
use the first power of $\rho$ and would give only linear growth. Requiring
$a-2\mid y$ forces the exponent itself to be of size $a$.

## 3. The one deep lemma

All remaining arithmetic can be stated as one finite-contact lemma. This is
the result a short paper should prove carefully; circuit details and expanded
coefficients belong in a supplement.

**Finite-contact lemma.** There are a constant $\mathcal H\ge1$ and a
finite system $\mathcal C(X,\mathbf Y)=0$ of rational quadratic equations
with the following properties. Every rational solution supplies hidden
integer labels $n,a,t,b$, with $b\ne0$, and, on putting

\[
 B=\max(|n|,|a|,|t|,|b|),qquad
 F=t^2-a(a-2)tb+(a-2)^2b^2-1,
\]

has:

1. **Anchor and scalar margin**
   \[
      |a|>(40\mathcal H)^{10},\qquad
      h(\beta)<|a|/40,qquad
      \log(40\mathcal H)<|a|/40.                         \tag{3}
   \]

2. **First gap.** If $F\ne0$, then
   \[
                         B^{1/10}<24\mathcal H.           \tag{4}
   \]

3. **Second gap.** If $n\ne\beta$, then
   \[
       \log B<\frac{12}{5}\log(40\mathcal H)
                    +\frac{19}{5}h(\beta).               \tag{5}
   \]

4. **Completeness.** For every $X\in\mathbb Z$, the system has a rational
   solution for which $n=\beta$ and $F=0$.

The lemma is finite and existential. Its equations quantify point
coordinates, local comparison values and pole witnesses, never primes or
integers.

### Why the lemma is true

The current manuscript proposes to establish the four clauses through four
ingredients. That derivation has extensive exact computational checks but
has not received independent human mathematical verification.

- The rank-one elliptic group supplies the integer labels.
- A scalar contact block and one large anchored label give (3).
- Three rational contact scales and the exponent-$19$ height estimate give
  (4) at precision $40$ and (5) at precision $12$.
- The simultaneous Gaussian-prime theorem, elementary prime separation,
  local continuity and one common elliptic index give completeness.

The local detector itself is a short idea. For tests $D_j$ of requested
orders $m_j$, form

\[
 W=\prod_j\left(1+R(D_j/R^{m_j})^2\right),qquad
 T=\operatorname {Tr}_{K/\mathbb Q}(W^{-1}),qquad B_R=R/T^2.
\]

At an odd contact of $R$, every nonconstant term has odd valuation. A pole
obstruction for $B_R$ forces one of the two $K$-places to make all tests
simultaneously deep. Contact radicals then divide any nonzero defect to the
specified power. The height theorem turns this divisibility into (4) and
(5). This is the finite existential substitute for the unavailable phrase
“at every denominator prime.”

The recent two-norm construction can shorten the detector's statement, but
it is not needed for this proof architecture.

## 4. The two-gap proof

**Conditional theorem.** If the finite-contact lemma holds, the integers
are Diophantine over the rationals, and a defining polynomial may be chosen
of degree four.

**Proof.** Suppose $\mathcal C(X,\mathbf Y)=0$. Since $B\ge|a|$, (3) gives

\[
                         B^{1/10}>40\mathcal H.
\]

This contradicts (4) unless $F=0$. The amplifier lemma now gives

\[
                         \log B\ge\log|t|>|a|-3.          \tag{6}
\]

If $n\ne\beta$, (3) and (5) give

\[
 \log B<\left(\frac{12}{5}+\frac{19}{5}\right)\frac{|a|}{40}
          =\frac{31}{200}|a|<|a|-3,
\]

contradicting (6). Hence $n=\beta$, and the reduced-denominator argument
above gives $X\in\mathbb Z$.

Conversely, if $X\in\mathbb Z$, clause 4 of the finite-contact lemma gives
a rational witness. Thus $\mathcal C$ projects exactly onto $\mathbb Z$.

Replace every rational operation and nonvanishing condition in
$\mathcal C$ by its quadratic graph, and clear fixed denominators. If the
resulting integer quadratics are $F_1,\ldots,F_m$, then

\[
                         P=F_1^2+\cdots+F_m^2
\]

vanishes over $\mathbb Q$ exactly when all source equations vanish. Hence
$P$ is the desired quartic. $\square$

The logical proof after the finite-contact lemma is the two displayed
contradictions and one sum of squares.

## 5. What remains deep

This organization does not hide the actual dependencies. A self-contained
verification of the finite-contact lemma still needs:

- the Mordell--Weil calculation $2E(K)=\mathbb ZP$;
- the exponent-$19$ height theorem;
- the pole obstruction and its restricted converse;
- the simultaneous-prime theorem in fixed Gaussian ray classes;
- local logarithm comparison and common-witness completeness.

Those are substantial results. The gain is that their role is now singular
and transparent: together they prove one finite-contact lemma. The theorem
then follows from the elementary norm-one amplifier and a two-gap argument.

### Verification ledger

| Layer | Present status |
|---|---|
| Pell--Lucas amplifier | Elementary proof above; congruences, identities, signs and parity choices have finite exact regression checks |
| Two-gap deduction | Exact conditional deduction from clauses 1--4 of the finite-contact lemma |
| Quadratic-to-quartic compression | Formal sum-of-squares argument; explicit compiler and replay exist for the larger source systems |
| Finite-contact lemma | Proposed in the current manuscript and supported by exact circuit/certificate checks; no independent human mathematical verification |
| External arithmetic inputs | Must be checked in their precise stated forms, including all hypotheses and uniformity needed here |

The first three rows explain the proof once the arithmetic engine is
available. The last two rows contain the unresolved burden of proof.

## 6. The presentation this suggests

A proof-from-the-book paper should have three layers.

1. **Main text:** integer labels, the amplifier lemma, the finite-contact
   lemma, and the two-gap proof above.
2. **Arithmetic section:** a proof of the finite-contact lemma organized as
   soundness and completeness, with no circuit optimization.
3. **Reproducibility supplement:** explicit source equations, compiler,
   certificates, expanded polynomials and record-size refinements.

The main text should introduce the norm-one amplifier before any detector
notation. It explains why the construction needs four labels and why two
successive height gaps appear. The detector then has one purpose: turn
finitely many existential contacts into the two inequalities that the
amplifier contradicts.
