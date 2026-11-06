# One local Lucas residual instead of three proxy comparisons

Status: new arithmetic source proposal, awaiting independent review and a measured combined implementation. The frozen conic proof and emitter are unchanged. This proposal retains every root point, raw contact, private primary point, difference, alternate ratio and G circuit. It replaces the three Lucas primary field tests by one field test at each of the 29 Lucas-bearing occurrences.

## Observation used by the replacement

Write the root indices as A=nP_*, S=sP_*, T=tP_*, Z=zP_*. The three-mode source uses full comparators at the five shared and eight T positions, beta-only comparators at the eight A positions, and Lucas-only comparators at the sixteen S/Z positions.

In a Lucas-bearing comparator let C_s,C_t,C_z be the three retained finite-logarithm quotients. The local proof establishes

    C_s,C_t,C_z are integral at the selected place,
    C_s=s, C_t=t, C_z=z modulo p^K,                    (1)

before using the primary tests against the global proxies. Indeed the alternate tests give h=4 modulo p^K and m_i=4n_i modulo p^K. Thus h is a unit, m_i/h is integral and congruent to n_i. Formal membership and the reciprocal-G approximation give C_i=m_i/h modulo p^K. This argument is unchanged for half-integer private indices in the reviewed rational-difference chart: the private indices are integral at the selected odd prime, and the same doubled-point logarithm identities apply.

The old three primary tests were needed to transfer (1) to the common rational proxies xi,tau,zeta, whose global Lucas equation then supplied a congruence for the integer indices. They are not needed to establish (1) itself.

## New field test and exact evaluation

Define the integer-coefficient polynomial

    F(X,Y,Z)=Y^2-X(X-2)YZ+(X-2)^2 Z^2-1.

At each full or Lucas-only comparator, replace all three old primary field tests

    C_s-xi, C_t-tau, C_z-zeta

by the single field test

    E=F(C_s,C_t,C_z), of order K.                      (2)

The beta primary test C_beta-beta remains in every comparator that previously had it. No formal or alternate test is removed.

A quadratic evaluation uses three new field pairs V,D,E and the six rational equations represented by

    V=(C_s-2) C_z,
    D=C_s C_t-V,
    E=C_t^2-V D-1.                                    (3)

Their field arithmetic is in Q(sqrt(2)); each component is a quadratic polynomial in retained coordinates. Substitution gives exactly (2). The letter D in (3) is a private evaluation coordinate, not the curve constant; an implementation should use distinct names. Pass the bound pair E as the field test to the chosen norm layer.

The source no longer needs global xi,tau,zeta or their global Lucas equation. They may be removed in the new source together with their call slots. An initial implementation may instead leave the old root and free interfaces unchanged, ignore those three input slots in the comparators, and retain the old proxy equation. This adds no arithmetic restriction: independently choose xi=0,tau=1,zeta=0 to satisfy it. The actual nonzero root point Z is unaffected by these unused proxy values. Any later deletion requires the complete incidence audit appropriate to that source version.

## Soundness

Fix any p>76176 where a relevant raw contact has odd valuation. The chosen norm layer, either the existing paired layer or the reviewed private-conic layer, supplies the stated field orders. The unchanged formal/alternate argument gives (1). Since F has integer coefficients and all three C_i and integer indices are p-integral, (1) implies

    E = F(s,t,z) modulo p^K.

The new order-K test forces v_p(E)>=K. Consequently

    p^K divides Delta,  Delta=F(s,t,z).                (4)

The first global contradiction consumes precisely (4). Every height contact for S,T,Z remains covered at its original Lucas-bearing occurrence. If Delta is nonzero, the same radical divisibility and height bounds give

    B_L^2-6 < 7H |Delta|^(h/K),
    |Delta|<5 B_L^4,
    B_L^(2-4h/K)<24H,

where B_L=max(|s|,|t|,|z|). The unchanged H19/K40/anchor25 cutoff contradicts this inequality. The reviewed H18 alternatives work under their own unchanged cutoff as well. Hence Delta=0.

The nonzero root point Z still gives z!=0, and the unchanged anchor gives |s|>=7. The released Lucas growth lemma therefore yields |t|>exp(|s|-3). The second global contradiction uses the unchanged beta tests on the shared, A and T positions. With B_AT=max(|n|,|t|), it proves beta=n just as before. No global proxy equality is asserted or needed.

This proof uses no ordinary-prime hypothesis in soundness. Repeated raw positions and repeated primes remain separate occurrences. There is no new cross-prime compatibility condition.

## Completeness

For an integral input use the existing scalar/anchor construction and its integer Pell solution s,t,z. Thus F(s,t,z)=0 exactly. Use the same common J and private primary/difference points as before. Their local construction gives (1) at every assigned prime with K precision for the three Lucas quotients. It follows directly that v_p(F(C_s,C_t,C_z))>=K. Assign V,D,E by (3). The chosen norm layer therefore has the required integral normalized leaves; its existing pole-completeness argument applies without change.

If the private-conic layer is used, fix all these new coefficients before choosing its private theta. The conic approximation can then meet the order-K requirement for E exactly as for any other field test. This replacement imposes no exact Pell equation on the truncated logarithm quotients; it imposes only the local order-K test. Requiring F(C_s,C_t,C_z)=0 as a rational field equality would be a stronger and unproved completeness requirement and is not proposed.

## Exact field lists for the four-field or three-field difference chart

The beta comparator stays unchanged with six field tests. The other lists are as follows. Every alternate is already the conjugated z-ratio supplied by the selected independently reviewed difference chart.

Full comparator, thirteen field tests:

    f(H),f(Q_beta),f(Q_s),f(Q_t),f(Q_z),conj(f(J)),
    C_beta-beta, E,
    alternate(H),alternate(Q_beta),alternate(Q_s),alternate(Q_t),alternate(Q_z).

The orders in this exact input order are

    [1]*6 + [q,K] + [K,q,K,K,K].

Lucas-only comparator, ten field tests:

    f(H),f(Q_s),f(Q_t),f(Q_z),conj(f(J)), E,
    alternate(H),alternate(Q_s),alternate(Q_t),alternate(Q_z).

Their orders are

    [1]*5 + [K]*5.

For the current tuple K40/q12, the total number of field tests is

    13*13 + 8*6 + 16*10 = 377,

compared with 435 in the preceding four-field chart. The private point count remains 145. The G approximation polynomials and precisions are unchanged. Three field pairs are added for (3) at each of the 29 Lucas-bearing occurrences. The final net variable change depends on the chosen norm layer, field-square fusion, lifting and alias elimination. No final variable saving is asserted here.

## Required independent checks

The new source must preserve every alternate and formal input, their conjugations and their orders. The C_s,C_t,C_z used in (3) must be the same retained quotients formerly compared to the three proxies. The source auditor must reconstruct all six equations in (3), the replacement test order and exact mode lists, unchanged beta primary tests, and all root/call changes. It must reject an exact-zero E constraint, a missing E test, a swapped quotient, any changed power/order, or use of a different E in the norm call.

This is an arithmetic source change with equality of the final input projection. It is not a map preserving every old global proxy witness tuple. It requires a named new source, independent arithmetic review, full source reconstruction and a fresh finite replay before use in a polynomial claim.
