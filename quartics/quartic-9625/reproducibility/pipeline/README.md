This is a separate exploratory source packet based on the measured 11,043
variable H19/high40/beta12/root37 construction. It keeps the full comparison
at 29 contacts and uses a beta-only comparison at raw positions 5 through12.
The raw contact equations, root points, proxies, anchor25, scalar32, and all
full-comparison modules are unchanged. It introduces q_compare_beta (16 free
arguments) and q_batch17 (11 order1 and6 order12 rational tests).

The selective-contact arithmetic theorem is a separate prerequisite. A
successful run reports an algebraic candidate and arithmetic_acceptance=false.
No H18, Jacobi, or three-mode changes are included.

Copy the files listed by `manifest.json`, and the manifest itself, into
`research/quartic-variables/selective-beta-pipeline/`. The packet includes the
small pinned modules/compiler files needed to regenerate its measured
baseline; no previous job directory is required. The 13 external pins are
existing algebraic tools and rule bodies in the integration checkout.

Run only in the root's existing bounded Linux workflow:

```text
python -E -B research/quartic-variables/selective-beta-pipeline/run_candidate.py --repo . --mode exploratory --output build/quartic-selective-beta-20261106 --stage-seconds 180
```

Use `--source-only` for source audit/testing without a quartic count. The
default pipeline regenerates the exact baseline modules, builds the new
source, independently checks its equations and complete flattening, tests
malformed inputs, repeats source generation byte-for-byte, and runs a fresh
lift followed by all existing reduction stages and full independent replay.
It finishes with the five named-source binding rejection tests.

The changed-module checker imports only the hash-pinned independent
arithmetic/parser core, never the producer. It reconstructs all beta
equations and ordered tests directly. The root is compared with the exact
baseline except for the eight named call substitutions and explanatory
metadata. Generic independent flattening is reused with only its final
expected instance-count assertion changed. The unchanged modules are exact
pinned baseline inputs.

The batching worker's dual-module adapter derives every norm guard and
bottom pair from the actual modules/map. Its synthetic fixtures check 37
batches,161 norm guards and644 bottom pairs, plus malformed layouts. These
are locator counts, not a claimed final variable saving. Existing rule
equations and full current-incidence checks remain unchanged.

Local work was limited to small hash, AST, template, and synthetic locator
checks. No source generation or complete candidate computation was run
locally. Root owns the first actual source and quartic test.
