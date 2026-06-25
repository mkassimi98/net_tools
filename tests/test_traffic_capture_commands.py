#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "traffic-capture-analysis"
    / "python"
)
sys.path.insert(0, str(SCRIPT_DIR))


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


tcpdump_ping = load_module("tcpdump_ping")
tcpdump_tcp = load_module("tcpdump_tcp")
tcpdump_udp = load_module("tcpdump_udp")
tshark_capture = load_module("tshark_capture")


class TrafficCaptureCommandTest(unittest.TestCase):
    def test_ping_capture_is_bounded_and_generates_matching_traffic(self):
        self.assertEqual(
            tcpdump_ping.build_capture_command("any", 20, 12),
            ["timeout", "12s", "tcpdump", "-n", "-i", "any", "-c", "20", "icmp"],
        )
        self.assertEqual(
            tcpdump_ping.build_traffic_command("8.8.8.8", 4),
            [
                "bash",
                "-c",
                'sleep 1; exec ping -c "$1" "$2"',
                "bash",
                "4",
                "8.8.8.8",
            ],
        )
        self.assertEqual(
            tcpdump_ping.build_tshark_command("any", 20, 12),
            ["timeout", "12s", "tshark", "-i", "any", "-c", "20", "-f", "icmp"],
        )

    def test_tcp_capture_is_bounded_and_generates_http_traffic(self):
        self.assertEqual(
            tcpdump_tcp.build_capture_command("any", "example.com", 443, 20, 12),
            [
                "timeout",
                "12s",
                "tcpdump",
                "-n",
                "-i",
                "any",
                "-c",
                "20",
                "tcp and host example.com and port 443",
            ],
        )
        self.assertIn(
            "https://example.com:443/",
            tcpdump_tcp.build_traffic_command("example.com", 443),
        )
        self.assertEqual(
            tcpdump_tcp.build_tshark_command("any", "example.com", 443, 20, 12),
            [
                "timeout",
                "12s",
                "tshark",
                "-i",
                "any",
                "-c",
                "20",
                "-f",
                "tcp and host example.com and port 443",
            ],
        )

    def test_udp_capture_is_bounded_and_generates_dns_traffic(self):
        self.assertEqual(
            tcpdump_udp.build_capture_command("any", "8.8.8.8", 53, 20, 12),
            [
                "timeout",
                "12s",
                "tcpdump",
                "-n",
                "-i",
                "any",
                "-c",
                "20",
                "udp and host 8.8.8.8 and port 53",
            ],
        )
        self.assertEqual(
            tcpdump_udp.build_traffic_command("8.8.8.8", 53, "example.com"),
            [
                "bash",
                "-c",
                'sleep 1; exec dig +time=2 +tries=1 -p "$1" "@$2" "$3"',
                "bash",
                "53",
                "8.8.8.8",
                "example.com",
            ],
        )
        self.assertEqual(
            tcpdump_udp.build_tshark_command("any", "8.8.8.8", 53, 20, 12),
            [
                "timeout",
                "12s",
                "tshark",
                "-i",
                "any",
                "-c",
                "20",
                "-f",
                "udp and host 8.8.8.8 and port 53",
            ],
        )

    def test_tshark_capture_is_bounded(self):
        self.assertEqual(
            tshark_capture.build_capture_command("any", 20, 12),
            ["timeout", "12s", "tshark", "-i", "any", "-c", "20"],
        )


if __name__ == "__main__":
    unittest.main()
