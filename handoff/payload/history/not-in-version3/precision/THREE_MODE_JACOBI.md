# Explicit composition of three comparator modes with Jacobi differences

This is a separate source contract for the composition of `THREE_MODE_CONTACTS.md` with the reviewed `../charts/PROOF.md` Jacobi difference model. It does not modify the frozen affine contracts. Source generation and independent audit must explicitly set `difference_model` to `Jacobi complete`; describing this source as retaining the old affine subtraction guards would be false.

Keep the exact three-mode root partition, input-selection indices, high/beta precisions and norm-test counts. The target four-tuples in each comparator now mean the two coefficients of U and the two coefficients of q, with U^2=1/x_target and q=y_target/x_target. They no longer mean affine x,y. These tuples are obtained once from the five shared targets 4P_*,4A,4S,4T,4Z, using the three field equations

```
x_target*F=1, U^2=F, q*x_target=y_target.
```

The root's eight height targets remain the original unscaled affine x-coordinate coefficients of A,S,T,Z. Neither U nor q is a height target. All root affine coordinates and doubling chains remain available to check this distinction.

For a retained private primary point with coordinates u,p,x and its target U,q, replace only that difference block by the five field variables r,v,w,T,Z satisfying

```
r=uU, w=rv, v+D*r*w=q-p,
T=2x-pq+2pv, ZT+q-p=0.
```

The reviewed Jacobi identities show that these are uniquely determined rational expressions in the inputs. Their denominators 1+D*r^2 and the resulting h_R are nonzero; w=0 represents the identity difference. When w is nonzero, the represented difference has f_R=w^2 and z_R=Z. The joint source must not add an inverse of w, Z or the difference itself.

In each mode retain primary f tests and the already-conjugated f(J) test, and replace every conjugated order-one difference f test by conjugated w. Keep every alternate ratio as conjugate(Z) times the already-conjugated inverse z(J). Thus the lists are:

| Mode | Order-one field tests | Later field tests | Rational orders |
| --- | --- | --- | --- |
| Full | five primary f, common conjugate f(J), five conjugate w | four primary proxy ratios and five alternate Z ratios, with the same q/K assignment | `[1]*23+[q]*2+[K]*8+[q]*2+[K]*6` |
| Beta-only | two primary f, common conjugate f(J), two conjugate w | one primary beta ratio and two alternate Z ratios, all q | `[1]*11+[q]*6` |
| Lucas-only | four primary f, common conjugate f(J), four conjugate w | three primary Lucas ratios and four alternate Z ratios, all K | `[1]*19+[K]*14` |

The first rational test in every row remains the root-error test. Source auditors must check expression identity and ordering, not only these lengths. Input selection is unchanged numerically, but its target slots must be explicitly retyped as U,q as described above.

At any relevant split prime, the order-one w condition places the difference in the formal group. For w nonzero the reviewed identity h_R^2=1-Dw^4 gives h_R a unit and v(Z)=v(w); for w=0 both the group difference and its logarithm are zero. Hence every retained alternate ratio has the same valuation as the corresponding integer index difference divided by j, allowing infinite valuation when the difference is zero. This is exactly the local conclusion used in `THREE_MODE_CONTACTS.md`. The two global height arguments and their distinct maxima are therefore unchanged.

Completeness uses the same prior choice of indices away from0,4,-4 and the same common J. Every shared target is a second double, so the reviewed formula U=2y2/(x2^2+D) supplies its square-root lift without a new hypothesis. Evaluate the Jacobi expressions after fixing the primary points; then choose theta last, including the actual rational coefficients of every new conjugated w. There are finitely many requirements across all modes, including repeated primes, so the same orientation and CRT argument applies. No old coefficient bound for f_R is substituted for the new coefficient bound for w. Norm positivity, square reduced denominators, the root37 infinity square factor and the three local square conditions are unchanged.

This establishes the arithmetic compatibility of the three-mode partition with the complete Jacobi model, conditional on the same reviewed inputs. It does not assert a rational map back to the old guarded affine difference chart at coincident points. A fresh source audit must check all retained and removed consumers, the shared target extension, the retyped boundaries, and each mode's exact test expressions before any finite lift or quartic count is accepted.
