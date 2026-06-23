#!/usr/bin/env python3
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
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def have(command):
    return subprocess.call(
        ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) == 0


def color_state(state):
    if state.startswith("connected"):
        return f"{GREEN}{state}{RESET}"
    if state == "disconnected":
        return f"{RED}{state}{RESET}"
    if state == "unavailable":
        return f"{GRAY}{state}{RESET}"
    return f"{YELLOW}{state}{RESET}"


def main():
    print("\033[2J\033[H", end="")

    hostname = run(["hostname"])
    hostname = hostname.strip() if hostname else "-"

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "NETWORKMANAGER DEVICE STATUS"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if not have("nmcli"):
        print(f"  {YELLOW}nmcli not found - NetworkManager is not in use on this system.{RESET}")
    else:
        output = run(["nmcli", "-t", "-f", "DEVICE,TYPE,STATE,CONNECTION", "device", "status"]) or ""

        print(f"{BOLD}{'DEVICE':<18} {'TYPE':<12} {'STATE':<24} {'CONNECTION':<20}{RESET}")
        print(f"{GRAY}{'-' * line_width}{RESET}")

        for line in output.splitlines():
            parts = line.split(":")
            if len(parts) < 4:
                continue
            device, dtype, state, connection = parts[0], parts[1], parts[2], parts[3] or "-"
            print(
                f"{CYAN}{device:<18}{RESET} "
                f"{dtype:<12} "
                f"{color_state(state):<33} "
                f"{DIM}{connection:<20}{RESET}"
            )

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}connected{RESET}=device in use | "
        f"{RED}disconnected{RESET}=no active connection | "
        f"{GRAY}unavailable{RESET}=device can't be used right now"
    )


if __name__ == "__main__":
    main()
