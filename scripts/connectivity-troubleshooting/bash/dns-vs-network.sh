#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_connectivity_config

NETWORK_TARGET="${1:-${DNS_NETWORK_TARGET:-8.8.8.8}}"
DNS_TARGET="${2:-${DNS_NAME_TARGET:-google.com}}"
COUNT="${COUNT:-${PING_COUNT:-4}}"

echo "+ ping -c $COUNT $NETWORK_TARGET"
ping -c "$COUNT" "$NETWORK_TARGET" || true

echo
echo "+ ping -c $COUNT $DNS_TARGET"
ping -c "$COUNT" "$DNS_TARGET" || true
