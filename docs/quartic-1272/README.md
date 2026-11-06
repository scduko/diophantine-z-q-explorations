This directory contains the source-application inventory for `quartic_1272.tex`, Version 5. It preserves the earlier inventories and binds their reviewed passages to the current manuscript individually. New applications have their own source versions, theorem locators, hypotheses, conventions, translations, review status, and current line anchors.

The current register covers 203 explicit citations to 83 bibliography entries, 101 external application families, eight inherited source ledgers, 127 internal results, and 19 arithmetic interfaces. It verifies 465 inherited application passages and 147 inherited citation passages. These counts include the retained Version 4 material. The 101 families comprise 82 baseline applications, five later inherited applications, and 14 new applications; the embedded ledgers retain their finer source-level entries.

| File | Contents |
| --- | --- |
| `new-applications.json` | Authored new applications, internal review records, interface dependencies, source qualifications, and evidence pins. |
| `theorem-applications.json` | Complete inherited and new application records with current manuscript anchors. |
| `inherited-bridge.json` | Exact passage comparisons from Version 4 to Version 5. |
| `citations.json` | Every explicit citation, its locator and paragraph, and its application or attribution classification. |
| `internal-results.json` | Every declared result, its statement and proof spans, explicit dependencies, and review status. Separate soundness/completeness proofs and titled detached proofs are included. |
| `dependency-graph.json` | Explicit references and authored arithmetic interfaces. |
| `bibliography.json` | Current bibliography text and its hashes. |
| `coverage.json` | Counts, manuscript pin, unresolved items, and qualifications. |
| `evidence/` | Reviewed manuscript fragments, source and review receipts, and exact foundation comparisons. External full texts are not redistributed. |

The Frei–Tinková proof-scope supplement in `evidence/FT_PROOF_SCOPE.md` and `evidence/FT_PROOF_DEPENDENCIES.json` records 36 proof nodes and 11 published-parent records. It distinguishes inspected arguments from proof steps that remain external inputs. The main application inventory and dependency graph include this supplement without treating its open proof nodes as established. Paths inside archived review documents refer to the original audit workspace; descriptions of collected source files do not mean those full texts are redistributed here.

Run these commands from the repository root with Python 3.10 or later:

```sh
python -E -B docs/quartic-1272/inventory.py validate --repo . --manuscript quartic_1272.tex
python -E -B docs/quartic-1272/test_inventory.py
```

After an authorized editorial change, regenerate the derived anchors with:

```sh
python -E -B docs/quartic-1272/inventory.py build --repo . --manuscript quartic_1272.tex
```

Both commands reject unresolved items by default. `--allow-review-items` is for preparing an incomplete register. It does not produce an acceptance verdict. `--expected-input-sha256 HASH` additionally checks the authored register against an externally selected hash. The release handoff descriptor pins the delivered files.

Regeneration cannot approve changes inside the three reviewed mathematical fragments. Their bytes must match their review pins, and their normalized text must occur exactly once in the current manuscript. A changed fragment needs a new review receipt and an explicit register update. A new citation or result outside those fragments also needs a record. The tests check these failures, changed inherited passages, missing references, broken dependency identifiers, and altered evidence pins without editing the repository.

`PASS_DOCUMENT_BINDING` means the registered document checks pass. It is not a formal proof certificate, a fresh proof of the inherited mathematics, or verification of every external paper's proof. The independent mathematical reviews and finite polynomial certificates have their stated scopes.

The five inherited qualifications remain in `coverage.json` and `theorem-applications.json`: the existing proof and assumption status; corrected prime-pattern versions and errata; the inspected Pan author theorem and Calegari formulation; the author-attested Yuan translation; and the fixed Faltings metric, arithmetic Frobenius, effective diamond quotient, and final primitive-form twist. Exact unchanged passages preserve those qualifications rather than upgrading them.

Version 5 also records these source limits explicitly:

- Frei–Tinková, Theorem 1.4, is checked against arXiv:2408.17441v3. The author lists the work as accepted/to appear in *Mathematika*. No final published version was verified, and its new internal proof steps remain an external input.
- Browning–Loughran and Browning–Heath-Brown are published works. Exact application checks used their pinned accepted manuscripts and compared preprints; the final typeset texts were not inspected.
- Dodos–Kanellopoulos is a published work. Theorem 5.1 was checked in arXiv version 4, dated after journal publication. The final typeset statement was not compared. The appendix uses it in an explicit repair of the majorant norm exponent inside the imported Frei–Tinková proof route.
- Voight's Proposition 14.6.7 was inspected in the published 2021 chapter, page 232, using equivalence (iii) with (v). A local byte-identical copy of that chapter was not obtained. The older corrected-book hash is a different version.
- Brox's working source supplies attribution. The delivered 1272-coordinate construction is independently rebuilt and reviewed; it is not identified with the unavailable original 1315-coordinate table.

The arithmetic interfaces use the original five-contact constant and exponent 24, the new scalar order 32, and the newly proved unramified local logarithm statement. They do not transfer the later exponent-19 source or the older split-prime restriction silently. The new CM reduction lemma treats the two Gaussian norms as group cardinalities and hence annihilators, without asserting exact point orders.
