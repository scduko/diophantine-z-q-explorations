# Normalized-Lucas outer integration review

PASS for the exact files in `BINDINGS.json`, SHA256
`74e0c653c4f1162fb005e96263b8da1b12f968a7b0d9aa5335f60a7ab3ab373b`.
No unresolved integration defect was found. This review compares the new
outer pipeline against the frozen local-Lucas packet manifest
`12d818714b70680eff617295008d685ebec8c81984d0402eb6ea79840ef330ed`.

The reviewed final producer wrapper is `build_source.py`
`9021cac6c2096732d592179edbb5bb7018d4a7285477d7a37284f83fcd9fbdb3`.
It installs normalization after the local-Lucas hook and before the
unchanged private-conic hook. It still regenerates the original pinned
baseline before constructing the new source. Its new hook changes the
full and Lucas comparison blocks; the root-proxy capture and removal
guard path remain intact.

The reviewed outer auditor is `check_source.py`
`7fcf0a8a3ea22b01eb8b39cd7bede33d6506b2d9a86350ec62ec3c09acad8152`.
It pins the incoming independent normalized module auditor, passes the
unchanged conic and anchor checker callbacks, and retains the complete
flattening and construction-map checks. The normalized source contract,
typed addon and parent preservation record are included in its inspected
file set. The source family, arities, 37 contacts, 377 field nodes, mixed
orders, and 29 normalized occurrences agree with those contracts.

The nine parent preservation hashes were independently compared against
the actual measured local-Lucas source and its source entry. They match
the eight required unchanged modules and `shared.json`. The parent entry,
compressed source, audit and packet manifest hashes also match the
record. The producer checks the nine emitted files; the auditor pins the
record itself, checks its parent identity against the typed addon,
requires the exact nine names, and checks their new-source bytes. This
satisfies the addon's literal byte-preservation requirement without a
runtime dependency on the parent artifact.

The locator requires normalized metadata on full and Lucas comparisons
and rejects either normalization marker on beta-only comparisons. It
retains the exact raw-contact, ignored-root-slot and private-conic
boundary checks. The final adapter,
`575bd9a4a246b4560da3122d4565c5df5dc15924f334a0df307b65b9481ccb3f`,
includes all new audited files and preserves the existing module/map,
residual/header, source-registry and original-source bindings. The
generated certificate checker still excludes obsolete log and ratio
handlers.

The outer runner adds the normalization identity fixture and switches
to the independent normalized mutation suite. Its CLI matches the new
suite, including the pinned core and anchor checker. It retains the
separate 12 root-removal guards, source regeneration comparison,
fresh-lift/reduction/full-expansion pipeline, and named-source mutation
checks. The old 30-case author mutation test was removed because it
targets the old coordinate layout; the new suite declares 208 semantic
cases and rejects resource aborts as test failures. Its full execution
belongs to the remote source trial.

Independently executed local checks passed:

- 65 locator negative fixtures.
- The exact normalization identity and 54 rational examples, including
  the `C_s=2` case, two ratio-only zero-ordinate branches, and the explicit
  nonunit valuation example.
- The pinned template and generated source-registry syntax check.
- All final-file syntax and hash checks, plus the nine-file parent
  preservation comparison.

The base adapter, fresh lift, algebraic pipeline, original tool pins,
local-Lucas/root-removal hook, private-conic hook, joint-chart hook and
their retained guard/checker files are byte-identical to the frozen
local-Lucas packet. Their hashes are recorded in `BINDINGS.json`.

This is an outer integration review. It does not replace the separate
normalized arithmetic or semantic-auditor reviews, and it does not
accept an emitted source or predict an endpoint count. No full source
was generated and no research polynomial was expanded locally. Before
dispatch, the existing `freeze_packet.py` regenerates `AUDITOR_PIN.json`
and the complete packet manifest from these final bytes. Those generated
records are not claimed to be the older pre-freeze policy files.
