# Version 5 research handoffs

The Version 5 handoff contains the 1,272-variable quartic manuscript, the complete independently reconstructed program and coefficient tables, exact certificates, source reviews, and dependency inventory. The Version 4 manuscript and package, earlier quartics, and original construction remain at their existing repository paths.

The release tag is `quartic-1272-version-5`. Its two archive names are:

| Archive | Contents |
| --- | --- |
| `z-in-q-version5-current-handoff.zip` | The complete recorded public Git snapshot and the selected mathematical research history |
| `z-in-q-version5-full-handoff.zip` | The same collection plus the unchanged November 4 revision-2 baseline ZIP |

The archives are built only after the complete Version 5 snapshot is committed. The release's `SHA256SUMS`, `BUILD_RECEIPT.json`, and frozen `handoff-plan.json` identify the actual archive bytes and included commit. A later commit recording these receipts cannot be included in the archive it describes.

Compare the archive checksum with the independently obtained release checksum, then run:

```
python -E -B handoff/verify_handoff.py ARCHIVE.zip --expected-archive-sha256 ARCHIVE_SHA --expected-plan-sha256 PLAN_SHA
```

Add `--extract NEW_DIRECTORY` to extract only after verification. The verifier checks every member, exact planned file coverage, all Version 5 package pins, the package manifest, the complete fresh-reproduction receipt, and the preserved historical file hashes. It rejects unsafe paths, duplicate or case-colliding names, symlinks, missing files, and unexpected package files.

The archived snapshot is under `current/`. Start with `current/quartic_1272.pdf`, `current/quartics/quartic-1272/README.md`, and `current/docs/quartic-1272/README.md`. To rerun all Version 5 checks from an authenticated current-only archive, use [replay_extracted_current.py](replay_extracted_current.py). It keeps replay outputs outside the extracted snapshot.

The historical baseline has 339,860,770 bytes and SHA-256 `827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b`. The full handoff stores those bytes without recompression. The current-only handoff gives the baseline URL and checksum. No old release asset is replaced by a Version 5 archive. The active repository's project credits use Jennifer Park's full given name; the descriptor records the one corresponding editorial exception to its historical file pins.

Version 4 release records remain in [research-2026-11-06-r3](research-2026-11-06-r3/), [research-2026-11-06-r2](research-2026-11-06-r2/), and the [original Version 4 validation directory](../docs/quartic-4973-validation/). Copies of the previous handoff descriptor and documentation are in [releases/version4](releases/version4/); their relative links retain their original `handoff/` interpretation. The historical Version 3 and Version 2 records are unchanged.

Archive integrity and exact replay are separate from the source arithmetic assumptions. The reconstructed program does not recover Brox's absent original program or table. Neither the package nor its checks complete the Lean formalization. See [BUILDING.md](BUILDING.md) for the build sequence and [SCOPE.md](SCOPE.md) for the selection policy.
