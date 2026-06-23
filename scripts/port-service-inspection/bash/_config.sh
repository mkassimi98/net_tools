#!/usr/bin/env bash

load_ports_config() {
  local script_dir config_dir cfg

  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  config_dir="${script_dir%/bash}/config"

  for cfg in "$config_dir/defaults.env" "$config_dir/local.env"; do
    if [[ -f "$cfg" ]]; then
      set -a
      # shellcheck disable=SC1090
      source "$cfg"
      set +a
    fi
  done

  if [[ -n "${PORTS_CONFIG:-}" && -f "${PORTS_CONFIG}" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${PORTS_CONFIG}"
    set +a
  fi
}
