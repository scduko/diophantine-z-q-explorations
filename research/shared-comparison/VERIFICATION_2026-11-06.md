# Shared-comparison follow-up verification

**6 November 2026; AI author self-review.** The reviewer supplied the original
CPO proof, so this is not independent mathematical review or human refereeing.
The original `CPO_PROOF.md` and `REVIEW_CPO_PROOF.md` remain historical records.
This note records the follow-up to proposal commit
`df5b0b2b5235ef113ca83dcf92579b57b3bb47d8`.

## Source application

The full text of Frei–Tinková, *Linear constellations in primes with arithmetic
restrictions*, arXiv:2408.17441v3 (5 November 2025), was read directly:

- [Theorem 1.4 and the local factors](https://arxiv.org/html/2408.17441v3);
- formulas (1.10), (1.15), and Corollary 1.6 in the same version.

The Artin-symbol theorem is unconditional. The separate primitive-root theorem
is not used. The application was checked as follows.

| Requirement | Application |
|---|---|
| Fixed Galois extensions of $\mathbb Q$ | The Gaussian ray class field $H_R$, fixed after choosing $L_0$; conjugation preserves its modulus. |
| Finite-complexity integral affine forms | The two active integer coordinates; denominators in slopes are absorbed by $V_0$; repeated forms are removed and distinct linear parts are pairwise independent. |
| Bounded system size and convex region | Fixed coefficients and a fixed positive-area box dilated by $X$, inside the common positivity cone. |
| Abelian compatibility | $H_R^{\mathrm{ab}}=\mathbb Q(i,\zeta_R)$; the fixed progression determines the allowed norm fibers. |
| Class normalization | Sum the sizes of all good compatible conjugacy classes, using $\eta$ in (1.10); do not multiply unconditional class densities. |
| Positive leading constant | Original admissibility and the uniform conditional bounds $g_\ell(t)$; the calculation following (5.4) in `CPO_PROOF_V2.md` relates this to (1.15). |
| Quantifier order | Fix targets and any optional cutoff, then $L_0$ and the ray field, then let $X$ tend to infinity. The error threshold may depend on $L_0$. |

These checks close the source-access item in the earlier review. They do not
constitute independent certification of CPO. The original review's phrase
"published theorem" is not a journal-publication claim supported by this check;
the source checked here is the specified arXiv version.

## Mathematical revisions

`CPO_PROOF_V2.md` spells out the conditional-density normalization and the
uniform Selberg weights, truncation bound, and remainder sums. It preserves
the theorem and order of choices. `SHARED_COMPLETENESS.md` supplies the bridge
from the common multiplier to the shared point, chart, approximation, and
field-test witnesses, retaining separate norm-batch witnesses.

The pinned manuscript was checked at `subsec:o8-pattern-proof`,
`subsec:o8-common-J-proof`, `eq:old41-private-crt`, `subsec:o8-root-proof`, and
the reciprocal comparison and compressed-primary-chart arguments. The earlier
Version 2 arithmetic inputs remain dependencies.

## Algebraic checks and reproducibility

The construction and generation algorithm are unchanged. The lift checker now
verifies that each selected product definition is a nonzero scalar multiple
of a retained equation, that reused definitions occur in the source, that
fresh definitions extend source assignments, and that the full selected
dependency graph is acyclic and does not eliminate $X$.

This distinction matters: source variable 52 represents three products, so
substitution using one selected definition need not annihilate the other two.
Those other equations remain constraints. Equality after substitution means
equality modulo the ideal of the selected triangular definitions; it does not
mean that all recognized product equations vanish identically.

The reproducibility command is:

```sh
sh research/shared-comparison/check.sh
```

The command passed on CPython 3.12.14 on Linux, with exact rational arithmetic
and the standard library: pinned hashes matched, and both generated directories
reproduced byte for byte. The verified output is 2,983 source witnesses,
2,819 source residuals, 1,167 fresh lift variables, 3,986 quadratic residuals,
4,151 total variables including $X$, and 19,910 quartic monomials. The maximum
absolute coefficient is 685783949153203534233601. The expanded polynomial hash
is `63defdb6a5578aeabe7779be7bb116e80a85b1de5fe6cfa20084c84db432e1cd`.
`SHA256SUMS` records the exact revised checker and documentation hashes.

The review also independently expanded the committed quadratic residuals by
ordered pairs of terms and obtained exactly the committed polynomial.
Two small checker fixtures were exercised: the equations
$v_1=2v_2v_3$, $v_1=v_4v_5$, $v_4v_5v_6=X$ passed, while the cyclic definitions
$v_1=v_2v_3$, $v_2=v_1v_4$ were rejected with `cyclic product definitions`.
All proposal files passed the repository handoff path and content scanner.
No optimized-pipeline replay, Version 2 certificate replay, Lean formalization,
or independent human referee review is claimed.
