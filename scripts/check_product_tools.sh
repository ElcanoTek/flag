#!/bin/sh
# check_product_tools.sh — the shared product scripts in tools/product/ are
# lint-clean (shellcheck, as are Flag's own scripts), executable, at the
# versions the docs name, and the AGENTS.md standard block shipped beside
# them has the hash stack-check.sh pins.
set -u
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
T="$ROOT/tools/product"
fail=0
err() { echo "check-product-tools: $*" >&2; fail=1; }

for f in flag-sync.sh stack-check.sh flag-drift.yml agents-standard-block.md README.md; do
  [ -f "$T/$f" ] || err "tools/product/$f is missing"
done
[ "$fail" = 0 ] || exit 1

# Executable, in the working tree and in git's index (what a clone gets).
for f in flag-sync.sh stack-check.sh; do
  [ -x "$T/$f" ] || err "tools/product/$f is not executable"
  mode=$(git -C "$ROOT" ls-files -s -- "tools/product/$f" 2>/dev/null | cut -d' ' -f1)
  [ -z "$mode" ] || [ "$mode" = 100755 ] || err "tools/product/$f is committed as $mode, not 100755 (git update-index --chmod=+x)"
done

# Lint: one pinned shellcheck release, at every severity (-S style, the
# default, spelled out). Releases disagree (0.9, the runner's packaged one,
# reports SC2015 where 0.11 does not), so only the pinned release's findings
# count:
#   - CI (GitHub Actions sets CI=true) installs exactly this release first on
#     PATH (.github/workflows/ci.yml, sha256-verified) and fails if shellcheck
#     is missing, is any other version, or reports anything;
#   - locally the pinned release lints the same way; any other version, or
#     none, skips the lint with a note instead of failing on findings that
#     version would make.
SHELLCHECK_PIN=0.11.0
scv=""
if command -v shellcheck >/dev/null 2>&1; then
  scv=$(shellcheck --version | sed -n 's/^version: //p')
fi
lint="lint skipped"
if [ "$scv" = "$SHELLCHECK_PIN" ]; then
  lint="shellcheck $scv"
  shellcheck -S style "$T/flag-sync.sh" "$T/stack-check.sh" || err "shellcheck reports problems in tools/product/*.sh"
  # Flag's own shell scripts are held to the same bar.
  shellcheck -S style "$ROOT"/scripts/*.sh "$ROOT"/design-system/*.sh || err "shellcheck reports problems in Flag's own scripts"
elif [ -n "${CI:-}" ]; then
  err "shellcheck ${scv:-is not installed}${scv:+ in CI}; CI must run the pinned release $SHELLCHECK_PIN"
elif [ -n "$scv" ]; then
  echo "check-product-tools: lint skipped: shellcheck $scv != pinned $SHELLCHECK_PIN; CI runs the pinned release"
else
  echo "check-product-tools: lint skipped: shellcheck not installed; CI runs the pinned release $SHELLCHECK_PIN"
fi

# Versions named in the docs match the scripts.
for pair in flag-sync.sh:FLAG_SYNC_VERSION stack-check.sh:STACK_CHECK_VERSION; do
  set -- "${pair%%:*}" "${pair#*:}"
  have=$(sed -n "s/^$2=\([0-9][0-9]*\)$/\1/p" "$T/$1")
  [ -n "$have" ] || { err "tools/product/$1 has no $2= line"; continue; }
  for doc in tools/product/README.md design-system/APPLY_TO_PRODUCT.md; do
    named=$(grep -o "$2=[0-9]*" "$ROOT/$doc" | sort -u)
    [ -n "$named" ] || err "$doc does not name $2"
    for n in $named; do
      [ "$n" = "$2=$have" ] || err "$doc names $n but tools/product/$1 is $2=$have"
    done
  done
done

# The standard block's hash is what stack-check.sh pins.
pinned=$(sed -n 's/^STANDARD_SHA=\([0-9a-f]*\)$/\1/p' "$T/stack-check.sh")
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
got=$(awk '/^<!-- BEGIN:elcano-frontend-standard/{f=1;next}/^<!-- END:elcano-frontend-standard/{f=0}f' "$T/agents-standard-block.md" | $SHA | cut -d' ' -f1)
[ "$got" = "$pinned" ] || err "tools/product/agents-standard-block.md hashes to $got; stack-check.sh pins $pinned"

# The drift template runs the shared script from the product's scripts/.
grep -q 'scripts/flag-sync.sh status' "$T/flag-drift.yml" || err "tools/product/flag-drift.yml does not run scripts/flag-sync.sh status"

[ "$fail" = 0 ] && echo "check-product-tools: ok ($lint, versions FLAG_SYNC=$(sed -n 's/^FLAG_SYNC_VERSION=//p' "$T/flag-sync.sh") STACK_CHECK=$(sed -n 's/^STACK_CHECK_VERSION=//p' "$T/stack-check.sh"), standard block hash)"
exit "$fail"
