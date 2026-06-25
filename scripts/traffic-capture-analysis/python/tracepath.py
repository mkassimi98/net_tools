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


def run_with_timeout(command, timeout_seconds):
    try:
        result = subprocess.run(
            command, text=True, capture_output=True, check=False, timeout=timeout_seconds
        )
        return result.returncode, (result.stdout + result.stderr).strip(), False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return 124, (stdout + stderr).strip(), True


def main():
    config = get_config()
    target = sys.argv[1] if len(sys.argv) > 1 else config.get("TRACEPATH_TARGET", "8.8.8.8")
    timeout_seconds = int(config.get("TRACEPATH_TIMEOUT_SECONDS", "20"))

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "TRACEPATH (MTU / PATH HINTS)"
    subtitle = f"target={target} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    cmd = ["tracepath", target]
    print(f"{DIM}$ {' '.join(cmd)}{RESET}")
    rc, output, timed_out = run_with_timeout(cmd, timeout_seconds)
    print(output or f"{YELLOW}No output captured{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    if timed_out:
        print(f"{YELLOW}tracepath timed out after {timeout_seconds}s (partial output shown).{RESET}")
    elif rc == 0:
        print(f"{GREEN}tracepath completed.{RESET}")
    else:
        print(f"{YELLOW}tracepath returned non-zero (tool may be missing or blocked).{RESET}")


if __name__ == "__main__":
    main()
