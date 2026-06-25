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
MAGENTA = "\033[35m"
GRAY = "\033[90m"

VPN_IFACE_RE = re.compile(r"^(tun|wg|tailscale)\d*")


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def load_routes():
    try:
        return json.loads(subprocess.check_output(
            ["ip", "-j", "route", "show"], text=True, stderr=subprocess.DEVNULL
        ))
    except Exception:
        return []


def main():
    config = get_config()
    explicit_iface = sys.argv[1] if len(sys.argv) > 1 else config.get("VPN_INTERFACE", "")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "VPN ROUTES"
    subtitle = f"ip route show | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    routes = load_routes()

    vpn_routes = [r for r in routes if VPN_IFACE_RE.match(r.get("dev", ""))]
    other_routes = [r for r in routes if not VPN_IFACE_RE.match(r.get("dev", ""))]

    def print_table(title_str, route_list, highlight=False):
        print(f"\n{BOLD}{title_str}{RESET}")
        if not route_list:
            print(f"  {GRAY}None{RESET}")
            return
        hdr = f"{'DESTINATION':<24}{'GATEWAY':<20}{'INTERFACE':<16}{'METRIC':<8}{'PROTOCOL'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in route_list:
            dst = r.get("dst", "?")
            gw = r.get("gateway", "-")
            dev = r.get("dev", "?")
            metric = str(r.get("metric", "-"))
            proto = r.get("protocol", "-")
            is_vpn = VPN_IFACE_RE.match(dev)
            dst_color = MAGENTA if highlight and is_vpn else CYAN
            dev_color = MAGENTA if highlight and is_vpn else GREEN
            print(
                f"  {dst_color}{dst:<24}{RESET}"
                f"{gw:<20}"
                f"{dev_color}{dev:<16}{RESET}"
                f"{metric:<8}"
                f"{DIM}{proto}{RESET}"
            )

    print_table("VPN routes (via tun*/wg*/tailscale*)", vpn_routes, highlight=True)
    print_table("All other routes", other_routes)

    if explicit_iface:
        iface_routes = [r for r in routes if r.get("dev") == explicit_iface]
        print(f"\n{BOLD}Routes via {explicit_iface} (from config){RESET}")
        if iface_routes:
            for r in iface_routes:
                dst = r.get("dst", "?")
                gw = r.get("gateway", "-")
                print(f"  {MAGENTA}{dst:<24}{RESET} via {gw}")
        else:
            print(f"  {GRAY}No routes via {explicit_iface}{RESET}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{MAGENTA}magenta{RESET}=VPN route (tun*/wg*/tailscale*)  "
        f"{CYAN}cyan{RESET}=destination  "
        f"{GREEN}green{RESET}=interface"
    )


if __name__ == "__main__":
    main()
