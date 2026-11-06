# Independent review of the exponent-19 precision consequences

Reviewed 2026-11-05. This is a mathematical and source-consumer review of
`DOWNSTREAM_EXPONENT19.md`, SHA256
`f76e1d7ef6086f2ee036312f6b4fbcf70ce89904f212d6212fb2cb82940490ed`.
I compared it with the current manuscript's anchor subgroup, exact norm
tests, common auxiliary point, root approximation, scalar height and final
contradiction arguments, and with the pinned degree-eight builder. No
generation, execution, large computation or shared edit was performed.

No mathematical gap was found. Conditional on the reviewed exponent-19
height theorem and the unchanged arithmetic inputs, all three proposed
high-precision/anchor pairs work with beta precision 10 or 12 and scalar
order 32:

| High precision | Anchor squarings | Beta precision | Scalar order |
| --- | --- | --- | --- |
| 40 | 25 | 10 or 12 | 32 |
| 44 | 24 | 10 or 12 | 32 |
| 48 | 23 | 10 or 12 | 32 |

This conclusion concerns the arithmetic specification. It does not certify
a generated source, logarithm circuit, quadratic lift, coefficient bound
or variable count. The separate 37-contact proposal is outside this review;
the proof checked here retains the original 41-contact construction.

## Odd contact valuations and the scalar batch

The negative-valuation case is handled correctly. For an odd integer
`R=v_p(r)`, nonzero summands of `N_r(a,b)=a^2+r b^2` have distinct valuation
parity, so the valuation of their sum is their minimum. Zero inputs are
handled by infinite valuation. In particular the norm is zero only when
both inputs are zero. Recursing to the constant leaf proves that the root
`W` is nonzero at every relevant odd-contact prime, without a global inverse
for `W`.

The constant leaf stays on the all-left path in the actual builder's tree:
it starts in the first node; each higher level pairs that node on the left
or carries it. Therefore `v_p(W)<=0` if `R<0`. Outside `S_*`, the scalar
multiplier `delta*mu` is a unit. The pole argument has odd valuation
`R+2v_p(W)` and the retained pole predicate forces this to be positive.
It cannot be positive when `R<0`. Thus the proof obtains `R>0` before using
the inequalities that depend on that sign.

Starting with `v_p(W)>-R/2`, descent through a node takes a bound
`v_p(N_r(a,b))>-cR`, `c<1`, to bounds with constants `c/2` and `(c+1)/2`,
both smaller than one. Every normalized leaf therefore has valuation
strictly greater than `-R`. An order-`L` leaf gives

    v_p(X) > (L-1)R >= L-1,

and integrality of the valuation gives `v_p(X)>=L`. This proof works for
every positive integer `L`, including 32, and for negative odd contact
valuations it first gives impossibility rather than incorrectly applying
the positive-`R` inequality.

The scalar batch tests the two rational coefficients of each of
`f(J_0)`, `f(S)` and `z(S)/z(J_0)`. The first four orders remain one.
At every place above a prime outside `S_*`, the integral basis elements
`1,sqrt(2)` show that coefficientwise divisibility by `p` gives positive
valuation of each of the first two field elements. On the retained curve,
negative valuation of `x=1/f` places both points in the formal group.

All these primes exceed 76176, so the field extension is unramified and the
curve has good reduction. Normalize the local valuation by `v(p)=1`.
It restricts to the ordinary rational `v_p` whether the prime splits or is
inert. For nonzero integer indices `J_0=jP_*` and `S=sP_*`, the homomorphism
identity on formal points gives `log(S)/log(J_0)=s/j`. Isometry gives

    v(z(S)/z(J_0)) = v_p(s/j).

The last two coefficient orders 32 therefore imply `v_p(s/j)>=32`.
Since `j` is an integer, `v_p(j)>=0`, and `v_p(s)>=32` follows. No split
root or common-theta argument is needed in this scalar batch.

Every prime in `M_5(beta)` has odd valuation in the unchanged scalar
polynomial. At an infinite contact its valuation is `5v_p(beta)`; at a
finite contact the other factors are units outside `S_*`. The extra root
`1/2` introduces no collision outside that fixed exceptional set. Hence
`M_5(beta)^32` divides the nonzero integer `s`, and

    h(beta) <= H |s|^(19/32).

For actual inputs `beta=X^2+2`, the scalar polynomial is nonzero and beta
avoids the four finite contacts. In fact a negative valuation of beta is
even, but the general negative-odd argument above remains necessary for
the norm specification and does not rely on that extra observation.

## Anchor and scalar height cutoff

Replacing the anchor length by an integer `A` gives exactly the subgroup

    s in 2 * 3^(2^(A-1)-1) Z,  s != 0.

The manuscript's proof at 3 is uniform in the chain length: it compares
`v_3(f(sP_*))=2+2v_3(s)` with `2^A`. The condition at 2 introduces no further
restriction. Thus the proposed anchor bound is valid and the allowed
indices still form a nonzero subgroup with positive representatives.
It can be combined with any finite list of integer divisibility conditions.

The two inequalities (1) in the proposal imply
`a>(24H)^(K/(2K-76))` and `a>(40H)^(32/13)` by
`log_2(3)>3/2`, `log_2(24)<5`, and `log_2(40)<6`.
Discarding the anchor's factor two only weakens the lower bound.
The second cutoff implies `a>40` and

    H a^(19/32) < a/40.

It also implies `log(40H)<a/40`: since `32/13>2`, it suffices that
`40 log(40H)<(40H)^2`. The latter holds at `H=1` and has positive difference
derivative `3200H-40/H` on `H>=1`.

The concrete exact comparisons check as follows:

| K, A | Retained lower bound for log2(a) | First required threshold |
| --- | --- | --- |
| 40, 25 | 25165822.5 | 20939710 |
| 44, 24 | 12582910.5 | (11/3) * 2093971 < 7678000 |
| 48, 23 | 6291454.5 | (12/5) * 2093971 < 5025600 |

The common scalar threshold is `32*2093972/13<5154400`, below every
retained lower bound in the table. These checks are rational comparisons;
no numerical approximation to a large logarithm is needed.

## Local comparisons and shortened logarithms

For the original parameter polynomial, use `m=ceil(e/4)` coefficients.
The first omitted degree is `n_0=4m+1<=65`. At a selected prime, the whole
tail has valuation at least `n_0 v_p(z)`: for degrees below `p`, denominators
are units; for degrees `n>=p`, the original estimate
`n-n_0>=v_p(n)` applies. Division by the nonzero formal logarithm gives
relative precision at least `4m>=e`. The previously reviewed global
nonvanishing proof works for every finite truncation, including three
coefficients.

For the reciprocal-coordinate polynomial, the earlier proof also extends
to every proposed order: `m<=16` is the bound used for its entire tail,
and `J=m-1>=2` is exactly the lower bound required for global nonvanishing.
In particular beta precision 10 or 12 uses three coefficients and reaches
the endpoint `J=2` without a gap. The high orders 40, 44 and 48 use ten,
eleven and twelve coefficients, respectively.

The field order list has eleven ones followed by
`[q,K,K,K,K,q,K,K,K]`. Including the root error, the rational order list is

    [1]*23 + [q]*2 + [K]*8 + [q]*2 + [K]*6.

The beta numerator uses order `q`; the shared logarithm denominator and
the other three numerators use `K`. The alternate shared-H test also uses
`K`. Thus `h=4 mod p^K` makes `h` a unit, and the other alternate tests give
`m_i=4n_i mod p^(e_i)`. Both full-logarithm ratios and their finite
approximations are integral, with the same residue to order `e_i`, since
`e_i<=K`. This yields exactly the mixed proxy congruences claimed.

The one common theta is still sufficient. Its required approximation
order depends on each coefficient's valuation as well as the test order;
it need not be merely `K`. The proposal correctly chooses it last to meet
the largest of the finitely many actual requirements.

## Both global contradictions

The unchanged 41-contact comparison and the new height theorem give
`h(x(Q))<7H |N|^(19/e)` when all relevant contact radicals to power `e`
divide the nonzero integer `N`. The proof uses the same three rational
heights for `e` and the two coefficients of `ex(Q)`; the residual additive
constant is smaller than 50, and `H>128` is more than sufficient.

For nonzero Lucas defect, the three high-precision proxies at every
contact give the radical divisibilities with `e=K`. This includes the
contacts controlling `A=nP_*`; high beta precision is not used here.
The inequalities in the proposal imply

    B^2-6 < 7*5^(19/K) H B^(76/K) < 16H B^(76/K),
    B^(2-76/K) < 16H+6 <=22H<24H.

The first strict bound uses `K>38` and `7sqrt(5)<16`. The exponent
`2-76/K` is positive, so this contradicts the first anchor cutoff.
The Lucas defect is zero and the unchanged growth lemma gives
`log B>a-3`.

For `beta!=n`, put `N=|num(beta-n)|` in lowest terms. The beta congruences
and integrality give the radical divisibilities with `e=q`. Using
`N<=2 exp(h(beta))B` and `alpha=19/q<2` gives

    B^(2-alpha) < (7*2^alpha+6) H exp(alpha h(beta))
                < 40H exp(alpha h(beta)).

Here `h(beta)>=0`, `B>=1` and `H>=1` justify absorption of the additive
six. Taking logarithms and using both scalar cutoffs gives

    log B < [(q+19)/(40(2q-19))] a <= (29/40)a < a-3.

The rational coefficient decreases for `q>=10`; its value at 10 is
`29/40`. The final inequality needs only `a>120/11`, already implied.
Thus beta equals the integer index `n`, and the unchanged denominator
argument from `X^2=beta-2` proves that the input `X` is an integer.

## Completeness and source consumers

For integral input, the scalar contact polynomial is a fixed nonzero
integer. Choose its sign and small-prime square class as before. Choose
`J_0` deep at every required place, then choose a positive anchor index `s`
with all further divisibilities. Arbitrarily deep choices ensure the
normalized scalar leaves are integral, and vanish where required by the
small-prime correction. This supplies a unit norm root and the same pole
completeness witnesses with order 32. The stronger old finite-depth
construction is still available; no scalar constraint has to be solved
after fixing incompatible index residues.

Next use Lucas existence, clear the four abscissa denominators and choose
the original contact prime pattern. The common comparison index is
`j=lcm d_(p,2)`. Private choices use
`h_p=4 mod p^(K+v_p(j))`, together with the unchanged two reduction-order
conditions. Their compatibility and the exclusions `h_p=0,4,-4` are
unchanged. Nonzero target indices then preserve every subtraction guard.
The lower beta order introduces no new condition. Choose theta last,
evaluate the finite logarithms, and complete the norm/pole witnesses.
This order of choices proves completeness without modifying a previously
fixed target point.

The following actual source consumers must be checked in any implementation:

| Consumer | Required change or invariant |
| --- | --- |
| `q_compare4` primary logarithms | Shared denominator and three Lucas numerators at K; beta numerator at q; lengths use the ceiling rule. |
| `q_compare4` tests and `q_batch41` | Exact mixed field/rational lists above, including both beta positions and the order-one root test. |
| `q_height_batch` | Last two orders change to 32; first four remain one; signed small-prime correction and constant-left norm tree remain. |
| Root scalar call | Same six coefficients in the same order: f(J0), f(S), z(S)/z(J0); its advertised scalar-order metadata must match the actual module. |
| Anchor and flattening | Chain has A squarings and A+1 shared coordinates; q_anchor must reference the resulting final C, including its negative global index. |
| Contacts and point arithmetic | Same S_*, 41 contacts, curve, generator, two doublings, difference guards and common auxiliary parameters. |
| Removed logarithm inverses | Nonvanishing certificate binds the new exact polynomial and its current chart premises; old J=15 source evidence is insufficient. |

The old builder's logarithm function only accepts multiples of four, and
the current reciprocal kernel only supports its earlier selected orders.
In particular its long-circuit normalization uses `a_12`, unavailable in
the new shorter high polynomials. New evaluation circuits and independent
checks are required, not a metadata-only precision edit. Root has confirmed
that separate low-precision circuits are being implemented and that the
current adapter remains restricted rather than silently accepting these
new values.

Subject to those future source and circuit checks, the proposed arithmetic
parameters are justified. No additional arithmetic assumption, height guard,
doubling change, or user approval condition is introduced by this review.
