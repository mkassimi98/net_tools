#!/usr/bin/env python3
import json
import shutil
import subprocess
from datetime import datetime

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""


def color_state(state):
    state = (state or "-").upper()
    if state == "UP":
        return f"{GREEN}{state}{RESET}"
    if state == "DOWN":
        return f"{RED}{state}{RESET}"
    return f"{YELLOW}{state}{RESET}"


def main():
    print("\033[2J\033[H", end="")

    interfaces = json.loads(run(["ip", "-j", "addr", "show"]) or "[]")
    hostname = run(["hostname"]).strip()

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "NETWORK INTERFACES OVERVIEW"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(
        f"{BOLD}"
        f"{'IFACE':<16} "
        f"{'STATE':<10} "
        f"{'MAC':<20} "
        f"{'IPv4':<20} "
        f"{'IPv6':<30}"
        f"{RESET}"
    )
    print(f"{GRAY}{'-' * line_width}{RESET}")

    for iface in interfaces:
        name = iface.get("ifname", "-")
        state = iface.get("operstate", "-")
        mac = iface.get("address", "-")

        ipv4 = [a["local"] for a in iface.get("addr_info", []) if a.get("family") == "inet"]
        ipv6 = [a["local"] for a in iface.get("addr_info", []) if a.get("family") == "inet6"]

        ipv4_str = ipv4[0] if ipv4 else "-"
        ipv6_str = ipv6[0] if ipv6 else "-"
        extra_v4 = len(ipv4) - 1 if len(ipv4) > 1 else 0
        extra_v6 = len(ipv6) - 1 if len(ipv6) > 1 else 0
        if extra_v4:
            ipv4_str += f" {DIM}(+{extra_v4}){RESET}"
        if extra_v6:
            ipv6_str += f" {DIM}(+{extra_v6}){RESET}"

        print(
            f"{CYAN}{name:<16}{RESET} "
            f"{color_state(state):<19} "
            f"{BLUE}{mac:<20}{RESET} "
            f"{YELLOW}{ipv4_str:<20}{RESET} "
            f"{GREEN}{ipv6_str:<30}{RESET}"
        )

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}UP{RESET}=link active | "
        f"{RED}DOWN{RESET}=link inactive | "
        f"{BLUE}MAC{RESET}=link-layer address | "
        f"{DIM}(+N){RESET}=extra addresses on that interface"
    )


if __name__ == "__main__":
    main()
