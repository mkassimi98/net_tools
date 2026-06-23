#!/usr/bin/env python3
import shutil
import socket
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


def probe_tcp(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "OPEN", GREEN, "TCP handshake completed"
    except ConnectionRefusedError:
        return "CLOSED", YELLOW, "host reachable, port refused the connection"
    except (socket.timeout, OSError):
        return "FILTERED/DOWN", RED, "no response (timeout or unreachable)"


def probe_udp(host, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.send(b"")
        sock.recv(1)
        return "OPEN", GREEN, "received a reply"
    except ConnectionRefusedError:
        return "CLOSED", YELLOW, "ICMP port-unreachable received"
    except socket.timeout:
        return "OPEN|FILTERED", DIM, "no reply (normal for UDP: could be open or filtered)"
    except OSError:
        return "DOWN", RED, "host unreachable"
    finally:
        sock.close()


def main():
    config = get_config()

    tcp_host = config.get("TCP_PROBE_HOST", "127.0.0.1")
    tcp_port = int(config.get("TCP_PROBE_PORT", "22"))
    tcp_timeout = float(config.get("TCP_PROBE_TIMEOUT_SECONDS", "2"))

    udp_host = config.get("UDP_PROBE_HOST", "127.0.0.1")
    udp_port = int(config.get("UDP_PROBE_PORT", "14550"))
    udp_timeout = float(config.get("UDP_PROBE_TIMEOUT_SECONDS", "2"))

    print("\033[2J\033[H", end="")

    width = shutil.get_terminal_size((120, 20)).columns
    line_width = min(width, 120)

    title = "TCP vs UDP PORT PROBE"
    subtitle = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print(f"{BOLD}{CYAN}{title.center(line_width)}{RESET}")
    print(f"{GRAY}{subtitle.center(line_width)}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    print(f"{BOLD}{'PROTO':<8} {'TARGET':<26} {'RESULT':<16} {'NOTE':<45}{RESET}")
    print(f"{GRAY}{'-' * line_width}{RESET}")

    tcp_result, tcp_color, tcp_note = probe_tcp(tcp_host, tcp_port, tcp_timeout)
    print(
        f"{CYAN}{'TCP':<8}{RESET} {tcp_host + ':' + str(tcp_port):<26} "
        f"{tcp_color}{tcp_result:<16}{RESET} {DIM}{tcp_note:<45}{RESET}"
    )

    udp_result, udp_color, udp_note = probe_udp(udp_host, udp_port, udp_timeout)
    print(
        f"{CYAN}{'UDP':<8}{RESET} {udp_host + ':' + str(udp_port):<26} "
        f"{udp_color}{udp_result:<16}{RESET} {DIM}{udp_note:<45}{RESET}"
    )

    print(f"{GRAY}{'-' * line_width}{RESET}")
    print(
        f"{BOLD}Legend:{RESET} "
        f"{GREEN}OPEN{RESET}=got a reply | "
        f"{YELLOW}CLOSED{RESET}=explicit refusal | "
        f"UDP has no handshake, so a timeout doesn't always mean closed"
    )


if __name__ == "__main__":
    main()
