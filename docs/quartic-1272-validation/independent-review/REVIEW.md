# Independent Version 5 review

The new 1272-variable section, arithmetic bridges, and simultaneous-prime appendix pass this source-level review within the arithmetic and external-source interfaces they explicitly identify. The exact coefficient check also passes. The review does not reprove every inherited arithmetic theorem or claim that every external input has a verified final journal version.

The machine-readable receipts `package-check.json` and `release-check.json` bind the checks to exact files. Final read-only inventory validation also passed, with every checked input unchanged during the run. The final manuscript SHA-256 is `16033e0471df605093b28210a9f81718c2486b147016ec8afc75d166dff0b90f`; the authored inventory input SHA-256 is `695769c38917efa35b6256132cd8b77807d6384ab6d27c38f250ff8947ae6c10`. `inventory-validation.json` records all resulting inventory pins.

## Reviewed mathematics

The accepted new section is `manuscript/new1272.tex`, SHA-256 `506675ede05bb3d369d9882945958c86d2d39c8fbe4d6e1e393c6a4e17f00000`. The accepted bridges are `bridge-review/arithmetic_bridges.tex`, SHA-256 `94696c3d3113c6ff23b8ff3039a17447424151d49f5ecbf1f178304aaf2d5544`. The accepted Sun appendix is `sun-proof/sun_appendix.tex`, SHA-256 `620e2e5652048c827efd8a1d9dae78462679e65992beeb20c3f089b3115fb77b`.

The review checked the point and quotient domains, reciprocal-logarithm precision at both split and inert unramified places, the sixteen field tests, the scalar norm tree, coordinate detectors, preparation quotient, and three-witness anchor. The section uses the original exponent-24 five-contact height bound and original large anchor scale. It does not substitute Version 4's exponent-19 estimate or its smaller constants.

The completeness argument chooses its fixed coefficients and real bounds before the simultaneous prime pattern, then imposes the compatible congruences for the comparison index. The added CM lemma identifies the unordered elliptic group cardinalities with the adjacent Gaussian norms. These cardinalities are used as annihilators. Exact orders of the selected reduced point are not required. The two-prime-form argument establishes the needed denominator is a unit at the selected prime.

The three bridges were checked against the inherited interfaces. They cover the order-32 scalar construction, the preparation-zero case at 17, and a real bound uniform over later arithmetic progressions. Eight full foundational blocks remain text-identical to the retained Version 4 source. Text identity establishes retention of the reviewed interface; it is not a fresh proof of all those blocks.

The Sun appendix review covered the local quadratic counts, primitive-point estimate, medium and large obstruction sieves, fixed-field Artin transference, ray-group normalization, local density lower bound, and final order of limits. The final diagonal first controls the obstruction error for fixed positive values of the shrinking parameter, then applies the polynomial asymptotic to the resulting piecewise choice of the progression length. The definition of that length is explicit.

The exact Frei--Tinkova input is the unconditional Artin-symbol linear-forms result in arXiv 2408.17441v3, Theorem 1.4. It is distinct from the conditional primitive-root theorem. Its author-reported acceptance by Mathematika is not a verified final journal text. The appendix and inventory retain this qualification. The earlier restrictions on Pan, Yuan, the prime-pattern correction sources, and the inherited restricted converse also remain applicable.

The appendix's added norm-exponent repair was independently checked against Frei--Tinkova Lemmas 9.1 and 9.3 and Dodos--Kanellopoulos Theorem 5.1. Requesting D = 4^(u+1) supplies the required U^(2u+2) majorant norm for a target U^(u+1) norm, with u >= 1. See `FT-local-repair.md` for the complete local argument. This repairs that invocation only. Dodos--Kanellopoulos was checked in arXiv v4; the final typeset statement was not compared.

## Finite construction and package

`check_package.py` imports none of the package's builder, compiler, or checkers. It independently reads all 1229 final residuals, reconstructs the coordinate map, performs exact rational convolution of every squared residual, and compares every encoded coefficient with the complete table. It verifies 1272 active coordinates, degree four, primitive integer content one, and 48001 nonzero coordinate monomials. The coefficient of the input's fourth power is one.

There are 47993 coefficients independent of the fixed integer S, seven coefficients proportional to S, and one coefficient 64*S^2. The largest S-independent coefficient has 5339 bits; the largest linear multiplier is 768. Elementary exponent comparisons establish that 64*S^2 dominates at S = 3^(2^27), so the exact coefficient height is 64*3^(2^28). The computation never materializes S or a giant coefficient.

The polynomial's SHA-256 is `02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586`. The top-level table is an exact-byte alias of the translated compiler table. All 78 manifest entries were independently checked against file inventory, byte lengths, and hashes. After the serialization correction below, the accepted package manifest is `aa7f04c54e8b778a419a1be8d24e0b3a9a8540c50202d41815864a156d6985c6`.

The earlier independent source evaluator tested the actual generated IR against manuscript expressions, including rational and finite-field checks. Those sampled identities supplement source review and exact certificate checks. They do not prove global arithmetic implications or establish the existence of rational witnesses. The anchor identity is exact: the translated residual equals sixteen times the original residual after the invertible affine substitution. The two normalized sums of squares are not asserted to be literally equal after substitution.

The portable replay scripts were inspected for source paths, dependency requirements, isolation, coefficient binding, and advertised checks. The package author separately ran fresh-path complete replays. Those replay receipts are implementation evidence from that lane; they are not relabeled as this reviewer's independent convolution.

## Serialization correction after Linux CI

Linux CI passed the computational checks but exposed platform-dependent line endings in regenerated JSON. The repair uses explicit UTF-8 and LF for generated metadata, residuals, certificates, and coordinate maps. The direct and translated polynomial tables and top-level alias use explicit CRLF to preserve their published bytes. Integrity checks enforce this policy in addition to the existing byte hashes. No exact comparison was removed or replaced by parsed-JSON comparison.

The independent patch check compares the new package with Git commit `81de7e45d60d458414ea0f96eb0f68ad8981a3a3` and the previously accepted manifest `37a5d9d0e4d1d9f51562a1ba4a004827ad5bc7c0fbdf3a7d74f031e9ddc933e3`. Seven mathematical Python modules have identical syntax trees after removing only explicit UTF-8 and newline settings. All thirteen core JSON artifacts are identical as parsed data. Both polynomial tables, their top-level alias, and the builder and independent checker programs retain their exact bytes. Other changed JSON fields are timestamps, runtime measurements, artifact hashes, and provenance. The full coefficient convolution and manifest checks passed again. `serialization-patch-check.json` records the comparisons.

## Findings and disposition

- The main polynomial statement now explicitly quantifies every rational input.
- The CM group-cardinality bridge and denominator-unit argument are explicit. This closes the ambiguous earlier reference to reduction orders.
- The Sun diagonal explicitly defines the progression length after choosing its piecewise shrinking parameter. Malformed sum text and row breaks were corrected.
- The imported relative inverse-theorem invocation now includes the correct higher majorant norm and an explicit local repair. Its scope does not claim closure of the full external proof.
- The replay command now rejects output directories inside the shipped package before creating files. This prevents a successful replay from invalidating the package's own inventory.
- The coefficient-table path now exists as the promised exact-byte alias.

No unresolved mathematical objection was found in the reviewed additions under their stated inputs. No Lean verification, fresh proof of every inherited result, all-published-only proof, recovery of the unavailable Brox 1315-variable table, or PDF layout approval is asserted by this review.
