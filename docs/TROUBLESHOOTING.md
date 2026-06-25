# Troubleshooting Guide

## Common Issues

### Scripts hang waiting for password

**Symptom:** Script waits indefinitely, no output after running with sudo required.

**Cause:** `sudo -n` (non-interactive) fails because sudo credentials are not cached.

**Solution:**

```bash
# Refresh sudo timestamp
sudo -v

# Verify non-interactive sudo works
sudo -n whoami
```

Then run the script again.

### "command not found" errors

**Symptom:** Script fails with "command not found: nmap" or similar.

**Cause:** Required tool is not installed.

**Solution:** See [Installation guide](INSTALLATION.md) for your distribution.

```bash
# Quick check for missing tools
which nmap arp-scan ethtool iw curl dig mtr nc

# Install missing tools (Ubuntu/Debian)
sudo apt-get install nmap arp-scan iw dnsutils mtr-packet net-tools curl
```

### Python import or syntax errors

**Symptom:** `ImportError` or `SyntaxError` when running Python scripts.

**Cause:** Python version mismatch or missing `_config.py`.

**Solution:**

```bash
# Check Python version (need 3.6+)
python3 --version

# Verify _config.py exists in script directory
ls scripts/<category>/python/_config.py

# Verify syntax
python3 -m py_compile scripts/<category>/python/*.py

# Run with explicit python3
python3 scripts/<category>/python/script.py
```

### Permission denied errors

**Symptom:** "Permission denied" when running bash script.

**Cause:** Script file is not executable.

**Solution:**

```bash
# Make all scripts executable
chmod +x scripts/*/bash/*.sh
chmod +x scripts/*/python/*.py

# Verify
ls -l scripts/*/bash/*.sh | head
```

### No output from script

**Symptom:** Script runs without error but produces no output.

**Cause:** 
- Command failed silently (network unreachable, tool not installed)
- Terminal size too small
- ANSI colors not rendering

**Solution:**

```bash
# Check script output directly
bash -x scripts/port-service-inspection/bash/listening-services.sh

# Run bash version to see raw command output
./scripts/port-service-inspection/bash/listening-services.sh

# Check terminal size (need at least 80x20)
stty size

# Disable colors temporarily (export TERM=dumb)
TERM=dumb ./scripts/port-service-inspection/python/listening_services.py
```

### Colors not displaying correctly

**Symptom:** ANSI color codes appear as raw escape sequences.

**Cause:** Terminal doesn't support ANSI colors or `TERM` is set incorrectly.

**Solution:**

```bash
# Verify terminal supports colors
echo $TERM
# Should be something like xterm, xterm-256color, screen, tmux, etc.

# Set correct TERM
export TERM=xterm-256color
./scripts/port-service-inspection/python/listening_services.py

# Or check if less/more is interfering
unset PAGER
./scripts/port-service-inspection/python/listening_services.py
```

### Network discovery scripts find no hosts

**Symptom:** nmap or arp-scan returns empty results.

**Cause:**
- Incorrect CIDR/subnet configured
- Network not reachable
- nmap/arp-scan not installed
- Missing sudo for arp-scan

**Solution:**

```bash
# Verify network connectivity
ping -c 1 192.168.1.1    # Replace with your gateway

# Check configured CIDR
cat scripts/network-discovery/config/defaults.env
cat scripts/network-discovery/config/local.env 2>/dev/null

# Test nmap directly
nmap -sn 192.168.1.0/24

# Test arp-scan with sudo
sudo -v
sudo arp-scan --localnet | head
```

### VPN interface not detected

**Symptom:** VPN scripts show "No VPN interfaces found".

**Cause:** VPN is not active or uses non-standard interface name.

**Solution:**

```bash
# Verify VPN is running
ip link show | grep -E '(tun|wg|tailscale)'

# Check available interfaces
ip addr show

# Override with explicit interface
./scripts/vpn-remote-access/python/vpn_interface.py tun0
# Or set in local.env
echo "VPN_INTERFACE=tun0" >> scripts/vpn-remote-access/config/local.env
```

### SSH or iptables commands require sudo

**Symptom:** Script output says "needs sudo" or shows no firewall rules.

**Cause:** lsof, arp-scan, ethtool, or iptables require elevated permissions.

**Solution:**

```bash
# Pre-cache sudo credentials
sudo -v

# Verify non-interactive sudo works
sudo -n whoami

# Then run script (will use cached credentials)
./scripts/port-service-inspection/python/firewall_rules.py
```

### Port scan times out

**Symptom:** `nmap` or `nc` hangs or takes too long.

**Cause:** Network is slow or target is unreachable.

**Solution:**

```bash
# Speed up nmap with timeouts
nmap -p 22,80,443 --max-rtt-timeout 1000ms 192.168.1.50

# Use bash version instead of python (less overhead)
./scripts/network-discovery/bash/port-scan.sh 192.168.1.50 22,80,443

# Test connectivity first
ping -c 1 192.168.1.50
```

### Routes not showing as expected

**Symptom:** `ip route` output doesn't match route decision for target.

**Cause:** Static routes, policy routing, or multi-table routing active.

**Solution:**

```bash
# Show all routing tables
ip route show
ip route show table all

# Check policy routing rules
ip rule show

# Trace actual route for a target
ip route get 8.8.8.8
# Compare with what the script shows
```

### DNS resolution failing in script

**Symptom:** DNS lookup returns "no answer" or "SERVFAIL".

**Cause:**
- Network unreachable
- DNS server misconfigured or down
- Domain doesn't exist

**Solution:**

```bash
# Check DNS server
cat /etc/resolv.conf
systemctl status systemd-resolved

# Test resolution manually
dig example.com
nslookup example.com
host example.com

# Test with specific DNS server
dig @8.8.8.8 example.com
```

## Debug Mode

### Enable bash debugging

```bash
# Show commands as executed
bash -x scripts/port-service-inspection/bash/listening-services.sh

# Show commands and variable expansion
bash -xv scripts/port-service-inspection/bash/listening-services.sh
```

### Enable Python debugging

```bash
# Add debug output (modify script temporarily)
python3 -u scripts/port-service-inspection/python/listening_services.py

# Run with python debugger
python3 -m pdb scripts/port-service-inspection/python/listening_services.py
```

### Capture full output

```bash
# Save output with colors preserved
./scripts/port-service-inspection/python/listening_services.py | tee output.txt

# Save without colors
./scripts/port-service-inspection/python/listening_services.py | sed 's/\x1b\[[0-9;]*m//g' > output-plain.txt

# Redirect stderr too
./scripts/port-service-inspection/python/listening_services.py 2>&1 | tee full-output.txt
```

## Getting Help

If you encounter an issue not covered here:

1. Check the script's source code — all scripts are readable and have comments
2. Run with debug output enabled (see above)
3. Test the underlying command manually:
   ```bash
   # To debug listening_services.py, test ss directly:
   ss -tulpen
   ```
4. Check system logs for related errors:
   ```bash
   journalctl -u ssh
   journalctl -xe
   dmesg | tail
   ```

## Performance Tips

### Speed up scanning

```bash
# Faster nmap (aggressive timing)
export DISCOVERY_CONFIG=/tmp/fast.env
cat > /tmp/fast.env << EOF
SCAN_TARGET_IP=192.168.1.50
SCAN_PORTS=22,80,443
EOF
# nmap defaults to T3 (normal), can use T4/T5 for faster scans
```

### Reduce output verbosity

```bash
# Use bash version (less processing)
./scripts/network-discovery/bash/host-discovery.sh

# Pipe to grep to filter results
./scripts/port-service-inspection/python/listening_services.py | grep LISTEN
```

### Cache sudo to avoid delays

```bash
# Refresh sudo once, then run multiple scripts
sudo -v
time ./scripts/network-discovery/python/arp_scan.py
time ./scripts/port-service-inspection/python/firewall_rules.py
```
