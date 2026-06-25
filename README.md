# net_tools

Network diagnostics, discovery, and monitoring tools — paired bash and Python scripts
for interface inspection, connectivity troubleshooting, port/service analysis, network
discovery, traffic capture, SSH monitoring, and VPN verification.

**Author:** Mouhsine Kassimi Farhaoui <mouhsine98@gmail.com>  
**License:** MIT — see [LICENSE](LICENSE)

## Quick Start

Basic commands to get started:

```bash
# Show local interfaces and routing
./scripts/interface-inspection/python/interfaces.py
./scripts/interface-inspection/python/routes.py

# Test port state
./scripts/port-service-inspection/python/port_state.py

# Scan a subnet (requires local network/config)
./scripts/network-discovery/python/host_discovery.py
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443

# Monitor SSH sessions
./scripts/ssh-session-observability/python/active_sessions.py

# Check VPN connectivity
./scripts/vpn-remote-access/python/vpn_interface.py
```

## What's Included

| Category | Purpose | Scripts |
| --- | --- | --- |
| **interface-inspection** | IP addressing, routes, DNS, NetworkManager | 5 bash + 5 python |
| **connectivity-troubleshooting** | Ping, traceroute, ARP, failure diagnosis | 5 bash + 5 python |
| **port-service-inspection** | Listening ports, service status, firewall rules | 5 bash + 5 python |
| **network-discovery** | Host/port scanning, TCP/UDP probing, link state | 7 bash + 7 python |
| **ssh-session-observability** | Active sessions, login history, SSH logs | 4 bash + 4 python |
| **vpn-remote-access** | VPN interface detection, routes, reachability | 3 bash + 3 python |

Each category includes:
- **Bash scripts** — raw command output, suitable for scripting
- **Python scripts** — colorized dashboards with tables and legends

## Documentation

- **[Installation](docs/INSTALLATION.md)** — Requirements and setup by OS
- **[Configuration](docs/CONFIGURATION.md)** — Config hierarchy, file formats, examples
- **[Gallery](docs/GALLERY.md)** — Visual demo of all scripts (with GIFs)
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Common issues and solutions
- **[Security](docs/SECURITY.md)** — Authorization, responsible use, legal considerations

## Usage Examples

### Interface Inspection

```bash
./scripts/interface-inspection/python/interfaces.py     # Show all interfaces
./scripts/interface-inspection/python/routes.py         # Show routing table
./scripts/interface-inspection/python/dns.py            # Show DNS config
```

### Connectivity Troubleshooting

```bash
./scripts/connectivity-troubleshooting/python/ping_test.py
./scripts/connectivity-troubleshooting/python/dns_vs_network.py
./scripts/connectivity-troubleshooting/python/failure_cases.py
```

### Port and Service Inspection

```bash
./scripts/port-service-inspection/python/listening_services.py
./scripts/port-service-inspection/python/port_state.py
./scripts/port-service-inspection/python/ssh_logs.py    # (if SSH is running)
```

### Network Discovery

```bash
# Auto-detect local subnet
./scripts/network-discovery/python/host_discovery.py

# Scan specific target
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443
./scripts/network-discovery/python/tcp_udp_probe.py
```

### SSH Sessions

```bash
./scripts/ssh-session-observability/python/active_sessions.py
./scripts/ssh-session-observability/python/ssh_logs.py
./scripts/ssh-session-observability/python/ssh_connections.py
```

### VPN Verification

```bash
./scripts/vpn-remote-access/python/vpn_interface.py      # Detect VPN
./scripts/vpn-remote-access/python/vpn_routes.py         # Show VPN routes
./scripts/vpn-remote-access/python/vpn_reachability.py   # Test connectivity
```

## Configuration

Some categories require configuration. Copy and edit `local.env` for your environment:

```bash
# Port service inspection
cp scripts/port-service-inspection/config/local.env.example \
  scripts/port-service-inspection/config/local.env
nano scripts/port-service-inspection/config/local.env

# Network discovery
cp scripts/network-discovery/config/local.env.example \
  scripts/network-discovery/config/local.env
nano scripts/network-discovery/config/local.env
```

See [Configuration guide](docs/CONFIGURATION.md) for details and env variables.

## Requirements

**Minimal:**

- bash ≥ 4.0
- python3 ≥ 3.6
- Standard Linux utilities: `ip`, `ss`, `bash`, `python3`

**Additional by category:**

- Port inspection: `systemctl`, `lsof`, `iptables`
- Network discovery: `nmap`, `nc`, `curl`, `dig`, `arp-scan`, `ethtool`, `iw`
- SSH monitoring: `journalctl`, `loginctl`, `who`, `w`, `last`
- VPN: `ip`, `ping`, `nc`, WireGuard tools

See [Installation guide](docs/INSTALLATION.md) for OS-specific setup.

## Features

- **Dual mode** — bash for raw output, Python for styled dashboards
- **Config hierarchy** — defaults.env → local.env → env vars → CLI args
- **Auto-detection** — VPN interfaces, local subnet, DNS servers, wireless state
- **Color-coded output** — green for UP/success, red for DOWN/failure, yellow for warnings
- **Tables and legends** — easy to read and understand
- **Read-only** — never modifies system state (firewall, routes, services)
- **Privileged operations** — uses `sudo -n` (non-interactive) to avoid hanging

## Security and Authorization

**These tools perform active network testing.** Only use on authorized networks.

- **Network discovery** (nmap, arp-scan) — only scan networks you own or are authorized to test
- **Packet capture** (tcpdump, tshark) — legal restrictions apply; requires authorization
- **SSH monitoring** — respect privacy laws and user consent
- **Port scanning** — can trigger security alerts; use responsibly

See [Security guide](docs/SECURITY.md) for legal considerations and best practices.

## Troubleshooting

Common issues and solutions in [Troubleshooting guide](docs/TROUBLESHOOTING.md):

- Scripts hang waiting for password
- "command not found" errors
- Python import/syntax errors
- Permission denied
- Network discovery finds no hosts
- VPN interface not detected

Run with `sudo -v` first if scripts require elevated privileges:

```bash
sudo -v
./scripts/network-discovery/python/arp_scan.py
./scripts/port-service-inspection/python/firewall_rules.py
```

## Demo Gallery

See [Gallery](docs/GALLERY.md) for visual demos of all scripts (37 GIFs).

[![interfaces](captures/videos/python/S03_01_interfaces.gif)](docs/GALLERY.md#section-3-interface-inspection)

## Project Structure

```text
scripts/
├── interface-inspection/       # Section 3
│   ├── bash/                   # Plain bash scripts
│   └── python/                 # Styled Python scripts
├── connectivity-troubleshooting/ # Section 4
│   ├── bash/
│   └── python/
├── port-service-inspection/    # Section 5
│   ├── bash/
│   ├── python/
│   └── config/                 # defaults.env, local.env
├── network-discovery/          # Section 6
│   ├── bash/
│   ├── python/
│   └── config/
├── ssh-session-observability/  # Section 8
│   ├── bash/
│   ├── python/
│   └── config/
└── vpn-remote-access/          # Section 10
    ├── bash/
    ├── python/
    └── config/

docs/
├── INSTALLATION.md
├── CONFIGURATION.md
├── SECURITY.md
├── TROUBLESHOOTING.md
└── GALLERY.md

captures/
└── videos/python/              # Demo GIFs (37 total)
```

## Development

All scripts pass syntax validation:

```bash
# Bash validation
bash -n scripts/*/bash/*.sh

# Python validation
python3 -m py_compile scripts/*/python/*.py

# Make executable
find scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
```

## License

MIT License — Free to use, modify, and distribute. See [LICENSE](LICENSE) for details.

---

**Author:** Mouhsine Kassimi Farhaoui <mouhsine98@gmail.com>  
**Repository:** [net-tools](https://github.com/mkassimi/net-tools)
