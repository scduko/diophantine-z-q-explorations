# Exact parity replacement

The input is the same rational number `b`. Put `B=17b`. The pinned source
uses seven private witnesses `t,U,e,p,q,s,h` and equations

```
U(1+bt²) = b(1-bt²),
p² = 17b(1+2e-3e²),
h = e(17b-U²),
17b q² = (s²-17b h)(s²+51b h).
```

The replacement uses twelve private witnesses
`u,v,a,z,e,p,c,w,s,q,j,k` and nine equations

```
z = u²,
a = bv,
z+va = b²,
c = be,
p²-17b-34c+51ec = 0,
w-17bc+cz = 0,
j = s²,
k = bq,
j²+34jw-867w²-17qk = 0.
```

Every displayed residual has total degree at most two. Its largest absolute
coefficient is 867. This bound is only local. The producer and full verifier
must check the coefficient bound after adding the squares of all residuals.

## Forward rational map

Let `D=1+bt²`. The source equations force `D≠0`. If `D=0`, then `bt²=-1`
and the first source equation gives `0=2b`, which contradicts `bt²=-1`.
Define

```
u=U, v=2bt/D, a=bv, z=U², c=be, w=bh, j=s², k=bq.
```

Keep `e,p,s,q`. The first source equation yields
`U=b(1-bt²)/D`. Direct expansion gives

```
[b(1-bt²)]² + b(2bt)² = b²(1+bt²)².
```

Thus `z+va=b²`. The first source conic gives the fifth replacement equation.
The source definition of `h` gives `w=be(17b-U²)=c(17b-z)`.
The last replacement equation is the negative of the last source residual
after substituting `w=bh`, `j=s²`, and `k=bq`.

## Reverse rational map

The replacement forces `u²+bv²=b²`. Keep `e,p,s,q` and define
`h=e(17b-z)`. Choose `U,t` as follows.

* If `b=0`, the norm equation forces `u=0`, hence `z=0`. Take `U=t=0`.
* If `b≠0` and `u+b≠0`, take `U=u` and `t=v/(u+b)`.
* If `b≠0` and `u+b=0`, the norm equation forces `bv²=0`, hence `v=0`.
  Take `U=b` and `t=0`.

In all cases `U²=z`. In the middle case the first source residual, multiplied
by `(u+b)²`, is

```
(u-b)(u+b)² + b(u+b)v²
  = (u+b)(u²+bv²-b²)
  = 0.
```

The other two cases satisfy that residual directly. The definition `c=be`
turns the replacement first conic into the source first conic. Also
`w=c(17b-z)=bh`. This gives the source last conic using `j=s²` and `k=bq`.
No division by `b`, `e`, `h`, or `s` occurs.

The reverse map can change the sign of `U`, and it need not preserve `t`.
The transformation is therefore an equality of existential projections, not
a claimed bijection of witness tuples. The old seven witnesses and every
deleted lift gate must have no use outside the selected rows. The checker
tests this condition in the full current residual incidence map.

## Source and gate checks

`parity_rule.py` contains independent hardcoded source and replacement
polynomials. It expands acyclic old gate definitions and compares all four
source residuals coefficient by coefficient up to nonzero rational scaling.
Every old witness and deleted gate must be private to those four rows and
their gate definitions. Every replacement witness must be a fresh allocation.
The shared verifier checks all supplied patches, every resulting degree,
the global source hash, and the complete expanded quartic.

`produce_parity.py` works on the raw `norm-base` parent. It deliberately fails
if simplification has already changed any required lifted row. It uses the
initial certificate's gate map and the pinned construction map to find every
instance. It does not change source files or hashes.

## Scope of failed alternatives

Directly substituting `h=e(17b-U²)` into the last source equation increases
degree and gives no useful quadratic lift without new gates. The replacement
instead stores `w=bh` and shares `c=be` between the first conic and `w`.

A single ordinary affine parametrization of the first conic excludes a
rational base point. For example, using `p/(1-e)` excludes `e=1,p=0`, which
occurs in source solutions. Unlike `U`, changing `e` changes `h`. No argument
was found that would justify deleting that chart while preserving the second
conic. Such a deletion is not part of this proposal.

Likewise, dividing by `s`, `h`, `e`, or `b` without branches is invalid.
The source has solutions with each of those quantities zero. The checked
replacement uses no such division and does not assume arithmetic facts about
the parity predicate.
