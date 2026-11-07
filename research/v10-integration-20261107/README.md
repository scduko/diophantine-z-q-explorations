# Version 10 integration: use the upstream 540-variable baseline

7 November 2026. Upstream advanced from Version 8 at
`5856286a57fba19574a40704571ee70e79738281` to Version 10 at
`ba7a3e0a0c171b7cd2ce75976addba57fad8a5dd`. The four intervening commits
integrate Version 9's odd-product construction, repair its CI/replay
packaging, and add Version 10's responses to Issue 2. The fork integrates
these changes while preserving all earlier experiments and frozen artifacts.

## The baseline has changed substantially

| Construction | Variables including input | Residuals | Monomials | Coefficient bits |
| --- | ---: | ---: | ---: | ---: |
| Frozen fork proposal | 933 | 890 | 51,907 | 3,247 |
| Previous fork direct-target candidate | 900 | 857 | 51,252 | 3,247 |
| Current upstream ordinary quartic | 540 | 509 | 35,213 | 3,247 |
| Current upstream symbolic quartic | 523 | 492 | 35,163 | symbolic fixed S |

Both upstream quartics have degree four and primitive content one. The
540-variable polynomial is now the appropriate ordinary-coefficient
research baseline. These reductions belong to Gabriel Conant with ChatGPT,
as attributed upstream; they are not newly discovered reductions from
this integration pass. Version 10 changes source explanations and proof
conventions, not the Version 9 polynomial data.

Ordinary JSON polynomial SHA-256:
`b14e76dda63ea4bb8b012a89a4f052c73e19877b451633df6ee9c198b8d83571`.
The equivalent decimal text download has a different serialization hash:
`83e7a31e11f9ad2edc2f67935e50bff437d87ef4b77d37b6a4391e8117770680`.

## What changes mathematically

The upstream construction incorporates direct targets and the smaller
anchor, restricts four root labels to odd indices, replaces nine height
detectors by three through an exact product-height identity, and replaces
five primary logarithm truncations by local parameters at deeper formal
points. It also changes the input label to 2X²+3 and uses the shifted
scalar point S-P, so the scalar index remains sufficiently divisible.

These are not deletions of unnecessary equations from the old source.
They require the odd-coset chart, odd Lucas witnesses, product-height
argument and strengthened common-index completeness construction.
BLACKBOARD.md explains those interfaces and maps them to precise source
labels. The inherited deep arithmetic inputs remain in force.

## What was actually checked in this pass

- Rebuilt both source precursors from their frozen patches and builders.
- Ran final verifiers twice for each upstream package; checked exact
  eliminations, complete sum-of-squares tables and ordinary constant lifts.
- Confirmed the pinned package files were unchanged and text downloads
  agree coefficient-for-coefficient with the JSON tables.
- Passed Version 9 dependency bindings and Version 10 document bindings.
- Passed the Version 10 bounded valuation regression (12,650 cases).
- Replayed the historical 933 package successfully after integration.

VERIFICATION.json contains the fresh receipts and hashes. The initial
document checks encountered missing files in the sparse checkout; after
materializing the required tracked docs/construction files, they passed.
No source-file modification was needed to obtain those passes.

Run the upstream replay with:

```sh
python3 -B scripts/check_odd_product.py --out /tmp/v10-replay
python3 -B docs/quartic-523-540/inventory.py validate
python3 -B docs/manuscript-revisions/version10/check.py
python3 -B docs/manuscript-revisions/version10/check_valuation.py
```

The proof notes were inspected for the new parity, height, denominator,
and prime-separation interfaces. This was AI review, not an independent
human proof review or a re-proof of every inherited analytic estimate.
Document binding checks are not mathematical theorem verification.

## Which previous circuit improvements still apply?

The new asymmetric builder already contains an eight-gate Laurent weight
circuit. Its q12 is now only an intermediate for q40, since the detector
orders are 1 and 40. The fork's eight-gate positive-power circuit therefore
offers no gate-count saving by simple substitution. No changed upstream
polynomial is proposed in this pass.

The earlier restricted lower bound extends to negative pure exponents.
Let m and M be the least and greatest available exponents in a pure-power
circuit, and let D=M-m. A quadratic monomial quotient introduces exponent
a+b-c in [2m-M,2M-m]. Adding one such exponent can enlarge the diameter
by at most a factor two. Starting from {0,1}, five gates give D<=32,
even when some intermediate exponents are negative.

If the only two q1-dependent gates must output q1*e^22 and q1*e^78,
the first output cannot have exponent 78: it is a difference of available
pure exponents. After producing 22, the second output can shift that
exponent by at most 32, or combine three q-dependent factors to obtain
one of -22,0,22,44. None gives 78. Thus eight gates are still minimal in
this class. Allowing negative exponents alone does not evade the bound.

This does not bound a circuit whose first mixed intermediate has a
different exponent, whose q1 powers differ from one, or that shares
work with the norm and delta equations. In particular the new upstream
architecture need not retain q12 as an intermediate: optimizing only q40
is the relevant next target. No exhaustive search of that larger class
was completed in this pass.
