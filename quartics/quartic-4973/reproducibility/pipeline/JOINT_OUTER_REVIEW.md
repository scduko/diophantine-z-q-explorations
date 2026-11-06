# Joint chart outer integration review

Static review passes for the five integration files below. No blocking
source, mapping or locator issue was found. This review is separate from
the earlier joint-chart helper and arithmetic reviews. No new source or
certificate was generated or executed by this reviewer.

The files are in `source-pipeline/sub5000/joint-chart-conic/`.

| File | SHA-256 |
| --- | --- |
| check_source.py | eb133736af4735cfbea53284c7042376cc74efa059354187fdff6898c932a453 |
| build_source.py | a0803272e210470c8a03d28f3e989d1a51ec47034b4f8b293e84372ea0e334f8 |
| source_layout.py | 389f40f01fee7ca067292107971fc9eb05c86d07575f42adb4f991b045f3ef9e |
| test_conic_locators.py | e922a865b89511f5d0a3d0d090475b3e89063f5daf43d1663e251c43690b8150 |
| test_conic_batches.py | 1eb0cec980d46d0caf4042c19d50290c0d124ec6d0960df41ece0755e1b68cb3 |

The producer regenerates all six pinned high40 baseline modules before
using a fresh builder. Its installation order preserves the captured
archive batch constructor, installs the joint chart before the conic
adapter, and then applies the independent anchor change. The emitted
contract names the new source, exact field orders and mode positions,
61/28/50 free counts, old 31/16/26 prefixes and 40 new target coordinates.

The outer auditor binds the exact joint, conic and anchor checker hashes.
It reconstructs all modules through those independent checkers. The
generic flattened-stream checker is taken from pinned core bytes; the
only textual replacement is its exact module-instance-count assertion,
and the wrapper requires exactly one occurrence. The expected count is
13 full, 8 beta, 16 Lucas and 38 parity instances. The checked source file
hashes and construction-map digest are carried into the report. Both
source contracts are checked against fixed hashes. The report correctly
keeps arithmetic acceptance and the final quartic bound separate.

The locator checks the enlarged free counts while retaining old-prefix
theta/error/raw positions. It rejects a legacy root input in a conic
call and checks that the raw contact is at legacy-1. It requires the
joint-chart flags, forbids old abscissa guards, and records conic fields
from the audited module metadata. These are producer hints, not standalone
proofs of rewrite validity. The full source/map audit precedes them, and
each later algebraic event still needs actual-row and incidence checking.
This division is explicit in the file and is sound for this integration.

The locator mutations target all new arity, prefix and model checks. The
batch harness pins the frozen conic test file and independent batch
checker, reruns all 60 batch mutations plus the anchor mutation, and
checks that a resource abort cannot count as a semantic rejection.
The two harnesses do not substitute for the forthcoming complete new
source audit, malformed-module tests, lift and endpoint replay.
