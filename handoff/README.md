# Current update: Version 9

The [Version 9 supplement](../research/version9/README.md) adds the 523/540-variable source, complete tables, arithmetic audit, new inventory and current TeX/PDF. Pair it with the Version 7 full archive for earlier research history. The older archives below are unchanged.

# Version 7 research handoffs

The Version 7 handoff adds the four Gaussian appendix audits and repairs. It contains the unchanged 962-coordinate quartic, its source and certificates, the optimization history, lower-bound audit, analytic proof work, and independent reviews. Earlier quartics and the original construction remain at their existing repository paths.

The release tag is `quartic-962-version-7`.

| Archive | Contents |
| --- | --- |
| `z-in-q-version7-current-handoff.zip` | Complete recorded public Git snapshot and current orientation notes |
| `z-in-q-version7-full-handoff.zip` | The same collection plus the unchanged Version 6 full archive |

The source inventory and final independent reviews are bound to the manuscript and authored register. Archive builds require a `READY` descriptor and a complete immutable Git commit. The release checksums and build receipt identify the resulting archives; this guide alone does not identify archive bytes.

Compare the archive checksum with the release checksum, then run:

```sh
python -E -B handoff/verify_handoff.py ARCHIVE.zip --expected-archive-sha256 ARCHIVE_SHA --expected-plan-sha256 PLAN_SHA
```

Add `--extract NEW_DIRECTORY` to extract only after verification. The verifier checks every archive member, exact planned file coverage, the complete frozen package and research inventory, reproduction receipt, and historical preservation pins.

The snapshot is under `current/`. Start with `current/manuscripts/quartic_v7.pdf`, `current/docs/quartic-962/README.md`, and the frozen package. The portable replay entrypoint is `current/scripts/check_quartic962.py`. [replay_extracted_current.py](replay_extracted_current.py) authenticates a current-only archive and runs its checks with outputs outside the snapshot.

The unchanged Version 6 full archive has 440,334,958 bytes and SHA-256 `93b53944ea93de08dc653beb70202797c1cbbdf19602ae583940bbf137dd43bc`. Its own nested revision-2 archive, source inventory and verification tools remain intact. Each historical `current/` directory describes its own release date. Previous handoff tools and notes remain under [releases/version5](releases/version5/), with earlier records at their existing paths.

Contributors: Stefan Baranczuk, Jose Brox, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry.

Archive integrity, finite computational checks and mathematical source review have separate scopes. The main Lean theorem remains unproved. See [BUILDING.md](BUILDING.md) for the build sequence and [SCOPE.md](SCOPE.md) for the selection policy.

Version 7 adds the four Gaussian audits and exact repairs under `docs/quartic-962/evidence/gaussian-four-audit-20261106/`, with an overview in `research/version7/README.md`. `V6_RESEARCH_MANIFEST.json` continues to describe the unchanged Version 6 research collection; `V7_AUDIT_MANIFEST.json` binds the new audit collection.
