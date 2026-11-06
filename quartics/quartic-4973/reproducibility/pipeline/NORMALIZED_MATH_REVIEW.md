# Independent normalized-Lucas arithmetic review

Verdict: PASS for the normalization proposed in
`precision/sub5000/normalized-lucas/NORMALIZED_LUCAS.md`, SHA256
`e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811`.
This review does not accept an emitted source or a final variable count.

## Exact identity and divisions

Let the retained quotient numerators satisfy `B_i Lambda=G_i`, with the
common equation `Lambda p_H=G_H`. Each G is nonzero for every rational
field input by the existing dyadic argument. Thus Lambda, p_H and all
B_i are nonzero. The new equations may safely determine `P=p_s/B_s`.

At a consumed odd prime, every primary has positive-valuation f. The
joint-chart eliminant forces `f p^2+D f^2=1`; D is a unit at these
primes, so `v(f)+2v(p)=0`. In particular all p_i are nonzero there. Only
at this stage set `C_i=B_i/p_i`. The unchanged formal and alternate
tests give the same integral quotients and index congruences as before.
This inference uses no old primary proxy tests or normalized residual.

The new rows imply

```
P=1/C_s,
V=(1-2P)C_z, Kc=(1-2P)C_t, U=P C_t-V,
E=U^2-Kc V-P^2=P^2 F(C_s,C_t,C_z).
```

I independently expanded this identity. Soundness requires only the
already proved integrality of C_s: `F=C_s^2 E`, so an order-40 bound on
E implies the old order-40 bound on F even when C_s has positive
valuation. There is no discarded denominator or assumption that C_s is
a unit in soundness. No division by `1-2P` occurs; `C_s=2`, `P=1/2`,
`V=Kc=0` is included.

## New global branches

The old quotient equations forced all numerator p_i nonzero globally.
The new equations do not do so for p_s and p_z. They do force p_t
nonzero: if p_t were zero, the second row forces P=0 and the third then
contradicts B_t nonzero.

When p_s or p_z is zero, the joint eliminant still gives a curve point
with x equal to d or -d. Its first graph denominator is `2qx`, which is
nonzero, and its finite difference parameter is `-q/(2x)`. Thus this
branch is valid for the joint chart. It cannot occur at a consumed
prime because its f is a unit. No local conclusion is required at an
occurrence without a consumed prime. The source and auditor must not
retain the old blanket nonvanishing claim, or add an inverse of P, p_s
or p_z.

## Completeness and prime avoidance

The root indices and target coordinates are fixed before the prime
pattern is chosen. The established rational-target prime lemma allows
any prescribed finite lower bound. In particular, after fixing the
nonzero integer s from the anchor, require every selected ordinary
prime to exceed |s|, along with the existing fixed exclusions. This
includes the underlying prime for the square-times-prime infinity
contact; it does not assert that the raw infinity contact is prime.
Repeated primes between positions remain allowed.

Consequently C_s is a unit at each assigned prime, since C_s is
congruent to s there. The old complete witnesses therefore give
`E=F/C_s^2` of order at least 40. Assign the new coordinates by the
displayed identities and only then choose each private conic parameter.
The old conic and parity completeness constructions apply unchanged.
This avoids a possible loss of order under division in completeness
without adding any soundness assumption.

I checked this choice order against
`work/quartic-astra-search-20261105/contact-count-next/INDEPENDENT_REVIEW.md`
(SHA256 `ca056065e4e48ac27c4f63ee84b8bc1c3009c754ae32bdc84fdff39248933019`),
including its arbitrary prescribed lower bound and explicit order of
root-data, prime-pattern and private-point choices. The G nonvanishing
argument is (4) in the frozen `precision-next/RECIPROCAL_PROOF.md`
(SHA256 `be5b08dd9ded743606d5c6a5fc869c4e9764575da49e5d80af13aca09950a98a`).
It is a dyadic valuation argument, not real positivity.

## Bounded checks and source obligations

The independent `test_normalization.py` passed the exact Laurent
polynomial identity and 27 rational-field examples, including nine
examples with C_s=2. Two additional algebraic block fixtures exercise
p_s=0 and p_z=0. Those fixtures test the allowed block equations, not
full elliptic source solutions.

The separate source checker must verify all five normalized equations,
all three B_i/G_i equations, the unchanged beta quotient, and exactly
the normalized E at the existing order-40 field position. Root,
interfaces, conic batches, formal and alternate tests must be preserved.
The mathematical conclusion concerns equality of the final input
projection. It is not an algebraic map from every old private witness:
an old witness with nonunit C_s can fail the new stronger local test.
Fresh source reconstruction, flattening, finite replay and coefficient
expansion remain required.
