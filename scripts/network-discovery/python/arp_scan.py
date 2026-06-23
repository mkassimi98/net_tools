#!/usr/bin/env python3
import re
import shutil
import subprocess
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


def main():
    get_config()

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "LOCAL DEVICE DISCOVERY (arp-scan --localnet)"
    subtitle = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{YELLOW}Caution: only scan networks you own or are authorized to test.{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    output = run(["sudo", "-n", "arp-scan", "--localnet"])
    if not output:
        print(f"  {YELLOW}arp-scan needs sudo - run this script with sudo to see live results.{RESET}")
        return

    print(f"{BOLD}{'IP':<18} {'MAC':<20} {'VENDOR':<30}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    rows = 0
    for line in output.splitlines():
        match = re.match(r"^(\S+)\t(\S+)\t(.*)$", line)
        if not match:
            continue
        ip, mac, vendor = match.groups()
        rows += 1
        print(f"{GREEN}{ip:<18}{RESET} {CYAN}{mac:<20}{RESET} {DIM}{vendor:<30}{RESET}")

    summary = next((line for line in output.splitlines() if line.startswith("Ending")), "")
    print(f"{GRAY}{'-' * line_width}{RESET}")
    if summary:
        print(f"{BOLD}{summary}{RESET}")
    print(f"{BOLD}Legend:{RESET} {CYAN}MAC{RESET}=link-layer address | {DIM}vendor{RESET}=OUI lookup")


if __name__ == "__main__":
    main()
