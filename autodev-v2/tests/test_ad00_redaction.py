"""AD-00 redaction canary tests."""

from __future__ import annotations

import importlib
import unittest

from ad00_helpers import ensure_src_on_path


class Ad00RedactionTests(unittest.TestCase):
    def _load_redact(self):
        ensure_src_on_path()
        candidates = (
            "autodev.redaction",
            "autodev.evidence",
            "autodev.safety",
            "autodev._redaction",
        )
        names = ("redact", "redact_text", "redact_secrets")
        for module_name in candidates:
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue
            for name in names:
                func = getattr(module, name, None)
                if callable(func):
                    return func
        self.fail("expected a redaction helper named redact/redact_text/redact_secrets")

    def test_redaction_removes_seeded_secret_canary(self) -> None:
        redact = self._load_redact()
        canary = "AD00_SECRET_CANARY_DO_NOT_LEAK_7f4e8c"
        redacted = str(redact(f"before {canary} after"))
        self.assertNotIn(canary, redacted)

    def test_redaction_preserves_non_secret_context(self) -> None:
        redact = self._load_redact()
        redacted = str(redact("route failed for project alpha"))
        self.assertIn("route failed", redacted.lower())
        self.assertIn("project alpha", redacted.lower())


if __name__ == "__main__":
    unittest.main()
