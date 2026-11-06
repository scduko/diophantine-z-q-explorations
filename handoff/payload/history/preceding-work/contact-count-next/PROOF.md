# Thirty-seven comparisons using rational height targets

This is a proposed change to the arithmetic source construction. It is not
an algebraic certificate step for the old pinned source. The argument below
preserves the integer-defining claim using the existing height, parity,
elliptic-group, and published prime-pattern inputs at their current review
status. It introduces no new arithmetic theorem assumption. Independent
review and a new finite compilation check are still required.

## Why the current source has 41 comparisons

The source uses four points `Q=A,S,T,Z`. It selects one rational common
denominator `e` and eight rational coefficients of `e*x(Q)`. These give nine
height targets. Each target is represented as the sum of two slopes, one
of which is common to all targets. The five-contact height theorem needs
four finite contacts for every slope and one infinity contact shared by
all slopes. Thus there are `1+4*(1+9)=41` comparison calls.

This count is distinct from the 41 rational tests inside each comparison:
23 tests have order one and 18 have order 64. The present proposal changes
the number of comparison calls to 37. It leaves those internal tests, their
orders, their four index proxies, and the five private comparison points
unchanged.

The common denominator is used for the completeness proof of the old
prime-pattern lemma, which is stated for integer targets. It is not needed
for the height inequalities themselves. The following extension permits
the eight unscaled rational coefficients of `x(A),x(S),x(T),x(Z)` to be
used directly.

## A rational-target prime-pattern lemma

Retain all fixed constants from the accepted source:

```
C = {0, 1, 2401, -343/32},
R = 47027 = 31*37*41,
W = 25878772920,
c = 18484837801,
V0 = 32W.
```

Fix arbitrary rational targets `a_1,...,a_k`, with `k<=8`, before making
any prime choices. Put `A_i=R*a_i+3`. Choose a positive integer `D` such
that every `D*a_i` is integral. This `D` belongs only to the existence
proof; it is not a new polynomial variable or coefficient. Let

```
T = V0*D²,
u = c+W*x,
p0 = c+W*y,
v = T*p0,
S = C union the sets (A_i-C),
K_s = T*s for s in S,
Psi_s = c+W*x-K_s*(c+W*y).
```

Every `K_s` is an integer divisible by `W`: the denominator 32 in `C`
is absorbed by `V0`, and `D²*A_i=D*(D*A_i)` is integral. Consequently
all `Psi_s` and `p0` are integer affine forms congruent to `c` modulo `W`.
Remove duplicate slopes, including collisions between distinct target
families. The remaining forms have pairwise independent linear parts.
There are `m=1+|S|<=37` distinct forms. Coincident slopes are permitted;
their repeated comparison occurrences simply receive the same prime.

For every prescribed lower bound, there are integers `x,y` such that all
these distinct forms are positive ordinary primes beyond that bound.
Here "ordinary" has exactly the accepted source meaning: the two good
reductions of the fixed elliptic curve at that prime have cardinalities
`d1,d2` with `gcd(d1,d2)=4` and `p` does not divide `d1*d2`. The actual raw
contacts are

```
r_infinity = v/V0 = D²*p0,
u-delta*v for delta in C,
u-(A_i-delta)*v for delta in C and 1<=i<=k.
```

Thus every finite raw contact is an ordinary prime. The infinity raw
contact is a positive rational square times one ordinary prime.

### Local admissibility, including denominator primes

At primes dividing `W`, every affine form equals `c` modulo that prime.
The existing residue checks for `c` therefore apply unchanged. As in the
accepted argument, no successor condition is imposed at 2.

Let `q>29` divide `D`. Since `D*A_i` is integral and the denominators in
`C` divide 32, every `K_s` is divisible by `q`. Modulo `q`, all finite
forms are therefore `u`, while `p0=c+W*y` is independent of `u=c+W*x`.
Choose `u=p0=1` modulo `q`. Their values and successors are nonzero.
This treats denominator primes without assuming any bound on `D`.

Now suppose `q>29` does not divide `D`. The map from `(x,y)` to `(u,v)`
is invertible modulo `q`. The slopes are well-defined there. If
`q` is 31, 37, or 41, each `a_i` is `q`-integral and `A_i=3` modulo `q`,
so there are at most eight slope residues. At all `q>=43` there are at
most 36. Choose distinct `b,e` outside those residues and put
`gamma=T^(-1)` modulo `q`. Reverse `b,e` if necessary so that
`e-b != -gamma`. This reversal is always possible at an odd prime.
Set

```
v = 1/(e-b),   u = b*v.
```

Then `u-s*v=v*(b-s)` and `u-s*v+1=v*(e-s)` are nonzero for every slope.
Also `p0=gamma*v` and `p0+1` are nonzero. This proves the required
value and successor admissibility at every remaining prime.

### The prime and order sieve

Choose a fixed real box in the nonempty cone
`v>0`, `u/v>max_i|A_i|+2413`, and add the same unused third coordinate
as in the accepted proof. Retain the inherited cutoff condition `Q>82`,
and include all primes dividing `D*W` and all nonzero integer differences
`K_s-K_t` below that cutoff. All coefficients, the box,
and this cutoff are fixed after the rational targets and `D` are fixed.

The accepted prime-pattern proof now applies with these integer `K_s`.
Its explicit fibers still have the same equations:

```
p0=p:         Psi_s=c+W*x-K_s*p;
Psi_s0=p:     Psi_s=p+(K_s0-K_s)*p0.
```

Outside the fixed cutoff, the other zero lines on each fiber are distinct.
Thus the same Selberg upper estimates and the same cutoff-first,
box-size-second argument apply. The complexity bound decreases from 39
to at most `m-2<=35`. The existing all-complexity MN and GI inputs already
cover it. The lower and bad-pattern bounds remain

```
c_a,D * X³ / ((log L)^(2m) * (log X)^m),
C_a,D * X³ / (L * (log X)^m) + o_a,D(X³/(log X)^m).
```

Their constants may depend on the fixed rational targets and `D`; this is
allowed by the existential completeness statement. No uniform bound in
target denominators and no growing-modulus prime theorem is asserted.
Choose `L`, then `X`, as in the accepted proof. The same-prime elliptic
order calculation is unchanged. No cross-prime order assertion is used.

The published prime-distribution interfaces are Green--Tao's
[Linear equations in primes](https://annals.math.princeton.edu/2010/171-3/p08),
Green--Tao's [Mobius orthogonality theorem](https://annals.math.princeton.edu/2012/175-2/p03),
and Green--Tao--Ziegler's [inverse theorem](https://annals.math.princeton.edu/2012/176-2/p11).
The exact theorem locators, Mertens and elliptic-curve applications, and
the inherited proof-version convention are those already recorded in
`degree8-original/arithmetic/sieve/source-ledger.json`. No new unpublished
input is introduced by the rational-target extension.

## The square factor at infinity is harmless

Choose the prime lower bound above every prime divisor of `D`. Then the
only prime at which `D²*p0` has odd valuation is `p0`, and its valuation
there is one. The finite raw contacts have valuation one at their own
ordinary prime and no other odd valuation. The existing comparison-point
construction therefore applies to one ordinary prime per occurrence,
exactly as before. It retains private shifts and one common `J`.

There is also no new normalized odd contact at a denominator prime.
For `q|D` outside `S_*`, put `d=v_q(D)>0`. All finite raw contacts are
primes larger than `q`, so `u` is a `q`-unit. We have

```
v_q(v)=2d,    v_q(A_i)>=-d,
v_q(A_i*v)>=d,    v_q(A_i*v-u)=0.
```

Both slopes `u/v` and `(A_i*v-u)/v` have valuation `-2d`. Their differences
from every finite point of `C` have the same even negative valuation, and
their normalized infinity depth is `2d`. Thus denominator primes add no
odd five-contact contribution.

For each comparison occurrence, take the private elliptic points and the
common root approximation deep enough at its selected prime that every
normalized nonconstant norm leaf is integral there. The constant leaf is
on the all-left path. The norm root `N_r` is consequently a unit at that
prime. This argument uses `v_p(r)=1`, which holds for `r=D²*p0` because
`p0` does not divide `D`.

Every raw `r` is positive, and the norm tree with constant leaf one is
positive and nonzero over the reals. Its parity argument `b=r*N_r²` is
therefore positive. At primes other than its selected prime, `v_q(r)`
is even, hence `v_q(b)` is even, even when `N_r` has a denominator. At
the selected prime it is one. Consequently the reduced denominator of
`b` is a square. Every selected prime is congruent to `c` modulo `W`,
so it is a square in `Q_2,Q_3,Q_17`; multiplying by `D²` or `N_r²`
preserves this property. These are exactly the existing seven-witness
parity-completeness hypotheses. No nonzero division or local integrality
condition at a prime dividing `D` has been added.

## Soundness and height inequalities

For arbitrary rational assignments, every normalized odd five-contact of
`u/v` or `(A_i*v-u)/v` still forces an odd valuation of one listed raw
contact. This is the old parity-of-the-common-minimum argument and uses
only the unit differences of the fixed finite branch points outside
`S_*`. It does not require integer targets or the completeness lattice.
All comparison soundness conclusions are therefore unchanged.

If the `K`th powers of the associated radicals divide a nonzero integer
`N`, the accepted height theorem gives

```
h(a_i) < 2*H_* * |N|^(24/K) + 14.
```

Now target the two rational coefficients `a,b` of each unscaled
`x(Q)=a+b*sqrt(2)`. The standard height sum inequality gives

```
h(x(Q)) <= h(a)+h(b)+h(sqrt(2))+log(2)
         < 4*H_* * |N|^(24/K) + 30
         < 5*H_* * |N|^(24/K).
```

The last step uses `H_*>50` and `|N|>=1`. In particular, the original
weaker bound with coefficient `7*H_*` still holds. Keeping that bound
makes the existing two contradiction arguments, precision 64, anchor,
scalar height batch, and Lucas relation apply without numerical changes.

For completeness, choose the target points exactly as before. Their eight
abscissa coefficients are rational. Apply the rational-target lemma to
them directly, choose the common `J`, private comparison points and common
root approximation, and use the parity argument above. The old choice of
an integer clearing denominator `e` and its eight products is unnecessary.

Thus the revised source defines precisely the same rational input set
claimed by the existing arithmetic theorem, with 37 comparisons. This
uses the source theorem's existing arithmetic dependencies. It is not a
new independent verification of those dependencies.

## Count and limitations

Eight rational targets plus one shared base slope give
`1+4*(1+8)=37` raw comparison positions. Within this unchanged two-slope
construction each of the nine slopes needs its four finite contacts and
the common infinity contact. This explains the count; it is not a proof
that no other arithmetic construction can use fewer.

The original source allocates 373 witnesses per comparison subtree:
315 in `q_compare4`, 51 in `q_batch41`, and seven in `q_primeparity`.
Deleting four subtrees removes 1,492 source witnesses. The root also loses
the denominator and its inverse, eight scaling products, and six target
contact coordinates, for a structural source reduction of 1,508 variables.
These counts must be checked by regenerating the source. They do not
measure the savings from the optimized 13,609-variable quartic. A final
quartic reduction on the order of four optimized comparison blocks is
expected, but no new variable count or coefficient bound has been run.

Merging different raw contacts into a product is not justified by this
argument. Odd valuations could cancel, and a single private comparison
point serving several distinct primes would need cross-prime order
compatibility absent from the accepted hypotheses. Nor does this proof
permit deleting any of the four index proxies or replacing the five-contact
height theorem by a smaller branch set.
