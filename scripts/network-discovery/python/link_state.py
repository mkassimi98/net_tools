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


def main():
    config = get_config()
    eth_iface = sys.argv[1] if len(sys.argv) > 1 else config.get("ETH_INTERFACE", "eth0")
    wifi_iface = sys.argv[2] if len(sys.argv) > 2 else config.get("WIFI_INTERFACE", "wlan0")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "PHYSICAL LINK STATE (ethtool / iw)"
    subtitle = f"eth={eth_iface} wifi={wifi_iface} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    eth_output = run(["sudo", "-n", "ethtool", eth_iface])
    print(f"{BOLD}Ethernet: {eth_iface}{RESET}")
    if eth_output:
        for key in ("Speed", "Duplex", "Link detected"):
            match = re.search(rf"{key}:\s*(.+)", eth_output)
            if not match:
                continue
            value = match.group(1).strip()
            if key == "Link detected":
                color = GREEN if value == "yes" else RED
            else:
                color = CYAN
            print(f"  {key:<16}{color}{value}{RESET}")
    else:
        print(f"  {YELLOW}No data (interface missing, or needs sudo){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")

    wifi_output = run(["iw", "dev", wifi_iface, "link"])
    print(f"{BOLD}WiFi: {wifi_iface}{RESET}")
    if wifi_output.startswith("Not connected"):
        print(f"  {YELLOW}Not connected{RESET}")
    elif wifi_output:
        for key, pattern in (
            ("SSID", r"SSID:\s*(.+)"),
            ("freq", r"freq:\s*(\S+)"),
            ("signal", r"signal:\s*(.+)"),
            ("rx bitrate", r"rx bitrate:\s*(.+)"),
            ("tx bitrate", r"tx bitrate:\s*(.+)"),
        ):
            match = re.search(pattern, wifi_output)
            if match:
                print(f"  {key:<16}{GREEN}{match.group(1).strip()}{RESET}")
    else:
        print(f"  {YELLOW}No data (interface missing, or iw not installed){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}Link detected: yes{RESET}=cable plugged & negotiated | "
        f"{GREEN}signal{RESET}=WiFi RSSI in dBm (closer to 0 is stronger)"
    )


if __name__ == "__main__":
    main()
