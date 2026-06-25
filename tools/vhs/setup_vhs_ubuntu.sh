#!/usr/bin/env bash
set -euo pipefail

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ttyd >/dev/null 2>&1; then
  echo "Installing ffmpeg and ttyd (requires sudo)..."
  sudo apt update
  sudo apt install -y ffmpeg ttyd
fi

if ! command -v vhs >/dev/null 2>&1; then
  if command -v go >/dev/null 2>&1; then
    echo "Installing VHS via go install..."
    go install github.com/charmbracelet/vhs@latest
    if [[ -d "$HOME/go/bin" && ":$PATH:" != *":$HOME/go/bin:"* ]]; then
      echo
      echo "Add this to your shell rc (~/.zshrc) then reload shell:"
      echo "  export PATH=\"$HOME/go/bin:\$PATH\""
    fi
  else
    echo "vhs not found and go is not installed."
    echo "Install Go first or install VHS manually from: https://github.com/charmbracelet/vhs"
    exit 1
  fi
fi

echo
command -v vhs >/dev/null 2>&1 && echo "vhs:    $(command -v vhs)"
command -v ttyd >/dev/null 2>&1 && echo "ttyd:   $(command -v ttyd)"
command -v ffmpeg >/dev/null 2>&1 && echo "ffmpeg: $(command -v ffmpeg)"

echo
printf '%s\n' "VHS setup complete."
