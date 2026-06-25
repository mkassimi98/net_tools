#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_traffic_config

IFACE="${1:-${TSHARK_INTERFACE:-any}}"
COUNT="${TSHARK_PACKET_COUNT:-20}"

if command -v tshark >/dev/null 2>&1; then
  echo "+ tshark -i $IFACE -c $COUNT"
  tshark -i "$IFACE" -c "$COUNT" || true
else
  echo "tshark not found. Use Wireshark GUI for visual analysis if preferred."
fi
