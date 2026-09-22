# AD-02 implementation plan

## Scope

Add repository-independent local safety primitives for explicit POSIX filesystem
roots. The milestone provides atomic byte storage, ordered kernel locks, bounded
redacted subprocess execution, durable idempotent operation journals, and a
strict passive Git adapter. It does not enable any CLI command or authorize live
configuration, credential, provider, scheduler, broker, or repository mutation.

## Work sequence

1. Implement `autodev.safety.locks` around non-blocking POSIX `flock`, with
   account -> installation -> repository ordering, diagnostic-only metadata,
   per-thread ownership tracking, and fail-closed unsupported-platform results.
2. Implement `autodev.safety.storage` for explicit roots and relative targets.
   Reject traversal and symlinks, compare expected SHA-256 state while locked,
   write mode-0600 same-directory temporary files, flush/fsync, persist a
   content-free recovery record, replace atomically, and fsync the parent.
3. Implement deterministic recovery classification for old-present,
   new-present, conflict, and corrupt/unknown states. Only unambiguous states may
   be finalized; ambiguous state blocks later mutation.
4. Implement `autodev.safety.command` with immutable specifications/results,
   explicit cwd and environment allowlists, `shell=False`, a fresh process
   group, timeout termination, bounded streaming capture, and redaction of every
   returned or raised string. Environment diagnostics expose keys only.
5. Implement `autodev.safety.journal` using strict canonical JSON and atomic
   storage. Persist PREPARED before returning a new operation, derive identity
   from persisted logical fields, enforce compare-and-set state transitions,
   preserve identical retries, reject changed arguments, and retain compact
   tombstones when eligible terminal records are pruned.
6. Implement `autodev.safety.git` as a command-runner-backed allowlist for
   `rev-parse`, porcelain-v2 `status`, `ls-files`, and `check-ignore`. Supply a
   sanitized environment and `-c` overrides that disable optional locks,
   system/global configuration, hooks, fsmonitor, external diff, textconv, and
   filters; reject unsupported arguments before process creation.
7. Add temporary-fixture and child-process tests for AD-02-AC1 through AC5 and
   F07, F34, F36, F38, F56, F69, and F70. Preserve the 13 deterministic exit-7
   CLI placeholders and rerun every AD-00/AD-01 regression.

## API and safety boundaries

- Public records are frozen dataclasses; public failures use typed exceptions or
  explicit result enums and never leak secret-bearing source strings.
- Atomic storage is format-neutral. JSON canonicalization belongs to the journal
  layer and rejects NaN, non-string object keys, and non-JSON values.
- Kernel ownership is authoritative for locks. Metadata timestamps, PIDs, host
  names, and nonces are never grounds for lock theft.
- Multiple held locks prohibit command and Git subprocess execution. No lock is
  distributed across hosts, and no filesystem rename is represented as a
  multi-system transaction.
- Recovery and journal files contain identities, timestamps, modes, UID/GID, and
  digests only; they never contain replaced bytes, canonical arguments, command
  environment values, or native secret material.
- Tests write only below temporary directories. No default home-directory root,
  implicit current-directory target, network operation, native dispatch, or
  actual project repository mutation is in scope.

## Verification and completion

Run the full unittest suite, focused multi-process/fault tests, package imports,
bytecode compilation, `git diff --check`, and an effect/path audit confirming
all new writes occurred under temporary fixtures. Record the exact commands,
counts, supported host/runtime, known limitations, and `CODE_VERIFIED` result in
`docs/verification/AD-02.md`. Completion does not certify a live deployment.

## Rollback

Remove the AD-02 safety package, its tests, and its plan/verification documents.
The committed AD-01 revision remains a complete fail-closed predecessor and no
live system requires cleanup.
