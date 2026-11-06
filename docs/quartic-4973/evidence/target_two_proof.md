# Compare with doubles using the finite doubling images

Status: separate arithmetic refinement of the reviewed doubled-index root proposal. This note changes the comparison targets from 4R,4Qi to 2R=P*,2Qi. It does not change H19, the root carrier, beta scaling, precision, anchor, scalar batch, contact positions or the two global contradictions. No source is accepted by this note alone.

## 1. The exact inherited finite groups

At each selected ordinary prime p>76176, the inherited prime-pattern theorem concerns the two full groups E(F_p) obtained from the two embeddings of K=Q(sqrt(2)). Let their orders be N1,N2. The inherited conclusions are

    gcd(N1,N2)=4,       p does not divide N1*N2.

The curve has good reduction there. Its roots 0,d,-d are distinct elements of each F_p, since the prime is odd and does not divide the discriminant. Thus the full rational two-torsion subgroup has exactly four points at each reduction. The kernel of [2] on the finite group is exactly those four points. Therefore the image subgroup

    H_i=2E(F_p)

has order M_i=N_i/4, and every element of H_i is killed by M_i. In particular

    gcd(M1,M2)=1,       p does not divide M1*M2.        (1)

These are image subgroup orders, not a claim that E(F_p) itself is cyclic or that a fixed point generates H_i. The argument only uses the elementary homomorphism cardinality formula and the inherited order/good-reduction statements.

Every doubled K-point 2Q reduces into H_i, by compatibility of reduction with the group law. Also P*=2R reduces into H_i. These are the only target points to which the order M_i is applied.

## 2. New target list and unchanged index conventions

Retain the reviewed nontorsion root points A,S,T,Z,J0,J in E(K). Their unique integer doubled indices are defined by

    2Qi=n_i P*,       2R=P*.

The new fixed denominator target is P*, and the numerator targets are 2Qi. Each is a nonzero point of 2E(K), hence has nonzero affine abscissa and ordinate. The target field interfaces and joint-difference formulas need no geometric change. The new source computes each variable target by one doubling instead of two.

Private primary points still lie in the same general-E joint chart. Write

    2X0=hP*,       2Xi=m_iP*,       2J=j'P*,

where h,m_i,j' are integers whenever the corresponding points are nontorsion. At consumed primes the formal conditions imply this nonvanishing; the root chart already makes J nontorsion, so j' is a nonzero integer.

## 3. Soundness at arbitrary odd-contact primes

This direction does not assume an ordinary prime or a chosen prime-pattern witness. Begin at any p>76176 with odd raw-contact valuation, and apply the already reviewed norm/pole and private-conic arguments. They give the required field orders at a selected split place. Retain all current primary formal and alternate tests and the current joint chart.

Put

    Y0=X0-P*,       Yi=Xi-2Qi.

Then the exact doubled identities are

    2Y0=(h-2)P*,       2Yi=(m_i-2n_i)P*.

The same joint-chart/local argument as before recovers the formal logarithm valuation of these differences at the opposite place, including the already permitted identity case. Since 2J=j'P*, the alternate ratios give

    v_p((h-2)/j')>=40,
    v_p((m_i-2n_i)/j')>=e_i,

where e_A=12 and e_S=e_T=e_Z=40. Because j' is an integer,

    h=2 modulo p^40,       m_i=2n_i modulo p^e_i.      (2)

The residue of h is a unit because p is odd. At the primary place the exact group identity [2h]Xi=[2m_i]X0 and the formal logarithm show log(Xi)/log(X0)=m_i/h. The unchanged relative reciprocal-G errors therefore give

    C_i=n_i modulo p^e_i,

with C_i integral. This is exactly the same local conclusion as in the target-four doubled-index proposal. The beta test is still C_A-2beta. The local-Lucas or normalized-Lucas field remains unchanged. Consequently the already reviewed two global contradictions and final denominator argument apply without altering a constant or an exponent.

If one writes J=jP* instead, then j'=2j and the displayed logarithm ratios have denominator 2j. These are the same statements. No factor of two is silently omitted, and its valuation is zero at every consumed prime.

## 4. Completeness from coprime image orders

Use the same order of choices as the reviewed doubled-index proposal: choose the integer input and beta, construct scalar J0,S and the anchor, choose integer Lucas t,z and roots, then choose the rational37 ordinary-prime pattern. If using normalized Lucas, the chosen primes still avoid the fixed nonzero integer s. All targets and denominator data are fixed before the prime-pattern limit.

For the selected primes, use the chosen orientation and let M_(p,i)=N_(p,i)/4. Set

    j=lcm_p M_(p,2),       J=jP*.

At every opposite place J is formal because P* reduces into H_2. It is nonzero because j is a positive integer and P* has infinite order. Its doubled index is j'=2j.

For each occurrence with selected prime p choose an integer k satisfying

    k=0 modulo M_(p,1),
    k=1 modulo M_(p,2),
    k=1 modulo p^(40+v_p(j)),
    k not in {0,1,-1}.                               (3)

Compatibility follows from (1). The first two moduli are coprime, and both are prime to p. The resulting arithmetic progression is infinite, so the finite exclusions in (3) may be imposed. This argument is private to the occurrence; it assumes no cross-prime coprimality of image orders. Repeated primes use one orientation as before.

Set

    X0=kP*,       Xi=k(2Qi)=k n_i P*.

They are nonzero points. At the primary place, their reductions lie in H_1 and k kills that subgroup, so they are formal. At the opposite place,

    Y0=(k-1)P*,       Yi=(k-1)(2Qi)=(k-1)n_iP*,

and k-1 kills H_2. Thus all required differences are formal. Since k differs from one, these differences are nonzero for the complete witness, although the chart may also permit identity differences in soundness.

The exact formal-logarithm ratios at the opposite place are

    log(Y0)/log(J)=(k-1)/j,
    log(Yi)/log(J)=(k-1)n_i/j.

Their valuations are at least40 by (3); the n_i are integers and the lower beta order imposes no additional condition. At the primary place, the exact ratio is log(Xi)/log(X0)=n_i. The same high40/beta12 finite-logarithm approximation consequently supplies every primary and alternate field test. All G nonvanishing, normalized-Lucas assignments, conic approximation and pole witnesses then follow as in the reviewed parent proof.

The finite exclusions also keep Xi away from plus or minus its target and X0 away from plus or minus P*. They therefore suffice even for an older affine difference chart; the present joint chart requires no stronger exclusion.

## 5. Source obligations and scope

The change must be recorded as one new source refinement. Its fixed target is exactly P*, not 4R; each variable target is exactly 2Qi, not 4Qi. Remove only the second doubling of A,S,T,Z after checking every old intermediate/final-target consumer. The first doubling is retained and still supplies the x^2 pair used by the smaller root chart. Recompute fixed-target rational binding values and all target metadata. The current beta factor two, six root charts, scalar/anchor predicates and 37 contact positions are unchanged.

The independent audit must check the actual inherited N_i are full group orders, the kernel/cardinality argument above, both target maps, all target field slots and conjugations, and the recomputed fixed constants. No count or coefficient maximum is asserted here. Source generation, complete replay and full expansion are still required.
