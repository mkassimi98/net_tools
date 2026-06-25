#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

TARGET="${1:-${MTR_TARGET:-8.8.8.8}}"
CYCLES="${MTR_CYCLES:-10}"

if command -v mtr >/dev/null 2>&1; then
  echo "+ mtr -rwzc $CYCLES $TARGET"
  mtr -rwzc "$CYCLES" "$TARGET" || true
else
  echo "mtr not found. Install mtr to show latency/loss per hop."
fi
