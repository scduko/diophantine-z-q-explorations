# Version 4 integration review

Reviewed on 2026-11-06 by the coordinating agent. This is an integration review,
not an independent repetition of every inherited arithmetic argument.

The final reviewed manuscript is `quartic_4973.tex`, SHA-256
`2cb539bdd7039eef9a8fe489ee3b153bfa2d0e74c26006b8da3c617aa815c32b`. Its mathematical integration was first reviewed at
`ed5734ceeeb92df2f9771812478a3b6cbb5edcff425457a8fb17bb42d5feb3e9`.
The sole subsequent edit adds a three-line preamble override widening contents
subsection numbers to 3.2em, so entries 15.10 through 15.12 do not touch their
titles. Every mathematical statement, proof, citation and displayed count is
byte-identical. The final PDF must be recompiled and visually checked.
The integrated selected appendix has SHA-256
`3d59f71d31c894b5641b8e806e421c9aee599ff50201fc598f725b12c49832ad`.
Its parent is revision 3 of the reviewed appendix, SHA-256
`e67b256be73b41fca2e74958ebf0f9749e78f5d98f0c05c06118d3d156defc85`.

## Reviewed changes

The exact `APPENDIX_INTEGRATION.diff` is retained beside this review. Changes
specialize the six explicit options to general roots, target two, direct
tangents, shared square and first norm, with scalar/J0 fusion excluded.
Section nesting changes and removal of inactive-option comments have no
mathematical effect. Citations to Version 3 become references to the retained
base compiler, height and reciprocal-logarithm proofs. The one Koenigsmann key
changes to `koenigsmann-defining`, the existing bibliography item for the same
paper. This is an explicit translation, not permission to ignore citation
differences in later checks.

The selected height argument now states only beta-prime = 2 beta and H-star =
5 H. Its proof, integrality conclusion and completeness choices retain exactly
that branch. In particular, 2 X^2 integral implies that the square of the reduced
denominator divides 2, so X is integral. Optional target-four and J0-inverse
arguments are not adopted.

The inserted scalar explanation uses the actual integer doubled indices.
The identity [2 j0]S = [2 s]J0 kills the possible two-torsion and justifies the
logarithm ratio at the tested primes, including inert primes where both rational
coefficients are tested. Integrality of j0 turns order 32 of s/j0 into the
required divisibility of s. The beta-height exclusions are valid: X^2+2 is not
0, 1 or -343/32, and 2399 is not a rational square. The anchor recurrence has
25 squarings, and its large terminal value is a witness, not a coefficient.

The inserted beta interface uses Lambda pH = GH, BA = CA pA and BA Lambda = GA.
Nonzero GH and GA force Lambda, pH, BA and pA nonzero. Thus CA is the ratio of
the two negative-logarithm approximations. The denominator precision is 12 in
beta-only mode and 40 otherwise. This argument is not used to exclude the
permitted zero ordinates of normalized Lucas numerators.

The retained H19 and reciprocal-logarithm proof spans are byte-preserved apart
from line-ending normalization. The rational 37-contact proof uses the eight
fixed rational abscissa coefficients, not membership of roots in 2E(K).
Its integration therefore allows nontorsion roots of E(K), while the subsequent
height argument uses their integer doubled indices. Completeness now cites
the selected private conic and linear-pole constructions, rather than the old
ordinary-pole predicate. The scalar pole predicate is unchanged.

The new selected-source theorem assembles the existing local deductions in the
required order. Soundness starts at arbitrary odd-contact primes, without
assuming ordinariness. Completeness fixes roots and the nonzero Lucas index s
before excluding its prime divisors, then fixes one common J, then private
points, then conics and pole witnesses. The first-norm change is an arithmetic
source replacement followed by an exact coordinate fusion. It does not assert
equivalence of arbitrary old and new private witness tuples.

The finite proof explicitly separates fresh defining lifts, reversible rational
row operations, constant-pivot relation eliminations, contact-power circuits
and the single inherited height-parity replacement. Contact-power identities
are valid at r=0; the first-norm source fusion instead uses the retained conic
to establish r != 0. Relation elimination divides only by nonzero rational
constants and retains its support equations. The all-one sum of squares has
the same rational zero set as the final residual system. No assertion that
every ambient coordinate occurs was added.

## Scope and disposition

The selected exposition, specialization and newly inserted assembly arguments
are accepted for this exact manuscript. This does not upgrade the inherited
source-version qualifications or the proof status of the original arithmetic
inputs. The three independent revision-3 reviews remain reviews of their
original text; this separate record covers the integration changes.

The final finite metrics must be supplied by the separate source audit and
complete certificate replay. Fresh reproduction and PDF inspection are separate
release checks. This document does not mark either of them complete.
