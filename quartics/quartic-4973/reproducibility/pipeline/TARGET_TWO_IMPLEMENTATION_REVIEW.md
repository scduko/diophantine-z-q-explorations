# Target-two source implementation review

Verdict: PASS for the literal four-module delta at the hashes below.
The new full source and final polynomial are not accepted by this review.

| File | SHA-256 |
| --- | --- |
| precision/sub5000/target-two/target2_rewrite.py | fa53e47698aaa11ddaf1383f74fb690fb69557c696064c8fd036893660c7c799 |
| precision/sub5000/target-two/CONTRACT.md | 8e42299e4d281ecab724868d39eeb21589957c971516296500b942605ac0b711 |
| audit_target2.py | b2737e3575ad8512dcc33c6c1d84f38178172e53b5d786193d8eed5c1df886c3 |
| test_target2_audit.py | c25ef8482c8f01befd2c0c9e5e3465cc3e221b7cd7d3cd821fe2cc9f1a240e67 |
| AUDIT_TEST.json | fd7501527b570641c962fbd17dcfc909a330e2eaaa1f89f22d9c97ad8e7cdec9 |

The independent audit uses the pinned independent root-four constructor,
then applies its own literal target-two delta. It does not use the
producer's field arithmetic, label discovery or rewriting functions.
All four produced modules agree exactly with that independent result.

For a retained root Q=(x,y), the first doubling has q=x^2,
lambda=(3q-D)/(2y), L=lambda^2 and M=lambda(3x-L). The new target binding
is exactly x2=L-2x and y2=M-y. Thus it is 2Q. The existing inverse of 2y
and the root curve equation remain, so this computation has no denominator
exception. The second-doubling coordinates are private after replacing
these four target bindings and may be removed. Full row and call
reconstruction verifies that none retains a reference to them.

Conversely, any root points and target-two comparison data supplied by the
reviewed arithmetic construction extend to these equations by the displayed
first-doubling formulas. The root chart inverse maps remain those in the
reviewed chart appendix. This is a source implementation of the target-two
theorem, not an extension of arbitrary target-four comparison witnesses.

The ten direct x,F,q,conjugate(s),conjugate(t) bindings agree with the exact
Pstar calculation in FIXED_TARGET2.json. The four linear rows are, in original
source indices and writing J=(J0,J1),

    357 r0 + 232 J0 - 172 J1 = 0,
    357 r1 - 86 J0 + 232 J1 = 0,
    127449 u0 - 291673 J0 + 176640 J1 = 0,
    127449 u1 + 88320 J0 - 291673 J1 = 0.

They implement r=J/conjugate(q) and u=J*conjugate(s/q), with J the
existing inverse-conjugate-z field. Both components and signs are checked
literally. Every new row is affine or quadratic. The isolated 14-row
sum of squares fits in 38 coefficient bits, including shared-J cross terms.
The full polynomial still needs its own bound check.

The source retains all scalar and anchor constraints, all six root chart
interfaces and both auxiliary z inverses. Raw height values still use the
original root abscissae. All three comparison boundaries keep the same
coordinate slots, with truthful target-two metadata. Both beta-bearing
comparisons still use C_A-2beta and beta=X^2+2. The private half-index
metadata is distinct from the integer doubled indices of root points.

I ran the small fixture under CPython 3.14 with -E -B. It compared the
complete four-module producer output and passed 112 semantic rejections
plus one resource-abort case. The root has 218 locals, 203 equations and
39 calls, which is 126 fewer raw root coordinates and equations than the
original pinned root. No full source was generated. Final variable savings,
coefficient bounds and theorem/source linkage require the complete outer
audit and remote replay.
