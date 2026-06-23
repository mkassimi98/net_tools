#!/usr/bin/env bash
set -euo pipefail

if command -v resolvectl >/dev/null 2>&1; then
  echo "+ resolvectl status"
  resolvectl status
else
  echo "+ cat /etc/resolv.conf"
  cat /etc/resolv.conf
fi
