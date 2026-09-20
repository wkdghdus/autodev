# AD-01 implementation plan

## Scope

Implement repository-local, immutable contract models and pure validation/evaluation APIs for PROJECT schema 2, EXECUTION schema 2, and version-1 host/evidence/result records. Preserve every AD-00 CLI placeholder and avoid discovery, persistence, approval application, native integration, credentials, or live effects.

## Work sequence

1. Add the pinned YAML runtime dependency and a strict YAML 1.2 ingestion boundary with size, document, tag, alias/anchor, merge-key, duplicate-key, key-type, and source-location controls.
2. Add immutable models and enums for repository, deployment, validation, admission, schedule, execution, resource, delivery, authority, identity, receipts, journals, command results, and migration previews.
3. Validate PROJECT and EXECUTION mappings without coercion, including portable paths, source-bound milestone graphs, approvals, verification references, and project identity agreement.
4. Implement pure permission intersection, installation identity checks, orthogonal readiness evaluation, and conservative V1 migration preview.
5. Add synthetic AD-01 fixtures and unittest coverage for AD-01-AC1 through AC5 and faults F02, F03, F08, and F66 while rerunning all AD-00 regression tests.
6. Run the milestone verification commands, audit changed paths/effects, and record CODE_VERIFIED evidence and known limits in `docs/verification/AD-01.md`.

## Boundaries and rollback

- All loaders accept explicit content and an explicit repository root; none discover or write files.
- Tests use temporary repositories and synthetic records only.
- Migration output is draft-only and has no apply method.
- Rollback is deletion of AD-01-owned files plus restoration of the dependency declaration; AD-00 artifacts and CLI behavior are not modified.
