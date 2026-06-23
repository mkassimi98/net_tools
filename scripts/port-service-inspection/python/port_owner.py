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
CYAN = "\033[36m"
YELLOW = "\033[33m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def main():
    config = get_config()
    port = sys.argv[1] if len(sys.argv) > 1 else config.get("PORT_TARGET", "22")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "PORT OWNER LOOKUP"
    subtitle = f"Port: {port} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    ss_output = run(["ss", "-tnp"])
    matches = [line for line in ss_output.splitlines() if f":{port}" in line]

    print(f"{BOLD}ss -tnp matches for port {port}{RESET}")
    if matches:
        for line in matches:
            process_match = re.search(r'\(\("([^"]+)",pid=(\d+)', line)
            if process_match:
                print(f"  {GREEN}{process_match.group(1)}{RESET} (pid {process_match.group(2)})")
            print(f"  {DIM}{line.strip()}{RESET}")
    else:
        print(f"  {YELLOW}No matching socket found for port {port}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")

    lsof_output = run(["lsof", "-i", f":{port}"])
    print(f"{BOLD}lsof -i :{port}{RESET}")
    if lsof_output.strip():
        print(f"  {DIM}{lsof_output.strip().replace(chr(10), chr(10) + '  ')}{RESET}")
    else:
        print(f"  {YELLOW}No process found (may need to run with sudo){RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}process{RESET}=owner of the socket | "
        f"pid=process id you can cross-check with {CYAN}ps aux{RESET}"
    )


if __name__ == "__main__":
    main()
