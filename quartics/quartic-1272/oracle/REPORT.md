# Independent arithmetic oracle

For this release, run the oracle through `python reproduce.py --out ../quartic1272-replay` from the package root. The standalone command described below writes a result file and is intended for that isolated copy.

The reconstructed raw program agrees with the independent source inventory on every tested value. These checks concern the arithmetic reconstruction. They do not reproduce the author's missing program or prove the manuscript's reported coordinate and coefficient counts.

`check_oracle.py` reads the source-review AST and the two generated IR files. It imports no builder or compiler code. It interprets the source formulas over exact finite fields and, for selected small dependency closures, over `fractions.Fraction`. The IR evaluator separately interprets sparse polynomial assignments and quotient equations.

## Results

Six generic samples use the primes 1,000,003, 1,000,037, and 1,000,099, with two seeds per prime. The script checks primality and that 2 is a quadratic nonresidue. Thus its pairs represent the field extension of degree two. Every encountered denominator is nonzero; no sample needed rejection.

Each sample checks:

- All 1,214 actual arithmetic gate residuals evaluate to zero after executing the program.
- All 47 actual structural residuals equal their source expressions. The residuals need not vanish at these generic inputs.
- 309 scalar intermediate values agree, including point doubling and subtraction, reciprocal coordinates, both logarithm orders, logarithm ratios, all 16 tests, all nine detector products, scalar norm values, pole data, and the anchor expression.
- All nine detector products agree with a separate direct evaluation of the displayed factors using the original normalization. The source interpreter also evaluates the grouped products directly as factors, whereas the IR uses shared symmetric coefficients and Horner evaluation.

The logarithm comparison uses the source's explicit sum of powers. The generated IR uses its Paterson–Stockmeyer evaluation. The scalar comparison includes all six normalized leaves, both intermediate branches, the norm root, correction factor through the final value, the preparation quotient, and both pole residuals.

Twelve selected intermediate values also agree over exact rational arithmetic. These include a doubled point, a subtracted point, and both G3 and G12 logarithms. This check evaluates 168 coordinates; its largest compared numerator or denominator has 1,142 bits.

An independent sparse polynomial expansion proves the identity between the two actual IR anchor rows over a polynomial ring over the rationals, with S left symbolic. The translated row is 16 times the original row after the stated affine substitution. All three inverse identities hold, and every nonanchor residual is unchanged. The raw anchor uses the physical expression T, so the translated coefficient is −48T². The manuscript's −3A² form uses A = 4T.

## Interpretation and limits

Finite-field and exact rational samples can expose a wrong formula; their agreement is not a universal rational-identity proof. The generic halfpoints are not required to lie on the curve, and these samples do not establish existence of structural solutions, integrality, or any external arithmetic input.

The anchor expansion is a universal polynomial identity for the reconstructed rows. It does not identify those rows with an unavailable author artifact.

The LP aliases in the IR store the ratio before conjugation. The actual cross-test expressions apply the conjugation. The oracle maps this convention explicitly and checks those cross tests.

Small values of S are used only as algebraic test specializations. No coefficient-height conclusion comes from them, and the enormous fixed integer is never expanded. The oracle does not check the compiler's eliminations or the final coefficient table; those are separate reviews.

`results.json` records all input hashes, sample seeds, base values, counts, and outcomes. Run the check from any directory with:

```powershell
& 'python' 'oracle/check_oracle.py'
```
