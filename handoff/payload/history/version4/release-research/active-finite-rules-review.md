# Review of the active finite rules

Reviewed on 2026-11-06 against `verify_certificate.py` SHA-256
`b7180b01029b3d9364d94914401a4f1f66b190762f10b99a38e9fd4f49437ffe`.
This review covers the six active rule families. It does not accept unused
handlers, establish the source arithmetic theorem, or replace full replay.

The linear rule replaces one row by a nonzero integer multiple of itself plus
an integer multiple of a distinct retained row. Solving back divides only by
the recorded nonzero integer. The elimination rule checks a nonzero constant
definition of a non-input coordinate and substitutes into every occurrence.
Its occurrence set is compared to the current incidence map. The shear rule
uses a distinct coordinate and has coefficient one on the changed coordinate;
its inverse changes the sign of the recorded rational shear. It also checks
the complete current occurrence set. These implement the corresponding
projection arguments in the retained `ALGEBRA.md`.

The embedded relation handler, SHA-256
`9db4bf4ac1501697dee6cc48e76af2cbe181f5b404a7096dcc08c9819f88c52b`,
checks the defining row v - N, rejects v = input0, and visits exactly every
affected row. Support rows must be unchanged, nonzero and v-free. It forms
F(N) minus the sum of the supplied support multiples in exact rational
arithmetic, and requires the result to be quadratic and v-free. The outer
patch checker compares the supplied replacement to this result up to nonzero
rational scale. Thus restriction and extension by v = N give both directions.
No nonconstant denominator or unit-cancellation rule is used by these events.

The circuit handler retains the specified boundary outputs, checks every
outside use of a deleted internal coordinate, and allocates every other new
target freshly. Both old and new definitions are acyclic constant-pivot
quadratics in the same external coordinates. It evaluates them as exact
polynomials and compares corresponding outputs. Its cache key includes the
complete normalized definitions and output order. The recorded contact-power
replacement uses r^2, r^24 and r^80; the seven displayed product definitions
give these powers also at r = 0. The existing power-selector reviews cover
the source locators separately.

The embedded parity handler, SHA-256
`dd43bdbe277ec4de10e0e5ad472cc5f54ef7f2408f99b80e70ce1b852a8f020f`,
compares the four expanded old equations against its fixed source equations,
checks privacy of the old seven witnesses and deleted lift coordinates, and
requires twelve fresh replacement coordinates. Its nine replacement rows
match the retained parity proof. In the forward map 1 + b t^2 cannot vanish,
because the old first equation would then imply b = 0. In the reverse map
b = 0 forces u = 0. For b != 0, either t = v/(u+b), or the exceptional
u = -b, v = 0 branch permits U = b, t = 0. Both retain U^2, which is all the
other rows consume. No division by b, e, h or s is used. This is equality of
existential projections, not a bijection of all private witness tuples.

The outer checker updates incidence after every patch, retains the original
input during compaction, compares the final residual file and positive
weights, and expands all ordered products of residual terms. It compares
every collected coefficient with the supplied monomial table, checks degree
four and the strict coefficient bound, and checks the active variable set.
Its assertion guard rejects optimized Python execution. The reported full
replay remains separate evidence that this exact certificate satisfies all
these checks.

Disposition: the inspected active handlers implement the stated finite
solution maps. Root inspected the outer handlers and AST-extracted embedded
parity and relation code; no generator or polynomial expansion ran locally.
