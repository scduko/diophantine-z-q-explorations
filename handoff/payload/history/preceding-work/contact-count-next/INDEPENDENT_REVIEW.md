# Independent review of thirty-seven rational-target comparisons

Reviewed by the unit-scale search agent on 2026-11-05. This is a static
arithmetic and dependency review. No prime search, source regeneration, or
heavy computation was run. No new optimized variable count is certified.

Conclusion: I found no arithmetic obstruction in the proposed change.
The rational-target prime-pattern argument, the square factor on the
infinity contact, and the resulting height estimates supply the required
soundness and completeness statements, subject to the same inherited
theorem qualifications as the current source. The old integer-target lemma
alone would not suffice; the explicit rational-target extension is necessary
and its argument passes this review. This is a new arithmetic source, not an
event accepted by the old source-pinned algebraic certificate.

For the sieve application, explicitly retain the inherited requirement that
the fixed initial cutoff Q exceeds 82. It may always be enlarged to include
the new denominator and determinant primes. This makes every later factor
1-2m/q positive and supplies the fixed-cutoff hypotheses used below. The
proposal's reference to the inherited cutoff argument permits this choice;
writing it explicitly would remove an avoidable omission in the presentation.

## Reviewed versions and inherited statements

| File | SHA256 |
| --- | --- |
| `contact-count-next/PROOF.md` | `e68c4707974ec0aca786a5a3ce1a548fb8bd4c7f5791e30e42de0096a717140d` |
| `contact-count-next/DEPENDENCIES.md` | `a7f289b20b0263756eb25970b86fee31f25059e25aa3bd575343006e60455860` |
| `contact-count-next/prepare_source.py` | `9d497fe596ba6d52830036e1e0c22ae0d2fdb92325661575b4d581503f8a7caa` |
| `degree8-original/arithmetic/sieve/original41-proof.tex` | `650e7564eb0158b6ad72506ab465bd054a14b32ed76433908d573a3d05a3228b` |
| `degree8-original/arithmetic/sieve/applications.json` | `28b8f85d33be96b7148de22214dbe7fd39d221a99ab56c75534ad47edc18b062` |
| `diophantine_zq.tex` | `b6c125899af3a8f8ba139abad332b8f98805967bab25b0dcf6d9651997f614b7` |

The last three files are in `work/quartic-variable-search-20261105/remote-repo`.
I compared the proposal with the actual inherited statements, including:

- The five-contact height theorem `hyp:o8-height`, whose domain is rational
  slopes outside the four finite branch values and whose exponent is 24.
- The exact seven-witness pole theorem `hyp:o8-pole` and its completeness
  lemma. Completeness assumes positivity, square reduced denominator, and
  being a square in Q_2, Q_3, and Q_17. It does not require the argument or
  raw contact itself to be prime or squarefree.
- The current forty-one-prime proof and application records OP01 through
  OP14, including the lower-count, bad-value, and fiber estimates.
- The local primary text of Green--Tao, Definition 1.5, Lemma 1.6, and Main
  Theorem on page 1763. Its finite-complexity conclusion, with the inherited
  GI and MN inputs, applies to fixed integer affine forms. The proposal meets
  that condition after its denominator choice. I also read the relevant MN
  theorem and the existing source/version ledger. This review does not
  independently reprove those deep inputs or alter the inherited GI
  correction convention.

## Fixed denominator and exact integer forms

For a fixed rational tuple a_i, choose a positive integer D with D a_i
integral and define T=V0 D^2. Then T delta is an integer multiple of W for
each delta in C, and T A_i=32W D(D A_i) is also an integer multiple of W.
Thus every K_s=T s is in W Z. Each finite form
c+Wx-K_s(c+Wy) is an integer affine form with the required residue c modulo
W. Its linear coefficient of x is W, so no finite form is constant.

Deduplicate exact rational slopes, not merely repeated targets. For
different surviving s,t, the determinant of the two finite linear parts
is a nonzero multiple of K_s-K_t. The p0 linear part is independent of every
finite part. Hence the resulting m forms have pairwise independent linear
parts and m<=37. This covers collisions between two secondary families and
collisions of a secondary slope with C. The old modulo-31 proof that whole
families cannot collide is neither true nor needed for arbitrary rationals.

Deleting a duplicate form only from the analytic prime-pattern problem does
not delete any comparison position in the polynomial. Restore every repeated
position with the same prime value. Such positions may use their own private
comparison points. One common orientation at each repeated prime and the
existing common J are sufficient. Accidental equality of values of two
nonidentical forms causes the same harmless repetition.

## Local admissibility

At q dividing W, all forms equal c modulo q, and the existing fixed residue
calculation applies. It gives value and successor nonvanishing at the odd
small primes. No successor restriction is imposed at 2.

At q>29 dividing D, with d=v_q(D)>=1, the denominator condition gives
v_q(A_i)>=-d. Thus T A_i and T delta are divisible by q, and every K_s
vanishes modulo q. Since W is invertible modulo q, x and y can independently
make u and p0 equal one. Every finite form is then one and every successor
is two, both nonzero. This case includes q=31,37,41 when such a prime occurs
in D; the separate small-slope argument is not incorrectly applied there.

At q>29 not dividing D, T and W are units and the change from x,y to u,v
is invertible. The slopes are q-integral. For q=31,37,41, R a_i vanishes
modulo q, so A_i=3 and there are at most eight slope residues. For q>=43
there are at most 36. In both cases at least two residues b,e are missing.
With gamma=T^(-1), at least one ordering satisfies e-b!=-gamma: both
orderings could fail only if 2gamma=0. The proposed u,v then avoid zero
and minus one for every finite form and for p0. This verifies exactly the
value/successor admissibility used by the inherited order sieve.

## Prime-pattern and fiber estimates

After the rational tuple and D are fixed, all K_s, coefficients, and the
positive real box are fixed. A box exists because taking v>0 and
u/v>max|A_i|+2413 makes all the forms positive with room to spare. In
homogeneous leading coordinates, every form is bounded between positive
fixed multiples of the dilation parameter. The unused third coordinate
retains the inherited X^3 counting setup.

Choose Q>82 containing every prime dividing D W and every nonzero
K_s-K_t. Then choose L>Q. Only after L is fixed apply the prime asymptotic
on the finitely many surviving residue classes, and only then let X grow.
The singleton partition has complexity at most m-2<=35, within the existing
at-most-39 inputs. No assertion uniform in D, the rational tuple, or a
growing modulus is required.

The fiber calculation survives unchanged. On p0=p, the finite forms are
c+Wx-K_s p, and their zero lines are distinct at q>Q with q<p. On a
finite fiber Psi_s0=p, the other forms are
p+(K_s0-K_s)p0. Their zeros are distinct from each other and from the
p0=0 line. The exclusions of determinant primes and q=p supply every
denominator used in this statement. Thus there are exactly (m-1)q forbidden
points in the two-dimensional residue space, as required by the inherited
Selberg fiber estimate.

The proposed lower and bad-pattern bounds have the same dependence on L
as the inherited proof. Constants may depend on the fixed tuple and D.
Since (log L)^(2m)/L tends to zero, L can be chosen to make the bad-pattern
constant smaller than the lower-count constant, and X can then be chosen
large enough. This proves the required existence for every fixed rational
tuple and every prescribed prime lower bound. It is a reapplication of the
inherited analytic theorems, not a direct use of the integer-target lemma.

## Infinity contact and denominator primes

Require all selected prime values to exceed every prime divisor of D.
For r_infinity=D^2 p0, the only odd valuation is then the valuation one at
p0. Every finite raw contact is a selected prime. The elliptic ordinary-prime
properties are needed at p0, not at the composite number D^2 p0, and the
dependency note makes that distinction correctly.

For q dividing D outside S_*, V0 is a unit. Because the delta=0 finite form
is u and is a prime larger than q, u is a q-unit. Also p0 is a q-unit.
Consequently v_q(v)=2d, v_q(A_i v)>=d, and A_i v-u is a unit. Both height
slopes have valuation -2d. In the primitive homogeneous normalization their
only positive branch depth is the infinity depth 2d, which is even.
Subtracting any finite branch value leaves the same negative affine
valuation. Therefore these denominator primes contribute no odd normalized
contact. This conclusion also holds when D has unnecessary prime factors.

At the selected prime for any occurrence, v_p(r)=1. The usual local-point
and theta choices make each nonconstant normalized leaf integral. The
constant leaf stays on the all-left path, so the norm root is a p-unit.
No special integral condition at a prime dividing D is needed.

For the parity input b=r N_r^2, positivity follows from r>0 and the norm
tree's constant leaf. At its selected prime, v_p(b)=1. At every other prime,
v_q(r) is even, so v_q(b) is even even when N_r has a denominator. Thus
every negative valuation of b is even and its reduced denominator is a
square. The selected prime is a square in Q_2,Q_3,Q_17 by the fixed c
residues; multiplying by D^2 and N_r^2 preserves these square classes.
This meets the actual seven-witness completeness theorem exactly. It does
not assume a square-class invariance theorem for arbitrary satisfying
assignments of the parity predicate.

## Soundness and heights

For an arbitrary rational assignment, the previous parity-of-the-common-
minimum argument still sends each odd normalized contact of u/v or
(A_i v-u)/v to an odd raw contact. It only uses each pair's two rational
coordinates and the unit differences between the fixed branch values.
It does not use D or the completeness lattice. The source retains the
nonzero raw-contact guards, so v is nonzero and both slopes avoid every
finite branch value. They lie in the domain of `hyp:o8-height`.

All four index proxies and each complete internal comparison remain in every
one of the 37 positions. Therefore the same comparison soundness gives the
same radical divisibilities. If the Kth powers divide a nonzero integer N,
the original two-slope argument yields

    h(a_i) < 2H |N|^(24/K)+14.

For x(Q)=a+b sqrt(2), the absolute logarithmic-height inequalities give

    h(x(Q)) <= h(a)+h(b)+h(sqrt(2))+log(2)
             < 4H |N|^(24/K)+30
             < 5H |N|^(24/K).

Here h(sqrt(2))+log(2)=3log(2)/2<2, while H>50 and |N|>=1 give the last
strict inequality. In particular the previous coefficient 7 bound still
holds. The existing Delta contradiction and the beta-minus-index
contradiction may therefore be retained with their previous constants.
The scalar-height batch, its correction bits, the anchor, and the Lucas
equation do not consume e and remain unchanged.

## Quantifier order and completeness

The permissible order of choices is:

1. Fix an integral input X and the same target points A,S,T,Z as in the
   existing completeness proof, including the scalar-height and anchor
   requirements on S and the Lucas choices for T,Z.
2. Their eight rational abscissa coefficients are now fixed. Choose D
   clearing their denominators; choose the real box and fixed cutoff Q.
3. Choose L and then X for the analytic counting argument, obtaining the
   prime values and source witnesses u,v. The counting variable X in this
   step should be renamed in exposition to avoid confusing it with the
   already fixed Diophantine input.
4. For the resulting finite set of selected primes, choose one orientation
   per prime, a common J, and private comparison points. Retain the original
   same-prime CRT conditions, then choose the common root approximation.
5. Assign norm intermediates and apply the established parity-completeness
   theorem for each occurrence.

No later step changes the target points or requires them to satisfy new
conditions at the prime divisors of D. D is not a polynomial witness and
does not become a fixed coefficient of the source. It appears only in
the existence proof choosing u,v. A bound on the height or size of D is
therefore unnecessary. The forward soundness argument does not quantify
over or recover D.

## Dependency and implementation boundary

The dependency replacements in `DEPENDENCIES.md` identify the substantive
changes correctly: OP02 uses full slope deduplication, OP03 gains the
denominator-prime case, OP04-OP08 apply the same analytic bounds to the
new fixed integer forms, and OP13 uses the square-times-prime parity
argument. OP09-OP12 keep the existing private-shift, common-J, formal-log,
and common-root statements. OP14 and all new source counts still need a
fresh finite compilation audit.

By inspection, `prepare_source.py` changes the root target list from e and
the eight e*x coefficients to the eight x coefficients, and changes the
two corresponding metadata counts. It does not alter the internal
41-test comparison module. The structural count explanation is consistent
with the inherited subtree counts, but remains a prediction until
regeneration. This review does not accept a changed source hash as an
algebraic equivalence certificate or certify final quartic savings.

The proposed 37-position limitation in `DEPENDENCIES.md` is appropriately
restricted to the stated raw-form coverage argument. It is not presented
as minimality of the arithmetic construction or of a Diophantine definition.
