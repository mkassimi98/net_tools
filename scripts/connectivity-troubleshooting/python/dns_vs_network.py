#!/usr/bin/env python3
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
GRAY = "\033[90m"


def run(command):
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def classify(ip_rc, dns_rc):
    if ip_rc == 0 and dns_rc == 0:
        return f"{GREEN}Network and DNS look healthy{RESET}"
    if ip_rc == 0 and dns_rc != 0:
        return f"{YELLOW}Likely DNS issue (IP works, name fails){RESET}"
    if ip_rc != 0 and dns_rc != 0:
        return f"{RED}Likely network/gateway/connectivity issue{RESET}"
    return f"{YELLOW}Mixed result, investigate further{RESET}"


def packet_summary(output):
    for line in output.splitlines():
        if "packet loss" in line:
            return line
    return "no packet summary"


def main():
    config = get_config()
    ip_target = sys.argv[1] if len(sys.argv) > 1 else config.get("DNS_NETWORK_TARGET", "8.8.8.8")
    dns_target = sys.argv[2] if len(sys.argv) > 2 else config.get("DNS_NAME_TARGET", "google.com")
    count = int(config.get("PING_COUNT", "4"))

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)
    title = "NETWORK FAILURE VS DNS FAILURE"
    subtitle = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    ip_rc, ip_out = run(["ping", "-c", str(count), ip_target])
    dns_rc, dns_out = run(["ping", "-c", str(count), dns_target])

    ip_status = f"{GREEN}OK{RESET}" if ip_rc == 0 else f"{RED}FAIL{RESET}"
    dns_status = f"{GREEN}OK{RESET}" if dns_rc == 0 else f"{RED}FAIL{RESET}"

    print(f"{CYAN}Ping to IP:{RESET}   {ip_target:<20} -> {ip_status}")
    print(f"  {DIM}{packet_summary(ip_out)}{RESET}")
    print(f"{CYAN}Ping to name:{RESET} {dns_target:<20} -> {dns_status}")
    print(f"  {DIM}{packet_summary(dns_out)}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{BOLD}Interpretation:{RESET} {classify(ip_rc, dns_rc)}")


if __name__ == "__main__":
    main()
