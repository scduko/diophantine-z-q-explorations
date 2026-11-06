# Independent review of the four-witness anchor

Date: 2026-11-06. Arithmetic PASS for `parity/sub5000/ANCHOR_FOUR_PROOF.md`, SHA-256 `9d349ae5caaaa9ed4433617762ecb4b8b349af58c2082ffa4b9be08442ba18e3`. This improves on the separate six-witness proposal. It gives exactly the old rational projection on f0,f1,C when C is the retained nonzero anchor constant. It is an arithmetic source equivalence, not a polynomial-identity elimination or a rational choice of quaternion witnesses.

The published trace convention and local-global facts were independently checked against the [publisher PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v183-n1-p02-p.pdf) for Koenigsmann, *Defining Z in Q*, Definition 4, Observation 5, and the proof of Proposition 6, printed pages 75–77. The quaternion algebra is (2,3), ramified exactly at 2 and 3, split over the reals. Its trace is 2x0, and its norm is x0^2-2u^2-3v^2+6w^2. At the ramified places its traces are integral and include the residue preimages of U2={1} and U3={0}. The global trace set is the intersection of the local ones. The new elementary step is the explicit extension from odd 2-adic traces to every trace divisible by four.

Let R=Z_(2) intersect Z_(3). For rational a,b set n=a^2+b^2 and h=9+3n. If h is a global trace, it is integral at 2 and 3. At 3, for m=min(v3(a),v3(b)) finite, the norm n has valuation 2m: unequal valuations cannot cancel, and equal unit squares sum to 2 modulo 3. If m<0, the term 3n has negative valuation strictly below v3(9), which contradicts integrality of h.

At 2, unequal valuations give v2(n)=2m, while equal finite valuations give v2(n)=2m+1 because the scaled unit squares sum to 2 modulo 8. If m<0, both possible valuations are negative, strictly below v2(9)=0. Thus h cannot be integral unless both a,b are integral. A zero coordinate has infinite valuation and is covered by the unequal case; both zero is immediate. No cancellation case is omitted.

Conversely, if a,b belong to R, h is zero modulo 3 and hence a local trace there. At 2, equal parities make h odd and therefore a local trace. Opposite parities give n=1 modulo 4 and h=0 modulo 4. For any such h, put x0=h/2. If x0=2 modulo 4, the unit (x0^2-1)/3 is 1 modulo 8; its 2-adic square root v gives norm-one coordinates u=w=0. If x0 is divisible by four, the unit 1-x0^2/6 is 1 modulo 8; its square root w and u=v=1 give norm one. Both calculations have exactly trace h, include h=0, and use only the elementary 2-adic unit-square criterion. Thus every case is a local trace at 2, and the published local-global equality supplies a rational quaternion. This proves h in S exactly when a,b belong to R.

The homogeneous equations are

```
C*H - 9*C^2 - 3*f0^2 - 3*f1^2 = 0,
H^2 - 8*U^2 - 12*V^2 + 24*W^2 - 4*C^2 = 0.
```

Since C != 0, the first gives H/C=9+3((f0/C)^2+(f1/C)^2). The second is precisely the trace equation for H/C with quaternion coordinates U/C,V/C,W/C. Therefore the new equations imply the old pair of semilocal conditions. The old equality T=R supplies the old witness tuples. In the forward direction the new criterion supplies a rational quaternion and multiplication by C gives H,U,V,W. This proves both projections for every rational input pair with the same external coordinates.

The module has four private rational variables, two quadratic residuals, and coefficient maximum 24. No auxiliary C^2 variable is needed because C^2 is a quadratic monomial in an existing source coordinate. The old terminal C must remain bound to its original nonzero repeated-squaring chain. These module counts alone do not establish a final optimized saving.

The exact old anchor condition is preserved, so its index cutoff and completeness choices remain unchanged. This replacement can compose with the three-mode, minimal-Jacobi, or reviewed four-field source without changing their arithmetic assumptions. The finite checker must still bind these literal equations, free-input order, terminal C, and private-coordinate incidence. A fresh source/lift/replay and full coefficient expansion remain necessary. The dependency inventory must record the explicit published trace facts and the elementary 2-adic construction; the old bare T equality alone is not a sufficient citation for the new criterion.
