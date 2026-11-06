# From CPO to one shared comparison core

**6 November 2026.** This is the completeness bridge for the shared-comparison
proposal based on Version 2, commit `28e87b1b62af0effd954605af7f70b2699dd5672`.
It supplements the proposed [CPO proof, version 2](CPO_PROOF_V2.md), retaining
the arithmetic inputs of the original manuscript. It is not an independent
proof of those inputs.

## Statement

For each integral input $X$, the witnesses in the completeness construction of
Version 2 can be chosen so that all ordinary contacts use the same comparison
core. Only the norm-batch witnesses remain private to each contact. Together
with the exact source-identification check, this gives the same $X$-projection
as the pinned source, subject to the manuscript's arithmetic inputs and CPO.

## Choice of points and precision

Keep the scalar height data, anchor, Lucas indices, proxies, and denominator
chosen in the original completeness construction. Write the four nonzero
target indices as $n_1,n_2,n_3,n_4$, and put $n_0=1$. At the ordinary-pattern
step use CPO for these fixed targets, removing repeated affine forms first.
Retain any fixed congruence restrictions needed by the original construction.
Choose the resulting primes larger than the original lower bounds, including
$76176$. Repeated occurrences of a prime use the same orientation.

Let $\mathcal P$ be the set of distinct selected primes, orient the two places
as in CPO, and put
$$
j=\operatorname{lcm}_{p\in\mathcal P}d_{p,2}>0,\qquad J=[j]P_*.
$$
Only after this finite set and $j$ have been chosen, choose an integer
$$
N\ge\max_{p\in\mathcal P}(64+v_p(j)).
$$
The pattern supplied by CPO works for every precision $N$: its coprimality
conditions do not depend on $N$. The generalized CRT therefore gives one $h$
with
$$
h\equiv0\pmod{d_{p,1}},\qquad h\equiv4\pmod{d_{p,2}},\qquad
h\equiv4\pmod{p^N}\quad(p\in\mathcal P).
$$
The solution set is an infinite arithmetic progression, so choose
$h\notin\{0,4,-4\}$ as required by the original nonzero and subtraction
guards. Define, once for all contacts,
$$
Q_0=[h]P_*,\qquad Q_i=[hn_i]P_*,\qquad
Y_i=[(h-4)n_i]P_*\quad(0\le i\le4).
$$
At each primary place the $Q_i$ are formal; at the opposite place $J$ and the
$Y_i$ are formal. The original formal-logarithm argument gives
$$
v_p\!\left(\frac{z(Y_i)}{z(J)}\right)
=v_p\!\left(\frac{(h-4)n_i}{j}\right)\ge64,
\qquad \frac{\log(Q_i)}{\log(Q_0)}=n_i.
$$
The reciprocal-log estimates then give all the original primary comparison
conditions, including the precision-$16$ beta condition and the remaining
precision-$64$ conditions. These are exactly the uses of the private $h_p$
in `subsec:o8-common-J-proof` and the reciprocal-system completeness proof.

## Common chart and approximation witnesses

The point coordinates just chosen are global elements of $K=\mathbb Q(\sqrt2)$,
not separate local coordinates. Choose their original chart witnesses once,
using the original chart-completeness construction. Every contact now has
the same input points and uses these same witnesses. The nonzero guards and
`lem:quartic-reciprocal-nonzero` make the required inverses defined.

Apply the explicit solution map in `lem:quartic-compressed-primary` once to
these charts: $p_i=y_if_i$, $\Lambda=G_0/p_0$, and $A_i=C_ip_i$.
All compressed coordinates, subtraction-chart witnesses, and reciprocal-log
witnesses are consequently common. Every equation in `q_compare4_core` is
independent of the contact radical; the source builder checks that the radical
occurs only as the norm-batch input in the original block.

Choose the common integer $\theta$ last. For each selected prime let $\rho_p$
be the root of two corresponding to its chosen primary place. For every field
test $A+B\sqrt2$ of assigned order $e$, impose, when $B\ne0$,
$$
v_p(\theta-\rho_p)\ge\max(1,e-v_p(B)),
$$
and in all cases impose precision at least one for the root test. There are
only finitely many requirements at each prime, and CRT realizes their maximum
simultaneously. Since $\theta+\rho_p$ is a unit, the field-test bounds imply
$$
v_p((\theta^2-2)B)\ge e,\qquad v_p(A+\theta B)\ge e.
$$
Thus the forty exported rational tests, together with the root test, can be
used unchanged in every contact batch. This is the argument of
`subsec:o8-root-proof`, now applied to one common set of field tests.

## Private norm batches

For each contact, its radical is the selected positive prime in the original
progression. All normalized nonconstant leaves of its norm batch are integral
at that prime. The constant-left construction gives a unit root there and a
positive, nonzero real root. The pole argument therefore has square reduced
denominator and is locally square at $2,3,17$, as in the original completeness
proof. The specialized parity-completeness lemma supplies that batch's own
witnesses. No equality between these batch witnesses is imposed or needed.
In particular the comparison points acquire no new integrality requirement
at $2,3,17$.

This constructs one shared core and all the separate norm batches. The
remaining source modules are unchanged, completing the claimed implication
from an integral input to a solution of the shared source.
