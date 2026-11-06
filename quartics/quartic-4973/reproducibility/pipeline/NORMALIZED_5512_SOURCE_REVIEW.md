# Independent emitted-source binding: normalized Lucas, 5512

Date: 2026-11-06. Verdict: PASS for the arithmetic/source binding described here. No merged conic-pole source, sub-5000 claim or public release is accepted by this receipt.

Artifact: `work/quartic-sub5000-20261106/normalized-lucas-result`, run42237431520, artifact13511208124, commit `d3a198d61c8d6bda0d0f61b9ab4f5fb98478b04b`. ZIP SHA-256 `dc1c65c1c6cfe9740939a3a4d325e045e2fe62e70c2e951c884beb1019edb494`. Packet manifest `47c72e39f589523d92041c6f5af26935b9efb126d0daeb3513b142c985876892`.

The source ID is `joint-chart-normalized-lucas-conic-anchor4-k40-q12-a25-h19-s32-306c44519001`. Uncompressed source SHA-256: `306c445190018c850c5610fab4172ddc8df00193eeb043732172e1ae5a2c7d08`; compressed named-source SHA-256: `be7a7508e75a67d7570c6f974caca7af7f30004bd0a34c2dc4ac3bd17d75a2bb`. There are5067 total source variables and4608 source rows.

I checked all manifest file hashes/sizes and all run/artifact metadata, outer step results and log hashes. The first emitted source, deterministic repeat and adapter copy agree for every file listed in the source audit. Auditor dependency hashes, construction map and layout match the adapter receipt. This is actual-file inspection, not an inference from the manifest.

The root, beta-only comparator, all three conic batches, scalar-height module, old parity module, four-witness anchor and shared constants are byte-identical to the accepted local-Lucas source. Hence root proxy removal, integer root points, all rational height targets,37 contact positions,13/8/16 partition, scalar order32 and anchor25 remain unchanged. No pole-parameter reuse is present.

For the two changed comparator types I independently reconstructed the five normalized coupling equations from the actual variable-role metadata and compared their exact component polynomials. They are precisely

```
P*B_s=p_s,
(U+V)*p_t=P*B_t,
K*p_t=(1-2P)*B_t,
V*p_z=(1-2P)*B_z,
E=U^2-K*V-P^2.
```

I also ran the previously read, frozen independent comparison specification on all three actual comparator modules under a short deadline. It verifies all B_i*Lambda=G_i equations, actual G polynomials, common logarithm, beta quotient, joint charts, all coordinate/row coverage, field bindings and calls. The exact E output is passed at the order40 Lucas position; the source metadata correctly identifies E=F(C_s,C_t,C_z)/C_s^2 and does not assert global nonvanishing of p_s,p_z. There is no E=0 condition or added p_s/p_z inverse.

The exact field lists remain13/6/10 with377 fields and145 point/difference pairs. Arity58/28/47 and ignored legacy theta/error slots are retained. All37 private conic triples are disjoint, their coefficient inputs precede the child allocation, and comparison equations do not capture child coordinates. The six root affine charts are the only such locators; no old comparison inverse or paired-norm locator remains.

The arithmetic proof is `NORMALIZED_LUCAS.md` (`e76a6361be9678369abb7d42e98255bce214dab4dd7215ff6584b029169cb811`), independently reviewed in `NORMALIZED_LUCAS_REVIEW.md` (`6a9da3f66aec7e5d796fb77569100dd8ecc1791cd533871942e89c490cf9f7c9`). Its typed addition is `af365079cce1bd502dc2d683fc1f76fa2a2ca85c396c22be888dbd9fb3237cb0`. The emitted equations satisfy those premises: global G nonvanishing supplies Lambda,B_i,p_H,p_t nonzero; every consumed primary formal test supplies local nonzero p_i and integral C_i. Soundness multiplies by integral C_s^2 to recover the old Delta congruence. The newly permitted global two-torsion primary branches have a regular joint graph and are excluded at consumed primes by the positive-f tests.

Completeness fixes s and all root data before the prime-pattern step, excludes primes dividing s by increasing its fixed cutoff, and then chooses common J and private points. C_s is a unit at each assigned prime. Normalized E therefore meets the old order, and all its rational coefficients are fixed before private conic choices. No new height input, prime-pattern theorem or global point-sharing condition is used. All inherited H19, rational-contact, integer-carrier, formal-logarithm, Lucas, norm/pole and anchor qualifications remain. Finite verification does not prove those arithmetic inputs.

The source audit SHA-256 is `386b3cb8a9b33ebeb8f7de0c3793d0e291da3f5192074257263450d1484fcc2a`, construction map `b81a122bb0793c35dc53c333f3ae92914e024669f53f2fc03847bc7c93dd2ca8`, and adapter entry `6bab62478d9cb5d200ce21e3190235e24794baf0ed1e4dc972bd97810a9f1abc`. For subsequent byte-preserving combinations the two comparator hashes are:

- q_compare4: `924daadfdb5fb9f13b9e06fc7e457f224115d2e34801c070810d3ab5eef310c4`.
- q_compare_lucas: `a9157980855175cc0072f63c193c43f31c1350d850fdaeb3569d75e738229feb`.

The recorded208 distinct source mutations and deadline-abort regression pass. All six algebraic-stage verifications pass against the same source. Final verification SHA-256 is `387d0558c28e8fa5f02e8884480577728c295d8e5260536d30d71075972a6ac2`; certificate `0d0771b2d28c27dcd8c5c10ad239350b7ca954de0e435aaa6d1b4e9a3a38197e`; expanded polynomial `fc6a9c0cd31a6658cc1c863deaa2b41f0214034ddb9eba94fc759723fc0a2aa6`; named-source checker `fa6dac3ad718d1bd47ddc0a71bb68fb70c0641d6f61fd1373450b3b6800ec764`.

The endpoint has5512 total variables,5511 witnesses,5054 rows,78540 monomials, degree4 and all weights1. Its maximum absolute coefficient is685783949153203534233600<2^80. The398 operations are6 root-chart,2 field-ordinate,38 parity-conic,230 linear,120 elimination and2 shear events.

The bounded inspector is `inspect_normalized_and_local_pole.py`, SHA-256 `3f7ef928731a9fefc48b4b1f7e85d61a0d23731f34382c948bc9d8824a72a352`; detailed receipt `NORMALIZED_5512_RECEIPT.json`, SHA-256 `8e3951f83b8f03a89b5a564935ac241c5a3aa5cf55941da0ba3d51bf4f96de67`. It passed. No full source generation or heavy certificate replay was run locally. No source-to-proof blocker remains within this review's scope.
