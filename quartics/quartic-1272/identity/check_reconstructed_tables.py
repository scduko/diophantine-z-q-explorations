"""Independent exact fixed-S statistics and raw affine equivalence checks.

Imports only this auditor's local polynomial arithmetic, never the producer
or compiler. Does not establish source arithmetic soundness/completeness.
"""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

from check_identity import (
    OUT, ROOT, EXPONENT, add, clean, coefficient_groups, encode, power,
    scale, specialize_sign, substitute, term, write_json,
)


def load(path):
    raw = path.read_bytes()
    return json.loads(raw), sha256(raw).hexdigest()


def decode(terms):
    result = defaultdict(Fraction)
    for t in terms:
        m = tuple(t["monomial"])
        k = t["sPower"]
        assert all(type(i) is int and i >= 0 for i in m)
        assert m == tuple(sorted(m))
        assert type(k) is int and k >= 0
        result[(m, k)] += Fraction(t["coefficient"])
    return clean(result)


def csub(p, q):
    return {k: p.get(k, 0) - q.get(k, 0) for k in p.keys() | q.keys()
            if p.get(k, 0) != q.get(k, 0)}


def cscale(p, a):
    return {k: a * c for k, c in p.items() if a * c}


def coeff_json(p):
    return [{"sPower": k, "coefficient": str(c)} for k, c in sorted(p.items())]


def check_table(variant):
    path = ROOT / "compiler" / variant / "polynomial.json"
    data, digest = load(path)
    assert data["schema"] == "brox-sparse-polynomial-v1"
    assert data["fixedParameter"] == "S = 3^(2^27)"
    assert Fraction(data["sosMultiplier"]) == 1
    p = decode(data["terms"])
    assert len(p) == len(data["terms"]), "Duplicate or zero entries"
    assert all(c.denominator == 1 for c in p.values())
    grouped = coefficient_groups(p)
    active = sorted({v for m in grouped for v in m})
    coordinate_ids = [c["id"] for c in data["coordinates"]]
    assert coordinate_ids == list(range(len(coordinate_ids)))
    assert active == coordinate_ids
    maximum = {}
    max_monomial = None
    independent_gcd = 0
    max_dominance_bound_bits = 0
    positive = {}
    for m, coeff in grouped.items():
        sign = specialize_sign(coeff)
        assert sign != 0
        absolute = cscale(coeff, sign)
        positive[m] = absolute
        if specialize_sign(csub(absolute, maximum)) > 0:
            maximum, max_monomial = absolute, m
        if set(coeff) <= {0}:
            independent_gcd = math.gcd(independent_gcd, abs(int(coeff.get(0, 0))))
    # Recheck the selected maximum against each absolute coefficient.
    for m, coeff in grouped.items():
        for signed in (coeff, cscale(coeff, -1)):
            diff = csub(maximum, signed)
            assert specialize_sign(diff) >= 0
            if diff:
                lead = diff[max(diff)]
                ratio = sum(abs(c) for k, c in diff.items() if k < max(diff)) / abs(lead)
                max_dominance_bound_bits = max(max_dominance_bound_bits, ratio.numerator.bit_length())
    assert independent_gcd == 1
    assert grouped[(0, 0, 0, 0)] == {0: Fraction(1)}
    return {
        "variant": variant, "path": path.relative_to(ROOT).as_posix(), "sha256": digest,
        "status": "PASS", "scope": "Exact specialized coefficient statistics, not source equivalence",
        "encoded_entries": len(p), "ordinary_monomials": len(grouped),
        "active_coordinates": len(active), "witnesses": len(active) - 1,
        "degree": max(len(m) for m in grouped),
        "maximum_absolute_coefficient": coeff_json(maximum),
        "maximum_attained_at_monomial": list(max_monomial),
        "max_required_leading_domination_bound_bits": max_dominance_bound_bits,
        "available_bound_bits": EXPONENT,
        "S_independent_coefficient_gcd": independent_gcd,
        "input_fourth_power_coefficient": "1", "primitive_after_specialization": True,
        "monomials_receiving_multiple_S_powers": [
            {"monomial": list(m), "coefficient": coeff_json(c)}
            for m, c in grouped.items() if len(c) > 1
        ],
        "identity_with_published_Brox1315": False,
    }


def check_raw_translation():
    base = ROOT / "builder"
    direct, direct_hash = load(base / "raw-ir.json")
    translated, translated_hash = load(base / "raw-translated-ir.json")
    assert len(direct["coordinates"]) == len(translated["coordinates"])
    assert len(direct["residuals"]) == len(translated["residuals"])
    private = direct["anchor"]["privateCoordinateIds"]
    assert private == translated["anchor"]["privateCoordinateIds"]
    for old, new in zip(direct["coordinates"], translated["coordinates"]):
        if old["id"] in private:
            assert {k: v for k, v in old.items() if k != "name"} == {
                k: v for k, v in new.items() if k != "name"}
        else:
            assert old == new
    rowid = direct["anchor"]["rowId"]
    assert rowid == translated["anchor"]["rowId"]
    u, v, w = private
    U, V, W = [term(variables=(i,)) for i in private]
    S = term(s_power=1)
    forward = {
        u: add(S, scale(add(U, scale(V, -3), scale(W, 3)), Fraction(1, 4))),
        v: add(scale(S, Fraction(1, 2)), scale(V, Fraction(1, 4))),
        w: add(scale(S, Fraction(3, 2)), scale(W, Fraction(1, 4))),
    }
    inverse = {
        u: add(scale(U, 4), scale(V, 12), scale(W, -12), scale(S, 8)),
        v: add(scale(V, 4), scale(S, -2)),
        w: add(scale(W, 4), scale(S, -6)),
    }
    for i in private:
        assert substitute(forward[i], inverse) == term(variables=(i,))
        assert substitute(inverse[i], forward) == term(variables=(i,))
    old_rows = {r["id"]: decode(r["terms"]) for r in direct["residuals"]}
    new_rows = {r["id"]: decode(r["terms"]) for r in translated["residuals"]}
    assert len(old_rows) == len(direct["residuals"])
    assert old_rows.keys() == new_rows.keys()
    for i in old_rows:
        if i == rowid:
            assert new_rows[i] == scale(substitute(old_rows[i], forward), 16)
        else:
            assert all(not set(m).intersection(private) for m, k in old_rows[i])
            assert old_rows[i] == new_rows[i]
    # The full raw SOS identity differs by exactly 255*(old anchor o T)^2.
    old_anchor_after = substitute(old_rows[rowid], forward)
    difference = add(power(new_rows[rowid], 2), scale(power(old_anchor_after, 2), -1))
    assert difference == scale(power(old_anchor_after, 2), 255)
    assert difference
    return {
        "status": "PASS", "direct_raw_sha256": direct_hash,
        "translated_raw_sha256": translated_hash,
        "residuals": len(old_rows), "coordinates": len(direct["coordinates"]),
        "anchor_row": rowid, "private_coordinate_ids": private,
        "unchanged_other_rows": len(old_rows) - 1,
        "anchor_identity": "q_translated = 16 * (q_direct composed with affine map)",
        "affine_inverse_checked_both_directions": True, "linear_determinant": "1/64",
        "private_coordinates_only_in_anchor": True,
        "residual_zero_sets_affinely_bijective_over_characteristic_zero": True,
        "rational_SOS_input_projections_equal": True,
        "literal_SOS_affine_identity": False,
        "exact_SOS_difference": "P_translated - (P_direct composed with affine map) = 255*(q_direct composed with affine map)^2",
        "does_not_establish": "Equivalence of either raw source to the published missing gate program or source arithmetic theorem",
    }


def main():
    results = [check_table("direct"), check_table("translated")]
    raw = check_raw_translation()
    write_json("reconstructed_table_checks.json", {
        "status": "PASS", "tables": results, "raw_translation": raw,
        "full_certificate_replay": "separate independent checker responsibility",
    })
    print(json.dumps({
        "status": "PASS",
        "tables": [{k: v for k, v in r.items() if k not in ("monomials_receiving_multiple_S_powers", "maximum_absolute_coefficient")} for r in results],
        "translated_maximum": results[1]["maximum_absolute_coefficient"],
        "raw_translation": raw,
    }, indent=2))


if __name__ == "__main__":
    main()
