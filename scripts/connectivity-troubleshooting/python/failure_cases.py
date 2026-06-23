#!/usr/bin/env python3
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
GRAY = "\033[90m"


def run(command):
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def get_global_ipv4_count():
    _, out = run(["ip", "-o", "-4", "addr", "show", "scope", "global"])
    return len([line for line in out.splitlines() if line.strip()])


def get_default_route_count():
    _, out = run(["ip", "route", "show", "default"])
    return len([line for line in out.splitlines() if line.strip()])


def get_dns_server_count():
    _, out = run(["cat", "/etc/resolv.conf"])
    return len(re.findall(r"^\s*nameserver\s+", out, flags=re.MULTILINE))


def probe_service(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def yes_no(value):
    return f"{GREEN}YES{RESET}" if value else f"{RED}NO{RESET}"


def main():
    config = get_config()
    host = sys.argv[1] if len(sys.argv) > 1 else config.get("SERVICE_HOST", "example.com")
    port = int(sys.argv[2]) if len(sys.argv) > 2 else int(config.get("SERVICE_PORT", "443"))
    timeout_seconds = int(config.get("SERVICE_TIMEOUT_SECONDS", "3"))

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)
    title = "CONNECTIVITY FAILURE CASES"
    subtitle = f"Probe: {host}:{port} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    ipv4_count = get_global_ipv4_count()
    default_count = get_default_route_count()
    dns_count = get_dns_server_count()
    service_ok = probe_service(host, port, timeout=timeout_seconds)

    print(f"{BOLD}Live checks{RESET}")
    print(f"  Global IPv4 present:          {yes_no(ipv4_count > 0)}")
    print(f"  Default gateway present:      {yes_no(default_count > 0)}")
    print(f"  DNS nameserver entries found: {yes_no(dns_count > 0)}")
    print(f"  Service response ({host}:{port}): {yes_no(service_ok)}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{BOLD}Checklist cases (point 4){RESET}")

    case1 = ipv4_count > 0 and default_count == 0
    print(
        f"  IP but no gateway: {yes_no(case1)} "
        f"{DIM}(host has address but no default route){RESET}"
    )

    case2 = default_count > 0 and dns_count == 0
    print(
        f"  Gateway but no DNS: {yes_no(case2)} "
        f"{DIM}(route exists but resolver is missing){RESET}"
    )

    case3 = default_count > 0 and not service_ok
    print(
        f"  Route exists but service not responding: {yes_no(case3)} "
        f"{DIM}(could be remote service/firewall issue){RESET}"
    )

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Note:{RESET} "
        f"These are observational checks, useful for recordings without changing system config."
    )


if __name__ == "__main__":
    main()
