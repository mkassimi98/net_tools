# Configuration Guide

## Overview

Configuration is optional for most categories. When needed, parameters are loaded in a
priority hierarchy:

1. **defaults.env** (in git, shared defaults)
2. **local.env** (git-ignored, local overrides)
3. External config file (via environment variable)
4. Environment variables
5. Command-line arguments (highest priority)

## Configuration Files

Each category with a `config/` folder follows the same pattern:

### defaults.env

Tracked in git, contains safe defaults suitable for most environments:

```bash
# Example: port-service-inspection/config/defaults.env
SERVICE_NAME=ssh
PORT_TARGET=22
PORT_STATE_OPEN_HOST=127.0.0.1
PORT_STATE_OPEN_PORT=22
...
```

### local.env

Not tracked in git (listed in `.gitignore`). Copy from `local.env.example` and customize:

```bash
# Create from example
cp scripts/port-service-inspection/config/local.env.example \
  scripts/port-service-inspection/config/local.env

# Edit with your values
nano scripts/port-service-inspection/config/local.env
```

Git will never commit changes to `local.env`, so it's safe for machine-specific settings.

## Loading Mechanism

### Bash Scripts

Bash scripts source `_config.sh` to load configuration:

```bash
source "$(dirname "$0")/_config.sh"
load_<category>_config   # e.g., load_ports_config
```

Then use variables like `$SERVICE_NAME`, `$PORT_TARGET`, etc.

### Python Scripts

Python scripts import `_config.py`:

```python
from _config import get_config
config = get_config()
service_name = config.get("SERVICE_NAME", "ssh")
```

## Using External Config

For complex setups or parameterized runs, load config from an external file via environment variable:

```bash
# Port service inspection
export PORTS_CONFIG=/tmp/my-ports.env
./scripts/port-service-inspection/python/port_state.py

# Network discovery
export DISCOVERY_CONFIG=/tmp/my-discovery.env
./scripts/network-discovery/python/port_scan.py

# VPN access
export VPN_CONFIG=/tmp/my-vpn.env
./scripts/vpn-remote-access/python/vpn_reachability.py
```

External config files have the same format as `defaults.env`:

```bash
# /tmp/my-discovery.env
SCAN_TARGET_IP=192.168.1.50
SCAN_PORTS=22,80,443,8080,1883,3000
TCP_PROBE_HOST=192.168.1.50
TCP_PROBE_PORT=22
```

## Categories and Their Config

### Connectivity Troubleshooting (Section 4)

**Optional.** If not configured, uses sensible defaults.

**File:** `scripts/connectivity-troubleshooting/config/defaults.env`

**Variables:**
- `PING_TARGET` — target for ping tests (default: `8.8.8.8`)
- `DNS_NAME` — domain for DNS testing (default: `google.com`)
- `TRACEROUTE_TARGET` — destination for traceroute (default: `8.8.8.8`)

**Example local.env:**

```bash
PING_TARGET=192.168.1.1
DNS_NAME=example.com
TRACEROUTE_TARGET=203.0.113.1
```

**Environment variable:** `CONNECTIVITY_CONFIG`

### Port Service Inspection (Section 5)

**Required** for meaningful testing (else uses defaults).

**File:** `scripts/port-service-inspection/config/defaults.env`

**Variables:**
- `SERVICE_NAME` — service to inspect (default: `ssh`)
- `PORT_TARGET` — port to test (default: `22`)
- `PORT_STATE_OPEN_HOST` / `PORT_STATE_OPEN_PORT` — a known open port
- `PORT_STATE_CLOSED_HOST` / `PORT_STATE_CLOSED_PORT` — a known closed port
- `PORT_STATE_DOWN_HOST` / `PORT_STATE_DOWN_PORT` — an unreachable host
- `FIREWALL_PORT` — port to inspect firewall rules for

**Example local.env:**

```bash
SERVICE_NAME=ssh
PORT_TARGET=22
PORT_STATE_OPEN_HOST=192.168.1.10
PORT_STATE_OPEN_PORT=22
PORT_STATE_CLOSED_HOST=192.168.1.10
PORT_STATE_CLOSED_PORT=9
PORT_STATE_DOWN_HOST=198.51.100.1
PORT_STATE_DOWN_PORT=80
FIREWALL_PORT=22
```

**Environment variable:** `PORTS_CONFIG`

### Network Discovery (Section 6)

**Required** for most functionality.

**File:** `scripts/network-discovery/config/defaults.env`

**Variables:**
- `NETWORK_CIDR` — subnet to scan (auto-detects if empty)
- `SCAN_TARGET_IP` — host for port scans
- `SCAN_PORTS` — comma-separated port list
- `TCP_PROBE_HOST` / `TCP_PROBE_PORT` — TCP test target
- `UDP_PROBE_HOST` / `UDP_PROBE_PORT` — UDP test target
- `HTTP_PROBE_URL` — URL for HTTP test
- `DNS_LOOKUP_NAME` — domain for DNS lookup
- `ETH_INTERFACE` — wired interface (auto-detect if empty)
- `WIFI_INTERFACE` — WiFi interface (auto-detect if empty)

**Example local.env:**

```bash
NETWORK_CIDR=192.168.1.0/24
SCAN_TARGET_IP=192.168.1.50
SCAN_PORTS=22,80,443,1883,3000,8080
TCP_PROBE_HOST=192.168.1.50
TCP_PROBE_PORT=22
UDP_PROBE_HOST=192.168.1.50
UDP_PROBE_PORT=5353
HTTP_PROBE_URL=http://192.168.1.50:8080
DNS_LOOKUP_NAME=example.com
ETH_INTERFACE=eth0
WIFI_INTERFACE=wlan0
```

**Environment variable:** `DISCOVERY_CONFIG`

**Auto-detection:** When `NETWORK_CIDR` is empty, scripts auto-detect the primary
network from `ip -o -4 addr show scope global`.

### VPN and Remote Access (Section 10)

**Optional.** Scripts auto-detect active VPN interfaces.

**File:** `scripts/vpn-remote-access/config/defaults.env`

**Variables:**
- `VPN_INTERFACE` — explicit VPN interface name (auto-detect if empty)
- `VPN_PING_TARGET` — reachability test target (default: `8.8.8.8`)
- `VPN_PING_COUNT` — number of pings (default: `4`)
- `VPN_SSH_TARGET` — SSH reachability test (optional)

**Example local.env:**

```bash
VPN_INTERFACE=tun0
VPN_PING_TARGET=10.8.0.1
VPN_PING_COUNT=4
VPN_SSH_TARGET=10.8.0.50
```

**Environment variable:** `VPN_CONFIG`

**Auto-detection:** Scripts detect tun*, wg*, and tailscale* interfaces automatically.

## Command-Line Overrides

Some scripts accept positional arguments to override config:

```bash
# Network discovery: CIDR and target
./scripts/network-discovery/python/host_discovery.py 192.168.1.0/24
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443

# VPN: interface and ping target
./scripts/vpn-remote-access/python/vpn_reachability.py tun0 10.8.0.1
```

Check each script's help or source code for supported arguments.

## Configuration Best Practices

1. **Use defaults.env for sharing** — defaults.env is tracked in git and suitable
   for sharing configurations across teams
2. **Use local.env for personal settings** — it's git-ignored and won't pollute repos
3. **Use env vars for scripting** — when automating or chaining scripts:
   ```bash
   export DISCOVERY_CONFIG=/tmp/prod.env
   for host in $(cat hosts.txt); do
     sed "s/TARGET/$host/" template.env > /tmp/temp.env
     DISCOVERY_CONFIG=/tmp/temp.env ./scripts/network-discovery/python/port_scan.py
   done
   ```
4. **Use CLI args for one-offs** — quick tests without creating config files

## Example Workflows

### Scan a specific subnet

```bash
# Setup
cp scripts/network-discovery/config/local.env.example \
  scripts/network-discovery/config/local.env
nano scripts/network-discovery/config/local.env
# Set: NETWORK_CIDR=192.168.1.0/24, SCAN_TARGET_IP=192.168.1.50

# Run
./scripts/network-discovery/python/host_discovery.py
./scripts/network-discovery/python/port_scan.py
```

### Test multiple targets

```bash
for target in 192.168.1.50 192.168.1.100 192.168.1.200; do
  export DISCOVERY_CONFIG=/tmp/target.env
  cat > /tmp/target.env << EOF
SCAN_TARGET_IP=$target
SCAN_PORTS=22,80,443,3000,8080
EOF
  echo "=== Testing $target ==="
  ./scripts/network-discovery/python/port_scan.py
done
```

### Monitor SSH activity

```bash
# No config needed, uses defaults
while true; do
  ./scripts/ssh-session-observability/python/active_sessions.py
  sleep 30
done
```

### Verify VPN connectivity

```bash
# Auto-detects VPN interface
./scripts/vpn-remote-access/python/vpn_interface.py
./scripts/vpn-remote-access/python/vpn_reachability.py

# Or with explicit config
export VPN_CONFIG=/tmp/vpn.env
./scripts/vpn-remote-access/python/vpn_reachability.py
```
