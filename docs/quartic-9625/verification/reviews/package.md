# Independent review of the 9,625-variable release package

Status: PASS for the static package and runner review and the final frozen
package's complete file closure at the hashes below. The root-dispatched
reproduction must still pass before release. This note does not assert
that reproduction has run.

The reviewer did not author the release copy-plan builder, installer or
runner. The reviewer did author the underlying selective-beta pipeline.
This is therefore an independent review of packaging, dependency closure,
runner sequencing and checker binding, not an independent re-review of
that pipeline's mathematical source definitions. The separate source and
arithmetic reviews remain necessary.

## Reviewed files

All paths in this section are relative to
`work/quartic-sub10000-20261106/elimination/release-package/`.

| File | SHA-256 |
| --- | --- |
| `plan_package.py` | `37050b26ad42b6d969244c651db41d51e41ec5a7b038db9d9301e640924f4847` |
| `prepare_package.py` | `2a009fbd951329418aa384b3bc54b0e06faf187b87eb3b70f647cd047750e173` |
| `run.py` | `8afd999aa7e3c2fa091705fc754e5a625bd7a1f40a4d09f31b4256128a87a66c` |
| `README.md` | `36a780ff2008022ca09a8238a00f7206a9f81048e1931e830c807bdb846ec911` |

## Artifact binding

The read-only `audit_metadata.py` in this review directory passed. It
checked the exact published candidate intended for Version 3: 9,625 total
variables, 9,624 witnesses, 9,161 rows, 82,476 monomials, degree four and
maximum absolute coefficient 685783949153203534233601, below 2^80.
It hashes files without generating a source, replaying a certificate or
expanding a polynomial. `METADATA_AUDIT.json` records its result.

The source identifier is
`selective-beta-k40-q12-a25-h19-s32-d68d86cdf995`. The source gzip hash is
`97b7bc300084afaefe9980f1feea760be8b4dedaf6eb788fcc4c3af440262579`;
the certificate hash is
`8aaa2249eda6972c441d58b212ec64a53e1202d5e9f74ea4cbc53e7e3f71a0bd`;
the expansion hash is
`6d67d45f3d615b7fd2242e3a9404dd9f5da570fc711a29ebe77f613e80ebbf99`;
and the verifier hash is
`cf587ff9c28af5593e346eb7484d1713bd3f1ff77d28aa5ada06b2b92909d6f4`.

The metadata audit parsed the verifier's literal source registry without
executing it and checked exact equality with `source-entry.json`. It also
checked the certificate's initial entry digest, the source header, the
source-audit and construction-map hashes, all 18 inspected source files,
all 33 frozen pipeline files and the reported 27 source mutations and five
named-source mutations. The pipeline manifest hash is
`eaaec2449711c625fc4afcf16dd33286c2c5d91ea568c6542317d2b1ba6623cb`.

The independent `audit_package.py` also passed against the final package
at `elimination/release-package/quartic-9625`. It checked all 114 manifested
files, exact equality of the complete file set, every digest and size,
Python syntax, and equality between the copy plan and the package manifest.
It executes no package code. `PACKAGE_AUDIT.json` records that result.
The final copy-plan hash is
`a85449f3ab93a4bbbfee1f055dbfd9e8726e88b6594ec4a4a864fbb6720ef85d`;
the final package-manifest hash is
`52288783312b46c809aab9300dab42597ff29f3b32a4484063da24c2ac2c072f`.
The last builder revisions add explicit equality checks between the
verifier's literal source registry and the entry, and bind the source-layout
and source-auditor hashes directly to the entry. They do not change any
source equation or algebraic event.

## Package and runner findings

The copy plan includes the eight final candidate files, the byte-identical
renamed verifier, every inspected source file, source metadata, the full
frozen pipeline, all 13 external input files, generated adapter tools and
original receipts. Path checks reject absolute paths, parent traversal,
drive separators and escapes after resolution. The installer refuses an
existing output, checks every source before copying, and verifies each
copy. Runtime validation checks both every listed file and the exact file
set. The release must bind the resulting plan and manifest hashes outside
the package; a manifest is not its own external trust anchor.

The runner copies the frozen artifact before replay, checks all source
mutations, regenerates and independently audits the source, regenerates
the byte-identical named-source adapter, and independently verifies every
algebraic stage. The explicit stage arguments agree with the successful
research runner. The final source, rows, variable map, weights and
expansion must match byte for byte. Only `final.report.seconds` may differ
in the regenerated certificate; both certificates receive complete
replay. No mathematical event or coefficient is ignored in this
comparison. A nonzero exit, timeout, mismatched report or differing file
prevents the final PASS status.

One blocking packaging defect was found and repaired before this review
passed: the temporary frozen adapter omitted `adapter-manifest.json`,
which the named-source mutation script requires. The reviewed runner now
copies the frozen adapter manifest before invoking that script.

Two operational boundaries are explicit in the reviewed documentation.
The standalone verifier writes `verification.json`, so it must run on a
copy if the immutable package is to pass exact-file validation afterward.
The runner applies a two-GiB address-space limit, timeouts and process-group
cleanup; direct-child parent-death handling does not by itself cover a
named-mutation verifier grandchild after an unhandled top-level SIGKILL.
The established outer workflow must terminate the full descendant tree.

## Acceptance boundary

The verifier checks exact projection-preserving algebraic equivalence to
the pinned source and the complete integer expansion. It does not prove
that the source defines the integers. The frozen exploratory receipts
correctly retain `arithmetic_acceptance=false`; release acceptance belongs
in separate reviewed mathematical documentation. This package contains
the H19, 37-contact, high40/beta12, anchor25, scalar32 selective-beta
construction. It does not include the three-mode, minimal-Jacobi or H18
research variants.
