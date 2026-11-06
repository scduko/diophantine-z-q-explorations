# Fuse the scalar comparison inverse

This is an exact algebraic projection rule on the separately reviewed
target-two root. It changes no arithmetic assumption, precision or index.
It is not included in the frozen target-two packet.

Write z_S for the retained formal parameter of the root S, z_0 for that of
the scalar-height root J0, i for the old inverse of z_0, and lambda for the
scalar ratio. The old equations are

    z_0 i=1,       lambda=z_S i.

The new equation is

    lambda z_0=z_S.

All equations are field equations in K=Q(sqrt(2)), implemented by their two
rational coefficient equations. The retained S chart has x_S f_S=1 and
y_S z_S+x_S=0. Therefore x_S is nonzero and z_S is nonzero. It follows from
the new equation that both lambda and z_0 are nonzero.

The forward map forgets i. The reverse map sets i=lambda/z_S, equivalently
i=1/z_0. This satisfies both old equations, while preserving every retained
variable. These maps are inverse on the old solution set and the new one.
In particular they preserve rational solutions and the distinguished input.
No p-adic or height argument is used to remove the inverse.

There is also a polynomial restoration formula in the retained coordinates:
the two S equations give 1/z_S=-y_S f_S, hence

    i=-lambda y_S f_S.

Its degree is irrelevant to the source degree because it is only a witness
map. The emitted replacement equations are quadratic.

In the target-two root, inverse coordinates 28,29 occur only in rows 6..9
and in no call. Rows 6,7 are the inverse equations. Rows 8,9 define lambda
at coordinates 30,31 from z_S at 6,7. The height parameter z_0 is at 24,25.
The helper checks the exact parent digest and these literal equations,
deletes coordinates 28,29 and rows 6,7, and replaces rows 8,9 by the displayed
product equation before reindexing every live coordinate and row field.
Historical provenance is left unchanged and identified as historical.

The output root has 216 local coordinates, 201 rows and 39 calls. Other modules
and every call's semantic arguments are unchanged. The two removed original
inverse coordinates are both live in the verified normalized5364 census;
a final saving still requires the fresh composed source and replay.

Use `fuse_scalar_ratio.postprocess_modules` immediately after the target-two
helper, before tangent or shared-square rewrites. Those later helpers need
their own explicit binding to the new root coordinates. The module pin is
not a replacement for complete parent-source verification.
