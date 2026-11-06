# Independent square-transfer review

PASS for the exact existential equivalence in `charts/SQUARE_TRANSFER.md`, SHA-256 `507651e852d764e84cafb447f03ccca09da6c8631836ddd80b6161e5fb5daada`, relative to the complete Jacobi source reviewed in `REVIEW.md`.

Each retained target is the final double of a retained affine point V. The rational function `U=2y(V)/(x(V)^2+D)` is defined because the retained doubling inverse forces y(V) nonzero and total positivity forces x(V)^2+D nonzero. The doubling equation gives U^2=F_Q. Thus deleting the shared U and passing F_Q instead does not require a new square-root assumption or an independent choice at each occurrence.

The retained equations x*f=1 and a*F_Q=1 make both factors nonzero. The replacement r^2=f*F_Q therefore makes r nonzero. Set u=r/U for each primary point. Then u^2=f and r=uU, restoring exactly the two relations needed by the former complete Jacobi source. Every retained w,Z,G,ratio and norm-test value is unchanged. If a former U had the opposite sign, u changes with it; this affects only the omitted sign choices.

Conversely forgetting u,U in a former solution gives r^2=f*F_Q directly. Hence both projections to retained coordinates agree. The reverse map is rational in the retained root-doubling witnesses and r. The equivalence is stronger than equality of integer-input projections, but it is not a bijection on the forgotten signs.

This argument applies to every retained primary point in all three comparator modes. There must be exactly one associated difference r from which to reconstruct that point's u, and all outside uses of u must be absent or reconstructed. The existing complete Jacobi source has precisely its f=u^2 and r=uU uses; the G expressions and ratio equations use f,p instead. Root affine coordinates and doubling chains must remain reconstructible.

The modified boundary must explicitly mean F_Q,q instead of U,q or x,y. The 16-, 26- and 31-input index selections may be reused only with that semantic change recorded. The original eight height coefficients remain those of x(A),x(S),x(T),x(Z). No old affine subtraction guard is reintroduced, and identities continue to have w=Z=0.

Because every rational test value is preserved, the prior raw-contact, formal-logarithm, theta, norm/pole, completeness and global-height arguments apply without alteration. This includes the root37 square-times-prime infinity contact and all three mode counts. No new external arithmetic result is used.

The standalone implementation still targets 64/16 and 41 full calls; its exact finite execution and any combined three-mode implementation are separate audit obligations. In a three-mode source the number of private primary points is 13*5+8*2+16*4=145, so one must not carry over an allocation estimate that assumes 37*5 points. This review asserts no measured variable saving or final coefficient bound. No code was executed locally.
