#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

TARGET_IP="${1:-${SCAN_TARGET_IP:-127.0.0.1}}"
PORTS="${2:-${SCAN_PORTS:-22,80,443,1883,8554,14550}}"

echo "Caution: only scan hosts you own or are authorized to test."
echo
echo "+ nmap -p $PORTS $TARGET_IP"
nmap -p "$PORTS" "$TARGET_IP"

echo
echo "+ nmap -sV $TARGET_IP"
nmap -sV "$TARGET_IP"
