#!/usr/bin/env python3
"""Finite regression checks for PROOF_FROM_THE_BOOK.md.

These checks do not prove the finite-contact lemma.  They check the exact
Lucas identities, congruences, parity choices, and numerical inequalities
used after that lemma has been granted.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def lucas(A: int, k: int) -> list[int]:
    u = [0, 1]
    for _ in range(1, k + 1):
        u.append(A * u[-1] - u[-2])
    return u


def main() -> None:
    samples = []
    negative_samples = []
    for A in range(7, 42):
        u = lucas(A, 2 * (A - 2) + 1)
        assert all((u[k] - k) % (A - 2) == 0 for k in range(len(u)))
        assert all((u[k] - ((-1) ** (k - 1)) * k) % (A + 2) == 0
                   for k in range(1, len(u)))
        assert all(u[k] >= (A - 1) ** (k - 1) for k in range(1, len(u)))

        # Positive-label completeness choice from the manuscript.
        if A % 6 == 1:
            k = 2 * (A - 2)
            b = u[k] // (A - 2)
            t = u[k + 1]
            assert (A - 2) * b == u[k]
            assert t * t - A * (A - 2) * t * b + (A - 2) ** 2 * b * b == 1
            assert b % 2 == 1 and t % 2 == 1
            samples.append({"a": A, "k": k, "b_bits": b.bit_length(),
                            "t_bits": t.bit_length()})

        # Bare negative-label existence from the second congruence.
        k_neg = A + 2
        b_neg = u[k_neg] // (A + 2)
        t_neg = u[k_neg + 1]
        a_neg = -A
        assert (A + 2) * b_neg == u[k_neg]
        assert (t_neg * t_neg - a_neg * (a_neg - 2) * t_neg * b_neg
                + (a_neg - 2) ** 2 * b_neg * b_neg == 1)
        if A in (7, 19, 41):
            negative_samples.append({"a": a_neg, "k": k_neg,
                                     "b_bits": b_neg.bit_length(),
                                     "t_bits": t_neg.bit_length()})

    # The final rational comparison is valid already for every integer A >= 4.
    assert all(Fraction(31, 200) * A < A - 3 for A in range(4, 10000))

    receipt = {
        "status": "pass",
        "scope": "finite regression; not a proof of the finite-contact lemma",
        "lucas_parameters_checked": [7, 41],
        "congruences": ["U_k = k mod (A-2)",
                        "U_k = (-1)^(k-1) k mod (A+2)"],
        "completeness_samples": samples,
        "negative_label_samples": negative_samples,
        "final_gap": "(31/200)A < A-3 checked for integers 4 <= A < 10000; exact algebra gives A > 600/169",
    }
    out = Path(__file__).with_name("BOOK_PROOF_CHECKS.json")
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
