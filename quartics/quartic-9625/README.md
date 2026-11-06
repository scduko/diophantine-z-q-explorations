# The 9,625-variable quartic

This Version 3 artifact has **9,625 rational variables**, including input0,
9,624 witnesses, degree four, and 82,476 nonzero monomials. Its 9,161
quadratic residuals produce a sum of squares whose largest absolute
coefficient is **685783949153203534233601**, strictly below 2^80.

The expanded polynomial is [polynomial.expanded.txt](polynomial.expanded.txt).
Its SHA256 is
`6d67d45f3d615b7fd2242e3a9404dd9f5da570fc711a29ebe77f613e80ebbf99`.
The original complete verification receipt is
[evidence/stages/coordinates.json](evidence/stages/coordinates.json).

The named source is
`selective-beta-k40-q12-a25-h19-s32-d68d86cdf995`: the selective-beta source
with 37 contacts, height exponent 19, high precision 40, beta precision 12,
anchor 25 and scalar order 32. [source-entry.json](source-entry.json),
[source-audit.json](source-audit.json), and
[construction-map.json](construction-map.json) bind its exact source and
compiler files. The finite checks establish equivalence to that fixed
source and the complete integer expansion; the arithmetic theorem is the
separate mathematical claim in the Version 3 manuscript.

From this directory, reproduce the artifact on Linux with a fresh output
directory outside this package:

```sh
python -E -B reproducibility/run.py --output /path/to/fresh-output --stage-seconds 180
```

See [the reproduction guide](reproducibility/README.md) for the compatible
Python/gzip environment, resource limits and exact checks. The package is
immutable: the runner writes to the selected output directory. Standalone
use of [verify_certificate.py](verify_certificate.py) should target a copy,
because it writes a verification receipt into its argument directory.
