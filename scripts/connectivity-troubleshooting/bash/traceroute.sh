#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_connectivity_config

TARGET="${1:-${TRACE_TARGET:-8.8.8.8}}"
MTR_CYCLES="${MTR_REPORT_CYCLES:-10}"

if command -v traceroute >/dev/null 2>&1; then
  echo "+ traceroute -n $TARGET"
  traceroute -n "$TARGET" || true
elif command -v mtr >/dev/null 2>&1; then
  echo "+ mtr -rwzc $MTR_CYCLES $TARGET"
  mtr -rwzc "$MTR_CYCLES" "$TARGET" || true
else
  echo "Neither traceroute nor mtr is installed."
fi
