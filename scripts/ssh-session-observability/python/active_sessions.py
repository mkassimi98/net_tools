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
BLUE = "\033[34m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def parse_who(output):
    rows = []
    for line in output.strip().splitlines():
        parts = line.split()
        if len(parts) >= 5:
            user = parts[0]
            tty = parts[1]
            date = parts[2]
            time = parts[3]
            host = parts[4] if len(parts) > 4 else "-"
            rows.append((user, tty, date, time, host))
    return rows


def parse_w(output):
    rows = []
    lines = output.strip().splitlines()
    # skip header lines (first two)
    for line in lines[2:]:
        parts = line.split(None, 7)
        if len(parts) >= 7:
            rows.append({
                "user": parts[0],
                "tty": parts[1],
                "from": parts[2],
                "login": parts[3],
                "idle": parts[4],
                "jcpu": parts[5],
                "pcpu": parts[6],
                "what": parts[7] if len(parts) > 7 else "-",
            })
    return rows


def parse_loginctl(output):
    rows = []
    for line in output.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("SESSION") or line.startswith("-"):
            continue
        # "1 1000 myuser seat0 tty2"
        parts = line.split()
        if len(parts) >= 3 and parts[0].isdigit():
            rows.append({
                "session": parts[0],
                "uid": parts[1],
                "user": parts[2],
                "seat": parts[3] if len(parts) > 3 else "-",
                "tty": parts[4] if len(parts) > 4 else "-",
            })
    return rows


def main():
    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "ACTIVE LOGIN SESSIONS"
    subtitle = f"who / w / loginctl | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    # --- who ---
    who_out = run(["who"])
    who_rows = parse_who(who_out)
    print(f"\n{BOLD}Connected users (who){RESET}")
    if who_rows:
        hdr = f"{'USER':<16}{'TTY':<12}{'DATE':<12}{'TIME':<8}{'HOST'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for user, tty, date, time, host in who_rows:
            is_remote = not tty.startswith("tty") or tty.startswith("pts")
            color = CYAN if is_remote else GREEN
            print(f"  {color}{user:<16}{RESET}{tty:<12}{date:<12}{time:<8}{host}")
    else:
        print(f"  {GRAY}No active sessions{RESET}")

    # --- w ---
    w_out = run(["w"])
    w_rows = parse_w(w_out)
    print(f"\n{BOLD}Session activity (w){RESET}")
    if w_rows:
        hdr = f"{'USER':<16}{'TTY':<12}{'FROM':<20}{'IDLE':<8}{'COMMAND'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in w_rows:
            idle_color = YELLOW if r["idle"] not in ("-", "0.00s", "0:00") else GREEN
            print(
                f"  {CYAN}{r['user']:<16}{RESET}"
                f"{r['tty']:<12}"
                f"{r['from']:<20}"
                f"{idle_color}{r['idle']:<8}{RESET}"
                f"{DIM}{r['what']}{RESET}"
            )
    else:
        print(f"  {GRAY}No data from w{RESET}")

    # --- loginctl ---
    lc_out = run(["loginctl", "list-sessions"])
    lc_rows = parse_loginctl(lc_out)
    print(f"\n{BOLD}Systemd sessions (loginctl){RESET}")
    if lc_rows:
        hdr = f"{'SESSION':<10}{'UID':<8}{'USER':<16}{'SEAT':<10}{'TTY'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in lc_rows:
            print(
                f"  {CYAN}{r['session']:<10}{RESET}"
                f"{r['uid']:<8}"
                f"{GREEN}{r['user']:<16}{RESET}"
                f"{r['seat']:<10}"
                f"{r['tty']}"
            )
    else:
        print(f"  {GRAY}No systemd sessions (loginctl not available or no sessions){RESET}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{CYAN}cyan user{RESET}=remote/SSH  "
        f"{GREEN}green user{RESET}=local console  "
        f"{YELLOW}yellow idle{RESET}=session has been idle"
    )


if __name__ == "__main__":
    main()
