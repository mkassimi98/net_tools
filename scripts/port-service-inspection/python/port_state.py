#!/usr/bin/env python3
import shutil
import socket
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


def classify(host, port, timeout):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return "OPEN", GREEN, "connected, something is listening"
    except ConnectionRefusedError:
        return "CLOSED", YELLOW, "host reachable, nothing listening on that port"
    except (socket.timeout, OSError):
        return "DOWN / FILTERED", RED, "no response (unreachable host or blocked by firewall)"


def main():
    config = get_config()

    cases = [
        (
            "Expected OPEN",
            config.get("PORT_STATE_OPEN_HOST", "127.0.0.1"),
            config.get("PORT_STATE_OPEN_PORT", "22"),
            float(config.get("PORT_STATE_OPEN_TIMEOUT_SECONDS", "2")),
        ),
        (
            "Expected CLOSED",
            config.get("PORT_STATE_CLOSED_HOST", "127.0.0.1"),
            config.get("PORT_STATE_CLOSED_PORT", "9"),
            float(config.get("PORT_STATE_CLOSED_TIMEOUT_SECONDS", "2")),
        ),
        (
            "Expected DOWN",
            config.get("PORT_STATE_DOWN_HOST", "203.0.113.10"),
            config.get("PORT_STATE_DOWN_PORT", "80"),
            float(config.get("PORT_STATE_DOWN_TIMEOUT_SECONDS", "2")),
        ),
    ]

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "PORT STATE: OPEN vs CLOSED vs DOWN"
    subtitle = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(f"{BOLD}{'CASE':<18} {'TARGET':<26} {'RESULT':<18} {'EXPLANATION':<40}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    for label, host, port, timeout in cases:
        result, color, explanation = classify(host, port, timeout)
        target = f"{host}:{port}"
        print(f"{CYAN}{label:<18}{RESET} {target:<26} {color}{result:<18}{RESET} {DIM}{explanation:<40}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}OPEN{RESET}=service responding | "
        f"{YELLOW}CLOSED{RESET}=host up, port not in use | "
        f"{RED}DOWN/FILTERED{RESET}=no response at all"
    )


if __name__ == "__main__":
    main()
