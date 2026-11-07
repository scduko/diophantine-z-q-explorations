# Independent adversarial review of the odd-index product architecture

## Accepted exact height lemma

The proof in `architecture/scales/odd_product_height.tex` is correct. At any finite place with v(D)=0, use the finite group E(K_v)/E_1(K_v). The class of T0=(0,0) has order two and x(Q+T0)=−D/x(Q). If one odd multiple of P is formal, the class of P has odd order, so no multiple can belong to T0+E_1. If no odd multiple is formal, all their x valuations are nonnegative. Therefore all odd multiples have the same weak valuation sign.

The sole place with v(D)>0 is δ=3−sqrt(2) above7. The source P reduces to nonsingular(1,6) on y²=x³; the nonsingular-reduction subgroup is closed under multiplication. Positive x valuation would force reduction to singular(0,0), so it never occurs on this orbit. This proves the required common weak sign there too.

At both real embeddings, nonidentity points in2E have x>δ>1. Thus all local positive-part logarithms add exactly, and

    h(product_i x([n_i]P)) = sum_i h(x([n_i]P))

for odd n_i. There is no bad-prime error or asymptotic qualification. The corollary with three scales retains the numerical factor7H; the same proof works with exponent19/k in the current source instead of historical24/k.

## Accepted odd-coset chart

Put ε=1+sqrt(2), R=(ε,2sqrt(2)), so P=2R. The inherited source proves2E(K)=ZP. Any halfpoint B of nP has B=nR+T for T∈E[2]. The standard x-squareclass homomorphism has α(R)=ε and torsion image{1,−1,δ,−δ}. The torsion classes have equal signs at the real embeddings, whereas ε has opposite signs. Hence α(B)=ε forces n odd. Conversely for oddn a torsion translate of B has α=ε, because the four torsion classes exhaust that factor of α(B).

The added equations

    t²=2(x+j), th+x+j=ε r²

on the existing chart x=h²,j²=x²−D,y=hj give the old halfpoint abscissa a=th+t²/2. The identity a(a−t²)=D forces a,t nonzero, and b=at gives an affine halfpoint with2B=(x,y). Its class is exactly ε. Conversely, the chosen torsion translate of a halfpoint with class ε supplies r. The h,j chart choices may change signs, but the actual x,y point and all downstream rational functions stay unchanged.

## Accepted shifted scalar point and odd Pell choices

Only the scalar tree and anchor use R_scalar=S−P, whose index is a−1; the comparison root S remains aP. This preserves the scalar theorem with |a−1| in place of |a|. Its added subtraction guard excludes a=±1, both irrelevant to the large positive completeness choice.

For completeness choose the old scalar index s arbitrarily divisible and positive, in particular divisible by2 and3, then set a=s+1. Thus a is odd and congruent1 modulo3. For U_0=0,U_1=1,U_(j+1)=aU_j−U_(j−1), choose k=2(a−2), t=U_(k+1), b=U_k/(a−2). The congruence U_k≡k modulo(a−2) proves b integral. Modulo2 the sequence is0,1,1 periodically; k≡1 modulo3 makes t,b odd. The Lucas identity is the required exact equation.

For integer inputX, β=2X²+3 is odd. Conversely β integral forces the reduced denominatorv of X to satisfy v²|2, hencev=1. The scalar contact β=2401 would require X²=1199, impossible overQ; the other contacts lie below3. The required even negative valuations at odd primes are unchanged.

## Anchor margins

No larger fixed coefficient is needed. With c=|a−1|, the existing S=3^(2^26) anchor yields log2c>25,165,823.5. Since log2H<2,093,966, this implies c>(80H)^10. Hence |a|≥c/2>(40H)^10, while

    h(β)≤Hc^(19/32)<c/80≤|a|/40,
    log(40H)<c/80≤|a|/40.

The original two PR4 height contradictions therefore apply with the same constants. The sharper margins in `ODD_ROOT_COMPLETENESS.md` are also valid.

## Source composition and finite checks

Read the actual integrated builder diff against the earlier source. OnlyA,S,T,Z receive odd-coset witnesses; the sharedH and comparisonU points remain unrestricted, as required because the common index is even. Product scales use exactly the four root abscissas. The scalar-point patch changes only scalar/anchorPS, not comparisonrootS. Pole allocation and detector loops both shrink from9 to3.

Fresh independent upstream checks passed for both precursors:

* Full-log odd-product source:561 coordinates,530 residuals,495 gate identities,484 compiler operations,32,857 monomials.
* Asymmetric-depth odd-product source:532 coordinates,501 residuals,458 gate identities,436 compiler operations,34,248 monomials.

The optional asymmetric-depth refinement composes correctly: roots, scales and scalar continuity modulus are fixed before selecting primes; only afterward is the common index chosen with the additional primary-depth congruence. Its separate prime-separation proof remains necessary and was audited in `log-depth-review.md`.

The final packages must specify S=3^(2^26) explicitly; the reusable raw-builder metadata still carries the historical S=3^(2^27) label. Circuit identities are formal inS.

## Scope

These are new soundness/completeness constructions relative to the inherited arithmetic theorems. They are not assertions that every old witness tuple lifts to the new odd-coset system. The exact height identity is unconditional arithmetic of the displayed curve; the integer-projection conclusion additionally uses the source generator, scalar-height, five-contact and pole-completeness results. No stronger external prime-pattern theorem is needed for the primary full-log version.
