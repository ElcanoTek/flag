#!/bin/sh
# check-vendorable.sh — keep the files products vendor (tokens, fonts, theme,
# icons, logos, components) safe to copy verbatim: no paths relative to this repo's docs,
# valid token JSON, and unique icon ids. See APPLY_TO_PRODUCT.md
# "Vendoring and drift".
set -eu

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$DIR"
fail=0

# 1. No relative references back into this repo (they break once vendored).
if grep -rnE '(\.\./|\./)[A-Z_]+\.md|\.\./(tokens|fonts|theme|icons|logos|preview)/' \
     tokens fonts/fonts.css theme icons logos components --include='*.css' --include='*.js' --include='*.svg' --include='*.json' 2>/dev/null; then
  echo "ERROR: vendorable files must not reference Flag docs by relative path; write \"Flag's design-system/<DOC>.md\"" >&2
  fail=1
fi

# 2. Token JSON parses.
if ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' tokens/design-tokens.json; then
  echo "ERROR: tokens/design-tokens.json is not valid JSON" >&2
  fail=1
fi

# 3. Icon ids are unique within the sprite.
dupes=$(grep -oE '<symbol[^>]*id="[^"]+"' icons/core-icons.svg | sed -E 's/.*id="([^"]+)"/\1/' | sort | uniq -d)
if [ -n "$dupes" ]; then
  echo "ERROR: duplicate icon ids in icons/core-icons.svg: $dupes" >&2
  fail=1
fi

[ "$fail" -eq 0 ] || exit 1
echo "check-vendorable: ok"
