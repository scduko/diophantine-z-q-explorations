# Review of the actual reproduction-certificate fix

PASS for revision 2. The change permits the observed runtime-metadata difference without changing the accepted proof certificate or ignoring proof data. This addendum replaces the earlier requirement that regenerated gzip bytes equal the frozen certificate bytes. It does not replace certificate replay or the arithmetic proof.

The reviewed revision is `work/quartic-sub10000-20261106/parity/release-handoff/revision2`. Its full `COPY_MANIFEST.json` has SHA-256 `7c1d59be6b1783268f49661624567d21acd6bbbc60755bbaf5017f05367da5f3`; `DELTA_MANIFEST.json` has SHA-256 `e0fb3f1ea822e3f9e26e481a677d9ae5ef963d95ac1a75e62475437e4ea1dc85`. I checked every one of the 61 file records. Exactly the four declared files differ from the base manifest: `release.json`, `release_config.py`, `test_release.py` and `BUILDING.md`.

## Actual evidence

I independently read and decompressed the real frozen certificate and the real regenerated certificate, rather than only inspecting synthetic fixtures:

| Artifact | SHA-256 |
|---|---|
| Frozen `quartics/quartic-9625/certificate.jsonl.gz` | `8aaa2249eda6972c441d58b212ec64a53e1202d5e9f74ea4cbc53e7e3f71a0bd` |
| Regenerated `docs/quartic-9625/verification/regenerated-certificate.jsonl.gz` | `bdf4765cd001cf36e265ce964ace7cb045f1e74885e86d4425f78bbe89467ada` |
| Actual `docs/quartic-9625/verification/REPRODUCTION.json` | `a093c3eb8d62926ab86bf3afa5d4b73fde414d191142499369113f1cc54ad80a` |

Both decoded files have 1,249 records. Records 0 through 1247 are byte-identical. Record 1248 is the terminal `final` record. Its only difference is `report.seconds`, which is 0.673 in the frozen file and 0.605 in the regenerated file. Replacing exactly that timing token makes the entire decoded text identical. The regenerated digest equals the actual receipt's `regenerated_certificate_sha256`; the frozen digest equals the receipt's expected certificate digest. The separate regenerated verification report is PASS and names the same polynomial digest, counts, source and checker as the release.

The independent comparison record is `ACTUAL_CERTIFICATE_COMPARISON.json`, SHA-256 `d031b4ee373937900b0b54c39566195d105f80043b7fc78bdd982bda0cf2e1cf`.

## Code and test review

The exact frozen certificate digest remains in `proof_pins`, and `validate_current` checks its bytes before comparison. The new regenerated-certificate path is fixed to the intended current verification directory and must be present in the current snapshot. Its actual compressed bytes must match the fresh receipt's digest. The receipt's expected frozen certificate digest must still match the original release pin. The existing source, checker, numerical, package-manifest and receipt-status checks remain.

The decoder bounds compressed and decompressed sizes, rejects duplicate object keys and nonfinite JSON constants, and requires exactly one terminal `final` record with a report object. It deletes only that record's `report.seconds` slot. It preserves the order and contents of every other record and field. It then compares canonical JSON strings, avoiding Python's equivalence between `True`, `1` and `1.0`. The change therefore does not turn numeric-type changes, other elapsed-time fields, removed report fields or altered mathematical rows into accepted differences. It also does not substitute the regenerated certificate for the independently pinned release certificate.

The author supplied an actual `validate_current` run, not just the earlier schema fixture. `ACTUAL_CHECK.json`, SHA-256 `4eed2560e5199e59404c94fe5bf7f52cecfa86dab1634ae6f2d06a00d29b04d6`, reads the actual assembled checkout's proof and receipt bytes. Only the proposed release descriptor is supplied in memory, because it was not yet copied into the checkout. I read this helper and its scope statement. Its initial directory-depth error was corrected before the successful run.

`TESTS.json`, SHA-256 `92701ef1a87ade5a3dc07b77d4de2f00b17a64c03c0215bb1c575c2a8ea5e084`, records 65 negative cases. I inspected the new fixtures. They accept the timing-only difference and reject a wrong regenerated digest, a missing regenerated file, a changed mathematical row, removal of a different final-report field, a seconds field elsewhere, integer-to-boolean and integer-to-float changes, duplicate keys and nonfinite constants. The previous exact-plan, generated-file and legacy-format protections remain unchanged. I did not rerun polynomial expansion or the full reproduction.

The final `release_config.py` has SHA-256 `162490bab804e1bb8f284c8ba99564d1c6f5769d9eaa834c1effaf7db7a49321`. No further correction is requested for this revision. Root still needs to copy the four declared files, include the real regenerated certificate in the public snapshot, and run the planned handoff preparation/build checks against that snapshot.
