# Package README delta review

PASS. The new root README accurately states the reviewed counts, coefficient
bound, source identifier and H19/37/high40/beta12/anchor25/scalar32 profile.
Its expansion digest and receipt links match the package. It keeps the
finite source/certificate checks separate from the mathematical source
theorem, directs full reproduction to a fresh output outside the package,
and warns that standalone verification must use a copy.

The independent read-only `audit_readme_delta.py` passed. All 113 existing
payload files are byte-identical to the package covered by
`INDEPENDENT_REVIEW.md`. The only addition is root `README.md`; the only
changed existing files are `reproducibility/copy-plan.json` and
`reproducibility/manifest.json`. Their other metadata is unchanged. The
revised package contains 115 manifested files, and its exact file inventory,
sizes and hashes all check. No compiler, checker, source, certificate or
polynomial byte changed. `README_DELTA_AUDIT.json` records the comparison.

The reviewed package is
`elimination/release-package/quartic-9625-with-readme`, relative to the
November 6 research directory. Its hashes are:

| Item | SHA-256 |
| --- | --- |
| Root README | `29e3ef58046d7c7fa58a6eefac4233ea5c6c86c51b377d1eb74865babab820b1` |
| Copy plan | `e0215e0c75e44bda8c6bdba917ef88bd9680c514ef2b43607268e78e81aeeee8` |
| Package manifest | `eb4b2ae93f932d96919d8779f937b7eec47163c8cf8909d1b66a55b1fdc08559` |

This review performed no source generation, certificate replay or polynomial
expansion. The required root-dispatched reproduction remains separate.
