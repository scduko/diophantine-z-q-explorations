# Elementary separation and the largest-label strategy

7 November 2026. AI-assisted research; no independent human review.
The production source and polynomial are unchanged. PR #4 is retired from
this workflow; further research lives on `conceptual-simplification`.

## A genuinely elementary replacement for the separation argument

**Lemma.** Let p_1,...,p_s be odd primes with max p_j <= 2 min p_i.
For each j let E_j/F_(p_j) have a model

    y^2=(x-a_j)(x-b_j)(x-c_j)

with three distinct rational roots. Put d_j=#E_j(F_(p_j)). Then
p_i does not divide d_j for any i,j.

**Proof.** The identity and the three points with y=0 form a subgroup of
order four, so 4 divides d_j. Counting points over each abscissa gives

    d_j <= 1 + 3 + 2(p_j-3) = 2p_j-2.

If p_i divided d_j, its oddness would imply 4p_i divides d_j. But

    d_j <= 2p_j-2 <= 4 min_i p_i-2 < 4p_i,

a contradiction. This uses neither Hasse's theorem nor prime spacing.

**Application to the reviewed source.** In Version 10,
`lem:v9-bridge` identifies d_+(p) as the opposite reduced elliptic-group
order and establishes the full rational two-torsion: the roots 0,+d,-d
are distinct beyond the fixed cutoff. The completeness argument selects
p_j=u+c_j w^2 with fixed c_j and w^2=o(u), so their ratio tends to one.
Thus the lemma applies. Equivalently d_+(p_j)/4 < min_i p_i, so

    gcd(product_i p_i, lcm_j(d_+(p_j)/4))=1.

No distinction between i=j and i!=j is needed. The extra lower bound
w>=N^(1/3), the removal of that strip from the count, the condition
on tau(N)N^(1/6)/(log N)^s, and the minimum spacing c_*N^(2/3)
can all be omitted from this particular separation argument.

There is also a direct way to obtain the narrow interval from the stated
prime theorem, without reopening its diagonal proof. Put
C=max_j |c_j| and request u/w^2>3C (use any positive bound if C=0).
Then 2u/3<p_j<4u/3, hence max p_j<2 min p_i. The theorem already
permits an arbitrarily large fixed real lower bound on u/w^2. Integer
scaling is fixed before choosing this bound. Retain all other required
lower bounds and congruences by taking their maximum.

**Scope.** This replaces only `v9:lem:separation`, whose consumer is
`subsec:v9-deep-completeness`. It does not establish
 gcd(M_-,M_+)=1, the congruences modulo L, or existence of the contact-prime
pattern. Those remain inherited inputs. It introduces no rational quotient
or nonvanishing obligation. The argument is for residue fields F_p, as in
the selected completeness pattern, not arbitrary inert reductions over F_(p^2).

**Historical disposition.** The existing proof already establishes the
separation claim. We inspected its actual proof in
`docs/quartic-523-540/addition.tex`, its bridge lemma, and the statement
`thm:v5-simultaneous-primes` in `manuscripts/quartic_v10.tex`, at upstream
036cebe4f1a4aa7ca89820a9b48f3629b4c364d6. This is a proposed shorter proof,
not a repair of a false claim. No priority or exhaustive-history claim is
made. Manuscript incorporation is pending; frozen files are untouched.

## Primitive divisors of the largest root label

The previous note asked for an additional auxiliary point with a sufficiently
large index. For the Lucas defect alone, there is a potentially cleaner
choice: use the root point whose hidden integer label has largest magnitude.
This avoids a separate index-size certificate, conditional on a new local
encoding described below.

Let Q_i=[n_i]P be the four root points and B=max_i |n_i|. Set

    F=t^2-a(a-2)tb+(a-2)^2 b^2-1.

The existing elementary estimate is |F|<5B^4 for B>4. Choose a root with
|n_i|=B. A good primitive denominator place of [B]P has reduction order B.
For residue degree f<=2, Hasse's bound implies

    p >= (sqrt(B)-1)^(2/f) >= sqrt(B)-1 >= sqrt(B)/2

when B>=4. Therefore, if the local mechanism enforces p^k | F there,

    p^k >= B^(k/2)/2^k.

For k=40 and B>=16 this is strictly larger than 5B^4, so F=0.
More generally any k>8 works above a fixed threshold; for k=9,
B>6,553,600 suffices using this deliberately coarse estimate.

No Lucas growth or input-height estimate is used in this implication.
Negative labels cause no issue: x([-B]P)=x([B]P). A primitive-divisor
existence theorem gives such a place for all sufficiently large B; finitely
many excluded places can be removed by increasing that threshold, since
each has at most one first positive denominator index. This is an
existential, potentially ineffective threshold. It is NOT claimed that the
current explicit anchor exceeds it without an effective bound. For a
nonexplicit theorem, a larger fixed anchor could be allowed if the
inherited anchor construction can impose that bound.

**Conditional replacement proposition.** Suppose a finite algebraic source
with integer-labelled roots can (i) force B beyond this fixed threshold,
(ii) ensure that at every good primitive denominator place of each root,
p^40 divides the integer F, and (iii) supply witnesses for every integral
input. Then the preceding argument forces F=0 without the three contact
height detectors in the first soundness contradiction. The second,
input-label contradiction still needs its own mechanism.

The phrase "at every primitive denominator place" is a semantic consequence
that the source would have to prove, not a universally quantified clause
we are entitled to insert into an existential formula. Requiring a
consequence at every good denominator place would be sufficient and would
avoid recognizing primitivity in the equations. There are only four root
points: require the local consequence for each, and select the largest
only in the mathematical proof. No existential maximum predicate is needed.

**Remaining obstacle.** The present detectors impose tests at contact
primes, not all root denominator primes. Moreover their two observations
use a common H and its shift at opposite places. Arbitrary primitive root
primes need not satisfy those paired reduction-order requirements. Simply
setting H equal to the largest root does not fix this: it forces the
opposite reduction order to divide B-1. Thus this proposition is a sharper
target, not a validated replacement source.

The next task is to find a local encoding of F at root denominator places
that uses one place, or otherwise avoids the incompatible shifted anchor.
The elementary separation lemma helps the existing completeness proof;
it does not solve this different primitive-divisor coverage problem.
