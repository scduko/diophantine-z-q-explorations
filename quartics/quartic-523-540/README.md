# Odd elliptic indices: 554- and 523-variable quartics

All variable counts include the rational input; all witnesses range over Q.

| Construction | Total variables | Degree | Quadratic residuals | Quartic monomials |
|---|---:|---:|---:|---:|
| Odd-product height | 554 | 4 | 523 | 33,440 |
| With a small-coefficient constant chain | 571 | 4 | 540 | 33,490 |
| Odd-product height and asymmetric formal depth | 523 | 4 | 492 | 35,163 |
| Depth version with the constant chain | 540 | 4 | 509 | 35,213 |

The main new argument proves exact additivity of the heights of abscissae of odd multiples of the repository's fixed elliptic point. Enforcing oddness lets one product replace four separate height quantities, reducing nine detector blocks to three. Modified input labels, a shifted scalar point, and odd Lucas witnesses establish completeness. The additional depth argument replaces five primary truncated logarithms by local parameters; its completeness uses a prime-separation consequence of the existing quantitative prime-pattern proof.

Read `h10-odd-product-reduction.pdf` (TeX source alongside it) for the combined proof. The `proofs/` directory contains the component arguments and adversarial AI reviews. `previous-chart-proof.pdf` supplies the previous point-chart reduction used as the starting source. The inherited direct-target argument is included as `UPSTREAM_DIRECT_TARGETS.md`.

The 554- and 523-variable tables use the exact fixed integer coefficient S=3^(2^26), written symbolically. S is not a coordinate. The other two versions add 17 uniquely determined coordinates and write every coefficient in decimal; their maximum coefficient bit length is 3,247. Every polynomial has primitive content one.

## Replay

From this directory run:

    python3 source-reproduction/reproduce.py --packages .

This requires Python 3.10+ and Node 18+, with no third-party dependencies or network access. It rebuilds both source systems, runs the pinned upstream compiler and independent checker, checks the match to the frozen precursors, and verifies all four final quartic tables. Each final directory also has its own standard-library-only `verify_all.py` for the final elimination, constant-lift and complete coefficient checks.

The source bundle and both final packages have separate hash manifests. The top-level `SHA256SUMS.json` covers every delivered file other than itself. The source replay receipts include successful runs from a fresh copied directory.

## Scope and provenance

These constructions retain the arithmetic dependencies of elliotglazer/diophantine-z-q, with the direct-target variant at commit 772c4adf4a05e21255e4c1784e08e917fda4c68a and main snapshot 5856286a57fba19574a40704571ee70e79738281. The preceding construction used 833 variables with the same fixed symbolic coefficient, or 850 with the constant chain.

The new arithmetic arguments received separate adversarial AI review. The finite certificates verify the algebraic construction and counts, not the entire number-theoretic proof of the repository. No independent human peer review or complete formalization is claimed. The source builders retain a historical S=3^(2^27) descriptive header; the final packages and replay explicitly correct only that metadata to the audited S=3^(2^26), with all algebraic identities formal in S.

Developed with ChatGPT for Gabriel Conant, November 7, 2026. No changes were published to GitHub.
