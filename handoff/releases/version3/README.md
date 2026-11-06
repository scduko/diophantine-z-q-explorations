# Version 3 release record

Published November 6, 2026. The [release](https://github.com/elliotglazer/diophantine-z-q/releases/tag/quartic-9625-version-3) contains `quartic_9625.tex`, `quartic_9625.pdf`, both research handoffs, checksums, the build receipt and the frozen plan.

The archives contain the exact public snapshot at commit `c1654a9e9653cf2e0c9a0495ea60dc9b81727226`. This record was added after publication and does not change that snapshot.

| Download | Bytes | SHA-256 |
| --- | ---: | --- |
| [Full research handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-9625-version-3/z-in-q-version3-full-handoff.zip) | 363,943,274 | `1cdf754d84ce8cc906f6f5a4952381a5d4708bf4fa8d68136a3234a37dcda70a` |
| [Current research handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-9625-version-3/z-in-q-version3-current-handoff.zip) | 24,082,228 | `3e758516b8e0b0d7c6739e8f432d1156f081b92b221b8ff6a65c736503a35486` |

The full archive includes the unchanged November 4 revision-2 baseline. Both archives include the selected research notes and the Version 3 public source tree. They contain no conversational transcript.

[Build run 42232288409](https://github.com/elliotglazer/diophantine-z-q/actions/runs/42232288409) passed. It checked packaging, verified the historical baseline, built and verified both archives, and extracted the current archive successfully. The [build receipt](BUILD_RECEIPT.json), [extraction result](handoff-extraction.json), [packaging tests](handoff-tests.json), [frozen plan](handoff-plan.json), and [asset comparison](ASSET_VERIFICATION.json) record the checks. All seven GitHub asset digests matched the build outputs and reviewed manuscript files.

The frozen plan's SHA-256 is `320062d2990381336a0918cf5fe5fe98d871d6c824ddf4ee05ac5ad636a25b48`. Use it with the verification commands in the [handoff guide](../../README.md). [SHA256SUMS](SHA256SUMS) also covers the TeX and PDF.

The released quartic has 9,625 total variables, including its input, and 82,476 nonzero monomials. Version 4 is reserved for a quartic with strictly fewer than 5,000 total variables. Archive validation certifies the packaged bytes and their recorded checks; it does not replace review of the mathematical argument.
