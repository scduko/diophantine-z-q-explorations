#!/bin/sh
# Export every input of the verification, at pinned commits, into a NEW directory.
#   sh fetch_inputs.sh OUTPUT_DIR
# Requires git and network access to github.com. Nothing fetched is executed.
set -eu
out=$1
[ ! -e "$out" ] || { echo "refusing: $out exists" >&2; exit 2; }
PR_HEAD=65ae9cdeba8b9d218bebfc392cd4184b4567f6fd      # elliotglazer/diophantine-z-q PR #158 head reviewed
PR_BASE=54a4e576f1c8c577f33b0b97a2cedb5ca96af642      # its stated base (published Version 20)
BROX=7501669160c1662a742ddd54baed364a47c82ddc         # JoseBrox/diophantine-z-q_improvements pin
mkdir -p "$out/git-upstream" "$out/git-brox" "$out/pkg" "$out/v19" "$out/brox" "$out/main"
git -C "$out/git-upstream" init -q
git -C "$out/git-upstream" fetch -q --depth=1 https://github.com/elliotglazer/diophantine-z-q "$PR_HEAD" "$PR_BASE"
git -C "$out/git-brox" init -q
git -C "$out/git-brox" fetch -q --depth=1 https://github.com/JoseBrox/diophantine-z-q_improvements "$BROX"
git -C "$out/git-upstream" archive "$PR_HEAD" research/brox-explicit229-v68 | tar -x -C "$out/pkg"
V19=research/version19/construction/inputs/jose/computation/quartic/affine_laurent195_v45
git -C "$out/git-upstream" show "$PR_BASE:$V19/quadratic-family.json" > "$out/v19/quadratic-family.json"
git -C "$out/git-upstream" show "$PR_BASE:$V19/transformation.json" > "$out/v19/transformation.json"
git -C "$out/git-upstream" show "$PR_BASE:docs/explicit-record/README.md" > "$out/main/explicit-record-README.md"
git -C "$out/git-upstream" show "$PR_BASE:docs/explicit-record/measure_plain_text.py" > "$out/main/measure_plain_text.py"
for f in quadratic.json polynomial.json graft.json contact-change.json; do
  git -C "$out/git-brox" show "$BROX:computation/quartic/explicit229_v62/$f" > "$out/brox/$f"
done
echo "inputs exported to $out"
