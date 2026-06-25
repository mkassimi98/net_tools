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


def parse_ss(output):
    rows = []
    for line in output.strip().splitlines():
        if not line or line.startswith("State"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        state = parts[0]
        local = parts[3]
        peer = parts[4]
        process = " ".join(parts[5:]) if len(parts) > 5 else "-"
        # extract process name from users:(("sshd",pid=1234,...))
        pm = re.search(r'"([^"]+)"', process)
        proc_name = pm.group(1) if pm else "-"
        pid_m = re.search(r"pid=(\d+)", process)
        pid = pid_m.group(1) if pid_m else "-"
        rows.append((state, local, peer, proc_name, pid))
    return rows


def parse_lsof(output):
    rows = []
    for line in output.strip().splitlines():
        if not line or line.startswith("COMMAND"):
            continue
        parts = line.split()
        if len(parts) < 9:
            continue
        rows.append({
            "cmd": parts[0],
            "pid": parts[1],
            "user": parts[2],
            "fd": parts[3],
            "node": parts[7],
            "name": parts[8] if len(parts) > 8 else "-",
        })
    return rows


def parse_ps(output):
    rows = []
    for line in output.strip().splitlines():
        if not line or line.startswith("USER"):
            continue
        parts = line.split(None, 10)
        if len(parts) < 11:
            continue
        rows.append({
            "pid": parts[1],
            "cpu": parts[2],
            "mem": parts[3],
            "user": parts[0],
            "cmd": parts[10],
        })
    return rows


def main():
    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    lw = min(width, 120)

    title = "SSH CONNECTIONS & PROCESSES"
    subtitle = f"ss / lsof / ps | port 22 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"{BOLD}{CYAN}{title.center(lw)}{RESET}")
    print(f"{GRAY}{subtitle.center(lw)}{RESET}")
    print(f"{GRAY}{'-' * lw}{RESET}")

    # --- ss -tnp grep :22 ---
    ss_out = run(["ss", "-tnp"])
    ssh_lines = [l for l in ss_out.splitlines() if ":22" in l]
    ss_rows = parse_ss("\n".join(ssh_lines))

    print(f"\n{BOLD}Active TCP connections on :22 (ss -tnp){RESET}")
    if ss_rows:
        hdr = f"{'STATE':<14}{'LOCAL':<26}{'PEER':<26}{'PROCESS':<12}{'PID'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for state, local, peer, proc, pid in ss_rows:
            state_color = GREEN if state == "ESTAB" else YELLOW
            print(
                f"  {state_color}{state:<14}{RESET}"
                f"{CYAN}{local:<26}{RESET}"
                f"{peer:<26}"
                f"{proc:<12}{DIM}{pid}{RESET}"
            )
    else:
        print(f"  {GRAY}No active SSH connections on :22{RESET}")

    # --- ps aux | grep sshd ---
    ps_out = run(["ps", "aux"])
    sshd_lines = [l for l in ps_out.splitlines() if "sshd" in l and "[s]shd" not in l]
    ps_rows = parse_ps("\n".join(sshd_lines))

    print(f"\n{BOLD}sshd processes (ps aux){RESET}")
    if ps_rows:
        hdr = f"{'PID':<8}{'USER':<12}{'%CPU':<7}{'%MEM':<7}{'COMMAND'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in ps_rows:
            is_parent = "sshd -D" in r["cmd"] or r["cmd"].strip().endswith("sshd")
            color = GREEN if is_parent else CYAN
            cmd = r["cmd"][:lw - 40]
            print(
                f"  {color}{r['pid']:<8}{RESET}"
                f"{r['user']:<12}"
                f"{r['cpu']:<7}"
                f"{r['mem']:<7}"
                f"{DIM}{cmd}{RESET}"
            )
    else:
        print(f"  {GRAY}No sshd processes found{RESET}")

    # --- lsof -i :22 ---
    lsof_out = run(["sudo", "-n", "lsof", "-i", ":22"])
    lsof_rows = parse_lsof(lsof_out)

    print(f"\n{BOLD}Processes using port 22 (lsof -i :22){RESET}")
    if lsof_rows:
        hdr = f"{'CMD':<12}{'PID':<8}{'USER':<12}{'FD':<6}{'CONNECTION'}"
        print(f"  {BOLD}{GRAY}{hdr}{RESET}")
        for r in lsof_rows:
            print(
                f"  {CYAN}{r['cmd']:<12}{RESET}"
                f"{r['pid']:<8}"
                f"{r['user']:<12}"
                f"{r['fd']:<6}"
                f"{r['name']}"
            )
    else:
        print(f"  {GRAY}No data (needs sudo — run: sudo lsof -i :22){RESET}")

    print(f"\n{GRAY}{'-' * lw}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}ESTAB{RESET}=established SSH tunnel  "
        f"{YELLOW}other state{RESET}=listen/time-wait  "
        f"{GREEN}green pid{RESET}=sshd parent daemon"
    )


if __name__ == "__main__":
    main()
