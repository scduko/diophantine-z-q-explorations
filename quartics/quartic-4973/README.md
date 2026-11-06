# Exact quartic package

The selected source, final certificate and expanded polynomial are bound by `reproducibility/selection.json` and `reproducibility/manifest.json`. The total variable count, including the input, is recorded in the manifest's `expected` object. No count is inferred from a filename.

For the complete independent reproduction procedure, read [reproducibility/README.md](reproducibility/README.md). On a sufficiently provisioned Linux host, run:

```text
python -E -B reproducibility/run.py --output /path/to/new-output
```

This regenerates the source and checkers and replays the exact selected final certificate. It reads packaged inputs only. Optional heuristic rediscovery uses `--rediscover` and is reported separately.

The finite checker establishes exact algebraic equivalence to the pinned source and verifies the full polynomial expansion. The source arithmetic theorem is supported separately by [the pinned source review](evidence/arithmetic-source-review.md) and the proof/contract files retained in the source pipeline. It is not a Lean proof or an arithmetic theorem established by certificate replay.

The package is immutable during verification. Standalone execution of `verify_certificate.py` writes a verification report, so use a writable copy of the candidate files outside this package. The mandatory runtime already makes that copy.
