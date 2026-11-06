# Independent review of the root literal checker

Date: 2026-11-06. PASS for the four-module checker and its bounded tests. Full source composition remains the outer checker's responsibility.

Reviewed `charts/sub5000/half-generator-review/audit_root_rewrite.py`, SHA-256 `05fa04d6016212cdfde1613ce3c265f984cfa6f4adcc48737e714269dbbb01b2`, and `test_root_audit.py`, SHA-256 `4d3499f018b3e268d67f4c0dad007905cc39dc2e9b2457eb484ef603d74f3ba8`. The producer compared in the test is pinned to `5a9d82fdb68db591a275c67b2c555735e1376a6a86da21221d76976abd68d479`.

I read the complete checker. It imports no producer or field-algebra generator. Its four parent modules are exact hash pins, checked both on file loading and object entry points. Expected root output combines the unchanged pinned rows with independent literal rational-component expansions for the 16 new chart rows and the four exact fixed-target rows. The real and imaginary coefficients of D=11-6sqrt(2), especially the mixed k0*k1 terms, are correct.

The explicit deleted-ID intervals and maps agree with the independent integration census. Candidate equality covers every row, call, construction record, count and metadata value. It distinguishes booleans from integer IDs. Current point/target/chart coordinates are remapped, the obsolete fixed ordinate disappears, and the old proxy-removal receipt remains historical. The new root declarations cover exactly 258 locals and 243 equations and have no forward coordinate references. Fixed-target and all variable-target records retain the correct types.

The two beta-bearing comparator specifications change exactly the literal real binding row from C_A-beta to C_A-2beta. All other comparator residuals and call arguments remain the parent's. The Lucas-only module changes metadata only. The checker requires the new R4 label and integer doubled-index semantics and never asserts equivalence of the old 2E and new general-E root predicates.

Resource bounds apply before recursive serialization, and resource failures have their own exception type. The test suite's semantic cases verify the expected mismatch exception rather than counting arbitrary failures as rejected mutations. I independently ran it with `-E -B`: the pinned producer matched, all 92 semantic mutations were rejected, and the separate resource-abort case passed. The mutations cover every new chart and fixed-binding row, retained inverse/square rows, beta factors, wrong target metadata, caller arguments, extra content and changed parent bytes.

The API correctly restricts itself to the four changed modules. The outer checker must still check the complete module set, unchanged scalar/anchor/pole/batch modules, full parent/source pins, honest general_E_mixed header, full flattening and construction map, and zero old root-chart locators. A shared-square composition must undo and validate its own exact delta before calling this checker. It cannot merely attach the name of the shared field or substitute an unreviewed parent hash.

The underlying new arithmetic is covered by the separate half-generator proof review; this finite checker does not establish that theorem. No full source generation or polynomial replay was run locally.
