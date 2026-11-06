# Normalized local Lucas with private-conic pole reuse

Arithmetic composition verdict: PASS under the exact source boundary below.
This note accepts neither uninspected merged source bytes nor a final count.
It preserves all existing packets and their historical scope.

The normalized-Lucas proof is SHA256
`e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811`;
its independent review in `normalized-lucas-audit/MATH_REVIEW.md` is
`3c6731295b96b1023e42b1d188692c9af5f7a1fece16b6fdc6e6fff905fe10ad`.
The conic-pole proof is `PARITY_CONIC_REUSE_PROOF.md`, SHA256
`a7d2712ce511aca30f5c8e94e0e2ce93c6ee64e21074e2bff91f412fe5a1cb5c`,
and its independent arithmetic review is
`84970af65abda253545e12cc7ac476183df321972316ed88e71a0e37a25b952f`.

## Soundness needs no new local unit

Use separate notation for the integer root index s, conic witness s_c,
normalized coordinates P_n,U_n,V_n,K_n,E_n, and pole coordinates D_p,U_p.
The retained conic is `theta^2-r*s_c^2=2`. It forces r and s_c nonzero
over Q. The pole equations force

```
D_p=4 theta^2-7=1+4r s_c^2,
U_p=r(9-4 theta^2)/D_p.
```

D_p is nonzero over Q because otherwise `(2 theta)^2=7`. The conic-pole
proof maps every new pole solution to the original predicate at
`b=r W^2`, preserving r, theta, the field values and every norm node.
This implication uses no positivity, approximation or local-unit
assumption. In particular it includes W=0 through the explicit zero
branch, without dividing by W.

The existing conic norm argument can therefore be applied unchanged at
every prime greater than 76176 where the raw r has odd valuation. It
recovers all 13/6/10 field orders. The retained formal tests and joint
curve identity force each primary p_i nonzero at such a prime. The
normalized equations then give `C_i=B_i/p_i`, integral C_i with their
old integer-index congruences, and

```
F(C_s,C_t,C_z)=C_s^2 E_n.
```

Only integrality of C_s is used to transfer order 40 from E_n to F.
C_s is not assumed to be a local unit in soundness. The unchanged two
height contradictions then prove the same integer-input conclusion.
The pole replacement cannot weaken it because it implies the old
predicate before the norm and normalized-Lucas arguments are applied.

Neither replacement excludes legitimate zero branches. Globally p_s or
p_z may be zero outside consumed occurrences; their joint-chart points
and finite difference parameters remain valid. P_n=0, P_n=1/2, U_p=0
and E_n=0 require no new inverse. At a consumed odd prime the norm
argument itself excludes W=0. For other occurrences the pole proof's
W=0 branch applies independently of the normalized coordinates.

## One compatible completeness construction

1. Fix the integral input, scalar-height data, anchored root S=sP_*,
   integer Pell indices t,z, and all root targets. Here s is nonzero.
2. Choose the original positive ordinary-prime pattern, retaining its
   residue conditions and increasing its prescribed lower bound past
   |s| and every earlier finite exclusion. This applies also to the
   underlying prime of the square-times-prime infinity contact.
3. Choose the common J, each private elliptic point, its joint-chart
   coordinates, G values and finite logarithm quotients. Every assigned
   prime now makes C_s a unit. Assign the normalized coordinates,
   including `E_n=F/C_s^2`, and freeze all rational field coefficients.
4. For each occurrence independently, choose the private conic point
   with the old sufficiently deep approximation to the selected root
   of 2, and simultaneously near theta=3/2 at the real, 2-adic, 3-adic
   and 17-adic places. Then assign packed nodes and all remaining pole
   witnesses by the fixed-U completion lemma.

The first three steps are independent of every private theta,s_c,S_c.
In particular the denominator C_s in step 3 depends only on already
fixed elliptic/G data. It can introduce large rational coefficients or
large valuations at other primes; it cannot introduce a denominator
depending on theta.

Thus for fixed r and field coefficients each packed node is
`(A_i^2+2A_i B_i theta+2B_i^2)/r^(2e_i)`, and W(theta) remains a polynomial.
At the selected prime, the unit C_s preserves the required normalized
field order. Conic approximation handles the possibly nonintegral
individual coefficients just as before. At the other four places,

```
R(theta)=(r/17) W(theta)^2 ((9-4theta^2)/(4theta^2-7))^2
```

is continuous and zero at theta=3/2. Its denominator has value 2 there:
being a nonunit at 2 does not prevent continuity of its inverse. The
factor 1/17 and any large field coefficients change only the required
depth. These places are distinct from the selected prime. Weak
approximation on the rational conic therefore meets all neighborhoods.
Repeated contact primes still have independent conics.

Since r>0 in this construction, the constant-left norm path gives W>=1
over R. Hence W is nonzero for the completeness scaling, `b=r W^2` has
the required positivity, square denominator and exceptional local
squares, and the fixed-U lemma applies. All field values were fixed
before this additional conic choice. No new analytic prime theorem or
simultaneous elliptic-point condition is needed.

This is equality of final input projections via soundness and integer
completeness. It is not a bijection preserving every old fixed conic or
normalized witness.

## Required merged-source binding

Use a fresh family
`H19-root37-joint-chart-normalized-lucas-conic-pole-anchor4-v1` and fresh
source ID. The existing normalized addon excludes pole reuse and its
three direct batch byte pins are incompatible with the new tails.
Supersede exactly those exclusions and exactly those three direct byte
comparisons. Retain their old hashes as provenance/reference inputs;
check the replacements through the complete independent batch
specification and literal tail delta. Do not discard the entire parent
pin record or weaken unrelated exclusions.

The earlier unnormalized local-Lucas pole addon is retained as provenance,
not as the merged comparator specification. Its old parent selection and
unnormalized E interpretation do not apply. The normalized addon governs
the comparators; this composition governs the new pole boundary and
13/6/10 registry. Earlier pole contracts supply only the explicitly reused
pole equations and mathematical premises, not their obsolete source
identities or batch registries.

The root, beta comparator, anchor, scalar-height batch, old q_primeparity
module and shared constants retain their six existing file pins. Full
and Lucas comparators must pass the exact normalized reconstruction;
once a normalized source artifact exists, also bind their unchanged
bytes to that artifact. Do not substitute unnormalized comparator pins.

The only new module is the literal `q_conicpole`: three free inputs,
twelve fresh locals, ten quadratic rows and no calls. Each of the 37
ordinary batch instances passes its exact triple
`[raw r, own private theta, own upper norm root W]`. Delete only the old
final square/argument coordinates and their two rows, after proving no
outside use. Restore those two rows for the old complete conic checker,
then verify the entire actual batch against the literal approved delta.
All powers, field bindings, orders, literal-one paths and carries remain.

Verify independence through the actual comparison expressions and full
instantiation map: no tested field coefficient may capture a private
conic or pole coordinate through an alias, shared slot or extra equation.
All private conic and pole allocations remain separate across
occurrences. Old shared theta/error inputs remain ignored as before.

The old q_primeparity has exactly its one scalar-height occurrence; the
new q_conicpole has exactly 37 occurrences and must be excluded from old
parity rewriting rules. Run normalized-equation mutations, conic/pole
literal and caller mutations, complete source flattening and map checks,
fresh lift, independent reduction replay and final coefficient expansion.
In particular test a pole call with another occurrence's theta, a wrong
W or r, a field coefficient depending on theta, old unnormalized E
metadata, and accidental retargeting of scalar height. No aggregate
count or hash-only check replaces these boundaries.
