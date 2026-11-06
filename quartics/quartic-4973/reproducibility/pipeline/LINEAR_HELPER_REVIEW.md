# Independent review of the direct and normalized linear pole helpers

Static review and the bounded helper tests pass. This is a review of the
two literal modules and their exact coordinate relationship, not acceptance
of a complete generated source or a measured variable count.

Reviewed files under parity/sub5000/linear-pole-next:

| File | SHA-256 |
| --- | --- |
| PROOF.md | 0b52a6ac4840636be12f455bf0e8b07ba02bb2308493d937afd840ea19bdb510 |
| spec_linear.py | 86789c5fd288d2c739659b1f15779d9c81599f84d54c14d7d26f17efe083603b |
| emit_linear.py | 19e7dc5b5516674dc972aa4b1e15c6b10725192d3f5e8bf48419dbdb93446878 |
| test_linear.py | 1f64ffa57b0ebc5e200e8d28bc7079c4d543abfbb75cba5486cf6ee7b410e1c4 |

The emitter's direct11 and normalized10 equations match the independent
literal dictionaries, including variable order, every row, empty call list,
labels, same-conic premise and r_normalized flag. The normalized form keeps
the field-independent inputs r,theta,W and uses l=(3-2*theta)W. The w row
is w-17e+cz, with c=re retained. Multiplying this row by r^2 and subtracting
17r times c-re recovers the direct row. The final conic scales by r^4;
q,j,k all scale by r^2 and s by r. No zero witness is excluded.

The new arithmetic argument is distinct from the old Cayley relation.
At every odd-valuation prime of r, the retained conic makes theta integral
and (3-2theta)(3+2theta)=1-4r*s_c^2 a unit, so both linear factors are units.
The direct/normalized equivalence only needs rational r nonzero, which the
same conic proves. The broader arithmetic proof has the separate review
arithmetic-audit/sub5000/LINEAR_POLE_REVIEW.md, SHA-256
885fa0233d3e739999ba0132a9bbae33f9eac53491945250fd08100751c685a3.
This note does not replace its inherited rank, simultaneous-realization or
completeness dependencies.

The test was executed with Python -E -B against archive builder
c7ef798894a106e3c6b02816583be2b6e966e4e701f73ee670c9a0de52a70912.
It passed 19 literal negative cases, nine symbolic scaling identities,
20 rational solution fixtures and 198 odd-valuation fixtures. Each module
has degree two and maximum coefficient 867. The receipt is
LINEAR_TINY_TEST.json in this folder. No full source or artifact was built.

An outer source checker must require the exact new pole name and literal,
the same r and private theta at all 37 ordinary calls, the exact existing
upper root W, and byte-identical retained batches outside the approved pole
metadata/call change. It must preserve all private conic/field constraints,
the scalar-height old parity module and the normalized-Lucas independence
contract. Its arithmetic acceptance must consume the new negative-odd
exclusion statement rather than claim unchanged Cayley witnesses.

The direct normalized10 form and the separate shifted-path11 proposal tie
in naive quadratic coordinate count. Their savings are alternatives.
