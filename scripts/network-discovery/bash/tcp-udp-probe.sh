#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

TCP_HOST="${TCP_PROBE_HOST:-127.0.0.1}"
TCP_PORT="${TCP_PROBE_PORT:-22}"
TCP_TIMEOUT="${TCP_PROBE_TIMEOUT_SECONDS:-2}"
UDP_HOST="${UDP_PROBE_HOST:-127.0.0.1}"
UDP_PORT="${UDP_PROBE_PORT:-14550}"
UDP_TIMEOUT="${UDP_PROBE_TIMEOUT_SECONDS:-2}"

echo "+ nc -vz -w $TCP_TIMEOUT $TCP_HOST $TCP_PORT"
nc -vz -w "$TCP_TIMEOUT" "$TCP_HOST" "$TCP_PORT" || true

echo
echo "+ nc -vzu -w $UDP_TIMEOUT $UDP_HOST $UDP_PORT"
nc -vzu -w "$UDP_TIMEOUT" "$UDP_HOST" "$UDP_PORT" || true
