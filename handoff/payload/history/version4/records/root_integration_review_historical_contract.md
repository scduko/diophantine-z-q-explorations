# Independent root-postprocessor integration review

Date: 2026-11-06. PASS for the reviewed postprocessor's arithmetic interfaces and bounded module delta. This is separate from Charts' independent literal checker and from acceptance of a complete new source.

Bindings:

| File | SHA-256 |
|---|---|
| `precision/sub5000/root-doubled-indices/root_rewrite.py` | `5a9d82fdb68db591a275c67b2c555735e1376a6a86da21221d76976abd68d479` |
| `UNIFIED_SOURCE_CONTRACT.json` | `ab4e98b768eb54b3bc7f4932ce34b2230363f0c8bdacd9bc1cbf2d5db33c686f` |
| `EMITTER_API.md` | `13e144e262607b67b1e5b6b80c934c3ba2bd8d5e31f45c9d5d73d7e5336d7289` |

The mathematical bindings remain `HALF_GENERATOR_ROOT_REVIEW.md` and `HALF_GENERATOR_FIXED_TARGET_ADDENDUM.md`. The unified contract correctly retains their changed carrier, fixed R, beta factor two, H_eff=5H19 and unchanged scalar/anchor hypotheses. The extra constant-accounting figures in the author contract are explicitly conditional reference figures; this review does not accept a whole-polynomial bound from them.

## Input pins and exact retained data

The helper pins the complete original root and three comparator objects to the already reviewed normalized-source bytes. It also rejects any unexpected root metadata key. It does not choose a full parent or validate unrelated modules, and its API correctly says so. The outer source checker must pin those other modules and the selected normalized-ten parent independently.

I ran the helper on the actual small parent module objects, without generating or flattening a full source. Independently deriving the deletion sets from the original role labels gives 90 removed coordinates and 102 removed rows. Four new k coordinates and 16 new rows result in root locals 258 and rows 243. This is the stated source delta of minus86, not a final quartic saving.

My bounded integration check compared all 223 retained nonbinding root rows under the exact deletion reindexing, all 39 calls, every original point-coordinate and joint-target metadata pair, all five target records, the scalar and anchor parameters, and the historical proxy-removal record. They agree. Its receipt is `ROOT_REWRITE_INTEGRATION_CHECK.json`. The author test also passed its 12 parent-pin rejection cases and output-index checks; that result is separately recorded in `ROOT_REWRITE_AUTHOR_TEST.json`.

The deleted old membership coordinates have no retained residual or call use. The code checks this before reindexing. Its explicit live metadata paths cover the ID-bearing fields in this exact pinned root: proxy_indices, point_coordinates, joint_chart_targets and old jacobi_targets. It leaves numerical parameters and the explicitly historical lucas_proxy_removal record unchanged. New chart metadata uses live remapped IDs, while general_root_rewrite records original IDs with an explicit historical scope.

## Root charts and fixed target

The retained first-doubling square pairs are checked against the actual corresponding x coordinates. Their tangent inverse rows remain among the byte-preserved rows. Thus the new equations y^2-xq+Dx=0 have the nonzero gate used by the reviewed chart proof. S alone keeps the old xf=1 and yz+x=0 rows. Both auxiliary roots keep f,z and receive the exact k=fz, f=z^2-Dk^2 equations. Their old scalar/common z inverses are retained. No old membership condition is silently inferred for these general-E points.

The removed fixed-base gates are the two old constant doublings and obsolete fixed ordinate. The four replacement binding rows agree exactly with the independently checked reduced rational x and q coefficients of 4R. The original fixed-target reciprocal and joint coefficient rows are retained under the same reindexing, so q^2=x-DF follows from the fixed values and xF=1. The other four targets remain the actual quadruples of the unchanged variable x,y root outputs.

The first target metadata is honestly changed to fixed_4R with x,p,f pairs and no ordinate. The remaining records have kind quadruple and retain their x,y,p,f values. The notation p here is the target ratio q=y/x; no primary-index variable or residue prime is being substituted.

## Beta, scalar and index conventions

In each beta-bearing comparator the helper identifies the unique real coefficient row for C_A-beta and changes only the coefficient of its free beta input from one to two. I checked that every other term, both conic field input lists, every call, all Lucas-only residuals, and every scalar/anchor module remain unchanged. The imaginary beta coefficient remains the original ratio's imaginary component. This implements C_A-2beta exactly.

The root scalar rule remains beta=X^2+2, its raw polynomial is untouched, and its six orders remain 1,1,1,1,32,32. The anchor remains the full two-place condition. H19 itself is unchanged; the new root metadata records effective multiplier five. The old private_index_group string describes the coefficient of P* modulo torsion, which can be half-integral. It must not be confused with the new integer doubled root index recorded by root_index_semantics. The proof compares doubled private indices and therefore recovers the integer root index against base R.

## Required outer integration

- Pin the completed parent source and every unaffected module before applying the helper. The four embedded module pins alone are not whole-source acceptance.
- Rebuild the header and flattening map from the returned modules. The current source chart must be general_E_mixed, with chart10 retained only as historical baseline information. Changing the builder's final header value must occur after exact old baseline regeneration.
- Require zero old root-chart locators and do not apply the old gpoint membership or ordinate-removal stages to these new root equations. Preserved labels do not justify an old rule.
- Check all current metadata and source-entry schemas for the replaced root_targets record. Do not leave an old fixed-target ordinate reference or relabel historical IDs as current.
- Apply any shared-square rewrite after this exact pinned root rewrite, or review a new input binding. Its root pair will have new IDs; the old census IDs are not transferable.
- Perform fresh independent full-module reconstruction, source flattening, replay and final coefficient collection. The isolated fixed-row SOS bound and raw minus86 allocation do not establish the endpoint.

No remaining arithmetic mismatch was found in this helper at the reviewed hash. The named combined source and its final field/coordinate maps remain unreviewed until emitted.
