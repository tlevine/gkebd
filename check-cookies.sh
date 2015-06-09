#!/bin/sh
set -e

url="$1"
domain=$(echo "$url" | cut -d/ -f3)

configdir=$(echo "$PWD"/elinks/$(date --rfc-3339 date)/"$domain")
echo $configdir
mkdir -p "$configdir"

elinks -config-dir "$configdir" -no-connect 1 -touch-files 1 \
  -eval 'set ecmascript.enable = 1' \
  -eval 'set ecmascript.ignore_noscript = 1' \
  "$url"
