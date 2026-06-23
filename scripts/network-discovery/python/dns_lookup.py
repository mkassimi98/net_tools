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
YELLOW = "\033[33m"
CYAN = "\033[36m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return getattr(exc, "output", "") or ""


def have(command):
    return subprocess.call(
        ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) == 0


def main():
    config = get_config()
    name = sys.argv[1] if len(sys.argv) > 1 else config.get("DNS_LOOKUP_NAME", "example.com")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "DNS LOOKUP (dig / nslookup)"
    subtitle = f"Name: {name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if have("dig"):
        output = run(["dig", name])
        server = "-"
        query_time = "-"
        answers = []
        for line in output.splitlines():
            if line.startswith(";; SERVER:"):
                server = line.split(":", 1)[1].strip()
            elif line.startswith(";; Query time:"):
                query_time = line.split(":", 1)[1].strip()
            elif line and not line.startswith(";") and "\tIN\t" in line:
                answers.append(line)

        print(f"{BOLD}Server:{RESET} {CYAN}{server}{RESET}   {BOLD}Query time:{RESET} {query_time}")
        print(f"{GRAY}{'-' * line_width}{RESET}")
        print(f"{BOLD}Answers{RESET}")
        if answers:
            for line in answers:
                print(f"  {GREEN}{line}{RESET}")
        else:
            print(f"  {YELLOW}No answer records (NXDOMAIN or no record of this type){RESET}")
    else:
        output = run(["nslookup", name])
        print(f"{BOLD}nslookup output{RESET}")
        print(f"  {DIM}{output.strip()}{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{CYAN}server{RESET}=resolver that answered | "
        f"{GREEN}answer{RESET}=resolved record"
    )


if __name__ == "__main__":
    main()
