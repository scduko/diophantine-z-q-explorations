# Quartic conversion and sparsity search

The starting point is the explicit 15,671-witness residual system in the private November 5 manuscript package. Its compressed source file has SHA-256 `6e68a9d39573279e894e29d8913b5ade932aa6526d28a2d40bc713c1cca934a2`. The source has 15,107 integer polynomial equations, each of degree at most four. Its sum of squares has degree eight and 129,497 nonzero monomials.

The search objective is the number of nonzero monomials after collecting like terms in a single degree-four integer polynomial. The input coordinate stays fixed throughout. The search also records the witness count, coefficient maximum and actual text size. No claim of a global minimum follows from these searches.

## What is preserved

For every rational input q, the source system has a rational witness tuple if and only if the resulting quadratic residual system has a rational witness tuple. If the residuals are R_i and the weights w_i are positive integers, define

    P = sum_i w_i R_i^2.

Over the rationals, P = 0 is equivalent to R_i = 0 for every i. The polynomial has integer coefficients and degree at most four. Its actual expansion establishes that its degree is exactly four.

This is an algebraic conversion of the source system. The conversion checker does not prove that the source system defines the integers. That assertion still depends on the arithmetic argument in the manuscript and has the same review status as that argument.

## Allowed transformations

1. **Use an existing product equation.** If a retained source equation says xy = a z, with rational a, occurrences of xy may be replaced by a z. The certificate retains the equations used for these replacements. Denominators are cleared by nonzero constants. Both directions follow by substitution using the retained equations.
2. **Introduce a product variable.** Add u = xy and replace occurrences of xy by u. A solution extends uniquely by u = xy. Restriction of an extended solution recovers the original system. Repeating this operation makes every residual quadratic.
3. **Share a polynomial expression.** Add u = D and replace a residual R by R - aD + au. This is equivalent in the presence of u = D. The definitions and resulting residuals remain quadratic.
4. **Split an equation.** Replace A + B = 0 by A - u = 0 and B + u = 0, with u fresh. Extension by u = A and restriction give both directions.
5. **Eliminate a variable with a linear defining equation.** From v = D, with v absent from D, substitute D into every other occurrence of v and delete the defining equation. The checker rejects omitted occurrences and rejects elimination of the input coordinate. Substitutions are used only when the resulting residuals remain quadratic.
6. **Apply an invertible row operation.** Replace R_i by a R_i + b R_j, keeping R_j and requiring a nonzero. The common zero set is unchanged.
7. **Change a witness coordinate.** Substitute v + t, or v + t w with w different from v, for a witness v in every equation. These rational affine changes are invertible. The input coordinate is never changed. Occurrences are checked exhaustively.
8. **Rescale an equation by a nonzero rational.** Clearing denominators and removing integer content leave its zero set unchanged. The checker compares exact normalized polynomials, not numerical evaluations.
9. **Choose positive integer weights.** Every weighted square is nonnegative over Q. Thus their sum vanishes exactly when all residuals vanish. Negative and zero weights are rejected.
10. **Compact variable names.** Retain the input as variable 0 and rename the remaining variables bijectively. Coordinates absent from every equation need not be quantified. The final producer assigns smaller indices to variables occurring more often in the expanded polynomial, reducing the number of characters used for indices. The checker verifies the full permutation.

## Certificate and checker

`build_certificate.py` is an untrusted producer. It reconstructs the search history and emits explicit changed equations. `verify_certificate.py` imports neither the producer nor either optimizer. It uses only Python's standard library and exact integer and rational arithmetic.

The checker binds the starting file by its SHA-256, verifies retained product equations and fresh product definitions, checks each subsequent transformation, and compares the final system with the distributed residual file. It then expands all **ordered** pairs of terms in every weighted square. The producer uses triangular pairs with doubled cross terms. The two expansions must agree coefficient by coefficient with the distributed plain-text polynomial.

The checked statement is quantified over every rational input, rather than being a test on sampled rational values. The code verifies finite algebraic identities and the side conditions of the transformations described above. This is not a Lean kernel proof of the checker or of the source arithmetic theorem.

`test_verifier.py` deliberately corrupts certificates, substitutions, the source file and the expanded polynomial. These rejection tests supplement the positive check.

The expanded format has a comment line followed by one monomial per line. The first integer is the coefficient; subsequent integers are variable indices, repeated to indicate powers. Thus `-6 0 2 2` denotes -6*x_0*x_2^2. A line containing only a coefficient denotes a constant. The rows are sorted lexicographically by their index tuples, and coefficients of identical monomials have already been combined.

## Resource policy

All substantive local calculations use the existing `run_bounded.py` wrapper, one process at a time, with below-normal priority and a 2 GiB memory ceiling. The search does not modify the manuscript, its versioned PDF, or the source polynomial package.
