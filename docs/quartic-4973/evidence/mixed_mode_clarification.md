# Correct denominator order in mixed comparison modes

2026-11-06. This clarification corrects an overstatement in the unpublished general-root and target-two proof notes. It leaves all frozen source packets and proof files unchanged. The old uniform order40 assertion is **not** proved for arbitrary beta-only source witnesses.

Affected frozen notes are `precision/sub5000/root-doubled-indices/PROOF.md`, SHA `ecdbfc9acd575a8ab194f8e76c356e7898544a506c705a40f169c6686c70a80e`, in the display for `(h-4)/j`, and `TARGET_TWO.md`, SHA `cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb`, section3 for `(h-2)/j'`. The same overstatement appears in `TARGET_TWO_REVIEW.md` SHA `d5048cc8ac8944d26c8af6d9b8cfcdd672ddee1beed73efaf3d634a53b012155`, and `TARGET2_IMPLEMENTATION_REVIEW.md` SHA `04aea447a4dd9cbae4ffe848e8b402252305014daebf1f117438a82b9ec8c9bd`. This note supersedes only those unconditional order40 phrases.

Let c be the target multiplier: c=4 for the general-root/target-four source and c=2 for target-two and its exact tangent refinement. Write `2X0=h Pstar`, `2Xi=m_i Pstar`, `2J=j_d Pstar`. In soundness the exact source orders are:

| Comparison mode | Denominator order e0 | Numerator orders e_i |
|---|---:|---|
| Full | 40 | beta12; each Lucas numerator40 |
| Beta-only | 12 | beta12 |
| Lucas-only | 40 | each Lucas numerator40 |

Thus the alternate tests imply

`v((h-c)/j_d)>=e0`, and `v((m_i-c*n_i)/j_d)>=e_i`.

The integer `j_d` is nonzero and locally integral, so `v(h-c)>=e0` and `v(m_i-c*n_i)>=e_i`. Since the consumed prime is odd and c is 2 or 4, h is a unit. Each integer n_i is locally integral. Therefore

`m_i/h-n_i = [(m_i-c*n_i)-n_i*(h-c)]/h`

has valuation at least e_i, because e_i<=e0 in every mode. The primary reciprocal-log approximation uses denominator precision e0 and numerator precision e_i, so it gives the same required `C_i=n_i mod p^e_i`. In beta-only mode every step needs only e0=e_i=12; no high-order or Lucas consumer is present in that mode.

The beta residual still yields `2beta=n_A mod p^12` for the doubled-index root variants. Full and Lucas-only blocks retain order40 for their denominator, so the first Lucas contradiction is unchanged. The second contradiction needs only beta congruences of order12 at its 21 supporting positions, and is unchanged. All height constants, anchor estimates, scalar orders, root targets and integer-denominator conclusions remain valid.

Completeness may continue to impose the stronger order40 congruence on its chosen multiplier at every occurrence. That constructs witnesses satisfying the weaker beta-only requirement, but does not justify a uniform order40 claim for arbitrary source witnesses. This distinction is the source of the corrected wording.

The actual emitted field lists already have these correct mode-dependent orders. No equation, coordinate, source hash, proof hypothesis, or polynomial changes. The shared-square identity, exact tangent deletion, and proposed first-norm change preserve these field orders and inherit this clarification. Their future arithmetic and publication inventories must include it when relying on the affected frozen proof text.
