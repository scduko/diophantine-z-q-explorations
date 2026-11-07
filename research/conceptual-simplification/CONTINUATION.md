# Conceptual-simplification checkpoint

7 November 2026. The fork main branch was fast-forwarded from
fef5fb2d7fc73798aeaca1017a3b3453253e1380 to upstream
036cebe4f1a4aa7ca89820a9b48f3629b4c364d6. The existing
combined-comparison branch and upstream PR #4 were left untouched at
4145131edb579440607cdeb1c3b0de5cee2fe19d. No further work is being
added to that pull. This work begins from a clean upstream baseline on
the separate conceptual-simplification branch.

The two new upstream commits add audit-history evidence and Issue 3
serialization documentation. They do not change the 523/540 polynomial
data. AGENTS.md and CONTRIBUTING.md were read. This research does not
reclassify a historical audit item.

## Main conclusion

A very short proof of the final existential theorem is already available
at the correct abstraction level: specify the finite quadratic source and
take the sum of squares of its rows. The expanded polynomial is unnecessary
for the proof, and the sum of squares is a canonical degree-four choice.

This does not shorten the arithmetic master proposition. The core
complexity comes from replacing a universal condition over denominator
primes by finitely many existential equations. The current mechanism is
elliptic labels, contact radicals, a height contradiction, Lucas
amplification and a simultaneous common witness.

SHORT_EXISTENTIAL_PROOF.md gives the compact theorem proof;
CONCEPTUAL_MAP.md explains the six moves; ALTERNATIVE_ROUTES.md evaluates
possible replacements without treating hidden assumptions as simplifications.

## Best next directions

The most promising different route is to replace simultaneous contact
primes by primitive divisors of one elliptic divisibility sequence. It
needs a uniform radical-height and prime-separation lemma, not merely a
primitive-divisor theorem.

The second target is a single global defect on a fiber product of the
label and comparison varieties. The high-confidence expository project
is a short paper that proves one master proposition and relegates expansion
and certificates to a supplement.

## Parallel finite experiment

The asymmetric source needs only \(q_1\) and \(q_{40}=q_1e^{78}\).
A direct positive-power circuit was compiled and replayed against the
532-coordinate precursor. It passed exact algebraic checks and has the
same 532 active coordinates, 501 compiled residuals and degree four.
It has 34,251 precursor monomials, three more than upstream's 34,248,
so it is rejected. The final source-specific nine-coordinate elimination
was not reused and no new 540-variable polynomial is claimed.

Further finite work should search for a seven-coordinate mixed circuit
or share a coordinate with the \(q_1,\delta\), or norm block. Replacing
the signed chain by an equally long positive chain is now recorded as
unproductive.

No independent human review is claimed. No pull request, upstream message,
merge or metadata edit was made from this branch.

## Two-route follow-up, 7 November 2026

Continued the conceptual branch at `55060fe0`, keeping this new study separate
from PR #4. Read the live contributor instructions and audit protocol and
inspected `subsec:v9-soundness`, `subsec:v9-local-depth`,
`v9:lem:separation` and `subsec:v9-deep-completeness` in the Version 10
addition. This is not a reclassification of an upstream audit item.

New file: `TWO_ROUTES.md`. The primitive-divisor route now has an elementary
reduction-order/Hasse annihilation criterion: a single sufficiently large
primitive prime can suffice, so radical growth is not the only possible
approach. Exact consecutive-place and CRT obstructions show why a generic
primitive-divisor theorem does not yet replace the common-prime argument.
The needed next result is a finite index-size certificate plus a compatible
local comparison; do not conflate arbitrary-large completeness witnesses
with a constraint valid on every satisfying witness.

The global-defect route yields an exact local binary-norm lemma, but rational
coefficients cannot give residue anisotropy at inert quadratic places.
Combining the Lucas and input defects also destroys the independence from
input height required by the first contradiction. The useful next target
is a global certificate for the Lucas defect alone. Full elimination of
all witnesses cannot work: its elimination ideal in Q[X] must be zero.

`check_two_routes.py` passes 163,968 exact local norm cases, 5,184 generalized
CRT cases, and 198 denominator/reduction-order cases on a separate small
elliptic-curve fixture. It also checks residue-field counterexamples and
exact height-exponent bookkeeping. `TWO_ROUTES_CHECKS.json` pins the script,
notes and reviewed source. These are finite regressions, not independent
proofs of the universal lemmas or of the main arithmetic theorem. Universal
lemmas have prose proofs; no independent human review has occurred.

No source polynomial, certificate, production builder, upstream manuscript
or PR metadata changed. No candidate was promoted and no full polynomial
replay is claimed for this documentation-only study. The work records one
completed research pass, not execution between runs.

## Elementary separation and largest-label follow-up

PR #4 is closed and no longer a target. Preserve new work on the conceptual
branch. `ELEMENTARY_SEPARATION.md` gives a proposed elementary proof of the
existing separation lemma: full rational two-torsion implies 4 divides the
group order, while direct point counting gives d<=2p-2. Primes within a
factor of two therefore cannot divide any opposite group order. The stated
prime theorem already permits this interval condition by increasing its
fixed u/w^2 bound. No Hasse estimate, prime-spacing cutoff, or extra counting
argument is needed for this lemma. The simultaneous-prime theorem and
cross-group coprimality remain indispensable in the current construction.

The primitive-divisor route is sharpened by selecting, only in the proof,
the root with maximal absolute label B. Hasse then supplies a primitive
prime large enough to annihilate the Lucas defect at order 40. A separate
auxiliary index-size certificate is unnecessary if local divisibility can
be imposed at all good root denominator places. That local encoding is
still missing; the current contact tests cannot simply be reused. The
primitive-divisor threshold may be ineffective and is not asserted below
the current explicit anchor.

Exact finite checks: 131,030 abstract group-order cases, 588 finite-field
curves, and 9,985 integer bound cases; receipts pin notes and source.
Prose proves the separation lemma; the replacement source remains conditional.
No independent human review, new polynomial, manuscript edit or PR action.

## Cyclotomic norm-packing follow-up

`NORM_PACKING.md` gives a structural alternative to the symmetric local-test
aggregation. The nine K-valued order-one tests and seven K-valued order-40
tests can be kept over K and packed by a degree-16 extension L/K. Its norm
is one K-valued order-640 test, with exact detector normalization after
powers of the already guarded delta inverse. Local equivalence holds at
inert unramified contact primes, and the construction preserves the proof's
necessary two-stage Lucas-then-input contradiction. The earlier attempt to
pack 32 rational coordinates is rejected: divisibility at one split K-place
does not imply componentwise rational divisibility.

A simpler explicit inertness construction supersedes the initial Gaussian
ray-class idea: let F be the degree-16 subfield of Q(zeta_97) and take
L=KF. It is disjoint from K, and primes congruent to 5 modulo 97 are inert
because 5 has order 96 and order 16 in the relevant quotient. The Gaussian
class 1+2i modulo 97 has norm 5 and leaves the two reduced group orders
congruent to 4 and 8, so it remains compatible with their required avoidance.
The conductor-17 attempt is rejected because a primitive class modulo 17 is
a nonsquare, conflicting with the existing Q_17 pole-completeness condition.
Compatibility with the complete prime-pattern application, exceptional-prime approximation,
and source-level quotient gates has not been checked. The existing one-place
lemma already proves soundness for the single order-640 test, and its local
completeness residue calculation survives. Chevalley--Warning shows that
degree 16 is minimal for any homogeneous one-scalar packer of sixteen
independent residues. The cyclic degree-16 norm also admits a four-step
quadratic-tower definition, avoiding an expanded determinant in the
existential proof.

Finite checks cover norm anisotropy in degrees 2 through 8, 3,125 mixed
valuation patterns, the exact detector exponents, and the residue arithmetic
modulo 97. An integral basis exists for the fixed field but has not been
chosen and encoded as a norm circuit. This is not a production candidate: no compiler
run or polynomial replay is claimed. No independent human review has occurred.

## Two-norm and ray-class follow-up

`TWO_NORM_PACKING.md` supersedes the one-norm design for a possible finite
source. Pack the nine order-one tests in a degree-9 norm and the seven
order-40 tests in a degree-7 norm. Exact homogeneity gives raw packed orders
9 and 280, with only the already guarded factors delta^-8 and delta^-6.
The existing one-place lemma selects one place for both packed factors and
unpacks them to the original thresholds. This avoids all nine fortieth
powers required by the literal one-norm design and lowers the maximum order
from 640 to 280.

One cyclic field supplies both extensions: the real subfield of Q(zeta_127)
has degree 63 and unique subfields of degrees 9 and 7. The class 3 has order
63 modulo sign. The Gaussian residue 1+16i has rational norm 3 and adjacent
norms 2 and 6 modulo 127, so it gives inertness without introducing 127 into
either reduced elliptic-group order.

The proof of the simultaneous-prime theorem yields a ray-class flexibility
lemma: any fixed auxiliary Gaussian class with nonzero norm and nonzero
adjacent norms may be inserted into its fixed base modulus. The local main
term uses u=N(r), w=0; the obstruction tails already allow prescribed
generators; and the ray-fibre product starts beyond the fixed base. This
also covers the case in which 127 divides a later progression modulus by
replacing the specialized residue i at that factor.

Finite checks cover 672 valuation patterns, both detector-normalization
identities, the order of 3 modulo 127 and the Gaussian adjacent-norm
arithmetic. Gaussian-period multiplication tables for the degree-7 and
degree-9 subfields are exact integral bases: their trace discriminants are
127^6 and 127^8. A preliminary quadratic count uses 52 assigned K-coordinates
for the two norms, compared with 65 for the current sixteen test squares and
symmetric-product trees before final evaluation. Dense structure constants
make this only a reason to run the experiment. The remaining mathematical
work is exceptional-prime approximation and reverse-map certification;
the remaining computational direction is a sparser norm basis. No
production promotion or independent human review is claimed.

The isolated dense-period builder experiment has now been compiled and
independently replayed. It gives 525 raw coordinates and 517 compiled active
coordinates, versus 540 and 532 for the current precursor. All 443 gate
identities and 421 certificate operations pass; the polynomial is primitive
of degree four. But it has 451,149 monomials rather than 34,248. Preserve the
exact 15-coordinate reduction as a minimum-variable branch and reject this
basis for the balanced record. A power-basis calculation reduces the nonzero
structure constants from 329 to 175 in degree 7 and from 603 to 369 in
degree 9, at the cost of larger coefficients, nontrivial order indices and
dense Galois matrices. Exact conjugation matrices have 43/49 and 73/81
nonzero entries, so the naive power-basis tradeoff is rejected. Any next
sparsification attempt must optimize multiplication and cyclic conjugation
together.
