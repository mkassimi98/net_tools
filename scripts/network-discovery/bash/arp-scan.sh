#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

echo "Caution: only scan networks you own or are authorized to test."
echo
echo "+ sudo arp-scan --localnet"
sudo arp-scan --localnet || true
