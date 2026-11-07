# Historical excerpt: off-filter

Origin in the research workspace: `work/quartic-version6-release/repository/docs/theorem-application-audit/evidence/closure-batch-007.md`

Full origin SHA-256: `2215f8d893a5823dae13efb51283181978d9117adb849b7785ffe6261ff836f7`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 17 to 29

```text
17: Fix an actual odd stage with moving prime `ell_0`. Let `F_o` be the finite elementary quadratic field cut out by the intrinsic odd label characters, and let `L_o = Gal(F_o/Q)`, with its actual coordinate relations. Let `F_e` cut out the fixed even label characters for `E^k`, and let `F_s` cut out all additional stationary quadratic tests. Put
18:
19:     F = K F_o F_e F_s,       H = Gal(F/K).
20:
21: All these fields are finite and Galois over Q. View H as the subgroup of `Gal(F/Q)` with trivial restriction to K. The actual common alphabet is the image of H in the retained odd, even and stationary coordinate groups. If the coordinates omit a redundant character, take this image rather than asserting that H itself embeds. This definition retains all relations among the coordinates.
22:
23: The even alphabet used in this construction is
24:
25:     L_e = image(H -> Gal(F_e/Q)).
26:
27: Equivalently it is the image of `G_K` in the fixed even label group. Enlarging the finite field F by `F_o` or `F_s` does not shrink this image: every automorphism of `K F_e` fixing K extends to the finite normal extension F. Thus the common-to-even projection is surjective by construction. This is the alphabet of individually K-split primes, not a claim that every unrestricted even label is K-split.
28:
29: This restriction is legitimate for the actual consumer. The even seed in lines 2479-2504 and 9881-9889 is specifically proved to consist of K-split primes. Restriction preserves the coefficient rules: the permitted types form a subgroup, contraction adds two types in that subgroup, and primary type zero belongs to it. The coefficient filter imposes total-label conditions rather than requiring every individual prime to satisfy the filter. In particular line 9975 explicitly does not impose the individual filter on the prime used in the nonempty-seed argument.
```
