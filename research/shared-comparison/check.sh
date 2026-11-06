#!/bin/sh
# Reproducibility check for research/shared-comparison.  Run from any directory.
#  1. Verify the pinned Version 2 inputs and this directory's files against SHA256SUMS.
#  2. Regenerate source/ and quartic/ (with their exact equivalence checks) and
#     compare them byte for byte with the committed files.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
(cd "$here" && sha256sum --quiet -c SHA256SUMS)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
python3 -I -B "$here/build_shared_source.py" "$here/../../quartics/quartic-12504/source" "$tmp/source"
python3 -I -B "$here/quadratic_lift.py" "$tmp/source/residuals.jsonl" "$tmp/quartic"
diff -r "$here/source" "$tmp/source"
diff -r "$here/quartic" "$tmp/quartic"
echo "PASS: inputs and files match SHA256SUMS; source/ and quartic/ reproduce exactly"
