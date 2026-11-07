# Historical excerpt: templates

Origin in the research workspace: `work/astra-final-ordinary-definition-001/REPORT.md`

Full origin SHA-256: `154109196bdf6864d77542d52b5ae530fc25a5e54ec8fe486b17aff9f48ea345`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 139 to 151

```text
139: ## 8. Actual shared witnesses
140:
141: The independent checker reads the saved JSON. In main, N is coordinates 0-4, ordinary t is 5, and the single K is 6-10. BOTH calls use exactly
142:
143:   [0,1,2,3,4,6,7,8,9,10,5].
144:
145: Close's private block starts at 11 with length 292,890,196,199. Test starts at 292,890,196,210 with length 35,282. The intervals are disjoint. The shared shift is not two unrelated existential choices.
146:
147: Inside Close, A,L,J occupy 11-25; the five natural encodings occupy 26-50. Its signed-encoding calls start at 51,140705,281359,422013,562667, each of length 140654. The precision block starts at 703321 and uses those exact encoded inputs. The coordinate comparison uses the same A,L,J,t, not independent approximants.
148:
149: value_union multiplies exception and main branches; value conjoins membership; integers quantifies N and calls value(N,t). Inactive product-branch witnesses may be arbitrary rational values because all remaining expressions are polynomials with guarded inverses, not partial runtime divisions. In an active branch its globally conjoined fixed equations remain active. Zero-length blocks may share a start without sharing coordinates; the checker uses a multiset of (start,length,template), not a false uniqueness-of-start assertion.
150:
151: Every template/recipe is partitioned exactly into parameters, explicit witnesses and private blocks. Backward edges, call arities and declared variable counts are checked. These finite facts establish the literal quantifier layout, not the arithmetic meaning by themselves; sections 3-7 provide that meaning.
```

## Original lines 197 to 206

```text
197: ## 11. Corrections and remaining scope
198:
199: No correction to the candidate polynomial or its ordinary-integer equivalence was found. Four distinctions must be preserved.
200:
201: 1. V02:175-181 defines Q_pole with degree 75. Saved template pole has root106 = node105 squared, with node105 equal to Q_pole. In outputs/multiplication-certificate.js:22-32 the builder returns eq(Q_pole,0); outputs/rational-elliptic-core.js:27-29 wraps it in a one-conjunct and; outputs/integer-diophantine-compiler.js:124-134 squares conjuncts. Hence the saved degree is 150. Its unique degree-75 part before squaring comes from 9*e^4*A^10*B, so the degrees are exact, not just upper bounds. Both versions have identical rational zero sets and the same eleven witnesses. V06 correctly records root106 and the actual height-24 pole traversal includes the square. An optional explanatory sentence can distinguish the displayed polynomial from its automatically squared template; no mathematical repair is needed.
202: 2. The old degree-free CM claim in raw S09 and the height-two wrapper comment in raw S26 are not current premises. V02:109-160 and V05:128-135 explicitly repair them. The exact prime-pattern logarithmic exponent is 44.
203: 3. The generator enumeration and current JSON translation/size checks were rerun here. Full universal-polynomial regeneration was not. Earlier binding receipts remain finite evidence with their stated scope; section 6 independently reads and reconstructs the all-input compiler argument.
204: 4. RC is imported under the assignment's permission and remains separately reviewed. Primary verification of the external G/H/L theorems belongs to the concurrent producer audit. The absence of a new downstream counterexample does not establish global acceptance of the proposed resolution of Z in Q.
205:
206: The direct checks cover arbitrary rational tuples becoming typed before M; value-preserving C_nat translation with private power calls; both actual pole calls satisfying the exact PC domain; choosing Test's kappa before applying every-fixed-kappa Close completeness; and the same five shift coordinates in both literal calls. These are the downstream claims established here.
```
