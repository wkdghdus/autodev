# AD-00 sanitized baseline

Baseline kind: provided-file-only
Evidence class: `PROVIDED_FILE`
Live verified: no

This baseline describes only artifacts present in the supplied `autodev-v2/`
requirements package. It contains no credential values, account identifiers,
absolute host paths, environment dump, native session or schedule IDs, process
details, or inferred installed versions. No command was run against Hermes, GJC,
a provider, cron, a gateway, or a messaging service.

The machine-readable record is [`inventory.json`](inventory.json). Canonical
package hashes remain in `reference/SHA256SUMS.json`; source-report identities
remain in `reference/source_manifest.json` and the identity-only records under
`docs/evidence/`.

## Evidence labels

| Label | Meaning here |
| --- | --- |
| `PROVIDED_FILE` | Directly supported by a file supplied in this repository. |
| `SIMULATED` | Intentionally synthetic fixture; never a machine observation. |
| `NOT_RUN` | A check or operation was not attempted. |
| `BLOCKED_EXTERNAL` | A live check requires external access or authority not available to AD-00; never a pass. |

The provided package says it is a documentation/specification package with 24
milestones and 70 fault cases. It does not contain an existing AutoDev
implementation or the bodies of reports S1–S3. Those are file-presence facts,
not statements about any live machine.

## Supplied artifact inventory

The baseline input consists of:

- six top-level specification/session documents plus the package README;
- 24 milestone definitions, AD-00 through AD-23;
- `reference/SOURCES.md`, `reference/source_manifest.json`,
  `reference/SHA256SUMS.json`, and `reference/PACKAGE-CHECKS.json`; and
- three supplied templates: project, execution, and milestone verification.

All identities are inherited from the provided manifests. This baseline does not
rehash absent uploads or treat their recorded digests as proof of current content.

## Later compatibility unknowns

Every category below remains unresolved. `NOT_RUN` means AD-00 deliberately did
not attempt a local/live observation. `BLOCKED_EXTERNAL` means a later live proof
requires separately authorized access. Neither state is `PASS`.

### Hermes

- installation distribution, executable realpath/version, configuration schema,
  API/protocol generation, supported read/mutation/probe operations, argument
  schemas, error mappings, and restart/new-session semantics;
- native scheduling, credential-pool, fallback-provider, tool-search, MCP, skill
  injection, and redacted credential-metadata capabilities; and
- actual gateway, worker, and CLI configuration generations.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### GJC

- installation distribution, executable realpath/version, optional interpreter
  requirement, coordinator/MCP protocol generation, and supported CLI/SDK calls;
- managed-worktree selection, session/turn lifecycle, broker generation and
  identity, cancellation/shutdown semantics, idempotency support, and native
  reconciliation sources; and
- supported permission/enforcement hooks and native trace fields.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Runtimes and execution surfaces

- OS/architecture, Python and optional Bun/Ruby versions, shells, PATHs, working
  directories, executable resolution, service managers, and environment
  differences across interactive CLI, gateway, MCP, verifier, and scheduled
  worker surfaces;
- installed package generations and restart requirements; and
- availability of deterministic local tools needed by later adapters.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Routes, accounts, billing, and resources

- effective provider/model/endpoint for supervisor, cron, GJC roles, and auxiliary
  model-using services;
- credential mechanism and redacted account identity/source, credential-pool
  rotation, primary fallback, auxiliary routing, entitlement, overage/paid-credit
  controls, and enforceable route closure; and
- supported quota telemetry, units/windows/reset/freshness, account-scoped
  concurrency, reservations, retry/fan-out limits, and provider-enforced spending
  boundaries.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Profiles, repositories, and project identity

- selected Hermes profile/service identity, ownership/adoption state, loaded skill
  and context hashes, disabled toolsets, Tool Search behavior, and profile-local
  environment;
- canonical repository and Git common-directory identity, worktree topology,
  tracked/untracked/ignored state, authority artifacts, approved plan hashes, and
  protected files/refs; and
- AutoDev installation/project identity and existing host-owned registry or
  journal state.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Scheduling

- scheduler ownership, job IDs, name uniqueness, paused/unscheduled creation,
  effective job route, cwd/profile/PATH, concurrency, missed-occurrence behavior,
  readback, pause/disable semantics, and recursion prevention;
- cheap pre-inference gate support and deployment-epoch enforcement; and
- actual scheduled-worker canary behavior.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Messaging and delivery

- configured platform, profile-bound destination, allowed content, native
  acknowledgement/message IDs, retry/deduplication behavior, outbox/history
  support, and separation of execution from delivery state;
- sanitization behavior on the actual delivery path; and
- whether notification failure can pause new unattended dispatch without losing
  reconciliation capability.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Host and process lifecycle

- local/server/container topology, uptime expectations, sleep/offline behavior,
  heartbeat source, process/service ownership, PID reuse defenses, broker/worker
  generations, active or uncertain native work, locks, and restart recovery;
- gateway and scheduler ownership boundaries; and
- availability of any separately provisioned external monitoring.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

### Enforcement and safety boundaries

- enforceable filesystem roots, read-only/control-file protections, Git operation
  restrictions, network/credential/provider route controls, raw Coordinator and
  terminal bypass prevention, grant/revocation behavior, and negative-test
  capability of the actual backend;
- atomicity/durability properties for local journals, locks, reservations, and
  compare-before-write changes; and
- whether the target supports strict enforcement or only `POLICY_ONLY` guidance.

Status: `NOT_RUN`; live compatibility proof: `BLOCKED_EXTERNAL`.

## Synthetic data boundary

Lifecycle examples created by AD-00 are `SIMULATED` and have
`live_verified: false`. They are test inputs only and do not update this baseline.
No simulated record may satisfy a later mandatory live gate.

## Baseline conclusion

The only affirmative findings are identities and contents of provided repository
files. All machine, service, account, runtime, and integration claims are
`NOT_RUN` or `BLOCKED_EXTERNAL`. The baseline therefore makes no live claim and
cannot be used as a live deployment certification.
