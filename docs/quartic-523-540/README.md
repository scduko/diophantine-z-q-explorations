# Version 9: the 523- and 540-variable quartics

Version 9 integrates Gabriel Conant's November 7 odd-product and asymmetric-depth construction, developed with ChatGPT. The original archive is identified by SHA-256 `fcb169b0fe78b7d8c7badec083f23b543901ae0efa17f9bc38f3025511764141`. The [arithmetic audit](evidence/AUDIT.md) and [source lineage](evidence/SOURCE_LINEAGE.json) predate integration and retain their original scope statements.

| Construction | Total variables | Witnesses | Degree | Monomials | Largest absolute coefficient |
| --- | ---: | ---: | ---: | ---: | --- |
| Symbolic coefficient table | 523 | 522 | 4 | 35,163 | `64 * 3^(2^27)` |
| Complete decimal coefficient table | 540 | 539 | 4 | 35,213 | `3^2048 + 1005072314631333 < 2^3247` |

The symbolic table uses the fixed integer `S = 3^(2^26)`, not an additional variable. A unique 17-coordinate squaring chain gives the ordinary table. Both have primitive content one. The [decimal text file](../../quartics/quartic-540-fully-expanded.txt) occupies 708,848 bytes; the [symbolic text file](../../quartics/quartic-523-symbolic-coefficients.txt) occupies 706,737 bytes. The JSON version is [here](../../quartics/quartic-523-symbolic-coefficients.json).

## Dependency closure

The [manuscript addition](addition.tex) gives the chart replacement, direct targets, smaller-anchor calculation, odd-coset equations, product-height identity, scalar shift, two height contradictions, asymmetric-depth argument, prime-separation lemma, and final projection theorem. It identifies the inherited statements at their actual labels in the same manuscript.

The direct targets use `P_*` and `Q_i`, which already belong to `2E(K)`. Full rational two-torsion makes the doubling-image orders `d_±/4`; the proof checks the resulting CRT overlaps. The smaller anchor is recalculated with `C=3^(2^25)` and `S=C^2`, giving `log_2|a-1| > 25165823.5`. The order-32 scalar argument uses the same norm tree, then applies the established exponent-19 height theorem to the new label `2X^2+3`.

The final local proof transfers integrality before claiming depth twenty. Prime separation comes from the existing fixed-field weighted count: remove the strip `w<N^(1/3)` by choosing the diagonal slowly, then apply Hasse's bound and full two-torsion. This does not assume an extra prime-pattern theorem.

The arithmetic chain still uses the manuscript's restricted converse, five-contact height theorem, and Gaussian prime argument. Their proofs and source-version qualifications remain those of the existing inventory. Integration does not turn the contributor's conditional-on-source audit into a fresh independent verification of all those earlier arguments.

## New theorem applications and conventions

[new-applications.json](new-applications.json) records four additional applications of the pinned 2009 second edition of Silverman, including exact statements, hypotheses, maps, valuation conventions, and translations. The source SHA-256 is `72ee67bfa1e3fdf582ac7e4b032d7ca0b35a168ed6443ac39c121fbb788cab25`.

1. The integral formal group near infinity uses `z=-x/y`. At the place above two the proof constructs an open subgroup directly and uses compactness for finite index; it does not apply a minimal-model proposition to a possibly nonminimal equation.
2. Proposition VII.2.1, pages 188–190, supplies closure of the nonsingular-reduction subgroup at the prime above seven. The equation is minimal there, and `P` reduces to `(1,6)`.
3. Theorem V.1.1, page 138, applies over `F_p`, not `F_(p^2)`, at the split good-reduction primes. The group order includes infinity.
4. Proposition IV.5.5, Lemma IV.6.3 and Theorem IV.6.4, pages 129–132, give the normalized formal logarithm and isometry on `r>=1>1/(p-1)` in the unramified completions. The stronger truncation error is proved separately from the manuscript recurrence.

The [derived inventory](inventory.json) rebinds the existing 125 application families and eight ledger bridges to unchanged text and traces the new derivations to source labels. The exact [revision](revision.json) accounts for every change from Version 8. Source-level bindings are mechanically checked; mathematical truth is not decided by an inventory validator. The existing qualifications about checked author versions versus final published typesetting are retained.

## Reproduce

From the repository root, with Python 3.10 or newer and Node.js 18 or newer:

```sh
python -B scripts/check_odd_product.py
python -B docs/quartic-523-540/inventory.py validate
python -B -m unittest discover -s docs/quartic-523-540 -p test_inventory.py -v
```

The first command rebuilds both precursors, checks the gate certificates, runs each final verifier twice, independently checks eliminations and complete sums of squares, compares the text downloads, and confirms that all pinned inputs remain unchanged. Its outputs go to `build/odd-product/`; no external Python packages are needed. The intermediate 554/571 tables remain in the package for reproducibility, not as current records.

The [verifier repair](evidence/READONLY_VERIFIER.patch) replaces writes to two hash-pinned JSON inputs with equality checks against the recomputed values. The original Windows bug made a second run fail after newline conversion. The integrated [provenance record](../../quartics/quartic-523-540/INTEGRATION.json) records old and repaired verifier hashes; the manifests cover the repaired files. Polynomial data are unchanged.

Finite checks and internal AI arithmetic review have passed. No completed Lean proof or independent human peer review is claimed.
