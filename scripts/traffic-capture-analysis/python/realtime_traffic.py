#!/usr/bin/env python3
import argparse
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
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def have(command):
    return subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def parse_args():
    parser = argparse.ArgumentParser(description="Show real-time network traffic.")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all_interfaces",
        help="monitor all interfaces",
    )
    parser.add_argument("interface", nargs="?", help="specific interface to monitor")
    return parser.parse_args()


def build_tshark_command(iface, seconds, all_interfaces):
    capture_iface = "any" if all_interfaces else iface
    return [
        "timeout",
        f"{int(seconds) + 2}s",
        "tshark",
        "-i",
        capture_iface,
        "-a",
        f"duration:{seconds}",
        "-q",
        "-z",
        "io,stat,1",
    ]


def main():
    config = get_config()
    args = parse_args()
    iface = args.interface or config.get("REALTIME_INTERFACE", "any")
    all_interfaces = args.all_interfaces or iface in {"", "any", "all"}
    seconds = config.get("REALTIME_SECONDS", "8")
    interface_label = "all interfaces" if all_interfaces else iface

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "REAL-TIME TRAFFIC VIEWERS"
    subtitle = (
        f"iface={interface_label} duration={seconds}s | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if have("iftop"):
        cmd = ["timeout", f"{seconds}s", "sudo", "-n", "iftop"]
        if not all_interfaces:
            cmd.extend(["-i", iface])
        cmd.append("-t")
        tool_name = "iftop"
    elif have("nethogs"):
        cmd = ["timeout", f"{seconds}s", "sudo", "-n", "nethogs", "-t"]
        cmd.append("-a" if all_interfaces else iface)
        tool_name = "nethogs"
    elif have("bmon"):
        cmd = ["timeout", f"{seconds}s", "bmon"]
        tool_name = "bmon"
    else:
        print(f"{YELLOW}None of iftop, nethogs, or bmon is installed.{RESET}")
        return

    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output = run(cmd)
    print(output or f"{YELLOW}No output captured{RESET}")

    if (
        rc != 0
        and "password is required" in output.lower()
        and have("tshark")
    ):
        print(
            f"{YELLOW}sudo credentials are unavailable; "
            f"falling back to tshark traffic statistics.{RESET}"
        )
        cmd = build_tshark_command(iface, seconds, all_interfaces)
        print(f"{DIM}$ {' '.join(cmd)}{RESET}")
        rc, output = run(cmd)
        print(output or f"{YELLOW}No output captured{RESET}")
        tool_name = "tshark"

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}{tool_name} run completed.{RESET}")
    elif "password is required" in output.lower():
        print(
            f"{YELLOW}sudo credentials are not available in this VHS terminal. "
            f"Run the renderer with passwordless access for {tool_name}, or use bmon.{RESET}"
        )
    else:
        print(f"{YELLOW}{tool_name} returned non-zero (often permissions or no traffic).{RESET}")


if __name__ == "__main__":
    main()
