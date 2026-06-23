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
```

## Shared configuration (bash + python)

Categories that need parameters (target host, port, service name, etc.)
keep their own `config/` folder with the same loading convention:

- `scripts/connectivity-troubleshooting/config/`
- `scripts/port-service-inspection/config/`
- `scripts/network-discovery/config/`

Each has a `defaults.env` (tracked in git) and an optional `local.env`
(ignored by git, copy it from `local.env.example`). Both bash and Python
scripts in that category load values in this order:

1. `defaults.env`
2. `local.env` (if present)
3. an external config file, if pointed to by an env var
   (`CONNECTIVITY_CONFIG` for connectivity-troubleshooting,
   `PORTS_CONFIG` for port-service-inspection,
   `DISCOVERY_CONFIG` for network-discovery)
4. environment variables
5. CLI arguments (highest priority for positional targets/ports)

Create your local override from the example, e.g.:

```bash
cp scripts/port-service-inspection/config/local.env.example \
  scripts/port-service-inspection/config/local.env
```

## Recording recommendation

- For terminal-only demos (any script here), use
  [asciinema](https://asciinema.org/) (`asciinema rec demo.cast`). It only
  captures the terminal (small files, no editing needed, exports to
  GIF/MP4 with `agg` if you need a video file for slides).
- For diagrams, antennas, or anything that isn't a terminal, use a normal
  screen recorder (e.g. OBS) instead.
- For backup captures in case a live demo fails (checklist section 13),
  pipe any script's output to a file, e.g.
  `./scripts/interface-inspection/python/routes.py | tee captures/routes.txt`
  (ANSI colors are
  preserved in the file; strip them with `sed -r "s/\x1b\[[0-9;]*m//g"` if
  you need plain text).
