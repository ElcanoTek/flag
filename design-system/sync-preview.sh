#!/bin/sh
# sync-preview.sh — refresh the preview's byte copies of canonical files.
# The live preview (Cloudflare Pages) publishes preview/ with only tokens/,
# fonts/, icons/ and logos/ beside it, so files the preview needs from
# elsewhere in design-system/ are copied in. CI (scripts/check_refs.py and
# check-email-template.sh) fails when a copy drifts.
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

cp "$SCRIPT_DIR/components/components.css" "$SCRIPT_DIR/preview/components.css"
printf 'Synced components/components.css -> preview/components.css\n'
sh "$SCRIPT_DIR/sync-email-preview.sh"
