# Two routes toward a shorter arithmetic proof

7 November 2026. Experimental research based on Version 10 and upstream
`036cebe4f1a4aa7ca89820a9b48f3629b4c364d6`. No polynomial is changed or
promoted. The deductions below are AI-assisted mathematical arguments;
exact checks are separately identified. No independent human review is claimed.

## 1. Primitive divisors: one sufficiently large prime can suffice

Our earlier route description asked for radical growth. That is one
possible route, but it is stronger than necessary for the elementary
last step: a single sufficiently large prime power dividing a bounded
nonzero integer is impossible.

### Reduction-order lemma

Let E be an elliptic curve over a number field K, P a nontorsion K-point,
and v a prime of good reduction with residue field of size p^f. Let D_n
be the denominator ideal of x([n]P), using an integral Weierstrass model
minimal at v. Suppose v is a primitive divisor of D_n: v divides D_n
and no D_j with 1 <= j < n. Then the reduction of P has order exactly n.
Consequently Hasse's bound gives

    n <= #E(F_(p^f)) <= (p^(f/2)+1)^2,
    p >= (sqrt(n)-1)^(2/f).

Proof. At good reduction, a denominator of x means reduction to the
identity. The first positive index with that property is exactly the
order of the reduced point. Apply Hasse to the finite group containing it.
This proof uses only the support of D_n; it is insensitive to whether one
records the full x-denominator or its square root.

**Conditional annihilation corollary.** Suppose a separate comparison
argument gives p^k | N, where N is an integer and |N| <= C B^d. If

    (sqrt(n)-1)^(2k/f) > C B^d,

then N=0. Here the index n belongs to the auxiliary point, not necessarily
the input-label point called n elsewhere in the manuscript. To avoid
confusion, call this auxiliary index m when applying the lemma.

For K=Q(sqrt(2)), f is at most two. In the worst case the sufficient
condition is (sqrt(m)-1)^k > C B^d. This replaces a radical-size estimate
by a reduction-order bound, provided the required local comparison and
index-size conditions can be enforced.

This is an elementary deduction, not a new primitive-divisor theorem.
The relevant literature supplies eventual existence of primitive divisors,
not the remaining clauses in this proposed application.

### Consecutive indices: what coprimality does and does not say

At a fixed good place v where P does not reduce to the identity, both
[h]P and [h-1]P cannot reduce to the identity. Otherwise their difference P
would also do so. Equivalently the nontrivial reduction order cannot divide
both h and h-1. Thus consecutive denominator supports are disjoint at that
place. This is useful, but **does not construct the current two-observation
witness at the same place**. It obstructs doing so.

The actual construction uses primary and conjugate places over the same
rational prime. Disjointness of prime-ideal support does not imply
coprimality of rational norms. For example, in Z[sqrt(2)], the ideals
(5-sqrt(2)) and (5+sqrt(2)) are distinct primes above 23. They are coprime,
but both have norm 23. Modulo the first, sqrt(2)=5; modulo the second,
sqrt(2)=-5. Their generators cannot vanish at the same place since their
sum is 10, a unit at 23.

This example is about ideals, not a claim that these particular ideals
are denominator ideals of the manuscript's curve. It disproves the
suggested abstract inference from ideal coprimality to norm coprimality.

For selected split primes write r_-(p), r_+(p) for the actual reduction
orders of P at the primary and opposite places. A common witness with
primary depth k0 requires, at minimum,

    h = 0 mod p^(k0-1) r_-(p),
    h = 1 mod r_+(p).

For many selected primes put A=lcm_p(p^(k0-1)r_-(p)) and
Bplus=lcm_p(r_+(p)). Compatibility is exactly gcd(A,Bplus)=1.
If h=h0 mod L is also required, the full conditions are

    gcd(A,Bplus)=1,
    h0 = 0 mod gcd(A,L),
    h0 = 1 mod gcd(Bplus,L).

These are the elementary generalized CRT conditions, not consequences of
primitive-divisor existence. The upstream version uses suitable
quotients of group orders as sufficient moduli; switching to actual point
orders may weaken the requirement, but has not been shown to give enough
usable primes.

An inert place cannot supply both observations in this same way:
conjugation preserves the unique place, and the preceding subtraction
obstruction applies outside the fixed denominator support of P.
Soundness may handle inert primes without completeness having to produce
witnesses there. These are different quantifiers.

### What the proposed replacement must prove

There are two separate tasks.

**Soundness target.** A fixed finite existential system must ensure that
an auxiliary point [m]P has a usable primitive denominator place, that
comparison tests imply p^k | N there, and that its index m satisfies the
annihilation inequality. One may invoke an eventual primitive-divisor
existence theorem once m is sufficiently large; one may not simply insert
"p is primitive" or "m is an integer prime" into an existential formula.
The integer labels exist abstractly from Mordell--Weil, but their numerical
values are not automatically available as rational coordinates.

**Completeness target.** After fixing the input, root labels, scales and
continuity modulus, find the usable places and one auxiliary witness with
the required paired reduction orders and depths. The current contact
forms must also have their prescribed arithmetic properties. Replacing
contact primes by arbitrary denominator primes is a change of source,
not a direct application of the old contact-height theorem.

A useful sharpened research target is a finite algebraic **index-size
certificate**, coupled with a comparison valid at a primitive denominator
place. Proving only that D_m has a primitive divisor leaves both tasks open.
Choosing m arbitrarily large is permitted in completeness; soundness must
hold for every satisfying witness, so it needs the certificate.

### Literature checked and scope

- Marco Streng, *Divisibility sequences for elliptic curves with complex
  multiplication*, Algebra & Number Theory 2 (2008), 183–208:
  https://msp.org/ant/2008/2-2/ant-v2-n2-s.pdf (article begins on PDF page 64).
  This treats ideal-indexed CM divisibility sequences and primitive divisors.
- Matteo Verzobio, *Primitive divisors of sequences associated to elliptic
  curves with complex multiplication*, Research in Number Theory 7, 37
  (2021), https://doi.org/10.1007/s40993-021-00267-9.
  The introduction states the rational and number-field primitive-divisor
  theorems (Theorems 1.2–1.3) and results for translated/endomorphism-indexed
  sequences (Theorems 1.7–1.8).

These statements do not assert the paired-place CRT conditions above.
We have not checked all proofs or proved their application to a replacement
source. CM endomorphisms must be defined over the field used: the j=1728
curve's multiplication by i is not defined over the real field Q(sqrt(2)).
Passing to a larger field would require a new label and encoding argument.

## 2. A global defect: exact compression and its obstruction

### Binary norm lemma

Let v be a discrete valuation of odd residue characteristic, and d a unit
whose residue is a nonsquare. For x,y in the valued field, put

    G=x^2-d*y^2.

Then, with v(0)=infinity,

    v(G)=2 min(v(x),v(y)).

Proof. Divide by a uniformizer to the smaller valuation. The normalized
pair is integral with at least one unit. If its norm vanished in the
residue field, either both residues would be zero or d would be a square.
Both are impossible. Restoring the scaling proves the identity.

Thus one order-2k norm test is exactly equivalent to two order-k tests at
these places. No variable denominator is introduced in G. Division by the
uniformizer is only in the proof, not a new witness operation.

Over Q, taking d=-1 gives G=x^2+y^2, so G=0 is equivalent to x=y=0.
But its valuation identity holds only where -1 is nonsquare. At p=5,
1^2+2^2=5 despite both entries being units. Real positivity does not give
local noncancellation.

There is an additional field issue: every nonzero element of F_p becomes
a square in F_(p^2). Consequently no fixed rational-unit d can give this
binary anisotropy at an inert place of Q(sqrt(2)). For instance at p=3,
the residue field is F_3[s]/(s^2-2), and s^2-2*1^2=0. More generally,
a^((p^2-1)/2)=1 for a in F_p^*. A rational norm coefficient alone therefore
cannot uniformly replace arbitrary K-valued local tests at inert places.

One could restrict consumed places or use coefficients in K, but either
choice needs a new coverage, nonvanishing and completeness argument. A
quadratic form in three or more variables over a finite field of odd
order is isotropic, so a single large quadratic form cannot retain the
same minimum-valuation identity for an unrestricted list of defects.

### Why combining the two final defects is not yet a shorter proof

Write the integer Lucas defect and rational label defect as

    F=t^2-a(a-2)tb+(a-2)^2 b^2-1,
    E=beta-n.

As a mathematical estimate, write beta=u/v in lowest terms, v>0. Then
G=(vF)^2+(u-vn)^2 is an integer and G=0 implies F=E=0.
This use of u,v is for analysis; asking for reduced integer numerator and
denominator as existential rational witnesses would be circular.

For B=max(|n|,|a|,|t|,|b|)>4 and h(beta)=log max(|u|,v), the existing
bound |F|<5B^4 gives

    0 <= G < 29 exp(2h(beta)) B^8.

At places with the binary anisotropy and the correct unit denominator
conditions, order-k divisibility of both defects gives order-2k divisibility
of G. Even granting a replacement transfer inequality

    B^2 <= C H |G|^(19/(2k)),

k=40 would give only

    log B <= 10 log(C H) + (19/8) log(29) + (19/4) h(beta)

when G is nonzero. Constants here follow from the displayed schematic
transfer, not from a newly proved contact theorem.

This does not contradict the scalar estimate h(beta) << |a|^(19/32).
Before F=0 is known, the available lower bound is merely B>=|a|.
The much stronger log B>|a|-3 is a consequence of F=0, via the Lucas
lemma. Using that inequality to prove G=0 would therefore be circular.

Upstream carefully avoids this: first it kills F using a bound independent
of h(beta), and only then uses Lucas growth to kill E. A global norm may
package *local tests* while retaining this two-stage reasoning. It has not
replaced the two-stage arithmetic contradiction. Preserving the first
stage's independence from h(beta) is the essential design constraint.

### Why a resultant cannot eliminate all witnesses

Let I in Q[X,Y_1,...,Y_N] be generated by any proposed defining equations
whose rational solutions project onto all integers. If g(X) belongs to
I intersect Q[X], evaluating at a witness for each integer shows that g
vanishes at every integer. Hence g=0, so

    I intersect Q[X] = (0).

Thus algebraic elimination of all witnesses produces no nonzero equation
in X. This does not exclude a useful resultant retaining some witnesses.
It says that the arithmetic restriction must survive as rational-point
solvability, not as an ordinary polynomial condition on X alone.

### Most useful remaining global target

Seek a scalar defect G_F on the label/comparison variety with all of:

1. G_F=0 forces F=0, without already assuming E=0 or Lucas growth;
2. its height is bounded in terms of B, independently of h(beta);
3. a finite algebraic condition gives enough local divisibility of G_F;
4. integral inputs admit witnesses and all quotient domains are preserved.

A global product formula or resultant only helps if it proves item 3
without reintroducing the existing contact detectors. Nonzero rational
numbers already obey the product formula, so it is not an annihilation
argument without bounds at the other places.

## Combined assessment

The primitive-divisor route now has a sharper target: one large primitive
prime can replace a radical estimate, but a finite index-size certificate
and paired-place comparison are missing. The global route has a usable
local norm lemma, but uniform local anisotropy and the first height
contradiction are decisive constraints. The next research should first
try a one-defect construction for F. Solving F independently would preserve
Lucas amplification and allow the beta=n comparison to remain unchanged.

These are partial deductions and precise obstacles, not a shorter proof
of the main theorem and not evidence against its existing argument.
