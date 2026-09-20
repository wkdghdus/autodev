"""AD-01 contract, identity, authority, and readiness tests."""

from __future__ import annotations

import hashlib
import importlib
import shutil
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

from ad00_helpers import PLACEHOLDER_COMMANDS, PROJECT_ROOT, ensure_src_on_path, run_autodev


ensure_src_on_path()

from autodev.contracts.errors import ContractValidationError
from autodev.contracts.models import (
    AdmissionState,
    ApprovalState,
    DeploymentState,
    DeliveryState,
    EnforcementAssurance,
    ExecutionState,
    InstallationBinding,
    Permission,
    ReadinessInputs,
    RepositoryState,
    ResourceState,
    ScheduleState,
    ValidationState,
)
from autodev.contracts.validation import load_execution_yaml, load_project_yaml, validate_mapping_record


FIXTURES = PROJECT_ROOT / "fixtures" / "ad01"


def _validation_api(name: str) -> Any:
    module = importlib.import_module("autodev.contracts")
    if not hasattr(module, name):
        raise AssertionError(f"AD-01 validation API is missing {name}()")
    return getattr(module, name)


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _codes(error: ContractValidationError) -> list[str]:
    return [issue.code for issue in error.issues]


def _paths(error: ContractValidationError) -> list[str]:
    return [issue.path for issue in error.issues]


def _outcome(result: Any) -> str:
    value = getattr(result, "outcome", getattr(result, "status", result))
    return getattr(value, "value", str(value))


class SyntheticRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for relative in (
            "src",
            "tests",
            "docs/Planning Space",
            "milestones",
            ".agent",
            "receipts",
            "docs",
        ):
            self.root.joinpath(relative).mkdir(parents=True, exist_ok=True)
        for relative in (
            "docs/requirements.md",
            "AGENTS.md",
            "milestones/AD-01.md",
            "docs/openai-approved.md",
            "docs/Hermes Autonomy Enabled.md",
            "docs/APPROVED-status.md",
        ):
            self.root.joinpath(relative).write_text("synthetic\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()


class Ad01Ac1DraftAndConfiguredProjectTests(SyntheticRepoTestCase):
    def test_draft_with_explicit_unknowns_loads_as_needing_input(self) -> None:
        project = load_project_yaml(_fixture("PROJECT.draft.yaml"), self.root)
        self.assertEqual(project.setup_state.value, "draft")
        self.assertEqual(project.repository_state, RepositoryState.DRAFT)
        self.assertEqual(project.alignment_outcome.value, "NEEDS_INPUT")

    def test_draft_with_explicit_unknowns_is_not_enable_ready(self) -> None:
        evaluate_readiness = _validation_api("evaluate_readiness")
        result = evaluate_readiness(
            ReadinessInputs(
                repository=RepositoryState.DRAFT,
                deployment=DeploymentState.ABSENT,
                validation=ValidationState.NOT_RUN,
                admission=AdmissionState.UNKNOWN,
                schedule=ScheduleState.ABSENT,
                execution=ExecutionState.IDLE,
                resource=ResourceState.UNKNOWN,
                delivery=DeliveryState.NOT_TESTED,
            )
        )
        self.assertFalse(result.ready_for_enable)
        self.assertIn("REPOSITORY_NOT_ALIGNED", result.reasons)

    def test_configured_but_unapproved_project_can_be_aligned_only(self) -> None:
        project = load_project_yaml(_fixture("PROJECT.configured.yaml"), self.root)
        evaluate_readiness = _validation_api("evaluate_readiness")
        result = evaluate_readiness(
            ReadinessInputs(
                repository=project.repository_state,
                deployment=DeploymentState.ABSENT,
                validation=ValidationState.NOT_RUN,
                admission=AdmissionState.UNKNOWN,
                schedule=ScheduleState.ABSENT,
                execution=ExecutionState.IDLE,
                resource=ResourceState.UNKNOWN,
                delivery=DeliveryState.NOT_TESTED,
            )
        )
        self.assertTrue(result.aligned)
        self.assertFalse(result.ready_for_enable)
        self.assertFalse(result.ready_to_dispatch)


class Ad01Ac2StrictYamlTests(SyntheticRepoTestCase):
    def assertProjectIssue(self, yaml_text: str, expected_code: str, expected_path: str | None = None) -> None:
        with self.assertRaises(ContractValidationError) as caught:
            load_project_yaml(yaml_text, self.root)
        self.assertIn(expected_code, _codes(caught.exception))
        if expected_path is not None:
            self.assertIn(expected_path, _paths(caught.exception))
        self.assertTrue(any(issue.line is not None for issue in caught.exception.issues), caught.exception.issues)

    def test_malformed_yaml_reports_source_location(self) -> None:
        self.assertProjectIssue("schema_version: [\n", "MALFORMED_YAML", "$")

    def test_duplicate_yaml_keys_are_rejected(self) -> None:
        self.assertProjectIssue("schema_version: 2\nschema_version: 2\n", "DUPLICATE_KEY", "$")

    def test_unsafe_yaml_tags_are_rejected(self) -> None:
        self.assertProjectIssue("schema_version: !unsafe 2\n", "UNSAFE_YAML", "$")

    def test_yaml_aliases_and_anchors_are_rejected(self) -> None:
        self.assertProjectIssue("schema_version: &version 2\nsetup_state: *version\n", "UNSAFE_YAML", "$")

    def test_multiple_documents_are_rejected(self) -> None:
        self.assertProjectIssue("schema_version: 2\n---\nschema_version: 2\n", "MULTIPLE_DOCUMENTS", "$")

    def test_non_string_mapping_keys_are_rejected(self) -> None:
        self.assertProjectIssue("1: value\n", "NON_STRING_KEY", "$")

    def test_unknown_project_fields_are_rejected(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("project:\n", "unexpected: true\nproject:\n", 1)
        self.assertProjectIssue(text, "UNKNOWN_FIELD", "$.unexpected")

    def test_unsupported_project_schema_version_is_rejected(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("schema_version: 2", "schema_version: 3", 1)
        self.assertProjectIssue(text, "UNSUPPORTED_VERSION", "$.schema_version")

    def test_unsupported_execution_version_and_unknown_fields_are_rejected(self) -> None:
        text = _fixture("EXECUTION.empty.yaml").replace("schema_version: 2", "schema_version: 3\nunexpected: false", 1)
        with self.assertRaises(ContractValidationError) as caught:
            load_execution_yaml(text, self.root)
        self.assertIn("UNSUPPORTED_VERSION", _codes(caught.exception))
        self.assertIn("UNKNOWN_FIELD", _codes(caught.exception))

    def test_permission_values_are_not_coerced_from_boolean_scalars(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("repo_write: human", "repo_write: true", 1)
        self.assertProjectIssue(text, "INVALID_PERMISSION", "$.authority.requested.repo_write")

    def test_oversized_input_is_rejected_before_parsing(self) -> None:
        with self.assertRaises(ContractValidationError) as caught:
            load_project_yaml(("x" * (1024 * 1024 + 1)).encode("utf-8"), self.root)
        self.assertEqual(_codes(caught.exception), ["INPUT_TOO_LARGE"])

    def test_absolute_paths_are_rejected(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("docs/requirements.md", "/tmp/requirements.md", 1)
        self.assertProjectIssue(text, "ROOT_ESCAPE", "$.sources.requirements[0]")

    def test_parent_traversal_paths_are_rejected(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("docs/requirements.md", "../requirements.md", 1)
        self.assertProjectIssue(text, "ROOT_ESCAPE", "$.sources.requirements[0]")

    def test_symlink_escapes_are_rejected(self) -> None:
        outside = self.root.parent / "outside-ad01"
        outside.mkdir(exist_ok=True)
        self.addCleanup(lambda: shutil.rmtree(outside, ignore_errors=True))
        self.root.joinpath("escape").symlink_to(outside, target_is_directory=True)
        text = _fixture("PROJECT.configured.yaml").replace("docs/requirements.md", "escape/requirements.md", 1)
        self.assertProjectIssue(text, "ROOT_ESCAPE", "$.sources.requirements[0]")

    def test_case_colliding_roots_are_rejected(self) -> None:
        text = _fixture("PROJECT.configured.yaml").replace("- src\n      - docs/Planning Space", "- src\n      - SRC", 1)
        self.assertProjectIssue(text, "CASE_COLLISION", "$.sources.discovery.roots[1]")


class Ad01Ac3ReadinessPredicateTests(unittest.TestCase):
    def readiness(self, **overrides: Any) -> Any:
        evaluate_readiness = _validation_api("evaluate_readiness")
        values = dict(
            repository=RepositoryState.ALIGNED,
            deployment=DeploymentState.CONFIGURED,
            validation=ValidationState.PASSED,
            admission=AdmissionState.ALLOW,
            schedule=ScheduleState.PAUSED,
            execution=ExecutionState.IDLE,
            resource=ResourceState.AVAILABLE,
            delivery=DeliveryState.DELIVERED,
            operator_grant_current=True,
            grant_content_bound=True,
            enforcement=EnforcementAssurance.ENFORCED,
            ownership_conflict=False,
            drift_conflict=False,
            eligible_approved_milestones=1,
            dependencies_satisfied=True,
            base_policy_satisfied=True,
        )
        values.update(overrides)
        return evaluate_readiness(ReadinessInputs(**values))

    def test_aligned_can_coexist_with_readiness_predicates_false(self) -> None:
        result = self.readiness(deployment=DeploymentState.ABSENT)
        self.assertTrue(result.aligned)
        self.assertFalse(result.ready_for_enable)
        self.assertFalse(result.ready_to_dispatch)

    def test_ready_for_enable_can_coexist_with_dispatch_false_when_no_work_is_eligible(self) -> None:
        result = self.readiness(eligible_approved_milestones=0)
        self.assertTrue(result.ready_for_enable)
        self.assertFalse(result.ready_to_dispatch)
        self.assertIn("NO_ELIGIBLE_APPROVED_MILESTONE", result.reasons)

    def test_exactly_one_eligible_approved_milestone_can_be_dispatch_ready(self) -> None:
        result = self.readiness()
        self.assertTrue(result.ready_for_enable)
        self.assertTrue(result.ready_to_dispatch)

    def test_active_execution_blocks_dispatch_without_changing_enable_readiness(self) -> None:
        result = self.readiness(execution=ExecutionState.EXECUTING)
        self.assertTrue(result.ready_for_enable)
        self.assertFalse(result.ready_to_dispatch)
        self.assertIn("EXECUTION_NOT_IDLE", result.reasons)

    def test_unknown_resource_blocks_dispatch_without_changing_enable_readiness(self) -> None:
        result = self.readiness(resource=ResourceState.UNKNOWN)
        self.assertTrue(result.ready_for_enable)
        self.assertFalse(result.ready_to_dispatch)
        self.assertIn("RESOURCE_NOT_AVAILABLE", result.reasons)

    def test_schedule_state_is_reported_independently_from_enable_readiness(self) -> None:
        paused = self.readiness(schedule=ScheduleState.PAUSED)
        enabled = self.readiness(schedule=ScheduleState.ENABLED)
        self.assertEqual(paused.ready_for_enable, enabled.ready_for_enable)


class Ad01Ac4IdentityTests(unittest.TestCase):
    def binding(self, **overrides: Any) -> InstallationBinding:
        values = dict(
            schema_version=1,
            installation_id="install-a",
            project_id="123e4567-e89b-12d3-a456-426614174000",
            repo_realpath="/repo/original",
            git_common_dir_realpath="/repo/original/.git",
            profile_identity="profile-a",
            service_identity="service-a",
            root_binding_policy="exact",
            runtime_capability_manifest_ref="capability.json",
            model_routes=(("supervisor", "gpt-5.5"),),
            auth_account_refs=("acct-redacted",),
            resource_policy="default",
            deployment_grant_ref="grants/current.yaml",
            skill_hash="a" * 64,
            delivery_target_ref="delivery/local",
            cron_id=None,
            cron_ownership=None,
            desired_enabled=False,
            deployment_epoch=1,
            project_slug="ad01-synthetic",
        )
        values.update(overrides)
        return InstallationBinding(**values)

    def identity(self, existing: tuple[InstallationBinding, ...], **kwargs: Any) -> str:
        check_installation_identity = _validation_api("check_installation_identity")
        result = check_installation_identity(existing_bindings=existing, **kwargs)
        return _outcome(result)

    def test_existing_binding_matches_same_project_and_roots(self) -> None:
        binding = self.binding()
        outcome = self.identity(
            (binding,),
            project_id=binding.project_id,
            project_slug=binding.project_slug,
            repo_realpath=binding.repo_realpath,
            git_common_dir_realpath=binding.git_common_dir_realpath,
        )
        self.assertIn("EXISTING_BINDING_MATCH", outcome)

    def test_slug_collision_does_not_adopt_different_project_id(self) -> None:
        binding = self.binding()
        outcome = self.identity(
            (binding,),
            project_id="223e4567-e89b-12d3-a456-426614174000",
            project_slug=binding.project_slug,
            repo_realpath="/repo/other",
            git_common_dir_realpath="/repo/other/.git",
        )
        self.assertIn("SLUG_COLLISION", outcome)

    def test_same_project_id_at_different_root_requires_new_installation(self) -> None:
        binding = self.binding()
        outcome = self.identity(
            (binding,),
            project_id=binding.project_id,
            project_slug="clone",
            repo_realpath="/repo/clone",
            git_common_dir_realpath="/repo/clone/.git",
        )
        self.assertIn("NEW_INSTALLATION_REQUIRED", outcome)

    def test_same_root_with_different_git_common_dir_is_an_installation_conflict(self) -> None:
        binding = self.binding()
        outcome = self.identity(
            (binding,),
            project_id=binding.project_id,
            project_slug=binding.project_slug,
            repo_realpath=binding.repo_realpath,
            git_common_dir_realpath="/repo/alternate/.git",
        )
        self.assertIn("INSTALLATION_CONFLICT", outcome)


class Ad01Ac5AuthorityTests(SyntheticRepoTestCase):
    def test_effective_permission_uses_most_restrictive_boundary_truth_table(self) -> None:
        effective_permission = _validation_api("effective_permission")
        ordered = (Permission.DENIED, Permission.HUMAN, Permission.AUTONOMOUS)
        for requested in ordered:
            for operator in ordered:
                for native in ordered:
                    for enforcement in ordered:
                        with self.subTest(requested=requested, operator=operator, native=native, enforcement=enforcement):
                            self.assertEqual(
                                effective_permission(requested, operator, native, enforcement),
                                min(requested, operator, native, enforcement),
                            )

    def test_missing_permission_boundary_fails_closed(self) -> None:
        effective_permission = _validation_api("effective_permission")
        self.assertEqual(
            effective_permission(Permission.AUTONOMOUS, None, Permission.AUTONOMOUS, Permission.AUTONOMOUS),
            Permission.DENIED,
        )

    def test_provider_names_and_status_filenames_create_only_permission_requests(self) -> None:
        project = load_project_yaml(_fixture("PROJECT.provider-names.yaml"), self.root)
        self.assertEqual(project.authority.permission_for("openai"), Permission.AUTONOMOUS)
        effective_permission = _validation_api("effective_permission")
        self.assertEqual(
            effective_permission(
                project.authority.permission_for("openai"),
                Permission.DENIED,
                Permission.AUTONOMOUS,
                Permission.AUTONOMOUS,
            ),
            Permission.DENIED,
        )

    def test_imported_approved_status_label_does_not_satisfy_approval_receipt(self) -> None:
        text = _fixture("EXECUTION.one-approved.yaml").replace("receipt_ref: receipts/ad01-approval.yaml", "receipt_ref: null")
        with self.assertRaises(ContractValidationError) as caught:
            load_execution_yaml(text, self.root, verification_ids=("unit",))
        self.assertIn("RECEIPT_REQUIRED", _codes(caught.exception))


class Ad01F66ExecutionGraphTests(SyntheticRepoTestCase):
    def test_empty_execution_index_is_structurally_valid(self) -> None:
        index = load_execution_yaml(_fixture("EXECUTION.empty.yaml"), self.root, verification_ids=("unit",))
        self.assertEqual(index.milestones, ())

    def test_configured_project_and_approved_index_load_together(self) -> None:
        project = load_project_yaml(_fixture("PROJECT.configured.yaml"), self.root)
        index = load_execution_yaml(_fixture("EXECUTION.one-approved.yaml"), self.root, project=project)
        self.assertEqual(len(index.milestones), 1)
        self.assertEqual(index.milestones[0].approval.state, ApprovalState.APPROVED)

    def test_duplicate_ids_missing_dependencies_cycles_revoked_approval_and_missing_scope_fail(self) -> None:
        with self.assertRaises(ContractValidationError) as caught:
            load_execution_yaml(_fixture("EXECUTION.graph-invalid.yaml"), self.root, verification_ids=("unit",))
        codes = set(_codes(caught.exception))
        self.assertIn("DUPLICATE_ID", codes)
        self.assertIn("MISSING_DEPENDENCY", codes)
        self.assertIn("DEPENDENCY_CYCLE", codes)
        self.assertIn("APPROVAL_REVOKED", codes)
        self.assertIn("REQUIRED", codes)

    def test_project_id_mismatch_fails_closed(self) -> None:
        project = load_project_yaml(_fixture("PROJECT.configured.yaml"), self.root)
        text = _fixture("EXECUTION.empty.yaml").replace(project.project.id, "223e4567-e89b-12d3-a456-426614174000", 1)
        with self.assertRaises(ContractValidationError) as caught:
            load_execution_yaml(text, self.root, project=project)
        self.assertIn("PROJECT_ID_MISMATCH", _codes(caught.exception))

    def test_null_execution_project_id_fails_closed_with_or_without_project(self) -> None:
        text = _fixture("EXECUTION.empty.yaml").replace(
            "123e4567-e89b-12d3-a456-426614174000", "null", 1
        )
        for project in (None, load_project_yaml(_fixture("PROJECT.configured.yaml"), self.root)):
            with self.subTest(bound=project is not None), self.assertRaises(ContractValidationError) as caught:
                load_execution_yaml(text, self.root, project=project)
            self.assertIn("TYPE", _codes(caught.exception))


class Ad01HostRecordAndMigrationTests(unittest.TestCase):
    def validation_receipt(self, **overrides: Any) -> dict[str, Any]:
        receipt: dict[str, Any] = {
            "schema_version": 1,
            "gate_id": "dispatch",
            "evidence_class": "LIVE",
            "probe_id": "read-only-probe",
            "installation_id": "install-a",
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "invocation_source": "operator-cli",
            "observed_at": "2026-09-19T00:00:00Z",
            "expires_at": "2026-09-20T00:00:00Z",
            "capability_fingerprint": "capability-v1",
            "bound_hashes": ["a" * 64],
            "repo_revision": "revision-a",
            "dirty_input_fingerprint": "clean",
            "route_identity": "redacted-route",
            "native_trace_refs": ["trace/native-1"],
            "allowed_effects": ["repo_read"],
            "observed_effects": ["repo_read"],
            "cleanup_state": "COMPLETE",
            "result": "PASS",
            "invalidation_keys": ["runtime-generation"],
        }
        receipt.update(overrides)
        return receipt

    def test_public_models_are_frozen_and_typed_record_validators_are_exported(self) -> None:
        contracts = importlib.import_module("autodev.contracts")
        result = contracts.validate_command_result(
            {
                "schema_version": 1,
                "operation": "status",
                "outcome": "NOT_READY",
                "checks": [],
                "warnings": [],
                "planned_changes": [],
                "applied_changes": [],
                "next_safe_action": None,
            }
        )
        with self.assertRaises(FrozenInstanceError):
            result.outcome = "PASS"
        for name in (
            "validate_installation_binding",
            "validate_mutation_grant",
            "validate_approval_receipt",
            "validate_validation_receipt",
            "validate_operation_record",
        ):
            self.assertTrue(callable(getattr(contracts, name)))

    def test_host_mapping_record_rejects_unknown_fields_and_versions(self) -> None:
        with self.assertRaises(ContractValidationError) as caught:
            validate_mapping_record(
                {"schema_version": 2, "installation_id": "install-a", "secret": "not allowed"},
                record_name="installation",
                allowed_fields={"installation_id"},
                required_fields={"installation_id"},
            )
        self.assertIn("UNSUPPORTED_VERSION", _codes(caught.exception))
        self.assertIn("UNKNOWN_FIELD", _codes(caught.exception))

    def test_live_pass_validation_receipt_requires_native_trace(self) -> None:
        validate = _validation_api("validate_validation_receipt")
        with self.assertRaises(ContractValidationError) as caught:
            validate(self.validation_receipt(native_trace_refs=[]))
        self.assertIn("NATIVE_TRACE_REQUIRED", _codes(caught.exception))

    def test_simulated_and_nonpassing_receipts_cannot_be_mistaken_for_live_pass(self) -> None:
        validate = _validation_api("validate_validation_receipt")
        simulated = validate(
            self.validation_receipt(evidence_class="SIMULATED", native_trace_refs=[], result="PASS")
        )
        failed = validate(self.validation_receipt(native_trace_refs=[], result="FAIL"))
        self.assertEqual(simulated.evidence_class, "SIMULATED")
        self.assertEqual(failed.result, "FAIL")

    def test_approval_and_grant_content_digests_are_sha256(self) -> None:
        validate_approval = _validation_api("validate_approval_receipt")
        validate_grant = _validation_api("validate_mutation_grant")
        approval = {
            "schema_version": 1,
            "receipt_id": "receipt-a",
            "operator_identity": "operator-a",
            "operator_action": "approve",
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "installation_id": "install-a",
            "artifact_digests": ["not-a-digest"],
            "operation_classes": ["repo_write"],
            "scope": ["src"],
            "expires_at": "2026-09-20T00:00:00Z",
            "revocation_epoch": 1,
        }
        with self.assertRaises(ContractValidationError) as caught:
            validate_approval(approval)
        self.assertIn("INVALID_DIGEST", _codes(caught.exception))

        grant = {
            "schema_version": 1,
            "grant_id": "grant-a",
            "operator_identity": "operator-a",
            "operator_action": "grant",
            "installation_id": "install-a",
            "operation_classes": ["repo_write"],
            "repository_membership_rule": "exact",
            "managed_worktree_membership_rule": "registered-only",
            "protected_files": ["PROJECT.yaml"],
            "protected_refs": ["refs/heads/main"],
            "allowed_routes": ["redacted-route"],
            "artifact_hashes": ["a" * 64],
            "resource_constraints": {"budget": "bounded"},
            "expires_at": "2026-09-20T00:00:00Z",
            "revocation_epoch": 1,
            "enforcement_backend": "sandbox",
            "content_digest": "b" * 64,
        }
        for field, invalid_value in (
            ("artifact_hashes", ["not-a-digest"]),
            ("content_digest", "not-a-digest"),
        ):
            with self.subTest(field=field), self.assertRaises(ContractValidationError) as caught:
                validate_grant({**grant, field: invalid_value})
            self.assertIn("INVALID_DIGEST", _codes(caught.exception))

    def test_migration_preview_records_digest_and_never_writes(self) -> None:
        preview_v1_migration = _validation_api("preview_v1_migration")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = b"name: Legacy\napproved: true\npaths:\n  - src\n"
            before = sorted(path.relative_to(root) for path in root.rglob("*"))
            plan = preview_v1_migration(source)
            after = sorted(path.relative_to(root) for path in root.rglob("*"))
        self.assertEqual(plan.source_sha256, hashlib.sha256(source).hexdigest())
        self.assertFalse(plan.applicable)
        self.assertFalse(plan.writes_performed)
        self.assertIn("$.approved", plan.unresolved_fields)
        self.assertEqual(before, after)

    def test_migration_preview_draft_target_contains_only_known_v2_constants(self) -> None:
        preview_v1_migration = _validation_api("preview_v1_migration")
        plan = preview_v1_migration(b"name: Legacy\n")
        draft_target = dict(plan.draft_target)
        self.assertEqual(draft_target.get("PROJECT.schema_version"), 2)
        self.assertEqual(draft_target.get("PROJECT.setup_state"), "draft")
        self.assertNotIn("approved", draft_target)

    def test_migration_preview_summary_excludes_legacy_secret_values(self) -> None:
        preview_v1_migration = _validation_api("preview_v1_migration")
        canary = "ad01-super-secret-value"
        plan = preview_v1_migration(f"credential: {canary}\n".encode())
        self.assertNotIn(canary, repr(plan))

    def test_migration_preview_uses_the_same_strict_yaml_boundary(self) -> None:
        preview_v1_migration = _validation_api("preview_v1_migration")
        with self.assertRaises(ContractValidationError) as caught:
            preview_v1_migration(b"legacy: &value yes\ncopy: *value\n")
        self.assertIn("UNSAFE_YAML", _codes(caught.exception))


class Ad01CliRegressionTests(unittest.TestCase):
    def test_all_existing_placeholder_commands_still_exit_7(self) -> None:
        for command in PLACEHOLDER_COMMANDS:
            with self.subTest(command=command):
                result = run_autodev(command)
                self.assertEqual(result.returncode, 7, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
