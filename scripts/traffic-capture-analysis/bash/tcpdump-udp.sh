#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

IFACE="${1:-${CAPTURE_INTERFACE:-any}}"
HOST="${2:-${UDP_TARGET_HOST:-8.8.8.8}}"
PORT="${3:-${UDP_TARGET_PORT:-53}}"
COUNT="${CAPTURE_PACKET_COUNT:-20}"

echo "+ tcpdump -n -i $IFACE -c $COUNT udp and host $HOST and port $PORT"
tcpdump -n -i "$IFACE" -c "$COUNT" "udp and host $HOST and port $PORT" || true
