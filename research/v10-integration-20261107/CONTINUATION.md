# Checkpoint: integrate the new Version 10 baseline

7 November 2026. Started from fork
`be8f1b4f51c643bd460bc07ee7d7a84237722065`, last integrated upstream
`5856286a57fba19574a40704571ee70e79738281`. Contributor instructions and
current research notes were read. No AGENTS.md was found. The unrelated
untracked compiler temporary file was left untouched.

## Upstream discovery and integration

Fresh upstream head is `ba7a3e0a0c171b7cd2ce75976addba57fad8a5dd`.
Four commits intervene:

- `ec87719a71ebbab724bd2545cec44eb9ced42cdd`: Version 9 odd-product
  quartics and audited dependency chain.
- `79a00791183ce963aade764036daff8bf72bd6bc`: pinned Windows Python repair.
- `14e8f601fe0d9173d4a5f084aedc3e07066a7688`: include the pinned replay receipt.
- `ba7a3e0a0c171b7cd2ce75976addba57fad8a5dd`: Version 10 Issue 2 responses.

These were integrated into the fork without conflicts. The new contribution
is credited upstream to Gabriel Conant with ChatGPT. All prior research
files, the frozen 933 package, and rejected experimental evidence remain.
The old Version 8 manuscript is archived upstream with its original hash.
No historical input manifest required repinning.

## Actual verification

The full upstream check_odd_product.py passed: both source reconstructions,
exact certificates, final-package double replay, independent sparse-ring
checks, unchanged pinned files and coefficient-for-coefficient download
comparisons. Version 9 and Version 10 document/dependency bindings passed.
The Version 10 valuation regression passed 12,650 bounded cases. The
frozen 933 artifact replay also passed after integration. Fresh receipts
and relevant hashes are in VERIFICATION.json.

Initial document checks failed because the sparse checkout omitted
dependency files, not because the repository bindings disagreed. The
required tracked docs and construction paths were materialized and the
checks rerun successfully. No checker or pinned source was modified.

The baseline is now the upstream ordinary quartic: 540 variables,
509 residuals, 35,213 monomials, degree four, primitive content one,
maximum coefficient length 3,247 bits. The 523-variable form uses a
symbolic fixed coefficient and should not be compared as if it were
the same coefficient representation. JSON and text polynomial hashes
differ because their serializations differ; both are recorded.

## Arithmetic assessment and intuitive explanation

Inspected the odd-coset chart and squareclass argument, product-height
identity, shifted scalar/odd Lucas construction, asymmetric local
integrality argument and prime-separation/completeness proof. BLACKBOARD.md
explains the parity/no-cancellation mechanism and deeper-primary-point
mechanism, with exact labels mapping them into the full proof.

This is AI inspection of the changed interfaces, not independent human
review of the entire manuscript. In particular the common-witness
argument still depends on the full inherited prime-pattern estimates;
finite replay and inventory binding cannot certify those estimates.

## Further circuit research

The diameter bound extends the prior restricted eight-gate lower bound
to signed pure exponents: one monomial quotient can at most double the
available exponent diameter. Negative powers alone therefore do not
permit seven gates when the only mixed gates must output q12 and q40.

Upstream already uses a different eight-gate signed-power circuit.
Moreover, q12 is no longer a required detector output, only an intermediate
for q40. Thus preserving q12 is an obsolete constraint for future searches
on this baseline. No exhaustive mixed-circuit search or changed 540
polynomial was completed in this pass; the upstream integration took
priority after discovering the much smaller construction.

Next: optimize the single output q40=q1*e^78, permitting additional mixed
intermediates and using the unchanged norm proof of e,q1 nonvanishing.
Any candidate should first replay against the 532-coordinate precursor,
then receive new certified eliminations and full ordinary polynomial
comparison. Do not reuse the final 523-coordinate elimination certificate
unchanged if its source rows or coordinate inventory have changed.

PR4_DESCRIPTION.md now proposes metadata reflecting the 540 baseline;
the previous 924/900 draft is archived here. No upstream PR metadata write,
merge into upstream, message, or unsolicited comment was performed.
This checkpoint records one completed pass, not continuous execution.
