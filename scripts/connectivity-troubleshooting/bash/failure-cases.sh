#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_connectivity_config

SERVICE_HOST="${1:-${SERVICE_HOST:-example.com}}"
SERVICE_PORT="${2:-${SERVICE_PORT:-443}}"
SERVICE_TIMEOUT_SECONDS="${SERVICE_TIMEOUT_SECONDS:-3}"

echo "+ ip -4 addr show scope global"
ip -4 addr show scope global || true

echo
echo "+ ip route show default"
ip route show default || true

echo
echo "+ cat /etc/resolv.conf"
cat /etc/resolv.conf || true

echo
echo "+ service probe: $SERVICE_HOST:$SERVICE_PORT"
if command -v nc >/dev/null 2>&1; then
  nc -vz -w "$SERVICE_TIMEOUT_SECONDS" "$SERVICE_HOST" "$SERVICE_PORT" || true
else
  timeout "$SERVICE_TIMEOUT_SECONDS" bash -c "cat < /dev/null > /dev/tcp/$SERVICE_HOST/$SERVICE_PORT" && \
    echo "TCP connect succeeded" || echo "TCP connect failed"
fi

global_ipv4="$(ip -o -4 addr show scope global | wc -l)"
default_route="$(ip route show default | sed '/^$/d' | wc -l)"
dns_count="$(grep -E '^\s*nameserver\s+' /etc/resolv.conf | wc -l)"

echo
echo "=== Quick diagnosis hints ==="
if [[ "$global_ipv4" -gt 0 && "$default_route" -eq 0 ]]; then
  echo "Case detected: IP present but no default gateway."
else
  echo "Case not detected: IP present but no default gateway."
fi

if [[ "$default_route" -gt 0 && "$dns_count" -eq 0 ]]; then
  echo "Case detected: default gateway present but no DNS configured."
else
  echo "Case not detected: default gateway present but no DNS configured."
fi

echo "Service probe helps show the case: route exists but service is not responding."
