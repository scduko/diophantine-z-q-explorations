# Precision consequences of the exponent 19 height bound

This is a conditional arithmetic source revision. It assumes the bound in
`PROVISIONAL_EXPONENT19.md` has passed the independent review and has been
accepted for use. It does not authorize a source pin or report a variable
count. The default contact construction here is the existing 41-contact
construction. The separate 37-contact proposal can be combined only after
its own proof and source audit.

Put H=H_19. Thus H>128, log_2(H)<2093966, and

    h(b) <= H M_5(b)^19.

Keep the curve, generator, Lucas equation, pole predicates, norm-batch
semantics, common root approximation, shifts and guards. Use an integer
high precision K with 39<=K<=64 and beta precision q with 10<=q<=K.
Use scalar orders [1,1,1,1,32,32]. Use A anchor squarings, where

    (3/2)(2^(A-1)-1) > K*2093971/(2K-76),
    (3/2)(2^(A-1)-1) > 32*2093972/13.            (1)

These inequalities imply the three cutoffs

    a=abs(s) > (24H)^(K/(2K-76)),
    a > (40H)^(32/13),
    a > 40.                                     (2)

The anchor gives the stronger exact divisibility
s in 2*3^(2^(A-1)-1) Z, with s nonzero. Inequalities (1) deliberately
discard its factor two and use only log_2(3)>3/2. The bounds
log_2(24H)<2093971 and log_2(40H)<2093972 explain every constant.

## The scalar order can be 32

The accepted norm argument applies to arbitrary positive integer orders.
In particular, put R=v_p(r(beta)) and recall that the scalar multiplier
delta*mu is a p-unit outside S_*. If R is odd and negative, the constant
leaf on the all-left path forces v_p(W)<=0, contradicting the pole
condition v_p(delta*mu*r(beta)*W^2)>0. Hence R is positive. Descending
the norm tree gives v_p(X/r(beta)^L)>-R for an order-L leaf. Consequently
v_p(X)>(L-1)R>=L-1 and v_p(X)>=L. This proves that changing 48 to 32
gives exactly order32 on each scalar coefficient, even when soundness
starts with an arbitrary rational beta. It does not presume positivity
of the contact valuation before applying the pole condition.

The scalar norm batch applies to both rational coefficients of
f(J_0), f(S), and z(S)/z(J_0). For any prime p outside S_* at which
r(beta) has odd valuation, its order-one tests put J_0 and S in the
formal group at every place above p. At any such place, write J_0=jP_*
and S=sP_*. The integer j is nonzero. If d is the order of the reduction
of P_*, both j and s are divisible by d. Formal logarithm isometry and
linearity give

    v(z(S)/z(J_0))
      = v(log(S)/log(J_0))
      = v(s/j).

The order-32 coefficient tests force this valuation to be at least 32.
Since j is an integer, v_p(s)>=32. The extension is unramified at p>2,
so the valuation restricted to Q is the ordinary v_p. This also works
when p is inert; no choice of a split root is used in the scalar batch.
The unchanged contact polynomial r(beta) has odd valuation at every
prime of M_5(beta), including an odd contact at infinity. Therefore

    M_5(beta)^32 divides s,
    h(beta) <= H a^(19/32) < a/40,               (3)

where the last step follows from (2). Scalar completeness is the same
finite divisibility construction: choose J_0 deep enough and then choose
s so that v(s/j)>=32 at the finitely many required primes. All original
small-prime sign and square-class choices remain available. The original
order-48 proof already asserts arbitrarily large finite valuations for
these same leaves, so lowering their required order adds no obstruction.

Also log(40H)<a/40. Indeed a>(40H)^(32/13)>(40H)^2, and
40 log(40H)<(40H)^2 for H>=1. For the latter inequality, at H=1 the
left side is less than 160 and the right side is 1600; the derivative
of their difference is 3200H-40/H>0.

## Local comparison precision

Use the finite logarithm at order K for the shared denominator and three
Lucas numerators, and at order q for the beta numerator. For the original
z-polynomial this means

    L_e(z)=z sum_(j=0)^(ceil(e/4)-1)
               (-1)^j binom(2j,j) D^j z^(4j)/(4j+1).

The previous local-tail proof applies unchanged: for m=ceil(e/4),
the first omitted degree is 4m+1<=65 and, at p>76176 with v_p(z)>=1,

    L_e(z)/log_E(z) is in 1+p^(4m) Z_p,

hence in 1+p^e Z_p. Coefficient-field embeddings do not alter the
valuation argument. The uniform original-polynomial nonvanishing proof
remains available if its inverse is eliminated algebraically.

If the separately audited reciprocal-coordinate logarithm is used,
take exactly its polynomial G_J(D f^2), with J=ceil(e/4)-1. Here e>=10
implies J>=2, which is precisely enough for its global nonvanishing
proof. Its tail proof uses m<=16 and gives the same p^e estimate.
Thus q=10 or 12 uses three coefficients, not four. This statement is
about the polynomial length, not a claim about a compiled gate count.

Assign order q to the primary beta comparison and its alternate shift
comparison. Keep order K on the other seven high-order field tests.
Keep all eleven order-one field tests and the order-one root test.
In the current field ordering the list is

    [1]*11 + [q,K,K,K,K,q,K,K,K].

The alternate H test implies h==4 mod p^K. The other alternate tests
imply m_i==4n_i mod p^(e_i), with e_1=q and e_2=e_3=e_4=K.
Consequently h is a p-unit, and the formal logarithm and finite-tail
estimates give

    beta==n mod p^q,
    (xi,tau,zeta)==(s,t,z) mod p^K.              (4)

All proxies are integral at the selected prime. Completeness uses the
same private CRT choice h_p==4 mod p^(K+v_p(j)), since q<=K, along with
the existing reduction conditions. Exclude h_p=0,4,-4 to preserve every
guard. Choose the common root approximation last at the largest of its
finitely many required precisions. These are the same finite compatibility
arguments as before.

## The two global contradictions

The shared-coordinate calculation, now with exponent 19, gives

    h(a_i)<2H abs(N)^(19/e)+14,
    h(x(Q))<7H abs(N)^(19/e),                   (5)

when the corresponding coordinate radicals have their eth powers
dividing a nonzero integer N. The fixed constants and the inequality
H>128 absorb the same additive terms as in the accepted calculation.
No coordinate-field degree changes. If the 37-contact proof is separately
accepted, its stronger bound with coefficient 5 implies (5) as well.

Let B=max(abs(n),abs(s),abs(t),abs(z)) and

    Delta=t^2-s(s-2)tz+(s-2)^2 z^2-1.

If Delta is nonzero, (4) gives the Kth-power radical divisibilities.
Using the unchanged index-height bound and abs(Delta)<5B^4 gives

    B^2-6 < 7H abs(Delta)^(19/K)
          < 7*5^(19/K) H B^(76/K)
          < 16H B^(76/K).

The last strict inequality follows from 19/K<1/2 and 7sqrt(5)<16.
Since B>=a>40 and H>=1, division by B^(76/K) yields

    B^(2-76/K) < 16H+6 <=22H<24H.

As K>38 this contradicts the first cutoff (2). Thus Delta=0, and the
unchanged Lucas growth lemma gives log B>a-3.

If beta is not n, put N=abs(num(beta-n)) in lowest terms. The beta
congruence in (4) gives the qth-power radical divisibilities, so

    B^2 < 7H N^(19/q)+6,
    N <= 2 exp(h(beta)) B.

Write alpha=19/q<2. Since B,H>=1,

    B^(2-alpha) < 40H exp(alpha h(beta)).

For example the coefficient is bounded by 7*2^alpha+6<34<40.
Combining this with (3) and log(40H)<a/40 gives

    log B < q/(2q-19) log(40H) +19/(2q-19) h(beta)
          < (q+19)/(40(2q-19)) a
          <= (29/40)a < a-3.

The fraction decreases for q>=10, so its maximum is at q=10. The last
inequality follows already for a>120/11, and (2) is stronger. This
contradicts Lucas growth. Therefore beta=n is an integer and, from
X in Q and X^2=beta-2, the rational input X is an integer.

For the converse, retain the original integral-input construction.
Choose the scalar data with order32, choose s in the anchor subgroup
with all required additional divisibilities, and apply Lucas existence.
Clear abscissa denominators and use the original prime pattern. The
private CRT choices described above and common root approximation meet
all changed precisions. Evaluate the chosen finite logarithms and their
ratios, and use the unchanged norm and pole completeness statements.
This constructs a witness for every integer input.

## Concrete choices and remaining work

Each row satisfies (1), with either q=10 or q=12 and scalar order32:

| High precision K | Anchor A | Retained anchor lower bound for log_2(a) |
| --- | --- | --- |
| 40 | 25 | 25165822.5 |
| 44 | 24 | 12582910.5 |
| 48 | 23 | 6291454.5 |

For the strongest first threshold in the first row,
K*2093971/(2K-76)=20939710<25165822.5. In the second row the threshold
is (11/3)*2093971<7678000. In the third row it is
(12/5)*2093971<5025600. The scalar threshold in all rows is
32*2093972/13<5154400. These are rational comparisons, not floating-point
assumptions.

All these choices require a new arithmetic source and its exact lift.
The source audit must bind both changed beta tests, the common denominator
precision, all three Lucas numerator precisions, the two scalar orders,
and the anchor length. Existing circuit identities and deletion rules
must be rechecked against that source. None of the displayed precision
choices by itself proves a new quartic variable count.

The current reciprocal-logarithm adapter is pinned to its audited
high-precision64 source shape and block normalization. Its unchanged
scalar-batch and anchor checks intentionally reject these new sources.
Adoption must update those source checks and construct the appropriate
new polynomial circuits. Replacing a precision field or coefficient list
in an old certificate is insufficient.
