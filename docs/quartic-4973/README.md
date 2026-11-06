# Version 4 theorem inventory

This inventory binds the accepted `quartic_4973.tex` to `target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b` and the finite
certificate with 4973 total variables, including the input, and
4972 rational witnesses. The reported polynomial has 72925
monomials and degree 4; its maximum absolute coefficient is
685783949153203534233890.

`theorem-applications.json` records each selected lemma and exact statement/proof
span. `dependency-closure.json` separates arithmetic dependencies, published
applications, and active finite certificate rules. `baseline-bridge.json` keeps
the historical reviewed objects and maps only their unchanged text to the
current manuscript. Historical source conventions are qualified by the explicit
current-consumption records; they are not silently carried forward.

The selected line includes target two, tangent fusion, shared square, first-norm
fusion, and the mixed-mode denominator correction. Optional scalar/J0 fusion is
excluded. Frozen context files may mention other branches as historical records;
their unselected proof artifacts are not copied here.

The new external application is Koenigsmann's quaternion trace criterion in
Definition 4, Observation 5 and the proof of Proposition 6, Facts (a),(b),(c),(e).
The other new steps are author-proved elementary/arithmetic construction lemmas.
All five inherited source-version and proof-status qualifications remain explicit.

Validate from a trusted checkout with the independently recorded acceptance hash:

```
python -E -B inventory.py validate --repo REPOSITORY --docs THIS_DIRECTORY --acceptance-sha256 TRUSTED_HASH
```

This command checks text spans, graph closure, source metadata, all inspected
source/auditor file pins, the compiled payload pins, and receipt correspondence.
It does not rerun the mathematical source audit, certificate replay, or clean
reproduction. Their separate accepted review/receipt objects are mandatory in
`acceptance.json`; the release must also run those checks. An internal hash list
alone is not an external trust anchor. Changes to the selected mathematics,
source family, final counts, or acceptance object require renewed review.
