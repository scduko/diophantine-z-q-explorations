# Four-field rational-difference implementation review

Static verdict: PASS for the local emitter and independent module
specification listed here, conditional on the separate arithmetic review
and the outer source adapter. No source generation or endpoint replay ran
locally. This review does not approve a new source by changing an old pin.

Reviewed files under charts/sub5000:

* rational_difference.py: be766e35b06d8f334c326dedfddc7c200d226a4c70af6a73fe66242aa4ccc898
* audit_rational_difference.py: 206443f19e4c54d94c6d27c003cfbe56e1030f21df12ab0bf6fc675367a09270
* test_source.py: 05dc96b6c4eab21d5b3956069a9b8cd87674b79577062855353bfcef425bbcaa

The producer emits exactly t=fF, M*(1+D*t)=p,
T=2*x-p*q+2*M*(q-p), and A*conjugate(T)+conjugate(q-p)*h=0.
All four pairs are quadratic. It retains the primary curve and inverse
rows, G equations and profiles, root target coordinates, common point J
and inverse, contact dispatch, anchor and height module. The original
batch constructor is explicitly passed and checked; the replacement
comparison constructor generates only the three intended reduced batches.
The old difference constructor is disabled.

The helper independently reconstructs the same four equations without
importing the producer. It reconstructs every ordered test and checks all
core rows, definitions, calls and local-coordinate coverage. The retained
root is reconstructed against the pinned high40 root in the same manner
as the earlier minimal-Jacobi helper. The old q_batch41 is not silently
retained: the exact module set is q_batch31, q_batch13 and q_batch25 plus
the three comparisons and four common modules. The three new norm trees
are checked against their exact order lists by the independent core.

For n modeled indices, the field list consists of n+2 formal tests, n
primary ratio tests and n+1 alternate tests. Therefore it contains 3*n+3
field tests and 6*n+7 rational tests including the root error. The full,
beta and Lucas cases have 15, 6 and 12 bottom pairs. Across 13/8/16
instances, the exact count is 435 pairs and 37 batches. It is not 870:
the two rational components of one field test make one bottom pair.

The 47 malformed cases check each new equation family, the primary curve
and inverse, G coupling, three kinds of ordered test arguments, extra
calls, prohibited metadata, root target order and root metadata. They
require exact rejection checkpoints and do not catch the separate core
resource exception. The outer adapter should retain its existing root
inverse, extra-content, flat-row/map and named-source binding tests. The
module suite alone does not claim to cover those outer obligations.

The local nonvanishing argument is consistent with the retained equations:
global nonzero G forces p nonzero; M*B=p forces B nonzero; T=0 in the fused
row forces q=p because h is a unit. The curve then gives (x-a)*B=0, so
P=Q, while T=(x^2+D)/x is nonzero. This also includes identity differences.
Deleting square membership and difference formal tests is a genuine
arithmetic change. The required half-index and torsion-neighborhood
arguments are outside this finite implementation verdict and must remain
attached to the new source's acceptance.

No change was made to the reviewed files or any frozen source.
