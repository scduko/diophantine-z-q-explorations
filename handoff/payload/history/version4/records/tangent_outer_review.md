# Target-two direct tangents: arithmetic and integration

2026-11-06. **PASS at the exact module and pre-run source-integration scope.** An emitted source, its full replay and complete coefficient bound remain pending.

The packet is `source-pipeline/sub5000/target2-tangent-shared-square/`, family `H19-root37-target2-tangent-shared-square-normalized-linear-pole-v1`. The joint contract is `b0fd110ac30061022c8b293a816626ec753592a0cae6184a80ee2955c82b995d`. It applies only the four first-doubling tangent substitutions after the reviewed target2 root rewrite and before the unchanged shared-square pass.

| Item | SHA256 |
|---|---|
| Tangent proof | `3591709058c666a1dd2786d46039b408a04f1908b644c16c6f722a72788a50c8` |
| Tangent producer | `a136e6cce43277ed63351fd1989c428c48b811b9a8682d213f6609d6a95f5cb2` |
| Independent literal transition checker | `75299d5a1118dd7d75892786079003cd8588dc0b814017ae33c82672d00b80b0` |
| Tangent contract | `d9ef1fedd0703377747353f44619d73eca47c160634757de7c477fc02c887e70` |
| Builder | `3b91012293dc0605fefb8fdaf59596c72a683e0d10faba73eb0105022506ae8f` |
| Full source checker | `dc958ee4f3c94694cc97adb4b373b94fccfa79451f9e93e413b1f9ab2cd6d01c` |
| Composed module checker | `f8c5834802690da51e083119da6d7b2b2369601be0bef212b5191902f3425721` |
| Locator | `73e742af8a8b7cebc7e6a4c5363bfa2866934a77f79233a6bd11c92b43ea290f` |

## Exact rational equivalence

I checked the proof directly. With retained `q=x^2`, `y^2=x^3-Dx` and new `2y lambda=3q-D`, the polynomial identity

`(3q-D)(3q-2D)-9x(x^3-Dx)=2D^2`

gives `y[2lambda(3q-2D)-9xy]=2D^2`. Since `D=11-6sqrt(2)` has rational norm49, it is nonzero. Thus y is nonzero and

`h=[2lambda(3q-2D)-9xy]/(4D^2)`

is a rational field expression satisfying `(2y)h=1` and `lambda=(3q-D)h`. Conversely the old inverse and slope equations imply the new tangent equation. Forgetting h and restoring it by this formula are inverse maps on the retained coordinates. No root extraction, extra arithmetic theorem, local integrality assumption, or unexplained nonzero guard is needed. The other doubling equations are unchanged, so each target stays exactly `2Q`.

Consequently the reviewed target2 soundness and completeness apply without alteration. The integer doubled root indices, half-integer private coefficient convention, beta factor2, scalar beta and orders, anchor, H19 effective multiplier5, contact list, local orientations, pole argument and theta-last choices are unchanged. This particular tangent deletion is a genuine rational projection equivalence on the pinned target2 system, despite earlier source refinements requiring separate arithmetic proofs.

## Privacy, metadata and source composition

The canonical input root hash is `1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2`; the tangent output is `e8b115ac5150212db52dc0a013db4a7d4c36c647c4b07f8654b9e9712239fe95`. The producer checks the input hash, every old doubling component equation, and the retained curve equations. The removed inverse pairs 38/39, 48/49, 58/59 and 68/69 occur only in their own inverse/slope rows and never in calls. It remaps all remaining rows, calls and live coordinate metadata, including target/fixed-binding records. Old provenance keeps its own explicitly historical index systems.

I read the literal checker. It independently specifies the eight new scalar tangent rows and exact deleted sets, then compares the entire transformed root including all metadata. Its parent hash is enforced before transformation; bounded preflight and disabled-assertion rejection remain in force. The fourteen fixed-target binding rows are unchanged under the coordinate map. Their isolated sum-of-squares maximum remains154563475872; the root sum-of-squares constant increases by624. Neither isolated calculation is a complete quartic coefficient certificate.

The outer builder installs this fragment at the required position. The outer checker first validates the full exact normalized-ten parent, reconstructs the reviewed target2 root with the independent target2/base auditors, and then uses the literal tangent transition check on the restored root. The shared-square restoration remains outermost. All three comparison modules are independently checked against target2 specifications; every other module must equal the selected parent. The emitted source binds the new proof and tangent contract. Current metadata identifies four direct tangents and supersedes only the private first-doubling inverse pairs from the target2 contract. No target4 clause, old gpoint locator, or obsolete ordinate stage is introduced.

## Small independent execution

I ran the portable literal probe against the actual normalized-ten parent: 31 semantic mutations and one resource-abort case passed, along with the complete expected-root comparison and fixed-binding aggregation. Its receipt is `TANGENT_LITERAL_CHECK.json`, SHA `91738ec7a50b766c06d8ccf1d66e65b73f7c82f5096f096fe853ede58620cae8`.

I separately ran the complete actual-parent dictionary composition through the current outer module checker, plus three mutations of the unchanged scalar, root and shared-square rows. All passed/rejected as intended. The resulting root has212 local coordinates and197 rows after shared-square. Receipt `TANGENT_OUTER_CHECK.json` has SHA `22c3dc90e843dc20d6f47d01b4dcb480d64834ced23ced388774221a586885da`. No full source generation, flattening or replay was run locally.

The remote runner retains all parent and fresh-source checks and adds the 31-case tangent probe plus twelve actual-source tangent mutations. Their execution against a newly generated artifact remains required. No pre-run blocker was found.

Final freeze: manifest `34be9b53e29041d2cc22eaf43b1dc449399f5c5b62791308261bbbd2de949cd5`. All 171 packet files match their recorded sizes and hashes; all 13 external pins match their corresponding files under `work/private-degree8-20261105/repository`. The reviewed code is unchanged. This closes the pre-run packet binding only.
