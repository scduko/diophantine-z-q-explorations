# Why odd labels let one height control four points

This explains upstream's Version 9 refinement, now included in Version 10.
It supplements the earlier intuitive proof; it does not claim an independent
proof of the inherited elliptic group, height or prime-pattern theorems.

## The elementary height mechanism: prevent cancellation place by place

For nonzero algebraic numbers x1,...,xr, suppose that at each place all
logarithms of their absolute values have the same weak sign. Then

    max(0, sum_i log|xi|_v) = sum_i max(0,log|xi|_v).

Summing with the normalized local weights gives

    h(product_i xi) = sum_i h(xi).

Usually this fails: a large factor can cancel a small one. The new
construction makes it true for abscissae of odd multiples of the chosen
elliptic generator. Therefore the height of one product controls every
factor's height, exactly, with no additional constant.

Why odd multiples? At a place with v(D)=0, work in the finite quotient
by the formal subgroup. Negative valuation of the abscissa means the
point is in that subgroup. Positive valuation means it lies in the coset
of the two-torsion point T0=(0,0), using x(Q+T0)=-D/x(Q).
If the generator's image has odd order, its cyclic subgroup cannot
contain this order-two element. If its order is even, an odd multiple
cannot be the identity. Either way, all odd multiples' abscissa valuations
have the same weak sign at that place.

At the exceptional place dividing D, upstream instead proves that the
generator has nonsingular reduction and its multiples stay in that
subgroup; positive abscissa valuation would be singular, so it cannot
occur. At both real embeddings the relevant abscissae exceed one. These
facts close the local gaps in the elementary no-cancellation argument.
The formal and nonsingular subgroup assertions require their stated
elliptic-curve hypotheses; parity alone does not prove them.

## From nine height detectors to three

Previously four abscissae, each with two rational components, needed
eight scaled detectors plus an unscaled one. Now form

    C=product_i x(Qi)=C0+C1*sqrt(2).

Only the scales 1, C0² and (1+C1²)² are needed to bound h(C). The exact
height identity bounds each h(x(Qi)) by h(C), so the same contradiction
argument applies to all four integer labels. This is the source of the
large detector reduction; it is not justified for unrestricted labels.

Quadratic odd-coset chart equations enforce those labels. Completeness
also changes: beta=2X²+3 is odd for integral X, the scalar construction
uses S-P=(a-1)P so a can be odd while a-1 is highly divisible, and the
Lucas recurrence supplies odd t,b. Once the labels are fixed, the three
scales are fixed positive rational squares before contact primes are chosen.

For soundness, integral beta still forces rational X to be integral:
if X=u/v is reduced, v² divides 2u², hence v² divides 2 and v=1.
The odd input convention does not introduce fractional half-integer inputs.

## Replace precision in a formula by depth of the point

Near the identity, write z=-x/y and r=v(z). The formal logarithm obeys

    log(Q)/z(Q) = 1 + an error of valuation at least 4r.

Thus a point deep enough in the formal group needs no correction
polynomial to reach the required accuracy. The new source requires the
primary anchor H to have r>=20. The cross tests first transfer
integrality between the primary and alternate ratios. Only then does
integrality of z(Ui)/z(H) imply r(Ui)>=20. This order matters: asserting
the stronger error before integrality would leave a gap.

The primary ratios then have error at least 80; alternate ratios retain
their G9 logarithms with error at least 40. Subtracting the two integer
index equations recovers the labels modulo p^40, as before.

Completeness must produce the deeper points. The common index h gains
a factor p^19 at each primary contact. Compatibility requires these p's
to avoid the opposite reduction orders. Upstream proves that separation
by removing a thin part of its prime-pattern count and applying Hasse's
bound. It is a further consequence to check in the inherited analytic
argument, not an automatic consequence of CRT. Trying to deepen both
sides would generally require p to divide both h and h-1 and fails.

## Precise map to the full proof

All labels below occur in `docs/quartic-523-540/addition.tex` and the
integrated manuscript.

| Blackboard step | Source label |
| --- | --- |
| Exact product height | `v9:lem:product` |
| Three scales and unchanged height constant | `v9:cor:scales`, `v9:eq:height-transfer` |
| Odd-coset equations and their converse | `v9:prop:odd-chart` |
| Odd labels and shifted scalar construction | `v9:sec:labels` |
| Integrality before deeper error estimates | `subsec:v9-local-depth` |
| Separation of primes and opposite orders | `v9:lem:separation` |
| Compatible deeper common witness | `subsec:v9-deep-completeness` |
| Finite quartic and certificate construction | `subsec:v9-finite` |

The existing local-to-global height theorem and simultaneous-prime
construction remain essential. The parity and no-cancellation mechanism
is a genuine conceptual simplification of the detector architecture;
it does not replace those deeper inputs with elementary arguments.
