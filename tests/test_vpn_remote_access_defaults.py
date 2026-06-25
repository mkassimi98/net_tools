#!/usr/bin/env python3
import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "vpn-remote-access"
    / "python"
)
sys.path.insert(0, str(SCRIPT_DIR))


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


vpn_reachability = load_module("vpn_reachability")


class VpnRemoteAccessDefaultsTest(unittest.TestCase):
    def test_reachability_defaults_point_at_tun1_and_vpn_server(self):
        commands = []

        def fake_run(command):
            commands.append(command)
            if command == ["ip", "route", "get", "1.0.0.1"]:
                return "1.0.0.1 via 10.8.0.1 dev tun1 src 10.8.0.2"
            if command == ["ping", "-c", "4", "-I", "tun1", "1.0.0.1"]:
                return (
                    "64 bytes from 1.0.0.1: icmp_seq=1 ttl=64 time=12.34 ms\n"
                    "4 packets transmitted, 4 received, 0% packet loss\n"
                )
            return ""

        with (
            patch.object(
                vpn_reachability,
                "get_config",
                return_value={
                    "VPN_INTERFACE": "tun1",
                    "VPN_PING_TARGET": "1.0.0.1",
                    "VPN_PING_COUNT": "4",
                    "VPN_SSH_TARGET": "",
                },
            ),
            patch.object(vpn_reachability, "run", side_effect=fake_run),
            patch.object(sys, "argv", ["vpn_reachability.py"]),
            redirect_stdout(io.StringIO()) as output,
        ):
            vpn_reachability.main()

        self.assertEqual(
            commands,
            [
                ["ip", "route", "get", "1.0.0.1"],
                ["ping", "-c", "4", "-I", "tun1", "1.0.0.1"],
            ],
        )
        self.assertIn("iface=tun1", output.getvalue())
        self.assertIn("target=1.0.0.1", output.getvalue())
        self.assertIn("traffic goes through VPN", output.getvalue())


if __name__ == "__main__":
    unittest.main()
