"""Bounded search for quadratic elimination modulo untouched quadratic rows.

The polynomial and linear-algebra code here is independent of the checker.
Only the standard library is needed. Run on the root-dispatched worker.
"""
import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
from math import gcd, lcm
from pathlib import Path
import sys
import time


def dec(row):
    return {tuple(mon): Fraction(c) for c, mon in row}


def enc(row):
    return [[int(c), list(mon)] for mon, c in sorted(row.items())]


def vars_in(row):
    return {v for mon in row for v in mon}


def plus(a, b, scalar=1):
    out = dict(a)
    for mon, c in b.items():
        value = out.get(mon, 0)+scalar*c
        if value:
            out[mon] = value
        else:
            out.pop(mon, None)
    return out


def add_to(a, b, scalar=1):
    for mon, c in b.items():
        value = a.get(mon, 0)+scalar*c
        if value:
            a[mon] = value
        else:
            a.pop(mon, None)


def times(a, b):
    out = {}
    for mon, c in a.items():
        for other, d in b.items():
            key = tuple(sorted(mon+other))
            out[key] = out.get(key, 0)+c*d
    return {mon: c for mon, c in out.items() if c}


def scale(a, c):
    return {mon: coefficient*c for mon, coefficient in a.items() if coefficient*c}


def primitive(poly):
    if not poly:
        return {}
    den = lcm(*(Fraction(c).denominator for c in poly.values()))
    row = {mon: int(c*den) for mon, c in poly.items()}
    common = gcd(*row.values())
    if row[min(row)] < 0:
        common = -common
    return {mon: c//common for mon, c in sorted(row.items())}


def rational(poly):
    den = lcm(*(Fraction(c).denominator for c in poly.values())) if poly else 1
    return {'terms': enc({mon: int(c*den) for mon, c in poly.items()}), 'denominator': den}


def substitute(row, v, replacement):
    result = {}
    for mon, c in row.items():
        term = {tuple(t for t in mon if t != v): c}
        for _ in range(mon.count(v)):
            term = times(term, replacement)
        result = plus(result, term)
    return result


def high(row):
    return {mon: c for mon, c in row.items() if len(mon) > 2}


def bit_size(row):
    return max((max(Fraction(c).numerator.bit_length(), Fraction(c).denominator.bit_length())
                for c in row.values()), default=0)


def divisors(mon, size):
    return sorted({tuple(mon[i] for i in inds) for inds in combinations(range(len(mon)), size)})


def quotient(mon, sub):
    result = list(mon)
    for v in sub:
        result.remove(v)
    return tuple(result)


class BoundExceeded(Exception):
    pass


class Search:
    def __init__(self, rows, args):
        self.rows = rows
        self.args = args
        self.incidence = defaultdict(set)
        self.quadratic_index = defaultdict(set)
        self.reasons = Counter()
        self.reindex()

    def reindex(self):
        self.incidence.clear(); self.quadratic_index.clear()
        for i, row in enumerate(self.rows):
            self.index(i, row, True)

    def index(self, i, row, insert):
        for v in vars_in(row):
            if insert:
                self.incidence[v].add(i)
            else:
                self.incidence[v].discard(i)
        if len(row) <= self.args.max_support_terms:
            for mon in row:
                if len(mon) == 2:
                    if insert:
                        self.quadratic_index[mon].add(i)
                    else:
                        self.quadratic_index[mon].discard(i)

    def candidates(self):
        out = []
        for i, row in enumerate(self.rows):
            for mon, c in row.items():
                if len(mon) != 1 or mon[0] == 0:
                    continue
                v = mon[0]
                if any(v in other for other in row if other != mon):
                    continue
                replacement = scale(plus(row, {mon: -c}), -Fraction(1, c))
                if not any(len(other) == 2 for other in replacement):
                    continue
                affected = self.incidence[v]-{i}
                if not affected or len(affected) > self.args.max_consumers:
                    continue
                difficulty = (sum(len(self.rows[j]) for j in affected), len(replacement), len(affected), i, v)
                out.append((difficulty, i, v))
        out.sort()
        return [(i, v) for _, i, v in out]

    def generators(self, seed, forbidden, v, deadline):
        queue = deque(sorted(seed, key=lambda m: (len(m), m), reverse=True))
        known = set(seed); seen = set(); generators = []
        while queue:
            if time.monotonic() >= deadline:
                raise BoundExceeded('time_limit')
            mon = queue.popleft()
            for sub in divisors(mon, 2):
                multiplier = quotient(mon, sub)
                eligible = [i for i in self.quadratic_index.get(sub, ()) if i not in forbidden]
                eligible.sort(key=lambda i: (len(high(self.rows[i])), len(self.rows[i]), i))
                for i in eligible[:self.args.max_rows_per_term]:
                    key = (i, multiplier)
                    if key in seen:
                        continue
                    seen.add(key)
                    assert v not in vars_in(self.rows[i])
                    full = times({multiplier: Fraction(1)}, self.rows[i])
                    hh = high(full)
                    if not hh:
                        continue
                    generators.append((key, hh))
                    if len(generators) >= self.args.max_generators:
                        self.reasons['generator_closure_truncated'] += 1
                        return generators
                    for term in hh:
                        if term not in known:
                            known.add(term); queue.append(term)
                    if len(known) > self.args.max_high_terms:
                        self.reasons['high_term_closure_truncated'] += 1
                        return generators
        return generators

    def build_basis(self, generators, deadline):
        # Each basis vector carries its exact expression in generators.
        basis = {}
        for number, (_, hh) in enumerate(generators):
            if time.monotonic() >= deadline:
                raise BoundExceeded('time_limit')
            current = hh.copy(); representation = {number: Fraction(1)}
            while current:
                pivot = max(current, key=lambda m: (len(m), m))
                if pivot not in basis:
                    lead = current[pivot]
                    basis[pivot] = (scale(current, 1/lead), scale(representation, 1/lead))
                    break
                previous, previous_rep = basis[pivot]
                factor = current[pivot]
                current = plus(current, previous, -factor)
                representation = plus(representation, previous_rep, -factor)
                if len(current)+len(representation) > self.args.max_linear_terms:
                    raise BoundExceeded('linear_algebra_size_limit')
                if max(bit_size(current), bit_size(representation)) > self.args.max_bits:
                    raise BoundExceeded('linear_algebra_bit_limit')
        return basis

    def solve(self, target, basis, deadline):
        residual = high(target); coefficients = {}
        while residual:
            if time.monotonic() >= deadline:
                raise BoundExceeded('time_limit')
            pivot = max(residual, key=lambda m: (len(m), m))
            if pivot not in basis:
                return None
            row, representation = basis[pivot]
            factor = residual[pivot]
            residual = plus(residual, row, -factor)
            coefficients = plus(coefficients, representation, factor)
            if len(residual)+len(coefficients) > self.args.max_linear_terms:
                raise BoundExceeded('solve_size_limit')
            if max(bit_size(residual), bit_size(coefficients)) > self.args.max_bits:
                raise BoundExceeded('solve_bit_limit')
        return coefficients

    def attempt(self, i, v, deadline):
        row = self.rows[i]
        c = row.get((v,), 0)
        if not c or any(v in mon for mon in row if mon != (v,)):
            self.reasons['definition_changed'] += 1; return None
        replacement = scale(plus(row, {(v,): -c}), -Fraction(1, c))
        affected = self.incidence[v]-{i}
        if len(affected) > self.args.max_consumers:
            self.reasons['consumer_limit'] += 1; return None
        images = {j: substitute(self.rows[j], v, replacement) for j in affected}
        seed = set().union(*(set(high(image)) for image in images.values())) if images else set()
        if not seed:
            self.reasons['ordinary_elimination'] += 1
        if len(seed) > self.args.max_high_terms:
            self.reasons['seed_limit'] += 1; return None
        generators = self.generators(seed, self.incidence[v], v, deadline)
        basis = self.build_basis(generators, deadline)
        patches = {i: {}}; reductions = []
        used_generators = set()
        for j, image in sorted(images.items()):
            solution = self.solve(image, basis, deadline)
            if solution is None:
                self.reasons['high_part_not_spanned'] += 1; return None
            multipliers = defaultdict(dict)
            for number, coefficient in solution.items():
                support, multiplier = generators[number][0]
                multipliers[support] = plus(multipliers[support], {multiplier: coefficient})
                used_generators.add(number)
            new = image
            terms = []
            for support, multiplier in sorted(multipliers.items()):
                if not multiplier:
                    continue
                new = plus(new, times(multiplier, self.rows[support]), -1)
                terms.append({'support': support, 'multiplier': rational(multiplier)})
            assert not high(new) and v not in vars_in(new)
            new = primitive(new)
            if len(new) > self.args.max_row_terms:
                self.reasons['row_size_limit'] += 1; return None
            patches[j] = new
            reductions.append({'row': j, 'terms': terms})
        data = {'row': i, 'variable': v, 'replacement': rational(replacement), 'reductions': reductions}
        event = {'kind': 'relation_eliminate', 'data': data,
                 'patches': [[j, enc(rr)] for j, rr in sorted(patches.items())]}
        stats = dict(variable=v, definition=i, consumers=len(affected), high_terms=len(seed),
                     generated=len(generators), rank=len(basis), used_generators=len(used_generators),
                     new_max_row_terms=max(map(len, patches.values()), default=0),
                     quadratic_multiplier=any(len(mon) == 2 for number in used_generators
                                              for mon in [generators[number][0][1]]))
        return event, patches, stats

    def apply(self, patches):
        for i, row in patches.items():
            self.index(i, self.rows[i], False)
            self.rows[i] = row
            self.index(i, row, True)


def main():
    assert __debug__, 'Assertions must remain enabled.'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--research-dir', type=Path)
    parser.add_argument('--source-entry', type=Path)
    parser.add_argument('--seconds', type=float, default=180)
    parser.add_argument('--candidate-seconds', type=float, default=1.5)
    parser.add_argument('--max-candidates', type=int, default=500)
    parser.add_argument('--max-operations', type=int, default=40)
    parser.add_argument('--max-consumers', type=int, default=8)
    parser.add_argument('--max-support-terms', type=int, default=12)
    parser.add_argument('--max-row-terms', type=int, default=96)
    parser.add_argument('--max-rows-per-term', type=int, default=16)
    parser.add_argument('--max-generators', type=int, default=240)
    parser.add_argument('--max-high-terms', type=int, default=240)
    parser.add_argument('--max-linear-terms', type=int, default=1200)
    parser.add_argument('--max-bits', type=int, default=512)
    parser.add_argument('--start', type=int, default=0)
    args = parser.parse_args()
    assert args.seconds > 0 and args.candidate_seconds > 0
    rows = [{tuple(mon): c for c, mon in row}
            for row in json.loads(gzip.decompress((args.parent/'candidate-rows.json.gz').read_bytes()))]
    records = [json.loads(line) for line in gzip.decompress((args.parent/'certificate.jsonl.gz').read_bytes()).splitlines()]
    source_entry = args.source_entry or args.parent/'source-entry.json'
    entry_bytes = source_entry.read_bytes()
    entry = json.loads(entry_bytes)
    assert entry['source_id'] == records[0]['source_id']
    assert entry['source_sha256'] == records[0]['source_sha256']
    assert hashlib.sha256(entry_bytes).hexdigest() == records[0]['source_entry_sha256']
    weights = json.loads((args.parent/'weights.json').read_text()) if (args.parent/'weights.json').exists() else [1]
    assert all(type(w) is int and w == 1 for w in weights)
    allocated = records[-1]['allocated_variables']
    records = [record for record in records if record['kind'] not in ('weights', 'final')]
    search = Search(rows, args)
    candidates = search.candidates()
    initial_active = len([v for v, ids in search.incidence.items() if ids])
    polynomial = {}
    for row in rows:
        add_to(polynomial, times(row, row))
    assert max(map(abs, polynomial.values())) < 2**80
    start = time.monotonic(); deadline = start+args.seconds
    stats = []; events = []; attempted = 0
    for i, v in candidates[args.start:args.start+args.max_candidates]:
        if time.monotonic() >= deadline or len(events) >= args.max_operations:
            break
        attempted += 1
        try:
            found = search.attempt(i, v, min(deadline, time.monotonic()+args.candidate_seconds))
        except BoundExceeded as exc:
            search.reasons[str(exc)] += 1; continue
        if found is None:
            continue
        event, patches, measured = found
        delta = {}
        for j, row in patches.items():
            delta = plus(delta, times(rows[j], rows[j]), -1)
            delta = plus(delta, times(row, row))
        if any(abs(polynomial.get(mon, 0)+c) >= 2**80 for mon, c in delta.items()):
            search.reasons['global_coefficient_limit'] += 1; continue
        add_to(polynomial, delta)
        search.apply(patches)
        events.append(event); stats.append(measured)
        print(json.dumps({'accepted': len(events), **measured}), flush=True)
    args.events.parent.mkdir(parents=True, exist_ok=True)
    args.events.write_text(''.join(json.dumps(event, separators=(',', ':'))+'\n' for event in events))
    active = len([v for v, ids in search.incidence.items() if ids])
    report = dict(status='UNTRUSTED SEARCH RESULT; independent replay required', parent=str(args.parent),
                  total_candidates=len(candidates), start=args.start, attempted=attempted, operations=len(events),
                  initial_variables=initial_active, final_variables=active, variables_removed=initial_active-active,
                  monomials=len(polynomial), max_abs_coefficient=str(max(map(abs, polynomial.values()))),
                  seconds=round(time.monotonic()-start, 3), reasons=dict(search.reasons), accepted=stats,
                  bounds={key: value for key, value in vars(args).items()
                          if key.startswith('max_') or key.endswith('seconds')})
    if args.output:
        assert args.research_dir
        sys.path.insert(0, str(args.research_dir))
        from export_artifact import export
        report['export'] = export(args.output, args.parent/'source-residuals.jsonl.gz', rows,
                                  records+events, allocated, {'relation_eliminations': len(events)})
        import shutil
        shutil.copy2(source_entry, args.output/'source-entry.json')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
