# Shared-square implementation review

Verdict: PASS for the emitter and independent restoration helper at the
hashes below. Acceptance requires the documented complete parent callback,
the outer source and flattening audit, and the final quartic replay. This
review does not accept a new full source or predict its endpoint count.

| File | SHA-256 |
| --- | --- |
| source-pipeline/sub5000/shared-square-next/shared_square.py | 5a4b325c86255beb9f6271b0638822656c31ce46b8fa67997629ecd3e8887c73 |
| batching/sub5000/field-bookkeeping/audit_shared_square.py | 2e7498a05baad8996341ce7c87c839683a6f196a2682167a731fd329f9101fba |
| batching/sub5000/field-bookkeeping/shared_square_cases.py | 42b33b7506998584b53d7ca7a6f309a1a8846c3d464cb9e620cabc5fe1c1cc7a |
| batching/sub5000/field-bookkeeping/test_shared_square_resources.py | 0c559035397a5b18c921e179fde7b157a8c906452c561e8571b17174cba58ccd |
| test_composition.py | 483b97ecc0ed048ed411f9f437ebdf924ac0069dadf4af9a6bc94a3fae7d66e6 |
| COMPOSITION_TEST.json | 712d7d92f0e5b94e86a0ce1ba41eb115cf36990bf2cbb0a40add56b37627f248 |

The proof and source-contract review is separately bound in
`../half-generator-review/SHARED_SQUARE_REVIEW.md`. The implementation
retains the original field F=A+B sqrt(2), its order-one test and its W.
It computes C=A^2+2B^2 and D=2AB once and replaces each old evaluation
Y=A+theta B by the same norm numerator C+theta D. The reverse assignment
of each Y uses that contact's own theta. No division or nonzero premise
is introduced, and all zero branches remain valid.

The root helper checks the exact two new definitions and four terminal
construction events. Both new coordinates must have no old-row use, and
only the designated two slots of each of the 37 comparison calls may use
them. It checks the 13/8/16 multiplicities, restores the original pair in
every call and removes just those definitions. The complete parent callback
then establishes that this pair is actually the original conjugate f(J),
not merely a pair asserted by metadata. Coherently changing that pair is
covered by a negative test.

Each comparator must have no residual use of its retyped free pair, and
each component must appear exactly once in its one batch call. The helper
checks the explicit pre-squared type, original order and field index.
Restoration changes the single layout token back and preserves every
other comparator field. This prevents silently treating F^2 as a new
ordinary field test or squaring the coefficients a second time.

The batch restoration checks the exact new norm row, r^2 power, W position
and agreement between the field record and tree leaf. It inserts the old
Y and its equation, replaces the norm equation and uniformly restores all
subsequent variable and equation indices. It remaps conic data, calls,
contact powers, field records, the full norm tree and pole inputs. The
parent callback checks the complete restored object, so extra content and
changes to non-designated fields cannot disappear during restoration.
The literal-one leaf and the original W/tree/pole interface are preserved.

I found one resource issue in the initial helper: bounds on outer list
lengths did not bound nested data before copying. The reviewed version
adds an iterative JSON preflight over the entire dictionary and each
public restore entry point. It bounds nodes, depth, containers, strings
and integer size before deepcopy or canonical serialization. Its dedicated
RuntimeError propagates through the mutation runner. Boolean-returning
parent predicates are also rejected; a real parent checker must raise on
failure and return a report or None on success. The caller must wire that
checker directly, not accept an arbitrary user-selected callback.

I tested composition on the actual normalized-linear-pole-result module
dictionaries. First the independent literal root specification produced
the four changed root/comparison modules. Then the shared-square emitter
ran in memory. The restoration helper recovered every module exactly.
The new common pair is [118,140], the square pair is [259,260], and the
new root definition rows are 243 and 244. The combined root has 260 locals.
The report pins every original module hash.

All 109 semantic mutation cases rejected, the boolean callback fixture
rejected, and all five resource-abort tests passed under CPython 3.14 with
-E -B. This used only small dictionaries, without source generation,
flattening, lifting or polynomial expansion. The exact source-coordinate
delta for this isolated rewrite is minus 35. The final endpoint saving
and coefficient bound still require the complete remote pipeline.
