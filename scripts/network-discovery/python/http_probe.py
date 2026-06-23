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
        result = subprocess.run(
            command, capture_output=True, check=False
        )
        combined = result.stdout + result.stderr
        return combined.decode("utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def color_status(code):
    if code.startswith("2"):
        return f"{GREEN}{code}{RESET}"
    if code.startswith("3"):
        return f"{CYAN}{code}{RESET}"
    if code.startswith(("4", "5")):
        return f"{RED}{code}{RESET}"
    return f"{YELLOW}{code}{RESET}"


def main():
    config = get_config()
    url = sys.argv[1] if len(sys.argv) > 1 else config.get("HTTP_PROBE_URL", "http://example.com")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "HTTP/API PROBE (curl -v)"
    subtitle = f"URL: {url} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    output = run(["curl", "-v", "-s", "-o", "/dev/null", url])

    print(f"{BOLD}Request{RESET}")
    for line in output.splitlines():
        if line.startswith(">"):
            print(f"  {CYAN}{line}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(f"{BOLD}Response{RESET}")
    status_line = None
    for line in output.splitlines():
        if line.startswith("<"):
            print(f"  {GREEN}{line}{RESET}")
            if status_line is None and re.search(r"HTTP/\S+\s+\d{3}", line):
                status_line = line

    if not status_line:
        print(f"  {YELLOW}No HTTP response received (connection or protocol error){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    status_match = re.search(r"(\d{3})", status_line) if status_line else None
    if status_match:
        print(f"{BOLD}Status code:{RESET} {color_status(status_match.group(1))}")

    print(
        f"{BOLD}Legend:{RESET} "
        f"{CYAN}>{RESET}=request headers sent | "
        f"{GREEN}<{RESET}=response headers received | "
        f"{GREEN}2xx{RESET}=success {CYAN}3xx{RESET}=redirect {RED}4xx/5xx{RESET}=error"
    )


if __name__ == "__main__":
    main()
