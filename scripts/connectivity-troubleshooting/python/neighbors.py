#!/usr/bin/env python3
import json
import shutil
import subprocess
from datetime import datetime

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""


def color_state(state):
    if isinstance(state, list):
        state = "/".join(str(item) for item in state if item) or "-"
    state = str(state or "-").upper()
    if state in {"REACHABLE", "PERMANENT"}:
        return f"{GREEN}{state}{RESET}"
    if state in {"FAILED", "INCOMPLETE"}:
        return f"{RED}{state}{RESET}"
    return f"{YELLOW}{state}{RESET}"


def main():
    print("\033[2J\033[H", end="")

    neigh = json.loads(run(["ip", "-j", "neigh"]) or "[]")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)
    title = "ARP / NEIGHBOR TABLE OVERVIEW"
    subtitle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(
        f"{BOLD}"
        f"{'IP':<24} "
        f"{'DEV':<12} "
        f"{'MAC':<20} "
        f"{'STATE':<16}"
        f"{RESET}"
    )
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not neigh:
        print(f"{DIM}No neighbors found. Generate traffic first (e.g., ping gateway).{RESET}")
    else:
        for entry in neigh:
            ip = entry.get("dst", "-")
            dev = entry.get("dev", "-")
            mac = entry.get("lladdr", "-")
            state = entry.get("state", "-")
            print(
                f"{YELLOW}{ip:<24}{RESET} "
                f"{CYAN}{dev:<12}{RESET} "
                f"{BLUE}{mac:<20}{RESET} "
                f"{color_state(state):<25}"
            )

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}REACHABLE{RESET}=neighbor is confirmed | "
        f"{RED}FAILED/INCOMPLETE{RESET}=resolution problem"
    )


if __name__ == "__main__":
    main()
