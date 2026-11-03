#!/usr/bin/env bash
# Verify a state license with the DEA Lookup.com State License API.
# Requires SL_API_ENDPOINT, SL_API_USERNAME and SL_API_PASSWORD environment variables.
# Usage: ./verify_license.sh A123456 CA MD DOE
set -euo pipefail
curl -sS -X POST "$SL_API_ENDPOINT" \
  --max-time 200 \
  --data-urlencode "username=$SL_API_USERNAME" \
  --data-urlencode "password=$SL_API_PASSWORD" \
  --data-urlencode "SL_n=$1" \
  --data-urlencode "SL_s=$2" \
  --data-urlencode "SL_pd=$3" \
  --data-urlencode "SL_ln=${4:-}" \
  --data-urlencode "OutputFormat=JSON"
echo
