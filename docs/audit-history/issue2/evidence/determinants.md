# Historical excerpt: determinants

Origin in the research workspace: `work/astra-final-rc-limits-independent-001/REPORT.md`

Full origin SHA-256: `ce431d308658d891f8a90c1d79f006c1dfd52500341a1dc264e3fb7255ad6ec4`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 159 to 185

```text
159: Fix p!=(2). Local acyclicity, H0 detection and duality kill fiber H0 and H3. Unit cancellation gives a free two-term DVR model. If the generic class is zero, the specified class-functional coordinate is zero. Otherwise generic rank is one and its kernel is saturated in the free source. A primitive generic kernel vector therefore reduces to a nonzero fiber vector. When the fiber dimension exceeds one, section 8 supplies a new prime, including this vector. In the nonquadratic or both-sign case finite localization is onto the two-dimensional finite plane. The exact self-annihilator image contains that plane and must equal it. The strict kernel has dimension s-2; the singular switch adds no localized vector and hence lowers s by two. In the one-sign exceptional case first use its dimension-preserving switch.
160:
161: Generic nonzero localization and the derivative relation make the new generic kernel rank one and preserve the determinant valuation by section 9. After each switch its primitive generic vector again survives in the fiber. Thus a putative drop below one is itself impossible. The finite process ends with fiber dimension one. A minimal model has one term in degrees one and two; its differential is zero because its generic kernel is rank one. Its actual class and the locally constructed functional are integral, so its determinant coordinate is integral. Reversing the exact switches proves v_p(u_prim)>=0. Since u_prim belongs to Frac(Lambda) and Lambda is normal, intersection of all these height-one localizations gives u_prim in Lambda[1/2]. The argument includes a base of full Selmer corank one: the complementary twist has rank-zero Selmer by the forward theorem, so central dimensions are (1,1), and semicontinuity gives generic dimensions at most one. Divisible Sha at that unknown base is not discarded.
162:
163: For the outer bound start instead with a contrary sequence of KNOWN SIMPLE-ZERO instances v_(2)(u_j)<-j. At each instance the nonzero central point, including its bounded nonzero trace multiplier, forces generic kernel rank one; central dimension one bounds it above. Minimalize over O_j. Residual H0 is zero by moving inertia, H3 is zero by duality, and the ranks in degrees one and two are equal and bounded. Fix the square size n on an outer-large set.
164:
165: Choose a primitive v_j in each actual generic kernel. Some coordinate is a unit on a large set, hence v_infinity is nonzero. The actual arithmetic vector A_j may be a multiple a_j v_j with v2(a_j) tending to infinity. The proof never requires A_infinity to be nonzero. If outer kernel dimension s>1, the rank-two evaluation includes v_infinity and an additional possibly approximate cycle. Section 6 realizes it by exact original-map equalities; section 7 legitimates the approximate cycle. On an outer-large set f(v_j) is generically nonzero, and hence so is f(A_j), because a_j is nonzero for each actual simple-zero instance. The exact switch preserves EACH inner determinant valuation. Over the outer field it drops dimension by two. Re-minimalize integrally and repeat with new primitive kernel vectors. There are only finitely many drops; N(E,A,j) for each fixed number of switches suffices. No uniform bound for an unbounded string is used.
166:
167: At terminal outer dimension one, D_infinity has rank n-1. Choose one nonzero (n-1)-minor THERE. Its inner determinants Delta_j have a common finite valuation b on an outer-large set. Nonzero inner minors chosen independently would not suffice: they might all tend to zero. The case n=1 uses the empty minor 1.
168:
169: Reorder D_j=[A B; C d] with A that minor. Generic rank n-1 gives d-C A^-1 B=0. Determinant-one triangular row and column operations isolate A and a zero line. The surviving cycle coefficient alpha is its original last source coordinate, hence integral. The surviving functional coefficient beta is its value on the original last target vector, hence in 2^-a O_j. The determinant tensor is EXACTLY
170:
171:     u_j=+/- alpha_j beta_j / det(A_j),
172:     v2(u_j)>=-a-b.
173:
174: The possibly nonintegral Schur operations do not create a hidden denominator in alpha or beta; this follows from which source column and target row they fix. The finite b may depend on the contrary sequence and its ultrafilter. Intersecting its large set with the cofinite set j>a+b contradicts v2(u_j)<-j. This proves qualitative existence of C(E,A), not a numerical value of C and not a uniform bound for an arbitrary chosen minor. It also does NOT apply this simple-zero bound to the unknown base.
175:
176: ## 11. Central specialization, Tor, and the unknown-base distinction
177:
178: RD892–933's lemma assumes both an actual cycle and an actual closed functional over A=Lambda_(t). Constant generic and central dimensions alone do not make an arbitrary rational functional regular. The correction note restores this necessary distinction. Section 9 constructs the A-functional using actual local acyclicity and the same generic inverse, so the lemma does apply to the coordinate at issue.
179:
180: For a bounded free C, derived central reduction is termwise reduction and has the exact sequence
181:
182:     0 -> H^i(C)/t -> H^i(C tensor^L Z2)
183:       -> H^(i+1)(C)[t] -> 0.
184:
185: Diagonalizing over the DVR A gives unit disks, nonunit t-power disks and free zero terms. Each nonunit disk would add a central cohomology class in each of two adjacent degrees compared with the generic fiber. Constant dimensions (1,1) and zero elsewhere exclude all such disks. The tensor of the actual regular cycle and regular functional therefore specializes to their central tensor. Integral two-primary torsion still contributes to the determinant over Z2; it is not removed by this rational t-adic argument.
```
