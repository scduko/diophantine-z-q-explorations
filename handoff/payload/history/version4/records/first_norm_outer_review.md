# First-norm integration review

2026-11-06. **PASS for the exact helper and pre-run composed-source integration.** New emitted-source and polynomial acceptance are still required.

The packet `source-pipeline/sub5000/target2-tangent-first-norm/` uses family `H19-root37-target2-tangent-first-norm-normalized-linear-pole-v1`. Its joint contract is `73e17ecc19a797ce442412549931ff11e43f42ebff9c48e1b2c636ff2d839a8c`. It composes the already reviewed target2, four tangents and shared-square changes, then changes only the first packed field/norm equations in the three batch modules.

| File | SHA256 |
|---|---|
| Builder | `2f973408d8f022fdf178606bc42a6ce41ec68aa0272b0e7186df2e5fff00bd61` |
| Full source checker | `58bf1da4007247bc4558eacce6bdbbc83d2394ac2a47f128390f20f26567d50a` |
| Composed module checker | `50add2b9cd294e86f91c45cc373b4433807a464a4a4cb7c8934688d0a623c281` |
| First-norm producer | `badaa92471df68d9250f77d8584fee0eecafd8641d3873ab0f8babbf0d1d7438` |
| Independent first-norm checker | `5e13e16621f5de043a5bb63d069f91fbab7b6284e19c4f077b093746efa2a2a5` |

The independent arithmetic review is `FIRST_NORM_ARITHMETIC_REVIEW.md`, SHA `90a8c92390d48a3ac5ceef6328b7451a3ffc67a78090537bc24294cdce29824c`. It proves that replacing the first virtual leaf T/r^2 by T/r preserves all local order1 conclusions and integer completeness, then proves the exact conic-dependent fusion. The packet explicitly binds `MIXED_MODE_DENOMINATOR_CLARIFICATION.md`, SHA `2a1eb8ed9a7175995afa665a08035728c1714b5fa30e1ba52030b6adf7b8ba34`; no uniform order40 denominator assertion for beta-only witnesses is used.

I read the producer and independent checker. The producer selects field index0, role H.f, order1, immediately after literal1; requires its only two row uses and no call use; replaces those rows by `T=2AY-A^2+2B^2` and `rN-r-T^2=0`; and retypes both field and tree records explicitly. It preserves the original r^2 power coordinate, N, all higher nodes, every other field and call, and all root/comparison modules. The checker imports no producer. It independently checks the two rows, scalar types, coordinate ranges and distinctness, metadata, exact first tree position, unique labels and numerator incidence. It reconstructs the old specification and calls the required complete parent checker. Boolean callbacks are rejected; resource aborts remain separate.

The full outer callback first reverses this specification delta, then uses the previously reviewed shared-square/tangent/target2 chain and independently rechecks all normalized-ten parent module semantics. This catches tampering with the conic, original power, H.f input channel, field order, higher tree, root calls, or unchanged scalar-height and anchor modules. The exact r!=0 premise is guaranteed by the retained rational conic; no isolated r=0 equivalence is asserted. Restoration is a source-specification check, not an arbitrary witness map back across the arithmetic denominator change.

The builder applies this helper after shared-square and before writing or flattening. The full checker binds the new proof, first-norm contract and mixed-mode clarification alongside the inherited contracts. The locator represents the first field by `norm=null`, a separate numerator, virtual denominator exponent1 and its first node; it retains the other 340 norm fields. This prevents interpreting the numerator as the former divided norm. The shared common-f(J) field remains independently typed and unchanged. The fused-node label is not an acyclic definition dividing by a rational variable. Generic fresh lifting and exact replay remain the final safeguards for the emitted row system.

The actual-source test first accepts the new full source, applies 87 first-norm mutations to it, and separately checks resource and callback handling. It then explicitly restores the parent specification for the inherited 109 shared/root and twelve tangent mutations. The report distinguishes those test scopes. It does not describe restored-parent mutations as additional tests of the new numerator equation.

I independently ran the 87-case module test against an actual accepted target2 source dictionary: all semantic mutations were rejected, four resource aborts propagated and both invalid Boolean callback forms were rejected. I also ran the complete current packet composition from its actual normalized-ten parent through target2, tangent, shared-square and first-norm, then through the complete outer checker. It passed; fresh scalar/root/shared-row mutations were rejected. The root remains 212 local coordinates and 197 rows. There was no full local source generation, flattening, expansion or replay.

Execution records are `FIRST_NORM_MODULE_CHECK.json` and `FIRST_NORM_OUTER_CHECK.json`; the latter was produced by `check_first_norm_outer.py`. All source coordinate/row counts are unchanged by this last helper. The proposed 37-variable lift improvement remains a forecast until an emitted candidate is checked. No pre-run arithmetic, helper or composed-checker blocker was found.

Final freeze: manifest `7654b06f450db87a3181dd5e16fe23949cb4e57d22751aef3681fed80a1fcf26`. I verified the exact file set and all 182 packet file sizes and SHA256 hashes, and all 13 external pins against `work/private-degree8-20261105/repository`. There are no unlisted files. The reviewed code is unchanged. Charts' separate locator review is bound as `96ffda2050e46b2b62f540ea107d31c9c92725857a8b15d82c0cb6ce1c714c24`. This closes the pre-run packet binding, not the still-required emitted-source and polynomial checks.
