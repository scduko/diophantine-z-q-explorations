# Offline source reproduction

This directory is self-contained. It reproduces and checks the two quadratic source systems underlying the new 554/571 and 523/540 variable quartics. It requires Python 3.10 or newer and Node 18 or newer, with no third-party Python or Node packages and no network access.

Run from any directory:

    python3 /path/to/source-reproduction/reproduce.py

For persistent rebuilt files and an audit receipt:

    python3 reproduce.py --work /tmp/h10-odd-product-replay

To additionally verify the elimination certificates, unique 17-coordinate constant lifts, and all four final polynomial tables, point to the directory containing the two final packages:

    python3 reproduce.py --packages .. --work /tmp/h10-odd-product-full-replay

The required sibling names are `final554_571` and `final523_540`. Each final package also runs independently with `python3 verify_all.py`.

The replay:

1. Checks every bundled file against `MANIFEST.json`.
2. Applies the supplied source patches to the previous 833-variable construction's builder. The optional branch first applies the asymmetric-depth transformation.
3. Requires byte-for-byte agreement with each frozen final builder.
4. Regenerates the raw systems, runs the unmodified upstream compiler, and runs the unmodified independent upstream checker on every gate, compiler certificate and expanded precursor polynomial.
5. Compares every compiled-source field with the frozen 561-coordinate or 532-coordinate precursor, except the explicitly documented fixed-parameter metadata correction.
6. With `--packages`, verifies all four final quartics using their independent exact Python checkers.

The source builders retain the historical metadata `S=3^(2^27)`. The final packages correct that descriptive declaration to the intended specialization `S=3^(2^26)`. Residuals and polynomial identities are formal in the fixed coefficient S. The replay checks the precise two declarations and permits no other compiled-source difference. S is not a coordinate. The ordinary-coefficient versions impose its value through 17 uniquely determined coordinates.

`builders/` contains the prior builder and both final standalone builders. `patches/` contains all new architecture transformations, their original driver scripts, and a pure-function adapter of the asymmetric driver. `tools/` contains the pinned upstream compiler and independent checker. `sources/` contains the exact source text whose hash the builders record. `expected/` contains the final packages' frozen compiled precursors. `PROVENANCE.json` records repository commits and original file locations.

`receipts/` records a successful complete replay including all four final quartics, and a separate successful replay after copying this directory into a fresh location.

These are algebraic reproducibility checks. The number-theoretic reasons that the new source systems define the integers are supplied separately in the proof documents. This directory makes no independent claim to prove those arithmetic arguments.
