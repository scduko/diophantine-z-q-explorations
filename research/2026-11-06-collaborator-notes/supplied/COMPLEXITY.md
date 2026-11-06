# Complexity ledger and comparison conventions

All witness counts below exclude the free input X. Upper-bound rows are conditional on the arithmetic assumptions in their own source. Results from different assumption packages and different representation formats must not be treated as directly interchangeable.

## Principal constructions

| Construction | Rational witnesses | Total degree | Representation and status | Main locator |
|---|---:|---:|---|---|
| Early finite-certificate note | <100,000,000 | No simultaneous optimized degree claim in this row | Existence/coefficient-extraction procedure; not emitted as a full polynomial. | `02_proof_development/finite-existential-integers.pdf` |
| Reduced arity note | <=11,029 | Separate degree-four conversion, not a simultaneous bound | 16,316 before finite-algebra compression; existence construction. | `02_proof_development/reduced-existential-arity.pdf` |
| Original focused construction | 17,030,326,787,289 | 4 | Fully specified modular circuit by finite composition/repetition; not fully expanded. | `05_original_archives/focused_diophantine_review.zip` |
| Improved enormous quartic circuit | 197,308,848,020 | 4 | Instantiated modular circuit; old high-complexity route retained. | `05_original_archives/quartic-circuit-improved-source.zip` |
| Improved universal-system bound | <=64,419,418 | 4 | Separate bound with three unevaluated universal program parameters; not the emitted circuit in the preceding row. | Same archive, `work/improved/universal_bound.json` |
| Supplied Pell construction | 1,515,857 | 4 | Full expansion and circuit records retained in the large original archive. | `05_original_archives/pell-contact-major-improvement.zip` |
| Shared-contact quartic | 25,794 | 4 | 25,928 quadratic residuals; 276,844 collected monomials; fully expanded. | `06_working_packages/quartic-shared-contact/pell-shared-contact-source/` |
| Balanced formula, degree 25 | 16,024 | 25 | Factored polynomial graph; historical alternative. | `05_original_archives/balanced-natural-formula-source.zip` |
| Balanced formula, degree 45 | 11,725 | 45 | Factored polynomial graph; historical alternative. | Same archive |
| Balanced formula, degree 75 | 9,606 | 75 | Factored polynomial graph; historical alternative. | Same archive |
| Primary degree-eight construction | 15,671 | 8 | 15,107 squared residuals; 129,497 collected monomials; fully expanded. | `05_original_archives/short-polynomial-source.zip` and compositional synthesis |
| Degree-eight elimination experiment | 14,176 | 8 | 125,413 monomials; increases the chosen size measures, so not selected as the main short-description result. | Short-polynomial archive, experiment/audit records |
| Supplied compact compositional construction | 3,186 | <=5,044,774 | Single-polynomial count, including the final guard witness; attribution/source retained in the package. | `05_original_archives/compositional-formula-source-and-audit.zip` |
| Merged compositional polynomial | 1,066 | <=227,772 | Recorded graph; fixed C = 3^(2^24) specified by composition; no full expansion. | `06_working_packages/compositional-synthesis/compositional-synthesis/merged/` |
| Merged version with constant chain | 1,090 | See its own structural count | 24 extra witnesses replace the composed constant with quadratic equations. | Same package, `merged/final/chain-factored-5-selector-sphere/` |
| Preliminary finite-algebra compression | <=557 | Not bounded in the chat observation | Historical uncompiled observation; no separate polynomial record recovered. | `CHRONOLOGY.md` |
| Shared-witness practical version | 100 | <=596,676 | Recorded JSON/binary circuit; no full expansion. | `06_working_packages/shared-witness/shared-witness-polynomials/polynomial-100/` |
| Shared-witness smaller-variable version | 82 | <=7,190,904 | Recorded JSON/binary circuit; no full expansion. | Same package, `polynomial-82/` |
| Local finite-choice version | <=59 | Not emitted/bounded here | Theoretical finite formula using local quartics; no compiled output. | Shared article, final paragraphs of `article/shared-definition.tex` |
| Global finite-algebra version | <=40 | Not emitted/bounded here | Conditional theorem; numerical constants and final polynomial not generated. | Shared article, Theorem `sd:forty` |

The short-anchor archive gives additional formula-level counts and ranks. Some count rational equations and guards before conversion to one polynomial. Use its `single_polynomial_witnesses` field when making a single-equation comparison; do not mix it with the uncompiled formula's variable count.

## Comparable circuit and recipe sizes

These three records use the same canonical lossless circuit encoding. Degree values are structural upper bounds.

| Record | Witnesses | Degree bound | Graph nodes | Binary circuit bytes | xz circuit bytes | ASCII recipe bytes/characters |
|---|---:|---:|---:|---:|---:|---:|
| Previous merged | 1,066 | 227,772 | 127,642 | 802,275 | 327,632 | 6,467 |
| Shared 100 | 100 | 596,676 | 7,024 | 33,971 | 18,412 | 5,410 |
| Shared 82 | 82 | 7,190,904 | 9,773 | 47,554 | 26,012 | 5,337 |

For the ASCII recipes, one character is one byte, including whitespace and the final newline. Thus 33,971 bytes and 5,410 characters are comparable as storage lengths: the circuit record is about 6.28 times as large. They are two different descriptions of the same polynomial. The circuit records operations and node references; the recipe uses definitions, indexed expressions, and composition.

The approximately 23.6-fold improvement from 802,275 to 33,971 concerns the circuit representation. The recipe improvement from 6,467 to 5,410 is much smaller and includes editorial shortening. No global minimality or universal coding-length record is claimed.

## Other representation sizes that should not be conflated

- The 5,719-character block text describes the degree-eight polynomial, not either shared-witness polynomial. It is an exact compositional presentation of the fully expanded record.
- The 5,381-byte `.pyz` is an executable compressed capsule including decoder, data, loader, and archive overhead. Python and its standard library are an assumed platform.
- The degree-eight package also records a 3,124-byte compressed recipe and a 4,283-byte decoder, for a combined 7,407-byte description under that convention.
- A fully expanded monomial list can be much larger than either the recipe or the arithmetic graph. The numerical value of C = 3^(2^24) is enormous even though its composition recipe is short.
- Fewer variables can raise degree, coefficient size, circuit size, or description length. This is why the 100-variable circuit can be preferable to the 82-variable circuit for short description, and why the 59-variable formula may be preferable to global 40-variable elimination.

## Lower bounds recorded in the latest note

Let r be the witness count, d total degree, and d_y joint degree in the witnesses.

| Class/measure | Necessary bound or obstruction |
|---|---|
| Arbitrary single polynomial | r >= 2 and d >= 4 |
| Joint witness degree | d_y >= 3 |
| Two quadratic equations with any linear equations | Insufficient to define all integers |
| Quartic defining polynomial | Absolutely irreducible |
| Globally nonnegative polynomial, r = 2 | d >= 8 |
| Globally nonnegative polynomial, r = 3 | d >= 6 |
| Globally nonnegative polynomial, d = 4 | r >= 4 |
| Globally nonnegative polynomial | d + 2r >= 12, together with r >= 2, d >= 4 |
| General monomial support | Affine dimension >= 3; at least 4 monomials |
| Nonnegative support of size s and affine dimension k | s >= k + 5; at least 8 monomials |
| Division-free circuit, nonconstant multiplication gates | At least 3 in general; at least 4 with two witnesses |

The complete proof hypotheses, including restrictions on circuit operations and the role of nonnegativity, are in the lower-bound note. The note does not establish r >= 3 in general, a simultaneous degree-four/two-witness construction, or a significant unconditional minimum recipe length. The lower-bound proofs were not all re-audited during this handoff.
