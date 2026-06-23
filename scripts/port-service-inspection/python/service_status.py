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
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def color_state(value):
    if value in ("active", "enabled", "running"):
        return f"{GREEN}{value}{RESET}"
    if value in ("failed",):
        return f"{RED}{value}{RESET}"
    if value in ("inactive", "disabled", "dead"):
        return f"{GRAY}{value}{RESET}"
    return f"{YELLOW}{value}{RESET}"


def main():
    config = get_config()
    service = sys.argv[1] if len(sys.argv) > 1 else config.get("SERVICE_NAME", "ssh")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "SERVICE STATUS (systemctl)"
    subtitle = f"Service: {service} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    output = run(
        [
            "systemctl",
            "show",
            service,
            "-p",
            "LoadState,ActiveState,SubState,UnitFileState,MainPID",
            "--no-pager",
        ]
    )

    props = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            props[key] = value

    print(f"{BOLD}{'PROPERTY':<16} {'VALUE':<20}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")
    for key in ("LoadState", "ActiveState", "SubState", "UnitFileState", "MainPID"):
        value = props.get(key, "-")
        print(f"{CYAN}{key:<16}{RESET} {color_state(value):<29}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}active/enabled/running{RESET}=service healthy | "
        f"{RED}failed{RESET}=service crashed | "
        f"{GRAY}inactive/disabled{RESET}=service not running"
    )


if __name__ == "__main__":
    main()
