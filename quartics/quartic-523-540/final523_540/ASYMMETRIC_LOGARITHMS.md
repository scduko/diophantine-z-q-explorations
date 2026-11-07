# Asymmetric formal depth replaces five truncated logarithms

Status: a new arithmetic refinement, not a projection-equivalence certificate for the old equations. The argument below retains the repository's arithmetic inputs and PR4 direct-target convention. It strengthens a consequence of the existing prime-pattern proof by deleting a thin set of small w. It does not assume a new prime-pattern theorem.

## Source change

Write U0=H, Vi=Ui-Qi, Q0=P*, Qi=ni P*, H=hP*, Ui=ui P*. All points and nonzero guards retain their previous meaning. Let f=1/x and z=-x/y. Replace the five primary truncated logarithms by z(Ui). Keep all five alternate logarithms as ell40(Vi)=z(Vi)G9(D f(Vi)^2), including V1, which formerly used G2. Define

    Li = z(Ui)/z(H),
    Li' = conjugate(ell40(Vi)/ell40(V0)).

The sixteen tests now have only two orders:

* Order 1: f(U1),...,f(U4), conjugate(f(V0)),...,conjugate(f(V4)); nine tests.
* Order 40: f(H), L1-L1',...,L4-L4', L1-beta, and the direct Lucas residual; seven tests.

Use the same detector lemma with these orders. Keep the scalar norm block, its order 32, all height scales, and the anchor. The beta tests are stronger than the previous order-12 tests.

All primary denominators z(H) are globally nonzero by the existing point-domain lemma. All alternate logarithms are globally nonzero by the existing dyadic G_J nonvanishing proof, with J=9. The source changes introduce no new quotient domain.

## Local estimate for the uncorrected parameter

At a consumed unramified place over p>76176, on the formal branch set r=v(z(Q))>=1. The existing identity log_E(Q)=z(Q)G(D f(Q)^2), together with v(f(Q))=2r, gives

    log_E(Q)/z(Q) in 1+p^(4r) O.

This follows from exactly the existing factorial-tail proof, now applied starting with j=1. For j with 4j+1<p the coefficient is p-integral. For larger j the bound v(a_j)>=-(4j+1)/(p-1) and j>=19044 imply v(a_j w^j)>=4r. Thus the entire nonconstant series has valuation at least 4r. Both log_E(Q) and z(Q) have valuation r.

The order-40 f(H) test implies v(f(H))>=40 and therefore v(z(H))>=20. All other order-one inverse-abscissa tests give formal membership at the corresponding places.

## Soundness, with integrality before the strong error estimate

At the primary and conjugate places, the two full logarithm ratios are

    ri=ui/h,       ri'=(ui-ni)/(h-1).

At least one of h,h-1 is a p-unit. Its full ratio is integral. Without yet invoking depth 20 for Ui, the weak unit estimates above show that the primary z-ratio has the same valuation as ri; the alternate truncated ratio has the same valuation as ri'. The order-40 cross test therefore transfers integrality to both approximate ratios and then to both full ratios.

Now Li=z(Ui)/z(H) is integral, so v(z(Ui))>=v(z(H))>=20. Hence both primary uncorrected parameters have relative logarithm error at least 80, and their ratio has error at least 80. The alternate logarithm ratio has its usual relative error at least 40. Integrality makes these errors absolute. Consequently

    Li=ri=ri' modulo p^40.

Multiplying by h and h-1 and subtracting gives Li=ni modulo p^40. At inert primes conjugation preserves the sole local valuation and the same argument applies. Thus the direct Lucas conclusion still has order 40 and beta now also has order 40. In particular every order-12 beta consequence in the established exponent-19 height proof remains valid. The two original height contradictions and scalar/anchor bounds apply unchanged.

## Separation of the selected primes from the reduction orders

The existing simultaneous-prime proof can be strengthened to ensure

    gcd(product_j p_j, product_j d_+(p_j))=1,

where p_j=u+c_j w^2 are its distinct contact forms and d_+(p)=N(pi_p+1).

Here are the details missing from the bare statement of that theorem. Its proof works with u in [N/2,N] and 1<=w<=T, where T=floor(tau(N)*sqrt(N)), tau(N)->0, and a diagonal choice permits tau to tend to zero arbitrarily slowly. Impose in that same diagonal choice

    tau(N)*N^(1/6)/(log N)^k -> infinity,

where k is the fixed number of distinct forms. The prime-pattern lower bound and obstruction-tail estimates are unchanged. Discard w<N^(1/3). Since each von Mangoldt prime weight is O(log N), this discarded range contributes O(N^(4/3)(log N)^k)=o(NT), whereas the retained lower bound is a fixed positive constant times NT. It therefore leaves a pattern after the same obstruction exclusions. Integer dilations and finite ray multiplicities only change fixed constants.

For the remaining patterns, w^2>=N^(2/3), w^2=o(N), and all p_j=u+o(N) with the same u. Hasse gives d_+(p_j)=p_j+O(sqrt(N)). For all sufficiently large N, every ratio d_+(p_j)/p_i lies strictly between 1/2 and 2. Thus p_i dividing d_+(p_j) would force equality. If i!=j, the difference |p_i-p_j|=|c_i-c_j|w^2 is at least c_* N^(2/3), where c_*=min_{i!=j}|c_i-c_j|>0 is fixed, contradicting the Hasse bound. If i=j, equality is impossible since d_+(p_i) is divisible by four whereas p_i is odd. This proves the asserted coprimality. Repeated contact forms are deleted before applying this argument, as in the original source.

## Completeness

Retain the existing order of choices: first X in Z, the scalar preparation, h0 divisible by64, the scalar label and Lucas witnesses, then all target points, scales and the continuity modulus L. The primary z-ratios and alternate G9-ratios are rational functions with nonzero denominators at the chosen initial point. The original continuity and real-progression arguments therefore still provide the needed fixed local and real bounds before selecting the primes.

Choose the contact primes using the strengthened consequence just proved, larger than every prime dividing L and the fixed scale data. Let M_minus and M_plus be the lcms of the doubling-image orders d_-(p)/4 and d_+(p)/4, as in the PR4 direct-target completeness proof. Set P=product_p p. The congruences

    h=0 modulo P^19*M_minus,
    h=1 modulo M_plus,
    h=h0 modulo L

are compatible. The old gcd(M_minus,M_plus)=1 and fixed 2-adic compatibility remain valid; the added P factor is coprime to M_plus by the separation lemma and to L by the cutoff.

Choose a sufficiently large positive h in this progression attaining the same real bounds. Set H=hP* and Ui=h ni P*. At each primary selected place, multiplication by the corresponding doubling-image order makes P* formal with z-valuation at least1. Multiplication by p^19 raises this valuation by19, because the formal logarithm is an isometry and a homomorphism. Hence H, and then every Ui, have z-valuation at least20. Their primary z-ratios differ from ni to order at least80. At the opposite place, V0=(h-1)P* and Vi=(h-1)niP* are formal; the alternate G9-ratios differ from ni to order40. All sixteen new tests meet their assigned orders.

The pole-completeness argument is uniform in the positive test orders. In particular its real asymptotic factor decay remains lambda^-3: for order m, q_m behaves as a fixed multiple of lambda^-3, regardless of m. Its small-prime valuation estimate 3nu+(10m-8)eta-2c still tends to infinity. Thus the same preparation-zero poles are available. The scalar conditions and anchor remain preserved by the original congruence modulo L.

This proves completeness under precisely the inherited arithmetic inputs, with the additional prime separation deduced above from the existing asymptotic proof.

## Why both sides cannot be made deep by this method

Making both H=hP* and V0=(h-1)P* deeply formal at the two places of a selected prime would generally require both h and h-1 to be divisible by a power of p. The asymmetric choice avoids this obstruction and is essential. The remaining alternate logarithms have not been discarded.
