"""Instrumented no-live-mutation checks for AD-00 CLI entry points."""

from __future__ import annotations

import contextlib
import importlib
import io
import subprocess
import sys
import unittest
from unittest import mock

from ad00_helpers import PLACEHOLDER_COMMANDS, decode_json_output, ensure_src_on_path


class Ad00InstrumentedEffectAuditTests(unittest.TestCase):
    def _load_main(self):
        ensure_src_on_path()
        for module_name in ("autodev.cli", "autodev.__main__"):
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue
            main = getattr(module, "main", None)
            if callable(main):
                return main
        self.fail("expected autodev.cli.main or autodev.__main__.main for in-process effect audit")

    def _call_main(self, *args: str) -> tuple[int, str]:
        main = self._load_main()
        stdout = io.StringIO()
        stderr = io.StringIO()
        calls: list[str] = []

        def blocked_effect(name: str):
            def _blocked(*_args, **_kwargs):
                calls.append(name)
                raise AssertionError(f"AD-00 command attempted live effect: {name}")

            return _blocked

        patches = [
            mock.patch.object(sys, "argv", ["autodev", *args]),
            mock.patch("subprocess.run", side_effect=blocked_effect("subprocess.run")),
            mock.patch("subprocess.Popen", side_effect=blocked_effect("subprocess.Popen")),
            mock.patch("subprocess.call", side_effect=blocked_effect("subprocess.call")),
            mock.patch("subprocess.check_call", side_effect=blocked_effect("subprocess.check_call")),
            mock.patch("subprocess.check_output", side_effect=blocked_effect("subprocess.check_output")),
            mock.patch("socket.socket", side_effect=blocked_effect("socket.socket")),
            mock.patch("socket.create_connection", side_effect=blocked_effect("socket.create_connection")),
        ]

        with contextlib.ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                try:
                    try:
                        result = main(list(args))
                    except TypeError:
                        result = main()
                    if isinstance(result, int):
                        exit_code = result
                    else:
                        exit_code = 0
                except SystemExit as exc:
                    exit_code = exc.code if isinstance(exc.code, int) else 1
                finally:
                    self.assertEqual(calls, [], f"blocked live effects were attempted: {calls}")
        return exit_code, f"{stdout.getvalue()}\n{stderr.getvalue()}"

    def test_help_does_not_call_subprocess_or_network(self) -> None:
        exit_code, output = self._call_main("--help")
        self.assertEqual(exit_code, 0, output)

    def test_placeholders_do_not_call_subprocess_or_network(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                exit_code, output = self._call_main(command)
                self.assertEqual(exit_code, 7, output)

    def test_placeholders_report_not_run_after_instrumented_execution(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                _exit_code, output = self._call_main(command)
                result = subprocess.CompletedProcess(args=["autodev", command], returncode=7, stdout=output)
                payload = decode_json_output(result)
                self.assertEqual(payload.get("evidence_class"), "NOT_RUN", payload)
                self.assertIs(payload.get("live_verified"), False, payload)

    def test_project_effect_harness_records_no_help_or_placeholder_effects(self) -> None:
        ensure_src_on_path()
        from autodev.effect_audit import instrument_live_effects

        main = self._load_main()
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            with instrument_live_effects() as audit:
                self.assertEqual(main(["--help"]), 0)
                for command in PLACEHOLDER_COMMANDS:
                    with self.subTest(command=command):
                        self.assertEqual(main([command]), 7)

        self.assertTrue(audit.clean, audit.as_dict())
        self.assertEqual(audit.events, [])


if __name__ == "__main__":
    unittest.main()
