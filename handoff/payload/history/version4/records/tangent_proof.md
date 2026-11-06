# Four direct tangents after the target-two rewrite

This fragment starts with the exact target-two root module. Its four
remaining doublings are the first doublings of A, S, T and Z. The earlier
eight-doubling fragment is a separate, unchanged option.

Work in K=Q(sqrt(2)), D=11-6sqrt(2). The rational norm of D is 49, so D
is invertible. Each input point has retained equations q=x^2 and
y^2=x*q-D*x. The old doubling also has

```
(2y)*h=1, lambda=(3q-D)*h,
a=lambda^2, X=a-2x, b=lambda*(x-X), Y=b-y.
```

Delete h and its two rational component equations. Replace the two slope
equations by the components of

```
2y*lambda=3q-D.
```

The old equations imply the replacement by multiplication. To recover an
old witness from any new one, let n=3q-D and f=x^3-D*x. The exact identity

```
n*(3q-2D)-9x*f=2D^2
```

holds when q=x^2. Since f=y^2 and n=2y*lambda,

```
y*[2lambda*(3q-2D)-9xy]=2D^2.
h=[2lambda*(3q-2D)-9xy]/(4D^2).
```

Thus y cannot vanish; the displayed polynomial with constant denominator
recovers h, satisfies (2y)*h=1, and then satisfies lambda=(3q-D)*h. All
its rational coordinate coefficients are rational because D is a fixed
invertible element of K. This formula is a witness reconstruction, not
an extra equation in the new source. No root extraction or additional
rational existence assumption is used.

The retained equations for a, X, b and Y remain identical. The output is
the same doubled point, and it still lies on the curve: putting t=X-x and
Y0=-y-lambda*t gives the exact identity

```
Y^2-X^3+D*X
 = (y^2-x^3+D*x) + t*(2y*lambda-3*x^2+D)
   + t^2*(lambda^2-X-2*x) + (Y-Y0)*(Y+Y0).
```

Every term on the right vanishes under the retained equations. There is
no second doubling in this parent source.

## Source boundary and privacy

The accepted root has canonical SHA256
`1cf2a225d6aeff52adfd5f6e87ca5e4cdadcec0bd3f43d68d7ec972ce40b49b2`,
where canonical means sorted-key compact ASCII JSON followed by a newline.
It is the output of `target2_rewrite.py`, SHA256
`fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799`,
on its pinned normalized-linear-pole root.

The producer checks all forty old doubling component equations and all
eight input-curve equations. It checks each deleted inverse component
against every row and every call. Its only consumers are the two inverse
and two slope equations being replaced. It remaps all live variable and
row metadata, including fixed-target linear bindings and target-two
output bindings; older provenance records keep their historical IDs.
All unchanged rows and calls are preserved under the index map, and
input coordinate zero remains zero.

The source changes from 218 to 210 local coordinates and from 203 to 195
residuals. The four deleted pairs are parent local IDs 38/39, 48/49,
58/59 and 68/69. These are source counts, not a measured final quartic
saving. The replacement rows are quadratic. Their coefficients and the
unchanged fixed-target rows remain subject to full-source generation,
lifting, replay and final coefficient checking.

This postprocessor neither accepts an old certificate modification nor
authorizes a source entry. It must run before any shared-square append,
and a composed source needs its own exact independent audit and registry
binding. The existing target-two and eight-tangent files remain unchanged.
