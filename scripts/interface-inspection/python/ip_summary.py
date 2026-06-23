#!/usr/bin/env python3
import ipaddress
import shutil
import subprocess
from datetime import datetime

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""


def classify(ip_str):
    ip = ipaddress.ip_address(ip_str)
    if ip.is_loopback:
        return "loopback", GRAY
    if ip.is_link_local:
        return "link-local", GRAY
    if ip.is_private:
        return "private", YELLOW
    return "public", GREEN


def main():
    print("\033[2J\033[H", end="")

    hostname = run(["hostname"]).strip()
    ips = run(["hostname", "-I"]).split()

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "QUICK IP SUMMARY (hostname -I)"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(f"{BOLD}{'IP ADDRESS':<40} {'VERSION':<10} {'SCOPE':<14}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not ips:
        print(f"  {GRAY}No IP addresses reported{RESET}")
    else:
        for ip_str in ips:
            version = "IPv6" if ":" in ip_str else "IPv4"
            scope, color = classify(ip_str)
            print(f"{MAGENTA}{ip_str:<40}{RESET} {version:<10} {color}{scope:<14}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}public{RESET}=routable on the Internet | "
        f"{YELLOW}private{RESET}=RFC1918/ULA, local only | "
        f"{GRAY}loopback/link-local{RESET}=not used to reach other hosts"
    )


if __name__ == "__main__":
    main()
