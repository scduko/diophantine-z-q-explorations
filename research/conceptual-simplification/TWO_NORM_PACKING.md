# Two norms respect the two precision classes

7 November 2026. AI-assisted conceptual research based on upstream
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6`; no independent human
mathematical review. No production source or polynomial is changed.

## The improvement over one-norm packing

The asymmetric source has nine $K=\mathbb Q(\sqrt2)$-valued tests of
order one and seven $K$-valued tests of order forty. Packing all sixteen
into one degree-$16$ norm works, but equalizing the two precisions requires
raising each of the nine low-order tests to the fortieth power. That is
clean in an existential proof and unattractive in a quadratic circuit.

Keep the two precision classes separate. Choose extensions $L_9/K$ and
$L_7/K$ of degrees $9$ and $7$, with local integral bases
$e_1,\ldots,e_9$ and $f_1,\ldots,f_7$. For the raw tests $D_i$ define

\[
 D_{(1)}=\delta^{-8}N_{L_9/K}\!\left(\sum_{m_i=1}D_i e_i\right),
 \qquad
 D_{(40)}=\delta^{-6}N_{L_7/K}\!\left(\sum_{m_j=40}D_j f_j\right).
 \tag{1}
\]

The negative powers use the source's existing guard $\delta\ne0$.
Homogeneity gives the two exact normalization identities

\[
 \frac{D_{(1)}}{\delta^{10}R^9}
 =N_{L_9/K}\!\left(\sum_{m_i=1}
      \frac{D_i}{\delta^2R}e_i\right),                    \tag{2}
\]

\[
 \frac{D_{(40)}}{\delta^{281}R^{280}}
 =N_{L_7/K}\!\left(\sum_{m_j=40}
      \frac{D_j}{\delta^{41}R^{40}}f_j\right).            \tag{3}
\]

Thus $D_{(1)}$ is one raw test of order $9$, and $D_{(40)}$ is one
raw test of order $280$. Replace the sixteen-factor detector by

\[
 W=\left(1+R\left(\frac{D_{(1)}}{\delta^{10}R^9}\right)^2\right)
   \left(1+R\left(\frac{D_{(40)}}{\delta^{281}R^{280}}\right)^2\right).
 \tag{4}
\]

Retain $T=\operatorname {Tr}_{K/\mathbb Q}(W^{-1})$, $B=R/T^2$, and
the same pole certificate.

## Exact local implication

Suppose a contact prime is unramified and inert in both extensions. At a
place $\mathfrak p$ above it, the norm-valuation identity gives

\[
 v_{\mathfrak p}(D_{(1)})
   =9\min_{m_i=1}v_{\mathfrak p}(D_i),
 \qquad
 v_{\mathfrak p}(D_{(40)})
   =7\min_{m_j=40}v_{\mathfrak p}(D_j),                  \tag{5}
\]

because $\delta$ is a contact-prime unit. Apply the source's existing
one-place lemma to the two packed raw tests, with assigned orders $9$ and
$280$. It selects one $K$-place for both and gives

\[
 v(D_{(1)})>(9-3/4)v_p(R),\qquad
 v(D_{(40)})>(280-3/4)v_p(R).
\]

The positive odd integer $v_p(R)$ is at least one. Since valuations are
integral, (5) forces

\[
 v(D_i)\ge1\quad(m_i=1),\qquad
 v(D_j)\ge40\quad(m_j=40).
\]

This is precisely the original local conclusion, at one common place.
The two-stage Lucas-then-input contradiction is unchanged.

Completeness has the same residue calculation. At the successful place
both normalized norms are integral, so both factors of (4) are congruent
to one. At the other $K$-place each inverse factor has residue zero or one.
Their product does too, and the trace has residue one or two. Hence it is a
unit at every odd contact prime. The parity of $v(B)$ away from the contacts
is unchanged because $B=R/T^2$. Exceptional-prime approximation and all
quotient reverse maps must still be checked in an integrated source.

## One cyclic field supplies both norms

Let

\[
 F=\mathbb Q(\zeta_{127}+\zeta_{127}^{-1}),\qquad L=KF.
\]

The extension $F/\mathbb Q$ is cyclic of degree $63=9\cdot7$. Since its
degree is odd, $F\cap K=\mathbb Q$. Let $F_9$ and $F_7$ be its unique
subfields of degrees $9$ and $7$, and put $L_9=KF_9$, $L_7=KF_7$.

The residue class $3$ has order $126$ modulo $127$. Its image in
$(\mathbb Z/127\mathbb Z)^*/\{\pm1\}$ has order $63$, so every rational
prime $p\equiv3\pmod {127}$ is inert in $F$. It is consequently inert in
both $F_9$ and $F_7$. Since the selected contact primes split in $K$, both
$K$-places above each contact prime are inert in $L_9/K$ and $L_7/K$.

There is a compatible Gaussian ray class:

\[
 r=1+16i\pmod {127},\qquad
 N(r)=257\equiv3,\quad N(r-1)=256\equiv2,
 \quad N(r+1)=260\equiv6\pmod {127}.                     \tag{6}
\]

Thus the new class gives exactly the inert rational Frobenius and makes
neither adjacent reduced elliptic-group order divisible by $127$.

## Ray-class flexibility lemma

The displayed simultaneous-prime theorem specializes its auxiliary odd
classes to $i$. Its proof establishes the following slightly more general
form.

**Lemma.** Fix an additional odd prime $\ell\ne7$ and a Gaussian residue
$r\bmod\ell$ for which $N(r)$, $N(r-1)$, and $N(r+1)$ are nonzero modulo
$\ell$. The simultaneous-prime conclusion remains valid with the extra
condition that every selected generator is congruent to $r$ or $\bar r$
modulo $\ell$. If $\ell$ already divides the avoidance modulus, this class
replaces the specialized class $i$ at that one factor.

**Proof.** In the ray-density proof, put $\ell$ into the fixed base modulus
$H_0$ and choose the base residue to be $r$ at $\ell$. The conjugation pair
$\{r,\bar r\}$ is a rational conjugacy class. The fixed local singular
factor is positive: take $u\equiv N(r)$ and $w\equiv0$ modulo $\ell$, so
every prime form has that nonzero norm. The medium- and large-prime
obstruction estimates allow any prescribed generator class and are
unchanged. The ray-fibre product is taken only over new primes beyond the
fixed base, so its lower bound is unchanged up to a positive constant.
Finally, $N(r\pm1)\ne0$ excludes $\ell$ from both adjacent norms. All
conditions at $2$, $7$, and the other fixed odd primes combine by CRT.

For (6), the retained adjacent residues are $2$ and $6$. Hence this lemma
also handles the case $127$ divides the later progression modulus: the
class $1+16i$ replaces $i$ and still keeps both group orders coprime to
$127$.

This closes the fixed-field and local-density issue for the conceptual
two-norm detector. A formal manuscript incorporation should state and prove
the flexibility lemma adjacent to the specialized theorem rather than
silently invoke a stronger theorem.

## Degree optimality and circuit implications

At a good residue field, a homogeneous scalar form in $n$ variables of
degree less than $n$ has a nonzero zero by Chevalley--Warning. Consequently
degrees $9$ and $7$ are individually minimal for homogeneous scalar packers
of the two test groups, unless one exploits additional relations among the
particular tests.

The degree-$9$ norm factors through two cubic norms along the unique tower
$9\to3\to1$; the degree-$7$ norm is one fixed septic form. Both have fixed
integral bases away from $127$. They can therefore be evaluated by quadratic
graph equations without expanding the final quartic. Unlike the one-norm
architecture, this construction introduces no fortieth powers of individual
tests and reduces the maximum packed order from $640$ to $280$.

The bases and their arithmetic can be made completely explicit. For
$d\in\{7,9\}$, put $h=126/d$ and

\[
 \eta_j^{(d)}=\sum_{t=0}^{h-1}\zeta_{127}^{,3^{j+dt}}
 \qquad(0\le j<d).
\]

Multiplication by the generator of the Galois group cyclically permutes
these periods. Counting sums in the residue cosets gives an integral
multiplication table. The exact checker computes its trace Gram determinant:

\[
 \operatorname {disc}(\eta_0^{(d)},\ldots,\eta_{d-1}^{(d)})
 =127^{d-1}.
\]

This equals the field discriminant from the conductor--discriminant formula,
so the periods are integral bases, not merely local spanning sets. The
degree-$7$ table uses coefficients
$-18,-16,-14,-13,0,1,2,3,4,5$ and has 329 nonzero structure constants out
of 343. The degree-$9$ table uses
$-14,-12,-11,-10,0,1,2,3,4$ and has 603 out of 729. The coefficients are
small, but the tables are dense.

There is also a preliminary quadratic-gate comparison. In the period basis,
the degree-$9$ norm can be evaluated with $9+3+3+1=16$ assigned
$K$-coordinates by descending through $9\to3\to1$. A balanced product of
the seven conjugates uses $3\cdot7+2\cdot7+1=36$ assigned $K$-coordinates.
The two norms therefore use 52 such assignments. The present source uses
16 test squares plus 29 and 20 assigned symmetric-product coefficients,
for 65 $K$-coordinate assignments before the final detector evaluation.
This comparison omits weights, quotient gates and possible common-subexpression
savings, so it is evidence for an experiment rather than a variable claim.

## Isolated compiler experiment

The experiment in `experiments/build_two_norm_candidate.py` replaces only
the symmetric test aggregation and detector evaluation in a copy of the
asymmetric builder. It uses the period multiplication tables above and the
weight identities

\[
 q_1^9R^{-8}=q_1(q_1e\delta)^8,
 \qquad q_{40}^7R^{-6}=q_{40}(q_{40}e\delta)^6,
 \]

where $e\delta=R^{-1}$. Each weight takes five scalar assignments.

The exact result is mixed:

| quantity | current precursor | dense two-norm candidate |
|---|---:|---:|
| raw coordinates | 540 | 525 |
| compiled active coordinates | 532 | 517 |
| compiled residuals | 501 | 486 |
| quartic monomials | 34,248 | 451,149 |

The compiler produced a degree-four primitive polynomial, and the
independent checker replayed all 443 gate identities and 421 certificate
operations. Thus the 15-coordinate reduction is exact algebra, not a gate
estimate. The dense normal-basis multiplication raises the monomial count by
416,901, a factor of about 13.17. This version is rejected for the balanced
record and preserved as a minimum-variable and basis-sparsification
experiment. It has not received the final source-specific elimination pass,
so 517 is not asserted to be the best coordinate count available from this
architecture.

A power basis is sparser at the multiplication-table level but introduces
large coefficients and dense Galois-action matrices. For the period
generators its minimal polynomials are

\[
 x^7+x^6-54x^5-31x^4+558x^3-32x^2-1713x+1121
\]

and

\[
 x^9+x^8-56x^7-118x^6+573x^5+1249x^4-1582x^3
      -2700x^2+1576x+32.
\]

Their direct multiplication tensors have 175 of 343 and 369 of 729
nonzero structure constants, respectively, but the power orders have
indices $19^3\cdot37$ and $2^{27}\cdot131$ in the integral period orders.
The conjugation matrices do restore the lost density: 43 of 49 entries are
nonzero in degree $7$, and 73 of 81 are nonzero in degree $9$. Their
numerators already reach $2,433,631,983$ and $1,486,231,851$, with
denominators divisible by the power-order indices. Because every norm step
uses these conjugations, the naive power-basis route is recorded as
unproductive. A useful sparse revision would need a basis or multiplication
algorithm that treats multiplication and the cyclic action simultaneously.

This is now the preferred norm-packing architecture. It may still be larger
than the source's highly optimized symmetric-coefficient circuit. No
variable, monomial, or coefficient improvement is claimed until an exact
gate program, certificate, and full-polynomial replay have been run.

## Remaining obligations

- encode the two norm circuits and certify the $\delta^{-8}$ and
  $\delta^{-6}$ quotient gates in both directions;
- re-run exceptional-prime approximation with the packed factors;
- compile, replay the certificate, and compare variables, monomials, and
  coefficient sizes for any sparse-basis revision before considering
  promotion;
- obtain independent human mathematical review.
