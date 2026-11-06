# First-norm locator and adapter review

Verdict: PASS for the specified locator/adapter integration. No blocking defect found. This review does not accept a generated source, a final quartic, or a measured saving. Guards owns the independent outer source review.

Reviewed packet: `source-pipeline/sub5000/target2-tangent-first-norm`, relative to `work/quartic-sub10000-20261106`.

| File | SHA256 |
| --- | --- |
| source_layout.py | 4e8f9ada790ead20e87be1bcb226da9da0df12b8260d3aadfbcd6ffa10800d30 |
| prepare_adapter.py | aa3c9f6ef0eed12da5ef3b9b26c4d58cfa37e23c3ad4c0e3e758e581b5a85809 |
| test_conic_locators.py | 244db18687ab123538043b8ed4645a1517467ba540899cec3d319b0048049762 |
| run_pipeline.py | 388151877642214d9ef831123e277e6928e5eb0f5a8c328fbc0878a5d39b5848 |

The first field must have the exact numerator record with field index zero, order one, inputs 1 and 2, `norm=None`, input-zero power, and virtual denominator exponent one. The separate fusion record binds its role to H.f, checks integer types, distinct local numerator/node/original-power coordinates, row bounds, and the two changed labels. The exported record keeps `norm=None` and `input_type='first field numerator'`; it separately exports the numerator, first node, and the instantiated raw contact r. In particular, input zero becomes the actual argument at each batch occurrence, rather than a literal zero or the old r-squared coordinate.

The row list includes the changed numerator label at its original position. The shared squared-field channel remains at indices 5, 2, and 4 in full, beta, and Lucas batches. Its missing private evaluation is distinct from the first field's retained evaluation. The adapter requires 37 numerator records, 340 ordinary norm records, 377 total fields, 340 evaluations, and unchanged mode/pole counts. Both the source module hashes and construction-map hash are checked before deriving the layout. The derived layout bytes and count dictionary are bound into the named source entry and checked again on loading.

The locator intentionally does not prove residual identities from labels. The independently reviewed first-norm restoration helper and complete parent source callback establish those identities, field order, all unchanged rows, and the full call graph before adaptation. The adapter pins that auditor and all helper dependencies and checks the exact inspected-file set, now including the first-norm contract, proof, and mixed-mode denominator clarification. The existing helper review in this directory covers the change from a norm witness to a numerator.

`run_pipeline.py` is byte-identical to the tangent parent. Its only stages are fresh lifting, parity, optional generic optimization, and coordinate merging, each followed by the named-source checker. Fresh lifting reads only the guard portion of the locator. The parity producer reads only parity records. No ordinary norm, batch-absorption, or G-specific locator consumer runs. Historical producer/rule files remain in the toolchain, but this verdict does not authorize applying an old norm interpretation to the first field. The new fused node is handled as a residual, not as an acyclic definition of N divided by r.

Validation used only tiny synthetic module/visit fixtures. All 153 locator negatives passed at their stated assertion. An additional independent probe assigned 37 distinct nonzero raw-contact arguments and 74 distinct first-field inputs, then checked every global numerator/node/row mapping and every preserved non-first norm record. It also checked the runner's byte identity to its parent. The result is `LOCATOR_PROBE.json`, produced by `probe_locators.py`. No full source generation or certificate replay was run.
