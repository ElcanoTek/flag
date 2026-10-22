#!/bin/sh
# check_license.sh — design-system/LICENSE (the copy products vendor next to
# their Flag files) must carry exactly the MIT text of the root LICENSE.
set -eu
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
root_mit=$(sed '/^THIRD-PARTY COMPONENTS/,$d' "$ROOT/LICENSE")
ds_mit=$(sed '/^This copy sits in design-system/,$d' "$ROOT/design-system/LICENSE")
if [ "$root_mit" != "$ds_mit" ]; then
  echo "ERROR: design-system/LICENSE's MIT text differs from the root LICENSE; copy it across" >&2
  exit 1
fi
grep -q 'ISC License' "$ROOT/design-system/icons/core-icons.svg" || {
  echo "ERROR: icons/core-icons.svg lost its Lucide ISC notice" >&2; exit 1; }
for f in fonts/nebula-sans/OFL.txt fonts/hack/LICENSE.md; do
  [ -f "$ROOT/design-system/$f" ] || { echo "ERROR: design-system/$f is missing" >&2; exit 1; }
done
echo "check-license: ok"
