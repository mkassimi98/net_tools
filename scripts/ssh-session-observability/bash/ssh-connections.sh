#!/usr/bin/env bash
# Processes and connections on port 22

echo "=== ss -tnp (connections on :22) ==="
ss -tnp | grep ':22' || echo "(no active connections on :22)"

echo ""
echo "=== ps aux | grep sshd ==="
ps aux | grep '[s]shd'

echo ""
echo "=== sudo lsof -i :22 ==="
sudo lsof -i :22 2>/dev/null || echo "(lsof needs sudo or is not installed)"
