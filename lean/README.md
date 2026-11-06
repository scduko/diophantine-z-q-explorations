# Accepted Lean helper snapshot

This directory contains the 48 modules accepted in integration 31. The Lean source files, root imports, dependency metadata, and frozen target are copied byte for byte from that snapshot. `SOURCE_MANIFEST.json` records their hashes and the source integration manifest hash. Historical filenames containing `Draft` are retained to preserve imports; those helper modules belong to the accepted snapshot.

**This is not a formal proof of the 11/5 manuscript's main theorem.** The snapshot contains 463 explicit public declarations and 69 private declarations, including definitions and helper results. The whole-model, height, restricted-converse, pole-completeness, multiplication, compiler, construction/bounds, and final composition obligations are not closed by this snapshot.

`Frozen/BoundedIntegerPolynomial.lean` is the exact approved, unproved target for the original polynomial in 292,890,231,905 total variables and contains one `sorry`. It is not a formal statement of the Version 4 quartic in 4,973 variables. No quartic-specific frozen target or completed quartic proof is included in this snapshot. It is excluded from `ZInQ.lean`, the default library, and the axiom audit. Its hash is checked so that the intended statement cannot silently change.

## Source provenance

The dated research archive contains the original paths under `formalization/z-in-q/` and the source record `outputs/z-in-q-integration-31.json`. The [research guide](../docs/research-guide.md) explains how to find those files. A few source comments refer to relative paths inside that archive. They are provenance references, not build dependencies.

The source integration manifest SHA-256 is:

```text
0e6ea11e782b845c7d316e2c5c01427583e85511ff15146c489c540e4ce9f45b
```

Upstream Mathlib and its dependencies are not vendored here. Their URLs and commit revisions are recorded in `lake-manifest.json`; their own licenses continue to apply. The alpha-sequence modules cite the Archive of Formal Proofs' `DPRM_Theorem` development where its mathematical arguments were used.

## Check source identity

From the repository root, with Python 3.9 or later:

```sh
python scripts/check_lean.py
```

This checks every listed source hash, the 48-module import closure, the absence of proof holes and custom axioms in the accepted modules, and the quarantine of the one frozen target. It does not run Lean or establish mathematical correctness.

## Rebuild and audit

Install Lean's `elan` toolchain manager and make `lean` and `lake` available on `PATH`. The checked-in `lean-toolchain` requests Lean 4.35.0. From the repository root:

```sh
cd lean
lake exe cache get
python ../scripts/check_lean.py --build
```

The first command resolves the pinned Lake dependencies and fetches their published compiled cache. The Python command verifies each dependency checkout revision and its tracked-source cleanliness. It then compiles all 48 project modules and the root into a new `.checks/` subdirectory, using only those new project artifacts and the pinned dependency libraries. It never imports an old project build directory.

Every compiler invocation includes `-Ddebug.skipKernelTC=false`. The last invocation checks `Checks/Axioms.lean`, which inspects imported declarations originating in the 48 project modules and rejects dependencies on any axiom outside `propext`, `Quot.sound`, and `Classical.choice`. The declaration count includes compiler-generated declarations and therefore need not equal the explicit-source count.

The output directory contains a log for every module, `axioms.log`, `commands.json`, and, only after success, `RESULT.json`. A failure stops the check. Do not report the main theorem as proved when these helper checks pass.

For an existing read-only cache of the same pinned dependencies, `--dependencies PATH` selects its packages directory. `--lean PATH` selects the compiler executable. `--output PATH` chooses the fresh project-output directory and refuses an existing directory. These options do not alter the source or dependency pins.

The default is two concurrent single-threaded compilers. `--jobs 1` through `--jobs 4` changes the concurrency without changing the checked targets. Git newline conversion is disabled within this directory to preserve the source hashes across platforms.

## Validation scope

The release preparation checks are recorded in the [validation report](VALIDATION.json) and the [704-declaration axiom ledger](AXIOMS.json). They distinguish a fresh build of the project modules from a rebuild of upstream dependencies. Published dependency caches are trusted inputs; this procedure does not independently rebuild Lean or Mathlib, and an axiom audit does not replace review of a theorem's statement or its relation to the 11/5 manuscript.
