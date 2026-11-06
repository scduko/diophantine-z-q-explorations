# First-norm fusion helper review

Verdict: PASS for the three-module emitter and independent restoration
helper at the hashes below. The combined source locators, arithmetic
contract binding, flattening and endpoint replay remain separate gates.

| File in batching/sub5000/first-norm-fusion | SHA-256 |
| --- | --- |
| first_norm.py | badaa92471df68d9250f77d8584fee0eecafd8641d3873ab0f8babbf0d1d7438 |
| audit_first_norm.py | 5e13e16621f5de043a5bb63d069f91fbab7b6284e19c4f077b093746efa2a2a5 |
| test_source.py | e63a0ef152d0c9442330430d881e6c9f22b00230d9dd0355f8ad1147af7d9822 |
| PROOF.md | b18b32854d4ef6e8c49495ce404f7c96566a0a1926baca6f4ee1ed4cbedcba05 |
| CONTRACT.json | b327fcc99625f09c36509c6b22cb12edc4fdeb40c2f8a7b70f65f2509c75570c |

The emitter changes exactly the first field's packed-numerator row and
the first node after the literal-one leaf. With T=2AY-A^2+2B^2, those rows
become T-2AY+A^2-2B^2=0 and rN-r-T^2=0. Their degree is at most two.
It checks the old row forms and that the old W coordinate occurs only in
these two rows, with no call use. It retains N, all of its consumers, the
conic, powers, other fields and the pole call.

The independent helper checks the exact new row forms, coordinate and
row bounds, the literal-one/field-zero tree pair, field order one and
all changed metadata keys. It checks complete numerator incidence,
restores precisely the four changed construction labels and requires
each event exactly once. It then restores the old specification and
passes every module to the required full parent checker. The parent
check is essential to establish the field-zero H.f interface, r^2 power,
unchanged conic, higher nodes, shared-square channel and all other rows.
It must be wired to the pinned checker and must raise on any failure;
Boolean predicates are rejected.

The source typing is explicit. The first leaf is conic_first_numerator,
with norm=null, numerator=T, power=0 and virtual denominator exponent one.
The coordinate is not an ordinary normalized norm W. The new fused node
label also prevents treating rN-r-T^2 as an acyclic polynomial definition
of N with a constant coefficient. A source locator must retain these
distinctions. Any ordinary r^2*W rule must skip this field or use a checked
numerator-specific case; it must never manufacture r^2*T=T_numerator.

This restoration is a source-specification check, not a fixed-witness
equivalence to the original denominator-r^2 source. The arithmetic proof
justifies the new denominator r. Within that virtual source the maps
T=rW and W=T/r are exact because the unchanged rational conic forces
r nonzero. No division by T or N is used, so their zero cases remain.
The separate Parity arithmetic review owns the valuation and completeness
argument. The combined source must bind it explicitly.

I ran the supplied bounded tests on the actual general-root-shared-square
module dictionaries. Complete restoration passed, as did 87 semantic
mutations, four resource-abort cases and two Boolean-callback rejections.
The exact identity suite also passed, including the isolated r=0
counterexample. No source was generated or flattened. The helper's
iterative JSON bound runs before copying, and resource exceptions are
not counted as semantic rejection.

No additional source coordinates or rows are removed. The proposed gain
comes from replacing one cubic node by a quadratic node per occurrence.
The old lift-product survival census supports investigating that gain,
but a new final variable count requires the composed replay. This review
does not claim that all existing cleanup, especially G-square reuse of
the first field, has already been adapted.
