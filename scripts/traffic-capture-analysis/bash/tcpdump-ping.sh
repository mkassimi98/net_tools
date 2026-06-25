#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

IFACE="${1:-${CAPTURE_INTERFACE:-any}}"
COUNT="${CAPTURE_PACKET_COUNT:-20}"
PING_TARGET="${2:-${PING_TARGET:-8.8.8.8}}"
PING_COUNT="${PING_COUNT:-4}"

echo "+ ping -c $PING_COUNT $PING_TARGET (background traffic generator)"
ping -c "$PING_COUNT" "$PING_TARGET" >/dev/null 2>&1 &

echo "+ tcpdump -n -i $IFACE -c $COUNT icmp"
tcpdump -n -i "$IFACE" -c "$COUNT" icmp || true
