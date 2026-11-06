# Release reproduction runtime

This runtime is restricted to the frozen target2, tangent, shared-square and first-norm source pipeline. It does not select a result or establish its arithmetic theorem. A release owner must supply all selected hashes in `selection.json`; missing pins are rejected. The planner derives the variable count from the selected verification report and rejects a count of 5,000 or more, including the input coordinate.

The mandatory run regenerates the source twice, checks every inspected source file, runs the current source mutation tests, regenerates the named base checker, and replays the base algebraic stages. It regenerates the extended checker from that fresh base when the selected final certificate uses the cleanup rules. It then replays the unchanged selected final certificate against the fresh source and compares every final row, variable map, weight and expanded polynomial through the selected full checker. Three malformed final candidates must fail.

`--rediscover` additionally reruns the selected power and relation search recipe. That result is separately verified and compared with the selected certificate and expansion. The searches use time limits, so reproducing their exact choices is not a requirement for mandatory reproduction. If optional rediscovery fails, the overall run reports failure and retains the already completed mandatory status in `SUMMARY.json`.

No command downloads an artifact. The package contains the source pipeline, its baseline and parent modules, all 13 external compiler/rule inputs, the selected source files, both checkers, the final certificate/candidate, the selected cleanup packet, and the pinned arithmetic review. Private artifact locations are preparation inputs only. Copy-plan paths use logical input families and relative paths.

## Selection

The exact JSON keys are:

```json
{
  "format": "quartic-release-selection/v1",
  "source_pipeline_manifest_sha256": "7654b06f450db87a3181dd5e16fe23949cb4e57d22751aef3681fed80a1fcf26",
  "source_entry_sha256": "REQUIRED_FULL_SHA256",
  "source_archive_sha256": "REQUIRED_FULL_SHA256",
  "base_checker_sha256": "REQUIRED_FULL_SHA256",
  "final_checker_sha256": "REQUIRED_FULL_SHA256",
  "final_certificate_sha256": "REQUIRED_FULL_SHA256",
  "final_expansion_sha256": "REQUIRED_FULL_SHA256",
  "arithmetic_review_sha256": "REQUIRED_FULL_SHA256",
  "cleanup_manifest_sha256": "REQUIRED_FULL_SHA256_OR_NULL"
}
```

The placeholders are intentionally invalid. `cleanup_manifest_sha256` may be JSON `null` only when the final checker is the base checker and no cleanup packet is selected. The arithmetic review must name the exact selected source. Hashing that review preserves its identity; it does not mechanically prove its conclusions.

## Preparation

Run the planner with explicit paths:

```text
python -E -B plan_release.py --selection selection.json --source-run SOURCE_RUN --pipeline FROZEN_PIPELINE --repository INPUT_REPOSITORY --final-artifact FINAL_CANDIDATE --final-checker FINAL_CHECKER --arithmetic-review REVIEW --cleanup-packet CLEANUP_PACKET --output copy-plan.json
```

`SOURCE_RUN` is the complete successful source-pipeline result. `FINAL_CANDIDATE` may be a later cleanup endpoint. `INPUT_REPOSITORY` supplies the 13 exact external files listed in the pipeline manifest. `CLEANUP_PACKET` is the complete selected named-power packet, including its original parent input, tool files and manifest. The planner checks the final certificate's source entry before writing the plan.

Apply the plan to a fresh directory with the unchanged reviewed installer:

```text
python -E -B prepare_package.py --plan copy-plan.json --input source=SOURCE_RUN --input pipeline=FROZEN_PIPELINE --input repository=INPUT_REPOSITORY --input final=FINAL_CANDIDATE --input checker=FINAL_CHECKER_DIRECTORY --input review=REVIEW_DIRECTORY --input selection=SELECTION_DIRECTORY --input runtime=THIS_DIRECTORY --input cleanup=CLEANUP_PACKET --output PACKAGE
```

Omit the cleanup argument only for a selection without cleanup. The input family names must exactly match those in the plan. README files are included before the exact package manifest is written. Do not add files afterward without regenerating the plan and manifest.

## Reproduction and bounds

From a Linux host:

```text
python -E -B PACKAGE/reproducibility/run.py --package PACKAGE --output FRESH_OUTPUT
```

The output must be new and outside the package. Python uses only the standard library. Exact source compression is checked against the selected archive hash; an incompatible Python/zlib build fails rather than substituting new bytes. Original environment information is preserved in `evidence/source-run/RUN_INPUTS.json`.

There is one active child at a time. The runner requires 8 GiB available memory at startup, aborts below 4 GiB, limits each child to 2 GiB address space and enforces per-stage timeouts. The default timeout is 180 seconds and the maximum is 600. Process groups are killed after a stage and on handled termination. Linux parent-death signaling covers the direct child. An outer supervisor must kill the entire descendant tree if the runner itself receives an uncatchable signal.

The runtime never treats timeouts, memory aborts, or unexpected exception types as successful negative tests. Source arithmetic acceptance remains a separate pinned review.

## Local validation scope

```text
python -E -B test_binding.py --pipeline FROZEN_PIPELINE --report bindings.json
```

This checks synthetic pins, registry parsing, certificate headers, report counts, relative paths, manifest files, disabled assertions, the tiny installer and coverage of the frozen outer script list. It performs no full source generation, lifting, expansion or certificate replay. A final selected package still requires a clean remote mandatory run and independent review before release.
