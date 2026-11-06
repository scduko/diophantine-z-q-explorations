# Seven products for the three full-mode powers

The full private-conic batch uses r^2, r^24 and r^80. Its recursive source
emitter constructs eleven powers, with exponents

    2, 3, 6, 12, 24, 4, 5, 10, 20, 40, 80.

The emitter's exponent metadata omits the temporary exponent 4 when it
overwrites the entry for exponent 5. The producer therefore includes all
allocations labelled as contact powers, then independently reconstructs
their current exponents from exact two-term product definitions. It does
not infer the complete circuit from that metadata list alone.

Replace that internal circuit by

    r2  = r*r,
    r4  = r2*r2,
    r8  = r4*r4,
    r16 = r8*r8,
    r24 = r16*r8,
    r40 = r24*r16,
    r80 = r40*r40.

The output coordinates for exponents 2, 24 and 80 are retained. All four
other new targets are fresh. Each equation is quadratic with coefficients
1 and -1. Each old non-output target must occur only in the selected old
defining rows. The producer checks current rows and complete incidence;
source metadata alone is never enough to authorize a replacement.

For either direction, preserve r and every outside coordinate. Each old
or new internal coordinate is uniquely its displayed power of r. Thus the
two circuits have identical retained outputs for every rational r,
including r=0. No division, sign choice, square-root extraction or conic
nonzero proof is needed. The existing `circuit` certificate rule verifies
acyclic definitions, privacy, fresh targets and exact polynomial output
identities independently of the producer.

There are four fewer active coordinates per qualifying full-mode batch.
The 13 full-mode source occurrences give an upper potential of 52 removals;
this is not a measured endpoint saving. Later cleanup can alter definitions
or expose outside uses, in which case the producer skips the occurrence.
Among multiplication-only power chains beginning with r, seven operations
are also necessary to reach exponent 80, since six multiplications cannot
exceed exponent 64. This observation does not rule out other algebraic
representations using the conic or divisions.

`power_chain.py` uses exact entry/checker/certificate pins and hash-bound
module/map metadata. Without `--output` it only reports structurally valid
plans. An exporting run computes the complete current sum of squares,
checks each exact coefficient change against 2^80, and emits ordinary
`circuit` events. Full named-source replay remains mandatory. The tiny test
replayed both circuits with the existing independent checker: 12 total
variables before, 8 after, and five malformed cases rejected.

This producer is independent of the new `nonsquare_product` proof branch
in the neighboring experiment. Its only polynomial-helper imports from
`probe_localized.py` are unchanged arithmetic and encoding functions.
