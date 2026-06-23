#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_connectivity_config

TARGET_OK="${1:-${PING_SUCCESS_TARGET:-8.8.8.8}}"
TARGET_FAIL="${2:-${PING_FAILURE_TARGET:-203.0.113.254}}"
COUNT="${COUNT:-${PING_COUNT:-4}}"

echo "+ ping -c $COUNT $TARGET_OK"
ping -c "$COUNT" "$TARGET_OK" || true

echo
echo "+ ping -c $COUNT $TARGET_FAIL"
ping -c "$COUNT" "$TARGET_FAIL" || true
