#!/usr/bin/env python3
import shutil
import subprocess
import sys
from datetime import datetime

from _config import get_config

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def main():
    config = get_config()
    port = sys.argv[1] if len(sys.argv) > 1 else config.get("FIREWALL_PORT", "22")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "FIREWALL RULES FOR A PORT"
    subtitle = f"Port: {port} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    rules = run(["iptables", "-L", "-n", "-v"])
    matches = [line for line in rules.splitlines() if f":{port}" in line]

    print(f"{BOLD}Rules mentioning port {port}{RESET}")
    if matches:
        for line in matches:
            print(f"  {GREEN}{line.strip()}{RESET}")
    else:
        print(f"  {YELLOW}No explicit rule for port {port} (likely falls under the default policy){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{BOLD}Live demo (run manually, not executed by this script):{RESET}")
    print(f"  {DIM}sudo iptables -A INPUT -p tcp --dport {port} -j DROP{RESET}   # block the port")
    print(f"  {DIM}sudo iptables -D INPUT -p tcp --dport {port} -j DROP{RESET}   # remove the rule afterwards")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Note:{RESET} this script only reads the current rules. "
        f"Applying/removing the DROP rule is left as a manual, narrated step."
    )


if __name__ == "__main__":
    main()
