# Evidence map and design decisions

## What the uploaded failures establish

The reports describe a layered reliability problem: a successful check often exercised a different process, route, lifecycle, or authority layer from the failing one. V2 keeps those observed causes separate rather than using one generic "integration healthy" flag. Historical incidents remain historical; no current machine diagnosis is asserted here.

| Lesson | Uploaded basis | Reported bottleneck | V2 requirement | Milestones | Fault coverage |
|---|---|---|---|---|---|
| L01 | S1 section 1 | Hermes/GJC/worker responsibilities blurred | Keep runtime, lifecycle, implementation and guard roles separate. | AD-00/13 | F57 |
| L02 | S1 sections 2-3; S2 sections 8-10; S3 section 7 | MCP registered or connected but not callable | Separate enabled, discovery, filtering, fresh visibility and real invocation gates. | AD-08/09 | F12/F15 |
| L03 | S2 bottleneck table | Tool Search was suspected incorrectly | Preserve search behavior; never reset unrelated disabled toolsets. | AD-08/09 | F13 |
| L04 | S1 section 4; S3 section 6 | Skill file existed outside actual usable profile context | Versioned profile-local install and fresh injection proof. | AD-08/13 | F16 |
| L05 | S1 section 5; S3 sections 1-2 | Explicit state needed but layout varied | Dynamic discovery -> reviewed source-bound machine index, any supported path. | AD-03/04 | F04/F66 |
| L06 | S1 section 6 | Existing repositories/profiles could be overwritten | Inspect, own, preview, reconcile; preserve comments and human decisions. | AD-02/03/16 | F06/F07/F62 |
| L07 | S1 sections 7-9 | Clean shell did not cover durable credentials | Scoped metadata/coverage audit, no payload reads or SELECT *. | AD-06 | F19 |
| L08 | S1 section 8 | Provider label did not reveal authentication type | Separate mechanism, effective route, entitlement and overage evidence. | AD-06 | F22 |
| L09 | S1 section 10 | models.yml could override the expected route | Audit profile/model/endpoint overrides across every used role. | AD-06 | F20 |
| L10 | S1 section 11; S3 section 5 | Service environment differed from shell | Probe actual distinct execution surfaces; do not trust shell alone. | AD-08/17/18 | F41/F50 |
| L11 | S1 sections 12-13 | Cron inherited/drifted from expected model | Verify actual installed resolution and pin each job route; invalidate on drift. | AD-18 | F23 |
| L12 | S1 section 14 | Fallback could escape subscription boundary | Audit reachable pools and auxiliaries as well as cross-provider fallback. | AD-06/07 | F21 |
| L13 | S1 sections 15-17; S3 section 12 | Frequent/endless/recursive scheduled agents wasted usage | Bound cycles; cheap pre-inference gate; deny recursive scheduling. | AD-07/13/18 | F39/F53/F68 |
| L14 | S1 section 18; S3 section 8 | Fresh wakes could duplicate milestone work | Single guarded lane, native reconciliation and second-wake test. | AD-11/12 | F30/F35 |
| L15 | S1 section 19; S3 section 23 | Cron still depended on awake local compute | Declare topology; report stale heartbeat; coalesce missed wakes. | AD-17/18 | F54 |
| L16 | S1 sections 20-21; S3 sections 13-15 | Engineering autonomy risked product/criteria/Git authority | Human content-bound approval; protected grant; verified branch != merged base. | AD-04/12/14 | F44/F45/F57 |
| L17 | S2 sections 2-3 | GJC update and Bun dependency failed mid-upgrade | Detect distribution/dependency first; inspect actual version after approved change. | AD-05 | F10/F11 |
| L18 | S2 section 7 | MCP PATH and lifecycle selector were conflated | Absolute outer executable; deterministic MCP PATH; preserve typed selector. | AD-05/09 | F14 |
| L19 | S2 sections 5-6 | Transport smoke hid invalid Bedrock model credentials | Separate route inference from workflow and end-to-end probes. | AD-06/15 | F17/F18 |
| L20 | S2 sections 4, 11-12 | spawn_failed hid worktree_bucket_not_ignored | Preflight actual bucket and run supported low-level lifecycle diagnosis. | AD-03/10 | F09/F27/F28 |
| L21 | S2 sections 13-14 | Unsupported broker.shutdown was mistaken for stale runtime | Use native identity/generation evidence; do not kill guessed processes. | AD-05/19 | F29/F38 |
| L22 | S3 sections 3, 5 | Ruby environment caused apparent verification failure | Validate verifier runtime before attributing failure to implementation. | AD-08/14/17 | F41 |
| L23 | S3 section 4 | Different HEAD did not necessarily stale source verification | Complete relevant-input applicability check, not SHA inequality alone. | AD-14 | F42/F43 |
| L24 | S3 section 9 | list_sessions missed the active coordination state | Multi-source provenance and conflict-aware reconciliation. | AD-11 | F30/F32 |
| L25 | S3 sections 10-11 | Unavailable response coexisted with live progressing execution | Uncertainty reserves lane; durable operation key before dispatch. | AD-11/12 | F31/F33/F34 |
| L26 | S3 section 12 | Waiting synchronously could occupy the supervisor indefinitely | Non-waiting native delegation and bounded observation budget. | AD-13 | F39 |
| L27 | S3 sections 19-21 | Quota guesses/retries wasted limited worker allowance | Supported fresh telemetry; UNKNOWN denies expensive work; local status may continue. | AD-07 | F24/F26/F68 |
| L28 | S3 section 17 | AGENT.md not necessarily auto-injected as project context | Detect and explicitly declare context; no silent rename. | AD-03/13 | F46 |
| L29 | S3 section 18 | Chat/Discord success did not prove cron deployment path | Actual scheduled-worker canary with per-surface fingerprint. | AD-17/18 | F50 |
| L30 | S3 section 22 | Invisible cron work was difficult to trust | Explicit delivery proof and separate delivery/execution status. | AD-17/19 | F55/F56 |
| L31 | S3 section 24 | Previous agent text could become stale truth | Fresh repo/native observations; historical messages are evidence only. | AD-11/14 | F30/F42 |
| L32 | S3 section 16; S2 sections 12, 15-17 | Skipping staged validation hid downstream faults | Authorized gate ladder, one execution, second wake, terminal proof before enable. | AD-15/18/22 | F48/F49/F65 |

## Conflicts resolved explicitly

### D1. Dynamic roadmap discovery versus mandatory explicit state

[S1 section 5] asks for an explicit manifest; [S3 section 1] rejects a single hardcoded roadmap location. V2 accepts arbitrary source layouts and requires a reviewed execution index that references them. This retains both safety objectives instead of silently choosing one report over the other.

### D2. Init as full onboarding versus repo-only init

The incident reports sometimes call the entire infrastructure flow "init". V1.1 separated init from onboard. V2 retains that useful command boundary and adds validate for experiments. The combined guided workflow may present all stages, but init alone never creates sessions, spends model usage, or enables schedules.

### D3. OAuth versus subscription-only billing

[S1] documents OAuth and API-key absence checks. V2 preserves them but does not accept OAuth as sufficient billing proof. Account credit/overage controls and all reachable model routes need separate evidence. This is a strengthened design requirement, supported by the primary-source account documentation [W6, W7], not a claim that the uploaded audit proved zero cost.

### D4. Historical flags/versions versus portable capability checks

Values such as GJC 0.16.6, Bun 1.4.0, a fixed tool count, named model releases, and a historical model_drift_guard flag are fixtures. V2 discovers installed distribution/protocol semantics. Public documentation also changes; adapter proof on the real target remains authoritative.

### D5. Read-only versus plan-only

A planning turn can consume quota and create native state even when no product files change. Passive doctor/preflight do not run it. An explicit validation plan authorizes those costs and artifacts.

### D6. No custom database versus durable idempotency

V1 discouraged a new task database. V2 keeps that non-goal but requires a minimal intent journal and evidence store where native records alone cannot bind pre-send intent to recovered IDs. It is not another task scheduler or execution authority.

### D7. Exact repo root versus managed sibling worktrees

A hard string equality to one repo path can reject legitimate GJC worktrees; a broad parent allowlist grants too much. V2 validates registered managed-worktree membership in the intended project, plus minimal explicit runtime capabilities.

### D8. Profiles/cwd versus enforceable isolation

Profile separation is useful configuration hygiene, not a filesystem security boundary. V2 makes this limitation visible and requires actual negative tests for strict unattended certification. [W8]

### D9. Verify-complete versus safe next milestone

The earlier loop could move from verified code in one worktree to a successor based on main without the predecessor changes. V2 adds VERIFIED_UNMERGED/INTEGRATED and defaults to dependency-integrated base selection. This is a new design safeguard.

### D10. Disable versus stop everything

V2 closes new-work admission before pausing native schedules and separately reports already accepted work. Killing broker processes is not the default stop action. This is a new race/recovery safeguard.

### D11. Skill reuse versus live-file drift

Use one source artifact with versioned profile-local installations, not an unpinned shared mutable skill file. Changing the source does not silently change every enabled deployment.

### D12. Prompt guardrails versus guaranteed enforcement

Critical admission and mutation rules live in deterministic code and tested permission boundaries. A prompt-only deployment is explicitly POLICY_ONLY. V2 cannot honestly promise strict isolation or spending guarantees when a raw terminal/API route bypasses the checks.

## Additional safeguards proposed, not claimed as past incidents

Account-scoped local reservations; disable epochs; compare-before-write change plans; conservative receipt invalidation; delivery-only retries; dirty/binary/untracked recovery preservation; protected control-file enforcement; refusal to infer approval from model confidence; bounded missed-occurrence handling; source-anchored dependency bases; and simulated-versus-live evidence classes are new requirements.

## Crosswalk from V1.1

| Old milestone | V2 replacement |
|---|---|
| M0 Baseline | AD-00 |
| M1 Contract | AD-01, AD-02, AD-04 |
| M2 Init | AD-03, AD-04 |
| M3 Generic supervisor | AD-11, AD-12, AD-13 |
| M4 Nous parity | AD-21 |
| M5 Preflight | AD-05, AD-06, AD-07, AD-15 |
| M6 Hermes provisioning | AD-08, AD-17 |
| M7 Gajae provisioning | AD-09, AD-10 |
| M8 Onboarding | AD-16 |
| M9 Enable/disable/cron | AD-18, AD-19 |
| M10 Registry/status | AD-02 foundations; AD-15/16/17 reporting |
| M11 Hardening | Early AD-02/06/07/12 foundations plus AD-20 audit |
| M12 Second project | AD-22 |
| M13 Release | AD-23 |

Nous parity now follows a complete safety/integration implementation rather than blocking initial development on a half-built generic skill. Live Nous mutation is still not authorized by the parity milestone.
