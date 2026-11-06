# Actual normalized-ten pole source binding

Date: 2026-11-06. PASS for the emitted source's correspondence to the reviewed normalized-ten arithmetic and for the inspected artifact identities. This is not a new proof of inherited arithmetic inputs, and no full replay was run locally.

The exact source is `joint-chart-normalized-lucas-linear-pole-anchor4-k40-q12-a25-h19-s32-0f54051d0d14`.

| Item | Value |
|---|---|
| Run | `42238870988` |
| Commit | `bf8e42e7c51a1e87c8c347bd76f37d665349f7f7` |
| Artifact | `13514830534` |
| ZIP SHA-256 | `7d8d6fd86a1a71a91af67fc6cd02fb444e76af25a5ee20e67b36694acbffe228` |
| Packet manifest | `5884f634e36980f133a50266cc506c51a9b0733672a70309c29d97ea586e9267` |
| Source compressed SHA-256 | `2629edef151e8bf0cb366edc3bc5876bbd5c09d59e1785670848a6ce12c5d82e` |
| Source uncompressed SHA-256 | `0f54051d0d1400c9944688f9aaf1db4a65177b548609da424c98fe5172f8595a` |

I checked the actual artifact ZIP and run metadata, all frozen packet files, every reported stage log and all audited source files in the original, deterministic-repeat and adapter copies. The decompressed source hash and its 4,682 residual records agree with the source entry. The complete bounded inspection is `inspect_linear_pole_artifact.py`, with detailed output in `LINEAR_POLE_5364_RECEIPT.json`.

## Exact change from the accepted merged source

The root, all three comparison modules, anchor, scalar-height module, original scalar parity module and shared constants are byte-identical to the accepted merged source `0ac4a7757fb9`. Each conic batch has exactly the same residuals, local variables, powers, fields and upper norm tree as that parent. Its only changes are the ordinary call's module name and the declared pole metadata. The actual new module is exactly the independently reviewed normalized-ten literal, with free inputs `[r,theta,W]`, ten local variables, eight quadratic rows and residual coefficient bound 867.

The actual construction map contains 37 ordinary calls. I checked every triple against its parent batch's raw input, its own private theta and its original upper norm root. All 111 private conic coordinates are distinct. The original fields precede each private conic, so the existing coefficient-independence property is retained. There is exactly one original parity call, inside scalar height. The source locator exposes only the six unchanged old root charts and no comparison contact inverse.

The 13 full, 8 beta-only and 16 Lucas-only occurrences retain their complete field lists and orders, totalling 377 fields. Thus normalized Lucas, the 29/21 height coverage, original root37 abscissa targets, primary formal tests, alternate ratios, G circuits, beta definition, H19/high40/beta12/anchor25/scalar32 and the four-witness anchor are all unchanged.

## Arithmetic scope

The replacement is governed by `parity/sub5000/linear-pole-next/PROOF.md`, SHA-256 `0b52a6ac4840636be12f455bf0e8b07ba02bb2308493d937afd840ea19bdb510`, and contract `19c3f7d65aae9f38aeaea9cc9c079d0ec7ca9918123d96d1744813ae81e61869`. Its independent mathematical review is `LINEAR_POLE_REVIEW.md`, SHA-256 `885fa0233d3e739999ba0132a9bbae33f9eac53491945250fd08100751c685a3`. The frozen integration is independently reviewed in `LINEAR_POLE_OUTER_REVIEW.md`, SHA-256 `f1e4b381692c1cf5e0edd2c56b4f4f311e3da5a405270d2d629b7a5bbdbb09f7`.

The actual source retains the same equation `theta^2-r*s_c^2=2`. At every odd valuation of r it makes `3-2theta` a local unit. The new ordinary pole therefore excludes negative odd valuation of nonzero rW^2 outside 2,3,17, including all zero-ordinate cases in its proof. This is exactly the one-sided assertion consumed by the comparison norm argument. The source and contract correctly deny a claim of equivalence to the old full Psi predicate. The unchanged scalar-height call continues to use its original stronger theorem.

For completeness all elliptic and normalized ratio field coefficients are fixed before private theta. The retained W(theta) is the same polynomial as in the parent. Its simultaneous approximation near the selected split root and near theta=3/2 at the real,2,3,17 places supplies the reviewed fixed-U smallness conditions. The exact source calls preserve these premises. No new prime restriction, root-height condition, or normalization is introduced. The H19 and other inherited arithmetic qualifications remain in force.

## Verified endpoint and limits

The source has 5,104 total coordinates including its input and 4,682 rows. All six remote algebraic stages report PASS on this same source. The endpoint has 5,364 total variables, 5,363 witnesses, 4,943 rows, 79,824 monomials and degree four. All weights are one; the maximum absolute coefficient is `685783949153203534233889`, below 2^80.

The endpoint certificate SHA-256 is `3bec519345f2b8e531b58cb2f56958998d21c22238550fddd8d3bec9bdc4accb`; expanded polynomial SHA-256 is `21a05bff86eb2e798175b8518bfff614c611709b2a6253a8acf24deeab2356d1`; checker SHA-256 is `0d794ea9a663f9e325bab51c6c8332eddec4686379a16a3f5ceff348af32fd3e`. I checked the actual files against these records. The 391 operations retain the same rule families as the accepted merged parent, including exactly one old scalar parity transformation.

The remote source test reports 208 distinct semantic mutations and a separate resource-abort regression. The new pole's local integration and locator mutation suites were independently checked before freezing. These finite checks establish the reported artifact relationship; they do not prove the inherited arithmetic literature interfaces. This source uses neither the proposed half-generator root rewrite nor shared-square rewrite, and it remains above the 5,000-total milestone.
