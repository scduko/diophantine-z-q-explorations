Version 4 of *Z is Diophantine in Q*, dated November 6, 2026, supplies an explicit integer quartic in 4,973 total variables, including one rational input and 4,972 rational witnesses. Its expansion has 72,925 nonzero monomials and maximum absolute coefficient 685783949153203534233890, strictly below 2^80.

The current files are `quartic_4973.tex`, `quartic_4973.pdf` and the `quartics/quartic-4973/` proof package. The source uses 13 full comparisons, eight beta-only comparisons and 16 Lucas-only comparisons, with H19, high40, beta12, anchor25 and scalar32. It includes general roots, doubled targets, direct tangent equations, shared field squares and first-norm fusion. Optional scalar/J0 fusion is not used.

The full handoff includes the exact public snapshot, selected project notes and the unchanged public November 4 revision-2 baseline ZIP. The current-only handoff supplies the same snapshot and notes with the baseline's URL and checksum. Check downloads against `SHA256SUMS`; `BUILD_RECEIPT.json` and the frozen plan identify the snapshot and payloads.

The baseline retains SHA-256 `827765f17087e1794c15770221a3a2d0fefed25839566a4a9bfb3b5aaa1ed42b`. The full ZIP is self-contained for its included collections, not all private history. Read `START_HERE.md`, `CURRENT_STATE.json` and `COVERAGE.md` after extraction.

Exact certificate checks establish rational projection equivalence to the pinned source and verify the complete integer expansion. They do not replace the arithmetic proof or upgrade its inherited theorem applications. The separate Lean formalization remains incomplete.

Version 4 is a collaboration using the collective agentic notes from Stefan Baranczuk, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry. The October 11 manuscript's provenance remains distinct.
