# Version 9 research handoff

Start with [the new inventory and arithmetic guide](../../docs/quartic-523-540/README.md), then the [current manuscript](../../manuscripts/quartic_v9.tex). The new theorem follows from explicit chart, height, local, prime-separation and compiler arguments in the manuscript, with its inherited arithmetic proofs unchanged.

The contributed [source package](../../quartics/quartic-523-540/) includes all intermediate residuals, certificates and source patches. The [initial audit](../../docs/quartic-523-540/evidence/AUDIT.md) records the independent arithmetic and finite checks before integration. The [source-lineage record](../../docs/quartic-523-540/evidence/SOURCE_LINEAGE.json) pins the contribution branch. The [integrated provenance](../../quartics/quartic-523-540/INTEGRATION.json) records the verifier repair; polynomial data are unchanged.

The [Version 9 supplement ZIP](z-in-q-version9-supplement.zip) contains these new files and the complete current TeX/PDF. It supplements, rather than replaces, the [Version 7 full history](../../handoff/README.md). Neither archive contains a conversational transcript. The complete repository is also available through GitHub's source download.

No new external arithmetic theorem is assumed. Existing source-version qualifications and the incomplete Lean status remain. The symbol S has changed to the fixed integer `3^(2^26)` in the new package, so do not reuse the 962-variable package's S value.

Verify the ZIP with python research/version9/verify_supplement.py ARCHIVE.zip --sha256 DIGEST, using the digest in [SUPPLEMENT.json](SUPPLEMENT.json) or the repository checksum file.
