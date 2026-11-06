# Combined comparison proposal: 1,267 variables with ordinary coefficients

**Status: additive research proposal; independent mathematical review pending.**
This combines the Version 5 source at upstream commit
`bf2fe53459c0cceff74566ea9b966eca54d11ca5` with the preserved Version 4
exponent-19 height theorem. The exact finite artifacts pass the upstream
independent algebraic checker. Their arithmetic interpretation is explained
in [ARITHMETIC.md](ARITHMETIC.md), subject to the inherited theorem inputs.

## Results

All counts include the input coordinate.

| Construction | Variables | Quadratic residuals | Quartic monomials | Coefficients |
|---|---:|---:|---:|---|
| Upstream Version 5 | 1,272 | 1,229 | 48,001 | Maximum $64\cdot3^{2^{28}}$ |
| Two scalar norm fusions | 1,270 | 1,227 | 45,936 | Same giant fixed-parameter convention |
| Fusions and comparison orders 12/40 | 1,250 | 1,207 | 45,430 | Same giant fixed-parameter convention |
| **Selected: orders 12/40, scalar order 32, smaller anchor and explicit chain** | **1,267** | **1,224** | **45,480** | **Ordinary integers; maximum bit length 4,059** |
| Earlier shared-comparison proposal | 4,151 | 3,986 | 19,910 | Maximum less than $2^{80}$ |

The selected polynomial has degree four and primitive content one. Its maximum
coefficient is less than $2^{4059}$, with every coefficient written explicitly
as an integer string. This improves the variable count and coefficient size
over Version 5 together. Compared with our earlier 4,151-variable proposal,
it has more monomials and larger coefficients; that remains a separate useful
tradeoff. No minimality claim is made.

The explored scalar-order-24 variant has the same counts and coefficient bit
length as scalar order 32. We retain order 32 because the lower order saves
no coordinates. [RESULTS.json](RESULTS.json) records all three experiments,
including their ordinary-coefficient versions and hashes.

## Changes and proofs

1. Implement the two scalar norm identities proposed in the upstream optimization
   report. These preserve the source projection and remove two gates.
2. Use the exponent-19 height bound to reduce comparison orders 16/52 to 12/40.
   The shorter logarithms remove twenty gates. A shared nine-multiplication
   chain computes both detector powers $e^{22}$ and $e^{78}$, avoiding the
   overhead of separate binary chains.
3. For the ordinary-coefficient variant, reduce the anchor constant from
   $3^{2^{27}}$ to $3^{2^{26}}$. Its label bound still exceeds $(40H_{19})^{10}$.
4. Encode this smaller constant with seventeen variables, starting at the
   explicit integer $3^{1024}$ and squaring sixteen times. The translated
   anchor remains quadratic. The constant chain is uniquely determined over
   the rationals, so it preserves the refined source projection exactly.

The arithmetic argument checks nonvanishing, split and inert logarithm estimates,
the two height contradictions, scalar completeness, and the common-point
construction. It retains the Version 5 quadratic prime-pattern theorem; our
earlier affine CPO lemma does not replace that stronger input. The source
qualifications and the reported Frei–Tinková local proof repair are retained.

## Reproduce

Requirements: Python 3.10 or later and Node.js 18 or later; standard libraries
only. Tested with CPython 3.12.14 and the Node version recorded in `VERIFICATION.json`.
From the repository root, replay the selected shipped artifact:

```sh
python3 -B research/combined-comparison/check_artifacts.py
```

Regenerate all variants in a new directory outside the repository:

```sh
python3 -B research/combined-comparison/explore.py --out /tmp/combined-replay
python3 -B research/combined-comparison/verify_variants.py /tmp/combined-replay
```

`explore.py` checks [INPUTS.json](INPUTS.json), applies narrowly matched changes
to a temporary copy of the upstream builder, and runs the unchanged compiler
and independent checker on each result. Original gate definitions are retained
and checked, including in the constant-chain source. All coordinate eliminations,
row normalizations, complete sum-of-squares expansions, and coordinate maps are
replayed. No original manuscript or generated upstream artifact is modified.

The compiler's intermediate JSON format retains an unused declaration of the old
fixed parameter for checker compatibility. The ordinary export removes that
convention entirely. `check_artifacts.py` adapts only this metadata and verifies
the same explicit coefficients against the residual squares.

## Shipped artifacts and scope

[ARTIFACTS.json](ARTIFACTS.json) pins compressed and uncompressed bytes of six
files under `artifacts/`: the parameter source, the constant-chain source, the
compiled residuals, reduction certificate, coordinate map, and complete ordinary
polynomial. Gzip compression changes storage only; it does not encode a symbolic
coefficient. The ordinary polynomial's SHA-256 is
`b4db1d6b35d260fc68a2e49c82b5b61ff373a9584dfcd13446e1c98e40171496`.

[VARIANT_CHECKS.json](VARIANT_CHECKS.json) records separate checks of the chain
transformation, exact arithmetic budgets, detector exponent identities, exported
coefficients, and rejection of an incorrect chain constant. The upstream checker
is independently implemented from its builder/compiler; this does not make the
new arithmetic argument independently reviewed.

The source architecture, detector construction, and original compiler/checker
are credited to the upstream Brox reconstruction under Elliot Glazer's direction.
The scalar fusion identities are explicitly suggested in its optimization report.
The present combination, lower-precision derivation, addition chain, constant-chain
specialization, and orchestration/checking scripts were developed with AI assistance
under the repository owner's direction. The earlier proof and artifacts remain
unchanged. No human referee acceptance or Lean formalization is claimed.
