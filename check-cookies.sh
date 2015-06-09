#!/bin/sh
url="$1"
domain=$(echo "$url" | cut -d/ -f3)
echo $domain
