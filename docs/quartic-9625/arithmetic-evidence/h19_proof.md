# Combined arithmetic relation with 37 contacts

Status on November 6, 2026: author proof packet, awaiting renewed independent review of the conjunction and a separately audited generated source. No new source pin, quartic count or coefficient bound is accepted by this note. This is a new arithmetic relation, not an algebraic rewrite of the released source.

The accepted reference is `work/quartic-12504-release/public-repository/quartic_12504.tex`, SHA-256 `38d458ba4178083766c5ae56a894da595fe27170c1ef07f6b49750fc5edf7c37`. All inherited theorem-version qualifications remain in force. In particular this packet adds no unpublished external theorem. Its extra modular-quotient facts have published sources identified below. Earlier notes are evidence to inspect, not accepted premises in place of the proof.

## 1. Fixed data and precise parameter theorem

Use the released curve, generator, pole predicate, index height and Lucas lemmas:

```
K = Q(sqrt(2)), d = 3-sqrt(2), D = d^2 = 11-6sqrt(2),
E: y^2=x^3-Dx, 2E(K)=Z P_*, h(x(nP_*)) >= n^2-6.
C = {0,1,2401,-343/32}, S_* = {p:p<=76176}.
B_* = product_(p<=76176) p, B_* < 2^109445.
A19 = 2^109 * 210^1800,
H19 = 2*A19*B_*^19+128, log2(H19)<2093966.
```

Section 2 proves the last height constant satisfies `h(a)<=H19 M5(a)^19` on the same domain as the released height theorem. Put H=H19. Let integers K,q,E_s,A satisfy

```
39<=K<=64, 10<=q<=K, 20<=E_s<=38, A>=2,
(3/2)*(2^(A-1)-1) > K*2093971/(2K-76),
(3/2)*(2^(A-1)-1) > E_s*2093972/(E_s-19).
```

The arithmetic relation in Sections 3-7, using high precision K, beta precision q, scalar orders `(1,1,1,1,E_s,E_s)` and A anchor squarings, has rational input projection exactly Z. This general statement is a proof-side parameter family. It does not extend any producer's accepted configuration automatically.

The generation-ready subset recovered from the old combined producer is exactly

| Root contacts | K | q | A | E_s |
| ---: | ---: | ---: | ---: | ---: |
| 37 | 40 | 12 | 25 | 32 |
| 37 | 44 | 12 | 24 | 32 |
| 37 | 48 | 12 | 23 | 32 |

Their retained lower bounds for log2(abs(s)) are respectively 25165822.5, 12582910.5 and 6291454.5. The first required bounds are respectively 20939710, `(11/3)*2093971`, and `(12/5)*2093971`. The common scalar bound is `32*2093972/13<5154400`. These are exact rational comparisons.

## 2. The height exponent 19 follows from the existing geometric construction

The released proof supplies, for R=B_*M5(a), an absolutely simple non-CM quaternionic surface A/L, a normal field L'/Q and a primitive weight-two form f with

```
[L:Q]<=576, d'=[L':Q]<=2304R,
N<=C0 R^2, rad(N)|R, C0=210^300,
V_l(A)|G_L' = (r_l+r_l)|G_L',
(det r_l)^2|G_L' = chi_cyc^2|G_L'.
```

These are the released LR3-LR5, LT1 and modularity calculation; no bound on the coefficient-field degree is assumed. The original stable Faltings normalization, metric comparison `h(a)<=2 max(0,h_F(A))+128`, CM bound `h_F(A)<854R`, general isogeny variation and Bost lower bound are retained.

For the nebentypus epsilon of f, the weight-two determinant is `epsilon*chi_cyc`. Thus epsilon squared is trivial on G_L'. The image order of epsilon squared divides d'; consequently `t=ord(epsilon)<=2d'<=4608R`. A consistent contragredient convention replaces epsilon by its inverse and does not change its kernel or order. One may not replace L' by L in this argument: the released LR2/LT1 expressly allows the sign-splitting character order to vary with R.

Let H0=ker(epsilon) in (Z/NZ)^*, and X_H=X_1(N)/H0 for the rational diamond action. This curve and its quotient map are defined over Q. Weight two makes epsilon even, so -I lies in Gamma_H. For the newform quotient q:J_1(N)->A_f, the pullback differentials span the Galois conjugates of f. Every h in H0 acts as one on this span. Therefore `q composed with <h> = q`: their difference has zero differential, hence zero-dimensional connected image and is the zero homomorphism in characteristic zero.

The rational idempotent `e_H=(1/|H0|)sum_(h in H0)<h>` therefore satisfies q e_H=q. If H_eff is the effective diamond group and pi:X_1(N)->X_H, the Jacobian identities are

```
pi^* pi_* = sum_(h in H_eff) h,  pi_* pi^*=[|H_eff|].
```

The averages over H0 and H_eff agree. Thus the image of e_H is Q-isogenous to J_H=Jac(X_H), and A_f is an isogeny factor of J_H. This treatment removes the ineffective action of -1 rather than counting it twice. By the same Faltings-Hom, absolute-simplicity and Poincare arguments used in the released LT1-LT3, there is an L'-isogeny A times Z -> J_H. Hence g=dim J_H>=2. The source J_H is principally polarized; no bounded polarization on A or Z is postulated.

The degree to X(1) and Belyi degree bound are

```
d_H=N*t*product_(p|N)(1+1/p),  deg_B(X_H)<=d_H,
g<=1+d_H/12<=d_H.
```

For p>=5, `(1+1/p)^6<=p`; the factors at 2 and 3 multiply to at most 2. Therefore with T=2^14 C0 R^(19/6), `d_H< T` and `g<T`. The published generic congruence-curve estimate gives

```
h_F(J_H)<=13000000*d_H^5*g < 2^24 T^6.
```

It is not restricted to squarefree level or trivial nebentypus. Retain exactly the released general isogeny-height term

```
V=2g^2[8g^2 log(7g)+log(d')+log max(1,log(d'),h_F(J_H))].
```

Writing u=log(T), we have `V<=16T^4(2+u)+2T^2(25+7u)<=T^6`. The last inequality follows for T>=16 from `2+log T<=T^2/32` and `25+7log T<=T^4/4`; each holds at 16 and its difference has positive derivative thereafter. Bost gives `h_F(Z)>-3g/2`, so

```
h_F(A)<(2^24+1)T^6+3T/2<2^25 T^6=A19 R^19.
```

The CM bound is smaller. The metric comparison gives the claimed H19 inequality. Finally

```
H19 < 4*A19*B_*^19
    < 2^(2+109+1800*8+19*109445)=2^2093966.
```

The first inequality uses A19 B_*^19>64. The extra published interfaces are Baker-Gonzalez-Jimenez-Gonzalez-Poonen (2005), sections 3.1 and 3.2.1, for the newform quotient and rational diamonds; Mascot (2022), section 2.1, especially (2.1.8), for the rational quotient model; Diamond-Im (1995), section 12.5, for the determinant convention; and von Kanel (2021), section 4, equations (4.1)-(4.2), together with Javanpeykar's Theorem 1.1.1, for the general Belyi-height bound. Gaudron-Remond (2023), Theorem 1.9(1), is already the released LT3 input. No new modularity or descent theorem is introduced.

## 3. Thirty-seven raw contacts for arbitrary rational targets

Use the eight rational coefficients of the four unscaled abscissas x(nP_*), x(sP_*), x(tP_*), x(zP_*) as a_1,...,a_8. Let R0=47027, W0=25878772920, c=18484837801, V0=32W0. Set A_i=R0 a_i+3 and w_i=A_i v-u. Retain all four proxies at every one of the following 37 raw contacts:

```
v/V0, u-delta*v, -(w_i-delta*v)
(delta in C, i=1,...,8).
```

The normalized slopes are u/v and w_i/v. The released parity-of-the-common-minimum argument works for arbitrary rational u,v,w_i. Thus every odd normalized contact outside S_* is detected by at least one raw contact. This direction does not assume integer targets, prime raw contacts, or ordinariness.

For completeness fix the rational targets first and choose a positive integer D0 with D0*a_i integral. D0 is only an existence-proof choice. It is not a source variable or a fixed polynomial coefficient. Set T0=V0 D0^2, p0=c+W0*y, u=c+W0*x, v=T0*p0. For the distinct slopes b in `C union union_i(A_i-C)`, put K_b=T0*b in W0 Z and Psi_b=u-K_b*p0. All these and p0 are integer affine forms congruent to c modulo W0. Deduplicate slopes only for the analytic prime-pattern argument; restore all repeated source positions with the same prime afterward. The distinct linear parts are pairwise independent and there are at most 37 forms.

The inherited value/successor admissibility has three cases. At primes dividing W0 use the same c residue as in the released proof. At q>29 dividing D0 all K_b vanish modulo q; choose u=p0=1. At q>29 not dividing D0 the change to (u,v) is invertible. For q=31,37,41, R0*a_i vanishes modulo q, so there are at most eight slope residues. For q>=43 there are at most 36. Choose two distinct absent residues b,e, ordering them so e-b is not -T0^(-1); this is possible at odd q. Then v=1/(e-b), u=b*v avoids both zero and minus one for every form, including p0.

Choose a fixed positive cone u/v>max_i|A_i|+2413, v>0. Enlarge the inherited fixed initial cutoff beyond 82 and all relevant denominator and nonzero determinant primes. With the same unused third coordinate, the released prime-pattern proof applies to these fixed integer forms: complexity is at most 35 rather than 39. The same fiber equations `Psi_b=p+(K_b0-K_b)p0` give the upper estimates. All coefficients, D0, the box and cutoff are fixed before its large-size limit. Thus no uniformity in denominators, growing-modulus theorem, or new GI/MN hypothesis is needed. Choose the cutoff and then the box size as in the accepted proof. This gives positive ordinary primes at all distinct finite contacts and p0, with the same same-prime elliptic order conditions.

Take those primes above every divisor of D0. The infinite raw contact is D0^2*p0, with odd valuation only at p0 and valuation exactly one there. At q|D0 outside S_*, u is a q-unit, v_q(v)=2v_q(D0) and v_q(A_i)>=-v_q(D0), so both normalized slopes have the even negative valuation -2v_q(D0). Their finite-contact differences and infinity depths are even. There is no additional normalized odd contact at a denominator prime.

For each occurrence its norm root can be made a unit at its assigned prime by choosing the private witnesses sufficiently deep. All raw contacts are positive, so the norm and its parity argument are positive. Away from the assigned prime their valuations are even; the reduced denominator is a square. They are squares in Q_2,Q_3,Q_17 because p0 and the finite primes have the retained c residue, and D0^2 and the squared norm do not change square classes. These are exactly the released pole-completeness hypotheses. Repeated primes use a common orientation but may have separate private comparison witnesses.

If all relevant radical e-th powers divide a nonzero integer N0, the new H19 bound and the two slopes yield

```
h(a_i)<2H*|N0|^(19/e)+14,
h(x(Q))<4H*|N0|^(19/e)+30<5H*|N0|^(19/e)<7H*|N0|^(19/e).
```

Here H>128 and |N0|>=1. The last, weaker coefficient permits the same cutoff formulas as the old nine-target argument.

## 4. Uniform reciprocal logarithms and compressed charts

Define a0=1, a1=-2/5 and `a_j=(4j-5)a_(j-1)/(4j+1)` for j>=2. For all J>=0 let G_J(w)=sum_(j=0)^J a_j w^j. Use `L_e=z*G_(ceil(e/4)-1)(Df^2)`, f=1/x. The released differential identity is valid formally:

```
f=z^2(1-Df^2), w=Df^2,
4w(1-w)G'(w)+(1+w)G(w)=1-w,
d(zG(w))/dz=(1-w)/(1+w)=(1+4Dz^4)^(-1/2).
```

Consequently log_E(z)=zG(Df^2). At either place of a split p>76176, assume the point is nonidentity and actually in the formal group, not merely that z has positive valuation. Then r=v(z)>=1, v(f)=2r and v(w)=4r. For m=ceil(e/4)<=16, the logarithmic remainder log_E(z)-L_e(z,f) has valuation at least (4m+1)r. Indeed v_p(a_j)>=-(4j+1)/(p-1). When 4j+1<p the coefficient is integral; otherwise j>=19044, 3j>=4m and `(4j+1)/(p-1)<=j`, so `v(a_j w^j)>=4jr-j>=4mr`. These bounds tend to infinity; multiplying the G-series tail by z supplies the additional r. Formal-logarithm isometry therefore gives `L_e/log_E in 1+p^e Z_p`.

For every f in K and J>=2, G_J(Df^2) is nonzero. Under the ramified 2-adic valuation v(a+b sqrt(2))=min(v2(a),v2(b)+1/2), D is a unit and v(a_j)=1 for j>=1. If v(f)>=0, the constant is uniquely least; if v(f)<0, then v(f)<=-1/2, and the final term is uniquely least with valuation at most 1-J<0. The allowed e>=10 ensure J>=2. This proof neither assumes good reduction at two nor transfers old fixed-degree nonvanishing without proof.

Thus the released compressed charts and their exact rational maps remain valid with the new G_J's. For each primary point retain

```
f=u^2, v^2+d*f=1, p^2=x-D*f, x*f=1.
Lambda*p0=G0, Ai=Ci*pi, Ai*Lambda=Gi (i=1,...,4).
```

Use high K for G0,G2,G3,G4 and beta q for G1. From a full chart take p=yf, Lambda=-L_K(Q0)=G0/p0 and Ai=Ci*pi. Conversely nonzero Gi force all pi and Lambda nonzero; `f*p^2=(1-df)(1+df)=v^2(1+df)` forces v nonzero. Reconstruct `z=-1/p`, `y=xp`, `h=up`, `w=up/v`, the original finite logarithms and their common inverse. Then Ci=Li/L0. All external point values are fixed. Replace every primary y occurrence in subtraction equations by xp, keep every subtraction guard, and keep all common/root/difference parameters. In particular the first subtraction equation becomes `x(lambda-p)-eta=0`. The chart equations alone would allow p=0; the retained G equations rule it out.

## 5. Mixed local orders and scalar order

Use the exact field-order list `[1]*11+[q,K,K,K,K,q,K,K,K]`. The root-error test precedes the two rational tests for every field expression, so the rational list is `[1]*23+[q]*2+[K]*8+[q]*2+[K]*6`. Nothing is deleted from this 41-test list.

Start soundness at any p>76176 where a raw contact r has odd valuation R. The released constant-left norm/pole argument first excludes negative R. It then descends the norm tree to give `v_p(X/r^e)>-R`, whence `v_p(X)>(e-1)R>=e-1` and v_p(X)>=e. This works for every positive integer order, including the mixed list and scalar E_s.

The order-one root test gives v_p(theta^2-2)>=1, so Hensel selects a root rho of 2 with theta+rho a unit. For a field expression A+B sqrt(2), its rational tests are `(theta^2-2)B` and A+B theta. Their order-e bounds imply v_p(A+B rho)>=e. The order-one f tests put the primary points in the formal group at this selected place; the conjugate tests put the common J and differences in the formal group at the other place.

Write Q0=hP_*, Qi=m_i P_*, J=jP_* with nonzero integer j and target indices (n,s,t,z). The released formal-logarithm isometry and homomorphism give from the alternate tests

```
v_p((h-4)/j)>=K, v_p((m_i-4n_i)/j)>=e_i,
h=4 mod p^K, m_i=4n_i mod p^e_i,
(e_1,e_2,e_3,e_4)=(q,K,K,K).
```

Thus h is a unit. The primary ratios, the relative finite-logarithm errors and q<=K imply integral proxies and

```
beta=n mod p^q, (xi,tau,zeta)=(s,t,z) mod p^K.
```

The scalar batch retains the two coefficients each of f(J0), f(S), z(S)/z(J0), with orders `(1,1,1,1,E_s,E_s)`. Its first four tests make J0=j0P_* and S=sP_* formal at every place over every relevant prime, including inert primes. The last pair gives `v_p(s/j0)>=E_s`, so v_p(s)>=E_s. The scalar raw polynomial detects every prime of M5(beta), including any odd infinite contact, and its small-prime correction is a unit outside S_*. Therefore

```
M5(beta)^E_s divides s,  h(beta)<=H*abs(s)^(19/E_s).
```

## 6. The two global contradictions

The same anchor calculation at 2 and 3, with A squarings, gives exactly the nonzero subgroup `s in 2*3^(2^(A-1)-1) Z`. Put a=abs(s), B=max(abs(n),abs(s),abs(t),abs(z)). The parameter inequalities imply

```
a>(24H)^(K/(2K-76)),
a>(40H)^(E_s/(E_s-19)), a>40,
h(beta)<a/40, log(40H)<a/40.
```

For the logarithm bound, E_s<=38 gives E_s/(E_s-19)>=2, so a>(40H)^2. The inequality `40 log(40H)<(40H)^2` holds at H=1, and the derivative of the right side minus the left side is `3200H-40/H>0` for H>=1. Thus log(40H)<a/40.

Let Delta=t^2-s(s-2)tz+(s-2)^2 z^2-1. If Delta is nonzero, the three high-order proxy congruences at every contact, the retained proxy Lucas equation, Section 3 and the index height imply

```
B^2-6<7H*abs(Delta)^(19/K)
     <7*5^(19/K)H*B^(76/K)<16H*B^(76/K).
```

Here abs(Delta)<5B^4 and K>38. Hence `B^(2-76/K)<22H<24H`, contradicting the first cutoff. Delta=0, so the unchanged Lucas growth lemma gives log B>a-3.

If beta differs from n, take N0=abs(num(beta-n)) in lowest terms. The beta congruences at every contact give

```
B^2<7H*N0^(19/q)+6, N0<=2 exp(h(beta))*B.
```

With alpha=19/q<2 this yields `B^(2-alpha)<40H exp(alpha h(beta))`, since `7*2^alpha+6<34<40`. Thus

```
log B < q/(2q-19)*log(40H)+19/(2q-19)*h(beta)
      < (q+19)/(40*(2q-19))*a
      <=29*a/40<a-3.
```

This contradicts Lucas growth. Thus beta=n is an integer. The unchanged relation X^2=beta-2, with X rational in lowest terms, forces its denominator to be one, so X is an integer.

For avoidance of doubt, the exact proved general parameter family in this packet restricts `20<=E_s<=38`; the three producer tuples all have E_s=32. No E_s outside that range is certified by the diagnostic.

## 7. Completeness in the correct order

For an integral input choose the scalar sign and small-prime square class exactly as in the released proof. Choose J0 deep at the finitely many scalar-contact places, then a positive s in the anchor subgroup with all additional required divisibilities. Arbitrarily deep choices make every scalar normalized leaf integral or sufficiently divisible and its norm root a unit. E_s=32 weakens the released order48 requirement; the same finite-depth construction works for any specified finite positive order. Apply Lucas existence and obtain the four nonzero target points.

Apply Section 3 to their eight rational abscissa coefficients; no clearing-denominator source variable is introduced. For the set P of distinct ordinary primes selected there, put j=lcm_(p in P) d_(p,2), J=jP_*. At each p choose h_p simultaneously satisfying

```
h_p=0 mod d_(p,1), h_p=4 mod d_(p,2),
h_p=4 mod p^(K+v_p(j)), h_p notin {0,4,-4}.
```

The released gcd and p-unit conditions prove compatibility. Set Q0=h_pP_* and Qi=h_p n_i P_*. The primary points are formal at the first place and their differences `(h_p-4)n_i P_*` and J are formal at the second. All required alternate and primary orders follow; lower q imposes no additional condition. Nonvanishing in Section 4 makes all compressed reverse maps and old ratios defined. Choose the single theta last to meet the actual coefficientwise requirements at every occurrence, not merely a guessed order K. The inherited norm/pole construction and Section 3's square factors give all remaining witnesses. Input coordinate zero is unchanged throughout.

## 8. Exact compiler obligations and limits

The recovered generator has explicit named profiles: K40 uses `block3/a6/s1`, K44 `powers45/unit/s1`, K48 `block3/a6/s1`; beta12 uses `direct/unit/s1`. All return quadratic G expressions with no separately bound G output. The independent circuit checker must verify those particular profiles and their generic product consumers. K40 and K44 each use four internal field pairs; beta12 uses one. These are local structural counts, not combined variable savings.

The independent source audit must bind all six regenerated original modules before mutation, every changed logarithm coefficient, both beta positions in the mixed list, scalar orders, anchor shared-chain length and final coordinate, all 37 root calls and their direct rational coefficient arguments. It must retain all four proxies per contact, the constant-left norm path, correction bits and products, all guards, and all external occurrences. It must check flattening independently. The new source then requires a fresh lift, independently replayed reductions, mutation tests and full collected coefficient expansion. An old source digest or old logarithm rule cannot substitute for these checks.

The arithmetic results above do not measure whether the combined quartic is below 10,000 variables and do not prove its final coefficient maximum. They justify testing the stated new sources.
