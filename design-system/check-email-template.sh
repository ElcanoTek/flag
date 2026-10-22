#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
SOURCE_FILE="$SCRIPT_DIR/email-safe.html"
PREVIEW_FILE="$SCRIPT_DIR/preview/email-safe.html"
HTML_LIMIT=100000
STYLE_LIMIT=8192

html_size=$(wc -c < "$SOURCE_FILE" | tr -d ' ')
style_size=$(perl -0ne 'my $sum = 0; while (/<style\b[^>]*>(.*?)<\/style>/sg) { $sum += length($1); } print $sum;' "$SOURCE_FILE")

printf 'Email HTML size: %s bytes\n' "$html_size"
printf 'Embedded style size: %s bytes\n' "$style_size"

if [ "$html_size" -gt "$HTML_LIMIT" ]; then
  printf 'ERROR: email HTML exceeds %s bytes\n' "$HTML_LIMIT" >&2
  exit 1
fi

if [ "$style_size" -gt "$STYLE_LIMIT" ]; then
  printf 'ERROR: embedded style blocks exceed %s bytes\n' "$STYLE_LIMIT" >&2
  exit 1
fi

if [ -f "$PREVIEW_FILE" ]; then
  if ! cmp -s "$SOURCE_FILE" "$PREVIEW_FILE"; then
    printf 'ERROR: preview email copy is out of sync. Run bash design-system/sync-email-preview.sh\n' >&2
    exit 1
  fi
  printf 'Preview copy is in sync.\n'
fi

printf 'Email template checks passed.\n'
