# Target-two source contract

This packet proposes a fresh arithmetic source. It does not authorize a new
source pin or mutate the frozen target-four helper. Its entry point is
`target2_rewrite.postprocess_modules(modules)`, with the same exact four input
module pins as the frozen root helper. Apply it to the original normalized
root and comparators, in place of that helper. Apply the independently audited
shared-common-square postprocessor afterwards if that variant is selected.

The mathematical input is `../root-doubled-indices/TARGET_TWO.md`, SHA256
`cfc62097ffdbf072fe77524f7e0448356812712689394ca22dfc4a0fd64b7feb`.
Guards independently reviewed it in `TARGET_TWO_REVIEW.md`, SHA256
`d5048cc8ac8944d26c8af6d9b8cfcdd672ddee1beed73efaf3d634a53b012155`.
The general root carrier and six root charts retain the separate mathematical
dependencies identified by `PROOF` and `COMPOSITION` in the emitter. This
contract replaces only their target-four choice by the target-two theorem.

All six root points lie in the nontorsion part of E(K), with integer root
index defined by `2Q=n_Q Pstar`. The retained private-index metadata still
describes the coefficient of Pstar modulo torsion, which may be a half
integer. These are different index conventions. Scalar beta remains
`beta=X^2+2`; both beta-bearing comparators impose `C_A-2 beta`, unchanged
from the general-root proposal. H19, its proof-effective multiplier 5,
precision 40/12, anchor 25, scalar order 32, 37 contact positions, all mode
assignments, all conic tests, and the scalar/anchor modules are unchanged.

The fixed comparison target is Pstar=2R. The four variable targets are 2Q_i.
For an arbitrary source solution write `2J=j_d Pstar`, `2X0=h Pstar`, and
`2Xi=m_i Pstar`. The alternate ratios yield the valuations of
`(h-2)/j_d` and `(m_i-2n_i)/j_d`. They imply h=2 and m_i=2n_i at the
required local orders; the primary ratio m_i/h therefore approximates n_i.
Completeness uses full finite group cardinalities N1,N2 with gcd(N1,N2)=4.
Each image 2E(Fp) has order Ni/4. Their orders are coprime, so the prescribed
k=0 modulo N1/4 and k=1 modulo N2/4 and the formal p-power condition are
compatible. Choose the common comparison point `J=j_c Pstar`, with
`j_c=lcm(N2/4)`, so `j_d=2j_c`. No surjectivity of global reduction or
coprimality between orders at different rational primes is assumed.

## Literal module changes

The input is the pinned root with 344 local coordinates, 329 equations and
39 calls. The six root charts are replaced exactly as in the reviewed
target-four helper. In original indices:

* Delete the second-doubling coordinates 122..131, 142..151, 162..171 and
  182..191, and rows 110..119, 130..139, 150..159 and 170..179.
* Retain every first-doubling equation, including its inverse of 2y. If the
  root is Q=(x,y), its first slope is lambda, its stored square is L=lambda^2,
  and its last stored product is M=lambda(3x-L). Replace target-binding rows
  200..215 by x_target=L-2x and y_target=M-y. These are exactly 2Q.
* Delete the old 20 constant-base gate coordinates 92..111 and their rows
  80..99, plus the old fixed y coordinates 212,213 and rows 198,199.
* Replace rows 196,197,269..272,291..294 by the ten primitive constant
  bindings for x,F,q,conj(s),conj(t) listed below.
* Replace rows 289,290 and 295,296 by the four primitive affine equations
  for r and u in the existing common J coordinates 208,209.

The fixed constants are

```
x = (57/8, -7/2)
F = (456/1681, 224/1681)
q = (-87/41, 129/164)
conj(s) = (-55123/14637, -19301/58548)
conj(t) = (7624/14161, -39904/127449)
r = J * (-232/357, 86/357)
u = J * (291673/127449, -29440/42483)
```

Here J is the field value `1/conj(z(Jroot))`, rather than the root point.
The definitions are q=y(Pstar)/x(Pstar), F=1/x(Pstar),
s=(x(Pstar)+DF)/q and t=1/q^2. The source stores conjugated s,t and uses
r=J/conj(q), u=J*conj(s/q). All retained target and call slots keep their
previous roles. The exact constants and their squared-row contributions
were independently calculated in Charts' `root-target2/FIXED_TARGET2.json`.

The emitter checks every retained equation and every call for forbidden
references before reindexing. It reindexes all live metadata, replaces
`jacobi_targets` by `root_targets`, and keeps historical proxy-removal IDs
historical. The five target kinds are `fixed_Pstar,double,double,double,double`.
The root and all three comparators declare `comparison_target_multiplier=2`.
The new `target_two_bindings` records the 16 live variable-target row IDs.
The fixed-target receipt records ten constant-bound coordinates and rows
plus four affine-bound coordinates and rows. The original-index receipt
contains all 30 replaced rows and the exact deletion sets.

The result has 218 local root coordinates, 203 root equations and 39 calls.
This is a source-coordinate reduction of 126 from the original module,
or 40 from the target-four root helper. It is not a measured final quartic
saving. The ten constant bindings and four affine bindings have a combined
isolated sum-of-squares maximum coefficient 154563475872. This does not
bound the complete polynomial, whose overlapping terms require fresh
expansion and coefficient verification.

## Maps and acceptance boundaries

A solution of the new root equations determines each Q in E(K) through the
reviewed root chart. The retained first doubling gives exactly 2Q and its
nonzero tangent denominator. The ten fixed bindings determine Pstar's
target data uniquely; the four affine equations determine r,u uniquely.
Thus the calls consume exactly the points and coefficient convention in
the target-two arithmetic theorem. Conversely any points and comparison
data chosen by that theorem extend to these root equations by the ordinary
doubling formulas and the displayed constants. These maps preserve the
original input coordinate 0.

This is not an extension map for an arbitrary target-four solution: its
comparison witnesses belong to a different arithmetic source. Completeness
is supplied by the separately proved target-two construction. The emitter
does not claim equality of private witness projections between those sources.

`test_target2_rewrite.py` performs small author fixtures only. Charts owns
an independent literal constructor and rejection tests. Acceptance of an
emitted candidate also requires the complete new source ledger, original
construction comparison, independent module audit, fresh flattening and
lifting, algebraic replay, and full polynomial expansion. None is inferred
from the local coordinate count or the isolated coefficient calculation.
