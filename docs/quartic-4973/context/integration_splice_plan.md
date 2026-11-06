# Version 3 to selected new quartic: splice plan

This is a plan, not an edited manuscript. Final counts, hashes, filename and release date must come from the accepted endpoint. No proposed endpoint is accepted here.

Inputs are the published `work/quartic-sub10000-release/repository/quartic_9625.tex`, SHA256 `dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552`, and the reviewed `precision/sub5000/publication-draft/revision-3/CONTENT.tex`, SHA256 `e67b256be73b41fca2e74958ebf0f9749e78f5d98f0c05c06118d3d156defc85`. All line numbers below refer to that exact Version 3 file unless stated otherwise. The companion `SPLICE_INVENTORY.json` records exact spans, normalized excerpt hashes, labels, references, and old metadata values. `build_splice_inventory.py` reproduces it by reading the two inputs only.

## Preserve the two-result structure

Keep the original huge-polynomial abstract claim at lines 41–45, Theorem `thm:target` at 63–79, its polynomial, bounds, construction and proofs. Keep the substantive material before the quartic section and the inherited appendices and bibliography after it. Update only the active quartic teaser at 47–48 and 94–100, together with authorized release metadata at 35–37. Keep the author blank and retain the existing credit statement unless the root supplies an explicit replacement.

Keep the base residual compiler, lines 6602–8678, as construction machinery and a source of inherited proofs. Its opening explicitly says that its degree-eight encoding is not a third final polynomial. Its archived counts, coefficient maximum and old 41-contact architecture are historical, not values to replace with the new endpoint. In particular, do not globally replace the decimal coefficient maximum: it appears both in this archived compiler and in the active quartic theorem.

Replace the active quartic in the existing `sec:quartics`; do not append a second quartic section. Keep exactly one active `thm:quartic`, one active expanded coefficient file specification, and one final proof of that theorem. The old 9625 artifact is not an additional current result in the integrated paper.

## Exact block disposition

| Version 3 lines | Action |
| --- | --- |
| 8679–8731 | Keep the `sec:quartics` and `thm:quartic` labels, but rewrite the theorem, literal artifact specification and source introduction for the selected endpoint. All finite values are pending. |
| 8732–8751 | Rewrite the source introduction. Keep the component formulas for multiplication/inversion if useful. Remove the assertions that the current roots/primaries belong to 2E and that all affine subtraction guards remain. |
| 8752–8909 | Retain the complete H19 theorem and proof, including all qualifications. The new appendix invokes this result rather than reproving it. |
| 8910–9035 | Retain the 37-contact arithmetic and prime-pattern proof with the narrow interface edits below. |
| 9036–9130 | Retain reciprocal-logarithm error and global nonvanishing proofs unchanged. They cover both G9 and G2, including the exact infinite-tail estimate. |
| 9131–9508 | Replace the old 29-full/8-beta specification, old local conclusion, two old contradictions, old source theorem and compressed-primary lemma. Transplant the still-needed scalar/anchor and beta-ratio definitions described below. |
| 9509–9529 | Transplant the exact quadratic G9/G2 evaluator. Adapt the sentence naming its equation consumers to the beta and normalized-Lucas equations in the new source. |
| 9530–9570 | Rewrite the arithmetic/finite boundary and all raw source metadata. Remove the old source ID, two-mode/eight-module description and hashes. |
| 9571–9605 | Retain the generic definition elimination, lift, invertible row operations, shear and full-incidence explanations, but point to the new arithmetic argument. Claim only operations actually present in the final certificate. |
| 9606–9669 | Remove the old norm-inverse, private contact-inverse, and full-root-chart application descriptions unless the final event census proves an application still occurs. They are not a description of the new source charts. |
| 9670–9712 | Retain the parity replacement proof only if that rule occurs in the final certificate. The expected remaining use is the separate height-parity block; take its actual multiplicity from the certificate, never the old 38. |
| 9713–9743 | Remove the root-error/bottom-norm absorption account unless an explicitly audited final event uses it. The private conic and first numerator cannot be treated as the old root-error norm pair. |
| 9744–9830 | Rewrite the complete finite realization, event census, checker descriptions/digests and proof of `thm:quartic`. |

The 13 ranges partition the entire existing quartic section without gaps or overlap. The inventory script checks this.

## Inherited material that must not disappear during replacement

The 37-contact lemma currently begins by requiring `A=[n]Pstar`, and similarly for S,T,Z, at 8914–8916. Its contact/parity/height proof and converse use only the eight rational abscissa coefficients. Restate its setup using the four nontorsion E(K) root points, or directly using eight arbitrary rational coefficients followed by the abscissa-height consequence. Do not keep a 2E restriction as a hidden premise for the enlarged carrier. Keep the exact raw forms, constants, order, fixed-denominator choice, finite exclusions, duplicate-position treatment and same-prime order hypotheses.

The old lemma's sentence at 8953 and last paragraph at 9026–9034 currently finish by supplying the old pole witnesses. Retain the positive contact, square-denominator, local-squareclass and orientation conclusions. State that the new conic and linear-pole completeness lemmas supply the selected source's witnesses. Do not assert that the old seven-witness pole is the new ordinary comparison pole. The scalar pole remains inherited and unchanged.

Extract the usable clauses from 9139–9147: the original equation `beta=X^2+2`; the scalar batch's two coefficients each of `f(J0), f(S), z(S)/z(J0)` with orders `(1,1,1,1,32,32)`; and `c0=3, c_(i+1)=c_i^2` for 25 squarings, with terminal C. C is computed, not inserted as a huge polynomial coefficient. Keep the direct eight abscissa height targets. Discard that paragraph's global proxy equation, old root carrier and old ordinary norm/pole assertions. The new four-witness anchor consumes the same terminal C.

Keep an explicit beta quotient definition after deleting the compressed-primary lemma. For each applicable comparison it is

`Lambda*p_H=G_H`, `B_A=C_A*p_A`, `B_A*Lambda=G_A`.

G nonvanishing gives the required denominator and beta-numerator nonvanishing. This is the algebraic definition of the beta quotient used by `C_A-2beta`. The revision-3 appendix treats this interface as inherited; it must not be lost with lines 9471–9507. For Lucas numerators use the new normalized equations instead, including their permitted global p_s/p_z zero branches.

Retain the G9/G2 circuit at 9509–9529, with the original recurrence defining its a_j already retained at 9041–9045. In particular keep `a6=-418/16575 != 0`, the four-pair high-order circuit, and the one-pair beta circuit. These are exact polynomial identities, not extra approximation hypotheses.

The scalar/anchor derivation at 9301–9316 supplies an inert-prime argument and explains why beta avoids the four branch values. Either retain that argument as a narrowly restated inherited lemma using doubled indices, or attach explicit references to the base scalar proof and new doubled-index derivation. Do not keep the old assertion `S=[s]Pstar` when s denotes the new doubled index. Both indices acquire the same factor two, so the scalar ratio and its integer divisibility survive as proved in the reviewed root note.

## Position and selection of the new material

A readable order within the single quartic section is: literal final specification; inherited H19/contact/reciprocal foundations; revision-3 conventions; three-mode joint chart; private conics/linear pole/four-witness anchor; local and normalized Lucas; general roots and selected targets; selected exact refinements; complete choice order; exact G circuit and source metadata; actual algebraic transformations; final realization and theorem proof.

Import the selected `CONTENT.tex` text, not `APPENDIX.tex`. The standalone wrapper repeats the document class, theorem environments, Q/Z macros, title, author, bibliography and document environment. Only `LogE` needs adding to the existing preamble. Demote imported `section` headings to `subsection` and imported `subsection` headings to `subsubsection`, or use equivalent explicit headings within `sec:quartics`. Preserve the imported label keys, even where their prefix says `sec:`. Keep `subsec:quartic-source` once, at the start of the new source material.

Select branches from the accepted source. The reviewed draft defaults are GeneralRoots, TargetTwo, TangentFusion, SharedSquare and FirstNorm enabled, ScalarFusion disabled. They are not an authorization to publish those options without the matching source. For that selection remove the target-four alternative and scalar-fusion lemma from the integrated current-source exposition. Remove editorial switch comments, 'optional' headings and the standalone draft notice after resolving the selection. Any different accepted source requires matching the actual selection and review.

## Labels and citations

The scan found 20 labels in the old quartic section and 21 in the full optional appendix. There are no collisions between any imported label and any label in the published manuscript, and no duplicate labels in either input. Nine old source labels are retired:

| Retired label | New reference target or treatment |
| --- | --- |
| eq:quartic-selected-parameters | New selected-parameter paragraph; no alias is needed. |
| eq:quartic-mode-partition | lem:quartic-three-mode-coverage |
| lem:quartic-selective-local | Joint chart, doubled-formal comparison, private-conic packing, and target-two lemmas together. |
| lem:quartic-height19-anchor | New doubled indices, four-witness anchor and general-root cutoff derivation. |
| eq:quartic-cutoffs19 | New general-root cutoff display; no old-H alias. |
| lem:quartic-selective-lucas-growth | thm:quartic-selective-arithmetic, retaining lem:o8-lucas as the inherited growth input. |
| lem:quartic-beta-only | thm:quartic-selective-arithmetic |
| thm:quartic-source-arithmetic | thm:quartic-selective-arithmetic for soundness and sec:quartic-composition for completeness. Do not silently rename the new conditional soundness theorem as the old full equivalence theorem. |
| lem:quartic-compressed-primary | lem:quartic-joint-chart and lem:quartic-general-root-charts, plus selected exact-refinement lemmas. |

All references to these nine labels occur inside the old quartic section. After replacing the blocks, the surviving references that need deliberate rewriting are at 9569, 9579, 9814 and 9815. The other six references disappear with their old arguments. `sec:quartics`, `thm:quartic`, `subsec:quartic-source`, `subsec:quartic-reductions`, and the H19/contact/reciprocal labels can remain once each.

The standalone appendix cites two keys absent from the main bibliography. Change `koenigsmann` to the existing `koenigsmann-defining` key while retaining the explicit Definition 4, Observation 5 and proof-of-Proposition-6 facts. Replace the draft's `cite{v3}` with precise internal references to the retained base/inherited sections and `app:sources`, while preserving every qualification in that paragraph. If an archival Version 3 citation is wanted as provenance, add a separately identified historical item; it must not replace the internal proof linkage. Do not append the standalone bibliography or duplicate the Koenigsmann entry.

## Pending metadata and final gates

`SPLICE_INVENTORY.json` stores every old file path and 64-digit hash in the active quartic section and the associated finite-value spans. The essential replacements are total variables N, witnesses N-1, nonzero monomials, final residual count, expanded coefficient bytes, expanded SHA256, exact coefficient maximum, raw source coordinate/residual counts, compressed and uncompressed source SHA256, source ID, source module count, certificate event counts by actual kind, certificate SHA256, verifier SHA256 and source-auditor SHA256. Read these from the same accepted endpoint and its complete source/audit chain. The old values are not defaults.

Regenerate the exact coefficient-order and variable-map description if the new exporter differs. Verify whether every weight is one before retaining that statement. Use the selected packaged receipt path; do not invent a package-root verification file. Update the displayed package/verifier links and the main TeX/PDF release basename only after the release slug is fixed. All cross-terms must be included in the final maximum, not just an isolated replacement calculation.

The source/dependency inventories must be rebased to the final TeX bytes and selected imported labels. Preserve unchanged historical source IDs and qualifications; replace the nine retired source-application anchors with the new argument's actual dependencies. Add the mixed-mode denominator clarification to the inherited root/target proof linkage. Record source replacements separately from exact algebraic projection maps. The statement 'base collection contains 83 sources' at 9852 is an inherited base count, not the size of the new combined inventory.

Before publication, compare all active numeric/hash references against the one accepted artifact; scan for duplicate/undefined labels and missing citations; ensure no old `29 full`, `8 modules`, affine-difference guard, global-theta, or proxy-equation assertion describes the new source; verify the selected conditional branches and all still-used algebraic rules; build and visually inspect the complete PDF; and rebind the proof/application inventory. No public file has been modified by this plan.
