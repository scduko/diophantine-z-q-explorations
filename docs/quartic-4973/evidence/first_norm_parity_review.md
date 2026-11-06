# Independent first-norm fusion arithmetic review

PASS for the proof and typed arithmetic contract. This is not acceptance
of an emitted source, implementation helper, measured variable saving, or
final coefficient bound.

Reviewed files in `batching/sub5000/first-norm-fusion`:

- `PROOF.md`: `b18b32854d4ef6e8c49495ce404f7c96566a0a1926baca6f4ee1ed4cbedcba05`
- `CONTRACT.json`: `b327fcc99625f09c36509c6b22cb12edc4fdeb40c2f8a7b70f65f2509c75570c`

The proposed first leaf is original field zero, H.f, of order one. Its
virtual denominator changes from r^2 to r. That step is an arithmetic
source revision with a new completeness argument, not a rational map
preserving the old norm root or every old witness. The subsequent fusion
is exact on the retained rational-conic source. The documents correctly
separate these scopes.

## Nonzero contact and the norm tree

The retained equations `S=s^2` and `theta^2-r*S=2` force both r and s
nonzero over Q. In particular, proving r nonzero does not use either
of the first-node rows that will be replaced. This avoids a circular
unit argument. It is a global rational fact, not a selected-prime or
integer-completeness assumption.

At any consumed odd prime let R=v(r) be odd. The conic gives
`E=v(theta^2-2)=R+2v(s)` odd. If theta has negative valuation, E would
be even; if theta has positive valuation, E would be zero. Therefore
theta is a unit, E is positive odd, and the selected root rho of 2
satisfies `v(theta-rho)=E`.

Recovering the virtual first leaf W=T/r makes the full upper tree
literally the usual tree of `N_r(a,b)=a^2+r*b^2`, with literal one
first. At an odd R its two finite summand valuations have opposite
parity. No cancellation is possible. The constant path makes the root
nonzero and of valuation at most zero if R<0. Then r times its square
has negative odd valuation, contradicting the retained one-sided pole.
Thus R>0. The same pole gives root valuation greater than -R/2.
Descent through each node gives every virtual leaf valuation greater
than -R. Zero leaves are permitted by valuation infinity.

The new first-node row therefore does not disrupt the negative-contact
exclusion argument or silently assume positive R in advance.

## The weaker numerator bound is sufficient

For the original field F=A+B*sqrt(2), put

    Y=A+theta*B,
    T=Y^2-(theta^2-2)*B^2.

Because E is odd, the finite summand valuations `2v(Y)` and `E+2v(B)`
have opposite parity. If `v(T)>=2e-1`, both are at least 2e-1. The
first is even, so `v(Y)>=e`; the second implies

    E+v(B)>=(2e-1+E)/2>=e.

Thus `F=Y+(rho-theta)B` has valuation at least e. Equality in the last
bound is harmless; strict inequality is not required. This closes the
rounding case E=1 that would be missed by reusing the old stronger
proof verbatim. No integrality of A or B is assumed.

For the proposed first leaf, `W=T/r` and `v(W)>-R` imply v(T)>0,
hence v(T)>=1. The lemma with e=1 yields the original H.f order. All
other fields keep their even denominator and their old proof.

If B or Y vanishes the same inequalities use infinity. If T vanishes,
opposite valuation parity forces both Y and B to vanish, hence F=0.
These cases are not excluded by division.

## Exact fusion and its zero cases

On the virtual mixed-denominator source, retain `T=rW` and
`N=1+rW^2`. The fused equations are

    T-2AY+A^2-2B^2=0,
    rN-r-T^2=0.

The forward map assigns T=rW. The reverse map assigns W=T/r; r is
nonzero by unchanged conic rows. It preserves N and every later node
and pole witness. All new residuals have integer coefficients and
total degree at most two, with coefficient magnitude at most two.

T=0 and W=0 give N=1 and cause no exception. N=0 is allowed, for
example r=-1, theta=s=A=1, B=0, T=1, W=-1. Neither direction divides
by N, T, a field coordinate, or a pole coordinate.

At r=0 the isolated fused row permits T=0 with arbitrary N, whereas
the virtual original norm node requires N=1. The contract explicitly
excludes invoking this rewrite without its unchanged rational conic.
It does not claim a generic all-r fixed-witness equivalence.

## Integer completeness and source obligations

The old selected contacts have r>0 and positive selected-prime
valuation. With points and field coefficients fixed before theta,
the old approximation makes T/r^2 integral; hence T/r is also
integral. The other leaves remain integral, and the constant path
keeps the new root a unit at that prime.

For fixed r, the new first leaf and the entire new norm tree remain
polynomials in theta with rational coefficients. At the real place
r>0 makes all binary norms nonnegative and the constant path at least
one. These are exactly the properties of the norm root used by the
reviewed linear-pole completeness argument. Its approximation near
3/2 at the real, 2-, 3-, and 17-adic places still applies, alongside
the selected-prime neighborhood. Although the new root need not equal
the old root, new pole witnesses exist by that argument. No stronger
form of the full old Psi predicate is asserted.

The implementation must check field zero and order one in all three
modes, the literal-one first pairing, the unchanged conic, and the
old leaf's complete incidence. It must retype the reused leaf slot as
numerator T, retain the first node ID and all its consumers, and retain
every other field, power, node, shared-square type and pole input.
The fresh source checker must distinguish this arithmetic delta from
the exact fusion; substitution into an old source identity is not
sufficient acceptance.

The source coordinate count is unchanged. One formerly cubic node
becomes quadratic at each of 37 occurrences, so a 37-coordinate lift
saving is a structural forecast only. Existing G-square elimination
of the same Y is compatible algebraically because T is still the
identical numerator. Its actual interaction with cleanup, as well as
the complete coefficient bound, requires the new emitted replay.

## Bounded verification

`test_review.py` pins both reviewed files. It checks 1,890 rational
local assignments at three odd primes, including negative coefficient
valuations and E=1 or 3, and all 2,388 qualifying order assertions.
It also checks 64 exact fusion assignments with positive and negative
contacts, an explicit zero-node solution, the isolated r=0
counterexample, and a witness that the denominator change does not
preserve the old norm root. The tests passed under CPython with
`-E -B`. No full source generation or quartic expansion was run.
