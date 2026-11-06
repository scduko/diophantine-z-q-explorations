# Independent review: local-Lucas plus conic-pole integration

Date: 2026-11-06. Verdict: PASS for the frozen implementation correspondence and composition contract. Final generated-source binding, coefficient counts and full replay remain separate obligations.

The reviewed packet is `parity/sub5000/conic-pole-local-lucas`, manifest SHA-256 `d6114c89d97ab3ee5f5e2919e59859b0cc2d52f1d8edac40a547002a68043553`. I checked all 97 file hashes and sizes and the exact file set. The 13 external-input pins remain subject to the runner's normal verification at execution; no remote job was launched for this review.

The combination contract is `LOCAL_LUCAS_CONIC_POLE_CONTRACT_ADDON.json`, SHA-256 `cd7e4039c533eed79afd75fea9ba6abb53f10b7a26ea990b195b9f2c15badd8b`, copied exactly as the packet's `CONIC_POLE_CONTRACT.json`. It inherits the original pole contract `44bcef6a37f57a847f963313b146614b56ecf3fdb101e5443c2c65321494e4a4` and the actual local-Lucas source contract `13ebcdd31363e8d482a8daac988da75ac314d66a1d989926e39bdf01d4418048`.

## Exact implementation delta

The parent local-Lucas manifest is `12d818714b70680eff617295008d685ebec8c81984d0402eb6ea79840ef330ed`. Its core auditor, local-Lucas module auditor, conic batch auditor, anchor checker, local-Lucas emitter, conic emitter, generic mutations and proxy-removal tests are byte-identical. In particular, `audit_local_lucas.py` remains `c08ee3db7b7711ccc32d942a615a893d4cb14b03a58a4eb0a3965430f5b89543` and `check_lucas_batch.py` remains `446ff0fb520d3922d1a3c96455dd4fade07206dbed5357dcc38700ce6eb2e0ce`.

The new pole kernel, literal checker and restoration wrapper differ from the previously reviewed conic-pole packet only by the two literal registry substitutions q_conic15 to q_conic13 and q_conic12 to q_conic10. I verified that byte transformation independently. No pole equation, local slot, zero branch, restoration row or ownership condition changed.

The builder installs the pole hook after the unchanged local-Lucas, conic and anchor hooks. The outer checker adds the one pole module and exact 37 new/1 old parity-instance counts, then uses the unchanged local-Lucas module checker with the restoration callback. It reconstructs each original conic batch before running the full frozen batch specification, then checks the entire proposed tail delta. It separately checks the literal new pole and exact caller sets. The source family is `H19-root37-joint-chart-local-lucas-conic-pole-anchor4-v1`, with required prefix `joint-chart-local-lucas-conic-pole-anchor4-k40-q12-a25-h19-s32-`.

The outer source checker is `3be3516aef7e22d2d07bfd3e3ca138e9a5e71a23df7e386cad97342e413c1034`. Its additional `PARENT_SOURCE_PINS.json`, SHA-256 `e34affe14c54475f606bcc8f923a2c2a9adda71d5710ca1db005fc50fd1b425d`, pins the actual already-reviewed parent root, all three comparisons, anchor, scalar-height, old parity and shared constants. I checked all eight pins against `local-lucas-result/source`. The outer checker enforces these exact bytes before accepting a new source. Thus there is no hidden normalization, proxy, height-target or field-coefficient change.

The adapter retains 58/28/47 comparison arities, 28/16/23 legacy arities, 377 fields, 37 private conics and 145 primary/difference pairs. It requires the exact field order lists and the new pole metadata, binds the new source name to its actual residual hash, and retains the complete source audit and construction map. The locator checks each module-local pole call `[0, conic_private.theta, norm_root]` and matches all instantiated pole triples against the batches. Only the old scalar parity instance is returned to the old parity-reduction locator; new poles are excluded. The actual generated source must still exhibit exactly six root chart locators. The isolated locator fixture has zero such charts by construction and is not evidence that a real source may omit them.

The bounded runner and inner algebraic pipeline are byte-identical to those of the preceding reviewed pole packet. Their Linux limits, process-group cleanup and failure propagation remain in force. Every produced algebraic stage is still verified against the named source. This review does not replace execution of those stages.

## Composition argument

The parent local-Lucas proof needs exactly E=F(C_s,C_t,C_z), with an order40 test, at the 29 Lucas-bearing positions. The parent comparison bytes pin that unnormalized E, the same logarithmic quotients and every formal/alternate test. Before choosing a private conic theta, the complete witness construction assigns all elliptic points, G/ratio values and these polynomial E coefficients. Therefore the field coefficients are independent of that theta.

For fixed coefficients, changing the finite field list from 15/6/12 to 13/6/10 changes only the number of packed leaves. Every packed leaf remains polynomial in theta with fixed rational denominators, as does the complete upper norm root W(theta). The constant-left tree remains positive over the reals for complete r>0. Thus the fixed-U pole proof's simultaneous approximation at the selected split prime and real/2/3/17 places applies without another arithmetic hypothesis. Its reverse map supplies the same original pole predicate at rW^2 in soundness, including W=0. The private-conic recovery gives the exact orders needed by the local-Lucas proof. No normalized F/C_s^2 identity or extra prime exclusion is used in this combination.

Accordingly H19, root37, high40, beta12, anchor25, scalar32, all retained height targets, the half-index argument and both global contradictions are unchanged. The original literature interfaces and source-version qualifications are inherited; finite module checks do not prove those inputs.

## Tests and remaining boundary

I independently reran the three isolated batch/pole positives with 46 malformed cases and the locator suite with 70 malformed cases. Both passed. I also verified the exact registry-only helper delta, actual-parent pins, frozen parent helpers and runner equivalence. The packet records further 22 pole mutations/20 rational fixtures, contract consistency and syntax checks; these were not rerun for this review.

The 165-case parent source suite is retained: its individual mutation functions are unchanged, while its positive path uses the new wrapper and its batch tests receive the restored old batch. Separate pole mutations cover the new tail. Full generation and that emitted-source suite have not yet been run in this review. A successful run must bind the actual root/comparison bytes and all 37 flattened triples, then complete named-source replay and expansion before any new polynomial count is accepted. No integration blocker was found.
