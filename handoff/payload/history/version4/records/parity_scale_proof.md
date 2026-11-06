# Fuse the parity argument's square factor

This is an exact algebraic projection rule. It requires no new trace theorem, arithmetic hypothesis or restriction on the two retained rational inputs `r,W`. It replaces the existing twelve-variable quadratic parity template together with its two private argument gates `B2=W^2`, `b=r*B2`.

## Source-level identity, including zero

The old seven-witness source predicate at `b=rW^2` is

```text
Uo*(1+b*to^2) = b*(1-b*to^2),
po^2 = 17b*(1-eo)*(1+3eo),
ho = eo*(17b-Uo^2),
17b*qo^2 = (so^2-17b*ho)*(so^2+51b*ho).
```

The rescaled version has eight private variables `t,U,e,p,q,s,h,L`:

```text
U*(1+r*t^2) = r*(1-r*t^2),
p^2 = 17r*(1-e)*(1+3e),
L = W*U,
h = e*(17r-L^2),
17r*q^2 = (s^2-17r*h)*(s^2+51r*h).
```

For `W!=0`, the map from new witnesses to old is

```text
to=t/W, Uo=W^2*U, eo=e, po=W*p,
ho=W^2*h, so=W^2*s, qo=W^3*q.
```

Its inverse uses the corresponding inverse powers of `W` and sets `L=W*U`. Substitution multiplies the four new source residuals, after using `L=W*U`, by `W^2,W^2,W^2,W^8` respectively. Thus both maps are exact for every rational `r`, including zero.

For `W=0`, the old input is `b=0`, and the old predicate has the all-zero witness tuple. The new predicate also has a solution for every rational `r`:

```text
t=0, U=r, e=1, p=q=L=0, h=17r, s=17r.
```

Indeed `s^2=17r*h`, so the last equation has both sides zero. Therefore neither direction excludes `W=0`; all internal witnesses may be replaced in that branch. Only `r,W` and other outside coordinates must be preserved.

## Quadratic template and direct maps

The installed old conic template has private variables
`uo,vo,ao,zo,eo,po,co,wo,so,qo,jo,ko` and rows

```text
zo=uo^2, ao=b*vo, zo+vo*ao=b^2,
co=b*eo, po^2-17b-34co+51eo*co=0,
wo=co*(17b-zo), jo=so^2, ko=b*qo,
jo^2+34jo*wo-867wo^2-17qo*ko=0.
```

Together with `B2=W^2,b=r*B2`, that is fourteen private variables and eleven quadratic rows. Replace it with thirteen private variables
`u,v,a,L,z,e,p,c,w,s,q,j,k` and ten rows:

```text
a=r*v,
u^2+v*a=r^2,
L=W*u,
z=L^2,
c=r*e,
p^2-17r-34c+51e*c=0,
w=c*(17r-z),
j=s^2,
k=r*q,
j^2+34j*w-867w^2-17q*k=0.
```

Every new row has integral coefficients, total degree at most two and maximum absolute coefficient at most 867. Their sum of squares is a quartic. The full exporter must still compute the global coefficient bound.

There are direct maps between these quadratic systems, so acceptance does not depend on choosing a chart for the conic parametrization. For `W!=0`, map old to new by

```text
u=uo/W^2, v=vo/W, a=r*v, L=W*u, z=L^2,
e=eo, p=po/W, c=r*e, w=wo/W^4,
s=so/W^2, q=qo/W^3, j=s^2, k=r*q.
```

The old norm equation divided by `W^4` gives the new norm equation. The first-conic row divides by `W^2`; the `w` row by `W^4`; and the last row by `W^8`. All remaining rows are definitions. Conversely, from new to old set

```text
B2=W^2, b=rW^2,
uo=W^2*u, vo=W*v, ao=b*vo, zo=uo^2,
eo=e, po=W*p, co=b*e, wo=W^4*w,
so=W^2*s, qo=W^3*q, jo=so^2, ko=b*qo.
```

These formulas in fact give an old solution for `W=0` as well. To extend any old solution at `W=0` in the other direction, use

```text
u=r, v=a=L=z=p=q=k=0, e=1, c=r,
w=17r^2, s=17r, j=289r^2.
```

The last row is zero because `j=17w`. No division by `r`, `b`, any conic coordinate, or any possibly zero norm root is used. The sole division by `W` has the separate branch just proved.

## Checker obligations and cost

The checker must match the nine old conic rows and both argument rows exactly up to nonzero rational scaling. All fourteen deleted coordinates must be distinct, non-input and private to these eleven rows; neither retained input may be among them. Retained inputs may have arbitrary outside uses. Replacement coordinates must be fresh, and the rule must delete every old selected row before writing the ten replacements.

Under those conditions every solution extends in both directions while retaining all outside coordinates. Hence the original source's integer completeness, exceptional cases and pole soundness are preserved without changes. The rule is allowed even if `r=W` or either retained input is zero. It does not share witnesses between parity calls.

The local measured template count drops by exactly one variable and one nonzero quadratic row. In the current three-mode source, all 37 ordinary batches have both private argument gates. The separately corrected height batch is outside this rule's initial scope. A complete run may therefore remove 37 variables if every old conic template and its gates still match and remain private. No final endpoint saving is claimed before that replay.
