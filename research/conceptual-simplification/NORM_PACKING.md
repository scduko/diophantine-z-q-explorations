# One norm packs the entire local test list

7 November 2026. Experimental proof architecture based on upstream
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6`. This is AI-assisted research
without independent human review. It changes no production source or
polynomial.

## The local norm-packing lemma

Let $L/K$ have degree $r$, let $e_1,\ldots,e_r$ be a basis integral at a
prime $\mathfrak p$ of $K$, and suppose that $\mathfrak p$ is unramified
and inert in $L$. Normalize the unique valuation above $\mathfrak p$
compatibly. For $z_1,\ldots,z_r\in K$,

\[
 v_{\mathfrak p}\!\left(N_{L/K}\Big(\sum_i z_i e_i\Big)\right)
   =r\min_i v_{\mathfrak p}(z_i).                          \tag{1}
\]

Indeed, divide all coefficients by the smallest uniformizer power. At
least one resulting coefficient is a unit. The reductions of the integral
basis are linearly independent over the residue field, so the resulting
element is a unit in the unramified degree-$r$ completion. Taking the norm
proves (1). The same argument permits negative coefficient valuations.

The norm is a fixed homogeneous polynomial of degree $r$ over $K$. Writing
its coefficients and output in the basis $1,\sqrt2$ gives two rational
polynomial expressions with fixed rational coefficients. By itself it
introduces no variable denominator or nonvanishing obligation. An
arithmetic circuit can evaluate it using quadratic graph equations,
although that circuit may be large. Adapting it to the detector's
normalization uses powers of an existing guarded denominator, as detailed
below.

## Apply it to the Version 10 tests

The asymmetric source has nine $K=\mathbb Q(\sqrt2)$-valued tests at order
one and seven $K$-valued tests at order forty:

- order one: four non-anchor primary $f$-tests and five alternate
  $f$-tests;
- order forty: the primary anchor $f$-test, four cross tests, the input
  comparison, and the Lucas test.

Keep the tests as $K$-valued quantities. Write the nine order-one tests as
$x_i$ and the seven order-forty tests as $y_j$. Take $L/K$ of degree
$r=16$ and put

\[
 \alpha=\sum_{i=1}^{9}x_i^{40}e_i
       +\sum_{j=1}^{7}y_j e_{9+j},
 \qquad G=N_{L/K}(\alpha).                                 \tag{2}
\]

At every unramified inert place $\mathfrak p$ of $K$,

\[
 v_{\mathfrak p}(G)=r\min\left(40v_{\mathfrak p}(x_1),\ldots,
 40v_{\mathfrak p}(x_9),v_{\mathfrak p}(y_1),\ldots,
 v_{\mathfrak p}(y_7)\right).                             \tag{3}
\]

Consequently

\[
 v_{\mathfrak p}(G)\ge40r
 \quad\Longleftrightarrow\quad
 v_{\mathfrak p}(x_i)\ge1\ \text{for all }i,
 \quad v_{\mathfrak p}(y_j)\ge40\ \text{for all }j.     \tag{4}
\]

This is an exact local equivalence, not a height heuristic. Globally,
$G=0$ also forces every component to vanish: a field norm is zero only at
zero, and the basis is independent.

Equation (2) therefore replaces the mixed list by one $K$-valued test of
order $40r=640$, provided both places over each contact prime are inert in
$L/K$. It does **not** combine the Lucas defect with the input-label
defect. After unpacking (4), the existing proof can still kill the Lucas
defect first and invoke Lucas growth only afterward. The construction thus
avoids the circularity in the naive sum of the two final defects.

### Exact compatibility with the detector normalization

There is a bookkeeping point that cannot be omitted. In the source, a raw
test $D_j$ of order $m_j$ enters a detector through

\[
       s_j=\frac{D_j}{\delta^{m_j+1}R^{m_j}}.
\]

Put $M=40$. For an order-one test define

\[
       c_i=\delta^{1-M}D_i^M,
\]

and for an order-$M$ test put $c_j=D_j$. Finally define the raw packed
test

\[
       D_*=\delta^{1-r}N_{L/K}\!\left(\sum c_i e_i\right). \tag{5}
\]

Homogeneity of the norm gives the exact identity

\[
 \frac{D_*}{\delta^{rM+1}R^{rM}}
 =N_{L/K}\!\left(
     \sum_{m_i=1}s_i^M e_i+\sum_{m_j=M}s_j e_j\right).     \tag{6}
\]

For example, an order-one entry on the right is
$D_i^M/(\delta^{2M}R^M)$; its counterpart inside (5), after the common
normalization is distributed through the degree-$r$ norm, is exactly the
same. An order-$M$ entry is $D_j/(\delta^{M+1}R^M)$ on both sides.

Thus $D_*$ is one test of order $rM=640$ in precisely the source's
normalization. For $r=16$, formula (5) uses $\delta^{-39}$ in the
order-one entries and the outer factor $\delta^{-15}$. The source already
guards $\delta\ne0$, so these quotients create no new nonvanishing
hypothesis. Their defining gates and reverse maps would still have to be
certified in any finite candidate.

The proposed single detector factor is

\[
       W=1+R\left(\frac{D_*}{\delta^{641}R^{640}}\right)^2. \tag{7}
\]

Retain the source definitions

\[
       T=\operatorname {Tr}_{K/\mathbb Q}(W^{-1}),
       \qquad B=R/T^2,
\]

and the same preparation-zero pole certificate for $B$.

### Soundness of the one-factor detector

At a contact prime, the source proves that $\delta$ is a unit. The existing
one-place lemma, applied to the single raw test $D_*$ of order $640$, gives
one place $\mathfrak p$ with
$v_{\mathfrak p}(D_*)\ge640$. If the contact prime is inert in $L/K$,
(1) and (5) give

\[
  v_{\mathfrak p}(D_*)=16\min\bigl(
      40v_{\mathfrak p}(D_i):m_i=1;
      v_{\mathfrak p}(D_j):m_j=40\bigr).
\]

It follows that every order-one test has valuation at least one and every
order-forty test has valuation at least forty at the same place. Thus the
soundness deduction is a direct application of the existing pole lemma;
it does not require a stronger height estimate.

The local part of completeness also survives the replacement. At the
successful place every normalized packed entry is integral, so the
nonconstant term of (7) has positive valuation and $W^{-1}\equiv1$. At the
other place the inverse of the one
factor has residue either one or zero, by the same odd-valuation argument
as the source. Hence $T$ has residue one or two and is a unit at every odd
contact prime. Therefore $B$ has the same positive odd contact valuation
as $R$; away from the contacts its valuation differs from that of $R$ by
an even integer. At the real place, the source has $R=O(\lambda^{-1})$
and every normalized original test is $O(\lambda^{-1})$. The packed norm
is then $O(\lambda^{-16})$, so $W=1+O(\lambda^{-33})$ and the same small
positive pole input is available.

This establishes the detector's contact-prime logic at the level of the
source proof. A finite source replacement must still check the exceptional
and small-prime approximation simultaneously, prove every new quotient
gate reversible, and replay the compiled certificate. Those are integration
obligations rather than a missing replacement for the pole theorem.

## An explicit cyclotomic degree-16 field

The needed inertness has a simpler realization than the initially
considered Gaussian ray-class construction. Let $F$ be the unique degree-$16$ subfield of
$\mathbb Q(\zeta_{97})$, and put

\[
 K=\mathbb Q(\sqrt2),\qquad L=KF.
\]

The group $(\mathbb Z/97\mathbb Z)^*$ is cyclic of order $96$; the field
$F$ corresponds to its subgroup of order $6$. Thus
$\operatorname {Gal}(F/\mathbb Q)$ is cyclic of order $16$. Its unique
quadratic subfield is $\mathbb Q(\sqrt{97})$, so
$F\cap K=\mathbb Q$ and $[L:K]=16$. The field $F$ is ramified only at
$97$, whereas $K$ is ramified only at $2$. Their discriminants are
coprime, so any integral basis of $F$ is also an integral $K$-basis after
base change to $L$.

The residue class $5$ has multiplicative order $96$ modulo $97$. Its image
in the quotient of order $16$ therefore has order $16$. Hence a rational
prime $p\equiv5\pmod {97}$ is inert in $F/\mathbb Q$. The contact primes
already split in $K$. At either $K$-place above such a $p$, the completion
is $\mathbb Q_p$, and base change of the inert unramified degree-$16$
extension from $F$ remains inert of degree $16$ in $L/K$. This proves
exactly the local hypothesis used in (1).

The new congruence can be imposed uniformly on the prime forms
$p_j=u+c_jw^2$ by choosing

\[
              u\equiv5,\qquad w\equiv0\pmod {97}.
\]

Every $p_j$ is then $5$ modulo $97$, so the local factor is nonzero and
independent of $c_j$. This is a new fixed local prescription, not part of
the displayed statement of `thm:v5-simultaneous-primes`. The general
prime-pattern framework is designed to accept finitely many such fixed
local conditions. More concretely, the Gaussian ray class
$\pi_p\equiv1+2i\pmod {97}$ has norm $5$, while
$N(\pi_p-1)\equiv4$ and $N(\pi_p+1)\equiv8$ modulo $97$. It therefore
imposes the desired rational Frobenius class without introducing a factor
$97$ into either reduced group order. This remains compatible even when
$97$ divides a later progression modulus. A source replacement must still
re-run the density and CRT argument with all existing ray conditions. The
field, disjointness, and desired Frobenius action themselves are no longer
conjectural.

The tempting smaller conductor $17$ does **not** work with the existing
pole certificate. Every generator of
$(\mathbb Z/17\mathbb Z)^*$ is a nonsquare, whereas completeness requires
each contact prime to be a square in $\mathbb Q_{17}$. The independent
modulus $97$ avoids that conflict.

The rejected earlier idea used a norm-one residue quotient modulo $257$
and a generalized-dihedral reflection field. It created unnecessary unit,
quotient, and disjointness obligations; the cyclotomic construction above
supersedes it.

Degree $16$ is minimal for packing the $9+7$ $K$-valued tests in one
basis. Packing the $32$ rational coordinates directly is invalid: at a
split prime, divisibility of $a+b\sqrt2$ at one $K$-place does not imply
componentwise divisibility of $a$ and $b$. This rejected degree-$32$
attempt is recorded so it is not repeated.

### A short formula and a minimality observation

Because $\operatorname {Gal}(F/\mathbb Q)$ is cyclic of order $16$, the
extension $L/K$ has a unique tower

\[
 K=L_0\subset L_1\subset L_2\subset L_3\subset L_4=L,
 \qquad [L_i:L_{i-1}]=2.
\]

The packed scalar can therefore be defined without a determinant or an
expanded polynomial:

\[
 N_{L/K}(\alpha)=
 N_{L_1/K}\!\left(N_{L_2/L_1}\!\left(
 N_{L_3/L_2}\!\left(N_{L/L_3}(\alpha)\right)\right)\right),
\]

and each displayed quadratic norm is just $z\mapsto z\sigma(z)$. This is
the most concise existential description and also supplies a canonical
quadratic-circuit architecture if a finite implementation is attempted.

There is a sense in which degree $16$ is forced. Reduce any proposed
homogeneous one-scalar packer in sixteen variables modulo a good contact
prime. If its degree were less than sixteen, Chevalley--Warning would make
the number of its zeros divisible by the residue characteristic. Since the
zero vector is a zero, there would be a nonzero zero as well. Such a form
could not force all sixteen residues to vanish. The degree-$16$ norm is
therefore optimal among homogeneous one-scalar packers. This does not rule
out a nonhomogeneous construction, several scalar equations, or a packing
that exploits additional relations among these particular tests.

## What this does and does not simplify

The norm construction gives a genuine structural alternative to the
source's symmetric-coefficient aggregation:

1. one fixed norm replaces all sixteen $K$-valued local tests;
2. local noncancellation follows from inertness and basis independence;
3. mixed precision is absorbed by the powers $x_i^{40}$ and the exact
   rescaling (5);
4. no maximum predicate, universal quantifier, or expanded polynomial is
   used in the statement.

It does not remove the contact-prime theorem, height transfer, common
witness, scalar anchor, or Lucas amplification. It trades the present
small explicit circuit for a high-degree fixed norm and an additional
Frobenius condition. For an existential proof this may be a substantial
expository simplification. For the variable or monomial record it is
likely worse unless a surprisingly small norm circuit exists.

Before promoting any finite candidate one would need:

- an exact norm circuit and every intermediate nonvanishing analysis;
- exceptional-prime and approximation checks for the integrated detector;
- a complete prime-pattern density and compatibility check;
- compiler, certificate, and full-polynomial replay.

None of those finite-candidate claims is made here.

## Architectural conclusion

There are now two distinct notions of a shorter proof.

- The elementary separation lemma shortens a genuine arithmetic step in
  the existing proof.
- Norm packing shortens the description of all local tests to one
  $K$-valued defect, at the cost of a larger fixed algebraic object.

The follow-up `TWO_NORM_PACKING.md` improves the finite architecture by
packing the order-one and order-forty groups separately. That avoids nine
fortieth powers and lowers the packed orders to $9$ and $280$. The present
one-norm construction remains the shortest literal one-defect statement,
but it is no longer the preferred route to an explicit source.

The remaining conceptual bottleneck is unchanged: the contact mechanism
is still the finite existential substitute for testing denominator primes.
Primitive divisors may eventually replace that mechanism for the Lucas
defect, but the missing local encoding identified in
`ELEMENTARY_SEPARATION.md` remains unresolved.
