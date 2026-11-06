# Three comparator modes using the growing T index

Status: separate arithmetic source proposal, extending `ASYMMETRIC_CONTACTS.md`. The earlier 29-full/8-beta-only source remains a distinct candidate. This note changes its partition to thirteen full, eight beta-only and sixteen Lucas-only positions. The independent reviewer has checked the argument provisionally; a final source audit and full finite verification remain necessary.

Use exactly the same root point order A=nP_*, S=sP_*, T=tP_*, Z=zP_*; eight unscaled rational height targets; and 37 raw contact formulas. Keep the same H19 or H18 height theorem and its reviewed high K, beta q=12, anchor and scalar tuple. This construction does not remove any raw position or assume distinct contact primes.

## Partition and exact module interfaces

| Zero-based raw positions | Target role | Comparator |
| --- | --- | --- |
| 0..4 | Common infinity and common finite slope | Full four-proxy |
| 5..12 | Two coefficients of x(A) | Beta-only |
| 13..20 | Two coefficients of x(S) | Lucas-only |
| 21..28 | Two coefficients of x(T) | Full four-proxy |
| 29..36 | Two coefficients of x(Z) | Lucas-only |

The beta-only interface, point charts, field list and q_batch17 are exactly those in `ASYMMETRIC_CONTACTS.md`. The thirteen full positions use the full four-proxy comparator without alteration.

The Lucas-only comparator has 26 rational inputs, in this order:

```
xi,tau,zeta,
flat(4P_*), flat(4S), flat(4T), flat(4Z),
coefficients(conj(f(J))), coefficients(1/conj(z(J))),
theta,epsilon,r.
```

Each flat point has coordinate order x0,x1,y0,y1. Its zero-based selection from the full 31-input list is

```
[1,2,3,4,5,6,7,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30].
```

It creates four private primary points H0,Q_s,Q_t,Q_z and their four respective differences from 4P_*,4S,4T,4Z. Use the same compressed primary charts, ratio equations and difference charts with all guards. All four finite logarithms have precision K.

The nine order-one field expressions are, in order:

```
f(H0),f(Q_s),f(Q_t),f(Q_z),conj(f(J)),
conj(f(H0-4P_*)),conj(f(Q_s-4S)),conj(f(Q_t-4T)),conj(f(Q_z-4Z)).
```

The seven order-K field expressions are, in order:

```
C_s-xi, C_t-tau, C_z-zeta,
conj(z(H0-4P_*))/conj(z(J)),
conj(z(Q_s-4S))/conj(z(J)),
conj(z(Q_t-4T))/conj(z(J)),
conj(z(Q_z-4Z))/conj(z(J)).
```

The passed f(J) and inverse z(J) coefficients are already conjugated and must not be conjugated again. The field-order list is `[1]*9+[K]*7`. The first order-one root-error test followed by the paired rational field tests gives `[1]*19+[K]*14`, of length33. Use a separate q_batch33 with precisely that order list and the unchanged constant-left norm/pole semantics.

## Local implications

At each full position the established argument gives beta=n modulo p^q and `(xi,tau,zeta)=(s,t,z)` modulo p^K at every prime with odd raw-contact valuation. At each beta-only position it gives only beta=n modulo p^q. At each Lucas-only position the same local argument, now with three numerator points and common denominator all at precision K, gives only `(xi,tau,zeta)=(s,t,z)` modulo p^K.

In the last case the order-one root error selects a split place, the nine formal tests put all four primary points at that place and J and all four differences at its conjugate. The four alternate tests yield h0=4 modulo p^K and m_i=4n_i modulo p^K for n_i=s,t,z. Thus h0 is a p-unit. The finite-logarithm quotient estimates and three primary tests yield the required integral proxies and congruences. This starts with arbitrary odd raw-contact valuations, excludes negative ones through the norm/pole argument, and uses no ordinariness premise in soundness.

The same nonvanishing proof covers every G polynomial. The compressed maps are unchanged after removing unused primary/numerator/difference blocks from this separately specified comparator. All retained external occurrences and guards are still checked.

## First contradiction is unchanged from the 29/8 argument

Every one of the 29 positions used to bound x(S),x(T),x(Z) still has all three Lucas comparisons: five shared full positions, eight full T positions, and sixteen Lucas-only S/Z positions. Put

```
a=abs(s), B_L=max(abs(s),abs(t),abs(z)),
Delta=t^2-s(s-2)*t*z+(s-2)^2*z^2-1.
```

If Delta is nonzero, the exact same coverage, index-height and scalar height arguments in `ASYMMETRIC_CONTACTS.md` give

```
B_L^2-6 < 7H*abs(Delta)^(h/K)
        < 16H*B_L^(4h/K),
B_L^(2-4h/K) < 24H.
```

This contradicts the unchanged anchor cutoff. Hence Delta=0.

The released Lucas lemma is stronger than the weakened conclusion used in the earlier proof: it states `abs(t)>exp(abs(s)-3)`, not merely a lower bound on B_L. The nonzero z and a>=7 conditions are unchanged. Thus

```
log(abs(t)) > a-3.
```

## Second contradiction uses only A and T heights

Suppose beta differs from n and put N=abs(num(beta-n)). Its q-th power radical divisibilities are needed only for the two abscissas x(A),x(T). Their four rational coefficients use the five shared positions, eight A positions and eight T positions. All 21 of these retain a beta comparison. Hence the same two-slope height argument gives the required upper bound for both abscissas without any beta statement at the S/Z-specific positions.

Set

```
B_AT=max(abs(n),abs(t)).
```

The point realizing B_AT has x-height at least B_AT^2-6 and at most `7H*N^(h/q)`. Also `N<=2 exp(h(beta))*B_AT`, because beta has denominator and numerator bounded by exp(h(beta)) and n is an integer. Therefore

```
B_AT^(2-h/q)<40H*exp((h/q)*h(beta)),
log B_AT < (q+h)/(40*(2q-h))*a.
```

The unchanged scalar batch and anchor supply h(beta)<a/40 and log(40H)<a/40. The coefficient is 31/200 for h=19,q=12, and 1/8 for h=18,q=12. Both yield log B_AT<a-3. But B_AT>=abs(t), whose logarithm is larger than a-3. This contradiction proves beta=n and hence X is an integer.

No bound such as abs(z)<abs(t), and no comparison between abs(n) and abs(t), was assumed. S remains essential to the scalar height bound and anchor, and S,Z remain height targets in the first step. Only their unused beta-comparison consumers disappear.

## Completeness, repetitions and exact scope

Choose the same integral-input scalar/anchor/Lucas data and the same 37-contact prime pattern as before. The common J still uses all selected primes. At a full occurrence choose the original five primary points. At an A occurrence choose only H0 and the beta numerator point. At an S or Z occurrence choose H0 and the three Lucas numerator points. The same h_p CRT conditions at high K suffice for every retained block, since q<=K. All nonzero-point and difference guards follow as before. Choose the single theta last to satisfy the maximum actual coefficientwise precision over all three module types.

Each smaller norm tree still has the constant leaf on its all-left path. Its normalized leaves can be made deep enough at the selected prime, so the same positivity, square reduced denominator and local-square argument supplies pole witnesses. Coincident slopes and coincident primes cause no loss: the source retains every position and its assigned module; the global proof only needs coverage of each target by the corresponding required congruences. It does not require cross-prime reduction-order coprimality.

The resulting source has the claimed input projection by this new arithmetic argument, not by an old-source algebraic equivalence certificate. Its producer must introduce named q_compare1/q_compare3/q_compare4 and corresponding q_batch17/q_batch33/q_batch41 modules, or an equally explicit audited representation. The full module set, call counts, free-input maps and flattening need independent checking. A fresh lift, replay, negative tests and complete coefficient expansion remain required before any sub-10,000 claim.
