#!/usr/bin/env bash
# Show VPN interfaces (tun*, wg*) and their addresses

source "$(dirname "$0")/_config.sh"
load_vpn_config

VPN_IFACE="${1:-$VPN_INTERFACE}"

echo "=== VPN interfaces detected ==="
ip addr show | grep -E "^[0-9]+:\s+(tun|wg)" -A 4 || echo "(no tun*/wg* interfaces found)"

if [[ -n "$VPN_IFACE" ]]; then
  echo ""
  echo "=== ip addr show $VPN_IFACE ==="
  ip addr show "$VPN_IFACE" 2>/dev/null || echo "(interface $VPN_IFACE not found)"
fi

echo ""
echo "=== WireGuard status (if applicable) ==="
sudo wg show 2>/dev/null || echo "(wg not installed or no WireGuard interfaces active)"
