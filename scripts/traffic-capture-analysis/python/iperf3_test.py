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


def main():
    config = get_config()
    server = sys.argv[1] if len(sys.argv) > 1 else config.get("IPERF3_SERVER", "127.0.0.1")
    port = sys.argv[2] if len(sys.argv) > 2 else config.get("IPERF3_PORT", "5201")
    duration = sys.argv[3] if len(sys.argv) > 3 else config.get("IPERF3_DURATION_SECONDS", "5")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "IPERF3 THROUGHPUT TEST"
    subtitle = f"server={server}:{port} duration={duration}s | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not have("iperf3"):
        print(f"{YELLOW}iperf3 not found. Install iperf3 to run throughput tests.{RESET}")
        return

    print(f"{DIM}Tip: run this on server side if needed: iperf3 -s -p {port}{RESET}")
    cmd = ["iperf3", "-c", server, "-p", str(port), "-t", str(duration)]
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output = run(cmd)
    print(output or f"{YELLOW}No output captured{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}iperf3 test completed.{RESET}")
    else:
        print(f"{YELLOW}iperf3 returned non-zero (often no server listening at target).{RESET}")


if __name__ == "__main__":
    main()
