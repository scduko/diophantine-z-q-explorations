# Independent anchor norm review

PASS for the mathematical source replacement in `parity/ANCHOR_NORM.md`, SHA-256 `19cb89a5acf699cdc021078d93b8b20183de61d30c915e2b20759e53daac8177`, read on November 6, 2026. This is a semantic equivalence using the same inherited exact T characterization. It is not an unconditional polynomial-ideal equivalence or a rational transfer map between the seven-witness tuples.

Let R be the rationals integral at 2 and 3, and use the released theorem T(t) iff t is in R. For a,b in Q, the two summands of a^2-2b^2 have distinct valuations at 2 whenever both are nonzero, since their valuations have opposite parity. Thus its valuation is the minimum of 2v2(a) and 1+2v2(b). Nonnegativity forces v2(a)>=0 and v2(b)>=0, including the integer-rounding step for the latter. Conversely those inequalities imply the norm is integral. Zero coordinates obey the same conclusion directly.

At 3, if the two coefficient valuations differ, the smaller squared valuation is unique. If they agree, division by that common power leaves units whose squares are both 1 modulo 3. Their norm is 1-2=-1 modulo 3 and cannot cancel. Thus v3(a^2-2b^2)=2min(v3(a),v3(b)), with the usual convention for zero. The zero norm itself forces a=b=0 because 2 is not a rational square.

Consequently T(a^2-2b^2) is equivalent to T(a) and T(b). With the unchanged nonzero shared constant C, setting C2=C^2 and C2*t=f0^2-2f1^2 makes t exactly the norm of (f0/C,f1/C). This proves both existential directions of the proposed replacement for every rational pair f0,f1, without using a curve equation. The anchor's permitted subgroup of point indices is therefore exactly unchanged, not merely enlarged or made sufficient.

The required nonzero premise is supplied by the retained repeated-squaring chain starting at 3. A checker must bind the same terminal C as the old anchor. C2 is constrained by its own equation; it is not a freely chosen replacement for the old denominator.

The algebraic coordinate maps are a_i=f_i/C and t=a0^2-2a1^2. Existence of appropriate T witnesses in either direction uses the exact T theorem, which is already present in the public anchor source-application ledger with SHA-256 `2f81ceea6b525913b1790c2695da9fb3cc3c9c8b63bfbe7e16bc26d0a227e5ef`. No new external theorem is required. A finite equality checker cannot by itself certify this witness transfer.

The proposed allocation is consistent: C2,t and seven T witnesses give nine locals, versus two scaled inputs and fourteen T witnesses giving sixteen. The two new norm/scaling equations and two T equations give four quadratic rows, versus six. All new coefficients have magnitude at most two; the retained T equations have maximum 24. These are source allocation facts, not a measured final-variable saving. Source incidence, the shared terminal constant and the actual new module still need independent binding and replay.

This equivalence is compatible with the reviewed H19/H18 anchors and the three comparator modes because it leaves the anchor relation on f(S) exactly unchanged. It does not alter a cutoff, height constant, scalar order or formal-logarithm hypothesis. No local computation was run for this review.
