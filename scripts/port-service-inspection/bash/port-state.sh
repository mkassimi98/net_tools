#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_ports_config

OPEN_HOST="${PORT_STATE_OPEN_HOST:-127.0.0.1}"
OPEN_PORT="${PORT_STATE_OPEN_PORT:-22}"
CLOSED_HOST="${PORT_STATE_CLOSED_HOST:-127.0.0.1}"
CLOSED_PORT="${PORT_STATE_CLOSED_PORT:-9}"
CLOSED_TIMEOUT="${PORT_STATE_CLOSED_TIMEOUT_SECONDS:-2}"
DOWN_HOST="${PORT_STATE_DOWN_HOST:-203.0.113.10}"
DOWN_PORT="${PORT_STATE_DOWN_PORT:-80}"
DOWN_TIMEOUT="${PORT_STATE_DOWN_TIMEOUT_SECONDS:-2}"

echo "+ nc -vz -w $CLOSED_TIMEOUT $OPEN_HOST $OPEN_PORT   # expected: open, service responding"
nc -vz -w "$CLOSED_TIMEOUT" "$OPEN_HOST" "$OPEN_PORT" || true

echo
echo "+ nc -vz -w $CLOSED_TIMEOUT $CLOSED_HOST $CLOSED_PORT   # expected: port closed, nothing listening"
nc -vz -w "$CLOSED_TIMEOUT" "$CLOSED_HOST" "$CLOSED_PORT" || true

echo
echo "+ nc -vz -w $DOWN_TIMEOUT $DOWN_HOST $DOWN_PORT   # expected: no response (filtered/unreachable)"
nc -vz -w "$DOWN_TIMEOUT" "$DOWN_HOST" "$DOWN_PORT" || true
