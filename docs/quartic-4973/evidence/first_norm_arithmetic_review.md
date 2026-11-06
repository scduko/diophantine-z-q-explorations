# First packed norm: independent arithmetic review

2026-11-06. **PASS for the proposed arithmetic change and exact subsequent fusion.** This is not a source-emitter or full-source acceptance receipt.

Reviewed proof: `batching/sub5000/first-norm-fusion/PROOF.md`, SHA `b18b32854d4ef6e8c49495ce404f7c96566a0a1926baca6f4ee1ed4cbedcba05`. Reviewed contract: `CONTRACT.json`, SHA `b327fcc99625f09c36509c6b22cb12edc4fdeb40c2f8a7b70f65f2509c75570c`.

Let the retained rational conic be `theta^2-r*s^2=2`. It implies both r and s are nonzero over Q. At an odd prime with odd R=v(r), delta=v(theta^2-2) is odd. Negative v(theta) would make delta=2v(theta) even; positive v(theta), or a unit theta without cancellation, would make delta=0. Hence delta is positive odd, theta is a unit, the prime splits, and the unique close root rho satisfies v(theta-rho)=delta. No common orientation across arbitrary source witnesses is needed.

For any field coefficients A,B, put `Y=A+theta B` and `T=Y^2-(theta^2-2)B^2`. The two summands have unequal valuation parity whenever finite, so there is no cancellation. If v(T)>=2e-1, then 2v(Y)>=2e-1 implies v(Y)>=e. Also delta+2v(B)>=2e-1 implies

`delta+v(B) >= e+(delta-1)/2 >= e`.

Thus `A+rho B=Y+(rho-theta)B` has valuation at least e. This covers arbitrary negative valuations of A or B; their integrality is not assumed. Infinite-valuation cases are consistent: if T=0, unequal parity forces both summands zero, and the field value is zero. The argument applies to general field values, not only globally square ones.

The existing virtual binary tree and one-sided linear pole still exclude negative odd R and give v(W)>-R for every leaf. They use the values of the virtual leaves and the unchanged tree equations, not the formula chosen to define the first leaf. For its order1 field, changing only that definition to W=T/r now gives v(T)=R+v(W)>0, hence v(T)>=1. The preceding argument with e=1 recovers exactly the required original field order. Every other denominator and order stays unchanged. The root, scalar-height, Lucas, beta, contact coverage, and both global contradiction arguments consume the same local conclusions as before.

For integer completeness, choose the same fixed indices, root/primary points, fields and raw contacts before theta. At each selected ordinary prime, the old depth-two approximation gives v(T)>=2 and the contact has R=1, so the new W is integral. The virtual constant-first tree remains a unit there. At the real and exceptional places, for fixed nonzero r and fixed A,B, W(theta)=T(theta)/r is polynomial in theta with rational coefficients. Its later norm-root value is continuous and finite near theta=3/2. The same approximation making 3-2theta small therefore gives the reviewed normalized linear-pole witnesses. This does not divide by a field value or a norm root, and requires no new prime-pattern input. For positive r the constant path keeps the real norm root strictly positive. Repeated contacts retain the original completeness orientation choices.

After this arithmetic denominator change, the fusion itself is exact over Q. From the virtual equations `rW=T`, `N=1+rW^2`, eliminate W to obtain `rN-r-T^2=0`. Conversely divide by the conic-proved nonzero r to restore W=T/r. The map preserves N, all higher nodes and all pole witnesses. Zero T, zero W, and even zero N for negative r are allowed. No division by T or N occurs. If the rational conic were dropped, the r=0 branch would be unsound; it must remain an explicit checker obligation.

The resulting first pair of equations is quadratic: `T-2AY+A^2-2B^2=0` and `rN-r-T^2=0`, with the unchanged definition of Y. The first leaf coordinate is now a packed numerator, not a norm leaf W. Its recorded type and only two permitted row uses must change accordingly. The other fields, all power definitions, higher tree rows, and the shared-square common-f(J) channel must remain exact. This is a new arithmetic source relative to the old denominator-r^2 source, followed by a rational equivalence to the virtual mixed-denominator source; it is not an arbitrary old-witness map.

No mathematical gap was found in the frozen statement. Required implementation gates remain: exact first-field/order/position selection in all three modes, preserved conic and higher tree, full outside-use check for the retyped coordinate, unchanged theta-independent field inputs, fresh flattening/replay, and final polynomial degree/coefficient/count verification. The claimed lift saving is a structural estimate until that work is complete.
