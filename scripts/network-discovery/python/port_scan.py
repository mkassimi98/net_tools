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
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def color_state(state):
    if state == "open":
        return f"{GREEN}{state}{RESET}"
    if state == "closed":
        return f"{RED}{state}{RESET}"
    return f"{YELLOW}{state}{RESET}"


def main():
    config = get_config()
    target = sys.argv[1] if len(sys.argv) > 1 else config.get("SCAN_TARGET_IP", "127.0.0.1")
    ports = sys.argv[2] if len(sys.argv) > 2 else config.get(
        "SCAN_PORTS", "22,80,443,1883,8554,14550"
    )

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "PORT SCAN + SERVICE VERSIONS (nmap -p -sV)"
    subtitle = f"Target: {target} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{YELLOW}Caution: only scan hosts you own or are authorized to test.{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    output = run(["nmap", "-p", ports, "-sV", target])

    print(f"{BOLD}{'PORT':<10} {'STATE':<10} {'SERVICE':<16} {'VERSION':<50}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    rows = 0
    for line in output.splitlines():
        port_match = re.match(r"^(\d+)/(tcp|udp)\s+(\S+)\s+(\S+)(?:\s+(.*))?$", line)
        if not port_match:
            continue
        rows += 1
        port, proto, state, service, version = port_match.groups()
        version = version or "-"
        print(
            f"{CYAN}{port + '/' + proto:<10}{RESET} "
            f"{color_state(state):<19} "
            f"{service:<16} "
            f"{DIM}{version:<50}{RESET}"
        )

    if rows == 0:
        print(f"  {GRAY}No port information parsed (target may be unreachable){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}open{RESET}=service responding | "
        f"{RED}closed{RESET}=reachable, nothing listening | "
        f"{YELLOW}filtered{RESET}=no response (likely firewall)"
    )


if __name__ == "__main__":
    main()
