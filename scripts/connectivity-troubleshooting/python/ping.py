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
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def packet_loss(output):
    match = re.search(r"(\d+(?:\.\d+)?)% packet loss", output)
    return float(match.group(1)) if match else None


def color_loss(loss):
    if loss is None:
        return f"{GRAY}unknown{RESET}"
    if loss == 0:
        return f"{GREEN}{loss:.0f}%{RESET}"
    if loss < 100:
        return f"{YELLOW}{loss:.0f}%{RESET}"
    return f"{RED}{loss:.0f}%{RESET}"


def one_probe(label, target, count):
    code, out = run(["ping", "-c", str(count), target])
    loss = packet_loss(out)
    status = f"{GREEN}OK{RESET}" if code == 0 else f"{RED}FAIL{RESET}"
    print(f"{CYAN}{label:<24}{RESET} target={target:<20} status={status} loss={color_loss(loss)}")
    summary = next((line for line in out.splitlines() if "packet loss" in line), "no packet summary")
    print(f"  {DIM}{summary}{RESET}")


def main():
    config = get_config()
    target_ok = (
        sys.argv[1] if len(sys.argv) > 1 else config.get("PING_SUCCESS_TARGET", "8.8.8.8")
    )
    target_fail = (
        sys.argv[2] if len(sys.argv) > 2 else config.get("PING_FAILURE_TARGET", "203.0.113.254")
    )
    count = int(config.get("PING_COUNT", "4"))

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)
    title = "PING SUCCESS VS FAILURE"
    subtitle = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    one_probe("Expected success", target_ok, count)
    one_probe("Expected failure", target_fail, count)

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}OK{RESET}=received replies | "
        f"{RED}FAIL{RESET}=no replies/error | "
        f"packet loss helps explain quality"
    )


if __name__ == "__main__":
    main()
