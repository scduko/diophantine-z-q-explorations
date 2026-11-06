# General-root and shared-square outer review

Date: 2026-11-06. Status: **PASS for the reviewed implementation and its arithmetic interfaces.** This is not acceptance of a generated source, expanded quartic, coefficient bound, or variable count. Those require the fresh emitted artifact and independent replay.

The packet is `source-pipeline/sub5000/general-root-shared-square/`. This review checks the composition against the actual accepted normalized-ten parent, rather than treating a manifest or an archived PASS as mathematical evidence. No full source generation, flattening, lift, or SOS replay was run locally.

## Exact scope and pins

| Item | SHA256 |
|---|---|
| Selected parent record | `248778bdda2810db04368a692bd39ff5e17edcf954585e19613493ec9b6f58d0` |
| Joint contract | `06955e6f98913dfc82c19eaa10983faa6df47d820ffc5547239b4abd46ff2fc4` |
| Root source contract | `505b3a743585187ebde58642bb02237dbb45bc55b328b5b88bd84a0724cf1d5c` |
| Builder | `b23050eb96b9176bebba2a6b37f5359ce93ac679078412cfbfc063491d9935ed` |
| Source checker | `f173d82bd5056c0cc9537c2aaee1f440f3c79f1f313bdb1c4f1c9b9e0d2d8aff` |
| Composed module checker | `ebb74acb8ddbaca5e1315c5b77c1fa86775c75cadf02d1537a090a706d3dde26` |
| Source locator | `dc6469fb584d6d049b45ded23693b7ecc0ececa7336a10b42449caea42914bba` |
| Adapter preparation | `ad480c476f0d73dd8fbfdd99db8bca94f9b477cd3efd2430fd74735d4b921acf` |
| Outer runner | `4848789f9640ea1607f13f497ad24dc982cd08c24f82ad3121fa7accb5b31a20` |
| Reduction runner | `388151877642214d9ef831123e277e6928e5eb0f5a8c328fbc0878a5d39b5848` |

The selected parent has source ID `joint-chart-normalized-lucas-linear-pole-anchor4-k40-q12-a25-h19-s32-0f54051d0d14`, compressed source SHA `2629edef151e8bf0cb366edc3bc5876bbd5c09d59e1785670848a6ce12c5d82e`, and uncompressed SHA `0f54051d0d1400c9944688f9aaf1db4a65177b548609da424c98fe5172f8595a`. All eleven copied module files, source entry, audit, construction map, and shared constants match the actual `normalized-linear-pole-result` artifact. Its independent arithmetic/source receipt is `LINEAR_POLE_5364_SOURCE_REVIEW.md`, SHA `f8feaa0584dc8da654baa04e8e3c0c6f864c0cb3b80c7548e778062f85925872`.

## Arithmetic composition

The first change is the reviewed general-E root construction: every root has integer doubled index `2Q=n_Q Pstar`, with base `R` satisfying `2R=Pstar`. This packet retains targets **4R and 4Q_i**. The later target-two proposal is excluded. The fixed target is `4R=2Pstar`, with the four rational binding rows in the root source contract and the retained field equations reconstructing the reciprocal abscissa and joint-chart coefficients.

The two beta-bearing modules test `C_A-2 beta`; the definition `beta=X^2+2`, scalar polynomial, scalar orders `[1,1,1,1,32,32]`, and four-witness anchor remain unchanged. The effective height constant is `5H19`; the proof still uses high order40, beta order12, and anchor25. The integer doubled indices of roots are distinct from the retained private `(1/2)Z via doubling` coefficient convention. The implementation records both conventions explicitly.

The root rewrite is bound to producer `5a9d82fdb68db591a275c67b2c555735e1376a6a86da21221d76976abd68d479` and independently reconstructed by literal checker `05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2`. The earlier independent implementation review (`dc4ef067e28770f3dce761ed8c00a74c3c1b00c2d67db5dc4109a78e00c232f5`) and checker review (`0171aa7b812c34ef26c483da4b7c443e340f1c5b82e1475c0cadf57c96fdd259`) cover the exact deletion incidence, mixed root charts, beta rows, and retained scalar/anchor uses.

The second change is exact: for `F=conj(fJ)=A+B sqrt(2)`, add `C=A^2+2B^2`, `D=2AB`. Replace the old local evaluation and norm equations by `P W=C+theta D`, with `P=r^2` and the same order1. This is a pre-squared coefficient interface for the original test of F; it is not a new order1 test of F squared. The deleted evaluation is reconstructed as `Y=A+theta B`. There is no division, including at zero values. Every norm value W, upper tree, private conic, and pole input is preserved. Consequently the already reviewed local orientation argument, negative odd exclusion, and theta-last completeness carry through unchanged. Field coefficients remain fixed before each private theta is chosen. Shared-square proof `378017d3ad813f69a0e6ee09c2de36f062fe2bd0e0b9c4c84a125eed99d84cc3` and independent arithmetic review `62af17f1d6e045d06ed32824bfc42918673d757fad4eaf8781940db03e1709d6` supply that exact identity and its source interface.

## Source checking and execution interfaces

The builder first produces and checks the complete exact normalized-ten parent. Only then does it apply the root rewrite and shared-square postprocessor, write the new module dictionaries, set the final chart metadata to `general_E_mixed`, and flatten. Thus the legacy chart10 setting used while reproducing the parent is not misreported as the new carrier.

The independent checker removes the shared-square layer, reconstructs every root/comparison change literally, and compares every other restored module with the selected parent. It also independently checks every selected parent module using the inherited normalized-Lucas/conic/anchor/pole specifications. A fabricated new root, wrong common field, hidden coordinate use, or changed scalar row cannot be accepted merely by editing provenance metadata. Current and historical file pins are distinguished: changed root/comparator hashes are checked through reconstruction, while the current unchanged scalar, anchor, parity, and shared files retain exact pins.

The source checker then uses the pinned full flattening checker with explicit module-instance counts and the final `general_E_mixed` header. It retains 37 private conics, 377 original field orders, and 340 local evaluation coordinates. The locator demands no old gpoint chart instances; the reduction runner removes the old chart/ordinate stages. The original scalar-height parity call remains separate from the 37 ordinary linear-pole calls.

The fresh-source mutation harness first checks the full proposed module set and then runs 109 shared-layer and delegated-parent mutations. The inherited 208-case harness is explicitly run on the selected parent; this is correctly described as inherited coverage, not as 208 fresh-root mutations. The exact root checker has its separate 92 semantic cases. Resource/deadline exceptions are distinguished from semantic rejection. These runner stages still require successful remote execution for a generated candidate.

## Independent small execution

`check_root_shared_outer.py` matched the actual parent files, applied both pure dictionary postprocessors, and called the complete composed module checker. It passed, then rejected three fresh mutations crossing the unchanged scalar, general-root, and shared-square layers. The resulting root has 260 private coordinates and 245 rows. These are module-local facts, not a forecast of the final quartic count.

Receipt: `ROOT_SHARED_OUTER_CHECK.json`, SHA `8ccda365f6baf70ba984f9b2140d22f21e764519ae6073527537e911c09943d7`. Runtime was 5.449 seconds. No flattening or replay was performed.

No implementation or mathematical-interface blocker was found. The final freeze manifest and emitted-source receipt must bind these exact files. All inherited external arithmetic obligations retain their earlier scope; the finite checker does not prove them. Neither a sub5000 count nor publication readiness follows from this review alone.

## Frozen packet addendum

The final manifest is `d308452e66f711d104b0b27db65313a66bee39a55b07072e3cdf248f868853c3`. All 154 listed files match their recorded sizes and hashes. All 13 external input pins match the corresponding files under `work/private-degree8-20261105/repository`. The reviewed code hashes above are unchanged. This closes the pre-run packet binding; the emitted-source and polynomial gates remain open.
