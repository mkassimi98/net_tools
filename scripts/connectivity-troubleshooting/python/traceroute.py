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
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        return 127, "command not found"


def have(command):
    return subprocess.call(
        ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) == 0


def main():
    config = get_config()
    target = sys.argv[1] if len(sys.argv) > 1 else config.get("TRACE_TARGET", "8.8.8.8")
    mtr_cycles = config.get("MTR_REPORT_CYCLES", "10")

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)
    title = "PATH TRACE TO EXTERNAL DESTINATION"
    subtitle = f"Target: {target} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    if have("traceroute"):
        cmd = ["traceroute", "-n", target]
    elif have("mtr"):
        cmd = ["mtr", "-rwzc", str(mtr_cycles), target]
    else:
        print(f"{YELLOW}Neither traceroute nor mtr is installed.{RESET}")
        return

    rc, output = run(cmd)
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    print(output)

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if rc == 0:
        print(f"{GREEN}Trace completed.{RESET}")
    else:
        print(f"{YELLOW}Trace command returned a non-zero exit code (often still useful).{RESET}")


if __name__ == "__main__":
    main()
