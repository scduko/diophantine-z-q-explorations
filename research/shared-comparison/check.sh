#!/bin/sh
# Regenerate source/ and quartic/ from the pinned Version 2 source and compare them
# byte for byte with the committed files.  Run from this directory.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
python3 -I "$here/build_shared_source.py" "$here/../../quartics/quartic-12504/source" "$tmp/source"
python3 -I "$here/quadratic_lift.py" "$tmp/source/residuals.jsonl" "$tmp/quartic"
diff -r "$here/source" "$tmp/source"
diff -r "$here/quartic" "$tmp/quartic"
echo "PASS: source/ and quartic/ reproduce exactly"
