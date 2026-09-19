"""AD-00 artifact contract tests."""

from __future__ import annotations

import importlib
import unittest
from typing import Any

from ad00_helpers import (
    EXPECTED_SOURCES,
    PROJECT_ROOT,
    SYNTHETIC_STATES,
    UNKNOWN_CATEGORIES,
    find_json_document_containing,
    flatten_strings,
    iter_records,
    json_files_under,
    load_json,
    ensure_src_on_path,
    read_text_tree,
)


class Ad00EvidenceInventoryTests(unittest.TestCase):
    def test_preserves_source_identity_without_fabricated_live_results(self) -> None:
        _path, data = find_json_document_containing(("docs", "evidence"), "S1", "S2", "S3")
        records = {
            str(record.get("id")): record
            for record in iter_records(data)
            if str(record.get("id")) in EXPECTED_SOURCES
        }

        self.assertEqual(set(EXPECTED_SOURCES), set(records))
        for source_id, expected in EXPECTED_SOURCES.items():
            with self.subTest(source_id=source_id):
                record = records[source_id]
                strings = "\n".join(flatten_strings(record))
                self.assertIn(expected["title"], strings)
                self.assertIn(expected["filename"], strings)
                self.assertEqual(record.get("sha256"), expected["sha256"])
                self.assertFalse(record.get("live_verified"), record)
                self.assertNotIn("PASS", strings.upper(), record)
                body_state = strings.lower()
                self.assertTrue(
                    "unavailable" in body_state or "not included" in body_state,
                    f"{source_id} must mark original body unavailable/not included: {record!r}",
                )


class Ad00BaselineTests(unittest.TestCase):
    def test_baseline_names_every_later_compatibility_unknown(self) -> None:
        text = read_text_tree("docs", "baseline").lower()
        self.assertTrue(text, "expected baseline artifact(s) under docs/baseline")
        for category in UNKNOWN_CATEGORIES:
            with self.subTest(category=category):
                self.assertIn(category, text)

    def test_baseline_does_not_fabricate_live_passes(self) -> None:
        text = read_text_tree("docs", "baseline").lower()
        self.assertNotIn("live_verified: true", text)
        self.assertNotIn('"live_verified": true', text)
        self.assertNotIn("live_certified", text)


class Ad00FixtureTests(unittest.TestCase):
    def test_fixture_manifest_has_six_simulated_non_live_state_examples(self) -> None:
        _path, data = find_json_document_containing(
            ("fixtures",), "ready", "active", "uncertain", "verifying", "human"
        )
        records = iter_records(data)
        matched: dict[str, dict[str, Any]] = {}
        for record in records:
            record_text = "\n".join(flatten_strings(record)).lower().replace("_", "-")
            for state in SYNTHETIC_STATES:
                if state in record_text:
                    matched.setdefault(state, record)

        self.assertEqual(set(SYNTHETIC_STATES), set(matched))
        for state, record in matched.items():
            with self.subTest(state=state):
                self.assertEqual(record.get("evidence_class"), "SIMULATED", record)
                self.assertFalse(record.get("live_verified"), record)


class Ad00EnvironmentManifestTests(unittest.TestCase):
    def test_environment_manifest_records_unknowns_without_live_values(self) -> None:
        manifest = PROJECT_ROOT / "templates" / "environment-manifest.json"
        self.assertTrue(manifest.exists(), "expected templates/environment-manifest.json")
        data = load_json(manifest)
        text = "\n".join(flatten_strings(data)).lower()

        semantic_categories = {
            "hermes": ("hermes",),
            "gjc": ("gjc", "gajae", "coordinator"),
            "runtime": ("runtime", "interpreter"),
            "route": ("route", "model"),
            "account": ("account", "provider"),
            "profile": ("profile", "service_identity"),
            "schedule": ("schedule", "cron"),
            "message": ("message", "delivery"),
            "host": ("host", "repo_realpath"),
            "process": ("process", "lock_backend", "effect_enforcement"),
            "enforcement": ("enforcement",),
        }
        for category, aliases in semantic_categories.items():
            with self.subTest(category=category):
                self.assertTrue(
                    any(alias in text for alias in aliases),
                    f"{category} missing from environment manifest",
                )
        self.assertNotIn('"pass"', text)
        self.assertNotIn('"live_verified": true', text)
        self.assertNotIn("secret", text)


class Ad00F63Tests(unittest.TestCase):
    def test_external_capability_classifier_is_blocked_and_non_live(self) -> None:
        ensure_src_on_path()
        evidence = importlib.import_module("autodev.evidence")
        result = evidence.classify_unavailable_external_capability("provider_probe")

        self.assertEqual(result.get("result"), "BLOCKED_EXTERNAL", result)
        self.assertEqual(result.get("evidence_class"), "BLOCKED_EXTERNAL", result)
        self.assertIs(result.get("live_verified"), False, result)

    def test_unavailable_external_capability_is_never_recorded_as_live_pass(self) -> None:
        combined = "\n".join(
            [
                read_text_tree("docs", "baseline"),
                read_text_tree("docs", "evidence"),
                read_text_tree("docs", "verification"),
            ]
        ).lower()
        self.assertTrue(combined, "expected AD-00 docs to record blocked/unsupported external scope")
        self.assertTrue("blocked_external" in combined or "unsupported" in combined)
        self.assertNotIn("fabricated", combined)
        self.assertNotIn('"outcome": "pass"', combined)
        self.assertNotIn("live pass", combined)

    def test_all_json_artifacts_reject_external_live_pass_claims(self) -> None:
        docs = []
        for area in (("docs",), ("fixtures",), ("templates",)):
            docs.extend(json_files_under(*area))
        self.assertTrue(docs, "expected JSON artifacts under docs, fixtures, or templates")
        for path in docs:
            with self.subTest(path=path.relative_to(PROJECT_ROOT)):
                data = load_json(path)
                for record in iter_records(data):
                    if record.get("live_verified") is not True:
                        continue
                    pass_like = any(
                        record.get(field) == "PASS"
                        for field in ("outcome", "result", "status")
                    ) or record.get("pass") is True
                    self.assertFalse(
                        pass_like,
                        f"{path} combines live_verified=true with PASS-like outcome: {record!r}",
                    )


if __name__ == "__main__":
    unittest.main()
