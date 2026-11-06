# Exact proof replacements and dependency changes

The reference text is the current `diophantine_zq.tex`, with the same labels
used in the accepted degree-eight packet. Section line numbers can move
when the manuscript is edited; the labels and quoted headings identify the
required changes.

| Current part | Required replacement |
|---|---|
| `eq:o8-contacts`, under "Forty-one contacts and one common comparison point" | Use eight arbitrary rational targets, the same fixed constants and the same list of raw forms. There are 37 positions. |
| Integer-target prime claim preceding `subsec:o8-pattern-proof` | State the rational-target lemma in `PROOF.md`: all finite contacts are ordinary primes, while the infinity contact is `D²*p0`. `D` is a chosen positive common denominator in the completeness proof, not a source variable. |
| `subsec:o8-pattern-proof`, first two paragraphs | Set `T=V0*D²` and `K_s=T*s`. Deduplicate all identical slopes, rather than proving that distinct target families are disjoint. There are at most 37 forms with independent linear parts. |
| Prime-pattern local argument | Add the denominator-prime case `q|D`, where all `K_s=0` modulo `q` and `u,p0` can independently equal 1. Retain the existing two-missing-slopes argument elsewhere. |
| Prime-pattern lower/fiber estimates | Include primes dividing `D` in the fixed cutoff. Use the same integer `K_s` fiber identities and order sieve. Complexity at most 35 suffices; the existing at-most-39 inputs already cover it. |
| Common `J`, private shifts and common root | Use the ordinary prime `p0` for the infinity occurrence, not the composite raw number `D²*p0`. No other change to the congruences or private witnesses. |
| Paragraph "The common root approximation and parity boundary" | Replace "every raw contact is a positive prime" by the exact square-times-prime statement. Verify parity completeness using the unit norm root at the unique odd-valuation prime and even valuations elsewhere. |
| Paragraph beginning "The nine rational targets" | Use the eight coefficients of `x(A),x(S),x(T),x(Z)`. Delete `e`, its inverse and all eight products `e*x`. |
| Shared height estimate | Two coefficient bounds give `<4H_*|N|^(24/K)+30<5H_*|N|^(24/K)`. The former `<7H_*|N|^(24/K)` bound remains available verbatim. |
| Final completeness paragraph | Apply the rational-target prime lemma directly to the chosen point coefficients. Do not choose a source witness `e`. |
| Source prescription and counts | Give the regenerated source its own source hash and measured counts. Keep the old source and its arithmetic review identifiable. |

The five-contact height theorem `hyp:o8-height`, the seven-witness parity
theorem `hyp:o8-pole`, the cyclic-group generator theorem, the formal-group
identities and the Lucas growth lemma retain exactly their previous
statements. The scalar batch and its correction bits are unchanged. The
raw comparison count decreases; the per-comparison rational test count is
still 41 and its precision is still 64.

The accepted sieve packet identifies the relevant application records as
OP01 through OP14 in `degree8-original/arithmetic/sieve/applications.json`.
OP02 must now deduplicate coincident slopes; OP03 gains the denominator-prime
case; OP04 uses at most 37 forms; OP05, OP06 and OP08 use the altered but
still fixed integer `K_s`; OP13 gains the square factor at infinity; OP14
must be checked against the altered source. The fixed constants, same-prime
CM order argument, shared-`J` CRT, logarithm soundness and common root
approximation retain their existing applications.

No new external theorem is required. In particular there is no claim about
coprimality of reduction orders at different primes. The earlier source's
arithmetic review limits and inherited inverse-theorem version convention
are retained, not upgraded by this proposal.

## Obstruction to merely deleting more contacts

For a generic eight-target tuple the 36 finite slopes are distinct. Choose
a large prime outside their denominator and pair-difference supports. If
one finite raw form is omitted, take `v=1` and choose `u` congruent to its
slope modulo `p` but not modulo `p²`. That form has odd valuation, every
other finite raw form is a unit, and the raw infinity contact is a unit.
The corresponding normalized contact is missed. If the shared infinity
form is omitted instead, choose `v=p`, `u=1`; every finite form is a unit
while all slopes have odd infinity depth.

Thus all 37 positions are needed by this particular unrestricted raw-form
coverage argument. This is not a lower bound for arbitrary Diophantine
definitions or an assertion that deleting a row necessarily gives a false
global predicate. Fewer contacts would need an additional coverage identity,
a different height representation, or a new arithmetic argument.
