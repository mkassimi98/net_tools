#!/usr/bin/env bash
# Active login sessions: who, w, and loginctl

echo "=== who ==="
who

echo ""
echo "=== w (users + activity) ==="
w

echo ""
echo "=== loginctl list-sessions ==="
loginctl list-sessions 2>/dev/null || echo "(loginctl not available)"
