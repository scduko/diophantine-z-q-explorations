"""Independent, bounded exact checks of the published Brox1315 anchor.

No author producer is imported. S is formal here and is specialized only
through proven inequalities or modular arithmetic. The giant integer is
never constructed. This does not reconstruct the missing full polynomial.
"""

from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math
import re


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "sources/diophantine_optimization_20261106_v3.tex"
PIN = "fc8bc7b8fae727e24f934ddd7de0a7cff8a005e89c3d0cac1ea14e5191b910ca"
COMMIT = "f4d1b5e6c23d4adeb3ae1f986ab0bf87884bdff6"
EXPONENT = 1 << 27


def clean(p):
    return {m: c for m, c in p.items() if c}


def term(c=1, variables=(), s_power=0):
    return clean({(tuple(sorted(variables)), s_power): Fraction(c)})


def add(*ps):
    out = defaultdict(Fraction)
    for p in ps:
        for m, c in p.items():
            out[m] += c
    return clean(out)


def scale(p, c):
    return clean({m: a * c for m, a in p.items()})


def mul(p, q):
    out = defaultdict(Fraction)
    for (m, k), a in p.items():
        for (n, l), b in q.items():
            out[(tuple(sorted(m + n)), k + l)] += a * b
    return clean(out)


def power(p, n):
    out = term()
    for _ in range(n):
        out = mul(out, p)
    return out


def substitute(p, mapping):
    out = {}
    for (m, k), c in p.items():
        t = term(c, s_power=k)
        for v in m:
            t = mul(t, mapping.get(v, term(variables=(v,))))
        out = add(out, t)
    return out


def encode(p):
    return [
        {"monomial": list(m), "sPower": k,
         "coefficient": str(c.numerator) + "/" + str(c.denominator)}
        for (m, k), c in sorted(p.items())
    ]


def support(p):
    return {m for m, _ in p}


def coefficient_groups(p):
    out = defaultdict(dict)
    for (m, k), c in p.items():
        out[m][k] = c
    return out


def specialize_sign(coefficients):
    """Sound sufficient test, not a complete sign algorithm.

    For S=3^EXPONENT > 2^EXPONENT and d=max degree,
    |sum_(i<d) a_i S^i| <= sum|a_i| S^(d-1).
    Test a stronger tiny-integer bound using numerator bit lengths.
    """
    coefficients = {k: Fraction(c) for k, c in coefficients.items() if c}
    if not coefficients:
        return 0
    d = max(coefficients)
    lead = coefficients[d]
    lower = sum(abs(c) for k, c in coefficients.items() if k < d)
    ratio = lower / abs(lead)
    # ratio <= numerator, so bit_length(numerator) <= EXPONENT proves
    # ratio < 2^EXPONENT < S. Do not construct 2^EXPONENT.
    if ratio.numerator.bit_length() > EXPONENT:
        raise ValueError("No domination certificate available")
    return 1 if lead > 0 else -1


def is_integer_at_fixed_s(coefficients):
    """For nonnegative S powers, check numerator(S) = 0 modulo D."""
    if any(k < 0 for k in coefficients):
        raise ValueError("Negative S powers need a separate certificate")
    denominator = math.lcm(*(Fraction(c).denominator for c in coefficients.values()))
    residue = pow(3, EXPONENT, denominator)
    total = sum(
        int(Fraction(c) * denominator) * pow(residue, k, denominator)
        for k, c in coefficients.items()
    )
    return total % denominator == 0


def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    raw = SOURCE.read_bytes()
    assert sha256(raw).hexdigest() == PIN
    lines = raw.decode("utf-8").splitlines()
    digests = []
    for i, line in enumerate(lines, 1):
        for digest in re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", line):
            digests.append({"line": i, "sha256": digest})

    variables = {i: term(variables=(i,)) for i in range(52, 58)}
    A = add(variables[52], variables[53], scale(variables[54], -1))
    U, V, W = [variables[i] for i in (55, 56, 57)]
    S = term(s_power=1)
    anchor = add(scale(power(A, 2), -3), scale(power(U, 2), 16),
                 scale(power(V, 2), 96), scale(power(W, 2), -32),
                 term(32, s_power=2))
    forward = {
        55: add(S, scale(add(U, scale(V, -3), scale(W, 3)), Fraction(1, 4))),
        56: add(scale(S, Fraction(1, 2)), scale(V, Fraction(1, 4))),
        57: add(scale(S, Fraction(3, 2)), scale(W, Fraction(1, 4))),
    }
    inverse = {
        55: add(scale(U, 4), scale(V, 12), scale(W, -12), scale(S, 8)),
        56: add(scale(V, 4), scale(S, -2)),
        57: add(scale(W, 4), scale(S, -6)),
    }
    translated = add(scale(power(A, 2), -3), power(U, 2),
                     scale(mul(U, V), -6), scale(mul(U, W), 6),
                     scale(power(V, 2), 15), scale(mul(V, W), -18),
                     scale(power(W, 2), 7), scale(mul(S, U), 8))
    assert substitute(anchor, forward) == translated
    assert all(substitute(forward[i], inverse) == variables[i] for i in forward)
    assert all(substitute(inverse[i], forward) == variables[i] for i in inverse)
    assert Fraction(1, 4) ** 3 == Fraction(1, 64)
    old_square, new_square = power(anchor, 2), power(translated, 2)
    assert substitute(old_square, forward) == new_square
    assert all(c.denominator == 1 for c in translated.values())
    assert all(c.denominator == 1 for c in new_square.values())
    assert len(support(old_square)) == 49
    assert len(support(new_square)) == 79
    private = {55, 56, 57}
    old_private = {m for m in support(old_square) if private.intersection(m)}
    new_private = {m for m in support(new_square) if private.intersection(m)}
    assert len(old_private) == 27
    assert len(new_private) == 64
    assert [(m, c) for (m, k), c in new_square.items() if k == 2] == [((55, 55), Fraction(64))]
    assert max(abs(c) for (m, k), c in new_square.items() if k == 1) == 288
    assert max(abs(c) for (m, k), c in new_square.items() if k == 0) == 540
    assert all(len(group) == 1 for group in coefficient_groups(new_square).values())

    # These checks prove the specialization statements without materializing S.
    assert specialize_sign({0: 1, 2: -192}) == -1  # 1 - 192*kappa
    assert specialize_sign({2: 64, 1: -288}) == 1
    assert specialize_sign({2: 64, 0: -(1 << 1020)}) == 1
    assert all(specialize_sign(g) != 0 for g in coefficient_groups(new_square).values())
    assert is_integer_at_fixed_s({1: Fraction(1, 2), 0: Fraction(1, 2)})
    assert not is_integer_at_fixed_s({1: Fraction(1, 2)})
    # Formal content 1 does not imply primitive specialized integer content.
    assert pow(3, EXPONENT, 2) == 1
    assert is_integer_at_fixed_s({1: Fraction(1, 2), 0: Fraction(3, 2)})
    # 64*S^2 < 2^429496736, by 3^5<2^8.
    assert 3 ** 5 < 2 ** 8
    assert 6 + Fraction(8, 5) * (1 << 28) < 429496736

    write_json("anchor_certificate.json", {
        "status": "exact-local-identity-verified",
        "scope": "Displayed anchor only; not the missing 1272-row residual system",
        "source_sha256": PIN,
        "source_lines": {"anchor_and_maps": [4674, 4708], "bounds": [4738, 4757]},
        "fixed_S": {"base": 3, "exponent": EXPONENT, "is_coordinate": False},
        "anchor": encode(anchor), "translated_anchor": encode(translated),
        "forward": {str(i): encode(p) for i, p in forward.items()},
        "inverse": {str(i): encode(p) for i, p in inverse.items()},
        "original_square": encode(old_square), "translated_square": encode(new_square),
        "linear_determinant": "1/64",
        "original_square_support": len(support(old_square)),
        "translated_square_support": len(support(new_square)),
        "original_private_support": len(old_private),
        "translated_private_support": len(new_private),
        "translated_integer_coefficient_max": 540,
        "translated_S_coefficient_max": 288,
        "translated_S_squared_coefficient": 64,
        "S_power_overlap_in_anchor_square": False,
        "global_support_29021": "not certified without full table and overlap checks",
        "global_height_64S2": "not certified without remainder coefficient bound and input coefficient 1",
    })
    write_json("source_receipts.json", {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_path": SOURCE.relative_to(ROOT).as_posix(), "source_sha256": PIN,
        "source_commit": COMMIT,
        "source_url": "https://github.com/JoseBrox/diophantine-z-q_improvements/blob/" + COMMIT + "/paper/diophantine_optimization_20261106_v3.tex",
        "printed_64_hex_digests": digests,
        "digest_objects_by_first_line": {
            "7623": "released 12504-variable coefficient table, repeated at 9451",
            "9107": "upstream quartic_12504.tex at 28e87b1b62af0effd954605af7f70b2699dd5672",
            "9453": "12493-variable coefficient table",
            "9455": "12465-variable coefficient table",
            "9457": "12449-variable uncompressed JSON coefficient table",
            "9459": "853-variable circuit", "9461": "854-variable circuit",
        },
        "printed_digest_for_1315_direct": None,
        "printed_digest_for_1315_translated": None,
        "direct_reported_statistics": {
            "variables": 1315, "residuals": 1272, "arithmetic_gates": 1285,
            "row_additions": 11, "eliminations": 60, "encoded_entries": 28991,
            "specialized_monomials": 28987, "degree": 4, "source_lines": [4607, 4641],
            "coefficient_overlaps": "constant c0+1024*kappa^2 and three coefficients 1-192*kappa",
        },
        "translated_reported_statistics": {
            "variables": 1315, "witnesses": 1314, "residuals": 1272,
            "specialized_monomials": 29021, "degree": 4,
            "primitive_height": "64*3^(2^28)", "source_lines": [4710, 4757],
            "compressed_bytes_from_benchmark": 277288,
            "benchmark_bytes_are_not_an_identity_check": True,
        },
        "missing_identity_receipts": [
            "research/phase3/quartic/quartic-direct/polynomial.json.gz",
            "research/phase3/quartic/quartic-direct-translated/polynomial.json.gz",
            "quartic-base-change-verification_20261106_v1.json",
            "full archive MANIFEST.json and verification index",
        ],
        "where_absent_receipts_are_described": [[4865, 4881], [7938, 7942], [9594, 9620], [9671, 9680]],
        "public_api_observation": {
            "main": COMMIT, "head_commit_utc": "2026-11-06T16:20:44Z",
            "tree_truncated": False, "release_count": 0,
            "paths": ["README.md", "data", "data/polynomial_benchmarks.csv", "data/polynomial_benchmarks.json", "docs", "docs/IMPORT_ARCHIVE.md", "paper", "paper/diophantine_optimization_20261106_v3.tex"],
            "observation_method": "Read-only GitHub API calls in this audit; no public artifact recovered",
        },
    })
    result = {
        "status": "PASS", "scope": "local identity and fixed-S proof criteria only",
        "full_1315_polynomial_verified": False,
        "source_hash_verified": True, "source_digest_occurrences": len(digests),
        "anchor_identity": True, "both_affine_compositions": True,
        "square_identity": True, "local_support_and_bounds": True,
        "fixed_S_domination_checks": True, "modular_integrality_checks": True,
        "primitive_specialization_caveat_checked": True,
    }
    write_json("checks.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
