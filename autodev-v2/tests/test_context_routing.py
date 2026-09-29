import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_context.py"
spec = importlib.util.spec_from_file_location("build_context", SCRIPT)
build_context = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = build_context
spec.loader.exec_module(build_context)


class ContextRoutingTests(unittest.TestCase):
    def load_map(self):
        with (ROOT / "context" / "context-map.json").open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def test_map_has_complete_ad_coverage(self):
        data = self.load_map()
        build_context.validate_context_map(data)
        self.assertEqual(sorted(data["milestones"]), [f"AD-{index:02d}" for index in range(24)])
        for milestone, entry in data["milestones"].items():
            self.assertTrue(entry["documents"], milestone)
            self.assertTrue(entry["fault_ids"], milestone)
            self.assertIn("implementation_roots", entry)

    def test_default_context_excludes_broad_sources(self):
        data = self.load_map()
        forbidden = {
            "AutoDev_v2_Complete_Specification.md",
            "05-MILESTONE-PLAN.md",
            "README.md",
            ".omx",
        }
        all_docs = list(data["shared_documents"])
        for entry in data["milestones"].values():
            all_docs.extend(entry["documents"])
        for doc in all_docs:
            path = doc["path"]
            self.assertNotIn(path, forbidden)
            self.assertNotIn(path.split("/", 1)[0], forbidden)
        self.assertNotIn(data["fault_matrix"]["path"], forbidden)

    def test_ad00_build_is_deterministic_and_bounded(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            body_a, digest_a, path_a = build_context.build_snapshot(
                "AD-00", output_dir=Path(first)
            )
            body_b, digest_b, path_b = build_context.build_snapshot(
                "AD-00", output_dir=Path(second)
            )
        self.assertEqual(body_a, body_b)
        self.assertEqual(digest_a, digest_b)
        self.assertLessEqual(len(body_a.encode("utf-8")), 32768)
        self.assertIn("Context map SHA-256:", body_a)
        self.assertIn("source_sha256=", body_a)
        self.assertIn("fault: `02-ACCEPTANCE-AND-FAULT-MATRIX.md`", body_a)
        self.assertIn("| F63 |", body_a)
        self.assertTrue(path_a.name.startswith("AD-00-"))
        self.assertEqual(path_a.name, path_b.name)

    def test_ad03_mapping_uses_selected_split_sources_and_fault_rows(self):
        data = self.load_map()
        entry = data["milestones"]["AD-03"]
        docs = {(doc["path"], doc["selector"]["value"]) for doc in entry["documents"]}
        self.assertIn(("00-PROJECT-SPECIFICATION.md", "### 3.2 Untrusted project content"), docs)
        self.assertIn(("00-PROJECT-SPECIFICATION.md", "### 3.3 Git and approval ceilings"), docs)
        self.assertIn(("00-PROJECT-SPECIFICATION.md", "### 4.1 Portable repository contract"), docs)
        self.assertIn(("00-PROJECT-SPECIFICATION.md", "## 6. Command contracts"), docs)
        self.assertIn(("00-PROJECT-SPECIFICATION.md", "## 7. Init: friendly, reversible repository alignment"), docs)
        self.assertIn(("04-CONTRACT-REFERENCE.md", "## A. PROJECT.yaml"), docs)
        self.assertEqual(entry["fault_ids"], ["F01", "F04", "F05", "F06", "F09", "F46", "F67"])
        self.assertEqual(data["fault_matrix"]["path"], "02-ACCEPTANCE-AND-FAULT-MATRIX.md")

    def test_fault_ranges_expand_to_exact_rows(self):
        expanded = build_context.expand_fault_ids(["F01-F03", "full regression suite", "F10"])
        self.assertEqual(expanded, ["F01", "F02", "F03", "F10"])
        with self.assertRaisesRegex(build_context.ContextError, "descending fault range"):
            build_context.expand_fault_ids(["F03-F01"])

    def test_ad01_includes_bounded_predecessor_evidence(self):
        body, _, _ = build_context.build_snapshot("AD-01", write=False)
        self.assertIn("predecessor=AD-00", body)
        self.assertIn("# AD-00 verification", body)
        self.assertNotIn("# AD-01 verification", body)

    def test_ad03_fails_closed_on_missing_ad02_evidence(self):
        with self.assertRaisesRegex(build_context.ContextError, "docs/verification/AD-02.md"):
            build_context.build_snapshot("AD-03", write=False)

    def test_unknown_milestone_fails_closed(self):
        with self.assertRaisesRegex(build_context.ContextError, "unknown milestone"):
            build_context.build_snapshot("AD-99", write=False)

    def test_expansion_requires_reason(self):
        with self.assertRaisesRegex(build_context.ContextError, "--reason is required"):
            build_context.build_snapshot(
                "AD-00",
                extra_headings=["milestones/AD-00.md::### Work"],
                write=False,
            )

    def test_expansion_changes_digest_and_records_reason(self):
        base_body, base_digest, _ = build_context.build_snapshot("AD-00", write=False)
        expanded_body, expanded_digest, _ = build_context.build_snapshot(
            "AD-00",
            extra_headings=["milestones/AD-00.md::### Work"],
            reason="Need exact work subsection for reviewer challenge.",
            write=False,
        )
        self.assertNotEqual(base_digest, expanded_digest)
        self.assertNotEqual(base_body, expanded_body)
        self.assertIn("reason=Need exact work subsection for reviewer challenge.", expanded_body)

    def test_budget_failure_does_not_write_snapshot(self):
        data = self.load_map()
        data["milestones"]["AD-00"]["byte_budget"] = 128
        with tempfile.TemporaryDirectory() as temp_root, tempfile.TemporaryDirectory() as out:
            temp_root_path = Path(temp_root)
            (temp_root_path / "context").mkdir()
            (temp_root_path / "context" / "context-map.json").write_text(
                json.dumps(data, sort_keys=True), encoding="utf-8"
            )
            shared = ROOT / "context" / "SHARED-INVARIANTS.md"
            milestone_dir = temp_root_path / "milestones"
            milestone_dir.mkdir()
            (temp_root_path / "context" / "SHARED-INVARIANTS.md").write_text(
                shared.read_text(encoding="utf-8"), encoding="utf-8"
            )
            (milestone_dir / "AD-00.md").write_text(
                (ROOT / "milestones" / "AD-00.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            reference_dir = temp_root_path / "reference"
            reference_dir.mkdir()
            (reference_dir / "SOURCES.md").write_text(
                (ROOT / "reference" / "SOURCES.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (temp_root_path / "02-ACCEPTANCE-AND-FAULT-MATRIX.md").write_text(
                (ROOT / "02-ACCEPTANCE-AND-FAULT-MATRIX.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(build_context.ContextError, "exceeds byte budget"):
                build_context.build_snapshot("AD-00", root=temp_root_path, output_dir=Path(out))
            self.assertEqual(list(Path(out).iterdir()), [])

    def test_exact_selector_failures_are_closed(self):
        markdown = "# A\none\n# A\ntwo\n"
        with self.assertRaisesRegex(build_context.ContextError, "duplicate heading"):
            build_context.extract_heading(markdown, "# A", "fixture.md")
        table = "| ID | Value |\n| --- | --- |\n| F01 | one |\n| F01 | two |\n"
        with self.assertRaisesRegex(build_context.ContextError, "duplicate table_row"):
            build_context.extract_table_row(table, "F01", "fixture.md")
        with self.assertRaisesRegex(build_context.ContextError, "missing table_row"):
            build_context.extract_table_row(table, "F02", "fixture.md")


if __name__ == "__main__":
    unittest.main()
