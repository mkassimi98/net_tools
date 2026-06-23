#!/usr/bin/env python3
import re
import shutil
import subprocess
from datetime import datetime

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


def have(command):
    return subprocess.call(
        ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) == 0


def main():
    print("\033[2J\033[H", end="")

    hostname = run(["hostname"]).strip()
    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "DNS CONFIGURATION OVERVIEW"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if have("resolvectl"):
        status = run(["resolvectl", "status"])
        print(f"{BOLD}Per-link DNS servers (resolvectl status){RESET}")
        current_link = None
        for line in status.splitlines():
            link_match = re.match(r"^Link \d+ \((\S+)\)", line.strip())
            if link_match:
                current_link = link_match.group(1)
                print(f"  {YELLOW}{current_link}{RESET}")
                continue
            dns_match = re.match(r"\s*DNS Servers?:\s*(.+)", line)
            if dns_match and current_link:
                for server in dns_match.group(1).split():
                    print(f"    {GREEN}{server}{RESET}")
            domain_match = re.match(r"\s*DNS Domain:\s*(.+)", line)
            if domain_match and current_link:
                print(f"    {DIM}domain: {domain_match.group(1)}{RESET}")
    else:
        print(f"{BOLD}Nameservers (/etc/resolv.conf){RESET}")
        resolv = run(["cat", "/etc/resolv.conf"])
        found = False
        for line in resolv.splitlines():
            if line.strip().startswith("nameserver"):
                found = True
                server = line.split()[1]
                print(f"  {GREEN}{server}{RESET}")
            elif line.strip().startswith("search"):
                print(f"  {DIM}{line.strip()}{RESET}")
        if not found:
            print(f"  {DIM}No nameserver entries found{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}server{RESET}=DNS resolver address | "
        f"{YELLOW}link{RESET}=interface the DNS config applies to"
    )


if __name__ == "__main__":
    main()
