# Product-height quartics: 554 and 571 total variables

All counts include the unchanged rational input. All witnesses range over Q.

| Representation | Variables | Quadratic residuals | Quartic monomials |
|---|---:|---:|---:|
| Fixed coefficient S=3^(2^26) | 554 | 523 | 33,440 |
| Ordinary decimal integer coefficients | 571 | 540 | 33,490 |

Both polynomials have degree four and primitive coefficient content one. The ordinary table's maximum coefficient bit length is 3,247. S is a fixed integer, not a variable in the first polynomial.

## Architectural change

The integer labels of the four root points are restricted to odd integers. For the fixed generator P*, the height of the product of their four abscissae is exactly the sum of their heights. This follows from the parity of the order of P* in each local formal-group quotient; at the sole prime dividing D, P* has nonsingular reduction. Both real abscissae are greater than one, so the archimedean terms are also additive. ODD_INDEX_HEIGHT.tex supplies the precise lemma and proof.

Consequently one K-valued product replaces four separate K-valued height quantities. Only three coordinate detectors remain: the unscaled detector and the two rational-component scales of the product. The odd-point charts, modified input label, scalar shift and completeness conditions are part of the accompanying mathematical proof. Deleting six detectors without that proof would not be valid.

This primary variant retains the full truncated logarithms. It does not use the optional asymmetric-depth refinement or its prime-pattern thinning step.

## Exact algebraic package

source561.json is the frozen quadratic source for this final stage. The certificate removes 7 coordinates using exact polynomial identities and invertible affine shears. The reverse maps preserve the input pointwise. Each displayed quartic is the complete sum of squares of its primitive integer quadratic residuals.

The ordinary-coefficient system adds seventeen uniquely determined coordinates c0,...,c16, where c0=3^1024 and c(i+1)=c(i)^2. Thus c16=3^(2^26), and substitution for S preserves quadratic residual degree. These are genuine additional rational witnesses with unique values.

Run `python3 verify_all.py` from this directory. Only the Python standard library is needed. The verifier checks the manifest, independently replays the elimination certificate, checks the constant lift and normalizations, and independently expands both full quartics and compares every coefficient. The producer compiler and search code are not imported. It also verifies support, coordinate maps, degree and primitive content.

The finite checks prove the exact algebraic statements above, not the number-theoretic source characterization of Z. The new architecture and its arithmetic proof require mathematical review. The source still inherits the repository's arithmetic inputs and PR4 direct-target convention. No independent human peer review or complete formalization is claimed.

## Metadata and provenance

The source builder retained a descriptive S=3^(2^27) header. This package corrects that header to the intended, audited S=3^(2^26). No residual coefficient is changed; the elimination identities are over Q[S]. PROVENANCE.json records the pre-correction source hash. SUMMARY.json records the actual final counts and table hashes.

The elimination and independent elimination verifier adapt the repository's version6 routines. The added constant-lift and full-table verifier uses separate direct polynomial arithmetic. The new work was developed with AI assistance for Gabriel Conant.
