# Independent frozen normalized-Lucas/conic-pole integration review

Date: 2026-11-06. Verdict: PASS for the exact frozen implementation and arithmetic contract correspondence. This is not an emitted-source or endpoint acceptance.

Packet: `source-pipeline/sub5000/normalized-conic-pole`. Manifest SHA-256: `07ded5a9a1fb0dcdd2e0f1e0930268841fcdc79bf4b1335189a952fef024963b`. I checked all103 file hashes/sizes and the exact file set. The13 external input records agree exactly with the frozen normalized parent manifest; their execution-time files remain subject to the runner's pin checks.

The composition proof and contract are respectively `f10ca2fe7efc52bdccf2b67adf3277e8a26dd79c73dd339a89ad9a38fe6bc258` and `0ad8288dd3a44daa524e753dfba04b0b788de46d84bfa63d3f34a71d3272dd10`. My independent mathematical review is `NORMALIZED_POLE_COMPOSITION_REVIEW.md`, SHA-256 `81cd82e196c38415844b059867deb24c5f747b2dc34e4bc33d95eead3619ce77`. No mathematical assumption was added after that review.

## Source pins and exact delta

The normalized parent is the actual inspected source `joint-chart-normalized-lucas-conic-anchor4-k40-q12-a25-h19-s32-306c44519001`, with compressed SHA-256 `be7a7508e75a67d7570c6f974caca7af7f30004bd0a34c2dc4ac3bd17d75a2bb`. Its final independent binding is `NORMALIZED_5512_SOURCE_REVIEW.md`, SHA-256 `06bbf6d4310b9c34610035528ad9428b5f13aadfd7ebf77d7edd6db4e129d8fb`.

The merged packet retains the six original direct pins for the root, beta comparator, anchor, scalar-height, old parity and shared constants. I compared these with the actual parent files. Only the three conic batch byte pins are superseded, and their original hashes are retained as reference values. The checker enforces this exact six/three partition against the frozen composition contract. It cannot remove the whole parent-pin requirement or substitute an unnormalized comparison source.

`NORMALIZED_PARENT_PINS.json`, SHA-256 `d94bf88c98b5c3e5110ed9ab58c587ba83a7cda17b736f1a0d9d226e0b415e59`, additionally binds the actual normalized source ID, source digest, entry, audit and construction-map hashes, and both full/Lucas comparator files. I checked every such value against the actual normalized artifact. The builder and outer source checker enforce both comparator hashes; the adapter includes the pin record among its required inspected source files. Thus all eight retained modules/data files have exact parent bindings, and the two normalized comparators are not merely inferred from aggregate metadata.

The only new module is the previously reviewed literal q_conicpole. The only changed batch equations are the final two argument gates, replaced by the exact call `[raw r, own private theta, own norm root W]`. The frozen pole kernel, literal checker and restoration wrapper are the reviewed13/6/10 versions. Each proposed batch is restored to its full old form and checked by the complete old conic specification; the whole actual batch then has to equal the permitted tail delta. The actual pole module and caller sets are checked separately. No restored view is used in place of checking actual new calls or rows.

## Comparator and interface checks

The core, normalized module auditor, conic batch auditor, anchor checker, normalized/local/conic emitters and inherited normalized mutation functions are byte-identical to the frozen normalized parent. I read the normalized auditor's changes from the earlier reviewed local-Lucas auditor: it reconstructs all eight field equations with the correct s,t,z point indices, keeps the common G equation and full-mode beta block, and checks the exact E=F/C_s^2 metadata and field position. It also requires `global_numerator_p_nonzero=false`, forbids obsolete unnormalized evaluation metadata and preserves all primary formal and alternate tests.

The merged source keeps arities58/28/47, legacy prefixes28/16/23,377 fields,145 primary/difference pairs and37 private conics. It retains H19/high40/beta12/anchor25/scalar32 and all root height targets. The locator checks the exact old ignored theta/error slots, each new local pole triple and the multiset of instantiated triples. Full flattening still checks all module equations, calls and fresh allocations. There is exactly one old scalar-height parity occurrence and37 new ordinary poles; the old algebraic parity rule targets only the former.

The main code hashes are:

- Builder: `4644b67baf5882d96d2ec4d926439288bd3ff16f1ecd81e5ce7a523dc7efc2b1`.
- Outer checker: `f793ae4be637c16436df06368f67b6708b2c3eca8e2b7fdc1b7fe5e5902aa545`.
- Adapter: `efe87f2b79a5d28a26d63707a671f31273f94244c3a6ec2ed1f0c4852060cb29`.
- Locator: `c1d34bba30f7533f38feec49ab671389305bb4b312f3a736cab29f96ba8ff718`.
- Combined mutation harness: `09e30592c0abb8d777f331fa9888bfc279b93ec63de94d0d1819fd6c1d1f445c`.

## Arithmetic conjunction and execution boundary

The combined witness order is explicit: first choose fixed root indices and a contact pattern avoiding the nonzero integer s; then common J, private points and normalized ratio coefficients; only then each private conic and its pole witnesses. The normalized denominator C_s is a unit at each assigned prime in completeness and is fixed before theta. Consequently W(theta) remains polynomial and the same real/2/3/17 smallness neighborhoods are compatible with the selected-prime approximation. In soundness C_s need only be integral: multiply E by C_s^2. Global zero p_s/p_z branches and the pole W=0 branch keep their separate valid proofs. No branch is removed by an extra inverse in the merged interface.

I independently ran the frozen75 locator mutations and46 pole-integration mutations; both passed. The combined source harness first accepts the actual eleven-module system, then runs the208 normalized mutation cases on the unchanged modules and explicit restored batch views. The separate46 pole tests cover actual caller/tail changes. I read this harness; its full emitted-source execution remains a remote-run obligation. Resource-abort propagation and full stage replay remain required and are not replaced by mutation counts.

No integration blocker was found. Final acceptance of a merged polynomial still requires inspecting its generated source, exact private ownership and field coefficients, source determinism and full named-source replay/expansion. No merged count is asserted here, and no inherited arithmetic theorem application is proved by this finite integration review.
