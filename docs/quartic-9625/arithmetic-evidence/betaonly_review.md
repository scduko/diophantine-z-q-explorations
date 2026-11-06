# Independent review of beta-only A contacts

PASS for the new arithmetic relation in `precision/ASYMMETRIC_CONTACTS.md`, SHA-256 `ec0146e593abc7a79eaf28fb3c09ddbbcfc01d2c3da7411de0a4b81361fabc98`, with `precision/ASYMMETRIC-CONTRACT.json`, SHA-256 `6a45f8ccb18e4dca100f87851bf40d21f92b684dfdd347a0588f0f88aac0a1e7`. This review covers both the H19 and H18 parameter families already reviewed in this directory. It supplies no new external arithmetic input and certifies no generated source or count.

The improvement is valid because the two contradictions may use different maxima. Earlier requirements to retain all four proxies at all contacts were sufficient conditions for a single common maximum. This proof replaces those conditions explicitly. It must be implemented as a new source, not by deleting tests under the old source's certificate.

## Coverage and local beta-only comparison

The 37 ordered positions are five shared positions, eight A positions, eight S positions, eight T positions and eight Z positions. They correspond to the eight unscaled rational coefficients in the fixed order A.x0,A.x1,S.x0,S.x1,T.x0,T.x1,Z.x0,Z.x1. Each target coefficient uses its own four finite contacts and the common base slope and infinity. All 29 positions outside 5 through 12 retain full comparisons. Coincident slopes or repeated raw values do not change this positional contract.

The proposed 16-input beta-only boundary is the exact sublist `[0,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30]` of the full 31-input boundary. It supplies beta, 4P_*, 4A, the common already-conjugated f(J), the inverse already-conjugated z(J), theta, its error and the raw contact. There is no missing target or denominator. Neither common input is conjugated a second time.

The module has two primary points, two differences, five formal field tests, one primary ratio test and two alternate parameter tests. The last three tests have order q. With the root-error test first, the rational order list is exactly `[1]*11+[q]*6`. The same arbitrary-size norm-tree proof applies to these 17 tests: the constant leaf remains on the all-left path, so negative odd raw valuations are excluded before the positive-order argument. No part of that proof depends on having 41 leaves.

For an arbitrary odd raw-contact prime p>76176, the root error selects the split place, the five formal tests give the required primary/common/difference memberships, and the alternate tests imply

```
v_p((h0-4)/j)>=q, v_p((m-4n)/j)>=q.
```

Since j and n are integers, h0 is a p-unit and m/h0 is integral and congruent to n modulo p^q. Both primary G polynomials have precision q, including the denominator. Their relative errors therefore suffice to give beta congruent to n modulo p^q. They need no high-K denominator. For q=12 each polynomial has J=2 and is globally nonzero by the reviewed ramified-2-adic argument. The compressed rational maps and inverse conditions continue to hold. No local statement about s,t,z is claimed at these eight positions.

## First contradiction

Take `a=|s|` and `B_L=max(|s|,|t|,|z|)`. Delta is the Lucas polynomial in s,t,z only. The six rational coefficients of x(S),x(T),x(Z) have every required raw contact among the 29 full positions. The raw-to-normalized parity argument is unchanged and applies to arbitrary rational assignments, including exceptional negative raw valuations. Thus, if Delta is nonzero, the Kth power of each relevant radical divides |Delta|.

Choose whichever of S,T,Z has index of magnitude B_L. The direct two-coefficient height estimate and the inherited index lower bound give

```
B_L^2-6 < 7H|Delta|^(h/K)
        < 7*5^(h/K)H B_L^(4h/K)
        < 16H B_L^(4h/K),
```

where h is 19 or 18 and the reviewed K satisfies K>2h. Hence `B_L^(2-4h/K)<22H<24H`, contradicting the unchanged strict anchor cutoff and B_L>=a. The height of A and the magnitude of n have not been used.

Now Delta=0. The actual released lemma `lem:o8-lucas` states the stronger conclusion `|t|>exp(a-3)` under a>=7 and z nonzero. Those hypotheses are still supplied by the anchor and nonzero root point Z. In particular `log B_L>a-3`. No estimate comparing n to B_L is needed.

## Second contradiction

Assume beta differs from n and write N for the absolute reduced numerator of beta-n. All 37 positions still imply beta congruent to n modulo p^q and beta integral at every relevant prime. Therefore the qth powers of all radicals for all eight coefficients divide N, including the A coefficients. This is where retaining the eight beta-only comparisons is essential.

Set `B=max(|n|,B_L)`. Whichever of A,S,T,Z has this index has all its height contacts covered, so

```
B^2<7H N^(h/q)+6, N<=2 exp(h(beta)) B.
```

The second inequality explicitly uses control of the integer n by B; substituting B_L there without another argument would be invalid. With alpha=h/q<2, these bounds imply `B^(2-alpha)<40H exp(alpha*h(beta))`. The unchanged scalar and strict anchor cutoffs then give

```
log B < (q+h)/(40(2q-h))*a.
```

At q=12 the coefficient is 31/200 for h=19 and 1/8 for h=18. For a>40 each upper bound is below a-3, whereas B>=B_L and the first step gives log B_L>a-3. The contradiction proves beta=n. The unchanged rational-square denominator argument proves X integral.

## Completeness and interaction with Jacobi

Use the same target points and all 37 positions in the rational-target prime-pattern construction. No new restriction is imposed on its proof-only common denominator. The common j is still the lcm over every selected prime, including primes occurring only at beta-only positions. At these eight positions choose the existing private h congruences with the former high precision if convenient, retain H0=hP_* and Q=hnP_*, and discard the need to construct the other three private primary points. The remaining differences satisfy all order-q requirements. Global G nonvanishing supplies the compressed denominators.

Choose theta after constructing both types of private point and evaluating both types of G. Its required depth is the maximum over all actual rational field-test coefficients. The shortened norm tree has the same positive/square-denominator/local-square completeness argument. Zero leaves are allowed. Duplicate raw positions may share a prime and its orientation while retaining separate private witnesses. No extra simultaneous congruence or cross-prime order condition appears.

The frozen asymmetric contract uses affine differences and retains their guards. Combining it with the independently reviewed Jacobi reform requires an explicit new joint contract: its difference model is complete Jacobi, its formal tests use w instead of f_R=w^2, and its target slots mean U,q instead of x,y. The selected slot indices still work, and the Jacobi identity/infinite-valuation argument works for two differences just as it does for five. However, a checker must not claim that it retained all old affine subtraction guards when it intentionally replaced that model. The original eight height coefficients must still refer to x(A),x(S),x(T),x(Z), not the new U,q boundary values.

## Finite acceptance boundary

A combined checker must independently reconstruct the exact positional dispatch, both complete comparator modules, both norm modules, the unchanged 37 raw expressions and their ordered arguments, both G12 outputs in the beta-only module, the primary ratio equations, and all shared common-J/root data. Counting eight calls of a named type does not prove that they are the correct eight positions. The source also needs full incidence, lift, reduction replay, mutation tests and a collected coefficient expansion. This arithmetic review establishes none of those finite results.
