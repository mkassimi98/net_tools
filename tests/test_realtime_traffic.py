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
    / "traffic-capture-analysis"
    / "python"
)
sys.path.insert(0, str(SCRIPT_DIR))

SPEC = importlib.util.spec_from_file_location(
    "realtime_traffic",
    SCRIPT_DIR / "realtime_traffic.py",
)
realtime_traffic = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(realtime_traffic)


class RealtimeTrafficTest(unittest.TestCase):
    def run_main(self, available_tool, argv=None, run_results=None):
        commands = []
        results = iter(run_results or [(1, "sudo: a password is required")])
        available_tools = (
            set(available_tool)
            if isinstance(available_tool, (set, tuple, list))
            else {available_tool}
        )

        def fake_have(command):
            return command in available_tools

        def fake_run(command):
            commands.append(command)
            return next(results)

        with (
            patch.object(
                realtime_traffic,
                "get_config",
                return_value={
                    "REALTIME_INTERFACE": "any",
                    "REALTIME_SECONDS": "8",
                },
            ),
            patch.object(realtime_traffic, "have", side_effect=fake_have),
            patch.object(realtime_traffic, "run", side_effect=fake_run),
            patch.object(sys, "argv", argv or ["realtime_traffic.py"]),
            redirect_stdout(io.StringIO()) as output,
        ):
            realtime_traffic.main()

        return commands, output.getvalue()

    def test_nethogs_cannot_wait_for_an_interactive_sudo_password(self):
        commands, output = self.run_main("nethogs")

        self.assertEqual(
            commands,
            [["timeout", "8s", "sudo", "-n", "nethogs", "-t", "-a"]],
        )
        self.assertIn("sudo -n", output)

    def test_iftop_cannot_wait_for_an_interactive_sudo_password(self):
        commands, output = self.run_main("iftop")

        self.assertEqual(
            commands,
            [["timeout", "8s", "sudo", "-n", "iftop", "-t"]],
        )
        self.assertIn("sudo -n", output)

    def test_all_flag_maps_to_nethogs_all_devices_flag(self):
        commands, output = self.run_main(
            "nethogs",
            ["realtime_traffic.py", "-a"],
        )

        self.assertEqual(
            commands,
            [["timeout", "8s", "sudo", "-n", "nethogs", "-t", "-a"]],
        )
        self.assertIn("all interfaces", output)

    def test_all_flag_lets_iftop_choose_its_default_interface(self):
        commands, output = self.run_main(
            "iftop",
            ["realtime_traffic.py", "--all"],
        )

        self.assertEqual(
            commands,
            [["timeout", "8s", "sudo", "-n", "iftop", "-t"]],
        )
        self.assertIn("all interfaces", output)

    def test_sudo_failure_falls_back_to_tshark_statistics(self):
        commands, output = self.run_main(
            {"nethogs", "tshark"},
            ["realtime_traffic.py", "-a"],
            run_results=[
                (1, "sudo: a password is required"),
                (0, "IO Statistics"),
            ],
        )

        self.assertEqual(
            commands,
            [
                ["timeout", "8s", "sudo", "-n", "nethogs", "-t", "-a"],
                [
                    "timeout",
                    "10s",
                    "tshark",
                    "-i",
                    "any",
                    "-a",
                    "duration:8",
                    "-q",
                    "-z",
                    "io,stat,1",
                ],
            ],
        )
        self.assertIn("falling back to tshark", output)
        self.assertIn("IO Statistics", output)


if __name__ == "__main__":
    unittest.main()
