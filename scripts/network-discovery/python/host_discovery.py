#!/usr/bin/env python3
import ipaddress
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
CYAN = "\033[36m"
YELLOW = "\033[33m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def detect_local_cidr():
    default_routes = run(["ip", "-o", "-4", "route", "show", "default"])
    dev_match = re.search(r"\bdev\s+(\S+)", default_routes)
    if dev_match:
        output = run(
            [
                "ip",
                "-o",
                "-4",
                "addr",
                "show",
                "dev",
                dev_match.group(1),
                "scope",
                "global",
            ]
        )
    else:
        output = run(["ip", "-o", "-4", "addr", "show", "scope", "global"])

    for line in output.splitlines():
        parts = line.split()
        for part in parts:
            if "/" in part and re.match(r"^\d+\.\d+\.\d+\.\d+/\d+$", part):
                interface = ipaddress.ip_interface(part)
                if interface.network.prefixlen < 32:
                    return str(interface.network)
    return ""


def main():
    config = get_config()
    cidr = sys.argv[1] if len(sys.argv) > 1 else config.get("NETWORK_CIDR", "")
    if not cidr:
        cidr = detect_local_cidr()

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "HOST DISCOVERY (nmap -sn)"
    subtitle = f"Network: {cidr} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{YELLOW}Caution: only scan networks you own or are authorized to test.{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not cidr:
        print(f"  {YELLOW}Could not determine a local network to scan.{RESET}")
        return

    output = run(["nmap", "-sn", cidr])

    print(f"{BOLD}{'HOST':<24} {'IP':<18} {'LATENCY':<12}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    hosts = 0
    pending_host = None
    for line in output.splitlines():
        report_match = re.match(r"Nmap scan report for (?:(\S+) \(([\d.]+)\)|([\d.]+))", line)
        if report_match:
            name = report_match.group(1) or "-"
            ip = report_match.group(2) or report_match.group(3)
            pending_host = (name, ip)
            continue

        latency_match = re.match(r"Host is up(?:\s+\(([^)]+)\))?", line)
        if latency_match and pending_host:
            hosts += 1
            name, ip = pending_host
            latency = latency_match.group(1) or "-"
            print(f"{CYAN}{name:<24}{RESET} {GREEN}{ip:<18}{RESET} {DIM}{latency:<12}{RESET}")
            pending_host = None

    if hosts == 0:
        print(f"  {GRAY}No hosts found{RESET}")

    summary_match = re.search(r"Nmap done: .*", output)
    print(f"{GRAY}{'-' * line_width}{RESET}")
    if summary_match:
        print(f"{BOLD}{summary_match.group(0)}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}IP{RESET}=responded to host discovery probe | "
        f"{DIM}latency{RESET}=round-trip time"
    )


if __name__ == "__main__":
    main()
