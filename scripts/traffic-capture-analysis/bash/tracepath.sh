#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

TARGET="${1:-${TRACEPATH_TARGET:-8.8.8.8}}"
TIMEOUT_SECONDS="${TRACEPATH_TIMEOUT_SECONDS:-20}"

echo "+ timeout $TIMEOUT_SECONDS tracepath $TARGET"
timeout "$TIMEOUT_SECONDS" tracepath "$TARGET" || true
