#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

ETH_IFACE="${1:-${ETH_INTERFACE:-eth0}}"
WIFI_IFACE="${2:-${WIFI_INTERFACE:-wlan0}}"

echo "+ ethtool $ETH_IFACE"
ethtool "$ETH_IFACE" || true

echo
echo "+ iw dev $WIFI_IFACE link"
iw dev "$WIFI_IFACE" link || true
