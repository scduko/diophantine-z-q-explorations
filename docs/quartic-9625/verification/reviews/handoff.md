# Version 3 handoff release-quality review

PASS for the frozen handoff script packet after the fixes described below. No unresolved defect was found in the reviewed release scope. This is a review of the scripts, metadata, selected records and their bindings. No full handoff archive was built or extracted, no remote workflow was dispatched, and no release was published by this reviewer.

The packet is `work/quartic-sub10000-20261106/parity/release-handoff`. Its `COPY_MANIFEST.json` has SHA-256 `3406703fc2b5013f5ea6e1c6d734f1fc79feeca1e093e948fab9f0056028d8fe`. I independently checked every listed size and digest, including the hidden workflow. All 61 files match, and there are exactly 61 files under `copy-files/`. The author confirmed this freeze. This receipt is outside that frozen directory and changes no packet or public-checkout file.

## Findings corrected before freeze

1. The first archive verifier checked that every planned member appeared in the manifest but allowed additional root or history members. That could pass with an unchanged externally authenticated plan. The final verifier requires the exact union of planned members, its explicit generated-file set and the optional pinned baseline. It also binds the top-level helper bytes to their committed `current/handoff/` copies, reconstructs the complete current-state object and guide from the plan, and checks the history-scope text. The recorded tests retain the same external plan digest while adding files or altering generated files, and reject those mutations.

2. The first release validator allowed an arbitrary later version, count and date when its names were made consistent. The final validator requires Version 3, 9,625 total variables and November 6, 2026. The tests reject a premature Version 4, the separate 8,777-variable result and a stale date. The next-release field requires Version 4 to have strictly fewer than 5,000 total variables, including the input. It does not replace the fixed current release.

3. The workflow initially checked only for an existing GitHub release. An existing Git tag without a release could therefore select a different commit. The final workflow separately queries the exact remote tag, aborts on a failed query, and refuses any existing tag before creating the draft with the full GITHUB_SHA target. This matches the documented CLI distinction: the target selects the commit for automatic creation of an absent tag. See the [official release-create documentation](https://cli.github.com/manual/gh_release_create).

The historical Version 2 verifier remains byte-identical to the previous public copy. The new wrapper rejects plan-only authentication for that legacy format and states that its independently published whole-ZIP checksum must be checked first. Its result is explicitly scoped to legacy integrity, without the stronger Version 3 exact-plan claim.

## Snapshot and reproduction bindings

The preparer resolves a full immutable commit ID, enumerates its complete regular-file Git tree and reads each blob from Git. It rejects nonregular members rather than silently dropping them. Every current destination is exactly `current/` followed by its original path. The builder independently re-reads the complete commit tree and requires the same path-to-blob map, so it cannot build a partial snapshot or swap current destinations while retaining the frozen plan. It hashes the bytes written to both archives and verifies both completed archives before writing a PASS receipt.

The release descriptor itself must be present in that same commit. All seven proof-file pins match the assembled `quartics/quartic-9625/` files I inspected. The pinned source entry binds the inspected source files. The reproducibility manifest binds its complete listed package files. Current verification and fresh reproduction must agree on source ID, source digest, checker digest and every selected numerical expectation. The fresh receipt must bind the exact package-manifest bytes and the regenerated certificate digest. These field names agree with the actual reproduction runner's output schema.

The preparer requires the real committed reproduction receipt. `check_packet.py` separately uses an explicitly synthetic in-memory receipt only to test compatibility; its result is labeled `PASS: STAGING CHECKS ONLY`. No synthetic receipt is written into the public release. The recorded staging check identifies the assembled package manifest as `eb4b2ae93f932d96919d8779f937b7eec47163c8cf8909d1b66a55b1fdc08559`.

The standalone archive verifier verifies bytes against the frozen plan and its generated-file rules. It does not independently fetch the advertised Git commit. The documentation correctly requires an independently obtained whole-archive checksum or, for Version 3, an independently obtained plan checksum. An embedded manifest is not presented as its own authentication source.

## Public scope and status

The current tree is the caller-selected, reviewed public commit. The additional history is a fixed list of 47 mathematical proof, review and orientation records. I checked all 47 sizes and hashes against `selection.json`. The paths select no conversation archive, credential store, unrelated project or private full-handoff collection. The inherited scanner rejects forbidden path components, dialogue markers and credential patterns, including within gzip text. Its negative fixtures cover those cases. Pattern scanning is not a claim of a new exhaustive content audit of all historical material.

The full archive includes the already-public November 4 revision-2 baseline unchanged, with required size 339,860,770 bytes and SHA-256 `827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b`. The builder checks this identity and streams it without recompression. The current-only archive records its URL and identity instead. Both the code and documentation expressly retain the baseline's original notices and filtering and disclaim a new baseline content audit.

The active descriptor, documentation and generated state consistently identify `quartic_9625.tex`, `quartic_9625.pdf`, 9,625 total variables, 9,624 witnesses, 9,161 residuals and 82,476 monomials. The selected source is `selective-beta-k40-q12-a25-h19-s32-d68d86cdf995`, with 37 contacts, 29 full plus 8 beta-only comparisons, H19, precisions 40 and 12, anchor 25 and scalar 32. Three-mode, Jacobi, tangent and anchor alternatives are separately labeled research. Historical provisional wording is retained as provenance, not silently relabeled as current acceptance.

The documentation separates archive integrity, exact algebraic replay and the arithmetic proof. It preserves inherited theorem-application qualifications and states that the separate Lean formalization remains incomplete. The workflow creates a draft only, under the intended public repository guard. It uploads the snapshot-bound plan, checksums and receipt alongside the manuscript and two archives. A later checksum or receipt commit is explicitly distinguished from the earlier commit actually archived.

## Recorded tests and remaining execution

`TESTS.json`, SHA-256 `165b09fa1f9242e929e50a3b03297fdac598a9e77fc8ce3b6f74483240ed73bb`, records 57 negative cases and a valid small archive fixture. I inspected the corresponding test code and cases. They cover unsafe paths, case collisions, symlinks, omitted or swapped Git members, credentials/dialogue, stale release fields, wrong reproduction evidence, the legacy authentication restriction, and the exact-plan/generated-file regressions found during this review. I did not independently rerun that test program.

`STAGING_CHECKS.json`, SHA-256 `d78ad4a80de24cda6f47fda750e93acddfbadfbc37524d874d07503a0acbc572`, accurately scopes its scan, syntax, selected-file and schema checks. The reviewed verifier has SHA-256 `2e69117152177798817b287f53074895582963dadd2ca39aee9cee6c3613706f`, the release configuration `7df2bbc01249424b7b31b3ca186414493d1fd4345c14dc1a46f2d1ca65defbf1`, the builder `2ca1434dd5c187a727fc533a6985d1570d3371e102249287b44c780d98f3b496`, and the workflow `420bd99163fd35e044699127303b2091d82a34e1e680f5c7184cc9d9ff2da705`.

Root still needs to copy these exact files, commit the complete intended public snapshot with its real fresh-reproduction receipt, run the remote build, and inspect the resulting draft assets and receipts. This review supplies no archive size, archive digest, successful remote-build claim or publication claim. No further script edit is requested for the frozen packet.
