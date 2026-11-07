# Further refinement: 1,180 ordinary-coefficient variables

Status: arithmetic proposal; exact algebraic replay passed; independent mathematical review pending.
All counts include the input coordinate. This is additive to the preserved 1,267-variable package.

| Cumulative change | Variables | Residuals | Monomials | Maximum coefficient bits |
|---|---:|---:|---:|---:|
| Previous ordinary-coefficient construction | 1,267 | 1,224 | 45,480 | 4,059 |
| Detector quotient and pole fusions | 1,240 | 1,197 | 45,493 | 4,059 |
| Quotient for delta cubed | 1,222 | 1,179 | 45,559 | 4,019 |
| Quotient for the detector weight | 1,204 | 1,161 | 46,020 | 3,247 |
| Doubled comparison targets | 1,180 | 1,137 | 44,048 | 3,247 |

The first three changes preserve the rational source projection. The fourth changes the arithmetic witness construction and is justified separately below. Compiler elimination accounts for the savings in this table; raw gate counts alone do not predict them.

## Sources and retained dependencies

The source is Version 5 at upstream commit `bf2fe53459c0cceff74566ea9b966eca54d11ca5`, pinned file by file in `INPUTS.json`. The starting refinements, exponent-19 height bound, comparison orders 12/40, scalar order 32 and explicit anchor chain are exactly those in `ARITHMETIC.md`. The source point-domain, two-anchor and two-reduction lemmas are in `docs/quartic-1272/evidence/reviewed-new1272.tex`, labels `lem:v5-point-domains`, `lem:v5-two-anchors`, and `lem:v5-two-reductions`; its source-projection theorem supplies the common-point completeness construction. The earlier finite-doubling-image observation is preserved in `docs/quartic-4973/evidence/target_two_proof.md`. That older note uses different index conventions: the argument below uses Version 5 indices throughout.

All inherited arithmetic hypotheses, including the simultaneous quadratic prime-pattern theorem and the qualifications about the height theorem, remain in force. This note does not replace them with a computational certificate.

## Detector quotient domains

Work over the rationals. In one detector write its positive scale as A, contact product as F, delta=t−1, weight e=(A delta)^5/F, and w=w0+w1 sqrt(2). The existing w0 inverse remains. Put

    N=(w0²−2w1²)/(2w0).

Since w0 is nonzero and 2 is not a rational square, N is nonzero. Replace the old inverse of e and the product R=1/(e delta), followed by B=R N², with

    E=e delta,     B E=N².

Every new solution has E nonzero, hence e and delta nonzero. Conversely every old solution uniquely supplies E and the same B. This recovers the removed e inverse and R, so no spurious rational solution is introduced.

Next replace the delta inverse and q1=e/delta³ computation with

    delta³ q1=e.

The previous equation already forces delta nonzero. Thus the removed inverse is recovered uniquely and this quotient has precisely its stated meaning.

Finally replace the F inverse and weight computation with

    F e=(A delta)^5.

The scales are nonzero on every solution of the unchanged point equations: A0=1, A_(2j−1)=x_(j,0)², and A_(2j)=(1+x_(j,1)²)². The point-domain lemma gives

    x(2(alpha,eta))=((alpha²+D)/(2eta))²>0

at both real embeddings, where D=(3−sqrt(2))² is totally positive and eta is nonzero. Consequently x_(j,0), the average of these two positive abscissae, is positive. Every scale A is therefore positive. Since delta is already nonzero, the new weight equation forces F nonzero. Its inverse can be recovered uniquely. This proves both directions of the source-projection equivalence for all three quotient changes without presupposing the main integrality theorem.

## Pole fusion

For each of the nine preparation-zero poles introduce eb=e b. The original first conic and h definition become

    p²−17b−34eb+51(eb)e=0,
    h=17eb−(eb)b.

Indeed 17b(1−e)(1+3e)=17b+34be−51be² and e(17b−b²)=17eb−eb b. The second conic is unchanged. These are polynomial identities, with no added division or domain assumption. Preparation-one scalar poles are unchanged.

## Doubled targets: soundness

Retain Q_i=[n_i]P*, H=[h]P*, U_i=[u_i]P* and 2E(K)=Z P*. Change the targets from 4P*,4Q_i to 2P*,2Q_i. Thus

    V0=H−2P*,     Vi=Ui−2Qi.

All point and subtraction guards remain. The doubled targets are finite nonidentity points of 2E(K), so the point-domain lemma still applies. At any consumed prime p>76176, split or inert, the full logarithm ratios in the two-anchor argument are now

    r_i=u_i/h,     r'_i=(u_i−2n_i)/(h−2).

The guards give h nonzero and different from 2. At least one of h,h−2 is a p-unit, so its ratio is integral. The unchanged cross test makes the other truncated ratio integral. The relative logarithm errors are consequently absolute errors at the required orders k_i=12,40,40,40. Hence L_i is congruent to both exact ratios modulo p^k_i. Multiply by h and h−2 and subtract to obtain 2L_i congruent to 2n_i, then divide by the p-unit 2. At inert primes conjugation preserves the valuation, just as in the parent proof. All subsequent height contradictions and the final integrality conclusion are unchanged.

## Doubled targets: completeness with one common index

Repeat the parent scalar and real-continuity construction with the translated target 2 in place of 4. Choose h0 positive and divisible by 64; it avoids 0 and ±2, so the new comparison denominators are nonzero there. The translation maps remain nonconstant, and their finite pole sets satisfy the same real-progression lemma. This gives a continuity modulus L divisible by 64. Select the contact primes using the same simultaneous prime theorem and avoidance modulus, after the scales and L have been fixed.

For each selected split prime let d_−(p),d_+(p) be the two full reduced group orders. The parent theorem gives

    v2(d_−)=6,   v2(d_+)=2,
    gcd(d_−(p),d_+(q))=4 for every pair p,q,

and no odd prime factor of L divides either order. The separate congruences modulo 7 remain part of this assertion.

At these good odd primes, the reduced curve has exactly four rational points in the kernel of doubling: the identity and the points with abscissae 0,d,−d. Therefore the subgroup 2E(F_p) has order d_±(p)/4. Since P* belongs to 2E(K), its reduction belongs to this subgroup and is annihilated by that order. No cyclicity or exact order of P* is asserted.

Put M_±=lcm_p(d_±(p)/4). Then

    gcd(M_−,M_+)=1,
    gcd(M_−,L)=16,   gcd(M_+,L)=1.

The congruences

    h=0 mod M_−,   h=2 mod M_+,   h=h0 mod L

are compatible, because 16 divides h0. Choose a sufficiently large positive h in their common progression attaining the real bounds and avoiding 0 and ±2. Set H=hP*, Ui=hn_iP*. At every primary place H and Ui are formal; at the opposite place V0=(h−2)P* and Vi=(h−2)n_iP* are formal. Both exact logarithm ratios equal n_i. The unchanged 12/40 approximation estimates supply every comparison test, while the continuity congruence preserves the scalar tests. The remaining contact, norm, conic and pole witnesses follow from the parent construction. The quotient-domain equivalences above recover the refined detector witnesses.

## Reproduction and scope of verification

Run from the repository root:

```sh
python3 -B research/combined-comparison/refine.py --out /tmp/refinement-replay
python3 -B research/combined-comparison/check_refined_artifacts.py
```

Use a new output directory. The generator checks pinned inputs and runs the unchanged independent algebraic checker for every stage. The artifact replay verifies compressed and uncompressed hashes, the explicit constant-chain projection, exact height budgets, all elimination certificates, coordinate maps, and the full sum-of-squares expansion. The output has degree four and primitive content one; all coefficients are ordinary integer strings. The symbolic parameter metadata used by the checker is unused, as in the previous package.

The checker does not prove the nonvanishing arguments or the arithmetic construction in this note. Independent mathematical review remains pending. The new quotient organization, pole fusion, adaptation of the doubling-image argument, code and checks were developed with AI assistance under the repository owner's direction; the underlying construction and compiler/checker remain credited to the upstream authors. No minimality claim is made.
