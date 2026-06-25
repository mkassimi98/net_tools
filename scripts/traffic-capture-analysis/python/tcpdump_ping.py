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


def build_capture_command(iface, count, timeout_seconds):
    return [
        "timeout",
        f"{timeout_seconds}s",
        "tcpdump",
        "-n",
        "-i",
        iface,
        "-c",
        str(count),
        "icmp",
    ]


def build_traffic_command(target, ping_count):
    return [
        "bash",
        "-c",
        'sleep 1; exec ping -c "$1" "$2"',
        "bash",
        str(ping_count),
        target,
    ]


def build_tshark_command(iface, count, timeout_seconds):
    return [
        "timeout",
        f"{timeout_seconds}s",
        "tshark",
        "-i",
        iface,
        "-c",
        str(count),
        "-f",
        "icmp",
    ]


def start_traffic(command):
    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    config = get_config()
    iface = sys.argv[1] if len(sys.argv) > 1 else config.get("CAPTURE_INTERFACE", "any")
    target = sys.argv[2] if len(sys.argv) > 2 else config.get("PING_TARGET", "8.8.8.8")
    count = config.get(
        "ICMP_CAPTURE_PACKET_COUNT",
        config.get("CAPTURE_PACKET_COUNT", "8"),
    )
    ping_count = config.get("PING_COUNT", "4")
    timeout_seconds = config.get("CAPTURE_TIMEOUT_SECONDS", "12")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "TCPDUMP DURING PING (ICMP)"
    subtitle = f"iface={iface} target={target} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    traffic_cmd = build_traffic_command(target, ping_count)
    print(f"{DIM}$ ping -c {ping_count} {target} (delayed background traffic){RESET}")
    start_traffic(traffic_cmd)

    cmd = build_capture_command(iface, count, timeout_seconds)
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output = run(cmd)
    if rc != 0 and "permission" in output.lower() and shutil.which("tshark"):
        print(f"{YELLOW}tcpdump lacks capture permission; falling back to tshark.{RESET}")
        start_traffic(traffic_cmd)
        cmd = build_tshark_command(iface, count, timeout_seconds)
        print(f"{DIM}$ {' '.join(cmd)}{RESET}")
        rc, output = run(cmd)
    print(output or f"{YELLOW}No output captured{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}Capture completed.{RESET}")
    else:
        print(f"{YELLOW}Capture ended with non-zero exit (still useful for demos).{RESET}")


if __name__ == "__main__":
    main()
