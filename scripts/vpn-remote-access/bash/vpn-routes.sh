#!/usr/bin/env bash
# Show routing table entries associated with VPN interfaces

source "$(dirname "$0")/_config.sh"
load_vpn_config

VPN_IFACE="${1:-$VPN_INTERFACE}"

echo "=== Full routing table ==="
ip route show

echo ""
echo "=== Routes via VPN (tun*/wg* interfaces) ==="
ip route show | grep -E "\b(tun|wg)[0-9]" || echo "(no VPN routes found)"

if [[ -n "$VPN_IFACE" ]]; then
  echo ""
  echo "=== Routes via $VPN_IFACE ==="
  ip route show dev "$VPN_IFACE" 2>/dev/null || echo "(interface $VPN_IFACE not found)"
fi
