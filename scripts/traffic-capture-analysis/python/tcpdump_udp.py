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


def build_capture_command(iface, host, port, count, timeout_seconds):
    return [
        "timeout",
        f"{timeout_seconds}s",
        "tcpdump",
        "-n",
        "-i",
        iface,
        "-c",
        str(count),
        f"udp and host {host} and port {port}",
    ]


def build_traffic_command(host, port, query_name):
    return [
        "bash",
        "-c",
        'sleep 1; exec dig +time=2 +tries=1 -p "$1" "@$2" "$3"',
        "bash",
        str(port),
        host,
        query_name,
    ]


def build_tshark_command(iface, host, port, count, timeout_seconds):
    return [
        "timeout",
        f"{timeout_seconds}s",
        "tshark",
        "-i",
        iface,
        "-c",
        str(count),
        "-f",
        f"udp and host {host} and port {port}",
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
    host = sys.argv[2] if len(sys.argv) > 2 else config.get("UDP_TARGET_HOST", "8.8.8.8")
    port = sys.argv[3] if len(sys.argv) > 3 else config.get("UDP_TARGET_PORT", "53")
    count = config.get(
        "UDP_CAPTURE_PACKET_COUNT",
        config.get("CAPTURE_PACKET_COUNT", "2"),
    )
    timeout_seconds = config.get("CAPTURE_TIMEOUT_SECONDS", "12")
    query_name = config.get("UDP_QUERY_NAME", "example.com")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "TCPDUMP UDP TRAFFIC"
    subtitle = f"iface={iface} host={host} port={port} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    traffic_cmd = build_traffic_command(host, port, query_name)
    print(
        f"{DIM}$ dig @{host} -p {port} {query_name} "
        f"(delayed background traffic){RESET}"
    )
    start_traffic(traffic_cmd)

    cmd = build_capture_command(iface, host, port, count, timeout_seconds)
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output = run(cmd)
    if rc != 0 and "permission" in output.lower() and shutil.which("tshark"):
        print(f"{YELLOW}tcpdump lacks capture permission; falling back to tshark.{RESET}")
        start_traffic(traffic_cmd)
        cmd = build_tshark_command(iface, host, port, count, timeout_seconds)
        print(f"{DIM}$ {' '.join(cmd)}{RESET}")
        rc, output = run(cmd)
    print(output or f"{YELLOW}No output captured{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}UDP capture completed.{RESET}")
    else:
        print(f"{YELLOW}Capture ended with non-zero exit (check permissions or traffic availability).{RESET}")


if __name__ == "__main__":
    main()
