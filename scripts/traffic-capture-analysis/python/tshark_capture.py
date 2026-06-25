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
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def have(command):
    return subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def build_capture_command(iface, count, timeout_seconds):
    return [
        "timeout",
        f"{timeout_seconds}s",
        "tshark",
        "-i",
        iface,
        "-c",
        str(count),
    ]


def main():
    config = get_config()
    iface = sys.argv[1] if len(sys.argv) > 1 else config.get("TSHARK_INTERFACE", "any")
    count = config.get("TSHARK_PACKET_COUNT", "20")
    timeout_seconds = config.get("CAPTURE_TIMEOUT_SECONDS", "12")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "TSHARK / WIRESHARK CAPTURE"
    subtitle = f"iface={iface} packets={count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not have("tshark"):
        print(f"{YELLOW}tshark not found. Use Wireshark GUI for visual demo if installed.{RESET}")
        return

    cmd = build_capture_command(iface, count, timeout_seconds)
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output = run(cmd)
    print(output or f"{YELLOW}No output captured{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}tshark capture completed.{RESET}")
    else:
        print(f"{YELLOW}Capture ended with non-zero exit (often due to privileges).{RESET}")


if __name__ == "__main__":
    main()
