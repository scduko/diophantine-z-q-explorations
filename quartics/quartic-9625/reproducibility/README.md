# Version 3 finite reproduction package

The selected release is the beta-only 9,625-variable endpoint. The builder
is parameterized, but the resulting plan pins every file and every expected
count from that exact verified artifact. Do not substitute a different
endpoint after the plan has been reviewed.

Create the explicit plan from the downloaded artifact, its exact frozen
pipeline, and the repository containing the thirteen external dependencies:

    python -E -B plan_package.py --artifact BETA_RUN --packet BETA_PIPELINE --repository REPOSITORY --output beta-copy-plan.json

Create the package in a fresh directory:

    python -E -B prepare_package.py --plan beta-copy-plan.json --input artifact=BETA_RUN --input packet=BETA_PIPELINE --input repository=REPOSITORY --input runtime=THIS_DIRECTORY --output PACKAGE

The public package root is quartics/quartic-9625. Its eight candidate files
remain at the root, with the exact checker renamed verify_certificate.py.
Audited modules and compiler files are under source/. The source entry,
source audit, construction map and source layout are also at the root.
Original receipts are under evidence/. The complete frozen pipeline,
its manifest, all thirteen external inputs, generated tool copies and this
runner are under reproducibility/. No conversation, credentials, unrelated
research, private archive or unlisted filesystem file is copied.

On the bounded Linux worker:

    python -E -B PACKAGE/reproducibility/run.py --output FRESH_OUTPUT

Use the original Linux CPython 3.12/zlib environment or another environment
that passes the exact gzip compatibility preflight. Each child runs with
assertions enabled, a two-GiB address-space limit and a separate process
group. Timeout and handled interruption terminate that process group.
Linux parent-death signaling also terminates the direct child if the runner
dies abruptly; a verifier grandchild launched by the named-mutation tests
does not inherit that signal and could finish its short check after an
unhandled SIGKILL. The caller's outer guard should terminate the descendant
process tree when it applies a hard kill.
The default limit is 180 seconds per stage. All stages run sequentially.
The caller should also impose its established overall job limit.

The runner checks the frozen source and mutations, replays the frozen
certificate, rebuilds and audits the source, regenerates the exact adapter,
then rebuilds and independently verifies every algebraic stage. It compares
the final source, rows, variable map, weights and expanded polynomial byte
for byte. The certificate is compared structurally after removing only
final.report.seconds; both original and regenerated certificates receive
complete independent replay. Named-source mutations run on both endpoints.

The final SUMMARY.json has status `PASS: FROZEN REPLAY AND CLEAN
REPRODUCTION`, top-level source_id/source_sha256/checker_sha256, and an
expected object containing the frozen variable/row/monomial/coefficient
counts and artifact digests. A failure writes a failure summary and logs;
it does not produce that PASS status. Mathematical acceptance of the source
theorem is a separate reviewed claim.

The package is immutable and its manifest checks the exact file inventory.
The standalone verifier writes verification.json into the supplied artifact
directory. Run it on a copy, never directly on the immutable package before
running this reproduction script. This runner already makes the required
reference copy. The packaged original receipt is
evidence/stages/coordinates.json; there is no root verification.json.

Package metadata authenticates files relative to the frozen copy plan.
The caller or public release must publish the plan/manifest hashes to bind
the package to the selected release externally.
