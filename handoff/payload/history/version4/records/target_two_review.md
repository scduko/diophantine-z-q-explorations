# Independent review of comparison targets 2Qi

Date: 2026-11-06. Verdict: PASS for the mathematical refinement of the reviewed doubled-index, general-E root proposal. This is not acceptance of an emitted source or a claimed coordinate saving.

Reviewed `precision/sub5000/root-doubled-indices/TARGET_TWO.md`, SHA-256 `cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb`. It depends on the root proposal `ecdbfc9acd575a8ab194f8e76c356e7898544a506c705a40f169c6686c70a80e`, its already reviewed root-chart appendix, and the unchanged primary/difference, reciprocal, norm/pole and H19 arguments. No new external arithmetic input is needed.

## Which finite groups occur

I read the inherited prime-pattern statement and its Frobenius-count argument in the released manuscript, SHA-256 `dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552`. The numbers there called d1,d2 are explicitly the cardinalities of the two full reduced elliptic curve groups. The inherited conclusions are gcd(d1,d2)=4 and p not dividing d1*d2. They are not orders of the particular generator and not orders of a quotient group. The unit change to the current normalized curve preserves these finite groups up to isomorphism at the selected good primes.

At each selected p>76176, the good reduced curve has the four distinct rational two-torsion points O,(0,0),(d,0),(-d,0). The characteristic is odd and D=d^2 is a unit. Thus the kernel of multiplication by two on E(Fp) has exactly four elements. The elementary finite-group homomorphism formula gives

```
|2E(Fp)|=|E(Fp)|/4=N/4.
```

This statement does not require cyclicity. Every element of the image is annihilated by its order N/4. Since reduction is a group homomorphism at good reduction, the reductions of 2Qi and P*=2R belong to this image. There is no assumption that the image of the global subgroup 2E(K) equals all of 2E(Fp); containment is sufficient.

Writing M1=N1/4 and M2=N2/4 gives gcd(M1,M2)=1, because gcd(N1,N2)=4. Neither Mi is divisible by p. These are exactly the two properties needed by the new CRT.

## Completeness

Root data, all eight abscissa coefficients and their denominator data are fixed first, just as in the reviewed root proposal. The ordinary prime pattern may still avoid primes dividing the nonzero integer s for normalized Lucas. At each selected prime fix the orientation; repeated occurrences may use that same orientation.

Set j_c=lcm_p M_(p,2) and J=j_c P*. Then J is a nonzero global point and is formal at every opposite place. For each occurrence choose

```
k=0 mod M_(p,1),
k=1 mod M_(p,2),
k=1 mod p^(40+v_p(j_c)),
k not in {0,1,-1}.
```

The first two moduli are coprime and both are prime to p. Thus the progression exists and is infinite, allowing the finite exclusions. No orders from different rational primes need to be coprime.

Take X0=kP* and Xi=k(2Qi)=k*n_i*P*, where 2Qi=n_i P*. These points are nonzero because k and each n_i are nonzero. Their reductions lie in the first doubling image, which k annihilates. Their differences from the new targets are Y0=(k-1)P* and Yi=(k-1)n_i P*. The factor k-1 annihilates the second image, so these differences are formal at the opposite place. The excluded value k=1 makes them nonzero for complete witnesses. They lie in the torsion-free global subgroup ZP*, so none is a nonzero two-torsion pole.

The formal logarithm identities are exactly

```
log(Xi)/log(X0)=n_i,
log(Y0)/log(J)=(k-1)/j_c,
log(Yi)/log(J)=(k-1)n_i/j_c.
```

Their alternate valuations are at least40. The integrality of n_i suffices; it need not be a unit. The beta order12 is therefore also satisfied. These are the same local inputs used by the reciprocal and normalized-Lucas completeness arguments. All field coefficients remain fixed before the private conic approximation and pole witnesses are chosen.

Other primes may divide j_c through other image orders. The explicit v_p(j_c) term absorbs this effect, so the construction introduces no hidden cross-prime condition. The finite exclusion k=-1 is harmless and also avoids opposition if an older affine difference chart were used; the current joint chart already permits it.

## Soundness at arbitrary raw-contact primes

This direction does not use the special prime-pattern cardinalities. At any odd raw-contact prime above the unchanged cutoff, the existing norm/pole and private-conic proof supplies a selected split place and all field orders, after excluding negative odd raw valuation. The old positive-f tests still select the primary O formal group.

For arbitrary source points write

```
2X0=hP*,  2Xi=m_iP*,  2Qi=n_iP*,  2J=j_dP*.
```

The root J is general-E, so the correct soundness variable is its integer doubled index j_d. It is nonzero, but no source condition requires J itself to lie in 2E(K). With the new targets,

```
2(X0-P*)=(h-2)P*,
2(Xi-2Qi)=(m_i-2n_i)P*.
```

The retained alternate tests and the reviewed joint-graph argument give valuations of (h-2)/j_d and (m_i-2n_i)/j_d. A difference may be O or (0,0); both have zero doubled index and the intended infinite valuation. The other two nonzero two-torsion differences are genuine z-poles and remain excluded by the joint equations. Near (0,0), the previous doubled-point valuation argument applies without a new sign assertion.

Since j_d is an integer, h is congruent to2 modulo p^40 and m_i to2n_i modulo the required order. Hence h is a unit at every consumed odd prime. The exact torsion-safe group identity [2h]Xi=[2m_i]X0 gives the primary logarithm quotient m_i/h. It is congruent to n_i and is integral. The reciprocal estimates therefore give precisely the same C_i congruences as before.

In complete witnesses j_d=2j_c. This accounts for the apparent factor-two difference between the soundness and completeness notation. Two is a local unit throughout; it is not an omitted denominator condition.

The beta test remains C_A-2beta. The scalar raw polynomial remains the original polynomial in beta, with all six scalar orders unchanged. The first and second height contradictions, H_eff=5H19, full two-place anchor and final denominator argument therefore need no alteration. In particular the eight height targets remain the original coefficients of x(Qi), not the coefficients of x(2Qi).

## Source contract required

The fixed target must change to 2R=P*, and each variable target to 2Qi. The first doubling of every variable root must remain, including its reused x^2 pair and tangent nonzero gate. Only its second doubling may be removed after complete incidence checking. All shared target coefficients, conjugated slots and current target metadata must refer to the resulting double. The root carrier and beta factor two from the general-E proposal must be implemented together with this refinement; this note is not an isolated target rewrite on the published or current old-carrier source.

For reference, I independently checked the new fixed values

```
x(P*) = 57/8 - (7/2)sqrt(2),
q(P*) = y(P*)/x(P*) = -87/41 + (129/164)sqrt(2),
1/x(P*) = 456/1681 + (224/1681)sqrt(2).
```

They satisfy q^2=x-D/x. Their exact source binding, any chosen denominator clearing and the final SOS coefficient bound remain implementation obligations. Metadata such as fixed_4R, quadruple and Fq(R4) must be replaced truthfully. The common J source chart remains general-E; J=j_c P* is only the completeness choice.

The required independent checks are the final target constructors, every removed second-doubling coordinate's incidence, all beta/scalar/anchor consumers, fresh module and flattening maps, and complete replay and expansion. No source count or final coefficient maximum follows from this mathematical review.
