"""AD-02 safety primitive contract tests.

These tests define the public behavior expected by the AD-02 plan:
explicit-root local locks, atomic storage, bounded redacted subprocesses,
durable idempotent journals, and passive Git reads only.
"""

from __future__ import annotations

import dataclasses
import hashlib
import importlib
import json
import math
import os
import shutil
import stat
import sys
import tempfile
import time
import unittest
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Any
from unittest import mock

from ad00_helpers import PLACEHOLDER_COMMANDS, decode_json_output, ensure_src_on_path, run_autodev


ensure_src_on_path()


SECRET_CANARY = "AD02_SECRET_CANARY_DO_NOT_LEAK_96b94f"


def _module(name: str) -> Any:
    return importlib.import_module(f"autodev.safety.{name}")


def _attr(module: Any, name: str) -> Any:
    if not hasattr(module, name):
        raise AssertionError(f"{module.__name__} is missing public API {name}")
    return getattr(module, name)


def _value(value: Any) -> str:
    return getattr(value, "value", str(value))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _assert_dataclass_frozen(testcase: unittest.TestCase, instance: Any) -> None:
    testcase.assertTrue(dataclasses.is_dataclass(instance), f"{instance!r} must be a dataclass")
    with testcase.assertRaises(dataclasses.FrozenInstanceError):
        setattr(instance, "__ad02_mutation_probe__", True)


def _child_hold_repository_lock(root: str, ready: Queue[str], release: Queue[str]) -> None:
    ensure_src_on_path()
    locks = _module("locks")
    LockScope = _attr(locks, "LockScope")
    LockSpec = _attr(locks, "LockSpec")
    OrderedLock = _attr(locks, "OrderedLock")
    with OrderedLock(LockSpec(str(Path(root)), LockScope.REPOSITORY, "project-alpha")):
        ready.put("held")
        release.get(timeout=10)


def _child_atomic_write(root: str, relative: str, payload: bytes, ready: Queue[str]) -> None:
    ensure_src_on_path()
    storage = _module("storage")
    atomic_write_bytes = _attr(storage, "atomic_write_bytes")
    atomic_write_bytes(Path(root), relative, payload, expected_sha256=_sha256(b"version: 1\n"))
    ready.put("written")


class Ad02PublicApiTests(unittest.TestCase):
    def test_safety_package_exposes_bounded_public_modules(self) -> None:
        package = importlib.import_module("autodev.safety")
        for name in ("locks", "storage", "command", "journal", "git"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(package, name), f"autodev.safety must expose {name}")
                _module(name)

    def test_public_records_are_frozen_dataclasses(self) -> None:
        command = _module("command")
        journal = _module("journal")
        CommandSpec = _attr(command, "CommandSpec")
        JournalStore = _attr(journal, "JournalStore")

        spec = CommandSpec(
            argv=(sys.executable, "-c", "print('ok')"),
            cwd=tempfile.gettempdir(),
            env=(),
            timeout_seconds=1.0,
            max_output_bytes=128,
        )
        with tempfile.TemporaryDirectory() as root:
            request = JournalStore(root, "operations.json").prepare(
                "idem-1",
                "dispatch",
                {"installation_id": "inst-1", "project_id": "project-1", "milestone": "AD-02"},
            )

        _assert_dataclass_frozen(self, spec)
        _assert_dataclass_frozen(self, request)


class Ad02LockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_child_process_lock_blocks_second_repository_owner(self) -> None:
        locks = _module("locks")
        OrderedLock = _attr(locks, "OrderedLock")
        LockSpec = _attr(locks, "LockSpec")
        LockScope = _attr(locks, "LockScope")
        LockBusyError = _attr(locks, "LockBusyError")
        ready: Queue[str] = Queue()
        release: Queue[str] = Queue()
        child = Process(target=_child_hold_repository_lock, args=(str(self.root), ready, release))
        child.start()
        self.addCleanup(lambda: child.is_alive() and child.terminate())
        self.assertEqual(ready.get(timeout=5), "held")

        with self.assertRaises(LockBusyError):
            with OrderedLock(LockSpec(str(self.root), LockScope.REPOSITORY, "project-alpha")):
                pass

        release.put("release")
        child.join(timeout=5)
        self.assertEqual(child.exitcode, 0)

    def test_lock_order_rejects_installation_after_repository_is_held(self) -> None:
        locks = _module("locks")
        OrderedLock = _attr(locks, "OrderedLock")
        LockSpec = _attr(locks, "LockSpec")
        LockScope = _attr(locks, "LockScope")
        LockOrderError = _attr(locks, "LockOrderError")

        with OrderedLock(LockSpec(str(self.root), LockScope.REPOSITORY, "project-alpha")):
            with self.assertRaises(LockOrderError):
                with OrderedLock(LockSpec(str(self.root), LockScope.INSTALLATION, "install-alpha")):
                    pass

    def test_old_lock_metadata_is_not_enough_to_steal_kernel_lock(self) -> None:
        locks = _module("locks")
        OrderedLock = _attr(locks, "OrderedLock")
        LockSpec = _attr(locks, "LockSpec")
        LockScope = _attr(locks, "LockScope")
        LockBusyError = _attr(locks, "LockBusyError")
        ready: Queue[str] = Queue()
        release: Queue[str] = Queue()
        child = Process(target=_child_hold_repository_lock, args=(str(self.root), ready, release))
        child.start()
        self.addCleanup(lambda: child.is_alive() and child.terminate())
        self.assertEqual(ready.get(timeout=5), "held")

        old_time = time.time() - 90 * 24 * 60 * 60
        lock_files = [path for path in self.root.rglob("*") if path.is_file()]
        self.assertTrue(lock_files, "lock implementation must persist diagnostic metadata/file under the root")
        for path in lock_files:
            os.utime(path, (old_time, old_time))

        with self.assertRaises(LockBusyError):
            with OrderedLock(LockSpec(str(self.root), LockScope.REPOSITORY, "project-alpha")):
                pass

        release.put("release")
        child.join(timeout=5)
        self.assertEqual(child.exitcode, 0)


class Ad02AtomicStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        storage = _module("storage")
        self.atomic_write_bytes = _attr(storage, "atomic_write_bytes")
        self.inspect_recovery = _attr(storage, "inspect_recovery")
        self.ExpectedDigestMismatch = _attr(storage, "ExpectedDigestMismatch")
        self.UnsafePathError = _attr(storage, "UnsafePathError")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_atomic_write_creates_mode_0600_file_and_content_free_recovery_record(self) -> None:
        result = self.atomic_write_bytes(self.root, "state/projects.yaml", b"project: alpha\n", expected_sha256=None)
        target = self.root / "state" / "projects.yaml"
        self.assertEqual(target.read_bytes(), b"project: alpha\n")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

        recovery_path = Path(result.recovery_path)
        self.assertTrue(recovery_path.is_file(), result)
        recovery_text = recovery_path.read_text(encoding="utf-8")
        self.assertNotIn("project: alpha", recovery_text)
        self.assertIn(_sha256(b"project: alpha\n"), recovery_text)

    def test_expected_hash_rejects_stale_preview_without_overwriting_changed_file(self) -> None:
        target = self.root / "projects.yaml"
        target.write_bytes(b"version: 1\n")
        stale_hash = _sha256(b"version: 0\n")

        with self.assertRaises(self.ExpectedDigestMismatch):
            self.atomic_write_bytes(self.root, "projects.yaml", b"version: 2\n", expected_sha256=stale_hash)

        self.assertEqual(target.read_bytes(), b"version: 1\n")

    def test_expected_hash_is_checked_after_concurrent_writer_changes_target(self) -> None:
        self.atomic_write_bytes(self.root, "projects.yaml", b"version: 1\n", expected_sha256=None)
        preview_hash = _sha256(b"version: 1\n")
        ready: Queue[str] = Queue()
        child = Process(
            target=_child_atomic_write,
            args=(str(self.root), "projects.yaml", b"version: child\n", ready),
        )
        child.start()
        self.addCleanup(lambda: child.is_alive() and child.terminate())
        self.assertEqual(ready.get(timeout=5), "written")
        child.join(timeout=5)
        self.assertEqual(child.exitcode, 0)

        with self.assertRaises(self.ExpectedDigestMismatch):
            self.atomic_write_bytes(self.root, "projects.yaml", b"version: parent\n", expected_sha256=preview_hash)

        self.assertEqual((self.root / "projects.yaml").read_bytes(), b"version: child\n")

    def test_relative_target_rejects_parent_traversal_absolute_paths_and_symlinks(self) -> None:
        outside = Path(tempfile.mkdtemp(prefix="ad02-outside-"))
        self.addCleanup(lambda: shutil.rmtree(outside, ignore_errors=True))
        (self.root / "escape").symlink_to(outside, target_is_directory=True)

        for relative in ("../escape.yaml", "/tmp/escape.yaml", "escape/file.yaml"):
            with self.subTest(relative=relative):
                with self.assertRaises(self.UnsafePathError):
                    self.atomic_write_bytes(self.root, relative, b"blocked\n", expected_sha256=None)

    def test_recovery_classifies_ambiguous_conflict_without_finalizing(self) -> None:
        self.atomic_write_bytes(self.root, "registry.json", b'{"old": true}\n', expected_sha256=None)
        conflict = self.root / "registry.json"
        conflict.write_bytes(b'{"third_party": true}\n')

        recovery = self.inspect_recovery(self.root, "registry.json")
        self.assertEqual(_value(recovery.status), "CONFLICT")
        self.assertEqual(conflict.read_bytes(), b'{"third_party": true}\n')

    def test_injected_replace_failure_preserves_old_file_and_content_free_recovery_record(self) -> None:
        target = self.root / "registry.json"
        target.write_bytes(b'{"old": true}\n')
        old_hash = _sha256(b'{"old": true}\n')
        real_replace = os.replace
        replace_calls = 0

        def fail_target_replace(source: str, destination: str) -> None:
            nonlocal replace_calls
            replace_calls += 1
            if replace_calls == 2:
                raise OSError("simulated disk failure")
            real_replace(source, destination)

        with mock.patch("autodev.safety.storage.os.replace", side_effect=fail_target_replace):
            with self.assertRaises(OSError):
                self.atomic_write_bytes(self.root, "registry.json", b'{"new": true}\n', expected_sha256=old_hash)

        self.assertEqual(target.read_bytes(), b'{"old": true}\n')
        recovery_text = (self.root / ".registry.json.autodev-recovery.json").read_text(encoding="utf-8")
        self.assertIn(old_hash, recovery_text)
        self.assertIn(_sha256(b'{"new": true}\n'), recovery_text)
        self.assertNotIn('"old": true', recovery_text)
        self.assertNotIn('"new": true', recovery_text)


class Ad02CommandRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        command = _module("command")
        self.CommandSpec = _attr(command, "CommandSpec")
        self.run_command = _attr(command, "run_command")
        self.CommandPolicyError = _attr(command, "CommandPolicyError")
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _spec(self, script: str, **overrides: Any) -> Any:
        values = dict(
            argv=(sys.executable, "-c", script),
            cwd=str(self.cwd),
            env=(),
            timeout_seconds=2.0,
            max_output_bytes=256,
        )
        values.update(overrides)
        return self.CommandSpec(**values)

    def test_runner_redacts_secret_canaries_from_stdout_stderr_and_result_repr(self) -> None:
        result = self.run_command(
            self._spec(
                "import sys; print('out AD02_SECRET_CANARY_DO_NOT_LEAK_96b94f'); "
                "print('err AD02_SECRET_CANARY_DO_NOT_LEAK_96b94f', file=sys.stderr)"
            )
        )
        combined = f"{result.stdout}\n{result.stderr}\n{result!r}"
        self.assertNotIn(SECRET_CANARY, combined)
        self.assertIn("out", result.stdout)
        self.assertIn("err", result.stderr)

    def test_runner_bounds_captured_output_and_reports_truncation(self) -> None:
        result = self.run_command(self._spec("print('x' * 10000)", max_output_bytes=64))
        self.assertLessEqual(len(result.stdout.encode("utf-8")), 64)
        self.assertTrue(result.stdout_truncated)

    def test_runner_terminates_timed_out_process_group(self) -> None:
        script = (
            "import os, signal, subprocess, sys, time; "
            "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)']); "
            "print(child.pid, flush=True); "
            "time.sleep(30)"
        )
        result = self.run_command(self._spec(script, timeout_seconds=0.25))
        self.assertTrue(result.timed_out)
        self.assertLess(result.returncode, 0)

    def test_environment_diagnostics_expose_allowed_keys_not_values(self) -> None:
        result = self.run_command(
            self._spec(
                "import os; print(os.environ['AD02_ALLOWED'])",
                env=(("AD02_ALLOWED", SECRET_CANARY),),
            )
        )
        diagnostics = json.dumps({"env_keys": result.env_keys}, sort_keys=True)
        self.assertIn("AD02_ALLOWED", diagnostics)
        self.assertNotIn(SECRET_CANARY, diagnostics)
        self.assertNotIn(SECRET_CANARY, result.stdout)

    def test_shell_string_argv_is_rejected_before_process_creation(self) -> None:
        with mock.patch("subprocess.Popen", side_effect=AssertionError("shell string argv reached Popen")) as popen:
            with self.assertRaises(self.CommandPolicyError):
                self.run_command(
                    self.CommandSpec(
                        argv=f"{sys.executable} -c 'print(1)'",
                        cwd=str(self.cwd),
                        env=(),
                        timeout_seconds=1.0,
                        max_output_bytes=128,
                    )
                )
        popen.assert_not_called()

    def test_runner_is_rejected_while_multiple_safety_locks_are_held(self) -> None:
        locks = _module("locks")
        OrderedLock = _attr(locks, "OrderedLock")
        LockSpec = _attr(locks, "LockSpec")
        LockScope = _attr(locks, "LockScope")

        with OrderedLock(LockSpec(str(self.cwd), LockScope.ACCOUNT, "acct-1")):
            with OrderedLock(LockSpec(str(self.cwd), LockScope.INSTALLATION, "inst-1")):
                with mock.patch("subprocess.Popen") as popen:
                    with self.assertRaises(self.CommandPolicyError):
                        self.run_command(self._spec("print('blocked')"))
        popen.assert_not_called()


class Ad02JournalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        journal = _module("journal")
        self.JournalStore = _attr(journal, "JournalStore")
        self.ChangedOperationError = _attr(journal, "ChangedOperationError")
        self.JournalTransitionError = _attr(journal, "JournalTransitionError")
        self.OperationState = _attr(journal, "OperationState")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _arguments(self, **overrides: Any) -> dict[str, Any]:
        values = dict(
            installation_id="inst-1",
            project_id="project-1",
            logical_id="logical-1",
            milestone="AD-02",
            plan_digest="abc123",
        )
        values.update(overrides)
        return values

    def test_prepare_persists_prepared_record_before_returning_identity(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        record = journal.prepare("idem-1", "dispatch", self._arguments())
        loaded = self.JournalStore(self.root, "operations.json").prepare("idem-1", "dispatch", self._arguments())
        self.assertEqual(loaded.operation_id, record.operation_id)
        self.assertEqual(_value(loaded.state), "PREPARED")
        self.assertEqual(loaded.idempotency_key, "idem-1")

    def test_prepare_records_identity_hashes_without_canonical_arguments_payload(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        record = journal.prepare("idem-1", "dispatch", self._arguments(secret=SECRET_CANARY))

        text = "\n".join(path.read_text(encoding="utf-8") for path in self.root.rglob("*") if path.is_file())
        self.assertIn(record.operation_id, text)
        self.assertIn(record.arguments_sha256, text)
        self.assertNotIn(SECRET_CANARY, text)
        self.assertNotIn('"secret"', text)
        self.assertNotIn('"milestone"', text)

    def test_identical_prepare_retry_preserves_operation_identity(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        first = journal.prepare("idem-1", "dispatch", self._arguments())
        second = journal.prepare("idem-1", "dispatch", self._arguments())
        self.assertEqual(second.operation_id, first.operation_id)
        self.assertEqual(second.arguments_sha256, first.arguments_sha256)

    def test_changed_arguments_with_same_idempotency_key_are_rejected(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        journal.prepare("idem-1", "dispatch", self._arguments())
        with self.assertRaises(self.ChangedOperationError):
            journal.prepare("idem-1", "dispatch", self._arguments(milestone="AD-03"))

    def test_compare_and_set_transition_rejects_stale_expected_state(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        record = journal.prepare("idem-1", "dispatch", self._arguments())
        sent = journal.transition(
            record.operation_id,
            expected=self.OperationState.PREPARED,
            new_state=self.OperationState.SENT,
        )
        self.assertEqual(_value(sent.state), "SENT")
        with self.assertRaises(self.JournalTransitionError):
            journal.transition(
                record.operation_id,
                expected=self.OperationState.PREPARED,
                new_state=self.OperationState.ACKNOWLEDGED,
            )

    def test_prune_terminal_record_retains_content_free_tombstone(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        record = journal.prepare("idem-1", "dispatch", self._arguments(secret=SECRET_CANARY))
        journal.transition(
            record.operation_id,
            expected=self.OperationState.PREPARED,
            new_state=self.OperationState.SUCCEEDED,
        )
        tombstone = journal.prune_terminal(record.operation_id)
        text = "\n".join(path.read_text(encoding="utf-8") for path in self.root.rglob("*") if path.is_file())
        self.assertEqual(tombstone.operation_id, record.operation_id)
        self.assertIn(record.operation_id, text)
        self.assertNotIn(SECRET_CANARY, text)
        self.assertNotIn('"secret"', text)

    def test_non_canonical_arguments_are_rejected_before_identity_allocation(self) -> None:
        journal = self.JournalStore(self.root, "operations.json")
        for arguments in ({"bad": math.nan}, {1: "non-string-key"}):
            with self.subTest(arguments=arguments):
                with self.assertRaises(TypeError):
                    journal.prepare("idem-1", "dispatch", arguments)


class Ad02PassiveGitTests(unittest.TestCase):
    def setUp(self) -> None:
        git = _module("git")
        command = _module("command")
        self.passive_git = _attr(git, "passive_git")
        self.GitRequest = _attr(git, "GitRequest")
        self.GitPolicyError = _attr(git, "GitPolicyError")
        self.CommandPolicyError = _attr(command, "CommandPolicyError")
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_status_uses_passive_safeguards_before_porcelain_v2(self) -> None:
        calls: list[Any] = []

        def record_run(spec: Any) -> Any:
            calls.append(spec)
            return dataclasses.make_dataclass(
                "Result",
                [("returncode", int), ("stdout", str), ("stderr", str), ("timed_out", bool)],
                frozen=True,
            )(0, "", "", False)

        with mock.patch("autodev.safety.git.run_command", side_effect=record_run):
            self.passive_git(self.repo, self.GitRequest("status"))
        self.assertEqual(len(calls), 1)
        argv = tuple(calls[0].argv)
        env = dict(calls[0].env)
        self.assertIn("status", argv)
        self.assertIn("--porcelain=v2", argv)
        self.assertIn("-c", argv)
        joined = "\n".join(argv)
        joined_lower = joined.lower()
        for safeguard in (
            "core.hooksPath=/dev/null",
            "core.fsmonitor=false",
            "diff.external=",
            "filter.lfs.required=false",
            "protocol.file.allow=never",
            "core.attributesfile=/dev/null",
        ):
            with self.subTest(safeguard=safeguard):
                self.assertIn(safeguard.lower(), joined_lower)
        self.assertEqual(env.get("GIT_CONFIG_NOSYSTEM"), "1")
        self.assertEqual(env.get("GIT_TERMINAL_PROMPT"), "0")
        self.assertEqual(env.get("GIT_CONFIG_GLOBAL"), "/dev/null")

    def test_unsupported_git_arguments_are_rejected_before_process_creation(self) -> None:
        with mock.patch("autodev.safety.git.run_command") as run_command:
            with self.assertRaises(self.GitPolicyError):
                self.passive_git(self.repo, self.GitRequest("diff", ("--ext-diff",)))
        run_command.assert_not_called()

    def test_check_ignore_does_not_allow_external_path_escape(self) -> None:
        with mock.patch("autodev.safety.git.run_command") as run_command:
            with self.assertRaises(self.GitPolicyError):
                self.passive_git(self.repo, self.GitRequest("check-ignore", ("../outside",)))
        run_command.assert_not_called()

    def test_passive_git_is_rejected_while_multiple_safety_locks_are_held(self) -> None:
        locks = _module("locks")
        OrderedLock = _attr(locks, "OrderedLock")
        LockSpec = _attr(locks, "LockSpec")
        LockScope = _attr(locks, "LockScope")

        with OrderedLock(LockSpec(str(self.repo), LockScope.ACCOUNT, "acct-1")):
            with OrderedLock(LockSpec(str(self.repo), LockScope.INSTALLATION, "inst-1")):
                with mock.patch("subprocess.Popen") as popen:
                    with self.assertRaises(self.CommandPolicyError):
                        self.passive_git(self.repo, self.GitRequest("status"))
        popen.assert_not_called()


class Ad02Ad00RegressionTests(unittest.TestCase):
    def test_existing_cli_placeholders_still_return_exit_7_without_live_effects(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                result = run_autodev(command)
                self.assertEqual(result.returncode, 7, result)
                payload = decode_json_output(result)
                self.assertEqual(payload.get("evidence_class"), "NOT_RUN", payload)
                self.assertIs(payload.get("live_verified"), False, payload)


if __name__ == "__main__":
    unittest.main()
