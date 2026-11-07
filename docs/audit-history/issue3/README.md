# Issue 3: exact finite cases and hash formats

This note answers the reproducibility questions in [Issue 3](https://github.com/elliotglazer/diophantine-z-q/issues/3). The report concerns the original construction at `97cec7fdd757d9a8e4f468151a47a6d3610fb2f2` and the Version 4 quartic at `5cb2c1997dde6e358f3c2fe9bbdb4b8f4c23bac6`. We compared the relevant source and data bytes with those commits. They are unchanged; [source-comparison.json](source-comparison.json) records the comparison.

Historical disposition: the cases and serialization rules were implemented in the original checkers, but were missing from the prose. This is a documentation correction, not a new mathematical argument or a change to a polynomial. The manuscript and the frozen Lean target are unchanged.

## Integer compiler cases

The source is [verify-integer-compiler.js](../../../construction/verify-integer-compiler.js). All inputs and witnesses in this suite are **nonnegative integers**, not arbitrary rationals. Bounds below are inclusive unless stated otherwise.

| Counter | Exact cases | Count |
| --- | --- | ---: |
| `digitCases` | `n=0,...,14`, `k=0,...,18`; set `B=2^(n+1)` and check `floor((B+1)^n/B^k) mod B = binomial(n,k)`, with `binomial(n,k)=0` for `k>n` | 285 |
| `bitCases` | All ordered pairs `a,b=0,...,63`. Each pair checks Lucas subset parity, disjointness parity, and the decomposition with `z=a AND b`, `x=a-z`, `y=b-z` | 4,096 |
| `packedCases` | Six two-instruction programs, `c=1,2`, `q=0,...,3`; all register sequences of length `q+1` with entries in `0,...,2^c-1`, and all state sequences of that length with entries in `{0,1}` | 30,120 |
| `backendCases` | `x,y=0,...,6`; search witnesses `d,u,v=0,...,7` for the polynomial below | 49 |

The three bit assertions, counted together as one case, are:

```text
binomial(b,a) odd       iff (a AND b) = a
binomial(a+b,a) odd     iff (a AND b) = 0
z AND x = z AND y = x AND y = 0
```

The six programs have instruction 0 operating on register 0 and instruction 1 equal to `halt`. Two programs increment and jump to `next=0` or `1`. Four decrement-if-positive programs use every ordered pair of `nonzero,zero` destinations in `{0,1}^2`. A zero register stays zero on the zero branch. The direct history predicate requires initial state 0, final state 1, final register 0, no earlier halt, and the specified transition at every step. The packed predicate is compared with this direct predicate on **every** sequence, including invalid histories. Register sequences are enumerated by increasing base-`2^c` code, least significant digit first; states by increasing binary code, least significant bit first. The count is

```text
6 * sum_{c=1,2} sum_{q=0,...,3} (2^c)^(q+1) * 2^(q+1) = 30120.
```

For the backend cases, the formula is `(x<y AND x congruent y mod 3) OR x=5`. With the builder's variable order `[x,y,d,u,v]`, its polynomial is

```text
((y-x-1-d)^2 + (x+3*u-y-3*v)^2) * (x-5).
```

The search visits `d`, then `u`, then `v` in increasing order and stops at the first zero. Its outcome is compared with the displayed formula for each pair `x,y`. This is a bounded existential test of that particular formula.

There are also eleven uncounted smoke tests of the clear-register machine on inputs `0,...,10`, followed by structural checks on its compiled circuit. These do not constitute an exhaustive test of the alpha or power representations.

## Division-polynomial evaluation points

The source is [verify-division-polynomials.js](../../../construction/verify-division-polynomials.js), using [rational-field-arithmetic.js](../../../construction/rational-field-arithmetic.js). Work over `Q(s)` with `s^2=2`, on

```text
E: y^2 = x^3 + (-11243 + 7950*s)*x,
P = ((1641-1160*s)/8, (-123720+87483*s)/32).
```

The complete Cartesian product is

```text
n in [0,1,2,3,4,5,6,7,8,-1,-4]
k in [-1,0,1,2].
```

For each pair, the two five-coordinate point blocks encode `[k]P` and `[n*k]P`, obtained by affine double-and-add. The order is `[infinity,x_0,x_1,y_0,y_1]`, with `x=x_0+x_1*s`, `y=y_0+y_1*s`. Infinity is `[1,0,0,0,0]`; an affine point has initial coordinate 0. Each rational entry is stored as a reduced numerator/positive-denominator pair.

For `n!=0` there is one inverse-norm witness. It is the reciprocal of the graph's denominator norm when `k!=0`, and 0 when `k=0`. For `n=0` there is no such witness. The suite checks:

- 44 correct assignments evaluate to zero;
- 44 assignments with 1 added to the **output** `x_0` coordinate evaluate to nonzero;
- 30 assignments with both output `y_0,y_1` negated evaluate to nonzero, for `n!=0` and `k!=0`.

The corrupted assignments retain the original inverse-norm witness. These are the entire point sets, not random samples or all points of a bounded height.

## Finite-expression cases and hashes

The source is [verify-finite-polynomial-expressions.js](../../../construction/verify-finite-polynomial-expressions.js). It compares expanded finite constructors with the direct builder at two fixtures:

```text
(cstar,ell,T) = (4,12,1), (8,144,0).
```

For each fixture, it checks template ids 9 through 12 in order: `multiply.scalar`, `multiply.guard`, `multiply`, `natural`. This gives eight root-hash comparisons and eight variable-count comparisons. All eight hashes appear in [construction-checks.json](construction-checks.json), under `verify-finite-polynomial-expressions.js`. The fixtures do not replace the prescribed large constants.

Four additional fresh copies of the symbolic library must be rejected:

1. Set `fixedConstants.P0` to `["literal","1"]`.
2. Set argument 1 of the `psi_component` node in template 9 to `999999`.
3. Set argument 0 of the `finite_guard_product` node in template 10 to `["literal","1"]`.
4. Set argument 0 of the `fixed_integer` node in template 11 to `["variable",0]`.

The hashes are **recursive expression hashes, not hashes of JSON files**. Let `H(s)` be lowercase hexadecimal SHA-256 of the UTF-8 bytes of `s`, with no BOM, newline, or terminating zero byte. For each node in topological order:

```text
const: H("const:" + args[0])
var:   H("var:"   + args[0])
add:   H("add:"   + child_hashes.join(":"))
mul:   H("mul:"   + child_hashes.join(":"))
call:  H("call:"  + args[0] + ":" + args[last] + ":"
                     + hashes_of_args_1_through_last_minus_1.join(":"))
```

Concatenation uses the stored decimal constant string or JavaScript's decimal string for an integer index. A call includes its template id, final shift argument, and ordered argument hashes. The reported value is the hash at `t.root`. Operand order is preserved; no commutative sorting or algebraic simplification is performed. Names, metadata, and unrelated nodes are not separately appended to the root hash.

## Version 4 `final.rows_sha256`

The serialization in [verify_certificate.py](../../../quartics/quartic-4973/verify_certificate.py) is

```python
json.dumps([encode(row) for row in rows],
           sort_keys=True, separators=(',', ':')).encode('ascii')
```

Here `encode(row)` is `[[coefficient, list(monomial)] for monomial, coefficient in row.items()]`. Specifically:

- `rows` is the complete terminal replay table, in row-id order, **before** removing empty rows or renumbering variables;
- all 4,879 rows are included, including 327 empty arrays;
- each coefficient is an exact signed integer JSON number, not a quoted string or floating-point value;
- a monomial is the nondecreasing list of its variable indices, with repetitions encoding powers; the constant monomial is `[]`;
- terms retain their insertion order in each row. `sort_keys=True` does not sort arrays;
- the encoding is compact ASCII JSON with no whitespace or final newline. Hash the encoded JSON, not its gzip container.

The result is

```text
758e6c9f9225109017d2d80ee663a266c92ccf51de91f308304a02147031c7ea
```

The saved `candidate-rows.json.gz` has the same row and term order. [replay_row_hash.py](replay_row_hash.py) reproduces the digest directly from that file and compares it with the final certificate record. It uses exact Python integers and does not import the certificate checker. It checks serialization only; the full certificate replay checks the algebra.

## Reproduction and disposition

From the repository root, with Python 3.11+ and Node.js 22+:

```sh
python -B scripts/check_construction.py --report build/issue3/construction-checks.json
python -B docs/audit-history/issue3/replay_row_hash.py
```

The November 7 replay passed all four original finite suites and regenerated the original polynomial byte for byte. [construction-checks.json](construction-checks.json) preserves the full output, including the expression hashes. The Version 4 certificate was also replayed without changing its files; [quartic-checks.json](quartic-checks.json) records that result.

The contributor's separate conditional Lean proof is welcome as a PR for review. It must retain its eight explicit hypotheses and remain separate from the unchanged frozen unconditional target. Inviting that PR neither accepts its statements nor verifies its hypotheses. Review and integration can proceed in the PR independently of this documentation issue.

Issue 3 supplies valuable independent reproduction of finite artifacts. Neither its report nor this follow-up establishes the main arithmetic theorem or a completed Lean formalization. Closing the issue records that the requested cases, serialization rules, and response to the PR offer have been supplied; further discrepancies can be reported here or in a new issue.
