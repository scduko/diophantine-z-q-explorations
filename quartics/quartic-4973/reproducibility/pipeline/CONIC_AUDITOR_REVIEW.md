# Independent review of the conic module auditor

Date: 2026-11-06. PASS for static correspondence of the frozen module auditor and mutation suite to `JOINT_SOURCE_CONTRACT.json`. No remaining static blocker was found. This does not replace execution on the complete emitted source, the outer source/flattening audit, or certificate replay.

The reviewed files are `batching/sub5000/conic-audit/audit_conic_source.py`, SHA-256 `0358e595147d8e840093b5f1a73e01c710f7c8bc0a7235f2d94611792c0b2baa`, and `test_conic_source.py`, SHA-256 `e022d97f11399d12fdbf0c2e70b90f4a29d386c2b0f007faea5f50bbed5ec0c8`. I also read its integration contract and the pinned core Module parser, polynomial operations and independent G coefficient construction. No source generator, mutation suite, or heavy computation was run by this reviewer.

## Module and field correspondence

The helper imports no producer. It uses the fixed core `0da0dfef661211fd4ada262050895ef24ca54dfdc1aca4aa4bec4e69c1dcbce8`, which validates consecutive unique variable allocations, complete ordered equation logs, index ranges, and acyclic definitions with nonzero rational leading coefficients. It expands definitions exactly and applies resource limits separately from semantic rejection.

The comparison audit reconstructs all primary inverse/curve equations, four-field difference equations, G outputs, common denominator and ratio equations. The G coefficients come from the independent finite series construction rather than the producer recurrence. The primary, common-J, proxy-error and alternate fields have the exact roles and orders in the joint contract, with 15, 6 and 12 fields for the three modes.

The input layouts are the retained 31/16/26 boundaries with F,q targets. The helper derives their target slots and common-J slots explicitly, verifies every ordered coefficient pair in the conic call, checks the exact raw-contact argument, and confirms the conic-field-input metadata. It does not merely count arguments. The root checker reconstructs all 37 calls from the pinned old high40 root and uses the exact 13/8/16 position selections, including all eight unchanged affine height coefficients and the five shared target extensions.

Old theta and epsilon are forbidden in every comparison residual, every expanded arithmetic definition and every conic argument. Their only remaining uses are therefore the unchanged root graph and ignored free interface positions. This matches the joint proof's harmless-auxiliary interpretation. The new field-coefficient binding rows must be affine.

During review, an earlier read showed the core-label check excluding only `arithmetic` even though it allowed `conic field coefficient` definitions. That would have rejected valid outputs. The final bytes above exclude both labels and add the affine-binding check. I reread the final content and hash together after the concurrent fix. This issue is closed in the reviewed hash.

## Conic and tree reconstruction

Each conic batch has exactly r and the expected rational coefficient pairs as free inputs. Its three private coordinates must be its first three local allocations, with the two conic rows exactly in positions zero and one. The helper verifies S=s^2 and theta^2-rS=2 as quadratic equations.

It reconstructs the deterministic contact-power schedule, including common-expression reuse of repeated powers, and checks each power definition literally. It also checks the expanded power is exactly r^(2e) at each field node. It therefore does not trust a power label or exponent in metadata without checking the equation.

For every field it checks the quadratic evaluation row Y=A+theta B and the packed row r^(2e)W=2AY-A^2+2B^2. The schedule is the stable increasing-order schedule in the contract. It reconstructs the complete upper tree from literal1 and those nodes, including every carry and every N_r(a,b)=a^2+r*b^2 row. It checks the root square and the one exact pole call on r times that square. All rows must be consumed, all local coordinates must have a recognized role, and all conic metadata must match the reconstruction. No contact inverse or old epsilon leaf can be hidden as an extra row or coordinate.

The helper checks conic/evaluation/power rows have degree at most two and upper norm rows at most three. The higher-degree source still needs the separate fresh quadratic lift. These degree checks do not misrepresent the upper source tree as already quadratic.

The full module set is exactly the ten names in the joint contract. The scalar-height and parity modules must equal their pinned old versions. For this source family the outer wrapper must pass the independent four-witness anchor callback, pinned to `0e5f93f61114f9bd6589dc950271938b5d630820a920565043f63ab749081e30`. The callback checks the actual new module; the helper does not replace it with an old anchor before validation. Omitting the callback permits only the old byte-identical anchor and therefore would reject this new four-witness module.

## Mutation coverage and execution boundary

The complete suite has 83 semantic mutations, or 84 with the four-witness anchor callback. The earlier count of 60 covers only its three sets of batch mutations. The complete set additionally tests raw comparison arguments, old-theta capture, field reordering, primary/G equations, ignored-root metadata, root contact sharing, shared-target equations and the anchor.

Batch mutations cover both conic equations, packed/evaluation signs, upper norms, final square and pole argument, wrong raw factor, wrong normalization power, a missing field constraint, reordered input/power metadata, lost literal1, boundary capture, extra calls, old leaves, and extra constraints. Each test requires the exact expected assertion checkpoint. It counts only AssertionError with the expected payload as rejection. An explicit resource-abort regression proves a resource exception is propagated rather than credited as a rejected malformed source. Unexpected program exceptions also escape.

The suite first requires a positive check of all actual modules, so a checker that rejects every input cannot pass it. Its baseline module and core/anchor hashes are fixed. It reports its actual auditor and test hashes; external authentication of those files remains the outer wrapper's obligation. The author reports isolated batch execution, but this review asserts only static inspection; the complete positive path and 83/84 cases require the dispatched run.

## Required outer checks

The helper explicitly does not authenticate the source manifest or compiler package, establish the canonical source digest, reconstruct the complete flattened stream/map, or prove separate conic allocations across different module instances. The outer wrapper must pin this helper and core, authenticate the old six-module baseline, pass the fixed anchor callback, verify the new family metadata, and perform those full source checks. In particular, a module-local mutation cannot by itself test aliasing of private coordinates across distinct calls; independent flattening must exclude it.

The integration must disable old comparison error-absorption and contact-inverse passes on these conic batches. There are no old paired-test B-square witnesses, epsilon leaves or inverse rows for those passes to consume. Existing unrelated scalar/root transformations can continue only with new locators and full replay.

Subject to these explicit outer obligations, the auditor checks the exact equations and field interfaces consumed by the joint arithmetic proof. Finite success establishes implementation correspondence, not the inherited height, pole, formal-group or prime-pattern theorems.
