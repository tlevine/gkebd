#!/bin/sh
set -e

url="$1"
domain=$(echo "$url" | cut -d/ -f3)
basedir=$($PWD/elinks/$(date --rfc-3339 day))

elinks -config-dir "$basedir/$domain" -no-connect 1 \
  -eval 'set ecmascript.enable = 1' \
  -eval 'set ecmascript.ignore_noscript = 1' \
  "$url"
