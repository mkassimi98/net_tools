#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

NETWORK_CIDR="${1:-${NETWORK_CIDR:-}}"
if [[ -z "$NETWORK_CIDR" ]]; then
  NETWORK_CIDR="$(ip -o -4 addr show scope global | awk '{print $4}' | head -n1)"
fi

echo "Caution: only scan networks you own or are authorized to test."
echo
echo "+ nmap -sn $NETWORK_CIDR"
nmap -sn "$NETWORK_CIDR"
