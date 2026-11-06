# Independent shared-leaf review

PASS for the mathematical rewrite and proposed source contract in
`batching/sub5000/field-bookkeeping`. No emitted replacement source or new
endpoint is accepted by this note. `CHECKS.json` binds all five reviewed files
and the nine actual parent inputs by SHA256.

The independent check was run with CPython using `-E -B`; it does not import
the author's census or test. It checks the actual source incidences and the
polynomial identity. The author's separate tiny test also passes. No source
generation, final expansion, or remote job was run.

## Exact maps, signs, and zero cases

The selected field is `F=conj(f(J))=A+B*sqrt(2)`. In the pinned actual root,
`A=root[200]`, `f(J)_1=root[201]`, and the retained equation
`root[230]+root[201]=0` gives `B=root[230]`. Hence the shared square must be

    C=A^2+2B^2, D=2AB,

so in terms of the unconjugated pair `(a,b)`, `D=-2ab`. The minus sign is
essential. Both original coefficients and their equations remain in the root.

For each private theta, write the old residuals as

    R_y=Y-A-theta*B,
    R_w=P*W-2A*Y+A^2-2B^2.

With `R_C=C-A^2-2B^2` and `R_D=D-2AB`, the new residual satisfies

    P*W-C-theta*D = R_w+2A*R_y-R_C-theta*R_D.

Forward, assign the two shared squares once and delete each local Y. Reverse,
assign `Y_j=A+theta_j*B` independently at all 37 contacts and discard C,D.
The identity and the defining rows give every deleted/replaced equation.
Every other coordinate, including each W, remains identical. These are
polynomial maps with no division or domain restriction: A, B, P, r and W may
vanish. There is no equality requirement between different theta choices.

This is the original order-one norm numerator evaluated using its shared
square coefficients. It is not a change of tested field or order. A generic
ordinary-field handler applied to C,D would square the numerator again and
would be incorrect. The contract expressly requires the pre-squared channel.

## Actual source boundary

The parent census is the measured `normalized-lucas-result/source`, with
survival recorded at `normalized-lucas-power-result/coordinates`. It is not
an assertion that the newer linear-pole source already has this rewrite.
Any integration on a later source must bind that selected parent and verify
the same boundary again.

The independent source scan checks these exact occurrences:

| Comparator | Calls | Free slots | Field | Batch slots | Deleted Y |
| --- | ---: | --- | ---: | --- | ---: |
| q_compare4 | 13 | 21,22 | 5 | 11,12 | 41 |
| q_compare_beta | 8 | 9,10 | 2 | 5,6 | 21 |
| q_compare_lucas | 16 | 16,17 | 4 | 9,10 | 33 |

All 37 root pairs are exactly `(200,230)`. Each comparator pair has no
residual use and exactly one argument use per component, at its designated
batch channel. Within each batch, A and B occur only in the two specified
old rows; Y occurs only in those rows and in no child call. The existing
power has the literal equation `P-r^2=0`, and both recorded field orders are
one. Thus retyping those inputs does not alter another field or consumer.

The source contract requires exact retention of W and its upper-tree
position, all other field rows, powers, private conics, literal-one leaves,
and pole inputs. It also requires full variable/row/metadata renumbering,
fresh root coordinates, and a complete reconstructed-parent check after
the two root square definitions have been verified. These obligations are
necessary; merely matching the new leaf equation or new module hashes
would not establish the rewrite. The listed negative cases cover wrong
conjugation, wrong pair or order, double squaring, foreign theta, hidden
Y uses, changed W/tree placement, and incomplete renumbering.

## Degree, arithmetic composition, and count

All three new row types have total degree at most two and coefficient
magnitudes at most two. The cubic terms that occur in the displayed ideal
identity cancel; they are not emitted residuals. No additional lift gate
is needed for the shared C,D definitions.

Because W is identical for every choice of theta, the rewrite preserves
all parent valuation, sign, approximation, and pole arguments literally.
The shared coefficients are fixed with f(J), before any private conic is
chosen. It introduces no new arithmetic input and makes no new assertion
about the old full-Psi versus newer one-sided pole semantics.

At source level the delta is exactly 37 private coordinates removed and
two root coordinates added, a net reduction of 35. The same row delta is
minus 35. The old Ys are recorded as live in the measured endpoint, but
the final optimized delta and global coefficient bound still require a
fresh full pipeline replay. No 5275-variable artifact is established here.

Independent checks: all nine source/census pins match; exact source
incidences pass in all three modes; the coefficient-level polynomial
identity passes; 243 rational residual assignments include zero powers
and coefficients; 37 different theta choices share the same conjugated
square correctly. The author's 625-assignment symbolic test also passes.
