"""Find quadratic-preserving elimination through certified affine units.

Run only on the remote/bounded worker. This producer is deliberately separate
from check_localized.py, which checks its polynomial identities independently.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import json
import math
from pathlib import Path
import sys
import time


def enc(p):
    return [[c, list(m)] for m, c in sorted(p.items())]


def dec(p):
    return {tuple(m): c for c, m in p}


def add(a, b, scale=1):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c * scale
        if not out[m]:
            del out[m]
    return out


def add_to(out, b, scale=1):
    for m, c in b.items():
        out[m] = out.get(m, 0) + c * scale
        if not out[m]:
            del out[m]


def mul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            k = tuple(sorted(m + n))
            out[k] = out.get(k, 0) + c * d
    return {m: c for m, c in out.items() if c}


def power(a, n):
    out = {(): 1}
    for _ in range(n):
        out = mul(out, a)
    return out


def primitive(a):
    if not a:
        return {}
    den = math.lcm(*(Fraction(c).denominator for c in a.values()))
    out = {m: int(c * den) for m, c in a.items()}
    common = math.gcd(*out.values())
    if out[min(out)] < 0:
        common = -common
    return {m: c // common for m, c in sorted(out.items())}


def signature(a):
    return tuple(primitive(a).items())


def variables(a):
    return {v for m in a for v in m}


def subtract_mon(a, b):
    out = list(a)
    for v in b:
        if v not in out:
            return None
        out.remove(v)
    return tuple(out)


def divide_exact(a, b):
    """Multivariate division by one polynomial, using graded lex order."""
    if not b:
        raise ValueError("zero divisor")
    order = lambda m: (len(m), m)
    lead = max(b, key=order)
    remainder = dict(a)
    quotient = {}
    while remainder:
        term = max(remainder, key=order)
        difference = subtract_mon(term, lead)
        if difference is None:
            return None
        coefficient = Fraction(remainder[term], b[lead])
        quotient[difference] = quotient.get(difference, 0) + coefficient
        remainder = add(remainder, mul({difference: coefficient}, b), -1)
    return {m: c for m, c in quotient.items() if c}


def split(row, v):
    """Write row = A*v - N, or reject a square in v."""
    a, n = {}, {}
    for m, c in row.items():
        if m.count(v) > 1:
            return None
        if v in m:
            a[tuple(w for w in m if w != v)] = c
        else:
            n[m] = -c
    return a, n


def cleared_substitute(row, v, a, n):
    k = max((m.count(v) for m in row), default=0)
    out = {}
    for m, c in row.items():
        q = m.count(v)
        term = {tuple(w for w in m if w != v): c}
        term = mul(mul(term, power(n, q)), power(a, k - q))
        out = add(out, term)
    return out


def discover_units(rows):
    """Explicit units and binomial propagation; no inferred arithmetic facts."""
    units = defaultdict(list)
    for i, row in enumerate(rows):
        if row.get((), 0):
            for witness in variables(row):
                if all(witness in m for m in row if m):
                    factor = {}
                    for m, c in row.items():
                        if not m:
                            continue
                        remaining = list(m)
                        remaining.remove(witness)
                        factor[tuple(remaining)] = c
                    if factor and max(map(len, factor)) == 1:
                        factor = primitive(factor)
                        units[signature(factor)].append(
                            (factor, {"kind": "inverse", "row": i, "witness": witness}))
        if len(row) == 3 and () in row:
            singles = [m[0] for m in row if len(m) == 1]
            squares = [m[0] for m in row if len(m) == 2 and m[0] == m[1]]
            if len(singles) == len(squares) == 1:
                e, theta = singles[0], squares[0]
                expected = {(e,): 1, (theta, theta): -1, (): 2}
                if e != theta and signature(row) == signature(expected):
                    factor = {(e,): 1}
                    units[signature(factor)].append(
                        (factor, {"kind": "root_error", "row": i, "error": e, "root": theta}))
    # If one side of a binomial relation is a product of known units,
    # every variable factor on the other side is also nonzero. Proofs point
    # only to previously known units, so the resulting graph is acyclic.
    known = {}
    for sig, choices in units.items():
        factor = choices[0][0]
        if len(factor) == 1:
            monomial = next(iter(factor))
            if len(monomial) == 1:
                known[monomial[0]] = choices[0][1]
    changed = True
    while changed:
        changed = False
        for i, row in enumerate(rows):
            # A monomial known nonzero equals v times an affine polynomial.
            # There is no sign/positivity assumption. All coefficients here
            # are integral primitive row coefficients.
            if 2 < len(row) <= 6:
                for right, coefficient in row.items():
                    if not set(right) <= known.keys():
                        continue
                    left_part = {m: c for m, c in row.items() if m != right}
                    common = set.intersection(*(set(m) for m in left_part))
                    for v in sorted(common - known.keys()):
                        cofactor = {subtract_mon(m, (v,)): c for m, c in left_part.items()}
                        if not cofactor or max(map(len, cofactor)) > 1:
                            continue
                        proof = {"kind": "product_unit", "row": i, "factor": [[1, [v]]],
                                 "cofactor": enc(cofactor), "monomial": list(right),
                                 "coefficient": -coefficient,
                                 "known": [[w, known[w]] for w in sorted(set(right))]}
                        factor = {(v,): 1}
                        units[signature(factor)].append((factor, proof))
                        known[v] = proof
                        changed = True
            if len(row) != 2:
                continue
            monomials = list(row)
            for left, right in (monomials, monomials[::-1]):
                if not set(right) <= known.keys():
                    continue
                for v in sorted(set(left) - set(right) - known.keys()):
                    proof = {"kind": "binomial", "row": i, "variable": v,
                             "known": [[w, known[w]] for w in sorted(set(right))]}
                    factor = {(v,): 1}
                    units[signature(factor)].append((factor, proof))
                    known[v] = proof
                    changed = True
    return units


def proof_variables(proof, rowvars, cache):
    key = id(proof)
    if key not in cache:
        result = set(rowvars[proof["row"]])
        for _, child in proof.get("known", []):
            result.update(proof_variables(child, rowvars, cache))
        cache[key] = result
    return cache[key]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--research-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--max-steps", type=int, default=500)
    parser.add_argument("--max-terms", type=int, default=128)
    args = parser.parse_args()
    start = time.monotonic()
    rows = [dec(r) for r in json.loads(gzip.decompress((args.parent / "candidate-rows.json.gz").read_bytes()))]
    rowvars = [variables(r) for r in rows]
    incidence = defaultdict(set)
    polynomial = {}
    for i, row in enumerate(rows):
        for v in rowvars[i]:
            incidence[v].add(i)
        add_to(polynomial, mul(row, row))
    initial_variables = len(incidence)
    assert max(map(abs, polynomial.values())) < 2**80
    records = []
    failures = Counter()
    history = []
    for step in range(args.max_steps if args.output else 1):
        units = discover_units(rows)
        support = {}
        for choices in units.values():
            for _, proof in choices:
                proof_variables(proof, rowvars, support)
        candidates = []
        eligible_pivots = 0
        for i, row in enumerate(rows):
            for v in sorted(rowvars[i] - {0}):
                parts = split(row, v)
                if parts is None:
                    continue
                a, n = parts
                if not a or max(map(len, a)) != 1:
                    continue
                proofs = [(f, pr) for f, pr in units.get(signature(a), [])
                          if v not in support[id(pr)]]
                if not proofs:
                    continue
                eligible_pivots += 1
                _, proof = proofs[0]
                cancellation_units = [(f, pr) for group in units.values() for f, pr in group
                                      if v not in support[id(pr)]]
                affected = sorted(incidence[v] - {i})
                changes = {i: {}}
                cancellations = []
                for j in affected:
                    result = cleared_substitute(rows[j], v, a, n)
                    factors = []
                    # A itself is usually the most useful cancellation factor.
                    options = [(a, proof)] + cancellation_units
                    for factor, factor_proof in options:
                        if not result:
                            break
                        if not variables(factor) <= variables(result):
                            continue
                        while result:
                            quotient = divide_exact(result, factor)
                            if quotient is None:
                                break
                            result = quotient
                            factors.append({"factor": enc(factor), "proof": factor_proof})
                    result = primitive(result)
                    if any(len(m) > 2 for m in result):
                        failures["degree"] += 1
                        break
                    if len(result) > args.max_terms:
                        failures["terms"] += 1
                        break
                    changes[j] = result
                    cancellations.append({"row": j, "factors": factors})
                else:
                    delta = {}
                    for j, new in changes.items():
                        delta = add(delta, mul(rows[j], rows[j]), -1)
                        delta = add(delta, mul(new, new))
                    if any(abs(polynomial.get(m, 0) + c) >= 2**80 for m, c in delta.items()):
                        failures["coefficient"] += 1
                        continue
                    term_change = sum(bool(polynomial.get(m, 0) + c) - (m in polynomial)
                                      for m, c in delta.items())
                    record = {"kind": "localized_eliminate", "data": {
                        "row": i, "variable": v, "denominator": enc(a), "numerator": enc(n),
                        "nonzero": proof, "affected": affected, "cancellations": cancellations},
                        "patches": [[j, enc(new)] for j, new in sorted(changes.items())]}
                    candidates.append(((term_change, len(affected), v, i), record, changes, delta))
        history.append({"step": step, "affine_units": len(units), "eligible_pivots": eligible_pivots,
                        "candidates": len(candidates), "variables": sum(bool(s) for s in incidence.values())})
        print(json.dumps(history[-1]), flush=True)
        if not candidates:
            break
        candidates.sort(key=lambda item: item[0])
        if not args.output:
            break
        score, record, changes, delta = candidates[0]
        records.append(record)
        add_to(polynomial, delta)
        for j, new in changes.items():
            for v in rowvars[j]:
                incidence[v].remove(j)
            rows[j] = new
            rowvars[j] = variables(new)
            for v in rowvars[j]:
                incidence[v].add(j)
    report = {"parent": str(args.parent), "initial_variables": initial_variables,
              "final_variables": sum(bool(s) for s in incidence.values()),
              "accepted": len(records), "history": history, "failures": dict(failures),
              "seconds": round(time.monotonic() - start, 3),
              "candidate_examples": [item[1] for item in candidates[:20]]}
    if args.output:
        if not args.research_dir:
            parser.error("--output requires --research-dir")
        sys.path.insert(0, str(args.research_dir.resolve()))
        from export_artifact import export
        parent_records = [json.loads(line) for line in gzip.decompress((args.parent / "certificate.jsonl.gz").read_bytes()).splitlines()]
        allocated = parent_records[-1]["allocated_variables"]
        parent_records = [r for r in parent_records if r["kind"] not in ("weights", "final")]
        report["artifact"] = export(args.output, args.parent / "source-residuals.jsonl.gz", rows,
                                    parent_records + records, allocated,
                                    {"localized_eliminations": len(records)})
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "candidate_examples"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
