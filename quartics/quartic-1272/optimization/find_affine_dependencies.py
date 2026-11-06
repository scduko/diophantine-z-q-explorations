"""Find exact rational combinations whose quadratic terms cancel.

This is a search aid. It does not certify the source arithmetic. Every proposed
combination can be implemented by invertible constant row additions, followed
by the compiler's checked affine substitution. S powers are distinct columns;
therefore no division by S, or specialization of S, enters a proposal.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def add_scaled(target, source, factor):
    for key, value in source.items():
        updated = target.get(key, Fraction()) + factor * value
        if updated:
            target[key] = updated
        else:
            target.pop(key, None)


def read_row(row):
    result = {}
    for t in row['terms']:
        key = t.get('sPower', 0), tuple(t['monomial'])
        value = result.get(key, Fraction()) + Fraction(t['coefficient'])
        if value:
            result[key] = value
        else:
            result.pop(key, None)
    return result


def search(data, max_combination=80, max_columns=1000):
    rows = {r['id']: read_row(r) for r in data['residuals']}
    protected = {c['id'] for c in data['coordinates']
                 if c.get('protected') or c.get('kind') == 'input'} | {0}
    quadratics = {rid: {key: value for key, value in row.items() if len(key[1]) == 2}
                  for rid, row in rows.items()}
    frequency = {}
    for q in quadratics.values():
        for key in q:
            frequency[key] = frequency.get(key, 0) + 1
    # Rare monomials tend to expose independent rows before fill-in occurs.
    column_order = {key: i for i, key in enumerate(sorted(frequency, key=lambda k: (frequency[k], k)))}
    basis = {}
    candidates = []
    skipped = 0
    for rid in sorted(rows, key=lambda r: (len(quadratics[r]), str(r))):
        q = quadratics[rid].copy()
        if not q:
            continue
        combination = {rid: Fraction(1)}
        while q:
            pivot = min(q, key=column_order.__getitem__)
            if pivot not in basis:
                basis[pivot] = q, combination
                break
            known_q, known_combination = basis[pivot]
            factor = -q[pivot] / known_q[pivot]
            add_scaled(q, known_q, factor)
            add_scaled(combination, known_combination, factor)
            if len(combination) > max_combination or len(q) > max_columns:
                skipped += 1
                break
        else:
            affine = {}
            for source, factor in combination.items():
                add_scaled(affine, rows[source], factor)
            if any(len(m) > 1 for _, m in affine):
                raise AssertionError('Quadratic cancellation failed')
            variables = {m[0] for s, m in affine if len(m) == 1 and s == 0}
            # Require a genuine rational scalar pivot: no other S^k*v term.
            variables = {v for v in variables if not any(s and m == (v,) for s, m in affine)}
            useful = variables - protected
            if not useful:
                continue
            candidate = {
                'rowCombination': [{'residual': source, 'coefficient': str(factor)}
                                   for source, factor in sorted(combination.items(), key=lambda p: str(p[0]))],
                'affineTerms': [{'sPower': s, 'monomial': list(m), 'coefficient': str(c)}
                                for (s, m), c in sorted(affine.items())],
                'eligibleCoordinates': sorted(useful),
            }
            candidates.append(candidate)
    return {'quadraticRank': len(basis), 'skippedForSearchBounds': skipped,
            'candidateCount': len(candidates), 'candidates': candidates,
            'limits': {'maxCombination': max_combination, 'maxColumns': max_columns}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--max-combination', type=int, default=80)
    args = parser.parse_args()
    raw = args.source.read_bytes()
    data = json.loads(raw.decode('utf-8-sig'))
    result = search(data, args.max_combination)
    result['inputSha256'] = hashlib.sha256(raw).hexdigest()
    result['schema'] = 'brox-affine-dependency-proposals-v1'
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'candidates'}, indent=2))


if __name__ == '__main__':
    main()
