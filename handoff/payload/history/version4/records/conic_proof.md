# Private conics and one norm node per field test

Status: arithmetic source proposal for independent review and a fresh source audit. No new source is accepted by this note, and no final variable saving is measured. The released Version 3 construction is unchanged. This note supersedes the preliminary version that retained a separate root-error leaf, and it does not assume that a tested field element is a square.

## Exact replacement

Fix one raw contact r and the ordered field tests F_i=A_i+B_i sqrt(2), with positive integer orders e_i. The coefficients A_i,B_i are rational expressions supplied by the chosen comparator. They are independent of the local conic variables introduced below. The actual list of tests, orders, point charts, logarithms, scalar batch, height theorem, anchor and contact assignment must be specified by the separate source manifest. This rule changes none of those consumers.

The old comparator first tested epsilon=theta^2-2, then tested epsilon B_i and A_i+theta B_i at order e_i. Its bottom pair was

    r^(2e_i) N_i = epsilon^2 B_i^2 + r(A_i+theta B_i)^2.

Replace that entire rational-test layer at this contact as follows.

1. Introduce three private rational coordinates theta,s,S and impose

       S=s^2,       theta^2-rS-2=0.

   They belong to this one contact. In particular, theta is not shared between distinct contacts. There is no separately retained epsilon coordinate or epsilon leaf.

2. For each field test, let P_i denote the retained power r^(2e_i). Introduce Y_i,W_i and impose

       Y_i=A_i+theta B_i,
       P_i W_i=2 A_i Y_i-A_i^2+2 B_i^2.                 (1)

   Equal powers can share their deterministic powering circuit. Put

       T_i=2 A_i Y_i-A_i^2+2 B_i^2
          =Y_i^2-(theta^2-2)B_i^2.                    (2)

3. Order the field tests by increasing e_i, preserving the given order within an order group. Start the upper tree with the ordered nodes

       1, W_1, ..., W_m.

   Pair successive nodes by N_r(a,b)=a^2+r b^2, carry a last unpaired node, and repeat until one root W remains. The literal 1 is always the first node, hence lies on an all-left path. Keep the same pole predicate Psi(r W^2) as in the comparator being replaced. Its existing quadratic implementation and any valid local algebraic reductions remain applicable after their changed inputs and incidences are audited.

This specifies a new tree. It is not an assertion that the old numerical norm root keeps its value. The scalar-height batch is outside this rule and remains unchanged. No scalar rational test is silently converted to a field test.

## Nonvanishing and the conic valuation

Every rational solution of the conic equations has r,s,S nonzero: either r=0 or s=0 would imply theta^2=2. Thus division by r in the following proof is legitimate, without an added inverse. This uses rational nonsquareness of 2, not a local genericity condition.

Let p>2 and suppose R=v_p(r) is odd. Write epsilon=theta^2-2 as a mathematical abbreviation, and E=v_p(epsilon). Since epsilon=r s^2 and s is nonzero,

    E=R+2v_p(s)

is odd. If v_p(theta)<0, then E=2v_p(theta) is even. If v_p(theta)>0, then E=0. If theta is a unit and epsilon is a unit, again E=0. These are impossible. Consequently

    v_p(theta)=0,       E>0 and odd.                    (3)

In particular 2 is a square modulo p. There is a root rho of 2 in Q_p such that theta-rho is divisible by p. The other factor theta+rho is a unit, so

    v_p(theta-rho)=E.                                  (4)

This conclusion holds before the sign of R is known. No ordinariness assumption is used.

## Constant path, negative contacts and field orders

At odd R, the two nonzero summands of N_r(a,b) have valuations 2v_p(a) and R+2v_p(b) of different parity. Hence their valuations cannot cancel. In particular N_r(a,b)=0 forces a=b=0 over Q_p. Recursion along the constant path proves W is nonzero, even when some W_i is zero.

The unchanged soundness direction of the pole predicate, at every p>76176 outside its fixed exceptional set, therefore gives

    v_p(rW^2)>0.                                      (5)

If R<0, descent along the all-left path, or direct ascent from its literal leaf 1, gives v_p(W)<=0: each parent has valuation at most twice the valuation of its left child. This contradicts (5). Thus R>0.

Equation (5) gives v_p(W)>-R/2. At a higher node, a bound v_p(N_r(a,b))>-cR with 0<=c<1 implies

    v_p(a)>-cR/2,       v_p(b)>-(c+1)R/2.

Repeated descent gives v_p(W_i)>-R for every field node. Equations (1) then imply

    v_p(T_i)>(2e_i-1)R >= 2e_i-1,
    v_p(T_i)>=2e_i.                                   (6)

This is the bound needed here. It is not generally a bound of 2e_i R.

The two terms in (2) have different valuation parity by (3). The same conclusion holds when a term is zero, with valuation infinity. Equation (6) therefore gives

    v_p(Y_i)>=e_i,       E+2v_p(B_i)>=2e_i.

By (4),

    v_p((theta-rho)B_i)=E+v_p(B_i)>=e_i+E/2>e_i.

Thus

    v_p(A_i+rho B_i)>=e_i.                            (7)

The argument also covers B_i=0 directly. Formula (7) is exactly the field-valued conclusion consumed by the released comparison argument. It holds for every retained field test at the same selected place determined by this contact's theta. Negative valuations of A_i or B_i have not been excluded by assumption.

In particular this compression applies to an arbitrary field test F_i. Global squareness of F_i, of primary f, or of a difference parameter is not a hypothesis. The chart proposal that drops global primary squareclasses must still prove its own field-test list suffices, but it does not invalidate this compression.

## Rational points on the private conics

In the existing completeness construction, every contact has the form

    r=d^2 p>0,

where p is a chosen positive prime congruent to 1 modulo 8, and d is a nonzero rational number that is a p-adic unit. Finite contacts have d=1. The infinity contact has the prescribed denominator-clearing factor d. The chosen primes can avoid its fixed prime divisors, as in the existing construction. Coincident contact primes cause no change to the argument: each contact has its own conic variables.

There is a rational point on theta^2-rs^2=2. Here is an elementary derivation, so this existence adds no external arithmetic input. The ring Z[sqrt(2)] is norm Euclidean. For an element of Q(sqrt(2)), subtract nearest integers from its two rational coefficients; the remainder a+b sqrt(2) has |a|,|b|<=1/2 and |a^2-2b^2|<=1/2<1. As p splits, the ideal (p,sqrt(2)-h), where h^2=2 modulo p, has norm p and is principal. A generator has norm p or -p. Multiplication by the unit 1+sqrt(2), whose norm is -1, gives integers a,b with

    a^2-2b^2=p.

Here b is nonzero since p is not an integer square. Therefore

    theta_0=a/b,       s_0=1/(db)

is a rational point of the required conic.

For clarity, rational approximation on this conic does not require an additional weak-approximation theorem. Lines theta=theta_0+t(s-s_0) give the rational parametrization

    delta=2(rs_0-theta_0 t)/(t^2-r),
    s=s_0+delta,       theta=theta_0+t delta.            (8)

The denominator is nonzero for rational t because r=d^2p is not a rational square. Away from the usual single exceptional point this parametrization has rational inverse t=(theta-theta_0)/(s-s_0). Rational numbers are dense in Q_p; continuity of (8) gives rational points arbitrarily close to every nonexceptional Q_p point of the conic. The exceptional point is handled by nearby nonexceptional points.

For either chosen root rho of 2 and arbitrarily large k, take a nonzero local s with v_p(s)=k. Hensel lifting gives the branch theta near rho satisfying theta^2=2+r s^2. Its error has

    v_p(theta^2-2)=1+2k,
    v_p(theta-rho)=1+2k.

Approximation by (8), sufficiently close to this point, preserves these valuations and this branch. Hence rational conic points can make the positive odd E arbitrarily large at the contact's chosen place. Only this one-place approximation is required for each private conic.

## Completeness of the replacement layer

Start with the unchanged integral-input construction, including its scalar and anchor data, its chosen primes, the common J and its private primary/difference points. Its existing CRT argument makes each field test satisfy v_p(F_i(rho))>=e_i at the assigned split place. All these coefficients and points are fixed before theta is chosen.

Choose a rational point on the private conic with E sufficiently large that, for every i with B_i nonzero,

    E+2v_p(B_i)>=2e_i.

Then v_p(Y_i)>=e_i and v_p(T_i)>=2e_i. Since v_p(r)=1 at the assigned prime, assigning W_i=T_i/r^(2e_i) gives p-integral W_i. Assign every higher node by its displayed N_r formula. All nodes are p-integral and the root W is a p-adic unit: along the all-left path the left child is a unit and r times the square of the right child is divisible by p.

The values W_i may be negative in the real embedding. That is harmless. Since r>0, each upper operation a^2+r b^2 is nonnegative; the nonzero constant path makes its root strictly positive. In particular W is nonzero. The pole argument rW^2 is positive. It is locally square at 2,3,17 because r has that property in the unchanged prime construction and W^2 is a nonzero rational square. At the only prime where r has odd valuation, namely p, its valuation is 1 because W is a p-adic unit. At every other prime its valuation is even. Thus its reduced denominator is a square, including at primes dividing the denominator-clearing factor d. These are exactly the retained completeness hypotheses of the pole predicate, so its witnesses exist.

This proves both directions required for the arithmetic source. An arbitrary rational solution gives all field conclusions (7), so the selected comparator's previously proved soundness yields the integer input condition. Conversely every integral input admits the unchanged arithmetic data and the newly constructed private conics, field nodes, upper nodes and pole witnesses. This does not give a rational map from every old private witness tuple to a new one. The new equations strengthen/change the auxiliary source; their equality of input projections rests on the arithmetic proof above, not on algebraic equivalence to the old source residuals.

## Degree, incidence and executable audit requirements

With r,A_i,B_i affine in retained coordinates, every displayed conic equation and every equation (1) has total degree at most two. In particular B_i^2 occurs additively, so it needs no separate product coordinate. The coefficients added directly by this rule have absolute value at most 2 before substitution of the existing affine expressions. These facts alone are not a bound on the expanded final polynomial's height.

The upper equation W=a^2+r b^2 is cubic as written. Use the existing quadratic implementation with its retained square/product coordinates, or a separately checked reduction. Do not advertise the complete source as quadratic merely from (1). Powers P_i are emitted by the existing deterministic multiplication circuit. A fresh lift, coefficient expansion, independent replay and source-to-proof audit are required.

The new source audit must check all of the following.

* There is one private triple theta,s,S per raw occurrence, with no shared theta or s. The old global theta, epsilon and root-error relation are removed only after every old use is accounted for.
* Each conic uses exactly that occurrence's raw r, and the two conic residuals are exactly S-s^2 and theta^2-rS-2.
* Every field test, its conjugation and its order is copied from the separately approved comparator contract. A_i,B_i have no local theta,s,S dependence. No test is lost or moved to another contact.
* Each Y_i and W_i satisfies (1), with P_i exactly r^(2e_i). The sign in the final term is +2B_i^2 on its right side. The corresponding norm is the difference in (2), not a sum.
* The old epsilon leaf and the old bottom paired norms are absent. The upper tree is the exact successive-pair tree on literal1 followed by the ordered W_i. Its constant path, carries, raw-r arguments, root square and pole argument are checked independently.
* The old odd powers r^(2e_i-1), B_i-square witnesses, paired-test definitions and inverse guards are deleted only if their actual incidences are internal. Shared or external uses must be retained or separately reconstructed.
* The scalar-height batch, original input coordinate and all unrelated modules are unchanged. A chart change, contact partition or precision change requires its own independent proof and named source manifest.

For the frozen three-mode field lists, there are 13*20+8*8+16*16=580 field tests. A literal unshared implementation of the old absorbed layer has one B_i-square witness per field test; the new layer has none. It also removes 37 first epsilon norm nodes, while replacing two shared root-error coordinates by 3*37 private conic coordinates. This nominal bookkeeping gives 580+37-(111-2)=508 fewer coordinates in that layer, before accounting for old square sharing, alias elimination, odd-power changes or the final lift. It is not a measured saving and must not be added to a chart saving without a combined run. New chart lists that remove some field tests require recomputing this table from the audited list.

## Proposed bounded verification packet

The source producer should emit an isolated named variant, for example `private-conic-field-norm-v1`, with a manifest containing the contact-to-comparator map, complete ordered field tests/orders, private conic incidence, exact upper-tree schedule and source hashes. Independent finite tests should check the polynomial identity (2), both conic residuals, generated power exponents, full tree schedules including carries, and mutation rejection for the sign of 2B_i^2, a wrong order, a missing field test, a shared conic variable, a wrong raw contact, or a lost constant path. Such finite tests audit the implementation. They do not replace the arithmetic proof or the separate pole theorem.
