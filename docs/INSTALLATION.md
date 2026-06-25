# Installation and Requirements

## Core Requirements

All scripts require:

- **bash** ≥ 4.0
- **python3** ≥ 3.6
- Standard Linux utilities: `ip`, `ss`, `grep`, `sed`, `awk`

## Tools by Category

### Interface Inspection (Section 3)
- `ip` — always available on modern Linux
- `hostname` — standard utility
- `nmcli` — optional, part of NetworkManager
- `resolvectl` — optional, part of systemd-resolved

### Connectivity Troubleshooting (Section 4)
- `ping` — standard utility
- `traceroute` or `mtr` — may need to install
- `nc` — netcat, often pre-installed
- `arp` — part of net-tools package

### Port and Service Inspection (Section 5)
- `ss` — standard utility (replaces netstat)
- `systemctl` — part of systemd
- `lsof` — often pre-installed, may need sudo
- `iptables` — standard on Linux, read-only access
- `sudo` — for privileged operations

### Network Discovery (Section 6)
- `nmap` — requires installation
- `nc` — netcat
- `curl` — often pre-installed
- `dig` or `nslookup` — part of bind-utils
- `arp-scan` — requires installation and sudo
- `ethtool` — requires installation and sudo
- `iw` — wireless tools, requires installation

### SSH Sessions and Observability (Section 8)
- `who`, `w`, `last` — standard utilities
- `journalctl` — part of systemd
- `loginctl` — part of systemd
- `ps`, `grep` — standard utilities
- `lsof` — optional, for process/port details

### VPN and Remote Access (Section 10)
- `ip` — standard utility
- `ping` — standard utility
- `nc` — netcat
- `wg` — WireGuard CLI (optional, for WireGuard details)
- `sudo` — for privileged operations

## Installation by Distribution

### Debian/Ubuntu

```bash
# Core utilities (usually pre-installed)
sudo apt-get update
sudo apt-get install -y bash python3 curl iputils-ping

# Additional tools
sudo apt-get install -y \
  nmap \
  arp-scan \
  iw \
  dnsutils \
  mtr \
  net-tools \
  ethtool \
  lsof \
  wireguard-tools
```

### Fedora/RHEL/CentOS

```bash
sudo dnf install -y \
  bash \
  python3 \
  curl \
  iputils \
  nmap \
  arp-scan \
  iw \
  bind-utils \
  mtr \
  net-tools \
  ethtool \
  lsof \
  wireguard-tools
```

### Arch Linux

```bash
sudo pacman -S \
  nmap \
  arp-scan \
  iw \
  bind-tools \
  mtr \
  net-tools \
  ethtool \
  lsof \
  wireguard-tools
```

### macOS (via Homebrew)

```bash
brew install \
  nmap \
  arp-scan \
  curl \
  bind \
  mtr \
  ethtool \
  lsof \
  wireguard-tools
```

Note: Some tools (arp-scan, ethtool, iw) may have limited functionality on macOS.

## Sudo Configuration

Some scripts use `sudo -n` (non-interactive sudo) to avoid hanging. Ensure sudo
credentials are available:

```bash
# Refresh sudo timestamp
sudo -v

# Or test non-interactive sudo
sudo -n whoami
```

If scripts hang, run `sudo -v` before executing them.

## Verification

Check that required tools are available:

```bash
# Core tools
which ip ss bash python3
which ping curl dig

# Optional tools (check which are available)
which nmap arp-scan ethtool iw lsof systemctl journalctl loginctl
which mtr nc traceroute

# Python modules
python3 -c "import json, socket, subprocess; print('OK')"
```

## Development Setup

For development or running scripts directly:

```bash
cd /path/to/net_tools
git clone https://github.com/mkassimi/net-tools.git
cd net-tools

# Verify bash scripts
for f in scripts/*/bash/*.sh; do bash -n "$f"; done

# Verify Python scripts
for f in scripts/*/python/*.py; do python3 -m py_compile "$f"; done

# Make scripts executable
find scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
```

## Troubleshooting Installation

### "command not found" errors

- **nmap, arp-scan, iw, ethtool**: Check your distribution's package manager
- **mtr**: May be named `mtr-packet` on some systems
- **dig**: Often part of `bind-utils` (Fedora) or `dnsutils` (Debian)

### Missing Python modules

All scripts use only Python standard library (json, socket, subprocess, re, pathlib, datetime, shutil). No pip install needed.

### Sudo password prompts

Pre-cache sudo credentials before running scripts:

```bash
sudo -v
```

Then run scripts. They will use cached credentials with `sudo -n`.
