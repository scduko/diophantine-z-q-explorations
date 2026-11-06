# Independent scalar-J0 inverse-fusion review

PASS for the exact root-module transformation below. No mathematical or
source-incidence defect was found. This review does not accept a complete
new source entry or establish a measured quartic saving.

Reviewed producer: `precision/sub5000/scalar-ratio/fuse_scalar_ratio.py`,
SHA256 `5563acb0e214d5084faea7edb174860425a730b26241a7131a7d3cbfa4831949`.
Reviewed proof: the adjacent `PROOF.md`, SHA256
`6814cb5338f5a42bf0c9863b2f0b67b5a0bc9d312b2df03745f1691632ea32e7`.
The producer author and this review/checker author are different agents.

## Rational maps and zero cases

Write x,f,y,z for the retained S coordinates, z0 for the height-J0 formal
parameter, L for the scalar ratio, and i for its old inverse. The four S
component rows 1..4 express x*f=1 and y*z+x=0 over Q(sqrt(2)). Thus

```
z*(-y*f)=1.
```

In particular x,y,z and f are nonzero. The new equation L*z0=z forces
both L and z0 nonzero, so neither zero-factor branch can be introduced.
An old solution projects to the new one. Conversely, keep all retained
coordinates and set i=-L*y*f. This restores i*z0=1 and z*i=L.

These statements have exact polynomial certificates. With
a=x*f-1, b=y*z+x and c=L*z0-z,

```
(-L*y*f)*z0-1 = -y*f*c - f*b + a,
z*(-L*y*f)-L = L*(a-f*b).
```

The checker tests expand both identities independently. No square root,
variable denominator, p-adic premise or height premise is used. The cubic
inverse formula is a witness map; both emitted component rows are quadratic.
The distinguished coordinate zero and its defining residual stay unchanged.

## Exact source boundary and incidence

The input is the root produced by target-two helper
`fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799`.
Its sorted-key compact-JSON-plus-newline SHA is
`1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2`.
The producer's insertion-order serialization of that same dictionary has
SHA `6ea7c5eb38c12b174c389744150a748910a8c2b35e25193fe71c2541854809ea`.
Both pins were checked against the exact normalized-linear-pole root.

The deleted inverse coordinates 28/29 occur exactly in rows 6,7,8,9 and
in no call. The new rows replace 8/9; rows 6/7 disappear. All other rows,
all 39 calls, live variable and row metadata, construction labels, target
bindings and historical receipts were compared with the exact index map.
Historical receipts remain in their original index systems. Output counts
are 216 local coordinates and 201 rows, from 218 and 203.

The output canonical SHA is
`6ad87fbd34af7c6d4b2abc1b9dd40cd7f3bd84e5bca081f24f84b33935267ede`.
This is a source allocation reduction of two, not a measured endpoint
reduction. The previously measured normalized5364 endpoint retains both
corresponding old source inverse coordinates.

## Tangent composition and scope

The frozen four-tangent branch `a136e6cc...` leaves the first ten target-two
rows unchanged, including every scalar-fusion support row. Therefore its
algebra does not interfere with this fusion. However, applying scalar
fusion first renumbers the subsequent tangent coordinates and changes the
input hash. The existing tangent producer must reject that new input;
composition requires a separate explicitly rebound tangent producer and
independent checker, or a separately pinned scalar transition after tangent.
The old tangent files must not be silently repurposed.

`check_scalar_ratio.audit_root_transition(target2_root, fused_root)` is the
independent root-only checker. It imports no producer. It reconstructs both
new rows literally and every other output field under an independently
specified index map. It pins the complete parent dictionary, checks all
inverse consumers and retained S proof rows, and compares canonical bytes
to distinguish JSON booleans from integers. A module-level assertion guard
rejects optimized imports; bounded JSON preflight distinguishes resource
aborts from mathematical rejection.

Checker SHA: `af5576603f8a6e99b13f6399fb8729cb5e75f133abd0103fe0058be6d64c85d0`.
Test SHA: `999a2677535ce008396f42a3bdb418f4397cdd40a7aa5e0e55c79c528081b7c6`.
Receipt `CHECK.json` SHA:
`5a42ea2cd207b525b04381744c200ab349fd1f6ee152edfd05a19fd5b2414adb`.

Executed: 64 exact rational-field cases, two independent polynomial
identities, 24 semantic rejection cases, one resource abort, optimized-import
rejection, complete output equality and the tangent support-row check.
No complete source generation, certificate replay or quartic expansion ran
locally. Complete source auditing, fresh named-source binding and full
coefficient checking remain the outer pipeline's responsibility.
