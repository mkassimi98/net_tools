<div align="center">

<pre>
███╗   ██╗███████╗████████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
████╗  ██║██╔════╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██╔██╗ ██║█████╗     ██║          ██║   ██║   ██║██║   ██║██║     ███████╗
██║╚██╗██║██╔══╝     ██║          ██║   ██║   ██║██║   ██║██║     ╚════██║
██║ ╚████║███████╗   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═╝  ╚═══╝╚══════╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
</pre>

<h3>Professional network diagnostics, discovery and monitoring tools for Linux-based systems</h3>

<p>
  <img src="https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Bash-4.0%2B-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Linux-black?style=for-the-badge&logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/License-GPL--3.0-orange?style=for-the-badge" />
</p>

<p>
  <img src="https://img.shields.io/badge/Mode-Read--Only-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Use-Authorized%20Networks%20Only-red?style=flat-square" />
</p>

</div>

---

# net_tools

`net_tools` is a curated collection of **Bash and Python utilities** for practical network inspection, troubleshooting, discovery and monitoring.

It is designed for engineering workshops, Linux-based integration environments, field diagnostics and technical demonstrations where engineers need to quickly understand the state of a networked system.

The repository is especially useful for showing, in a clear and visual way:

- which network interfaces are available,
- which interfaces are up or down,
- which IP addresses and MAC addresses are assigned,
- which routes and gateways are active,
- whether DNS and basic connectivity are working,
- which ports and services are exposed,
- which devices are visible on the local network,
- whether SSH sessions are active,
- whether VPN interfaces and routes are behaving as expected.

The repository combines two complementary execution modes:

| Mode | Purpose |
| --- | --- |
| **Bash scripts** | Raw, transparent command output for quick checks, scripting and low-level diagnostics |
| **Python scripts** | Styled, colorized dashboards with tables, legends and cleaner presentation output |

> These tools are intended for diagnostics, training and educational use. Network discovery, port scanning and packet inspection must only be used on systems and networks where you have explicit authorization.

---

## Table of Contents

- [Quick Start](#quick-start)
- [What's Included](#whats-included)
- [Documentation](#documentation)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Requirements](#requirements)
- [Features](#features)
- [Security and Authorization](#security-and-authorization)
- [Troubleshooting](#troubleshooting)
- [Demo Gallery](#demo-gallery)
- [Project Structure](#project-structure)
- [Development](#development)
- [License](#license)
- [Author](#author)

---

## Quick Start

Basic commands to get started:

```bash
# Show local interfaces and addressing
./scripts/interface-inspection/python/interfaces.py

# Show routing table, default gateway and metrics
./scripts/interface-inspection/python/routes.py

# Test port state
./scripts/port-service-inspection/python/port_state.py

# Discover hosts on the local network
./scripts/network-discovery/python/host_discovery.py

# Scan selected ports on a target host
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443

# Monitor active SSH sessions
./scripts/ssh-session-observability/python/active_sessions.py

# Check VPN interface state
./scripts/vpn-remote-access/python/vpn_interface.py
```

Some scripts may require additional Linux tools or elevated permissions depending on the operation being performed.

---

## What's Included

| Category | Purpose | Scripts |
| --- | --- | --- |
| **interface-inspection** | IP addressing, interfaces, routes, DNS and NetworkManager state | 5 bash + 5 python |
| **connectivity-troubleshooting** | Ping, traceroute, ARP, DNS checks and failure diagnosis | 5 bash + 5 python |
| **port-service-inspection** | Listening ports, service state, firewall rules and SSH logs | 5 bash + 5 python |
| **network-discovery** | Host discovery, port scanning, TCP/UDP probing and link state | 7 bash + 7 python |
| **ssh-session-observability** | Active SSH sessions, login history and SSH connection analysis | 4 bash + 4 python |
| **vpn-remote-access** | VPN interface detection, VPN routes and remote reachability | 3 bash + 3 python |

Each category includes:

- **Bash scripts** for direct, transparent and scriptable command output.
- **Python scripts** for colorized, workshop-friendly dashboards.
- **Configuration files** where target-specific values are needed.

---

## Documentation

The repository includes dedicated documentation pages:

| Document | Description |
| --- | --- |
| [Installation](docs/INSTALLATION.md) | Requirements and setup by operating system |
| [Configuration](docs/CONFIGURATION.md) | Configuration hierarchy, file formats and examples |
| [Gallery](docs/GALLERY.md) | Visual demo of all scripts using GIF captures |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and practical solutions |
| [Security](docs/SECURITY.md) | Authorization, responsible use and legal considerations |

---

## Usage Examples

### Interface Inspection

Use these scripts to inspect local network interfaces, IP addresses, MAC addresses, DNS configuration and routing state.

```bash
# Show all interfaces, IP addresses, MAC addresses and UP/DOWN state
./scripts/interface-inspection/python/interfaces.py

# Show routing table, default gateway and metrics
./scripts/interface-inspection/python/routes.py

# Show DNS configuration
./scripts/interface-inspection/python/dns.py
```

Typical workshop use case:

```bash
./scripts/interface-inspection/python/interfaces.py
./scripts/interface-inspection/python/routes.py
```

This is useful for explaining the difference between:

- interface availability,
- interface state,
- IP addressing,
- routing,
- default gateway selection,
- route metrics.

---

### Connectivity Troubleshooting

Use these scripts to verify whether the system can reach local and remote targets, resolve DNS names and identify basic connectivity issues.

```bash
# Basic connectivity test
./scripts/connectivity-troubleshooting/python/ping_test.py

# Compare DNS resolution against raw network connectivity
./scripts/connectivity-troubleshooting/python/dns_vs_network.py

# Show common failure cases
./scripts/connectivity-troubleshooting/python/failure_cases.py
```

These scripts are useful for separating problems such as:

- no physical or logical interface,
- no IP address,
- no default route,
- DNS failure,
- remote host unreachable,
- firewall or service-level blockage.

---

### Port and Service Inspection

Use these scripts to inspect local listening services, open ports, firewall rules and service status.

```bash
# Show listening services
./scripts/port-service-inspection/python/listening_services.py

# Test whether selected ports are open or closed
./scripts/port-service-inspection/python/port_state.py

# Show SSH logs if SSH is available
./scripts/port-service-inspection/python/ssh_logs.py
```

These scripts are useful when explaining:

- difference between a host being reachable and a service being available,
- TCP port state,
- listening sockets,
- local service exposure,
- firewall impact.

---

### Network Discovery

Use these scripts to discover hosts and services inside an authorized network.

```bash
# Auto-detect local subnet and discover hosts
./scripts/network-discovery/python/host_discovery.py

# Scan selected ports on a specific target
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443

# Run TCP/UDP probing
./scripts/network-discovery/python/tcp_udp_probe.py
```

Example:

```bash
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443,8080
```

> Only run discovery or scanning operations on networks where you have explicit authorization.

---

### SSH Session Observability

Use these scripts to inspect current and historical SSH access.

```bash
# Show currently active sessions
./scripts/ssh-session-observability/python/active_sessions.py

# Show SSH logs
./scripts/ssh-session-observability/python/ssh_logs.py

# Show SSH connection information
./scripts/ssh-session-observability/python/ssh_connections.py
```

These scripts are useful for explaining:

- active remote users,
- login history,
- SSH access visibility,
- basic auditability in Linux systems.

---

### VPN Verification

Use these scripts to detect VPN interfaces, inspect VPN-specific routes and verify reachability through the tunnel.

```bash
# Detect VPN interfaces
./scripts/vpn-remote-access/python/vpn_interface.py

# Show VPN routes
./scripts/vpn-remote-access/python/vpn_routes.py

# Test VPN reachability
./scripts/vpn-remote-access/python/vpn_reachability.py
```

These scripts are useful for workshops involving:

- WireGuard,
- OpenVPN,
- Tinc,
- remote access,
- overlay networks,
- routed VPN architectures.

---

## Configuration

Some categories require local configuration before execution.

Configuration follows this hierarchy:

```text
defaults.env -> local.env -> environment variables -> CLI arguments
```

To configure local values, copy the provided examples:

```bash
# Port service inspection
cp scripts/port-service-inspection/config/local.env.example \
   scripts/port-service-inspection/config/local.env

nano scripts/port-service-inspection/config/local.env
```

```bash
# Network discovery
cp scripts/network-discovery/config/local.env.example \
   scripts/network-discovery/config/local.env

nano scripts/network-discovery/config/local.env
```

See the [Configuration guide](docs/CONFIGURATION.md) for the full list of supported variables and examples.

---

## Requirements

### Minimal Requirements

| Requirement | Version |
| --- | --- |
| Bash | 4.0 or newer |
| Python | 3.6 or newer |
| Operating system | Linux |

The scripts rely on standard Linux networking utilities such as:

```text
ip
ss
bash
python3
ping
```

### Additional Tools by Category

| Category | Common tools |
| --- | --- |
| Port inspection | `systemctl`, `lsof`, `iptables` |
| Network discovery | `nmap`, `nc`, `curl`, `dig`, `arp-scan`, `ethtool`, `iw` |
| SSH monitoring | `journalctl`, `loginctl`, `who`, `w`, `last` |
| VPN verification | `ip`, `ping`, `nc`, WireGuard tools where applicable |

See the [Installation guide](docs/INSTALLATION.md) for OS-specific setup instructions.

---

## Features

- **Dual execution mode**: Bash for raw output, Python for styled dashboards.
- **Color-coded output**: green for UP/success, red for DOWN/failure and yellow for warnings.
- **Readable tables and legends**: designed for live demos, recordings and workshops.
- **Configuration hierarchy**: defaults, local overrides, environment variables and CLI arguments.
- **Auto-detection**: VPN interfaces, local subnet, DNS servers and wireless state.
- **Read-only behavior**: scripts are designed for diagnostics and do not modify firewall rules, routes or services.
- **Non-interactive sudo handling**: privileged checks use `sudo -n` where needed to avoid hanging.
- **Workshop-ready output**: useful for technical presentations and video captures.

---

## Security and Authorization

These tools perform diagnostics and, in some cases, active network testing.

Use them responsibly.

| Operation | Security consideration |
| --- | --- |
| Network discovery | Only scan networks you own or are authorized to test |
| Port scanning | Can trigger alerts in IDS, IPS or firewall systems |
| Packet capture | May expose sensitive data and may be legally restricted |
| SSH monitoring | Must respect privacy, policy and user consent |
| VPN diagnostics | May reveal internal routing or remote access information |

Before running active tests, make sure that:

- you own the target system or network,
- you have explicit authorization,
- you understand the potential impact,
- the test is appropriate for the environment.

See the [Security guide](docs/SECURITY.md) for responsible use guidelines.

---

## Troubleshooting

Common issues and solutions are documented in the [Troubleshooting guide](docs/TROUBLESHOOTING.md).

Typical issues include:

- scripts waiting for a password,
- missing Linux tools,
- Python syntax or import errors,
- permission denied errors,
- network discovery returning no hosts,
- VPN interface not detected,
- firewall or service visibility problems.

If a script requires elevated privileges, validate sudo first:

```bash
sudo -v
```

Then run the required script:

```bash
./scripts/network-discovery/python/arp_scan.py
./scripts/port-service-inspection/python/firewall_rules.py
```

---

## Demo Gallery

The repository includes a visual gallery with GIF captures of the Python scripts.

See the full gallery here:

[Demo Gallery](docs/GALLERY.md)

Example:

[![interfaces](captures/videos/python/S03_01_interfaces.gif)](docs/GALLERY.md#section-3-interface-inspection)

The gallery is useful for:

- README previews,
- workshop preparation,
- internal training material,
- quick tool selection,
- presentation recordings.

---

## Project Structure

```text
scripts/
├── interface-inspection/              # Section 3
│   ├── bash/                          # Plain bash scripts
│   └── python/                        # Styled Python scripts
│
├── connectivity-troubleshooting/      # Section 4
│   ├── bash/
│   └── python/
│
├── port-service-inspection/           # Section 5
│   ├── bash/
│   ├── python/
│   └── config/                        # defaults.env, local.env
│
├── network-discovery/                 # Section 6
│   ├── bash/
│   ├── python/
│   └── config/
│
├── ssh-session-observability/         # Section 8
│   ├── bash/
│   ├── python/
│   └── config/
│
└── vpn-remote-access/                 # Section 10
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
└── videos/python/                     # Demo GIFs
```

---

## Development

Useful validation commands:

```bash
# Validate Bash scripts
bash -n scripts/*/bash/*.sh
```

```bash
# Validate Python scripts
python3 -m py_compile scripts/*/python/*.py
```

```bash
# Make scripts executable
find scripts -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
```

---

## License

This project is licensed under the GNU General Public License v3.0 — see [LICENSE](LICENSE) for details.

---

## Author

**Mouhsine Kassimi Farhaoui** <mouhsine98@gmail.com>

Repository: [mkassimi98/net_tools](https://github.com/mkassimi98/net_tools)
