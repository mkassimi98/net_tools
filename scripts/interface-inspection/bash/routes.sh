#!/usr/bin/env bash
set -euo pipefail

echo "+ ip route"
ip route

echo
echo "+ ip route get 8.8.8.8"
ip route get 8.8.8.8
