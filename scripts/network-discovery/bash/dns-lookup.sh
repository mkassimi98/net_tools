#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

NAME="${1:-${DNS_LOOKUP_NAME:-example.com}}"

if command -v dig >/dev/null 2>&1; then
  echo "+ dig $NAME"
  dig "$NAME" || true
else
  echo "+ nslookup $NAME"
  nslookup "$NAME" || true
fi
