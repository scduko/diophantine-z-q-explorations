# Dependencies, assumptions, and logical boundaries

This ledger describes the preserved manuscripts. It does not assert that the imported preprints have been independently proved or that the sufficient packages are logically necessary.

## Third version: precise black-box inputs

Use the complete statements in Section 2 of `01_current_articles/two-proofs-reduced-inputs-v3.tex`. The source labels below are stable within that file.

| Input | Exact place in v3 | Content needed | Role |
|---|---|---|---|
| Geometric family | `in:geometry` | For every parameter outside five contacts, an abelian surface over a uniformly bounded-degree field, controlled ramification, good reduction away from a fixed set, a geometric quaternion division-algebra action, isogenies to Galois conjugates, and a comparison of parameter height with Faltings height. | Supplies the geometric situation to which the earlier height theorem is applied. |
| Prime-contact representations | `in:prime-pattern` | For every integer A and every lower bound, A is a sum of three rational slopes sharing a denominator; all thirteen contact expressions are sign times a fixed multiplier times a sufficiently large selected prime. The selected primes split in Q(sqrt(2)) and the two relevant reduction-group orders have gcd 4. | Completeness of the finite certificates. CRT constructs formal witnesses after the primes have been obtained. |
| Restricted simultaneous point existence | `in:restricted-realization` | A restricted first squareclass associated with a selected contact prime, a compatible second squareclass, and one twist parameter for which two elliptic curves both have rational points in the prescribed first squareclass. | Restricted completeness of the parity predicate. |

The imported point-existence statement is weaker than full square-denominator completeness. The first squareclass has only one variable prime, up to a fixed multiplier. No elementary proof of this remaining simultaneous existence statement was obtained.

The prime representation assumption is not a consequence of CRT alone. CRT controls finitely many prescribed valuations and residues; it does not prevent extra uncontrolled prime factors in the resulting contact expressions. The supplement allows suitable bounded products of primes with additional certificates, but does not prove such global coverage by elementary means.

## Results supplied outside these three inputs

| Step | Source or local argument | Qualification |
|---|---|---|
| Rank one of the simpler curve and nontorsion of Q0 | The explicit 2-isogeny descent in v3, Lemma 2.3; Silverman supplies the classical descent formalism. | The exact specialized calculation is proved in the note; it was not replaced by a claim that this exact curve is listed in a textbook. |
| Finitely generated elliptic group and cyclic image | Mordell--Weil and annihilation of finite torsion. | No explicit generator is needed for qualitative definability. |
| Height exponent 24 | von Känel--Kret (7.19), together with the compatibility and field-of-definition argument in Proposition 2.2. | Earlier preprint input, not described as a published theorem without checking. CM gives exponent 10 separately. |
| Endomorphism field and ramification | Masser--Wüstholz/Silverberg, Néron--Ogg--Shafarevich, Serre--Tate. | The bounded extension defining geometric endomorphisms must be accounted for. |
| GL2-type conjugacy compatibility | Wu's structural facts and Skolem--Noether as applied in v3. | The verification is retained because the citation alone does not perform the application. |
| Finite squareclass multiplier lists | Weak approximation and openness/finiteness of local squareclasses. | Fixed lists are coefficients/finite branches, not integer quantifiers. |
| Formal logarithm estimates | Standard formal-group facts plus the recorded uniform estimate. | Precision and denominator hypotheses must be retained. |
| Simultaneous multiples at finitely many places | Finite index of deep formal subgroups and CRT, with the stated selected-prime order condition. | This constructs local witnesses; it does not prove the prime-pattern theorem. |
| Model-only contradiction to Mazur | Cornelissen--Zahidi, Theorem 3.6. | Applies to a model with domain in Q^k. No definition of the actual integers is required. |
| Exponential relation on the model | DPRM. | Used only after addition and multiplication on the model have been constructed. |
| Pell/Lucas classification | Jones, Corollary 2.7, plus the elementary growth estimates retained in the note. | Used in the direct route. |

## Inputs removed or weakened along the way

- The new Fontaine--Mazur-at-2 input is not needed in the reduced-input proof route.
- Rank one is no longer assumed from H10 in v3; the special descent is included.
- The first proof no longer needs the original recursive theory and compactness argument to obtain multiplication.
- The alternate proof's large fixed anchor is removed in v3 by rescaling the cyclic generator.
- The old model-to-integers step using an explicit recursive prime mask and fixed-prime integrality predicates is replaced by the scalar certificate and exponential growth.
- The qualitative proofs can use precision 24. This does not mean the existing explicit circuits were all recompiled at precision 24; many retain their old constants and precision 64.
- V3 only needs the restricted parity completeness stated there. Do not transfer this reduction without proof to a construction using Phi on more general square-denominator inputs.

## Shared-witness route: stronger assumptions

The shared-witness article and its `article/shared-definition.tex` state their own inputs. In particular:

1. Sun's change of coordinate uses five finite contact values and no contact at infinity. This differs from the v3 convention. At a denominator prime of the parameter, all five normalized finite-contact depths can be zero; one must not silently add that prime to the radical.
2. The pole predicate Phi0 needs completeness for a larger class of rationals: no negative odd valuation anywhere, appropriate small positive real size, and prescribed positive valuations at a fixed exceptional set. The article expressly says the weaker prime-squareclass input of v3 is insufficient for this use.
3. The simultaneous-prime theorem imposes compatibility between reduction orders at distinct selected primes, not just the two orders at one prime. The displayed requirement includes gcd(d_+(q), d_-(q')) = 4 for all selected q,q', specified 2-adic valuations, and avoidance of auxiliary odd moduli and 7.
4. The 40-variable compression uses Sun's Section 10 finite-algebra elimination, including finite branches, separability, degree drops, rational recovery of roots, and nonzero guards.

The common elliptic point used in the scalar and main conditions must satisfy both the fixed local congruences and real boundedness requirements. The article's completeness argument fixes the scalar indices and modulus first, invokes simultaneous prime selection with that modulus, and then chooses the common point. Interchanging this order can invalidate the compatibility argument.

## Verification levels

| Evidence | What it supports | What it does not support |
|---|---|---|
| Byte-for-byte circuit rebuild | Reproducibility of the specified graph and its serialization. | Correctness of the arithmetic theorem represented by the graph. |
| Independent structural recount | Variable list, graph topology, reachability, sum-of-squares structure, structural degree bound. | Exact total degree when cancellations could lower it; number-theoretic completeness. |
| Exact coefficient comparison | Identity of the collected polynomial with the specified residual/circuit construction. | That its rational zero set projects exactly to Z unless the mathematical argument is also valid. |
| Modular evaluations in some older compiler audits | Consistency checks at the recorded assignments. | Polynomial identity by themselves. Exact identities or derivations are separate. |
| Mathematical audit note | The audit's recorded reasoning and conclusions about specified steps. | Formal proof-assistant certification or validation of every cited source. |
| Coq/extracted-code material in the early focused package | The specific natural-number compiler theorems and their recorded extraction chain. | Formalization of all the elliptic arithmetic or a kernel-checked rational definition of Z. |
| Current handoff inventory and CRC/SHA checks | Preservation, integrity, and reproducibility of the handoff contents. | A new research-level audit of every manuscript. |
