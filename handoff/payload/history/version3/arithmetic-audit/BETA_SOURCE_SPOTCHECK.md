# Beta-only checker semantic spotcheck

I statically compared `source-pipeline/beta-only/check_source.py`, SHA-256 `41a3d780636c1f28852762ee0ce7a252e207ec74e7367da275676200a6068ffa`, with the frozen asymmetric arithmetic contract. No semantic mismatch was found in the inspected boundary and equations.

The checker requires positions 5 through 12, the exact 16-input selection, two primary charts, two affine differences with their distinct-abscissa guards, G12 for both primary points, the correct compressed ratio equations, the already-conjugated common-J inputs, and 17 ordered rational tests with the root error first. Its strict root-object reconstruction permits only the specified dispatch changes and metadata. It compares other old modules unchanged and checks the shortened batch against `[1]*11+[12]*6`.

The baseline descriptor read has SHA-256 `2a1c41a19f0813e8676c4cbe57eb49a3faa0926f095389d8a4a2b390ea91035d`, identifies `combined-k40-beta12-a25-h19-s32-502e3ed250f7`, and binds source SHA-256 `3bad8b614f1593ab84f068bb42e0b5e0bd6877fa6d315cc6f72f48d57b22df43`. Its authenticity must come from the frozen packet manifest and the prior independent baseline check, not from accepting an arbitrary caller-supplied descriptor.

This is a targeted static semantic review. It is not an execution result, a full review of the reused parser/flattening core, or acceptance of a generated source. In particular it does not cover the later three-mode or Jacobi source variants.
