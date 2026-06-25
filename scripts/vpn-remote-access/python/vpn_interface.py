#!/usr/bin/env python3
import json
import re
import shutil
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
BLUE = "\033[34m"
GRAY = "\033[90m"
MAGENTA = "\033[35m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def detect_vpn_interfaces():
    try:
        data = json.loads(subprocess.check_output(
            ["ip", "-j", "addr", "show"], text=True, stderr=subprocess.DEVNULL
        ))
    except Exception:
        return []
    vpn = []
    for iface in data:
        name = iface.get("ifname", "")
        if re.match(r"^(tun|wg|ovpn|tailscale)\d*", name):
            vpn.append(iface)
    return vpn


def vpn_type(name):
    if name.startswith("wg"):
        return "WireGuard"
    if name.startswith("tun"):
        return "OpenVPN/tun"
    if name.startswith("tailscale"):
        return "Tailscale"
    return "VPN"


def main():
    config = get_config()
    explicit_iface = sys.argv[1] if len(sys.argv) > 1 else config.get("VPN_INTERFACE", "")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "VPN INTERFACES"
    subtitle = f"ip addr (tun*/wg*/tailscale*) | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    vpn_ifaces = detect_vpn_interfaces()

    if not vpn_ifaces:
        print(f"\n  {YELLOW}No VPN interfaces found (tun*, wg*, tailscale*){RESET}")
        print(f"  {DIM}Start a VPN connection and re-run this script.{RESET}")
    else:
        hdr = f"{'INTERFACE':<16}{'TYPE':<16}{'STATE':<10}{'ADDRESS':<22}{'FLAGS'}"
        print(f"\n  {BOLD}{GRAY}{hdr}{RESET}")
        for iface in vpn_ifaces:
            name = iface.get("ifname", "?")
            flags = iface.get("flags", [])
            state = "UP" if "UP" in flags else "DOWN"
            state_color = GREEN if state == "UP" else RED
            addrs = iface.get("addr_info", [])
            first = True
            if addrs:
                for addr in addrs:
                    ip = f"{addr.get('local','?')}/{addr.get('prefixlen','?')}"
                    family = addr.get("family", "")
                    if not first:
                        print(f"  {'':16}{'':16}{'':10}{CYAN}{ip:<22}{RESET}{DIM}{family}{RESET}")
                    else:
                        print(
                            f"  {BOLD}{name:<16}{RESET}"
                            f"{MAGENTA}{vpn_type(name):<16}{RESET}"
                            f"{state_color}{state:<10}{RESET}"
                            f"{CYAN}{ip:<22}{RESET}"
                            f"{DIM}{' '.join(flags)}{RESET}"
                        )
                    first = False
            else:
                print(
                    f"  {BOLD}{name:<16}{RESET}"
                    f"{MAGENTA}{vpn_type(name):<16}{RESET}"
                    f"{state_color}{state:<10}{RESET}"
                    f"{GRAY}{'no address':<22}{RESET}"
                    f"{DIM}{' '.join(flags)}{RESET}"
                )

    # WireGuard details
    wg_out = run(["sudo", "-n", "wg", "show"])
    if wg_out.strip():
        print(f"\n{GRAY}{'-' * lw}{RESET}")
        print(f"{BOLD}WireGuard peer details (wg show){RESET}")
        for line in wg_out.strip().splitlines():
            if line.startswith("interface"):
                print(f"\n  {BOLD}{CYAN}{line}{RESET}")
            elif line.strip().startswith("peer"):
                print(f"  {MAGENTA}{line.strip()}{RESET}")
            else:
                key, _, val = line.strip().partition(":")
                print(f"    {GRAY}{key.strip():<20}{RESET}{val.strip()}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{MAGENTA}WireGuard{RESET}=wg*  "
        f"{MAGENTA}OpenVPN/tun{RESET}=tun*  "
        f"{MAGENTA}Tailscale{RESET}=tailscale*  "
        f"{GREEN}UP{RESET}=active  {RED}DOWN{RESET}=not connected"
    )


if __name__ == "__main__":
    main()
