"""AD-00 CLI contract tests."""

from __future__ import annotations

import importlib
import unittest

from ad00_helpers import PLACEHOLDER_COMMANDS, decode_json_output, ensure_src_on_path, run_autodev


class Ad00CliSmokeTests(unittest.TestCase):
    def test_package_imports(self) -> None:
        ensure_src_on_path()
        module = importlib.import_module("autodev")
        self.assertTrue(hasattr(module, "__version__"))

    def test_global_help_exits_successfully(self) -> None:
        result = run_autodev("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage", result.stdout.lower())


class Ad00PlaceholderContractTests(unittest.TestCase):
    def test_each_future_command_exits_exactly_unsupported_code_7(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                result = run_autodev(command)
                self.assertEqual(result.returncode, 7, result.stderr or result.stdout)

    def test_each_future_command_emits_deterministic_unsupported_json(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                result = run_autodev(command)
                payload = decode_json_output(result)
                self.assertEqual(payload.get("schema_version"), 1, payload)
                self.assertEqual(payload.get("command"), command, payload)
                self.assertEqual(payload.get("outcome"), "UNSUPPORTED", payload)
                self.assertIs(payload.get("implemented"), False, payload)
                self.assertEqual(payload.get("evidence_class"), "NOT_RUN", payload)
                self.assertIs(payload.get("live_verified"), False, payload)

    def test_future_command_options_do_not_enable_command_semantics(self) -> None:
        disallowed_options = ("--dry-run", "--plan", "--apply", "--json")
        for command in PLACEHOLDER_COMMANDS:
            for option in disallowed_options:
                with self.subTest(command=command, option=option):
                    result = run_autodev(command, option)
                    self.assertNotEqual(result.returncode, 0, result.stderr or result.stdout)
                    combined = f"{result.stdout}\n{result.stderr}".lower()
                    self.assertNotIn('"implemented": true', combined)
                    self.assertNotIn('"outcome": "pass"', combined)
                    self.assertNotIn("live_verified\": true", combined)


if __name__ == "__main__":
    unittest.main()
