# Elimination over retained equations and certified units

This packet changes only the algebraic presentation of the released source.
It does not change its arithmetic parameters or accept a different source.
All polynomial identities are over the rational numbers. Input variable 0
is never eliminated.

## Nonzero factors

An affine factor A may be used as a denominator only after a finite proof
from equations retained unchanged and not containing the removed variable.
The checker supports these cases:

1. An equation A*w=c with nonzero rational c proves A nonzero.
2. An equation proportional to E-theta^2+2 proves E nonzero. If a rational
   theta=a/b in lowest terms had theta^2=2, then a^2=2b^2 forces a even,
   and then b even, a contradiction. Therefore E=theta^2-2 is nonzero
   at every rational solution. There is no real-solution assertion here.
3. In a two-term equation c*M=d*N, with both coefficients nonzero, if all
   variable factors of N have already been proved nonzero, all variable
   factors of M are nonzero.
4. A retained equation proportional to B*C-c*M, where c is nonzero and
   all variable factors of M are already nonzero, proves B nonzero. A
   nonzero rational multiple A of B is nonzero too. B and C are affine.
   The new producer uses this for R*(F-1)=E^2. It neither assumes F
   nonzero nor assumes E is a positive quantity.

Each child proof is checked recursively, using current rows. Cycles and
proofs longer than 256 recursive steps are rejected. A proof cannot use any
row containing the coordinate being eliminated. Thus no proof relies on
an equation which is removed or replaced by this operation. The product
identity must be a nonzero polynomial, excluding tautological certificates.

## Exact elimination identity

Choose a defining row proportional to A(y)*x-N(y), where x is a witness,
A is nonconstant affine, N has degree at most two, and neither contains x.
Prove A nonzero as above. Let J be every other current row containing x;
the checker computes J from current incidence rather than trusting a list.

For j in J write k_j=degree_x(F_j), so 0 <= k_j <= 2, and form exactly

    T_j(y) = A(y)^k_j F_j(N(y)/A(y), y).

The certificate supplies unchanged x-free support rows H_jh, rational
polynomial multipliers M_jh of degree at most two, a quadratic x-free row
G_j, and zero or more certified nonzero affine factors U_jl. The checker
requires the polynomial identity, up to one nonzero rational constant,

    T_j - sum_h M_jh H_jh = c_j G_j product_l U_jl.

All variables must already be allocated. Support indices are unique for
each row, not part of any changed row, and checked against current rows.
All factors' nonvanishing proofs are checked against current unchanged
rows. Every row in J must have exactly one replacement; there are no extra
patches. The defining row is replaced by zero. The remaining rows stay
unchanged. Constant-pivot relation_eliminate is the existing special case
with a nonzero constant A and no unit factors.

Forward map: omit x. At an old solution the retained supports vanish and
T_j=0. The nonzero factors then force G_j=0, including the case that G_j
is identically zero.

Reverse map: set x=N(y)/A(y). Every proof row is retained and x-free, so
A and each U_jl remain nonzero at every new rational solution. The defining
equation holds. Each support vanishes and each G_j vanishes, so T_j=0.
Dividing by the nonzero A^k_j gives F_j=0. Other rows are unchanged.
This proves equality of projections onto input0 in both directions.

## Search implementation and exact limits

The producer first divides T_j by available certified affine factors when
exact polynomial division succeeds. It then solves the remaining terms of
degree above two as a rational linear combination of monomial multiples
of retained quadratic support rows. If P is the divided factor product
and M a multiplier in this quotient identity, the certificate records P*M
in the original identity. Multipliers exceeding degree two are rejected.
This is a bounded heuristic; failure says nothing about existence of a
different presentation.

Rows are normalized by nonzero rational constants only. The producer
maintains the full unweighted sum of squared rows and checks every changed
coefficient strictly below 2^80. Both producer entry points reject parents
whose stored weights are not all one. Exported rows are integral and at
most quadratic. The separate full checker reconstructs the named source,
replays all old and new operations, compacts variables with input0 fixed,
and compares the complete expanded quartic and coefficient bound. The
producer's own report is never an acceptance certificate.

The structural census does no sum-of-squares expansion. Its counts are
not an equivalence proof. Source labels serve only to explain cost; none
are used to justify a transformation.
