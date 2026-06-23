#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_ports_config

SERVICE_NAME="${1:-${SERVICE_NAME:-ssh}}"

echo "+ systemctl status $SERVICE_NAME --no-pager"
systemctl status "$SERVICE_NAME" --no-pager || true
