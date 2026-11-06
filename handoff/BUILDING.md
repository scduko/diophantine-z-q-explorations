# Building the Version 5 handoffs

Use Python 3.10 or later and Node.js 18 or later. Build outputs and reproduction directories must stay outside the repository. The commands below do not publish or upload anything.

The historical pins are frozen in `handoff/releases/version4/PRESERVED_FILES.json`. They bind 607 original construction and earlier quartic files to public commit `5cb2c1997dde6e358f3c2fe9bbdb4b8f4c23bac6`. Do not regenerate these pins from the Version 5 tree.

The requested expansion to Jennifer Park in project credits is recorded separately. The descriptor preparer permits that exact textual replacement in the historical October 11 README and records its original and new hashes. All mathematical files retain their original pins.

First finish the Version 5 manuscript, PDF, package manifest, source reviews, and `docs/quartic-1272/` inventory. Run the package reproduction into a new directory outside the repository:

```
python -E -B quartics/quartic-1272/reproduce.py --out /tmp/version5-fresh-replay
```

Copy its successful `REPRODUCTION.json` to `handoff/releases/version5/REPRODUCTION.json`. Keep the generated work tree outside Git. Then prepare the descriptor and run the small packaging tests:

```
python -E -B handoff/prepare_release_v5.py --repo . descriptor --receipt handoff/releases/version5/REPRODUCTION.json
python -E -B handoff/test_handoff.py
```

The descriptor preparer fails if any current package file, manifest entry, required replay stage, count, source pin, or preserved historical file disagrees. Commit the complete reviewed snapshot, including the descriptor and replay receipt. Only then freeze and build the archives:

```
python -E -B handoff/prepare_handoff.py --repo . --commit SNAPSHOT_SHA --release handoff/release.json --verification-receipt handoff/releases/version5/REPRODUCTION.json --output /tmp/version5-handoff-plan.json
python -E -B handoff/build_handoff.py --repo . --plan /tmp/version5-handoff-plan.json --baseline /tmp/baseline-r2.zip --output /tmp/version5-handoff
```

The unchanged baseline is the [November 4 revision-2 archive](https://github.com/elliotglazer/diophantine-z-q/releases/download/research-handoff-2026-11-04-r2/z-in-q-research-handoff-2026-11-04-r2.zip). It must have 339,860,770 bytes and SHA-256 `827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b`. The builder streams it with ZIP_STORED and never downloads it.

The output directory must be new. It receives both Version 5 ZIPs, `SHA256SUMS`, and `BUILD_RECEIPT.json`. Archive members have fixed timestamps, permissions and platform metadata; the same plan, source bytes, Python and compression library produce the same archives. The manifest records every member's size and SHA-256. Both archives undergo member and package verification before the successful build receipt is written.

Finally authenticate, extract, and replay the current-only archive:

```
python -E -B handoff/replay_extracted_current.py /tmp/version5-handoff/z-in-q-version5-current-handoff.zip --expected-archive-sha256 CURRENT_SHA --expected-plan-sha256 PLAN_SHA --extract /tmp/version5-extracted --replay-output /tmp/version5-extracted-replay --report /tmp/version5-extracted-check.json
```

Take `CURRENT_SHA` and `PLAN_SHA` from the build's checksum and receipt, then preserve the plan, build receipt, extraction report, and checksums as release records. Archive extraction and replay need new, separate directories. Publish only after the release review accepts these exact files. Preserve all existing release tags and assets.
