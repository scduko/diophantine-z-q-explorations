# Version 10 research supplement

This supplement contains the current TeX/PDF, the nine-point response to [Issue 2](https://github.com/elliotglazer/diophantine-z-q/issues/2), the source and convention register, and the exact revision and inventory checkers. It also contains the Version 9 supplement as a nested archive so that the unchanged polynomial data and its audit can be retrieved alongside this revision.

Download [z-in-q-version10-supplement.zip](z-in-q-version10-supplement.zip). [SUPPLEMENT.json](SUPPLEMENT.json) records its SHA-256 and contents. It is a supplement to the [Version 7 full history](../../handoff/README.md), not a replacement for that archive. No conversational transcript is included.

Start with [the review dispositions](../../docs/manuscript-revisions/version10/README.md). The exact source pins distinguish published originals, corrected author versions, historical metadata and unpublished attribution sources. New unpublished arithmetic results are not assumed. The archive does not claim a completed Lean proof or fresh independent validation of the entire manuscript.

The ZIP contains `version9-base.zip`, a `current/` overlay, a manifest of SHA-256 hashes, and `restore.py`. After unpacking it in a new directory, run `python -B restore.py restored`. This checks both manifests, extracts the Version 9 baseline, and overlays Version 10 without replacing the historical manuscript. From `restored/`, run:

```sh
python -B docs/manuscript-revisions/version10/check.py
python -B docs/manuscript-revisions/version10/check_valuation.py
python -B scripts/check_construction.py
```

The last command requires Node.js 22 or later. The archive includes the complete original construction program and its saved expression. External literature PDFs are identified by URLs and hashes; they are not newly redistributed here.
