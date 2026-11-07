# Proposed PR #4 title

Refine the quartic proposal to 924 variables, with a 900-variable direct-target candidate

# Proposed PR #4 description

## Summary

The branch integrates upstream Version 8 at `5856286a57fba19574a40704571ee70e79738281` and preserves the frozen 933-variable ordinary-coefficient package. A new exact rational weight circuit reduces that design to **924 variables**. Combining it with the separately documented direct-target proposal gives a **900-variable candidate**.

| Construction | Variables including input | Quadratic residuals | Monomials | Maximum coefficient bits |
| --- | ---: | ---: | ---: | ---: |
| Frozen ordinary-coefficient package | 933 | 890 | 51,907 | 3,247 |
| Mixed weights, doubled targets | 924 | 881 | 51,880 | 3,247 |
| Mixed weights, direct targets | 900 | 857 | 51,252 | 3,247 |

Both new polynomials have degree four and primitive content one. The upstream and historical fork artifacts are preserved.

## Changes and justification

The existing exponent-19 height refinement, comparison precisions 12/40, degree-nine logarithm circuit, redundant-inverse removal and explicit constant chain remain in place. The new change computes the detector weights in eight gates instead of nine:

    a=e², b=a², c=b², d=c²,
    a*f=d², g=f²,
    c*q12=q1*f, b*q40=q12*g.

These equations give q12=q1*e^22 and q40=q1*e^78. Every new denominator is a power of e. The retained inverse and norm equations force e!=0 on every source solution, so this is an exact reparameterization in both directions. It saves one variable per detector without new height or local estimates.

The direct-target variant additionally replaces 2P*,2Qi by P*,Qi. Its separate soundness and common-index completeness argument is documented, but still requires independent mathematical review. The 900-variable count must not be read as certification of that arithmetic argument.

## Review and reproduction

Start with [research/mixed-weights-20261107/README.md](https://github.com/scduko/diophantine-z-q-explorations/blob/combined-comparison/research/mixed-weights-20261107/README.md). It includes the exact projection proof, all new denominator obligations, input pins and reproduction commands. The new variants are generated on demand; the earlier 933 package remains the frozen compressed artifact set.

Both new variants passed the unchanged compiler and independent algebraic checker, elimination-certificate checks, full ordinary-polynomial replay, constant-chain projection and numerical height budgets. All ten emitted logarithm polynomials and all nine emitted mixed weight circuits were separately checked. This includes inspecting the actual quotient denominators, not only a handwritten exponent chain.

Ordinary polynomial SHA-256:

- 924: `bff480cc9d5984716cba5e34529dbdd5a1373256acb6452a20a1bf82dab4129b`
- 900: `444f6bee0839d9df052fec4764458245c8b5d81d460c03ecb022c808c4410bad`

The intuitive proof architecture is in `research/overnight-20261106/INTUITIVE_PROOF.md`; the exact comparison thresholds are in `research/overnight-20261107/COMPARISON_LEMMA.md`.

## Dependency and review boundary

Finite algebraic checks do not certify the inherited height theorem, elliptic-curve group calculation, local arithmetic or simultaneous-prime construction. Version 8's Gaussian-appendix repairs have been integrated; the full analytic argument has not been independently re-proved by this work. Independent human mathematical review remains pending, and Lean formalization remains incomplete.

The new circuit, proof notes and verification scripts were developed with AI assistance under the repository owner's direction. Upstream construction and compiler/checker attribution are preserved. No global minimality claim is made.
