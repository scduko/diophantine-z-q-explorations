# Normalized-Lucas checker review

Independent static review passes. No blocking equation, branch, boundary
or coverage defect was found in the normalized comparison delta. This
review does not accept a generated source, a flattened stream or an
endpoint count.

| File | SHA-256 |
| --- | --- |
| batching/sub5000/normalized-lucas-audit/audit_normalized_lucas.py | 105f4cc79a85649041e95be4a9059ed93e1d296fb77e0937e612f54aa801bb33 |
| batching/sub5000/normalized-lucas-audit/test_normalized_source.py | b862d6d0959eb4b357d4a999228f6fb70f4ded5562e39542b8c65c593314c54c |
| batching/sub5000/normalized-lucas-audit/test_normalization.py | 88a684160db6fdfce700c830cd8ab702a42c87bac4f0601f38a5641428b819bf |
| precision/sub5000/normalized-lucas/NORMALIZED_LUCAS.md | e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811 |
| precision/sub5000/normalized-lucas/normalized_lucas.py | 3e1e420306de2fbe51c17aeb8f24169e23a9d74f47601262d3333360e7c7d921 |

I compared the complete checker delta with the previous local-Lucas
checker. The root reconstruction, mode specifications and dispatcher are
unchanged. The altered comparison specification maps s,t,z to point
indices 2,3,4 in the full mode and 1,2,3 in Lucas-only mode. It separately
retains the beta quotient at point 1 where present. Every B_i equation
uses the matching exact G polynomial and the same common Lambda.

The five reconstructed equations have the required signs and factors:
P B_s=p_s; (U+V)p_t=P B_t; K p_t=(1-2P)B_t;
V p_z=(1-2P)B_z; and E=U^2-KV-P^2. Both rational components are checked
after independent expansion of arithmetic definitions. The field passed
to the conic test is exactly E, at zero-based field position 7 in full
mode and position 5 in Lucas-only mode, with order 40. All primary f,
common f_J, alternate fields and their original order remain present.

The checker introduces no inverse of P,p_s,p_z or 1-2P. It therefore
preserves the intended p_s=0 and p_z=0 global branches. The unchanged
joint equations still recover the curve in those branches. At p_i=0,
x_i=+d or -d and the first difference denominator is 2 q x_i, nonzero;
its value is z=-q/(2x_i). Such a point fails the positive formal f_i
test at a consumed large prime, so the local divisions in the proof
remain justified. The case C_s=2 also remains present; no equation
divides by its vanishing factor 1-2P.

The normalization is a new input-projection theorem. The code and
metadata correctly say that the tested value is F/C_s^2, not F, and
remove the old blanket global numerator-nonzero assertion. Soundness
uses F=C_s^2 E with integral C_s; completeness separately avoids primes
dividing the already fixed nonzero integer s. The checker does not
pretend to prove that arithmetic input, and does not claim every old
private witness is transformed into a new one.

I checked the inherited core Module mechanism as part of the review.
Arithmetic labels authorize only acyclic definitions with a nonzero
constant coefficient of the new coordinate, not arbitrary hidden
constraints. Core labels, multiplicities, coordinate roles and every
ordered call argument are checked. An extra nonzero guard cannot hide
as an arithmetic inverse. Old root-input dependencies are forbidden.
The new evaluation metadata is compared with actual coordinate IDs,
including B roles, P,U,V,K,E and the order; labels alone do not establish
the equations. This still relies on the outer auditor pinning the core
and delegated checkers and checking the complete source and map.

The source mutation suite tests both components of every new equation,
the factor 2, changed numerator roles, missing B_s, replacement by E=0,
extra inverse constraints, normalized metadata and the actual ordered
E field. Ordered-field mutations synchronize metadata so they reach the
intended semantic checkpoint. Only the requested AssertionError counts
as a rejection; unexpected exceptions and resource aborts fail. The
root and batch checks remain in the full 208-case remote suite.

I ran only the tiny independent algebra test. It passed the exact
Laurent identity, 27 field examples including nine C_s=2 cases, two
zero-ordinate block fixtures, and degree-two/max-coefficient-four checks.
Those zero-ordinate fixtures are correctly described as block examples,
not full elliptic solutions. I did not generate modules or run the full
208-case suite locally. Fresh outer source auditing, flattening, lifting,
certificate replay and final coefficient checks remain necessary.
