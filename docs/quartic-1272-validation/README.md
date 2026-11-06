# Version 5 release validation

The receipts in this directory bind the final Version 5 manuscript and the independently reconstructed quartic. `build-report.json` records the pinned Tectonic build. `visual-review.json` records the rendered pages and inspection scope. `REPRODUCTION.json` records a fresh isolated reconstruction with all 14 checks and exact coefficient-table byte identity. `original-construction-checks.json` records the retained original construction check.

The theorem-application inventory and its independent reviews are in [../quartic-1272/](../quartic-1272/README.md). Source qualifications remain explicit there. These finite and document checks do not independently prove every external arithmetic theorem.

The retained Version 4 manuscript and polynomial are unchanged. The requested credit correction from the short first name to Jennifer Park is recorded separately in the handoff preservation metadata. Release snapshots and archive checksums are recorded after the archives are built.

The first Linux CI run exposed a line-ending mismatch in regenerated metadata after all computational stages passed. `serialization-repair.json` records the exact changes. Metadata now uses explicit LF; polynomial tables preserve their published CRLF bytes. Mathematical syntax trees and parsed core artifacts are unchanged. The final `REPRODUCTION.json` is the complete replay after this repair. `root-serialization-replay.json` records an additional independent local replay before the final README-only clarification; its earlier package-manifest hash is intentional.
