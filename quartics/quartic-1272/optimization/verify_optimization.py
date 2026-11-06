"""Independent count, exponent and quadratic-rank checks for the reconstruction.

Uses only the Python standard library. Imports neither the builder nor compiler.
This check does not certify the external number-theoretic inputs.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
from math import isqrt

ROOT = Path(__file__).resolve().parent.parent


def load(relative):
    data = (ROOT / relative).read_bytes()
    return json.loads(data.decode('utf-8-sig')), sha256(data).hexdigest()


def rank_mod_prime(rows, p):
    # A full row rank over F_p proves full row rank over Q, because all
    # denominators are units and a nonzero minor survives reduction.
    assert p > 2 and all(p % d for d in range(2, isqrt(p) + 1))
    pivots = {}
    denominator_count = 0
    for row in rows:
        q = {}
        for term in row['terms']:
            if len(term['monomial']) != 2:
                continue
            assert term.get('sPower', 0) == 0, 'Quadratic terms depend on S'
            c = Fraction(term['coefficient'])
            assert c.denominator % p
            denominator_count += 1
            key = tuple(term['monomial'])
            value = (q.get(key, 0) + c.numerator * pow(c.denominator, -1, p)) % p
            if value:
                q[key] = value
            else:
                q.pop(key, None)
        while q:
            leading = max(q)
            if leading not in pivots:
                scale = pow(q[leading], -1, p)
                pivots[leading] = {key: value * scale % p for key, value in q.items()}
                break
            factor = q[leading]
            for key, value in pivots[leading].items():
                new_value = (q.get(key, 0) - factor * value) % p
                if new_value:
                    q[key] = new_value
                else:
                    q.pop(key, None)
    return {'prime': p, 'rank': len(pivots), 'rows': len(rows),
            'denominatorUnitsChecked': denominator_count,
            'quadraticTermsContainS': False,
            'pivotMonomialSha256': sha256(json.dumps(sorted(pivots)).encode()).hexdigest()}


raw, raw_hash = load('builder/raw-ir.json')
compiled, compiled_hash = load('compiler/direct/compiled-ir.json')
trace, trace_hash = load('compiler/direct/reduction-certificate.json')
coordinate_ids = {c['id'] for c in raw['coordinates']}
residual_ids = {r['id'] for r in raw['residuals']}
assert len(coordinate_ids) == len(raw['coordinates'])
assert len(residual_ids) == len(raw['residuals'])
gate_coordinates = [g['coordinateId'] for g in raw['gates']]
gate_rows = [g['definitionResidualId'] for g in raw['gates']]
assert len(set(gate_coordinates)) == len(gate_coordinates)
assert len(set(gate_rows)) == len(gate_rows)
assert set(gate_coordinates) <= coordinate_ids
assert set(gate_rows) <= residual_ids
assert len(coordinate_ids - set(gate_coordinates)) == 90
assert len(residual_ids - set(gate_rows)) == 47
operation_counts = Counter(op['kind'] for op in trace['operations'])
assert len(compiled['coordinates']) == len(raw['coordinates']) - operation_counts['eliminate']
assert len(compiled['residuals']) == len(raw['residuals']) - operation_counts['eliminate']
active = {v for row in compiled['residuals'] for term in row['terms'] for v in term['monomial']}
assert active == {c['id'] for c in compiled['coordinates']}
assert len(compiled['coordinates']) - len(compiled['residuals']) == 43

# Laurent monomials use exponent triples for (A, delta, F).
e = (5, 5, -1)
q1 = (5, 2, -1)
R = tuple(-x - y for x, y in zip(e, (0, 1, 0)))
assert R == (-5, -6, 1)
weight_checks = []
for order in (1, 16, 52):
    by_chain = tuple(x + (2 * order - 2) * y for x, y in zip(q1, e))
    by_source = (10 * order - 5, 10 * order - 8, 1 - 2 * order)
    assert by_chain == by_source
    weight_checks.append({'order': order, 'exponents': by_chain})
chain = [(2, 1, 1), (3, 2, 1), (6, 3, 3), (12, 6, 6),
         (24, 12, 12), (48, 24, 24), (96, 48, 48), (30, 24, 6), (102, 96, 6)]
available = {1}
for target, a, b in chain:
    assert a in available and b in available and target == a + b
    available.add(target)
assert {30, 102} <= available

# The optional scalar identities are Laurent monomial identities in (r,t).
# r*(t/r)^2 = t*(t/r), both with exponent (-1,2).
assert (1 + 2 * -1, 2) == (-1, 2)
scalar_powers = [1]
for _ in range(5):
    scalar_powers.append(2 * scalar_powers[-1])
assert scalar_powers[-1] == 32

rank = rank_mod_prime(compiled['residuals'], 1000000007)
assert rank['rank'] == rank['rows']
report = {
    'schema': 'brox-independent-optimization-check-v1',
    'status': 'passed',
    'inputSha256': {'raw': raw_hash, 'compiled': compiled_hash, 'trace': trace_hash},
    'counts': {'baseCoordinates': 90, 'structuralRows': 47,
               'rawCoordinates': len(raw['coordinates']), 'rawRows': len(raw['residuals']),
               'gates': len(raw['gates']), 'traceOperations': dict(operation_counts),
               'compiledCoordinates': len(compiled['coordinates']),
               'compiledRows': len(compiled['residuals']), 'allCoordinatesActive': True,
               'coordinateMinusRowInvariant': 43},
    'weightExponents': weight_checks,
    'ePowerChain': chain,
    'ePowerChainMultiplications': len(chain),
    'scalarInversePowers': scalar_powers,
    'optionalScalarGateSaving': 2,
    'optionalScalarChangesApplied': False,
    'quadraticRankCertificate': rank,
    'scope': 'Counts, exponent identities and affine-dependency exclusion only; no source arithmetic certification.'
}
destination = ROOT / 'optimization/optimization-check.json'
destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(report, indent=2))
