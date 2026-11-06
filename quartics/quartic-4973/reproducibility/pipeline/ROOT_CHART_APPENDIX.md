# Smaller charts once the root carrier is enlarged

This is a separate implementation option for `PROOF.md`. It does not change its arithmetic relation, doubled-index convention, fixed base R, beta test or cutoffs. It replaces the conservative uniform chart by charts adapted to the actual root consumers. The new root source still requires a complete independent incidence audit. No existing source has been changed.

## A, T and Z: reuse the first doubling's square

These three root points expose only x,y: the raw height targets use x, and the first doubling uses x,y. Retain just these two field pairs. Let q be the field pair x^2 already allocated by that first doubling and impose

    q=x^2,       y^2=xq-Dx.                           (1)

The first equation is already part of the doubling, so only the second is new. It is quadratic in the retained pairs. Keep the original first-doubling inverse of 2y, or its independently verified compressed tangent equation

    2y lambda=3q-D.                                  (2)

Either supplies the necessary nonzero condition. For the compressed version, if y=0, (1) gives x in {0,d,-d}. Then 3q-D is respectively -D,2D,2D, all nonzero, contradicting (2). Thus y and x are nonzero. Equations (1) define the same nontorsion curve point as the conservative chart; recover f=1/x, z=-x/y and p=y/x if needed for the proof. Those recovered quantities are not source coordinates here.

Conversely any nontorsion point has x,y nonzero and its actual doubling supplies q,lambda and the remaining old doubling data. This preserves the downstream quadruple 4Q exactly. No branch of the elliptic doubling law is discarded.

## S: keep the two scalar/anchor outputs

Use the same x,y and the same first-doubling pair q, with (1),(2). In addition retain f,z and

    xf=1,       yz+x=0.                              (3)

These are exactly the f(S),z(S) values consumed by the unchanged anchor and scalar batch. No u,v or p pair is needed. The nonzero conditions and rational reconstruction are the same as above.

## J0 and J: use only f,z and their product

For each auxiliary root keep f,z and a new field pair k, with

    k=fz,       f=z^2-Dk^2.                          (4)

Retain the existing inverse of z(J0) used in the scalar ratio and the existing inverse of conjugate(z(J)) used by every comparison. Thus z is nonzero. Equations (4) then imply f is nonzero: f=0 would force k=0 and z^2=0. Set

    x=1/f,       p=-1/z,       y=xp.

Dividing (4) by z^2 gives fp^2=1-Df^2, so y^2=x^3-Dx and y is nonzero. These formulas recover exactly f=1/x and z=-x/y. Conversely any nontorsion curve point supplies a unique k=fz. Hence (4), with the retained z inverse, has precisely the required nontorsion curve-point image.

The old root code uses x(J0),y(J0),x(J),y(J) only inside their own point charts. They are not height targets or doubling inputs. This is confirmed at the source-code interface; the new producer's audit must check the actual emitted residuals, calls and all variable-bearing metadata before deletion. The public outputs remain f(J0),z(J0),f(J),z(J).

## Allocation and verification boundary

The old raw root charts allocate 16 rational coordinates each, 96 in total. This option allocates four each for A,T,Z, eight for S, and six each for J0,J, totalling 32. The four first-doubling q pairs are pre-existing allocations and are not counted as new chart coordinates. The source-level difference is therefore 64 coordinates before later optimizations.

The measured normalized5512 root slice has 79 surviving point-associated coordinates: A,S,T,Z each have 14, J0 has 12, and J has 11. Its receipt is `elimination/sub5000/normalized5512-root-slice.json`, SHA256 `fce094e7a1f44ca9d06acf667479eb890d1252d57eeb61366548c8945577ffae`. Comparing 79 with the new 32 gives a 47-coordinate allocation opportunity; it is not a measured net saving. Existing linear eliminations may identify new coordinates, and the new root equations may change later reductions. Two additional surviving original lift coordinates lie outside those 79 and are not counted as savings here.

The independent source checker must verify the exact square reuse, tangent equations or inverse, the untouched scalar/anchor outputs, both retained auxiliary z inverses, and every old deleted coordinate's incidence. This is a fresh source implementation of the enlarged arithmetic carrier, not an algebraic deletion rule on the old 2E source.
