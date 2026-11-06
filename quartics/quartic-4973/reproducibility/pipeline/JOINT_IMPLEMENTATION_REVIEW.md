# Joint chart and conic composition: independent review

Static review: PASS for the files below. This covers the joint chart's
equations, rational reconstruction, module-level implementation and conic
composition. Full source generation, the 59 source mutations, flattening,
the reduction pipeline and the final coefficient bound remain remote
execution obligations. The 830-coordinate saving is an allocation estimate,
not a measured endpoint reduction.

## Exact files reviewed

Paths are relative to `work/quartic-sub10000-20261106/`.

| File | SHA256 |
| --- | --- |
| `charts/sub5000/next-interface/joint-chart/PROOF.md` | `947b505969ee3b6f1c8677e452703454adac6933c2bb01bbb54ab4b27b5e7451` |
| `charts/sub5000/next-interface/joint-chart/joint_chart.py` | `f6868d7fc6f6898388288d4f088966220158e888aa47def53cd21c599ef7ff85` |
| `charts/sub5000/next-interface/joint-chart/audit_joint_chart.py` | `12893b64a3e72363fa359c0981641baaeaecad1cf4297bab2df5af1906cfda85` |
| `charts/sub5000/next-interface/joint-chart/audit_joint_conic.py` | `0c304cc799563ce26631ee5969d96afadc564be8ac502bb676e618e0320ab907` |
| `charts/sub5000/next-interface/joint-chart/test_conic_source.py` | `2e374076fa453fd5b6db1fb6811fe0397749f5611b119e658900ec6ac1ea5595` |
| `precision/sub5000/conic_emitter_joint.py` | `ab04ab979b8c239a89b7e129fd53031587438943efac266f6b9fc28040b7b4f1` |

The delegated conic checker must remain the independently reviewed
`audit_conic_source.py` with SHA256
`0358e595147d8e840093b5f1a73e01c710f7c8bc0a7235f2d94611792c0b2baa`.
The optional anchor callback must be the independently reviewed, pinned
anchor-four checker. The outer auditor must pin these callbacks and its
baseline; the helper intentionally does not establish their provenance.

## Mathematical checks

Write `E` for the second joint equation and `E2` for the third. After
`K=(A-r)p`, `x=p^2+Df`, `r=J/q`, `s=c/q`, `t=q^-2`, and `u=rs`, direct
expansion gives `E1=2E+E2`. The combinations `q(E1+E2)/2` and
`q^2(E1-E2)/2` are exactly the two displayed graph equations. All
operations are reversible because the retained target and shared inverse
give nonzero `q` and `J`.

The graph eliminant, using only `c^2-q^4=4D`, is
`-4Dq^2(fp^2+Df^2-1)`. Thus the source's three equations force the deleted
curve equation and `xf=1`. The unchanged G equations supply the existing
nonvanishing argument for `p`. No assumption that a private primary is
already in `2E(K)` enters this recovery.

The common-denominator zeros are the two genuine nonzero two-torsion
differences. They cannot satisfy the graph equations: their `H2` is
nonzero, since `q^4=4D` would imply `N(q)^2=28`. Identity and the difference
`(0,0)` have `A=0` and are retained; opposite configurations use the second
denominator. No division by a private chart coordinate or a difference
index is used. The expanded domain therefore needs the stated half-index
arithmetic argument, including the zero difference case. It is not an
equivalence of every private tuple with the earlier open chart.

Literal functions tested by the norm layer remain the same `f`, primary
ratio and alternate `A`. Consequently the separately reviewed conic
arithmetic theorem applies to the same arbitrary field values. Its
nonvanishing and approximation premises are unchanged by these rational
reconstructions.

## Source and incidence checks

The emitter and both auditors conjugate `f,p,D,q` consistently with
`A=conj(z(P-Q))*jz`. Root construction retains the old target reciprocals
and ordinate ratios, adds exactly the four shared coefficient pairs per
target, then applies the same 13 full / 8 beta / 16 Lucas selection.
Every retained root field and row is compared with independently built
expected content. The old target boundary is replaced by `(r,q)` and
the appended boundary contains `(s,t,u)` in the same selected target
order. There are 60 added rational root coordinates in total relative
to the original affine target interface, of which 40 belong to this
joint-chart change.

The new free counts are 61/28/50. Legacy boundary counts remain
31/16/26, and the ignored old theta/error slots remain respectively
28/29, 13/14 and 23/24. The composite auditor checks these fixed slots;
it does not infer them from the enlarged free count. Raw conic contact
slots likewise remain 30/15/25. Every raw row, arithmetic definition and
ordered conic argument is checked for unwanted old-root dependence.

Private core coordinates are only `f,p,A,K`, plus the retained logarithm
coordinates. Exact core-row comparison, arithmetic substitution,
all-coordinate coverage and exact ordered calls exclude a hidden use of
the removed primary `x`. The raw field orders are reconstructed for
each mode and passed to the independent conic batch checker. Retained
height and parity modules are compared literally; the actual anchor
module goes to the independently pinned callback.

Bounded AST comparisons passed: standalone and composite `check_root`
are identical; the original and joint conic emitter's
`make_conic_batch` are identical. The conic boundary hook checks the
legacy theta/error inputs before removing their temporary call slot,
suppresses only the two explicitly unreachable old small batches and
rejects any remaining old-batch caller.

## Tests and remaining execution

I independently ran `test_joint_chart.py` with `-E -B`. It passed seven
exact symbolic identities, 34 valid field examples including all four
exceptional configurations, two genuine pole exclusions, and the six
joint component rows' degree-two/max-coefficient-88 check. Five reviewed
Python files parsed successfully. These are small algebra and syntax
checks, not a source-generation run.

Static review found one mutation fixture defect: nine argument mutations
left `conic_field_inputs` stale and therefore stopped at the metadata
check. The final test file above repairs each fixture's metadata so its
required failure is the actual `Ordered argument` assertion. The suite
has 59 distinct cases, exact expected rejection checkpoints and a final
deadline check. Its `except AssertionError` does not catch the pinned
core's separate resource-abort exception. It still must be executed
against the emitted source. Full conic-batch and anchor mutations belong
to their separate suites and must also run; these 59 cases do not replace
them.

The outer wrapper remains responsible for exact compiler/baseline pins,
the complete generated module set, all flattening and construction-map
rows, fresh source identity, the finite lift and final coefficient audit.
This review does not authorize acceptance by replacing an old source
hash or by reporting only matching counts.
