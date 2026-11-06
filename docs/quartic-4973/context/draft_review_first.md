# First-half draft revision 3: PASS

Reviewed the exact immutable file
`precision/sub5000/publication-draft/revision-3/CONTENT.tex`, SHA256
`e67b256be73b41fca2e74958ebf0f9749e78f5d98f0c05c06118d3d156defc85`,
through line 507, the end of the two height contradictions.
`DRAFT_BINDINGS.json` has SHA256
`b404299941e2e92584c5a2badecd694d170bad8e1dfa0f27564e636074038e05`.
Both byte hashes were checked locally.

This closes all findings in `DRAFT_R2_FIRST_HALF.md` for this scope.
The prior proof-step review and its independence disclosure remain part of
this receipt. It accepts the first-half exposition relative to its stated
inherited hypotheses; it is not a full-manuscript, later optional-section,
emitted-source, polynomial, or publication acceptance.

I compared the complete revision-2/revision-3 diff and rechecked the changed
mathematical passages against the pinned author proofs:

- The joint chart now explicitly restricts the primary point to an affine
  point with nonzero abscissa and finite difference parameter. This agrees
  with the recovered relation xf=1; it does not exclude the valid zero
  difference or p=0 numerator cases.
- The fixed-U argument now states and derives the positive squarefree
  representatives' congruences, disjoint supports and mutual-square
  conditions. Outside the exceptional primes, odd support of B forces
  positive valuation of U0^2/B; odd support of V forces equal valuations
  and strict cancellation. The U0=0 case is handled by eta_sf=1.
  These are the actual inherited realization premises, with no altered
  rank or restricted-converse assertion.
- The application b=rW^2 now proves its square reduced denominator from
  r=d0^2*p0 and the selected-prime unit condition on W. Its local-square
  conditions at 2,3,17 are also stated. The subsequent approximation
  preserves that unit condition while imposing the pole smallness bounds.
- The forced V=0 statement is restricted to consumed places where p_z is
  nonzero. The allowed global p_z=0 branch is now expressly distinguished.
  No division by 1-2P has been introduced.
- The height theorem explicitly retains integer root indices, s,z nonzero,
  and the two beta conventions. The large-a assumption supplies |s|>=7
  before the Lucas lemma is used. The two exponent expressions and the
  Koenigsmann proof-Facts citation are corrected.

No other first-half mathematical change appears in the diff. The conic
valuation/tree reasoning, linear-pole negative-odd proof and witness
scalings, four-witness anchor, normalized-Lucas identity, mode-dependent
40/12/40 denominator orders, and height estimates remain as checked in the
revision-2 review. In particular, the final bound is still
`log B < 31a/200 < a-3`, and the reduced-denominator argument for
`2(X^2+2)` correctly yields v^2 dividing 2 and hence v=1.

No outstanding correction remains in lines 1–507 at this exact hash.
Changes later in the file were visible in the diff but are outside this
first-half acceptance.
