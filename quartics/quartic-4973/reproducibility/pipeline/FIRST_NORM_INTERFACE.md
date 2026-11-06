# Integration contract

The files in this directory are a separate proposed source change. Do not
modify a frozen packet or reuse its source identifier. The mathematical
proof is PROOF.md; CONTRACT.json states its scope. Parity's independent
review is `parity/sub5000/first-norm-fusion-review/REVIEW.md`, SHA-256
`0208bf985c72d24e83863bb8b305b552b56c5fb9c5b6e9953c0df8b32ac0ef72`.

`first_norm.postprocess_modules(modules)` returns a fresh module dictionary
and a receipt. It runs after the selected root/shared-square postprocessors
and before writing or flattening the modules. It changes only q_conic13,
q_conic6 and q_conic10. The caller first verifies the entire selected parent,
including the root/comparator field-zero mapping to H.f. This helper does
not authorize unverified input modules.

There are no variable or row insertions/deletions. The first field's old
normalized-norm coordinate becomes its unnormalized numerator T. Both its
`field_bindings` entry and its `norm_tree` entry become

    type = "conic_first_numerator"
    norm = null
    numerator = the retained coordinate ID
    power = 0                     # raw contact input r
    virtual_denominator_exponent = 1

All original field/order/input/evaluation values remain. The additional
`first_norm_fusion` record binds the numerator ID, first node ID, the two
changed rows, original r-squared coordinate, field role and denominator.
The new labels are `first conic field numerator` and `fused first norm node`.
The second label must not be treated as an acyclic polynomial definition
of N, whose coefficient in r*N-r-T^2 is the variable r.

`audit_first_norm.check_modules(new_modules, parent_check)` first checks
these exact rows, types, labels and numerator privacy, then restores the
old specification and invokes the required complete parent checker. The
callback must raise on failure; Boolean callbacks are rejected. This
restoration proves the source construction is exactly the declared delta.
It is not a claimed old-witness equivalence across the denominator change.
The proof's separate arithmetic argument supplies that part.

The parent checker must be digest-bound and must validate every restored
module, including the conic, field-zero order/role, all power definitions,
all higher tree rows, shared-square typing and all root/call arguments.
Outer checks still bind every compiler input, fresh flattening and map,
module set, counts, and all metadata. Run the independent restoration before
the whole-source flattening check, as in the other source postprocessors.

## Locator and reduction consumers

This first entry is not an ordinary normalized norm coordinate. A locator
must emit its `numerator`, `virtual_denominator_exponent=1` and `first_node`,
and keep `norm=null`. It must reject the old ordinary-norm interpretation.
Any ordinary norm rule requiring P*W=eval(F^2) must skip this record. In
particular, never manufacture r^2*T=eval(F^2).

G-square reuse remains possible directly against

    T = 2*A*Y-A^2+2*B^2 = eval_theta(F^2).

It can remove Y using the same retained G-power identities, with a numerator
output instead of P*W. A generic exact retained-row checker can verify this
without a new proof rule. A producer that relies on ordinary field metadata
needs a dedicated numerator case or should skip it. The other 108 primary
occurrences are unchanged; the 37 first occurrences are included in the
original total of 145, not an additional family. A skipped optimization
could erase the hoped-for net gain, so check this explicitly in a new run.

All later node IDs and every consumer of the first node remain unchanged.
The ordinary linear-pole call still receives the actual upper norm root.
The scalar-height module is unchanged. Target-four, target-two and tangent
root changes do not alter this local boundary, but any combined packet must
bind its selected variant exactly.

## Bounded local checks

Run Python with `-E -B`:

    test_identities.py
    test_source.py --modules PATH/TO/SELECTED/source/modules --report module-tests.json
    census.py --source PATH/TO/SELECTED/source --map construction-map.json \
      --initial-certificate fresh-lift/certificate.jsonl.gz \
      --final-map FINAL/variable-map.json --report census.json

The identity test includes the intentionally invalid isolated r=0 case.
The module test restores complete existing module dictionaries, exercises
87 semantic mutations, four resource aborts and two invalid callback forms.
It performs no flattening, source generation, SOS expansion or replay.

The saved census uses the existing normalized-ten source and final power
endpoint. It locates all 37 first-node lift products and finds all 37 still
live. The recorded lift uses r*W products rather than W^2 products; either
choice disappears from the fused quadratic source. The census is evidence
for the target's survival, not a measured new-source reduction.
