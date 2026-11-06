# Independent Version 3 inventory review

**PASS; no release blocker found.** This was a bounded metadata, dependency
and provenance review. No shared file was edited and no polynomial was
expanded. Exact reviewed file hashes are recorded in bindings.json.

The current TeX is
`dc77c88b5cc0819201343dc85d0891d4dad81d97ac3267ec1df34eb38003b552`.
The validator preserves the frozen arithmetic patch and checks the entire
current body after precisely one specified display split and removal of
its leading spacing command. It does not generally ignore whitespace or
allow arbitrary mathematical changes during inventory refresh.

The source and quartic counts are correctly distinguished: the named source
has 9,318 variables and 8,854 residuals; the compiled quartic has 9,625
variables, 9,624 witnesses, 9,161 quadratic rows and 82,476 monomials. Source
id, raw/compressed source, source-entry/audit/map, auditor, certificate,
checker and expansion digests match the frozen beta-only package. The
maximum coefficient is correctly stated as 685783949153203534233601, below
2^80. Input0 is included in the total count and remains compact variable0.
All 115 files listed in the current package manifest were independently
checked for exact byte size and SHA256.

The 74 dependency edges are substantive links from the main theorem to
the fixed-source arithmetic theorem, finite certificate binding and generic
algebraic reductions. The arithmetic theorem then reaches the new height,
contact, local precision, anchor and beta conclusions, together with their
inherited and published applications. All 40 nodes are reachable from the
main theorem and the graph has no directed cycle. The validator requires
the exact edge set derived from the pinned arithmetic registry and retained
algebraic dependencies, so merely adding an isolated bibliography item
cannot satisfy closure.

Historical review scopes are preserved. The original source excerpts and
citation paragraphs must remain byte-identical through the historical
bridge. The old H5 input feeds a separately bound H19 proof; it is not
renamed as an H19 review. The old 24-squaring anchor cutoff remains
historical while the new 25-squaring cutoff is explicitly assigned to the
current anchor lemma. Released 16/64 realizations do not automatically
accept the new 12/40 estimates or circuits. The pole/restricted-converse,
Pan/Calegari, Yuan and sieve source-version qualifications remain explicit.
The retained generic algebraic lemmas keep their original provenance;
only the finite sum-of-squares row count is instantiated at 9,161.

I independently ran validate.py and all 14 malformed-inventory cases; both
passed. The cases reject dropped or changed arithmetic nodes, publication
and inherited applications, retained rules, source-version qualifications,
finite targets, dependency edges, historical anchors/citations/scopes,
registry targets and the approved layout record. Receipts are validation.json
and negative.json beside this review.

There is a deliberate division of checks. The inventory validator binds
claims, provenance and selected exact finite inputs; it does not replay the
certificate or independently inspect the compiled candidate-row files.
Those files are bound by the complete package manifest and the separately
required fresh full replay. I checked the manifest coverage here. This
scope distinction does not leave an open release gap and requires no extra
validator assertions. Neither metadata closure nor this review claims to
prove the mathematical theorems or replace the full replay.
