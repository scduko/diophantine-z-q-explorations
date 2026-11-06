# Joint-chart interface for the unchanged conic batches

`conic_emitter_joint.py` is a separate adapter derived from frozen `conic_emitter.py`, SHA-256 `b8899e6b8c4bc443e207d8fa43abb696ce90997b35285f0c929c59efa851f327`. The original file is unchanged. No conic equation, field order, power circuit, tree schedule or pole argument changes.

Install in this order on a fresh archive builder:

1. The pinned three-mode kernel.
2. `rational_difference.install(b, combined, low, base_make_batch)`.
3. `joint_chart.install(b, rational_difference, low, base_make_batch)`.
4. `conic_emitter_joint.install(b)`.

The joint-chart hook appends shared target inputs after the original prefix. Consequently the conic wrapper uses explicit legacy slots rather than inferring them from the new free-input count.

| Comparison | New free count | Legacy prefix | Old theta slot | Old error slot | Raw-contact slot |
| --- | ---: | ---: | ---: | ---: | ---: |
| q_compare4 | 61 | 31 | 28 | 29 | 30 |
| q_compare_beta | 28 | 16 | 13 | 14 | 15 |
| q_compare_lucas | 50 | 26 | 23 | 24 | 25 |

The old theta/error slots are still checked and ignored; each conic batch creates its own private triple. The new joint target inputs are not reinterpreted by this adapter. It delegates all point, G, ratio and difference construction to the independently reviewed joint-chart hook. The field lists remain 15/6/12, and the batches remain q_conic15/q_conic6/q_conic12 with unchanged free arguments and metadata. Comparison metadata adds `conic_legacy_input_count` to record the checked prefix length.

The adapter requires both `_rational_difference_installed` and `_joint_chart_installed`, and rejects a previous conic installation. The existing suppression/removal of the two temporary old small batches remains valid because the joint hook still emits them through the archive constructor. The independent auditor must check the complete resulting modules and root against the joint-chart source, not the earlier rational-difference root.

This is interface adaptation only. It does not install the later local-Lucas residual proposal, change precision, or supply an arithmetic approval for a new source. No local execution was performed; the pipeline owns bounded syntax, generation and full replay checks.
