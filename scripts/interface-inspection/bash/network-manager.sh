#!/usr/bin/env bash
set -euo pipefail

if command -v nmcli >/dev/null 2>&1; then
  echo "+ nmcli device status"
  nmcli device status
else
  echo "nmcli not found - NetworkManager is not in use on this system."
fi
