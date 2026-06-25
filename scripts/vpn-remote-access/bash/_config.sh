#!/usr/bin/env bash
# Shared config loader for vpn-remote-access scripts.
# Source this file, then call load_vpn_config.

load_vpn_config() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local config_dir="$script_dir/../config"

  set -a
  # shellcheck source=/dev/null
  [[ -f "$config_dir/defaults.env" ]] && source "$config_dir/defaults.env"
  [[ -f "$config_dir/local.env"    ]] && source "$config_dir/local.env"
  [[ -n "$VPN_CONFIG" && -f "$VPN_CONFIG" ]] && source "$VPN_CONFIG"
  set +a
}
