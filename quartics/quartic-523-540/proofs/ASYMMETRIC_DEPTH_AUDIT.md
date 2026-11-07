# Independent audit of asymmetric formal depth

Reviewed `architecture/logarithms/PROOF.md` against the current V8 manuscript, especially the fixed-field weighted count (lines 18443–18461 of the inspected source) and final diagonal argument (lines 18738–18779).

## Accepted local argument

The primary parameter ratio z(U_i)/z(H) has the same valuation as the full formal-logarithm ratio u_i/h once both points are formal. The alternate truncated ratio has the same valuation as (u_i-n_i)/(h-1). Since at least one of h,h-1 is a p-unit, one full ratio is integral. An order-40 cross difference therefore forces both approximate ratios, and hence both full ratios, to be integral. Only after this step may one infer v(z(U_i))≥v(z(H))≥20 from the strengthened inverse-abscissa test on H. The two primary logarithmic corrections are then 1 modulo p^80; this gives the needed order-40 comparison without computing primary truncated logarithms.

All quotient domains remain justified. At an inert prime, conjugation preserves the unique valuation; the same bootstrap applies. The stronger beta congruence implies all prior order-12 consequences, so it does not weaken either inherited height contradiction.

## Accepted prime-separation argument

The source weighted prime count is S*NT+o(NT), with S a fixed positive constant after the coefficient and ray data are fixed. The final obstruction removal retains a fixed positive proportion at this scale. Its piecewise-constant diagonal τ(N)→0 may be chosen still more slowly so that

    τ(N) N^(1/6)/(log N)^k → infinity.

Indeed, for each fixed positive τ_j the extra inequality eventually holds, and its threshold can be included in the same recursive choice of N_j.

The discarded strip w<N^(1/3) contains O(N^(4/3)) integer pairs, and each product of k prime weights is O((log N)^k), so its total weight is o(NT). Thus a good pattern remains outside the strip after the original obstruction removal.

For distinct rational coefficients c_i,c_j, the correct spacing lower bound is

    |p_i-p_j| ≥ c_* N^(2/3), c_*=min_{i≠j}|c_i-c_j|>0.

The fixed factor c_* is essential in the literal inequality but harmless in comparison with the Hasse error O(sqrt N). All selected primes are asymptotic to the same u, so a selected p_i dividing any opposite reduction order d_+(p_j) would force equality for sufficiently large N. Distinct indices contradict the spacing; equal indices contradict divisibility of d_+(p_i) by four. Hence the added product of selected primes is coprime to the opposite modulus.

## Accepted completeness assembly

The added congruence h≡0 modulo P^19 M_minus is compatible with h≡1 modulo M_plus and the old continuity congruence modulo L. Selected primes exceed the primes dividing L, and the separation argument makes P coprime to M_plus. Multiplication by the doubling-image order first puts the fixed point in the formal group; p^19 raises formal-parameter valuation from at least one to at least twenty. The old real-progression argument remains applicable to the resulting, possibly enormous, integer modulus. The scalar constraints are preserved by the unchanged congruence modulo L.

The detector completeness asymptotics are uniform in the sense required here: the orders are fixed before choosing the prime pattern; the common large-real-parameter decay remains order λ^-3; and the small-prime valuation lower bounds grow with the previously chosen divisibility of w. No new global prime-pattern hypothesis is being silently assumed.

## Scope

This is an arithmetic refinement of the source: its witnesses and equations are not claimed to be in exact bijection with all old witnesses. Soundness and completeness use the inherited number-theoretic source results, plus the explicitly proved prime-separation consequence above. The remaining alternate truncated logarithms cannot be removed by asserting both h and h-1 are highly p-divisible.
