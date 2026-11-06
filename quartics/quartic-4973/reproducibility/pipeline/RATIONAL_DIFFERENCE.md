# Four-field rational difference chart

This research proposal changes the comparison source, but leaves the root
points, all root doubling chains, height targets, scalar batch, anchor,
contact positions, arithmetic constants and logarithm polynomials unchanged.
It starts with the 13/8/16 three-mode source, which has 145 private primary
points and five shared targets. Version 3 is not changed.

## Equations and domain

Write `K=Q(sqrt(2))`, `d=3-sqrt(2)`, `D=d^2`, and
`E: y^2=x^3-Dx`. Both embeddings of D are positive. The accepted group
identification is `2E(K)=Z P_*`; the torsion subgroup consists of the four
rational two-torsion points. Each shared target remains an actual retained
quadruple `Q=[4n]P_*=(a,b)` of a nonzero root point in this group. The boundary
supplies `F=1/a`, `q=b/a`. In particular a,b,F,q are nonzero.

A private primary point uses three field pairs f,x,p with

    x f=1,                  p^2=x-Df.                    (P)

The existing G equations remain verbatim. Their global nonvanishing proof
applies to every f in K, without assuming that f is a square. To recall it,
the constant coefficient is 1, and each nonconstant coefficient of G2 and
G9 has dyadic valuation 1. Since the valuation of f is a half-integer and
D is a unit, if v(f)>=0 the constant term has strictly least valuation;
if v(f)<0 the final term has strictly least valuation. The degrees 2 and 9
are both at least two, so the final valuation in the latter case is
negative. Thus G never vanishes. The retained ratio equations therefore
force every p nonzero. Hence `P=(x,xp)` is a nonidentity, non-two-torsion point
of E(K). We no longer impose that f is a square or that P belongs to 2E(K).

Let J be the unchanged common nonzero point, and let the boundary value be
`jz=1/conj(z(J))`, which is nonzero. Introduce four field pairs t,M,T,A and
impose

    t=f F,
    M(1+D t)=p,
    T=2x-pq+2M(q-p),
    A conj(T)+conj(q-p) jz=0.                            (R)

Every rational component is quadratic. The alternate field test is A at
its original order e. There is no separate difference formal field test.
All primary formal tests, the conjugate f(J) test, primary ratio tests,
root-error test and norm/pole guards remain.

For proof notation put `B=1+D fF`, `k=q-p` and `Z=-k/T`.
The second equation and p nonzero imply B nonzero. The rational graph
domain for the forward construction is B nonzero and the following
formula for T nonzero. The circuit forces both conditions in the reverse
direction, as proved below. The explicit forward map on this domain is

    t=fF, M=p/B, T=2x-pq+2pk/B,
    Z=-k/T, A=conj(Z) jz.                               (F)

Conversely the four equations force exactly these values. No division by
k, x-a, an index difference, a difference logarithm or A occurs.

## The rational function and its exceptional cases

The function Z in (F) is `z(P-Q)=-x(P-Q)/y(P-Q)`, with `z(O)=0`.
For x different from a use the ordinary chord with slope
`L=(xp+aq)/(x-a)`. Substitution of `p^2=x-D/x` and `q^2=a-D/a` gives

    X=L^2-x-a, Y=L(x-X)-xp,              T X=(q-p)Y.

This is an identity of rational functions on E times E; a tiny independent
Laurent-polynomial reduction checks its cleared numerator. That test passes,
as do 32 exact valid K-point examples, two excluded B-zero examples and
the two nonidentity pole examples. The valid examples include equality,
opposition, a half-generator and its torsion translates. On the curve
z is regular away from `(d,0)` and `(-d,0)`, and extends to zero at O and
`T0=(0,0)`. The formula agrees on its open chord domain and hence wherever
both rational functions are regular.

The circuit itself guarantees T nonzero. If T=0, the last equation, with
jz nonzero, gives k=0. Then p=q, and the curve relations give
`(x-a)B=0`. Since B is nonzero, x=a and P=Q. But at that point

    T=2x-p^2=x+D/x=(x^2+D)/x,

which is nonzero because x^2+D is positive at both real embeddings.
Thus the circuit has no solution with T zero. The two remaining poles
can also be excluded directly, without an extension argument. If
`P=Q+(s,0)` with s=d or s=-d, the addition formulas give

    x=s(a+s)/(a-s), y=-2D b/(a-s)^2, pq=-2s,
    ax=s(x+a+s).

All denominators are nonzero because Q is not two-torsion. Using these
identities and p^2=x-D/x yields

    BT=(2x-pq)B+2p(q-p)
      =2[-s+D(x+a+s)/(ax)]=0.

On the specified B-nonzero domain this forces T=0, which was excluded.
Also k cannot vanish there, since k=0 and B nonzero would give P=Q.
It also cannot happen that P-Q=T0:
translation by T0 has `x(P)=-D/a`, which would give B=0.

At P=Q the circuit has k=Z=A=0 and the displayed nonzero T. It represents
the identity difference. At P=-Q it represents the double of P; the
equal-abscissa division was not used in the circuit. Such a double lies
in the torsion-free group 2E(K), so it is not a nonzero two-torsion point.
All four inputs x,p,a,q remain nonzero in these cases.

The locus B=0 is deliberately excluded. It can contain private primary
points in the enlarged ambient E(K), but no old complete witness used
below, because its original primary and target abscissas are positive at
both real embeddings. We claim input-projection equivalence, not a map
from every possible tuple of arbitrary E(K) points into this chart.

## Local effect of the alternate test

Fix one split good odd prime selected by the unchanged norm/pole argument.
Its size is greater than 76176, so D and 2 are units. Evaluate the alternate
tests at the conjugate place. The unchanged common f(J) order-one test
puts J in the formal group, and J is nonzero, so z(J) is nonzero and
`v(z(J))>0`. The A test of order e gives

    v(Z)=v(A)+v(z(J)) >= e+v(z(J)) > 0.                  (L)

The statement includes Z=0 with infinite valuation. It does not assume
any coefficientwise integrality before the paired rational tests have
been decoded at the selected root of 2.

Here is the needed local replacement for a separate formal test. If
R=(X,Y) is a nontorsion affine point and `v(z(R))>0`, then

    z(R)^2=X/(X^2-D).

If v(X)=0, the right side has nonpositive valuation, a contradiction.
If v(X)<0, R lies in the formal group. If v(X)>0, translate by T0:

    X'= -D/X,            Y'=D Y/X^2,
    z(R+T0)=-z(R).

Then v(X')<0, so R+T0 lies in the formal group with the same parameter
valuation. Thus R is formal after translation by either O or T0.
The identity case uses O itself. The other three torsion possibilities
have already been excluded by the circuit. In particular [2]R is formal
and formal logarithm isometry and homomorphism give

    v(log_E([2]R))=v(z(R)),                              (D)

because 2 is a unit. We use the usual convention of infinite valuation
for the identity. No logarithm of a nonformal point is asserted.

## Half-integer indices and the unchanged local conclusions

Every primary P has a unique half-integer index alpha(P) determined by

    [2]P=[2 alpha(P)]P_*,       alpha(P) in (1/2) Z.

This uses only the accepted equality 2E(K)=Z P_*, not an additional
descent or choice of rational half of an arbitrary point. All these
indices are integral at the selected odd prime. The root target
Q=[4n]P_* has alpha(Q)=4n. Put alpha(P0)=h and alpha(Pi)=m_i.

For R=Pi-Qi the doubled index is `2(m_i-4n_i)`. From (D), from J=[j]P_*
formal and nonzero, and from the homomorphism on the formal group, one
obtains

    v(Z(R)/z(J))=v((m_i-4n_i)/j).                        (I)

To justify comparing logarithms even if P_* itself is not formal, note
that both [2]R and J are formal and their integer multiples satisfy
`[j]([2]R)=[2(m_i-4n_i)]J`. Apply the formal logarithm to this equality.
Since 2 and j are nonzero rationals, division is legitimate. The same
argument applies when the difference is the identity.

The old integer j is nonzero, so `v(j)>=0`. Hence the unchanged alternate
orders imply

    h=4 mod p^e0,             m_i=4n_i mod p^ei.

In particular h is a p-adic unit. Each primary is already formal at the
primary place by its retained f test. The exact relation there is
`[4h]Pi=[4m_i]P0`. Both coefficients are integers, and the equality follows
by applying the defining doubled-point identities. Taking logarithms gives
`log(Pi)/log(P0)=m_i/h`. A relation with coefficients 2h and 2m_i is not
asserted, since it could differ by two-torsion before formal membership
is used. The denominator is
nonzero because a nonzero formal point in characteristic zero has
nonzero logarithm. The same reciprocal G approximation, same orders
ei<=e0, and same primary ratio tests therefore give the original local
conclusions `b_i in Z_p`, `b_i=n_i mod p^ei`.

No later height, radical or Lucas step uses integrality of the private
h,m_i outside this selected odd prime. The root indices n,s,t,z remain
the unchanged ordinary integers. Thus those steps give exactly the same
integral-input soundness theorem. This paragraph requires independent
checking against the complete selective-source proof; it is not a new
claim that the old private-point projection is unchanged.

## Completeness and the arithmetic/finite boundary

For integral input use the existing construction's primary points in
G=2E(K), its shared quadruple targets, common point J, contact primes and
private congruence choices. In particular the primary and target f,F are
positive at both embeddings, so B=1+DfF is nonzero. Their differences
are formal at the assigned conjugate places and avoid the old affine
subtraction exceptions by the old choices of indices. Formula (F)
therefore constructs the four new field pairs. A is exactly the old
alternate ratio, so all its prescribed inequalities remain true.

Only after all actual field-test coefficients are fixed choose the
single theta by the old finite CRT argument. This handles denominators
in M,T,A and permits negative valuations of individual rational field
coefficients. Each reduced norm tree keeps its constant leaf on its
all-left path, and all retained leaf orders and pole witnesses are
constructed with the same prime and the same local square conditions
at 2,3,17. Removing the separate difference tests removes leaves; it
does not weaken a retained pole or invert a new vanishing expression.

The proof above establishes the arithmetic input projection. A future
finite auditor must independently reconstruct every ordered equation,
arithmetic definition, call, module boundary and flattened row. It must
pin the unchanged root, scalar, anchor and G circuits, verify all three
new batch lists and retain every nonzero premise used here. Such a
finite audit alone would not prove the half-index/local argument.

## Expected structural effect

The frozen minimal source allocates r,v,w,T,Z and the alternate ratio,
six field pairs per site. The proposed source allocates t,M,T,A, four.
Across 145 sites the raw difference is 580 rational coordinates.
Removing each difference's separate formal field test changes the
rational batch lengths from 41,17,33 to 31,13,25 for full,beta,Lucas.
Any saving in subsequent norm and elimination coordinates needs an
actual combined generation and replay. These counts are not additive
to independently measured optimizations.
