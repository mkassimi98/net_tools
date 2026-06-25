# Security and Authorization

## Authorized Use Only

These tools perform network diagnostics, discovery, and monitoring that may be
restricted or illegal if used without proper authorization.

**All use must be authorized by the network/system owner.**

## By Category

### Interface Inspection (Section 3)

**Safe.** Only reads local interface configuration. No network activity.

- Can be run on any system without restriction
- Reads from `/proc/net`, `ip`, `systemctl`, DNS config
- No elevated privileges required (mostly)

### Connectivity Troubleshooting (Section 4)

**Generally safe for authorized networks.**

Performs ping, traceroute, ARP lookups on specified targets.

- Only test against **networks and hosts you own or have permission to test**
- `ping` may be blocked by some firewalls or networks
- `traceroute` reveals network topology; some networks block this
- `arp` traffic is local-link only, no WAN impact

### Port and Service Inspection (Section 5)

**Safe on local system. Remote testing requires authorization.**

- `ss` and `systemctl` inspect local services only ✓
- `iptables` reads firewall rules (read-only, no changes made) ✓
- Testing **remote ports** requires authorization from network owner

### Network Discovery (Section 6)

**Requires explicit authorization for all targets.**

These tools perform active scanning and probing:

- **nmap** — Port scanning, OS detection, service discovery
  - Can trigger IDS/IPS alerts on some networks
  - Illegal without authorization in many jurisdictions
  - Use only on authorized targets
  
- **arp-scan** — Local network device enumeration
  - Only works on local link, cannot reach remote networks
  - Generates ARP traffic that administrators may monitor
  - Requires sudo/elevated privileges
  
- **nc/netcat** — Direct port probing
  - May be detected as port scanning by IDS/IPS
  - Use on authorized networks only
  
- **curl, dig** — HTTP and DNS queries
  - Generally safe, but reveals your probing targets in logs
  - Use on systems you have permission to test

**Authorization checklist:**
- [ ] I own this network/host
- [ ] OR I have written permission from the owner
- [ ] OR This is a CTF/lab environment designed for this
- [ ] I will not probe external networks without authorization

### SSH Session Monitoring (Section 8)

**Safe on local system. Be respectful of privacy.**

- `who`, `w`, `last` — session monitoring (local only)
- `journalctl` — system logs (requires privileges to see other users' activity)
- `loginctl` — system session info
- `ss`, `ps`, `lsof` — process inspection (local system only)

**Privacy considerations:**
- Monitoring other users' sessions may violate privacy laws
- Use in authorized contexts (system administration, incident response)
- Respect user privacy and data protection regulations (GDPR, CCPA, etc.)

### VPN and Remote Access (Section 10)

**Safe if you own/manage the VPN.**

- `ip`, `ping` — interface and connectivity inspection
- `wg show` — WireGuard peer details (requires elevated privileges)
- No active probing by default

**Authorization requirements:**
- You must be authorized to inspect the VPN
- Do not inspect third-party VPN services without permission

### Traffic Capture (Section 7)

**Requires explicit authorization. May be illegal if misused.**

Packet capture can reveal sensitive data (passwords, APIs, private messages).

- **tcpdump** — Packet capture (requires root/sudo)
  - Captures all network traffic, including encrypted protocols
  - Illegal to use without authorization in most jurisdictions
  - Use only on networks you own or have explicit permission to monitor
  - Respect encryption and privacy regulations
  
- **tshark/Wireshark** — Packet analysis
  - Same considerations as tcpdump
  - Extremely powerful for deep packet inspection
  - Use responsibly and legally only

- **iperf3** — Throughput testing
  - Generally safe (tests own network/hosts)
  - Can impact network performance if used excessively
  - Coordinate with network administrators

**Packet capture authorization checklist:**
- [ ] I own/manage this network
- [ ] OR I have written permission to capture traffic
- [ ] OR This is a lab/test environment designed for training
- [ ] I understand packet capture may reveal sensitive data
- [ ] I will handle captured data responsibly

## Responsible Disclosure

If you discover security vulnerabilities while using these tools:

1. **Do not exploit the vulnerability** beyond confirming it exists
2. **Do not disclose publicly** until the owner has time to fix it
3. **Notify the owner privately** via secure channels
4. **Follow responsible disclosure practices** (30-90 day grace period typical)

## Legal Considerations

Network scanning and traffic analysis laws vary by jurisdiction:

- **United States** — Computer Fraud and Abuse Act (CFAA) prohibits unauthorized
  access and testing. Even on your own network, be cautious with shared infrastructure.

- **European Union** — GDPR and local laws restrict data collection and monitoring.
  Packet capture may violate privacy regulations.

- **Other jurisdictions** — Laws vary. Some countries have stricter regulations on
  network scanning and traffic interception.

**Always:**
- Get written authorization before testing networks you don't own
- Know your local laws and regulations
- Document your authorization (scope, dates, approvals)
- Use these tools professionally and ethically

## Recommended Use Cases

### Authorized (safe to use these tools)

✓ Your own home network  
✓ Company network you administer  
✓ Lab/test environment for training  
✓ CTF (Capture The Flag) competitions  
✓ Authorized penetration testing (with signed agreement)  
✓ Incident response on systems you manage  
✓ Network troubleshooting for systems you support  

### Unauthorized (do not use)

✗ Networks you don't own or manage  
✗ Competitors' networks  
✗ Public/shared networks without admin approval  
✗ Testing for unauthorized access  
✗ Capturing traffic without consent  
✗ Port scanning external services  
✗ Any use that violates local laws  

## Best Practices

1. **Start with read-only tools**
   - Interface inspection, route analysis, DNS lookups
   - No modifications, low risk

2. **Use in isolated environments first**
   - Lab or test network
   - Verify behavior before production use

3. **Document your actions**
   - What you tested
   - When and why
   - Results and findings
   - Helps with compliance and troubleshooting

4. **Minimize blast radius**
   - Use specific targets instead of broad scans
   - Limit concurrent operations
   - Avoid peak traffic times

5. **Respect privacy and data protection**
   - Don't capture more data than needed
   - Secure and delete captured traffic when done
   - Follow data retention policies

6. **Coordinate with stakeholders**
   - Inform security/network teams before testing
   - Agree on test windows
   - Get explicit approval for privileged operations

## No Warranty

These tools are provided as-is for legitimate diagnostic and educational purposes.

- No warranty of fitness for any particular use
- Users are responsible for ensuring authorized use
- Authors/maintainers disclaim liability for misuse
- Use at your own risk

See LICENSE file for full terms.
