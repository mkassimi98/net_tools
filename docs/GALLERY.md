# Demo Gallery

Visual captures of each script category and its Python dashboards.

## Section 3: Interface Inspection

- **interfaces.gif** — Display network interfaces, IP addresses, MAC addresses, and UP/DOWN state
  ![interfaces](../captures/videos/python/S03_01_interfaces.gif)

- **routes.gif** — Show routing table, default gateway, and route decision for external targets
  ![routes](../captures/videos/python/S03_02_routes_and_route_get.gif)

- **dns.gif** — Display DNS configuration (systemd-resolved or /etc/resolv.conf)
  ![dns](../captures/videos/python/S03_03_dns_config.gif)

- **ip-summary.gif** — Quick IP summary with address classification
  ![ip-summary](../captures/videos/python/S03_04_hostname_ip_summary.gif)

- **network-manager.gif** — NetworkManager device status (if available)
  ![network-manager](../captures/videos/python/S03_05_networkmanager_status.gif)

## Section 4: Connectivity Troubleshooting

- **ping-success-vs-failure.gif** — Successful and failed ping attempts
  ![ping](../captures/videos/python/S04_01_ping_success_vs_failure.gif)

- **dns-vs-network.gif** — Distinguish DNS failure from network failure
  ![dns-vs-network](../captures/videos/python/S04_02_network_vs_dns_failure.gif)

- **traceroute-or-mtr.gif** — Path tracing with latency and loss per hop
  ![traceroute](../captures/videos/python/S04_03_traceroute_or_mtr.gif)

- **ip-neigh.gif** — ARP neighbors table
  ![arp](../captures/videos/python/S04_04_ip_neigh_arp_neighbors.gif)

- **failure-cases.gif** — IP without gateway, gateway without DNS, service not responding
  ![failure-cases](../captures/videos/python/S04_05_failure_cases_gateway_dns_service.gif)

## Section 5: Ports, Services, and Processes

- **listening-services.gif** — Services listening on ports with well-known service names
  ![listening-services](../captures/videos/python/S05_01_listening_services_ss_tulpen.gif)

- **service-status.gif** — systemctl service status with state coloring
  ![service-status](../captures/videos/python/S05_02_systemctl_service_status.gif)

- **port-owner.gif** — Find which process owns a given port
  ![port-owner](../captures/videos/python/S05_03_port_owner_ss_lsof.gif)

- **port-states.gif** — Classify ports as open, closed, or filtered/down
  ![port-states](../captures/videos/python/S05_04_open_closed_down_port_states.gif)

- **firewall-rules.gif** — Show iptables rules affecting a port (read-only)
  ![firewall](../captures/videos/python/S05_05_firewall_rules_for_port.gif)

## Section 6: Network Discovery

- **host-discovery.gif** — nmap discover hosts on a subnet
  ![host-discovery](../captures/videos/python/S06_01_nmap_host_discovery.gif)

- **port-scan.gif** — nmap port scan with service/version detection
  ![port-scan](../captures/videos/python/S06_02_nmap_port_scan_service_version.gif)

- **tcp-udp-probe.gif** — Test TCP and UDP port reachability
  ![tcp-udp](../captures/videos/python/S06_03_tcp_udp_probe.gif)

- **http-probe.gif** — HTTP/API test with curl and response parsing
  ![http](../captures/videos/python/S06_04_http_api_probe_curl.gif)

- **dns-lookup.gif** — DNS resolution via dig or nslookup
  ![dns-lookup](../captures/videos/python/S06_05_dns_lookup_dig_nslookup.gif)

- **arp-scan.gif** — Local network device discovery via ARP
  ![arp-scan](../captures/videos/python/S06_06_arp_scan_localnet.gif)

- **link-state.gif** — Ethernet and WiFi link state inspection
  ![link-state](../captures/videos/python/S06_07_eth_wlan_link_state.gif)

## Section 7: Traffic Capture and Analysis

- **tcpdump-ping.gif** — Capture ICMP traffic during ping
  ![tcpdump-ping](../captures/videos/python/S07_01_tcpdump_icmp_during_ping.gif)

- **tcpdump-tcp.gif** — Capture TCP traffic
  ![tcpdump-tcp](../captures/videos/python/S07_02_tcpdump_tcp_traffic.gif)

- **tcpdump-udp.gif** — Capture UDP traffic
  ![tcpdump-udp](../captures/videos/python/S07_03_tcpdump_udp_traffic.gif)

- **tshark.gif** — Text-based packet capture with tshark
  ![tshark](../captures/videos/python/S07_04_tshark_or_wireshark_capture.gif)

- **iperf3.gif** — Throughput test between client and server
  ![iperf3](../captures/videos/python/S07_05_iperf3_throughput_test.gif)

- **mtr.gif** — Latency and packet loss per hop
  ![mtr](../captures/videos/python/S07_06_mtr_latency_loss.gif)

- **tracepath.gif** — Path trace with MTU hints
  ![tracepath](../captures/videos/python/S07_07_tracepath_mtu_route_hints.gif)

- **realtime-traffic.gif** — Real-time traffic analysis with iftop, nethogs, or bmon
  ![realtime](../captures/videos/python/S07_08_realtime_traffic_iftop_nethogs_bmon.gif)

## Section 8: SSH Sessions and Host Observability

- **active-sessions.gif** — Show who is logged in and session activity
  ![active-sessions](../captures/videos/python/S08_01_active_sessions.gif)

- **session-history.gif** — Login history with session duration
  ![history](../captures/videos/python/S08_02_session_history.gif)

- **ssh-logs.gif** — SSH service logs with ACCEPT/FAILED/CLOSE annotations
  ![ssh-logs](../captures/videos/python/S08_03_ssh_logs.gif)

- **ssh-connections.gif** — Active SSH connections and sshd processes
  ![ssh-connections](../captures/videos/python/S08_04_ssh_connections.gif)

## Section 10: VPN and Remote Access

- **vpn-interface.gif** — Active VPN interfaces (tun, wg, tailscale) with addresses and peers
  ![vpn-interface](../captures/videos/python/S10_01_vpn_interface.gif)

- **vpn-routes.gif** — Routing table split between VPN and non-VPN routes
  ![vpn-routes](../captures/videos/python/S10_02_vpn_routes.gif)

- **vpn-reachability.gif** — Test connectivity through the VPN with ping and SSH probe
  ![vpn-reachability](../captures/videos/python/S10_03_vpn_reachability.gif)
