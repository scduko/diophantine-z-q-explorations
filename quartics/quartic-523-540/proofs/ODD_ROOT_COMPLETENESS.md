# Odd root labels: input, shifted scalar point, anchor, and Pell witnesses

This note supplies the scalar and Pell part of the proposed product-height construction. It does not itself prove the product-height lemma or implement the odd-coset point charts.

## Source changes

1. Replace the input expression by `beta=2X^2+3`.
2. The four comparison root points remain `A=nP,S=aP,T=tP,Z=bP`, and the proposed source requires all four labels to be odd.
3. In the scalar norm tree and the three-witness physical anchor, replace the point `S` by `R=S-P=(a-1)P`. The root `S` in all comparison tests and height scales remains unchanged.
4. Retain the current fixed anchor constant `Sfixed=3^(2^26)`. The primary margin calculation below suffices. A larger-constant variant is recorded separately if a later height-transfer constant requires it.

The shifted point can be computed by the retained guarded subtraction formula. Its abscissa-difference guard excludes `a=1` and `a=-1`. These exclusions do not affect completeness, which chooses a positive and arbitrarily large a. The resulting R is a finite nonidentity point in `2E(K)`, so the inherited ordinate, reciprocal and local-parameter domain lemmas apply.

The file `odd_scalar_patch.py` applies changes 1 and 3 to either the full-log or compressed-log builder. Its scalar `PS` then supplies both the scalar leaves and the physical anchor, so no separate anchor replacement is necessary. The comparison root `points.S` is preserved.

## Input equivalence and contact domains

For integral X, beta is a positive odd integer. Conversely, if X=u/v in lowest terms and beta is integral, then `v^2 | 2u^2`, hence `v^2 | 2`; thus v=1 and X is integral.

For every rational X, beta>=3. Therefore none of beta, beta-1, 32beta+343, or 2beta-1 vanishes. The remaining possible zero beta=2401 would give `X^2=1199`, impossible because 1199 is not a rational square (34^2<1199<35^2). Consequently the original scalar polynomial

    r=beta(beta-1)(beta-2401)(32beta+343)(2beta-1)

is nonzero. At every odd prime a negative valuation of beta is twice the negative valuation of X, so is even. This is exactly the fact used by the scalar soundness argument above the fixed prime cutoff. The prime two is below that cutoff.

## Scalar soundness

Put `s=a-1`, and let H=hP be the shared comparison anchor. The scalar point is now R=sP. The original scalar proof, with its parameter s in place of a, applies without any other change: the order-one leaves make H and R formal at every consumed prime; the ratio `z(R)/z(H)` has valuation `v_p(s/h)`; the order-32 leaves imply

\[
 M_5(\beta)^{32}\mid s,\qquad
 h(\beta)\le H_{19}|s|^{19/32}.
\]

No claim that the odd point aP itself is formal is made or needed. That claim would be false in the required generality.

## Primary anchor margins: unchanged fixed constant

Retain `Sfixed=3^(2^26)` and put `c=|a-1|`. The existing exponent-19 anchor calculation gives `c>(40H19)^10`. Consequently

\[
 |a|\ge c-1>(39H_{19})^{10}>(24H_{19})^{10}.
\]

With the existing height-transfer coefficient `7H19`, the first (Lucas) contradiction gives `B<(24H19)^10`, exactly as before, and is therefore impossible. The scalar inequality gives

\[
 h(\beta)\le H_{19}c^{19/32}<c/40,
 \qquad \log(40H_{19})<c/40.
\]

The second contradiction would imply

\[
 \log B<\frac{12}{5}\log(40H_{19})
       +\frac{19}{5}h(\beta)
       <\frac{31}{200}c<c-4\le |a|-3.
\]

The strict inequality `31c/200<c-4` holds for c>5, amply guaranteed by the anchor. Lucas growth gives the opposite strict inequality `log B>|a|-3`. This treats both signs of a and requires no change to the fixed coefficient or the explicit constant-chain length. The product-height lemma must, of course, retain the stated height-transfer coefficient (or provide a numerical replacement).

## Optional larger anchor with more generous constants

The unchanged three-witness anchor applied to R=sP with `Sfixed=3^(2^27)` forces

\[
0\ne s\in 2\,3^{2^{25}-1}\mathbf Z.
\]

Writing `A=|s|`, the published elementary bound gives

\[
\log_2 A>50331647.5.
\]

The exponent-19 constant satisfies `1<=H19<2^2093966`. Since `10^4<2^14`, this proves the deliberately generous bound

\[
 A>(10^4H_{19})^{20},
\]

because `20(14+2093966)=41879600<50331647.5`.

It follows that

\[
 H_{19}A^{19/32}<A/100,
 \qquad \log(400H_{19})<A/100.
\]

For example, the first follows from `A^(13/32)>100H19`; the second follows immediately from the displayed twentieth-power lower bound. These bounds are uniform in the sign of a. The elementary inequalities

\[
 |a|\ge A-1,\qquad \log B>|a|-3\ge A-4
\]

replace the old uses of `|a|`, where `B=max(|n|,|a|,|t|,|b|)` and the second inequality is the inherited Lucas growth conclusion.

For clarity, these margins also tolerate any product-height transfer bound of the form

\[
 B^2\le K|N|^{19/k}+6,\qquad 1\le K\le100H_{19}.
\]

For the Lucas discrepancy, `k=40` and `|N|<5B^4` would imply

\[
 B^{1/10}<K5^{19/40}+6<300H_{19}+6,
\]

contradicting `B>=A-1` and the anchor bound. For the beta discrepancy, `k=12` and `|N|<=2e^{h(beta)}B` give

\[
 \log B<\frac{12}{5}\log(400H_{19})
            +\frac{19}{5}h(\beta)
        <\frac{31}{500}A<A-4,
\]

again contradicting Lucas growth. Constants larger than this stated range require a fresh numerical substitution; the argument does not silently assume an unproved product-height estimate.

## Scalar completeness with odd a

Fix an integral X, hence odd n=beta. Choose the original finite correction c making `cr` positive and locally square at 2,3,17. Choose h0 positive and divisible by 64, sufficiently deep at the finite support of cr, exactly as in the original scalar completeness lemma. Now choose a positive integer s sufficiently divisible relative to h0 that the point R=sP satisfies all normalized-leaf valuation conditions and the physical anchor.

In particular s is even and divisible by three. Define `a=s+1`. Then a is positive, odd, congruent to one modulo three, and arbitrarily large. The root point S=aP has the required odd label, while its shifted point S-P is precisely the previously chosen R. The scalar construction and its local continuity modulus are therefore exactly those of the old proof.

After R (and therefore S) is fixed, the scalar functions are rational functions of H with the same domain and local continuity properties. One obtains a congruence `h=h0 mod L` with `64|L`, preserving the scalar conditions. Replacing the comparison target shift by one in the already-reviewed construction remains compatible with this modulus; no new prime-distribution hypothesis is introduced by the scalar shift.

## Odd Pell witnesses

For the positive odd a above, define the Lucas sequence

\[
 U_0=0,\quad U_1=1,\quad U_{j+1}=aU_j-U_{j-1}.
\]

Modulo two, because a is odd, the sequence has period three `0,1,1`. Modulo a-2 it satisfies `U_j=j`. Put

\[
 k=2(a-2),\qquad b=U_k/(a-2),\qquad t=U_{k+1}.
\]

The quotient b is a positive integer because a-2 divides k and hence U_k. Since `a=1 mod3`, one has `k=1 mod3`. Thus U_k and U_(k+1) are odd. The denominator a-2 is odd, so b is odd; t is odd as well. The standard Lucas identity gives

\[
 t^2-a(a-2)tb+(a-2)^2b^2=1.
\]

Therefore all four root labels n,a,t,b can be chosen positive and odd, with the scalar conditions and the anchor already fixed. The subsequent simultaneous-prime and common-index choices have exactly the old quantifier order: first these labels and height scales, then the fixed scalar continuity modulus, then contact primes, then a common h.

## Reusing the odd-coset carrier when available

If the odd-index module represents `S=P+2R` with an already constructed point `R=sP` in `2E(K)`, it is preferable to use that R directly in the scalar block and anchor. No new subtraction point is needed. In this variant `a=2s+1`, so the scalar bound is `h(beta)<=H19|s|^(19/32)` and the anchor controls `|s|`. All preceding soundness margins become stronger because `|a|>=2|s|-1`. Completeness chooses s positive and arbitrarily divisible exactly as before, and then a=2s+1 is odd and congruent to one modulo three. The same k=2(a-2) gives odd Pell witnesses. This reuse is valid only when the point module actually retains R with the stated arithmetic meaning; it should not be inferred from an unrelated square-abscissa chart variable.
