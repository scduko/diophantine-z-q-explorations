#!/bin/sh
# Fetch the pinned inputs into a fresh directory and run the independent checks.
#   sh run_all.sh [WORK_DIR]
set -eu
here=$(cd "$(dirname "$0")" && pwd)
work=${1:-$(mktemp -d)/inputs}
sh "$here/fetch_inputs.sh" "$work"
pkg="$work/pkg/research/brox-explicit229-v68"
python3 -I -B "$here/verify_pr158.py" --pkg "$pkg" --v19 "$work/v19" --brox "$work/brox" --main "$work/main"
python3 -I -B "$here/mutate.py" "$pkg" "$work/v19" "$work/brox" "$work/main"
python3 -I -B "$here/check_section5.py"
echo "ALL PASS"
