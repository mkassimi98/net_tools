#!/usr/bin/env python3
import json
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
BLUE = "\033[34m"
MAGENTA = "\033[35m"
GRAY = "\033[90m"


def run(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""


def color_metric(metric):
    if metric == "-":
        return f"{GRAY}{metric}{RESET}"
    try:
        value = int(metric)
        if value <= 100:
            return f"{GREEN}{metric}{RESET}"
        if value <= 600:
            return f"{YELLOW}{metric}{RESET}"
        return f"{RED}{metric}{RESET}"
    except ValueError:
        return metric


def route_type(dst):
    if dst == "default":
        return f"{GREEN}DEFAULT{RESET}"
    if "/" in dst:
        return f"{CYAN}NETWORK{RESET}"
    return f"{BLUE}HOST{RESET}"


def main():
    print("\033[2J\033[H", end="")

    routes = json.loads(run(["ip", "-j", "route", "show"]) or "[]")
    hostname = run(["hostname"]).strip()

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "ROUTING TABLE OVERVIEW"
    subtitle = f"Host: {hostname} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    default_routes = [r for r in routes if r.get("dst") == "default"]

    print(f"{BOLD}Default route summary{RESET}")
    if default_routes:
        for route in default_routes:
            gateway = route.get("gateway", "-")
            dev = route.get("dev", "-")
            metric = str(route.get("metric", "-"))
            proto = route.get("protocol", "-")
            src = route.get("prefsrc", "-")

            print(
                f"  {GREEN}default{RESET} via "
                f"{YELLOW}{gateway}{RESET} dev "
                f"{CYAN}{dev}{RESET} metric "
                f"{color_metric(metric)} proto "
                f"{MAGENTA}{proto}{RESET} src "
                f"{BLUE}{src}{RESET}"
            )
    else:
        print(f"  {RED}No default route found{RESET}")

    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(
        f"{BOLD}"
        f"{'TYPE':<14} "
        f"{'DESTINATION':<24} "
        f"{'GATEWAY':<18} "
        f"{'DEV':<14} "
        f"{'SRC':<18} "
        f"{'METRIC':<10} "
        f"{'PROTO':<10}"
        f"{RESET}"
    )

    print(f"{GRAY}{'-' * line_width}{RESET}")

    for route in routes:
        dst = route.get("dst", "default")
        gateway = route.get("gateway", "-")
        dev = route.get("dev", "-")
        src = route.get("prefsrc", "-")
        metric = str(route.get("metric", "-"))
        proto = route.get("protocol", "-")

        print(
            f"{route_type(dst):<23} "
            f"{YELLOW}{dst:<24}{RESET} "
            f"{gateway:<18} "
            f"{CYAN}{dev:<14}{RESET} "
            f"{BLUE}{src:<18}{RESET} "
            f"{color_metric(metric):<19} "
            f"{MAGENTA}{proto:<10}{RESET}"
        )

    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(f"{BOLD}Route decision example (ip route get){RESET}")
    for target in ["8.8.8.8", "1.1.1.1"]:
        decision = run(["ip", "route", "get", target]).strip()
        if decision:
            print(f"  {CYAN}{target}{RESET} -> {decision}")

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}DEFAULT{RESET}=Internet exit route | "
        f"{YELLOW}gateway{RESET}=next hop/router | "
        f"{CYAN}dev{RESET}=output interface | "
        f"lower metric = higher priority"
    )


if __name__ == "__main__":
    main()
