# Independent shared-square composition review

Date: 2026-11-06. PASS for the exact mathematical rewrite and proposed interface. The emitter, source checker, complete incidence and final endpoint remain separate obligations.

Reviewed `batching/sub5000/field-bookkeeping/SHARED_SQUARE.md`, SHA-256 `378017d3ad813f69a0e6ee09c2de36f062fe2bd0e0b9c4c84a125eed99d84cc3`, and `SOURCE_CONTRACT.json`, SHA-256 `13f97f687a15f1d0bf283b608c8c00b425c2c4797eb9b4dc0df14fa2a93c3750`.

For the original shared field F=conj(f(J))=A+B sqrt(2), set C=A^2+2B^2 and D=2AB. The old two rows are R_y=Y-A-theta B and R_w=PW-2AY+A^2-2B^2. With R_C=C-A^2-2B^2 and R_D=D-2AB, direct expansion gives

```
PW-C-theta D = R_w+2A R_y-R_C-theta R_D.
```

Consequently each old solution extends by the unique C,D, then loses Y; each new solution reconstructs Y=A+theta B and loses C,D. These maps fix every remaining coordinate, including the input and W. There is no division or restriction on A,B,P,r,theta or W. In particular P=0 and F=0 introduce no exception. The new equations are quadratic, with maximum residual coefficient two.

The conjugation sign is correct: if the original f(J) is a+b sqrt(2), then A=a, B=-b, C=a^2+2b^2 and D=-2ab. The interface must carry coefficients of the square of the original tested field, not silently reinterpret that channel as an ordinary field to be squared again. The original field order remains one and the power remains P=r^2. The rewrite neither doubles that order nor weakens a square valuation test.

This is stronger than a new integer-completeness construction: it preserves every rational source solution under the stated incidence conditions. Thus all prior local arguments, including negative odd raw contacts, the selected root orientation and zero pole branches, follow by reconstructing the exact old solution. The original W is unchanged at every occurrence. The real nonnegativity and local-unit properties of that W therefore remain the old ones. There is no new approximation requirement or arithmetic theorem.

Completeness keeps the original order of choices. F is root data, so C,D are fixed before all private conics. The function W(theta) is identical to the original function after substitution. Both the old conic-conditioned pole and the separately reviewed linear-unit pole may therefore be composed with this rewrite, provided their equations and exact r/theta/W inputs remain unchanged. No relationship between different private theta orientations is required.

The proposed mode slots are consistent with the typed original interfaces: full slots21/22 feed field5, beta slots9/10 feed field2, and Lucas slots16/17 feed field4. Each is the common conjugate-f(J) field of order one. The original A,B and all their root consumers must remain. The new source checker must independently establish their identity and conjugation, the two global square rows, every changed call, absence of outside use of each deleted Y, and full row/coordinate/metadata remapping. Reconstruction of a parent view must be justified by these equations before invoking its checker. Hard-coded census IDs alone would not establish the claim for a later root source.

I ran the bounded exact identity test. It passed its symbolic polynomial identity, 625 rational assignments, two zero-power cases, conjugation check and example showing that a normalized-Lucas residual need not be rational. No complete source was generated. The forecast of 35 fewer coordinates is not a verified endpoint count, and the final sum-of-squares coefficient bound still requires replay and expansion.
