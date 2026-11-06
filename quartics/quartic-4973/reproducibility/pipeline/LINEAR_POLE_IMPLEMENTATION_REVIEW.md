# Independent normalized pole implementation review

Date: 2026-11-06. Verdict: PASS for the literal helper and its typed contract. This is not an emitted-source or endpoint acceptance.

The reviewed packet is `parity/sub5000/linear-pole-next/MANIFEST.json`, SHA-256 `919e7a3c5e22c7138cdbe82e63a8a687e85b8040d3e73624b701d2db2e1db8bc`. I checked all eight listed file sizes and hashes. The arithmetic proof remains `0b52a6ac4840636be12f455bf0e8b07ba02bb2308493d937afd840ea19bdb510`, independently reviewed in `LINEAR_POLE_REVIEW.md`, SHA-256 `885fa0233d3e739999ba0132a9bbae33f9eac53491945250fd08100751c685a3`.

The exact implementation bindings are:

| File | SHA-256 |
|---|---|
| `NORMALIZED10_CONTRACT.json` | `19c3f7d65aae9f38aeaea9cc9c079d0ec7ca9918123d96d1744813ae81e61869` |
| `emit_linear.py` | `19e7dc5b5516674dc972aa4b1e15c6b10725192d3f5e8bf48419dbdb93446878` |
| `spec_linear.py` | `86789c5fd288d2c739659b1f15779d9c81599f84d54c14d7d26f17efe083603b` |
| `test_linear.py` | `1f64ffa57b0ebc5e200e8d28bc7079c4d543abfbb75cba5486cf6ee7b410e1c4` |

## Equations and checker

The normalized module has free slots `[r,theta,W]` and ten local slots `[l,z,e,p,c,w,s_p,q,j,k]`. Its eight residuals are exactly

```
l-(3-2theta)W,
z-l^2,
c-re,
p^2-17r-34c+51ec,
w-17e+cz,
j-s_p^2,
k-rq,
j^2+34jw-867w^2-17qk.
```

Substituting the defining rows gives precisely the normalized ten-variable theorem. In particular the sign in `w=17e-cz` is correct. Every residual is quadratic and the largest absolute integer coefficient is 867. There are no hidden inverse rows or calls. The direct eleven-variable form is also consistent with the proof's scaling by the nonzero raw contact r.

The independent specification enumerates every monomial, slot, row, variable label, metadata field and call list. Its comparison is whole-module canonical JSON equality, with nonfinite numbers forbidden. It does not import the emitter. I inspected both literal row lists and ran the bounded test with the original builder pinned to `c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912`. Result: 19 negative cases, nine polynomial scaling identities, 20 rational solution fixtures and 198 odd-valuation fixtures passed. This test generated no complete source and replayed no quartic certificate.

## Actual arithmetic interface

The contract correctly requires the same r and theta in `theta^2-r*s_c^2=2`, all field coefficients fixed independently of theta, and the same W supplied by the full constant-left norm tree. At an odd valuation of r, this conic makes `3-2theta` a local unit. The new pole theorem excludes a negative odd valuation of nonzero `rW^2` outside 2,3,17. That one-sided assertion is sufficient for the ordinary comparison norm proof. It does not assert equivalence to the old full Psi predicate. W=0 and zero pole ordinates remain permitted; their treatment is included in the arithmetic proof.

Integer completeness uses the already reviewed simultaneous conic approximation: theta approaches the selected square root at the ordinary prime and 3/2 at the real, 2-adic, 3-adic and 17-adic places. With fixed field inputs, W(theta) is polynomial, so the required smallness follows. The fixed-U realization hypotheses and inherited arithmetic inputs remain necessary.

The requested replacement is only `q_conicpole(r,theta,W)` by `q_linearnormalpole(r,theta,W)` at the same 37 ordered argument triples. The original scalar-height parity call, its module and all six scalar orders must remain unchanged. Root, anchor, comparison equations, field orders, conics, powers and norm trees also remain unchanged. The contract states these conditions and does not claim a measured saving.

The merged producer, all actual call triples, source metadata, full module/flattening audit, and polynomial replay are still separate obligations. No whole-source conclusion follows from this helper review.
