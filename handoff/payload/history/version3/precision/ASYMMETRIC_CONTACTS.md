# Beta-only comparisons at the eight A contacts

Status: new arithmetic source proposal. The independent reviewer has checked the two-stage maximum argument provisionally; final source construction, independent replay and expansion remain required. No local transformation of a frozen source certificate is asserted.

This note applies to either reviewed height exponent h=19 or h=18, with its exact constant H and supported high/beta/anchor/scalar tuple. It changes neither the 37 raw contact formulas nor their order. It changes the comparator called at exactly eight positions. All root points, proxies, the Lucas equation, scalar batch, anchor and common auxiliary point remain.

## Exact source interface

Order the root points as A=nP_*, S=sP_*, T=tP_*, Z=zP_*, and the eight rational height targets as their x-coordinate pairs, in that order. The raw positions, numbered from zero, are:

| Positions | Role | Comparator |
| --- | --- | --- |
| 0 | Common infinity v/V0 | Full four-proxy |
| 1..4 | Four finite contacts of common slope u/v | Full four-proxy |
| 5..8 | Four finite contacts for first coefficient of x(A) | Beta-only |
| 9..12 | Four finite contacts for second coefficient of x(A) | Beta-only |
| 13..20 | Eight finite contacts for x(S) | Full four-proxy |
| 21..28 | Eight finite contacts for x(T) | Full four-proxy |
| 29..36 | Eight finite contacts for x(Z) | Full four-proxy |

Thus there are 29 full comparisons and eight beta-only comparisons. Do not deduplicate, multiply, delete or reorder raw positions. Equality of raw values or primes between positions is allowed. The common five positions remain full because every target uses that common slope.

The beta-only comparator has sixteen rational free inputs in this order:

```
beta,
x0(4P_*),x1(4P_*),y0(4P_*),y1(4P_*),
x0(4A),x1(4A),y0(4A),y1(4A),
coeff0(conj(f(J))),coeff1(conj(f(J))),
coeff0(1/conj(z(J))),coeff1(1/conj(z(J))),
theta,epsilon,r.
```

Equivalently select these zero-based indices from the full comparator's thirty-one inputs:

```
[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30].
```

It creates exactly two private primary points H0=h0P_* and Q=mP_*, with differences H0-4P_* and Q-4A. Retain the same compressed primary chart and full difference chart formulas, including every nonzero-abscissa subtraction guard. Use G_(ceil(q/4)-1) for both primary logarithms, where q=12 for the proposed runs. Retain

```
Lambda*p_H=G_H, A_beta=C_beta*p_Q, A_beta*Lambda=G_Q.
```

The five order-one field expressions, in order, are

```
f(H0), f(Q), conj(f(J)),
conj(f(H0-4P_*)), conj(f(Q-4A)).
```

The last three field expressions, all of order q, are

```
C_beta-beta,
conj(z(H0-4P_*))/conj(z(J)),
conj(z(Q-4A))/conj(z(J)).
```

The already-conjugated f(J) and inverse conjugated z(J) are passed as inputs; do not conjugate those inputs a second time. The field order list is `[1]*5+[q]*3`. With the retained first order-one root-error test and the same two rational tests for each field expression, the rational list is `[1]*11+[q]*6`, of length seventeen. It therefore calls a separate q_batch17 with the unchanged constant-left norm rule and pole predicate. For q12 its G polynomials have three coefficients each and use the reviewed `direct/unit/s1`, unbound-output profile. No high-order G polynomial is needed in this comparator.

## Local conclusion at a beta-only contact

Start with an arbitrary rational solution and any p>76176 where this raw r has odd valuation. The same constant-left norm and pole proof first excludes a negative odd valuation and gives the assigned orders for every rational test. The order-one root error selects a split place rho of Q(sqrt(2)). The paired tests transfer to that place exactly as in the released proof.

The two primary points are formal at the selected place, and J and the two differences are formal at the opposite place. Their indices h0,m,j,n are integers and j is nonzero. The two alternate order-q tests give

```
v_p((h0-4)/j)>=q, v_p((m-4n)/j)>=q,
h0=4 mod p^q, m=4n mod p^q.
```

Thus h0 is a p-unit. Both finite logarithms have relative precision q at their actual formal points. The quotient differs from m/h0 by a multiple of p^q, and the primary test gives beta integral and

```
beta=n mod p^q.
```

No conclusion about s,t,z is asserted at this position. No ordinary-prime or distinct-prime assumption was used in soundness. The compressed reverse maps use the same globally nonzero G_J lemma, now J=2 for both points, and preserve every retained external occurrence.

## First global step uses only the Lucas maximum

Put a=abs(s), B_L=max(abs(s),abs(t),abs(z)) and

```
Delta=t^2-s(s-2)*t*z+(s-2)^2*z^2-1.
```

The polynomial Delta contains no n. The 29 full positions include every finite contact of the six coefficients of x(S),x(T),x(Z), and the common finite and infinity contacts needed by all their slopes. The parity-of-the-common-minimum argument therefore detects every normalized odd contact used to bound these six coefficients at a full comparator. If Delta is nonzero, the three high-order proxy congruences and the retained proxy Lucas equation imply p^K divides Delta at each such prime. Hence every associated radical to its Kth power divides abs(Delta).

Choose a point among S,T,Z whose index has absolute value B_L. The same H19 or H18 two-slope height calculation bounds its x-height by `7H*abs(Delta)^(h/K)`. The lower bound is `B_L^2-6`. Since `abs(Delta)<5B_L^4`,

```
B_L^2-6 < 7*5^(h/K)*H*B_L^(4h/K)
        < 16H*B_L^(4h/K).
```

The supported K satisfies K>2h. Thus `B_L^(2-4h/K)<24H`, contradicting `B_L>=a>(24H)^(K/(2K-4h))`. It follows that Delta=0. The same nonzero z and anchor conditions allow the released Lucas lemma, yielding

```
log B_L > a-3.
```

The height of x(A) and the size of n are not used anywhere in this first step. This is the precise reason its eight private finite contact positions do not need the three Lucas comparisons.

## Second global step still controls all four indices

Suppose beta differs from n and put N=abs(num(beta-n)) in lowest terms. Every one of the 37 positions still gives beta=n modulo p^q at each odd raw-contact prime: the 29 full comparators by the prior proof and the eight beta-only comparators by the local argument above. Therefore all normalized radicals for all eight coefficients of x(A),x(S),x(T),x(Z), including the common slopes and infinity, have their qth powers dividing N.

Now use the larger maximum

```
B=max(abs(n),abs(s),abs(t),abs(z))=max(abs(n),B_L).
```

Whichever point realizes B has all required height contacts covered. The same upper/lower x-height estimates give

```
B^2 < 7H*N^(h/q)+6,
N <= 2*exp(h(beta))*B.
```

The latter holds because n is an integer and beta is written in lowest terms; its denominator and numerator are both at most exp(h(beta)), and B>=1. Since alpha=h/q<2,

```
B^(2-alpha)<40H*exp(alpha*h(beta)).
```

The unchanged scalar/anchor argument gives h(beta)<a/40 and log(40H)<a/40. Consequently

```
log B < (q+h)/(40*(2q-h))*a.
```

For the q12 proposals the coefficient is 31/200 for H19 and 1/8 for H18. Both are strictly smaller than 1 and imply log B<a-3 for a>40. But B>=B_L and the first step gave log B_L>a-3. This contradiction proves beta=n. The unchanged X^2=beta-2 denominator argument proves X is an integer.

It would be incorrect to omit the A-height contacts altogether, or to use B_L in the second step without controlling n. This construction retains beta information at all of them and explicitly switches maxima between the two steps.

## Completeness and source boundary

For integral X use exactly the prior scalar, anchor and Lucas choices and the same 37-contact rational-target prime-pattern construction. The common J uses the lcm of reduction orders over all selected distinct primes, including those assigned to beta-only positions. At a full position choose the same five primary points as before. At a beta-only position choose h_p with the prior congruences, even at the stronger common K precision if desired, and take H0=h_pP_* and Q=h_p nP_*. Their two shifted differences are nonzero under the same exclusions. The order-q estimates follow. Both G2 values are nonzero, so the compressed equations have the stated solutions.

Choose theta last at the maximum of every actual rational coefficient requirement across both comparator types. The smaller norm tree still has its constant leaf on the all-left path. The same positive prime or square-times-prime raw contact and sufficiently deep normalized leaves give a positive norm root, square reduced denominator and the local squares required by pole completeness. No different-prime coprimality, shared private primary point, or simultaneous modular condition on a new index is imposed.

This proves the new relation has the same rational input projection Z under the inherited arithmetic inputs. It is not a claim that arbitrary witness tuples of the full and reduced source correspond by merely deleting coordinates: the denominator truncation and norm tree change. The new family needs an explicit source entry, independent construction audit, fresh lift and exact algebraic certificate. Variable 0 is preserved. Counts, coefficient growth, and final savings require the combined run.
