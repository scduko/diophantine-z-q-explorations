# Version 3 theorem and source inventory

This inventory binds [the current manuscript](../../quartic_9625.tex) to the
[9,625-variable package](../../quartics/quartic-9625/README.md). The polynomial
has 9,624 rational witnesses, 9,161 quadratic residuals, 82,476 collected
monomials and degree four. Its arithmetic source uses height exponent 19,
37 raw contacts, 29 full comparisons and eight beta-only comparisons, with
high precision 40, beta precision 12, anchor 25 and scalar precision 32.

[Theorem applications](theorem-applications.json) records 11 current arithmetic
lemmas, 13 retained algebraic lemmas, ten inherited application groups and
four explicit published-application groups. The latter include the determinant,
intermediate modular quotient, Belyi-height and isogeny-height applications.
[The dependency closure](dependency-closure.json) records all 74 directed edges.
[Publication additions](publication-additions.json) preserves the exact reviewed
statements, source locators, conventions and qualifications.

[The historical bridge](baseline-bridge.json) transports only unchanged text
from the original reviewed manuscript. Historical review files and their hashes
are unchanged. New height and selective-source claims have their own current
bindings; earlier reviews are not relabeled as reviews of those claims.

The [original reviewed arithmetic patch](reviewed-arithmetic-patch.tex) remains
byte-for-byte frozen. [The layout record](layout-transform.json) permits one
explicit display split, including removal of its leading spacing command.
The validator compares the entire resulting arithmetic body with the current
manuscript. It does not ignore arbitrary whitespace or mathematical edits.

From the repository root:

```text
python -E -B docs/quartic-9625/validate.py --repo . --output build/quartic-9625-inventory.json
python -E -B docs/quartic-9625/test_inventory.py --repo . --report build/quartic-9625-inventory-negative.json
```

The checked [validation receipt](VALIDATION.json) and
[14-case negative-test receipt](VALIDATION-NEGATIVE.json) concern metadata,
dependency closure, exact text and source/artifact hashes. They do not prove
the arithmetic theorems or replace the package's independent source audit and
full certificate/expansion replay.

To refresh line locations after an approved manuscript layout change, using
only evidence already included in this repository:

```text
python -E -B docs/quartic-9625/build_inventory.py --repo . --registry docs/quartic-9625/publication-additions.json --out docs/quartic-9625
python -E -B docs/quartic-9625/validate.py --repo . --output docs/quartic-9625/VALIDATION.json
```

Refresh fails if the reviewed arithmetic body changes beyond the explicitly
listed layout operation, if an inherited application excerpt changes, or if
the source or certificate differs from the fixed Version 3 target. It cannot
approve a new proof by updating its hash.
