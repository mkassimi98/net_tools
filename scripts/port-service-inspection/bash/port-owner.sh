#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_ports_config

PORT="${1:-${PORT_TARGET:-22}}"

echo "+ ss -tnp | grep ':$PORT'"
ss -tnp 2>/dev/null | grep ":$PORT" || echo "No matching socket found for port $PORT"

echo
echo "+ sudo lsof -i :$PORT"
sudo lsof -i ":$PORT" || true
