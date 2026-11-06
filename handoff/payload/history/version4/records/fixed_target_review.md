# Half-generator fixed-target addendum

Date: 2026-11-06. PASS for the exact partial fixed-target substitution. This extends the mathematical scope of `HALF_GENERATOR_ROOT_REVIEW.md`, SHA-256 `418becf67de2e5a3957d8e4066e4a9d3a96d70e8d3b7ba2552401f0733d08702`. It does not accept an emitted source or a global coefficient bound.

The reviewed constants are `charts/sub5000/half-generator-review/FIXED_TARGET.json`, SHA-256 `03d5ffae826a5183d1c1470594c113bc62c285ca12a09702c26f1fb0e69c1409`. I independently recomputed 2P*=4R over Q(sqrt(2)), using the separate exact arithmetic fixture already reviewed with the half-generator proposal. Every listed x,y,q,F,c,s,t,inverse-q and s/q coefficient matches that calculation.

Let a=x(4R), q=y(4R)/a, F=1/a, c=a+DF, s=c/q and t=1/q^2. The proposed four primitive rational binding rows fix the two coefficients of a and q. They are reduced fractions with positive denominators. The retained equation aF=1 then fixes F uniquely, and the exact constants satisfy q^2=a-DF. Consequently retaining sq=a+DF and tq^2=1 gives precisely the same shared target quantities as the two explicit fixed-base doublings. The J-dependent quantities remain r=J/q and u=rs in the joint-chart convention. Neither a nor q is zero.

Thus the two fixed-base doubling circuits can be omitted if the new source binds these four values exactly and retains the stated reciprocal and shared-target equations. No arithmetic assumption changes. Conjugated source slots must use conjugated values consistently, rather than reversing only one coefficient in the graph equations.

I checked the four squared binding rows independently. Their total constant contribution is exactly `123824835334257812600380`. The largest coefficient in their isolated sum of squares is `395918230471021175779344`, which is less than 2^80 and has 79 bits. This includes the summed constant term, not only each row's coefficients. It does not include any other source residual. A later elimination, rescaling or combination may change the global coefficient total, so the full source and final expanded polynomial must still be checked.

Required source evidence includes the exact four binding rows, consistent target role and conjugation, retained F/s/t/r/u equations, complete absence of outside uses of removed constant-base gates, and the unchanged variable targets 4A,4S,4T,4Z. The stronger root-chart appendix and all doubled-index arithmetic changes must be implemented together. Old source IDs, counts or coefficient maxima cannot be reused for this new source.
