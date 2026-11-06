# Joint arithmetic contract for rational differences, private conics, and the four-witness anchor

Date: 2026-11-06. This proves the rational-input projection for the source family `H19-root37-rational-conic-anchor4-v1` specified in `JOINT_SOURCE_CONTRACT.json`. It is ready to bind to an emitted source after the checks in the final section. No new polynomial, source digest, or endpoint count is accepted by this document alone. Version 3 remains unchanged.

The joint contract has SHA-256 `e658843c6ba95dc797f10e7c25c086189f9694a0689a88c203979c38f05ed79e`. It records the frozen component proofs and helper bytes read. The three new proof files are:

| Proof relative to `work/quartic-sub10000-20261106/` | SHA-256 |
| --- | --- |
| `charts/sub5000/RATIONAL_DIFFERENCE.md` | `8558cbfdb09bfaf12054caa2907900bc30b6de91fd6ab43c14ddc294f1cd7e9d` |
| `precision/sub5000/ODD_DISCRIMINANT_PAIR_COMPRESSION.md` | `ef4de3f02fa3d17c18dc7c2af490960a62f35cc541eac8e4b80958d320fa8ab9` |
| `parity/sub5000/ANCHOR_FOUR_PROOF.md` | `9d349ae5caaaa9ed4433617762ecb4b8b349af58c2082ffa4b9be08442ba18e3` |

The H19/rational37 proof and the three-mode coverage proof remain `precision/PROOF.md`, SHA-256 `258d07739bed4bd114580a51bbbbeac07f6b5f6441024db2f7c19ed237b7818f`, and `precision/THREE_MODE_CONTACTS.md`, SHA-256 `66311fffec418e9a6aa44f7f7503057133f92e21c4f70c3468971dd04ac55659`. The normalized curve, integer carrier, height lower bound, formal-group and reduction-order statements, Lucas lemmas, pole predicate and prime-pattern inputs are inherited with their existing source-version qualifications. The new anchor uses the explicit published trace facts in Koenigsmann's Proposition 6 proof, not only the older equality T=S+S. There is no new unpublished external input.

## The relation to be emitted

The rational input is X. Work over K=Q(sqrt(2)), encoded in the rational basis 1,sqrt(2), with conjugation fixing the first coefficient and negating the second. Set d=3-sqrt(2), D=d^2=11-6sqrt(2), and E: y^2=x^3-Dx. The retained root charts put A,S,T,Z and the auxiliary points in G=2E(K)=Z P_*. Write their integer indices as n,s,t,z and write the common comparison point as J=[j]P_*, j != 0. The inherited height bound is h(x([m]P_*))>=m^2-6.

Use beta=X^2+2 and rational proxies xi,tau,zeta. The source's historical code labels `s,t,z` for these proxies do not make them integer indices. The root equation is

```
tau^2-xi*(xi-2)*tau*zeta+(xi-2)^2*zeta^2-1=0.
```

The integer indices s,t,z belong to S,T,Z; they need not initially equal those rational proxies. Soundness below uses local congruences between them. Completeness chooses the proxies equal to the indices.

Retain the eight unscaled rational coefficients of x(A),x(S),x(T),x(Z) as the height targets a_i, in that order. With delta in {0,1,2401,-343/32}, the 37 raw contacts are

```
v/(32*25878772920),
u-delta*v,
u-(47027*a_i+3)*v+delta*v,       i=1,...,8.
```

Their position modes are full at 0..4 and 21..28, beta-only at 5..12, and Lucas-only at 13..20 and 29..36. Thus all 29 positions covering S,T,Z retain the Lucas comparisons, and all 21 positions covering A,T retain beta. No raw position is removed or merged, even if values or primes coincide.

The five shared targets are Q0=4P_*, Qbeta=4A, Qs=4S, Qt=4T, Qz=4Z. Their affine coordinates and original doubling chains remain. Each target Q=(a,b) supplies F,q through aF=1 and aq=b. The comparison boundary means the two coefficients of F followed by those of q. These are not the root height targets.

The four-witness anchor is

```
C*H-9*C^2-3*f0^2-3*f1^2=0,
H^2-8*U^2-12*V^2+24*W^2-4*C^2=0,
C=3^(2^25),       f0+f1*sqrt(2)=f(S)=1/x(S).
```

The existing shared chain supplies this exact nonzero C. The scalar batch remains unchanged with orders 1,1,1,1,32,32.

Each retained private point P has f,x,p with xf=1 and p^2=x-Df, representing P=(x,xp). For its target F,q introduce t_den,M,T_den,A_alt with

```
t_den=fF,
M*(1+D*t_den)=p,
T_den=2x-pq+2M(q-p),
A_alt*conj(T_den)+conj(q-p)/conj(z(J))=0.
```

The last expression uses the retained inverse of conjugate(z(J)); it does not introduce division in the polynomial source. No primary square condition or separate difference-formal test remains. The private points are independent between occurrences. There are 13*5+8*2+16*4=145 private point/difference pairs.

For each mode, the field list consists first of all primary f values followed by the already-conjugated f(J), then all retained primary proxy errors C_i-b_i, then all A_alt values in target order. The exact field orders are

| Mode | Field count | Orders |
| --- | ---: | --- |
| Full | 15 | `[1]*6+[12,40,40,40]+[40,12,40,40,40]` |
| Beta-only | 6 | `[1]*3+[12]*3` |
| Lucas-only | 12 | `[1]*5+[40]*7` |

There are 435 fields in total. The full-mode G precisions are 40,12,40,40,40; beta-only uses 12,12; Lucas-only uses 40,40,40,40. All compressed G equations and the common logarithm denominator remain.

Each occurrence passes r and the ordered rational coefficient pairs of these fields to its own conic batch. For F_i=A_i+B_i sqrt(2), introduce a private triple theta,s_c,S_c and equations

```
S_c=s_c^2,       theta^2-r*S_c=2,
Y_i=A_i+theta*B_i,
r^(2e_i)*W_i=2*A_i*Y_i-A_i^2+2*B_i^2.
```

Coefficients A_i,B_i are affine in retained comparator coordinates and independent of the private conic triple. Powers use the deterministic multiplication circuit. There is no contact inverse or epsilon leaf in this batch. Sort the fields by order, stably within each order, and build the successive-pair N_r(a,b)=a^2+r*b^2 tree on literal1 followed by the W_i. Carry any last unpaired node. The upper level sizes are 16,8,4,2 for full, 7,4,2 for beta-only, and 13,7,4,2 for Lucas-only. If its root is N, keep the original pole predicate Psi(r*N^2).

This first implementation retains the old root-global theta_g,epsilon_g, their equation epsilon_g=theta_g^2-2, and the 31/16/26 comparison interfaces. The corresponding two free slots are ignored. There must be no comparator residual, field coefficient, conic input, or power depending on them. This harmless auxiliary graph always has rational solutions, for example theta_g=0 and epsilon_g=-2. It has no role in the local embeddings selected below. Retaining it is a definitional extension of the frozen conic proof, not a second approximation requirement.

## Soundness of the new anchor

Put a=f0/C and b=f1/C. The two anchor equations say that h=9+3(a^2+b^2) is a rational norm-one trace for the quaternion algebra (2,3). This algebra is ramified precisely at 2 and 3, and its local trace sets are integral there. At 3, v(a^2+b^2)=2min(v(a),v(b)) because -1 is nonsquare in F_3. At 2, it is 2m when the valuations differ and 2m+1 when they agree and are finite. In either case m<0 would make h nonintegral at that prime. Zero inputs are included by valuation infinity. Hence a,b are integral at both primes.

Conversely, such integral a,b make h a permitted local trace: at 3 it is zero modulo 3; at 2 it is either odd or divisible by four. Odd traces are supplied by the published U2 condition. Every h in 4Z_2 is also a trace. With x0=h/2, if x0=2 mod4, choose v^2=(x0^2-1)/3 and u=w=0; if x0=0 mod4, choose w^2=1-x0^2/6 and u=v=1. The indicated units are 1 mod8. The published local-global trace equality supplies rational witnesses. Thus the new anchor is exactly equivalent to the old two semilocal conditions, with all other coordinates fixed.

The inherited anchor argument therefore still gives s in the nonzero subgroup 2*3^(2^24-1)Z. This is a statement about the integer index of S, not the rational proxy xi.

## Every odd raw contact yields all required field orders

Take any p>76176 with R=v_p(r) odd. This is an arbitrary rational source solution; neither primality of r nor ordinariness at p is assumed. The conic makes r and s_c nonzero, since otherwise theta^2=2 over Q. Write epsilon=theta^2-2. Then E=v_p(epsilon)=R+2v_p(s_c) is odd. A negative valuation of theta would make E even; a positive valuation, or a unit epsilon, would give E=0. Therefore theta is a unit and E>0 is odd. Select rho^2=2 with theta-rho divisible by p. Then theta+rho is a unit and v_p(theta-rho)=E.

At each upper node the summand valuations 2v(a) and R+2v(b) have opposite parity, so there is no cancellation. The literal1 path makes the root N nonzero. The pole theorem gives v_p(r*N^2)>0. If R<0, ascent along the all-left constant path would give v_p(N)<=0, a contradiction. Hence R>0.

Starting from v_p(N)>-R/2, descent through the finite tree gives v_p(W_i)>-R. Therefore

```
v_p(2*A_i*Y_i-A_i^2+2*B_i^2)>(2e_i-1)R>=2e_i-1,
```

and this valuation is at least 2e_i. The polynomial identity

```
2*A_i*Y_i-A_i^2+2*B_i^2=Y_i^2-epsilon*B_i^2
```

has summands of opposite valuation parity. It follows that v_p(Y_i)>=e_i and E+2v_p(B_i)>=2e_i. Hence v_p((theta-rho)B_i)>=e_i+E/2>e_i, and v_p(A_i+rho B_i)>=e_i. Zero coefficients and zero fields are allowed. This recovers exactly the field orders in the table; it does not assume their coefficients are integral in advance.

## The enlarged private-point domain still gives the index congruences

Global nonvanishing of both G_2(Df^2) and G_9(Df^2) holds for every f in K. Under the ramified 2-adic valuation, D is a unit and every nonconstant coefficient has valuation one. If v(f)>=0, the constant is the uniquely least term; if v(f)<0, then v(f)<=-1/2 and the last term is uniquely least because the degrees are at least two. The retained equations Lambda*p0=G0 and aux_i=C_i*p_i, aux_i*Lambda=G_i therefore force all p_i and Lambda nonzero. Each P=(x,xp) is a nontorsion affine point, without needing a squareclass premise.

For a point/target pair set B=1+DfF and k=q-p. Its equations give B != 0, M=p/B and T_den=2x-pq+2pk/B. If T_den=0, the last equation forces k=0; then (x-a)B=0, so P=Q and T_den=(x^2+D)/x != 0. Thus T_den is nonzero. The represented rational function is Z=-k/T_den=z(P-Q), and A_alt=conj(Z)/conj(z(J)). The chord identity proves this away from equal abscissas. At P=Q it is Z=0 and the identity difference; at P=-Q it is the doubling formula. The potential difference T0=(0,0) has B=0 and is excluded. For the other two nonzero two-torsion differences, direct translation formulas give B*T_den=0 and hence exclude them too. These are exactly the reviewed rational chart's open conditions.

The recovered primary f orders put each primary point in the formal group at rho. The recovered conjugate(f(J)) order puts the nonzero J in the formal group at the opposite place. At that opposite place, the alternate order gives

```
v(Z)>=e+v(z(J))>0.
```

For a nontorsion affine R=(X_R,Y_R), z(R)^2=X_R/(X_R^2-D). If v(z)>0, then v(X_R) cannot be zero. If v(X_R)<0, R is formal. If v(X_R)>0, R+T0 is formal because x(R+T0)=-D/X_R, and z(R+T0)=-z(R). Consequently 2R is formal in both cases and v(log(2R))=v(z(R)), since p is odd. The identity difference gives infinite valuations and needs no inverse.

Define the half-integer alpha(P) by 2P=[2alpha(P)]P_*. This is possible and unique from 2E(K)=Z P_*. These indices are integral at every relevant odd prime. Write h=alpha(P0), m_i=alpha(Pi). The target index is 4n_i. The exact integer-multiple identity

```
[j](2(Pi-Qi))=[2(m_i-4n_i)]J
```

and formal logarithms give v(Z/z(J))=v((m_i-4n_i)/j). Since j is an integer, the alternate tests imply h=4 mod p^e0 and m_i=4n_i mod p^ei. Thus h is a p-adic unit.

At the primary place, the exact identity [4h]Pi=[4m_i]P0 gives log(Pi)/log(P0)=m_i/h. It uses integer multiples and avoids a possible two-torsion discrepancy. For a nonidentity formal point and e=12 or 40, the frozen reciprocal-tail argument gives L_e/log in 1+p^e Z_p. It controls the whole infinite tail, including later coefficients divisible by p. The compressed ratio equations give C_i=L_i/L_0 exactly. Hence the primary-error tests imply b_i=n_i mod p^ei, with the rational proxy b_i p-integral.

This gives beta=n mod p^12 at every full or beta-only occurrence and (xi,tau,zeta)=(s,t,z) mod p^40 at every full or Lucas-only occurrence. It is valid for arbitrary odd raw contacts, including the initially possible negative ones. No global integrality of h,m_i is used.

Different occurrences of the same p may select opposite roots rho in soundness. Each occurrence proves the same rational proxy/index congruence. The global argument combines these rational congruences, not selected embeddings. A common J constrained at both orientations is then formal at both, which is consistent with every required local step. Completeness below chooses consistent orientations anyway.

## The unchanged height arguments force the input to be integral

Let B_*=product_(p<=76176)p and

```
H=2*(2^109*210^1800)*B_*^19+128,       log2(H)<2093966.
```

The unchanged scalar batch gives M5(beta)^32 | s, hence h(beta)<=H|s|^(19/32). The anchor gives a=|s|>40 and

```
log2(a)>25165822.5,
a>(24H)^10,
a>(40H)^(32/13),
h(beta)<a/40,              log(40H)<a/40.
```

The numerical cutoffs are strict: log2((24H)^10)<20939710, and log2((40H)^(32/13))<32*2093972/13<5154400. They are below the anchor lower bound. The logarithm estimate also follows from a>(40H)^2 and the elementary inequality 40log(40H)<(40H)^2 for H>=1.

Conic nonvanishing makes every raw contact nonzero. Thus the normalized rational37 slopes avoid their marked points, and the inherited parity-of-the-common-minimum coverage applies. For any relevant coefficient, its two slopes have every odd contact outside the fixed small set detected by one of its five common or four private raw positions. If the relevant prime powers divide a nonzero integer N0, the H19 two-slope estimate gives h(x(Q))<7H|N0|^(19/e). The original rational height coefficients have not been replaced by F,q or private quantities.

Set B_L=max(|s|,|t|,|z|) and Delta=t^2-s(s-2)tz+(s-2)^2z^2-1. If Delta != 0, the proxy Lucas equation and the 29 retained Lucas positions give the required 40th-power divisibilities for the S,T,Z height bounds. Since |Delta|<5B_L^4,

```
B_L^2-6<7H|Delta|^(19/40)<16H B_L^(19/10),
B_L^(1/10)<22H<24H.
```

But B_L>=a>(24H)^10. Therefore Delta=0. The inherited Lucas lemma, with z != 0 and a>=7, gives the specific bound |t|>exp(a-3).

Suppose beta != n, put N0=|num(beta-n)|>=1 and B_AT=max(|n|,|t|). The 21 retained beta positions cover all A,T height coefficients. They give

```
B_AT^2<7H N0^(19/12)+6,
N0<=2exp(h(beta))*B_AT,
log(B_AT)<(12/5)log(40H)+(19/5)h(beta)
         <(31/200)a<a-3.
```

This contradicts B_AT>=|t|>exp(a-3). Thus beta=n is an integer. Since X is rational and X^2=beta-2 is an integer, its reduced denominator is one. Hence X is an integer. The proof never needs the rational proxies to equal integer indices globally before these deductions.

## Completeness in the required order

Given an integer X, choose beta=n=X^2+2. Use the inherited scalar construction and choose a positive integer s in the same anchor subgroup, with all needed scalar divisibilities. Choose t,z by the inherited Lucas existence lemma and set xi=s, tau=t, zeta=z. This fixes the nonidentity root points and their eight rational abscissa coefficients. The new anchor has witnesses because its relation is exactly the old one.

Choose the denominator-clearing integer D0 only in the existence proof. The rational37 prime-pattern construction then gives finite raw contacts equal to assigned positive ordinary primes and infinity equal to D0^2 times its assigned prime. All assigned primes are 1 mod8, above the cutoff and the fixed denominator divisors, and have the retained same-prime reduction-order properties. Analytically duplicate slopes can be deduplicated for the theorem and restored as separate source occurrences. No new uniformity in denominators or cross-prime order theorem is used.

Choose j as the lcm of the selected conjugate reduction orders. At each occurrence choose its own private h_p, satisfying h_p=0 modulo the primary reduction order, h_p=4 modulo the conjugate order, and h_p=4 to sufficiently high p-adic depth including v_p(j). The inherited same-prime gcd and unit conditions make these compatible. Avoid h_p=0,4,-4. Set the occurrence's private points to [h_p]P_* and [h_p n_i]P_* for its retained targets only. Do not share these private choices between different primes. These points lie in G, have positive abscissas at both real embeddings, and lie in the rational chart's B*T_den != 0 domain. The rational formulas fix all four difference coordinates and their exact alternate ratios.

Now all field coefficients are fixed, independently of the private conics. At an occurrence r=d0^2p, p=1 mod8, use norm Euclideanity of Z[sqrt(2)] to write p=A^2-2B^2 with B != 0. This gives a rational point theta0=A/B, s0=1/(d0B) on theta^2-rs_c^2=2. Lines through this point give the explicit rational parametrization from the frozen conic proof. Rational approximation of its parameter supplies a point arbitrarily close to the chosen rho branch, with E=v(theta^2-2) positive odd and arbitrarily large.

Choose E large enough for every actual B_i at this occurrence. The old field valuations and the correction theta-rho then make Y_i and the packed numerators have orders at least e_i and 2e_i. Since v_p(r)=1, every W_i is integral. The upper norm tree is integral with a unit root, by its constant-left path. Because r>0, its real root is positive even if an individual W_i is negative. The argument r*N^2 is positive, has valuation one at the assigned prime, even valuations elsewhere, a square reduced denominator, and the retained Q_2,Q_3,Q_17 square classes. The old pole-completeness theorem gives its witnesses.

Each occurrence has its own conic, so repeated primes cause no simultaneous-conic constraint. Choose the same orientation at repeated primes as in the inherited point construction. Finally assign any rational theta_g and epsilon_g=theta_g^2-2 to the unused global auxiliary graph. This proves completeness of the emitted relation under the joint contract.

## Final emitted-source checks

The following are binding obligations, rather than conclusions from a source identifier or a successful search:

1. Pin the complete builder/helper/checker bytes and the old baseline regeneration. Bind the emitted source family, source ID, canonical source hash, residual-file hash, module hashes, shared constants and flattening map. The module set must be exactly the ten names in the joint JSON contract.
2. Reconstruct the root from the pinned rational37 root, keeping the original affine height targets, root charts, doubling chains, scalar calls and original input X. Verify all 37 positions and the exact 13/8/16 input selections. Check the five F,q targets against the retained affine targets.
3. Check the new anchor's two literal equations and the same C at global index -26. Check the scalar batch against its unchanged module, including orders 1,1,1,1,32,32 and all correction factors.
4. Reconstruct all 145 private point/difference blocks and all G/ratio circuits. No primary square-transfer or membership equation may be required by the checker as a substitute for the half-index proof. Conversely, every inverse, curve and G equation used to prove p,Lambda,B,T_den nonzero must be present.
5. Check each mode's full ordered field expressions and precision list, not only its field count. Confirm already-conjugated J inputs are not conjugated a second time. Check alternate signs and conjugations against A_alt*conj(T_den)+conj(q-p)*inv_conj_zJ=0.
6. Verify one separate conic triple per occurrence, its exact raw r, every affine coefficient pair, all powers r^(2e), stable sorting, all upper nodes/carries, the literal constant path, root square, and exact pole argument. The total is 37 private conics and 435 packed fields.
7. Prove through incidence that the old global theta_g/epsilon_g slots are ignored by every comparator and every conic coefficient. Their sole retained mathematical relation is the old root equation. The new batch has neither the old epsilon leaf nor an unreviewed contact inverse. Any later deletion of the harmless global graph requires its own exact source or certificate account.
8. Run malformed-source tests for wrong position/mode, wrong field/order, double conjugation, shared conic coordinates, wrong raw factor, wrong norm sign/exponent, missing constant path, altered anchor C and hidden legacy-root dependencies. Then perform independent flattening, fresh quadratic lifting, every reduction replay, and complete collected coefficient expansion. Report total variables including X, degree, monomial count, weights, coefficient maximum and hashes from that actual output.

The elementary arithmetic above supplies the new source theorem only after those checks establish that the emitted equations implement this relation. Future two-denominator charts, scaled parity fusion, global sharing of private points, H18 parameters, and scalar conic conversion are excluded from this contract and need separate justification.
