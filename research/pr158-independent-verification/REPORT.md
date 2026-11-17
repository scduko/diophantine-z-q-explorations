# Independent verification of the PR #158 data chain

**Subject.** [elliotglazer/diophantine-z-q#158](https://github.com/elliotglazer/diophantine-z-q/pull/158),
*Candidate: explicit quartic with 229 variables and 74,007 canonical bytes*, at head
`65ae9cdeba8b9d218bebfc392cd4184b4567f6fd`, with stated base
`54a4e576f1c8c577f33b0b97a2cedb5ca96af642` (published Version 20). This branch is based on
main `a6446885418134a4ce6a867fc26a0c839e2bfb88`.

**Purpose.** Address the open finite-algebra scope of the second review round:
- finding `44115113273-1-fable-F2-graft-certificate-absent`, the binding of the source tables
  and coordinate maps to the final quadratic, polynomial and literal artifacts;
- the unreviewed items "identification of the 207 source rows with the three-detector
  system", "`thm:compact-coefficients`" and "checkers inspected but not run";
- Fable's note N2 on what the graft checker pins.

This is a verification report, not a review decision. It does not resolve any finding on
the reviewers' behalf.

**Date and environment.** 17 November 2026. CPython 3.13.18 on Linux. The new scripts use
only the Python standard library. The PR's `check_independent.py` was run with SymPy
1.14.0.

## How to reproduce

```sh
sh research/pr158-independent-verification/run_all.sh /path/to/new/work-dir
```

`fetch_inputs.sh` exports every input by `git fetch` at pinned commits:
- the PR head and its base, from `elliotglazer/diophantine-z-q`;
- `7501669160c1662a742ddd54baed364a47c82ddc`, from `JoseBrox/diophantine-z-q_improvements`.

Nothing fetched is executed. The three scripts then run with `python3 -I -B`, which takes
about 15 seconds in total.

## What was checked, and how

All checks are exact comparisons, using integer or rational arithmetic, written for this
report. **No code from the PR, from Brox's repository or from upstream is imported or
reused.**

### `verify_pr158.py` (107 checks, PASS)

1. **Provenance.**
   - `source/quadratic195.json` and `source/transformation195.json` are byte-identical to the
     published Version 19 files under
     `research/version19/construction/inputs/jose/computation/quartic/affine_laurent195_v45/`.
     The table's SHA-256 is `304f9484…` (Git blob `5d6c4a4b…`).
   - `source/quadratic229-v62.json`, `graft.json` and `contact-change.json` are
     byte-identical to Brox's pinned `computation/quartic/explicit229_v62/` files. The
     229-coordinate table's SHA-256 `f0e6fc3f…` also equals the pin in `transformation.json`.
   - The copied notation document and measuring script equal upstream's
     `docs/explicit-record/`.
2. **Graft structure, as stated in `paper.tex` §1.**
   - The second detector's local coordinates are exactly {7..10} ∪ {86..99} ∪ {134..149},
     34 in all.
   - They are copied in increasing order to x196..x229. The new argument is x200, the copied
     guard coordinates are x204 and x205, and every copied name has its detector index
     replaced by 2.
   - Outside the 31 detector-1 rows, only row 175 (the aggregate) uses a local coordinate,
     and that coordinate is x86.
   - Rows 1–174 equal the Version 19 table except rows 22, 24, 25, 34, 36 and 37.
   - Rows 176–206 are the coordinate-mapped copies of the (new) detector-1 rows.
   - Residual names are unique.
3. **Contact circuit (§3).** These checks cover all three detectors.
   - The ten contacts are distinct, with diameter 25/11, and the midpoint 3/22 is not one of
     them.
   - The paired constants and the five values L·e_j agree with the paper.
   - The identity P₅((22t−3)²) = 22¹⁰ ∏(t−θ)(t−c+θ) holds.
   - Each of the twelve contact rows (22–25, 34–37, 176–179), after substituting the
     paper's table of physical values, is a nonzero multiple of the corresponding physical
     equation. The multiple is ±q² or ±L·q².
   - Each contact row uses **only** the coordinates in that table; any other coordinate is
     rejected. This pins the contact-coordinate occurrences raised in note N2.
   - The guards x77x78 = 1, x90x91 = 1 and x204x205 = 1 each occur exactly once, in rows 26,
     38 and 180.
4. **Aggregate rows (§2).** Here A₀ + A₁√2 is computed independently in ℚ(√2) from
   `eq:components`.
   - The Version 19 aggregate row is 2q(x2−x86) + 14q² + A₀.
   - The new row 175 is 2q(x2−x86) + 26q² + A₀ (`eq:trace`); only its q² coefficient
     changes.
   - Row 207 is 2q(x2−2x86+x200) − 8q² + A₁ (`eq:shift`).
5. **Restoring the assertion that `check_graft.py` dropped.** The diff against Brox's
   original checker shows one assertion removed: the symbolic sum of squares equals the
   490 KB polynomial family. Expanding the 229-coordinate table symbolically in C gives
   3,322 parameter terms, **identical** to Brox's pinned `polynomial.json`.
6. **N = 15 specialisation and diagonal map (`prop:compact-map`, `thm:compact-coefficients`).**
   - C = 149¹⁵, and the input exponent a₁ = 0.
   - Both exponent tables printed in `paper.tex` equal `transformation.json` (127 nonzero
     coordinate exponents, 81 nonzero row exponents).
   - All 207 rows of 149^{b_j}·Q_j(149^{a}y) are integral, primitive and quadratic, and
     equal `quadratic.json`.
   - Before rescaling, the N = 15 quartic has largest coefficient exactly 149³², as stated
     in `thm:source`.
7. **Expansion and text.**
   - Σ R_j² equals `polynomial.json` coefficient by coefficient.
   - It has 3,312 monomials, degree 4 and content 1; all 229 variables occur; the x1⁴
     coefficient is 1.
   - The largest coefficient is exactly 149³⁰ (217 bits). The monomial support is unchanged
     by the rescaling.
   - A renderer written from the notation specification reproduces `quartic229-N15.txt`
     byte for byte: 74,007 bytes, with the stated SHA-256.

### `mutate.py` (negative controls, all rejected)

Each corruption is applied to a fresh copy of the package and must make the verifier fail:
1. one coefficient of `quadratic.json`;
2. one coefficient of `polynomial.json`;
3. one exponent in `transformation.json`;
4. one entry of the printed row-exponent table;
5. one digit of the literal text;
6. one source-table coefficient.

All six were rejected. The sixth is caught by the hash pins.

### `check_section5.py` (25 checks, PASS)

This recomputes the numerical steps of §5 (effective soundness at N = 15) and the
exceptional-set claim of §4. It uses exact integers and fractions, with correctly rounded
80-digit logarithms.

- **Exceptional set.** Γ \ S = {79, 89, 647, 3593} is exactly the set of primes outside S
  needed by the contact denominators, the pairwise contact differences and c/2 − θ.
- **Constants.**
  - J* = 30366775457346956958330 < 2⁷⁵, and c₀C₀ < 2¹⁴⁹.
  - 𝒞 = c₀C₀J*²E(J*) < 2³⁰⁰.
  - The product of (1 + 1/p) over primes p ≤ 1000 outside Γ is below 21/10, and
    p·log p > 6006 for p > 1000.
- **Remaining inequalities.** All other stated inequalities hold, including:
  - 121·√(21/10)·14^{1/3+1/36036} < 500;
  - L₁₅ = 66;
  - (23/22)·log(256036·2³⁰⁴) < 240;
  - |Δ| ≤ 14B⁴ (proved for all B ≥ 1);
  - the scalar constant is below 2²³⁷.
- **The decisive comparison at s = 66 log 149** is 220.1370 > 219.7689, so the true margin
  is **0.368**. The paper's stated rational bounds (219.963 and 219.8194) are valid and
  leave a margin of 0.144.

### The PR's own checkers

All were run, which round 2 had not done; all PASS:
- `build.py` reproduces `quadratic.json`, `polynomial.json` and the literal text byte for
  byte;
- `check_graft.py`, `check_arithmetic.py`, `check.py`, the upstream measuring script and
  `check_independent.py` all pass;
- the arithmetic replay equals the committed `arithmetic_certificate.json`;
- the graft replay differs from Brox's original certificate only in its list of output file
  hashes, which is expected.

## What was not checked

- **The arithmetic theorem itself.** That covers N = 15 soundness and completeness
  (`thm:source`, §§4–7), `lem:cutoff-free`, the witness construction in §7, the supplier's
  corollary behind the constants 40 and 2285/2425, the height-input theorem and its
  constants c₀ and C₀, and the prime-pattern, prepared-pole and Lucas inputs. For §5, only
  the arithmetic of the displayed inequalities was recomputed, taking their inputs from the
  paper. The logical derivation of each inequality was not reviewed.
- **The meaning of the inherited rows.** The 168 unchanged rows and the recovery formulas
  `eq:recovery` take their meaning from the Version 19 construction. Item 4 shows only that
  the published Version 19 aggregate row has the stated form in the stated coordinates.
- **Brox's original scripts were not run;** the sandbox's permission policy blocked it.
  Their key assertion was instead reproduced from his data (item 5).
- **Not a model review.** This is not a Protocol B review, and no finding is closed or
  waived by it.

## Minor observations

- `paper.tex` refers to `computation/quartic/explicit229_compact_v68/` (end of §8). That
  directory does not exist at the pinned Brox commit `7501669…`. This is consistent with
  Fable's round-2 note N1 on stale paths.
- `check_graft.py` itself still does not pin the SHA-256 of `source/quadratic229-v62.json`,
  but `build.py` and `check.py` do, through `transformation.json`.

## AI involvement

These scripts and this report were written and run by Claude Code (Anthropic), working in
an agent session directed by Scott Duke Kominers. The human directed the work but did not
independently re-derive the results.
