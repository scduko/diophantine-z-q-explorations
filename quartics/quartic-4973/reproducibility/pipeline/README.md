# First conic numerator with twofold targets and direct tangents

This candidate extends the frozen target-two/tangent/shared-square packet
34be9b53e29041d2cc22eaf43b1dc449399f5c5b62791308261bbbd2de949cd5.
It retains the same complete, pinned normalized-ten parent and repeats every
independent root, tangent and shared-square check.

Only the first H.f field in each of the 37 conic batches changes. Its virtual
leaf becomes W=T/r, where T=eval_theta(H.f^2). The field remains order one.
The two new rows are T-2AY+A^2-2B^2=0 and rN-r-T^2=0. The retained rational
conic excludes r=0. All other fields, powers, higher norm nodes, pole calls,
root equations and comparisons remain unchanged.

The denominator change is an arithmetic-source change. The old and new
private tuples are not asserted to be equivalent. After that change, the
fusion T=rW is an exact rational coordinate change. The independent first-norm
auditor restores the old module specification and delegates to the full
root/tangent/shared checker. That restoration checks the declared source
change; the separate arithmetic proof supplies soundness and completeness.

There are still 377 field records and 340 private evaluations. The locator
marks 37 first numerators with norm=null, numerator=T, power=r and virtual
denominator exponent one. The remaining 340 records are ordinary or shared
norm coordinates. It must not interpret T as an old r-squared norm coordinate.
The scalar-height source and its parity predicate are unchanged.

MIXED_MODE_DENOMINATOR_CLARIFICATION.md states the existing precision split:
the beta-only common denominator has precision12; full and Lucas modes use40.
This corrects a uniform-precision phrase in older proof prose without changing
the existing source equations or their conclusions.

The runner checks 153 locator mutations and exact first-norm identities.
After the actual full source passes its audit, it checks87 first-norm
mutations. The inherited109 shared-square and12 tangent mutations run on an
explicitly restored specification view. Four first-norm resource tests and
two invalid callback forms are also checked. The remaining source tests,
deterministic regeneration, fresh lift and certificate replay are retained.

No new endpoint count is claimed. The source coordinate and row counts are
unchanged by this last pass; the first cubic norm equation becomes quadratic.
Only a fresh remote run can determine the final effect after cleanup.

Root installs this directory as
research/quartic-variables/target2-tangent-first-norm-pipeline and runs:

```text
python -E -B research/quartic-variables/target2-tangent-first-norm-pipeline/run_candidate.py --repo . --mode exploratory --output build/quartic-target2-tangent-first-norm-20261106 --stage-seconds 180
```

Only root dispatches the bounded Linux run. Earlier packets remain immutable.
Version4 requires fewer than5000 total variables, including the input.
