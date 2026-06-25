#!/usr/bin/env python3
import re
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
        return ""


def parse_last(output):
    rows = []
    for line in output.strip().splitlines():
        if not line or line.startswith("wtmp") or line.startswith("btmp"):
            continue
        # "user   pts/0   192.168.1.10   Wed Jun 25 10:30   still logged in"
        # "user   tty1                   Wed Jun 25 09:00 - 09:45  (00:45)"
        parts = line.split(None, 9)
        if len(parts) < 4:
            continue
        user = parts[0]
        tty = parts[1]
        # host may be empty for local logins — detect by checking if part[2] is a date word
        date_words = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
        if parts[2] in date_words:
            host = "-"
            rest = " ".join(parts[2:])
        else:
            host = parts[2]
            rest = " ".join(parts[3:])
        rows.append((user, tty, host, rest.strip()))
    return rows


def main():
    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "LOGIN HISTORY"
    subtitle = f"last -n 30 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    out = run(["last", "-n", "30"])
    rows = parse_last(out)

    if rows:
        hdr = f"{'USER':<16}{'TTY':<12}{'HOST':<22}{'WHEN / DURATION'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for user, tty, host, rest in rows:
            if user in ("reboot", "shutdown"):
                color = YELLOW
            elif "still logged" in rest:
                color = GREEN
            else:
                color = CYAN
            host_col = f"{DIM}{host:<22}{RESET}"
            print(f"  {color}{user:<16}{RESET}{tty:<12}{host_col}{rest}")
    else:
        print(f"  {GRAY}No login history available{RESET}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}still logged in{RESET}=active session  "
        f"{CYAN}past session{RESET}=completed login  "
        f"{YELLOW}reboot/shutdown{RESET}=system event"
    )


if __name__ == "__main__":
    main()
