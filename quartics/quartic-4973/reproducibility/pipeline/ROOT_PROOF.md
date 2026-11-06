# Root points with integer doubled indices

Status: new arithmetic-source proposal for independent review. No source file or frozen producer is changed. This retains H19, the 37 contacts, high precision 40, beta precision 12, scalar order 32 and 25 anchor squarings. It changes the root carrier and the fixed comparison base. The purpose is to remove two square-membership pairs from each of the six root points. Final savings require source auditing and replay.

## 1. Inherited group facts and the new indices

Use the same curve

    K=Q(sqrt(2)), d=3-sqrt(2), D=d^2,
    E: y^2=x^3-Dx,
    R=(1+sqrt(2),2sqrt(2)),
    P*=(57/8-7sqrt(2)/2,-165/8+417sqrt(2)/32).

Direct duplication gives 2R=P*. The inherited generator theorem says 2E(K)=Z P*, and the inherited torsion computation says E(K)_tors=E[2](K). Consequently every Q in E(K) has one and only one integer n_Q with

    2Q=n_Q P*.

Equivalently Q=n_Q R+tau_Q with tau_Q in E[2](K). The index is nonzero exactly when Q is nontorsion. The old carrier 2E(K) is no longer imposed on the six root points A,S,T,Z,J0,J; they are required to be nontorsion points of E(K).

Write their doubled indices as n,s,t,z,j0,j respectively. These symbols remain integers. The old names do not mean the coefficient of P* anymore. The source must record this change explicitly. Local private comparison points already use this same integer doubled-index convention under the reviewed general-E joint chart.

## 2. A conservative uniform root chart

For each root point retain field coordinates x,y,f,zpar and add p, with the four field equations

    x f=1,       y zpar+x=0,
    p=y f,       p^2=x-D f.                            (1)

Each component is quadratic over Q. Equations (1) imply x,f,y,zpar,p are all nonzero, pzpar=-1 and y=xp. Therefore y^2=x^3-Dx. Conversely any point of E(K) with x,y nonzero has the unique extension f=1/x, zpar=-x/y, p=y/x. Since the only nonidentity torsion points have y=0, this chart represents exactly the nontorsion points of E(K).

The old root chart has eight field pairs u,v,w,zpar,f,h,x,y. Replacing it by (1) removes u,v,w,h and adds p, saving three field pairs, or six rational coordinates, per root before the existing chart reductions. Against the currently optimized root chart, which already replaces w,h by p and eliminates y where its incidence allows, the additional deletion is precisely the two pairs u,v. Thus the conservative allocation difference is four rational coordinates per root, 24 over the six roots. This is a structural comparison, not a measured endpoint count.

All external x,y,f,zpar values and their consumers retain their meanings. In particular the root height targets are still the two coefficients of x(A),x(S),x(T),x(Z). The old square-membership chart rule must not be replayed on (1); the new source must be freshly audited and lifted. More aggressive x^2 reuse in the doubling circuit is outside this conservative proposal.

## 3. Fixed comparison base and local integer recovery

Use R, rather than P*, as the fixed comparison base. The shared denominator target is now 4R=2P*. The numerator targets remain 4A,4S,4T,4Z. Thus only the fixed base-point constant and its computed quadruple change; no variable root is divided or halved.

At a consumed odd-contact prime p>76176, write the private points as

    2X0=h P*,       2Xi=m_i P*.

For a numerator root Qi, 2Qi=n_i P*. If Yi=Xi-4Qi and Y0=X0-4R, then

    2Yi=(m_i-4n_i)P*,       2Y0=(h-4)P*.

The unchanged joint chart, formal tests, alternate ratios and norm/pole argument give the required orders of z(Yi)/z(J). Formal logarithms can be compared after doubling, since two is a unit at these primes. They therefore give

    v_p((m_i-4n_i)/j)>=e_i,
    v_p((h-4)/j)>=40,
    m_i=n_i*4 modulo p^e_i,       h=4 modulo p^40,

where e_A=12 and e_S=e_T=e_Z=40. The integer j is nonzero. Hence h is a unit. The exact group identity [2h]Xi=[2m_i]X0 follows from their doubled indices, including any torsion components. Applying the formal-group homomorphism and canceling two gives the primary logarithm ratio m_i/h. Thus no torsion is discarded before applying an actual group identity. The unchanged reciprocal-G estimates imply that the local primary quotients satisfy

    C_A=n modulo p^12,
    C_S=s, C_T=t, C_Z=z modulo p^40,

and these quotients are integral there. This is exactly the integer-index conclusion needed by the current local-Lucas or normalized-Lucas block.

Replace only the beta test C_A-beta by C_A-2beta. Put beta'=2beta for the proof. The beta conclusion becomes beta'=n modulo p^12. The Lucas residual and its order remain unchanged because s,t,z are still integers. The normalized variant continues to test F(C_S,C_T,C_Z)/C_S^2, with the same local nonunit argument and completeness avoidance of primes dividing the fixed s.

## 4. The root height bound and an effective constant

Retain the published inequalities already used by the source:

    h(x(kP*))>=k^2-6,
    h(x(2Q))<=4h(x(Q))+log(676).

For any nontorsion root Q with 2Q=n_Q P*, these imply

    n_Q^2-6 <=4h(x(Q))+log(676),
    h(x(Q)) >=n_Q^2/4-(6+log(676))/4 > n_Q^2/4-4.

No canonical-height formula on a newly chosen generator is assumed.

The unchanged two-slope H19 argument gives h(x(Q))<7H19 N^alpha whenever the relevant contact radicals to their required powers divide the nonzero integer N. Define H_eff=5H19, for proof estimates only. Since log(676)<7 and H19 N^alpha>=1,

    n_Q^2-6 <28H19 N^alpha+7 <35H19 N^alpha
            =7H_eff N^alpha.                          (2)

This restores the exact format of the old index-versus-contact estimate with H_eff in place of H19. The source still uses the same H19 theorem and does not assert a new sharper height theorem. H_eff is only a convenient enlarged constant accounting for doubled indices.

## 5. Scalar tests and both anchor places

Keep every scalar source equation, its raw polynomial in beta=X^2+2, its six rational tests and their orders (1,1,1,1,32,32). Only its points J0,S now have doubled indices j0,s. At every relevant large prime, including inert primes, the formal-group ratio is still

    log(S)/log(J0)=s/j0.

The two is canceled after doubling. The coefficientwise scalar tests therefore imply v_p(s)>=32. The same odd-contact argument gives

    M5(beta)^32 divides s,
    h(beta)<=H19*abs(s)^(19/32).

Since h(2beta)<=h(beta)+log(2), we have

    h(beta')<H_eff*abs(s)^(19/32).                     (3)

The four-witness anchor is unchanged. It still means both coefficients of f(S)/C are integral at 2 and 3, with C=3^(2^25). In particular S is formal at 3 and v3(f(S))>=2^25. Doubling is an isometry on the formal group at 3, so v3(f(2S))=v3(f(S)). But 2S=sP*, and the retained explicit reduction calculation for P* gives, when this valuation is positive,

    s is even,       v3(f(sP*))=2+2v3(s).

Thus the same necessary lower divisibility holds:

    s in 2*3^(2^24-1) Z,       s nonzero.             (4)

The condition at 2 is retained, not dropped or reinterpreted. The lower bound (4) requires only the 3-adic part. For completeness, choose S in the old subgroup 2E(K), with the additional old divisibility at 2 and 3 and all scalar places; that satisfies the full unchanged anchor. There is no claim that (4) characterizes the enlarged carrier's entire anchor locus.

The choices may make s divisible by four or any further fixed integer. The scalar and Lucas constructions allow arbitrary additional divisibility before the root targets and contact primes are fixed.

## 6. Unchanged precisions and both contradictions

The H19 input has log2(H19)<2093966, hence log2(H_eff)<2093969. For a=abs(s), (4) and log2(3)>3/2 give

    log2(a)>(3/2)*(2^24-1)=25165822.5.

Also log2(24H_eff)<2093974 and log2(40H_eff)<2093975. Therefore

    log2(a)>10*2093974,
    log2(a)>(32/13)*2093975.

The high40 and scalar32 cutoff inequalities hold with H_eff. In particular

    a>(24H_eff)^10,
    a>(40H_eff)^(32/13),
    h(beta')<a/40,       log(40H_eff)<a/40.

The last logarithmic estimate follows by the same argument as before, since 32/13>2. There is no precision change, anchor reduction or H18 assumption.

Set B_L=max(abs(s),abs(t),abs(z)). If Delta=F(s,t,z) is nonzero, all 29 Lucas-bearing contacts still force their 40th radical powers to divide Delta. Use (2) with N=abs(Delta), alpha=19/40, and abs(Delta)<5B_L^4. Exactly as before,

    B_L^(2-76/40)<24H_eff,

contradicting B_L>=a. Thus Delta=0, and the retained Lucas lemma gives abs(t)>exp(a-3).

If beta' differs from n, let N=abs(num(beta'-n)) and B_AT=max(abs(n),abs(t)). The 21 beta-bearing positions still cover A and T. Equation (2), now with alpha=19/12, and the usual rational numerator estimate give

    B_AT^2<7H_eff N^(19/12)+6,
    N<=2exp(h(beta'))B_AT,
    log(B_AT)<(12+19)/(40*(24-19))*a=31a/200<a-3.

This contradicts B_AT>=abs(t). Hence 2beta=beta'=n is an integer. Write the rational input as X=a0/b0 in lowest terms with b0>0. Since 2beta=2X^2+4 is integral, b0^2 divides 2a0^2. Coprimality gives b0^2 dividing 2, hence b0=1. The input X is an integer.

## 7. Completeness and the order of choices

For integral X retain beta=X^2+2 and set A=beta P*=(2beta)R. Its doubled index is n=2beta. Choose J0 and S together in the old carrier 2E(K), using the old scalar construction: first choose J0 deep at the finitely many scalar places, then S sufficiently divisible relative to J0 and at 2 and 3. Both new indices j0,s are twice their old indices, so s/j0 is exactly the old scalar ratio. This satisfies the unchanged scalar batch and full anchor. The new index s may satisfy any extra finite divisibility conditions. Apply Lucas existence to this integer s and set T=tR, Z=zR for the resulting nonzero integers t,z. These points need not lie in 2E(K), which is now permitted.

The eight rational abscissa coefficients and their denominator-clearing integer are then fixed. Apply the same rational37 positive ordinary-prime pattern, with any finite avoidance required by the normalized-Lucas block, including primes dividing s. No target depends on a later prime choice.

For the chosen prime set put j=lcm_p d_(p,2) and J=jR. At each prime choose h with

    h=0 modulo d_(p,1),       h=4 modulo d_(p,2),
    h=4 modulo p^(40+v_p(j)), h not in {0,4,-4}.

The original same-prime gcd and p-unit hypotheses prove compatibility. Both group orders are divisible by four, so h is a multiple of four. Set X0=hR and Xi=hQi, separately at each occurrence. The primary points are formal at the first place. Their differences from 4R and 4Qi, and J, are formal at the other place. Multiplication by h kills any rational two-torsion in the root Qi; the exact primary logarithm ratios are their doubled indices n_i. This also follows directly by doubling, without choosing a torsion decomposition in the source.

These choices satisfy all unchanged local field-order requirements and the new beta test. The joint chart, G nonvanishing, normalized-Lucas coordinate assignments, private-conic approximation and pole completeness then apply with their existing hypotheses. The root chart (1) extends all six nontorsion roots uniquely. No cross-prime order compatibility is added.

## 8. Required source binding

A new producer and independent source audit must bind all of the following together: the six general-E root charts; the fixed point R and target 4R; every retained numerator target 4Qi; doubled-index semantics in all local arguments; the beta field expression C_A-2beta in full and beta-only modes; unchanged Lucas and normalized-Lucas formulas; unchanged scalar polynomial in beta and all six scalar tests; the full unchanged anchor; the direct abscissa height targets; and the enlarged proof constant H_eff=5H19 with its checked cutoffs.

Changing only the root equations or only the beta expression would not implement this proposal. The exact root and comparison input maps, compiler locators, fresh source pin, new arithmetic contract, full module audit, reduction replay and coefficient expansion remain outstanding. The 24-coordinate comparison is not a final count.
