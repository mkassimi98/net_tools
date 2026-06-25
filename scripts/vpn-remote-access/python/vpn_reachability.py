#!/usr/bin/env python3
import json
import re
import shutil
import socket
import subprocess
import sys
from datetime import datetime

from _config import get_config

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
GRAY = "\033[90m"

VPN_IFACE_RE = re.compile(r"^(tun|wg|tailscale)\d*")


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def detect_vpn_iface():
    try:
        data = json.loads(subprocess.check_output(
            ["ip", "-j", "addr", "show"], text=True, stderr=subprocess.DEVNULL
        ))
    except Exception:
        return ""
    for iface in data:
        name = iface.get("ifname", "")
        if VPN_IFACE_RE.match(name) and "UP" in iface.get("flags", []):
            return name
    return ""


def parse_ping(output):
    rows = []
    for line in output.splitlines():
        m = re.match(r"(\d+) bytes from (.+): icmp_seq=(\d+) ttl=(\d+) time=([\d.]+) ms", line)
        if m:
            rows.append({
                "seq": m.group(3),
                "from": m.group(2),
                "ttl": m.group(4),
                "time_ms": float(m.group(5)),
            })
    stat = re.search(r"(\d+) packets transmitted, (\d+) received", output)
    loss = re.search(r"([\d.]+)% packet loss", output)
    rtt = re.search(r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)", output)
    return rows, stat, loss, rtt


def probe_ssh(host, timeout=3):
    try:
        sock = socket.create_connection((host, 22), timeout=timeout)
        banner = sock.recv(256).decode(errors="replace").strip()
        sock.close()
        return "OPEN", banner[:60]
    except ConnectionRefusedError:
        return "CLOSED", ""
    except Exception:
        return "FILTERED/DOWN", ""


def main():
    config = get_config()
    vpn_iface = sys.argv[1] if len(sys.argv) > 1 else config.get("VPN_INTERFACE", "") or detect_vpn_iface()
    ping_target = sys.argv[2] if len(sys.argv) > 2 else config.get("VPN_PING_TARGET", "8.8.8.8")
    count = config.get("VPN_PING_COUNT", "4")
    ssh_target = config.get("VPN_SSH_TARGET", "")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "VPN REACHABILITY"
    subtitle = (
        f"iface={vpn_iface or 'auto'}  target={ping_target}  "
        f"ssh={ssh_target or 'not configured'} | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    # --- Route decision ---
    route_out = run(["ip", "route", "get", ping_target])
    route_dev = re.search(r"\bdev\s+(\S+)", route_out)
    route_via = re.search(r"\bvia\s+(\S+)", route_out)
    print(f"\n{BOLD}Route decision for {ping_target}{RESET}")
    if route_out.strip():
        dev = route_dev.group(1) if route_dev else "?"
        via = route_via.group(1) if route_via else "direct"
        is_vpn = bool(VPN_IFACE_RE.match(dev))
        dev_color = MAGENTA if is_vpn else YELLOW
        vpn_note = f"  {GREEN}✓ traffic goes through VPN{RESET}" if is_vpn else f"  {YELLOW}⚠ NOT via VPN{RESET}"
        print(f"  via {via}  dev {dev_color}{dev}{RESET}{vpn_note}")
    else:
        print(f"  {RED}No route to {ping_target}{RESET}")

    # --- Ping ---
    print(f"\n{BOLD}Ping {ping_target} (count={count}){RESET}")
    cmd = ["ping", "-c", count]
    if vpn_iface:
        cmd += ["-I", vpn_iface]
    cmd.append(ping_target)
    ping_out = run(cmd)
    rows, stat, loss, rtt = parse_ping(ping_out)

    if rows:
        hdr = f"{'SEQ':<6}{'FROM':<22}{'TTL':<6}{'TIME (ms)'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in rows:
            t = r["time_ms"]
            t_color = GREEN if t < 20 else (YELLOW if t < 100 else RED)
            print(f"  {r['seq']:<6}{r['from']:<22}{r['ttl']:<6}{t_color}{t:.2f}{RESET}")
        if rtt:
            print(
                f"\n  min={GREEN}{rtt.group(1)}{RESET} ms  "
                f"avg={CYAN}{rtt.group(2)}{RESET} ms  "
                f"max={rtt.group(3)} ms"
            )
        if loss:
            loss_val = float(loss.group(1))
            loss_color = GREEN if loss_val == 0 else (YELLOW if loss_val < 50 else RED)
            print(f"  Packet loss: {loss_color}{loss.group(1)}%{RESET}")
    elif ping_out.strip():
        print(f"  {RED}All packets lost — target unreachable{RESET}")
    else:
        print(f"  {RED}ping failed (no output){RESET}")

    # --- SSH probe (optional) ---
    if ssh_target:
        print(f"\n{BOLD}SSH probe → {ssh_target}:22{RESET}")
        state, banner = probe_ssh(ssh_target)
        state_color = GREEN if state == "OPEN" else (YELLOW if state == "CLOSED" else RED)
        print(f"  {state_color}{state}{RESET}", end="")
        if banner:
            print(f"  {DIM}banner: {banner}{RESET}", end="")
        print()
    else:
        print(f"\n  {GRAY}SSH probe skipped (set VPN_SSH_TARGET in local.env to enable){RESET}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{MAGENTA}VPN interface{RESET}=traffic exits via VPN  "
        f"{YELLOW}⚠{RESET}=traffic NOT through VPN  "
        f"{GREEN}low latency{RESET}=<20ms  {YELLOW}medium{RESET}=<100ms  {RED}high{RESET}=>100ms"
    )


if __name__ == "__main__":
    main()
