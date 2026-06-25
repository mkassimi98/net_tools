#!/usr/bin/env bash
# Test connectivity through the VPN: ping + optional SSH check

source "$(dirname "$0")/_config.sh"
load_vpn_config

VPN_IFACE="${1:-$VPN_INTERFACE}"
PING_TARGET="${2:-$VPN_PING_TARGET}"
COUNT="${VPN_PING_COUNT:-4}"

echo "=== Ping $PING_TARGET (count $COUNT) ==="
if [[ -n "$VPN_IFACE" ]]; then
  echo "    (forcing traffic out of $VPN_IFACE)"
  ping -c "$COUNT" -I "$VPN_IFACE" "$PING_TARGET" 2>/dev/null \
    || ping -c "$COUNT" "$PING_TARGET"
else
  ping -c "$COUNT" "$PING_TARGET"
fi

echo ""
echo "=== Route decision for $PING_TARGET ==="
ip route get "$PING_TARGET" 2>/dev/null || echo "(ip route get failed)"

if [[ -n "$VPN_SSH_TARGET" ]]; then
  echo ""
  echo "=== SSH reachability test to $VPN_SSH_TARGET ==="
  nc -vz -w 3 "$VPN_SSH_TARGET" 22 2>&1 || echo "(SSH port not reachable)"
fi
