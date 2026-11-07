"""Reproduce the Version 4 terminal-row digest without the certificate checker."""
import gzip
import hashlib
import json
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parents[3]
    package = repo / "quartics" / "quartic-4973"
    rows = json.loads(gzip.decompress((package / "candidate-rows.json.gz").read_bytes()))
    records = [json.loads(line) for line in
               gzip.decompress((package / "certificate.jsonl.gz").read_bytes()).splitlines()]
    final = records[-1]
    assert final["kind"] == "final"
    assert len(rows) == 4879 and sum(bool(row) for row in rows) == 4552
    for row in rows:
        for coefficient, monomial in row:
            assert type(coefficient) is int and coefficient != 0
            assert all(type(v) is int and v >= 0 for v in monomial)
            assert monomial == sorted(monomial)
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(encoded).hexdigest()
    expected = "758e6c9f9225109017d2d80ee663a266c92ccf51de91f308304a02147031c7ea"
    assert digest == final["rows_sha256"] == expected
    print(json.dumps({"status": "PASS", "scope": "terminal-row serialization only",
                      "rows": len(rows), "nonempty_rows": sum(bool(row) for row in rows),
                      "serialized_bytes": len(encoded), "rows_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
