#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"
load_discovery_config

URL="${1:-${HTTP_PROBE_URL:-http://example.com}}"

echo "+ curl -v $URL"
curl -v "$URL" || true
