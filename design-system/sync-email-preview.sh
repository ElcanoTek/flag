#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
SOURCE_FILE="$SCRIPT_DIR/email-safe.html"
PREVIEW_FILE="$SCRIPT_DIR/preview/email-safe.html"

cp "$SOURCE_FILE" "$PREVIEW_FILE"

printf 'Synced %s -> %s\n' "$SOURCE_FILE" "$PREVIEW_FILE"
