# Version 3 research orientation

Date: November 6, 2026.

Read the current manuscript and `current/docs/quartic-9625/README.md` first. The exact polynomial, source, certificate, verifier and reproduction instructions are in `current/quartics/quartic-9625/`. `CURRENT_STATE.json` records the immutable public snapshot and exact current counts.

Version 3 releases the 9,625-variable selective-beta construction. Its arithmetic changes are height exponent 19, 37 rational-target contacts, high logarithm precision 40, beta precision 12, 25 anchor squarings and scalar orders `[1,1,1,1,32,32]`. The eight A-coordinate contacts use beta-only comparisons. The other 29 contacts retain full comparisons. This distinction does not change the root contact formulas or the common auxiliary point.

The selected combined proof and arithmetic review are in `history/version3/precision/` and `history/version3/arithmetic-audit/`. The exact source and artifact review is in `history/version3/parity/beta-source-review/`. Earlier height and contact derivations are in `history/preceding-work/`. Original notes sometimes describe their then-pending review or implementation status; the final source bindings and release records state which result is current.

Three-mode and Jacobi constructions, along with tangent and anchor alternatives, are separate research in `history/not-in-version3/`. They are included to support further work. They are not part of the released source, its witness count or its certificate. Do not add savings from different experiments or substitute a differently audited source while retaining this release's artifact hashes.

The next publication threshold is fewer than 5,000 total variables, including the input. Only a result meeting that strict threshold is a candidate for Version 4. Intermediate improvements do not replace the fixed 9,625-variable Version 3 release.

The current certificate proves exact rational projection equivalence between its pinned source system and the final integer quartic, and checks the complete expansion. The separate arithmetic proof identifies that projection with the integers, under its stated inherited theorem applications. These checks do not upgrade the external arithmetic assumptions or complete the separate Lean formalization.

Version 3 is a collaboration using the collective agentic notes from Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, Caroline Terry. The October 11 manuscript's provenance remains distinct.
