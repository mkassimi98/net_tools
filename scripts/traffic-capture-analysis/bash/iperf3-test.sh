#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

SERVER="${1:-${IPERF3_SERVER:-127.0.0.1}}"
PORT="${2:-${IPERF3_PORT:-5201}}"
SECONDS="${3:-${IPERF3_DURATION_SECONDS:-5}}"

if command -v iperf3 >/dev/null 2>&1; then
  echo "Tip: if needed, start a server first on the target host: iperf3 -s -p $PORT"
  echo
  echo "+ iperf3 -c $SERVER -p $PORT -t $SECONDS"
  iperf3 -c "$SERVER" -p "$PORT" -t "$SECONDS" || true
else
  echo "iperf3 not found. Install it with your package manager to run throughput tests."
fi
