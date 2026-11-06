# Version 4 research handoffs

The repository working manuscript now includes the Pheidas attribution update. The existing research ZIPs predate that editorial change; use the current [TeX](../quartic_4973.tex) and [PDF](../quartic_4973.pdf) for the updated manuscript.

## Latest credit update

The [November 6 revision-3 research release](https://github.com/elliotglazer/diophantine-z-q/releases/tag/research-handoff-2026-11-06-r3) supersedes revision 2 as the newest handoff. It includes the corrected [project credit](../CREDITS.md) and otherwise retains the same mathematical research and unchanged Version 4 manuscript and polynomial. Its own release checksum and receipt identify the rebuilt archives.

The refreshed archives contain public snapshot `098b50006d1459821daeb4d29269a37688b87e8e`.
The [new build receipt](research-2026-11-06-r3/BUILD_RECEIPT.json) records successful member/hash verification of both archives. The current-only archive passed extraction and the research checks were rerun successfully from the extracted copy.

| Updated archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `z-in-q-version4-full-handoff.zip` | 374769889 | `c278ff1383570cee840fbfd9cf249297546e6e13fff5c93fd0e066787fd1986d` |
| `z-in-q-version4-current-handoff.zip` | 34908844 | `ecbbfc6b18a23ae3cdee64287a18bf863996bc8bff98486b40b2f0842a6ebcc9` |

The new [frozen plan](research-2026-11-06-r3/handoff-plan.json) has SHA-256 `bbe7aa99b2a710e1f544f52efcf2e5ab8aa90fe094e27978881afb84c6a22784`. These post-build records do not alter the snapshot inside either archive.

## November 6 revision 2

The [November 6 revision-2 research release](https://github.com/elliotglazer/diophantine-z-q/releases/tag/research-handoff-2026-11-06-r2) contains refreshed full and current-only handoffs. The manuscript and polynomial remain Version 4. The added [collaborator research collection](../research/2026-11-06-collaborator-notes/README.md) has unchanged supplied articles, the height replacement, source pins, and reproducible small checks. The original Version 4 archives below remain immutable historical snapshots.

The ZIP asset names retain `version4` because that is the manuscript they contain; use the dated research-release URL to distinguish this update. The release supplies its own new `SHA256SUMS`, `BUILD_RECEIPT.json` and `handoff-plan.json`.

The refreshed archives contain public snapshot `363f623014741037a19df138777e4d11ea946bab`.
The [new build receipt](research-2026-11-06-r2/BUILD_RECEIPT.json) records successful member/hash verification of both archives. The current-only archive passed extraction and the research checks were rerun successfully from the extracted copy.

| Updated archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `z-in-q-version4-full-handoff.zip` | 374630650 | `23fb8d7e5179f3b6a4bbcaaa764f3d58674cd2eedd8564338122c5e08e7006e0` |
| `z-in-q-version4-current-handoff.zip` | 34769597 | `e7fd377a15f7bfef8d3c296ad7bc9c2f6511181641c71d2df15b0203007466b0` |

The new [frozen plan](research-2026-11-06-r2/handoff-plan.json) has SHA-256 `43b524fdaaa4bc57f25da9b28d486c5c9805f5fa1f5855b7cd70a10b8b083cf8`. These post-build records do not alter the snapshot inside either archive.

## Original Version 4 handoffs

Date: November 6, 2026.

The [Version 4 release](https://github.com/elliotglazer/diophantine-z-q/releases/tag/quartic-4973-version-4) contains two archives:

| Asset | Contents |
| --- | --- |
| `z-in-q-version4-full-handoff.zip` | Exact public snapshot, selected mathematical research and reviews, and the unchanged November 4 revision-2 baseline ZIP |
| `z-in-q-version4-current-handoff.zip` | The same current snapshot and selected notes, with the baseline URL and checksum instead of the nested ZIP |

The current manuscript is `quartic_4973.tex/pdf`, Version 4. Its selected quartic has 4,973 total variables, 72,925 monomials and degree four. Source arithmetic reviews, finite certificate replay and fresh reproduction have separate roles in the included evidence.

Compare each archive's SHA-256 with the release's `SHA256SUMS`. `BUILD_RECEIPT.json` gives the exact snapshot and frozen-plan digest. An internal manifest does not authenticate its own origin.

After extraction read `START_HERE.md`, `CURRENT_STATE.json`, `COVERAGE.md` and `RESEARCH_NOTES.md`. `current/` is every regular tracked file at the recorded public commit. `history/version4/` contains selected proof and review provenance; its dated pending statuses are historical. Optional scalar/J0 fusion is excluded from the selected source. Earlier version directories retain their original meaning and claims.

```
python -E -B handoff/verify_handoff.py PATH_TO_HANDOFF.zip --expected-plan-sha256 DIGEST
python -E -B handoff/verify_handoff.py PATH_TO_HANDOFF.zip --expected-plan-sha256 DIGEST --extract NEW_DIRECTORY
```

Use the plan digest from the independently obtained release receipt. The verifier checks every member, exact planned file coverage, source-package closure and the selected reproduction receipt. It rejects unsafe names, duplicate paths, case collisions and symlinks. The archived Version 3 verifier and matching helpers remain under `history/version3/tooling/` for Version 3 archives. Version 2 uses the preserved legacy verifier with its independently published whole-archive checksum.

Run the actual mathematical computations from `current/` using the [reproduction instructions](../quartics/quartic-4973/reproducibility/README.md). Archive integrity does not establish the arithmetic theorem. The finite checks do not upgrade the inherited theorem qualifications or complete the Lean formalization.

The unchanged historical baseline is 339,860,770 bytes, SHA-256 `827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b`. Its own `current/` directory means current at its historical date. The full archive is self-contained for the included collections, not a claim to contain every private research record. Conversational transcripts and credentials are excluded.

See [BUILDING.md](BUILDING.md) and [SCOPE.md](SCOPE.md). A later commit may record the finished archive checksums; the archive continues to identify the earlier snapshot it actually contains.

## Verified Version 4 artifacts

The archives contain public snapshot `2ba2e731eba9a9886bd10a0c3535ad0a8d368a7c`.
The [build receipt](../docs/quartic-4973-validation/HANDOFF_BUILD_RECEIPT.json)
records complete member checks for both archives. The current-only archive also
passed extraction. [The frozen plan](../docs/quartic-4973-validation/HANDOFF_PLAN.json)
has SHA-256 `1eeafb3f7eb413ee882091792a19384ca557cd82c3ddf251b55b38504b81ed42`.

| Archive | Bytes | SHA-256 |
| --- | ---: | --- |
| `z-in-q-version4-full-handoff.zip` | 371756101 | `65b113940ea88433d34fc00fcb5f472011664d127bcbaccec7ceb5b5b672ad20` |
| `z-in-q-version4-current-handoff.zip` | 31895055 | `b5a4ed9e0b4e58ad53c0410f3976259b696892a4883557aab5ab05e567b00086` |

These post-build records were added after the archived snapshot. They do not change either ZIP.
