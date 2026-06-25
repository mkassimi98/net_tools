# net_tools

Scripts and material used to capture/record the demos for the internal
networking workshop (RF, connectivity, NAT, VPN, UAV/GCS architecture).

## Structure

- `checklist.md` — full capture checklist for the workshop (translated to
  English), split into numbered sections.
- `scripts/<category>/bash/` — plain bash scripts, one per topic, that just
  run the real command(s) you'd type by hand (e.g. `ip addr`, `ip route`).
  Use these when you want the raw, unstyled command on screen.
- `scripts/<category>/python/` — same topics, but rendered as a colorized
  dashboard (table, legend, highlighted state) for a more polished
  recording. Each file pairs 1:1 with its bash counterpart by name
  (`bash/routes.sh` ↔ `python/routes.py`).

Each checklist section gets its own `<category>` folder under `scripts/`.
So far:

- `scripts/interface-inspection/` — checklist section 3 (basic equipment
  check): interfaces, routes, DNS, quick IP summary, NetworkManager status.
- `scripts/connectivity-troubleshooting/` — checklist section 4 (basic
  connectivity troubleshooting):
  - `ping` success vs failure
  - network failure vs DNS failure (`ping 8.8.8.8` vs `ping google.com`)
  - path tracing with `traceroute` or `mtr`
  - ARP/neighbors table with `ip neigh`
  - practical checks for:
    - IP present but no default gateway
    - gateway present but no DNS
    - route present but service not responding
- `scripts/port-service-inspection/` — checklist section 5 (ports, services,
  and processes):
  - listening sockets with `ss -tulpen`, annotated with well-known
    services (SSH/MQTT/RTSP/MAVLink/Grafana/InfluxDB)
  - `systemctl` status for a given service
  - process owning a port (`ss -tnp` / `lsof -i`)
  - open vs closed vs down/filtered port classification
  - current firewall rules for a port (read-only; the actual block/unblock
    commands are printed for you to run live, not auto-applied)
- `scripts/network-discovery/` — checklist section 6 (network discovery
  tools). **Caution:** only point these at networks/hosts you own or are
  authorized to test:
  - host discovery on a subnet (`nmap -sn`, auto-detects the local /24 if
    no CIDR is given)
  - port scan + service/version detection (`nmap -p` + `-sV`)
  - TCP vs UDP port probing (`nc -vz` / `nc -vzu`)
  - HTTP/API probing (`curl -v`), parsed into request/response/status
  - DNS lookups (`dig`/`nslookup`)
  - local device discovery (`arp-scan --localnet`, needs sudo)
  - physical link state (`ethtool` for wired, `iw dev ... link` for WiFi)
- `scripts/ssh-session-observability/` — checklist section 8 (SSH sessions and
  host observability):
  - active sessions: `who`, `w`, `loginctl list-sessions`
  - login history: `last`
  - SSH service logs via `journalctl -u ssh`, annotated ACCEPT / FAILED / CLOSE
  - processes and connections on port 22: `ss -tnp`, `ps aux | grep sshd`,
    `lsof -i :22`
- `scripts/vpn-remote-access/` — checklist section 10 (VPN and remote access):
  - VPN interface detection (tun*, wg*, tailscale*) with type, state, address
  - WireGuard peer details via `wg show`
  - routing table filtered to show VPN routes vs others, split-tunnel vs full
  - reachability test through the VPN: ping + route decision + SSH port probe
  - auto-detects active VPN interface; override via `VPN_INTERFACE` in config
- `scripts/traffic-capture-analysis/` — checklist section 7 (traffic capture
  and analysis). **Caution:** packet capture may require sudo/root and
  should only be performed on networks you are authorized to monitor:
  - `tcpdump` during `ping` (ICMP)
  - `tcpdump` for real TCP and UDP traffic
  - `tshark` text capture (or Wireshark GUI if preferred)
  - `iperf3` throughput test
  - `mtr` latency/loss per hop
  - `tracepath` route + MTU hints
  - real-time traffic viewers (`iftop` / `nethogs` / `bmon`)

## Usage

Run either version directly while recording your terminal:

```bash
./scripts/interface-inspection/bash/routes.sh      # plain `ip route` / `ip route get`
./scripts/interface-inspection/python/routes.py    # same data, styled dashboard

./scripts/connectivity-troubleshooting/bash/dns-vs-network.sh
./scripts/connectivity-troubleshooting/python/dns_vs_network.py

./scripts/connectivity-troubleshooting/bash/failure-cases.sh
./scripts/connectivity-troubleshooting/python/failure_cases.py

./scripts/port-service-inspection/bash/listening-services.sh
./scripts/port-service-inspection/python/listening_services.py

./scripts/port-service-inspection/bash/port-state.sh
./scripts/port-service-inspection/python/port_state.py

./scripts/network-discovery/bash/host-discovery.sh
./scripts/network-discovery/python/host_discovery.py

./scripts/network-discovery/bash/port-scan.sh 192.168.1.50 22,80,443
./scripts/network-discovery/python/port_scan.py 192.168.1.50 22,80,443

./scripts/ssh-session-observability/bash/active-sessions.sh
./scripts/ssh-session-observability/python/active_sessions.py

./scripts/ssh-session-observability/bash/ssh-logs.sh
./scripts/ssh-session-observability/python/ssh_logs.py

./scripts/vpn-remote-access/bash/vpn-interface.sh
./scripts/vpn-remote-access/python/vpn_interface.py

./scripts/vpn-remote-access/bash/vpn-reachability.sh
./scripts/vpn-remote-access/python/vpn_reachability.py

./scripts/traffic-capture-analysis/bash/tcpdump-ping.sh
./scripts/traffic-capture-analysis/python/tcpdump_ping.py

./scripts/traffic-capture-analysis/bash/iperf3-test.sh
./scripts/traffic-capture-analysis/python/iperf3_test.py
```

## Shared configuration (bash + python)

Categories that need parameters (target host, port, service name, etc.)
keep their own `config/` folder with the same loading convention:

- `scripts/connectivity-troubleshooting/config/`
- `scripts/port-service-inspection/config/`
- `scripts/network-discovery/config/`
- `scripts/traffic-capture-analysis/config/`
- `scripts/vpn-remote-access/config/`

Each has a `defaults.env` (tracked in git) and an optional `local.env`
(ignored by git, copy it from `local.env.example`). Both bash and Python
scripts in that category load values in this order:

1. `defaults.env`
2. `local.env` (if present)
3. an external config file, if pointed to by an env var
   (`CONNECTIVITY_CONFIG` for connectivity-troubleshooting,
   `PORTS_CONFIG` for port-service-inspection,
   `DISCOVERY_CONFIG` for network-discovery,
   `TRAFFIC_CONFIG` for traffic-capture-analysis,
   `VPN_CONFIG` for vpn-remote-access)
4. environment variables
5. CLI arguments (highest priority for positional targets/ports)

Create your local override from the example, e.g.:

```bash
cp scripts/port-service-inspection/config/local.env.example \
  scripts/port-service-inspection/config/local.env
```

## Recording recommendation

- Python demos from checklist sections 3 to 7 are configured for
  [VHS](https://github.com/charmbracelet/vhs). Validate the 30-entry inventory,
  render one GIF, or render the complete batch from the repository root:

  ```bash
  ./tools/vhs/render_python_videos.sh --validate
  ./tools/vhs/render_python_videos.sh --one S03_01_interfaces
  ./tools/vhs/render_python_videos.sh --all
  ```

  Generated recordings use names such as `S03_01_interfaces.gif` and are
  written to `captures/videos/python/`. Completed recordings include a hidden
  fingerprint of their command, Python source, config, and VHS settings.
  `--all` skips only up-to-date GIFs and regenerates missing or stale ones, so
  it can safely resume an interrupted batch after code/config changes. Pass
  `--force` to regenerate even current GIFs. VHS waits until each Python command
  finishes and then keeps its final output visible for two seconds. Commands
  time out after 10 minutes by default; override this with
  `VHS_WAIT_TIMEOUT=20m` when needed.
  Before a batch containing privileged tools (`tcpdump`, `tshark`, `arp-scan`,
  `ethtool`, `iftop`, or `nethogs`), refresh the sudo timestamp once with
  `sudo -v`.
- For diagrams, antennas, or anything that isn't a terminal, use a normal
  screen recorder (e.g. OBS) instead.
- For backup captures in case a live demo fails (checklist section 13),
  pipe any script's output to a file, e.g.
  `./scripts/interface-inspection/python/routes.py | tee captures/routes.txt`
  (ANSI colors are
  preserved in the file; strip them with `sed -r "s/\x1b\[[0-9;]*m//g"` if
  you need plain text).
