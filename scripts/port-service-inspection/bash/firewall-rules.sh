#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_ports_config

PORT="${1:-${FIREWALL_PORT:-22}}"

echo "+ sudo iptables -L -n -v"
sudo iptables -L -n -v 2>/dev/null || echo "Could not read iptables rules (need sudo / iptables not installed)."

echo
echo "Lines mentioning port $PORT:"
sudo iptables -L -n -v 2>/dev/null | grep -i ":$PORT" \
  || echo "No explicit rule mentioning port $PORT (likely falls under the default policy)."

echo
echo "To demo a live block during the talk, run these manually (not executed by this script):"
echo "  sudo iptables -A INPUT -p tcp --dport $PORT -j DROP   # block the port"
echo "  sudo iptables -D INPUT -p tcp --dport $PORT -j DROP   # remove the rule afterwards"
