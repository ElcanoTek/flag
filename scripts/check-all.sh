#!/bin/sh
# check-all.sh — every check CI runs, in one command (also `make check`).
# Needs only sh, perl and python3 (standard library), plus shellcheck for the
# tools lint (pinned release; skipped with a note when absent); no npm.
set -u
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT" || exit 2
failed=""
run() {
  name=$1; shift
  echo "== $name"
  if ! "$@"; then failed="$failed $name"; fi
}
run vendorable sh design-system/check-vendorable.sh
run email      sh design-system/check-email-template.sh
run tokens     python3 scripts/check_tokens.py
run refs       python3 scripts/check_refs.py
run license    sh scripts/check_license.sh
run tools      sh scripts/check_product_tools.sh
if [ -n "$failed" ]; then
  echo "FAILED:$failed" >&2
  exit 1
fi
echo "all checks passed"
