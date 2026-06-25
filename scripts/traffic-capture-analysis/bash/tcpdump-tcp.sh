#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

IFACE="${1:-${CAPTURE_INTERFACE:-any}}"
HOST="${2:-${TCP_TARGET_HOST:-example.com}}"
PORT="${3:-${TCP_TARGET_PORT:-443}}"
COUNT="${CAPTURE_PACKET_COUNT:-20}"

echo "+ tcpdump -n -i $IFACE -c $COUNT tcp and host $HOST and port $PORT"
tcpdump -n -i "$IFACE" -c "$COUNT" "tcp and host $HOST and port $PORT" || true
