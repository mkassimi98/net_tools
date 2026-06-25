#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

IFACE="${1:-${REALTIME_INTERFACE:-any}}"
SECONDS="${REALTIME_SECONDS:-8}"

if command -v iftop >/dev/null 2>&1; then
  echo "+ timeout ${SECONDS}s sudo -n iftop -i $IFACE -t"
  timeout "${SECONDS}s" sudo -n iftop -i "$IFACE" -t || true
elif command -v nethogs >/dev/null 2>&1; then
  echo "+ timeout ${SECONDS}s sudo -n nethogs -t $IFACE"
  timeout "${SECONDS}s" sudo -n nethogs -t "$IFACE" || true
elif command -v bmon >/dev/null 2>&1; then
  echo "+ timeout ${SECONDS}s bmon"
  timeout "${SECONDS}s" bmon || true
else
  echo "None of iftop, nethogs, or bmon is installed."
fi
