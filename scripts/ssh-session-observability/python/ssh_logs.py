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

ACCEPTED_RE = re.compile(r"Accepted\s+(\S+)\s+for\s+(\S+)\s+from\s+(\S+)")
FAILED_RE = re.compile(r"Failed\s+\S+\s+for\s+(?:invalid user\s+)?(\S+)\s+from\s+(\S+)")
DISCONNECT_RE = re.compile(r"Disconnected from\s+(?:user\s+\S+\s+)?(\S+)")
CLOSED_RE = re.compile(r"Connection closed by\s+(?:authenticating user\s+\S+\s+)?(\S+)")


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def classify(line):
    if ACCEPTED_RE.search(line):
        return "ACCEPT", GREEN
    if FAILED_RE.search(line):
        return "FAILED", RED
    if DISCONNECT_RE.search(line) or CLOSED_RE.search(line):
        return "CLOSE ", GRAY
    return "INFO  ", CYAN


def main():
    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "SSH SERVICE LOGS"
    subtitle = f"journalctl -u ssh -n 30 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    out = run(["journalctl", "-u", "ssh", "--no-pager", "-n", "30", "-o", "short"])
    if not out.strip():
        out = run(["journalctl", "-u", "sshd", "--no-pager", "-n", "30", "-o", "short"])

    if not out.strip():
        print(f"\n  {YELLOW}SSH journal not available (try: sudo journalctl -u ssh){RESET}")
    else:
        print(f"  {BOLD}{'TAG':<8}{'TIMESTAMP':<20}{'MESSAGE'}{RESET}")
        for line in out.strip().splitlines():
            # journalctl short format: "Jun 25 10:30:01 host sshd[pid]: message"
            m = re.match(r"^(\S+\s+\d+\s+\S+)\s+\S+\s+sshd\[\d+\]:\s*(.*)", line)
            if m:
                ts = m.group(1)
                msg = m.group(2)
            else:
                ts = ""
                msg = line
            tag, color = classify(line)
            # truncate long messages to terminal width
            max_msg = lw - 30
            if len(msg) > max_msg:
                msg = msg[:max_msg - 1] + "…"
            print(f"  {color}{tag}{RESET} {GRAY}{ts:<20}{RESET}{msg}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}ACCEPT{RESET}=successful login  "
        f"{RED}FAILED{RESET}=failed attempt  "
        f"{GRAY}CLOSE {RESET}=disconnect  "
        f"{CYAN}INFO  {RESET}=other SSH event"
    )


if __name__ == "__main__":
    main()
