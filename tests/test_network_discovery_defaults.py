#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "network-discovery"
    / "python"
)
sys.path.insert(0, str(SCRIPT_DIR))


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


host_discovery = load_module("host_discovery")
link_state = load_module("link_state")


class NetworkDiscoveryDefaultsTest(unittest.TestCase):
    def test_local_network_uses_default_route_interface_not_vpn_address(self):
        outputs = {
            ("ip", "-o", "-4", "route", "show", "default"): (
                "default via 192.168.1.1 dev wlp3s0f0 proto dhcp\n"
            ),
            ("ip", "-o", "-4", "addr", "show", "dev", "wlp3s0f0", "scope", "global"): (
                "3: wlp3s0f0 inet 192.168.1.22/24 brd 192.168.1.255 scope global\n"
            ),
        }

        with patch.object(
            host_discovery,
            "run",
            side_effect=lambda command: outputs.get(tuple(command), ""),
        ):
            self.assertEqual(host_discovery.detect_local_cidr(), "192.168.1.0/24")

    def test_link_interfaces_are_detected_from_system_state(self):
        outputs = {
            ("ip", "-o", "link", "show"): (
                "1: lo: <LOOPBACK,UP> mtu 65536\n"
                "2: eth0: <BROADCAST> mtu 1500\n"
                "3: wlp3s0f0: <BROADCAST,UP> mtu 1500\n"
            ),
            ("iw", "dev"): "phy#0\n\tInterface wlp3s0f0\n",
        }

        with patch.object(
            link_state,
            "run",
            side_effect=lambda command: outputs.get(tuple(command), ""),
        ):
            self.assertEqual(link_state.detect_interfaces(), ("eth0", "wlp3s0f0"))


if __name__ == "__main__":
    unittest.main()
