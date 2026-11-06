# Emitted first-norm source: independent arithmetic binding

2026-11-06. **PASS for the exact emitted source-to-arithmetic binding**, including the mixed-mode correction. The bound endpoint has 5173 total variables; this review makes no claim about a later cleanup or a below-5000 result.

## Exact artifact

The artifact is `work/quartic-sub5000-20261106/target2-tangent-first-norm-result`, run 42242278973, commit `97e1af55578d1caf6a1decc44c050aea5b4bb315`, artifact 13517231821. ZIP SHA256: `c2ccf97370ecc32d6f202f68b92cf61601acb960711c3ec6e2d52992f6a13e3b`. Frozen packet manifest: `7654b06f450db87a3181dd5e16fe23949cb4e57d22751aef3681fed80a1fcf26`.

Source ID: `target2-tangent-first-norm-normalized-linear-pole-k40-q12-a25-h19-s32-4a82d9a8dc1b`. Compressed source SHA256: `94f8a1972cbfc0cf6493d418e628a18482307dec5c427db72e86d3eacb1a6f5d`. Uncompressed source SHA256: `4a82d9a8dc1b5c92eb40a49751c0a6aae073c8f765ca5e276a74802fd56b84be`. The source has 4935 variables and 4513 residual rows before lifting.

I verified the actual artifact/run/commit identities and ZIP, every packet file hash, all recorded stage logs, inspected source and compiler hashes in the source/repeat/adapter copies, the source header and row count, complete construction-map-derived layout, and final source/certificate/polynomial/checker bindings. The full independent composed module auditor passed on the actual emitted dictionary. This is not acceptance inferred from the pre-run manifest.

## Exact source change and mathematical scope

All eight modules other than the three conic batches are byte-identical to the accepted tangent artifact. In particular the 212-local/197-row root, comparison modules, scalar height, full anchor and ordinary linear pole are unchanged. All old raw-contact relations, target-two bindings, beta scaling and shared-square definitions survive. The selected source has no scalar-J0 fusion or common-root-curve change.

For each of the 37 instantiated batches, I separately checked the emitted first field record, its literal scalar rows and its full private-coordinate incidence. The first field is H.f of order one with coefficients A,B, evaluation Y, numerator T, and first node N. Its exact rows are

`T - 2*A*Y + A^2 - 2*B^2 = 0`,

`r*N - r - T^2 = 0`.

The numerator occurs only in these two rows and in no call argument. Its metadata has no old norm coordinate, records raw r as the virtual denominator, and records exponent one. The original r-squared power is retained separately. The first numerator is not interpreted as an old divided field norm by the locator. The common-f(J) shared-square field is separate and unchanged.

The source change has two logically different parts. The new virtual leaf is W0=T/r instead of T/r squared. At an arbitrary odd raw-contact valuation, the retained private conic gives positive odd discriminant valuation, and the constant-first tree plus one-sided pole gives R>0 and v(W0)>-R. Hence v(T)>0. Opposite valuation parity in `T=Y^2-(theta^2-2)*B^2` gives order one for the original field at the selected square root, even for nonintegral coefficients. Every other field uses its original power and order. This is a full arithmetic input-projection argument, not a map from arbitrary old batch witnesses.

After that change, the fused row is exactly equivalent to `T=r*W0` and `N=1+r*W0^2`: the retained rational conic proves r nonzero, so W0=T/r is allowed. Zero T or N and negative rational r are not excluded. For integer completeness, the original depth-two choice at the selected prime makes the new leaf integral and the norm root a unit. With fields fixed, all new tree values remain rational polynomials in private theta for fixed nonzero r, preserving simultaneous real/2/3/17 pole approximation and the chosen split-prime depth. Private orientation may vary in soundness; completeness can choose a common orientation at repeated primes. No new external arithmetic assumption is added.

These are the exact statements reviewed in `FIRST_NORM_ARITHMETIC_REVIEW.md`, SHA256 `90a8c92390d48a3ac5ceef6328b7451a3ffc67a78090537bc24294cdce29824c`, and the pre-run integration review, SHA256 `97c0720e681dec3044d1912d12a7fab609f28648025e697038a644d0405eb3a3`. The current source matches both statements and their coefficient-independence and completeness-order premises.

## Preserved arithmetic and actual coverage

The map has 13 full, 8 beta-only and 16 Lucas-only occurrences: 377 fields, 340 evaluations, 37 first numerators and 340 other field-norm coordinates. All 37 private conic triples are disjoint; each pole call receives exactly its own raw r, private theta and upper norm root. The shared-square common-f channels all receive the same globally defined pair. The independent complete parent checks and unchanged comparison bytes bind their ordered field lists and exclude old global theta/error consumers. There are no old gpoint locators or ordinary comparison inverse guards.

High40, beta12, scalar orders `[1,1,1,1,32,32]`, anchor25, H19 with proof-effective factor 5, integer doubled root indices, target multiplier 2, beta residual `C_A-2*beta`, and the normalized Lucas residual are unchanged. The scalar polynomial still uses `beta=X^2+2`. The four direct tangents remain the exact projection-preserving changes accepted in `TANGENT_5210_SOURCE_REVIEW.md`, SHA256 `b8074e332800cef8644aac1f1e45074179f6f3d0c33f248308526d99200c3c98`.

The source contains the exact `MIXED_MODE_DENOMINATOR_CLARIFICATION.md`, SHA256 `2a1eb8ed9a7175995afa665a08035728c1714b5fa30e1ba52030b6adf7b8ba34`. Denominator order is 12 for beta-only and 40 otherwise. Since every numerator order is at most that denominator order, the local unit and quotient argument gives the required congruences. No unconditional order40 assertion for arbitrary beta-only witnesses is accepted. Both height contradictions and all inherited theorem/version qualifications remain as in the accepted target-two/tangent arithmetic.

The bound remote tests first accepted this actual source and rejected 87 first-norm semantic mutations, with four resource-abort cases and two invalid Boolean callback cases. The 109 shared/root and twelve tangent mutations use an explicitly restored parent specification; the record does not mislabel them as additional new-row tests. The separate 208 inherited mutations and literal tangent tests retain their original scopes. I reran only the small complete module audit and artifact/row checks locally, not full generation, flattening, replay or expansion.

## Bound finite result

The endpoint reports **5173 total variables, 5172 witnesses, 4752 rows, 74782 monomials, degree 4**, maximum absolute coefficient **685783949153203534233890 < 2^80**, all weights 1. The coefficient is one greater than in the tangent parent; it is not reported as unchanged. There are 420 operations: one parity conic, 296 linear, 121 elimination and two shear operations.

Verification SHA256: `3479b547c270f3f017e2db1feea0d070abb05e8e02c35e04c8c306bdf12c4257`; certificate: `110209d9b52a81bad47389406658c8ded498345bedbfdb589cb2121e0ea8000f`; expanded polynomial: `3ac4fd30d3846ef8d7f011659eeb803b70f0e35c5a3c3b0584eb8d8d2a8ab82d`; checker: `324ab603f1ce1175da6de18f3f600aa2b0c1e2474ea65a575b4a4cac48e09f90`.

The independent small-artifact inspector is `inspect_first_norm_artifact.py`, SHA256 `768c53b81473e020c379480c00db67afc76d1dd97a9f4a69f644922db7da2a3d`. Its detailed receipt is `FIRST_NORM_5173_RECEIPT.json`, SHA256 `c98966932e8d198142f327d49da2789fb3b08a6a4bb5c37e0b02423c4090c677`. These establish the exact source binding and identify the remote finite verification; they do not replace the inherited mathematical assumptions or certify a future endpoint.
