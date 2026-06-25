#!/usr/bin/env bash
# SSH service logs via journalctl

echo "=== journalctl -u ssh (last 30 lines) ==="
journalctl -u ssh --no-pager -n 30 2>/dev/null \
  || journalctl -u sshd --no-pager -n 30 2>/dev/null \
  || echo "(SSH journal not available)"
