# Root postprocessor implementation review

Verdict: PASS for the four-module source delta at the hashes below. The full
source and final polynomial remain unaccepted pending fresh source checking,
lifting, reduction replay and expansion. The measured allocation here is
only the small root module.

| File | SHA-256 |
| --- | --- |
| precision/sub5000/root-doubled-indices/root_rewrite.py | 5a9d82fdb68db591a275c67b2c555735e1376a6a86da21221d76976abd68d479 |
| audit_root_rewrite.py | 05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2 |
| test_root_audit.py | 4d3499f018b3e268d67f4c0dad007905cc39dc2e9b2457eb484ef603d74f3ba8 |
| arithmetic-audit/sub5000/HALF_GENERATOR_COMPOSITION_CONTRACT.json | 4e41f830938c3bdf8b5361b410a2fb639bd74299f0461fb356afe2efb012f2b7 |

The independent auditor uses literal integer-coordinate formulas rather
than the emitter's generic field multiplication or label-based selection.
It pins all four input modules and reconstructs complete output objects.
The four root curve pairs expand y^2-x*q+(11-6sqrt(2))*x with the correct
signs. The J0 and J pairs expand k=f*z and f-z^2+(11-6sqrt(2))*k^2.
Their imaginary equation is f1-2*z0*z1-6*k0^2-12*k1^2+22*k0*k1.
The retained original z inverses exclude f=z=0. The existing inverses of
2y exclude all affine two-torsion branches in the x,y charts.

All four original x^2 pairs are reused. Their definitions, inverse-of-2y
rows, downstream doubling equations and call arguments remain in the
exact expected output. The remaining S reciprocal and z equations retain
its scalar and anchor interface. The common f(J) conjugation alias is
unchanged, which permits the separate shared-square rewrite.

The exact fixed-target x,q values were independently calculated in
FIXED_TARGET.json and checked on the curve. The implementation deletes the
old two-doubling constant circuit and fixed ordinate, binds just these four
rational coefficients, and retains F and all shared joint coefficients.
The x*F=1 equation and exact q^2=x-D*F identity supply the same required
target interface. The four isolated squared bindings fit below 2^80;
the final aggregate bound remains a full-replay obligation.

The scalar beta definition remains beta=X^2+2. Exactly one real-component
row in each beta-bearing comparator becomes C_A-2beta. Its imaginary
component and all field-order data remain unchanged. Lucas-only rows are
unchanged. All three comparator metadata objects identify R as the base
and the integer doubled-index convention. No scalar or anchor equation
is changed.

All current coordinate and row metadata is reindexed. The first target
is explicitly fixed_4R with x,p,f; the old ordinate is not retained as
misleading metadata. Historical proxy-removal IDs remain historical.
Complete-object comparison rejects extra or missing rows, calls, keys,
declarations, and wrong metadata, including bool-versus-integer changes.
Root declaration coverage is also checked independently.

I ran the bounded fixture with CPython 3.14 using -E -B. It compared all
four emitter outputs with the independent construction and passed 92
semantic negative tests plus one resource-abort regression. The root has
258 local coordinates, 243 rows and 39 calls, down by 86 coordinates and
86 rows from its pinned parent. This does not predict the final quartic
variable saving. No full source was generated locally.

The input carrier change is justified by the separate reviewed global
doubled-index proof; it is not a claim that every new root can be lifted
to the old 2E chart. The source integration must disable old root gpoint
locators for general_E_mixed, pin every dependency, and check the complete
flattened source before any artifact can be accepted.
