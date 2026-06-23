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
MAGENTA = "\033[35m"
GRAY = "\033[90m"

KNOWN_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    554: "RTSP",
    1883: "MQTT",
    3000: "Grafana",
    8086: "InfluxDB",
    8554: "RTSP",
    14550: "MAVLink",
}


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def parse_line(line):
    parts = line.split(None, 6)
    if len(parts) < 6 or parts[0] == "Netid":
        return None

    netid, state, _recvq, _sendq, local, _peer = parts[:6]
    rest = parts[6] if len(parts) > 6 else ""

    port = local.rsplit(":", 1)[-1] if ":" in local else "-"
    process_match = re.search(r'\(\("([^"]+)"', rest)
    process = process_match.group(1) if process_match else "-"

    return netid, state, local, process, port


def main():
    get_config()
    print("\033[2J\033[H", end="")

    output = run(["ss", "-tulpen"])
    hostname = run(["hostname"]).strip()

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "LISTENING SERVICES (ss -tulpen)"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(
        f"{BOLD}"
        f"{'PROTO':<8} {'STATE':<12} {'LOCAL ADDRESS':<28} {'PROCESS':<20} {'KNOWN SERVICE':<14}"
        f"{RESET}"
    )
    print(f"{GRAY}{'-' * line_width}{RESET}")

    rows = 0
    for line in output.splitlines():
        parsed = parse_line(line)
        if not parsed:
            continue
        netid, state, local, process, port = parsed
        rows += 1

        service = KNOWN_PORTS.get(int(port), "-") if port.isdigit() else "-"
        service_str = f"{GREEN}{service}{RESET}" if service != "-" else f"{GRAY}-{RESET}"

        print(
            f"{MAGENTA}{netid:<8}{RESET} "
            f"{YELLOW}{state:<12}{RESET} "
            f"{CYAN}{local:<28}{RESET} "
            f"{DIM}{process:<20}{RESET} "
            f"{service_str}"
        )

    if rows == 0:
        print(f"  {GRAY}No listening sockets found{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}known service{RESET}=well-known port for SSH/MQTT/RTSP/MAVLink/Grafana/InfluxDB | "
        f"{GRAY}-{RESET}=no mapping for that port"
    )


if __name__ == "__main__":
    main()
