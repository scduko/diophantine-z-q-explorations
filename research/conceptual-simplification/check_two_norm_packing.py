"""Exact finite checks for TWO_NORM_PACKING.md; not a proof of the main theorem."""
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json


def multiplicative_order(a, p):
    x = a % p
    for n in range(1, p):
        if x == 1:
            return n
        x = x * a % p
    raise AssertionError((a, p))


def bareiss_det(matrix):
    a = [row[:] for row in matrix]
    previous = 1
    sign = 1
    for k in range(len(a) - 1):
        if a[k][k] == 0:
            pivot_row = next(i for i in range(k + 1, len(a)) if a[i][k])
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) // previous
        previous = pivot
        for i in range(k + 1, len(a)):
            a[i][k] = 0
    return sign * a[-1][-1]


def period_table(degree):
    """Multiplication in the Gaussian-period basis for the degree-d subfield."""
    orbit_size = 126 // degree
    cosets = []
    coset_of = {}
    for j in range(degree):
        coset = sorted({pow(3, j + degree * t, 127) for t in range(orbit_size)})
        cosets.append(coset)
        for value in coset:
            coset_of[value] = j
    assert len(coset_of) == 126

    # eta_i eta_j, with the constant eliminated by 1=-sum eta_k.
    table = []
    for i in range(degree):
        row = []
        for j in range(degree):
            constant = 0
            totals = [0] * degree
            for x in cosets[i]:
                for y in cosets[j]:
                    value = (x + y) % 127
                    if value == 0:
                        constant += 1
                    else:
                        totals[coset_of[value]] += 1
            assert all(value % orbit_size == 0 for value in totals)
            row.append([value // orbit_size - constant for value in totals])
        table.append(row)

    def multiply(x, y):
        out = [0] * degree
        for i, xi in enumerate(x):
            for j, yj in enumerate(y):
                for k, coefficient in enumerate(table[i][j]):
                    out[k] += xi * yj * coefficient
        return out

    one = [-1] * degree
    basis = []
    for i in range(degree):
        vector = [0] * degree
        vector[i] = 1
        basis.append(vector)
        assert multiply(one, vector) == vector
    for i, j, k in product(range(degree), repeat=3):
        assert multiply(multiply(basis[i], basis[j]), basis[k]) == \
               multiply(basis[i], multiply(basis[j], basis[k]))

    trace_gram = [[-sum(table[i][j]) for j in range(degree)]
                  for i in range(degree)]
    discriminant = bareiss_det(trace_gram)
    assert abs(discriminant) == 127 ** (degree - 1)
    coefficients = [coefficient for row in table for entry in row
                    for coefficient in entry]
    return {
        "degree": degree,
        "orbit_size": orbit_size,
        "discriminant": discriminant,
        "coefficient_values": sorted(set(coefficients)),
        "nonzero_structure_constants": sum(value != 0 for value in coefficients),
        "structure_constants": degree ** 3,
    }


# Cyclotomic and Gaussian residue arithmetic.
p = 127
assert all(p % d for d in range(2, isqrt(p) + 1))
assert multiplicative_order(3, p) == 126
assert min(n for n in range(1, 64) if pow(3, n, p) in (1, p - 1)) == 63
a, b = 1, 16
assert (a * a + b * b) % p == 3
assert ((a - 1) ** 2 + b * b) % p == 2
assert ((a + 1) ** 2 + b * b) % p == 6

# Detector homogeneity: delta^(1-r) converts a degree-r norm of raw
# order-m tests into the standard packed order-rm normalization.
groups = []
for r, m in ((9, 1), (7, 40)):
    packed = r * m
    assert (1 - r) - (packed + 1) == -r * (m + 1)
    groups.append({"count": r, "original_order": m,
                   "packed_order": packed,
                   "outer_delta_exponent": 1 - r,
                   "normalizing_delta_exponent": packed + 1})

# Check the strict one-place inequalities on a valuation grid.  If all
# raw valuations in a group fail their target, the packed norm cannot meet
# the lower bound from the existing lemma.
valuation_cases = 0
for alpha in range(1, 12, 2):
    for low_min, high_min in product(range(-3, 11), range(35, 43)):
        low_norm = 9 * low_min
        high_norm = 7 * high_min
        low_pass = low_norm > (9 - 0.75) * alpha
        high_pass = high_norm > (280 - 0.75) * alpha
        if low_pass:
            assert low_min >= 1
        if high_pass:
            assert high_min >= 40
        valuation_cases += 1

period_tables = [period_table(7), period_table(9)]

# K-coordinate assignments in direct quadratic norm circuits:
# degree 9: 9 for x*tau^3(x), 3 for the relative cubic result,
# 3 for z*tau(z), and 1 for the final norm;
# degree 7: three pair products, two next-level products, and one scalar
# final product, giving 3*7+2*7+1.
norm_coordinate_assignments = {"degree_9": 9 + 3 + 3 + 1,
                               "degree_7": 3 * 7 + 2 * 7 + 1}
assert sum(norm_coordinate_assignments.values()) == 52

# The current balanced coefficient trees assign 29 K-coefficients for
# nine leaves and 20 for seven, in addition to the sixteen test squares.
current_aggregation_assignments = 29 + 20 + 16
assert current_aggregation_assignments == 65

root = Path(__file__).resolve().parents[2]
paths = [
    "research/conceptual-simplification/TWO_NORM_PACKING.md",
    "research/conceptual-simplification/check_two_norm_packing.py",
    "manuscripts/quartic_v10.tex",
    "quartics/quartic-523-540/source-reproduction/builders/odd-product-asymmetric-source.cjs",
]
print(json.dumps({
    "status": "PASS_EXACT_FINITE_REGRESSIONS",
    "groups": groups,
    "valuation_cases": valuation_cases,
    "period_bases": period_tables,
    "preliminary_K_coordinate_counts": {
        "two_norms": norm_coordinate_assignments,
        "two_norm_total": 52,
        "current_test_squares_and_symmetric_trees": current_aggregation_assignments,
        "scope": "Excludes weights, final factor evaluation, quotients, and optimization.",
    },
    "cyclotomic_field": {
        "conductor": 127,
        "real_subfield_degree": 63,
        "subfield_degrees": [9, 7],
        "frobenius_class": 3,
        "ambient_order": 126,
        "real_quotient_order": 63,
        "gaussian_residue": [1, 16],
        "adjacent_norms_mod_127": [2, 6],
    },
    "scope": "Normalization, valuation thresholds, and residue arithmetic only.",
    "ray_flexibility_proved_in_prose": True,
    "production_candidate": False,
    "independent_human_review": False,
    "sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest()
               for path in paths},
}, indent=2))
