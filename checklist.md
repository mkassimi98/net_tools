# Workshop Material Checklist for Networking: Diagrams, RF, Connectivity, and Advanced Concepts

Checklist of material to capture/record for the networking workshop.

## 1. Base diagrams in Lucidchart

- [ ] Base diagram of the lab setup: laptop, switch/router, remote device, WAN interface, LAN interface, and Internet egress.
- [ ] Simple network diagram with interface names: `eth0`, `wlan0`, `wwan0`, `usb0`, `tun0`/`wg0`.
- [ ] Diagram with IP addressing: IP of each device, mask, gateway, and network/subnet.
- [ ] Diagram showing where traffic exits to the Internet.
- [ ] Diagram showing LAN vs WAN.
- [ ] Diagram showing one device sharing Internet with another.
- [ ] Basic UAV/GCS architecture diagram.
- [ ] Full architecture diagram: UAV + GCS + RF + 4G/5G + VPN + cloud + NTN.
- [ ] OSI model diagram applied to the workshop: RF/cable → link → IP → TCP/UDP → application.
- [ ] Encapsulation diagram: application → TCP/UDP → IP → Ethernet/WiFi/RF.
- [ ] Optional real photo of the physical setup to complement the diagrams.
- [ ] Optional real photo of integration equipment: Raspberry/Jetson/embedded PC/GCS/MultiSIM.

## 2. RF, antennas, and propagation

- [ ] Short photo/video explaining antenna types and their use cases.
- [ ] Photo/video showing antenna orientation and line of sight.
- [ ] Photo/video of an example with obstacles between transmitter and receiver.
- [ ] Line-of-sight diagram.
- [ ] Fresnel zone diagram.
- [ ] Interference diagram.
- [ ] RSSI vs SNR diagram.
- [ ] RF propagation diagram: distance loss, reflections, and multipath.
- [ ] Diagram comparing RF, WiFi, 4G/5G, and NTN/satellite.
- [ ] Photo of real antennas: RF, WiFi, 4G/5G, GNSS, or satellite if available.

## 3. Basic equipment check

- [ ] Short video showing `ip addr`, identifying interfaces, IPs, MACs, and UP/DOWN state.
- [ ] Short video showing `ip route`, identifying gateway, default route, and metrics.
- [ ] Capture of `ip route get 8.8.8.8` to show which interface traffic would exit through.
- [ ] Capture of the device's DNS configuration.
- [ ] Capture of `hostname -I` as a quick way to see IPs.
- [ ] Capture of `nmcli device status` if NetworkManager is in use.

## 4. Basic connectivity troubleshooting

- [ ] Short video with `ping` succeeding and `ping` failing.
- [ ] Video/capture telling apart a network failure from a DNS failure: `ping 8.8.8.8` vs `ping google.com`.
- [ ] Capture of `traceroute` or `mtr` to an external destination.
- [ ] Capture of `ip neigh` to explain ARP/network neighbors.
- [ ] Capture of a case with an IP but no gateway.
- [ ] Capture of a case with a gateway but no DNS.
- [ ] Capture of a case with a route but the service not responding.

## 5. Ports, services, and processes

- [ ] Short video showing `ss -tulpen` to see listening services and open ports.
- [ ] Capture of typical services: SSH, MQTT, RTSP, MAVLink, Grafana, InfluxDB, or similar.
- [ ] Capture of `systemctl status ssh` or another real service.
- [ ] Capture of the process bound to a port with `lsof` or `ss -tnp`.
- [ ] Capture telling apart an open port, a closed port, and a downed service.
- [ ] Capture of a firewall blocking a port, if it can be simulated.

## 6. Network discovery with useful tools

- [ ] Short video with `nmap -sn <network>/24` discovering hosts on a subnet.
- [ ] Video/capture with `nmap -p <ports> <ip>` showing open ports.
- [ ] Capture with `nmap -sV <ip>` identifying services.
- [ ] Capture of a TCP port test with `nc -vz`.
- [ ] Capture of a UDP port test with `nc -vzu`, if applicable.
- [ ] Capture of an HTTP/API service test with `curl -v`.
- [ ] Capture of DNS diagnostics with `dig` or `nslookup`.
- [ ] Capture of `arp-scan --localnet` discovering local devices.
- [ ] Capture of `ethtool eth0` showing Ethernet link state.
- [ ] Capture of `iw dev wlan0 link` to show WiFi state, if relevant.

## 7. Traffic capture and analysis

- [ ] Short video with `tcpdump` capturing traffic during a `ping`.
- [ ] Capture of `tcpdump` showing real TCP traffic.
- [ ] Capture of `tcpdump` showing real UDP traffic.
- [ ] Capture or short video of Wireshark/tshark for a more visual demo.
- [ ] Capture of an `iperf3` client/server test for throughput.
- [ ] Capture of `mtr` showing latency and loss per hop.
- [ ] Capture of `tracepath` to mention MTU/route, if desired.
- [ ] Capture of `iftop`, `nethogs`, or `bmon` showing real-time traffic.

## 8. SSH sessions and host observability

- [ ] Short video connecting via SSH from another device and watching the session appear.
- [ ] Capture of `who` showing connected users.
- [ ] Capture of `w` showing connected users and activity.
- [ ] Capture of `last` showing access history.
- [ ] Capture of `journalctl -u ssh` showing SSH service logs.
- [ ] Capture of `ss -tnp | grep ':22'` showing active SSH connections.
- [ ] Capture of `loginctl` showing active sessions.
- [ ] Capture of `ps aux | grep sshd` showing SSH processes.
- [ ] Capture of `sudo lsof -i :22` showing processes using the SSH port.

## 9. NAT, firewall, and Internet sharing

- [ ] Quick video of the `Internet Sharing` repo: WAN/LAN selection, apply, check connectivity, and cleanup.
- [ ] Capture of the `Internet Sharing` app.
- [ ] Capture of `sysctl net.ipv4.ip_forward`.
- [ ] Capture of normal `iptables` rules.
- [ ] Capture of NAT/MASQUERADE rules.
- [ ] Capture of the remote device's `ip route`.
- [ ] Capture of the remote device's `ping 1.1.1.1`.
- [ ] Capture of the remote device's `ping example.com`.
- [ ] Diagram explaining forwarding + NAT + remote gateway.
- [ ] Capture of cleanup/restoration, to show that no persistent changes remain.

## 10. VPN and remote access

- [ ] Short capture/video showing an active VPN interface: `tun0` or `wg0`.
- [ ] Capture of routes associated with the VPN.
- [ ] Capture of remote access to a device through the VPN.
- [ ] VPN-over-Internet/4G/5G overlay diagram.
- [ ] CGNAT diagram and why the VPN helps reach devices behind mobile networks.
- [ ] Capture of `ip addr` showing the VPN interface.
- [ ] Capture of `ip route` showing routes through the VPN.
- [ ] Capture of ping or SSH through the VPN.
- [ ] Capture comparing split tunnel vs full tunnel, if worth mentioning.

## 11. Topologies and final architecture

- [ ] Point-to-point diagram.
- [ ] Star diagram.
- [ ] Tree diagram.
- [ ] Mesh diagram.
- [ ] Hybrid UAV + GCS + RF + 4G/5G + VPN + cloud diagram.
- [ ] Diagram adding NTN/satellite as a complementary link.
- [ ] Final diagram with video, telemetry, commands, remote access, and monitoring.
- [ ] Single points of failure diagram.
- [ ] Redundancy/failover diagram.
- [ ] Diagram separating critical vs non-critical traffic.

## 12. Advanced concepts to represent visually

- [ ] MTU/MSS and fragmentation diagram.
- [ ] NAT, firewall, and port forwarding diagram.
- [ ] Bonding/failover/multi-link diagram.
- [ ] QoS/traffic prioritization diagram: commands/telemetry vs video.
- [ ] VLAN or logical traffic separation diagram, if worth mentioning.
- [ ] Multicast/broadcast/unicast diagram.
- [ ] Bridge vs router diagram.
- [ ] Policy routing diagram.
- [ ] CGNAT diagram.
- [ ] Capture of network monitoring: Grafana, logs, `iftop`, `nethogs`, `bmon`, or similar.

## 13. Backup captures in case demos fail

- [ ] Capture of every basic command working.
- [ ] Capture of a DNS failure example.
- [ ] Capture of a closed port or downed service example.
- [ ] Capture of an incorrect route example.
- [ ] Capture of an active VPN example.
- [ ] Capture of an applied NAT example.
- [ ] Capture of an `nmap` example discovering hosts and ports.
- [ ] Capture of a `tcpdump` example.
- [ ] Capture of an `iperf3` example.
- [ ] Capture of an active SSH example.
- [ ] Capture of SSH logs example.
- [ ] Capture of a downed/IP-less interface example.
- [ ] Capture of several active interfaces example.

## 14. Minimum required material

- [ ] General diagram in Lucidchart.
- [ ] Applied OSI diagram.
- [ ] UAV/GCS/RF/4G/5G/VPN/cloud/NTN architecture diagram.
- [ ] Antennas/RF/propagation.
- [ ] `ip addr` + interfaces.
- [ ] `ip route` + gateway + metrics.
- [ ] `ip route get`.
- [ ] `ping` succeeding/failing.
- [ ] DNS failure.
- [ ] `ss -tulpen`.
- [ ] `nmap`.
- [ ] `tcpdump`.
- [ ] `iperf3`.
- [ ] SSH/sessions/logs.
- [ ] Internet Sharing.
- [ ] VPN.
- [ ] Final architecture.
