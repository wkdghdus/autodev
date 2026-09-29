# AD-00 implementation plan

Status: approved consensus plan
Milestone: AD-00 — Baseline, scope lock, and evidence inventory
Boundary: repository-local work under `autodev-v2/`; stop before AD-01
Context snapshot: .omx/context/AD-00-7102baac701d.md
Context SHA-256: 7102baac701d3dc4d502958c99769a3b5ed5638530fe8fb2e0c68418101c5d65
Context map SHA-256: 25a4b314812fd5ffb57b1c31ae7c01f79c8bcc62b262f64fe52eb84b7a33087f

## Scope

AD-00 establishes a deterministic, importable Python package and a fail-closed
command-line scaffold. It records the identities of the three unavailable source
reports, inventories only the files supplied with this repository, captures every
known category of future compatibility work as unresolved, provides explicitly
synthetic lifecycle examples, and supplies local tests for the scaffold and its
no-live-mutation contract.

The implementation uses the Python standard library. It does not add a dependency
or infer native Hermes or Gajae Coordinator (GJC) interfaces from historical
commands.

## Non-goals and authority boundary

AD-00 does not:

- inspect credentials, accounts, provider billing, quota, or private environment
  values;
- probe, install, upgrade, configure, start, stop, restart, or mutate Hermes, GJC,
  gateways, brokers, cron jobs, profiles, services, or account state;
- call a model, network service, messaging service, or native session API;
- create a real GJC session or managed worktree;
- define AD-01 schemas, grant operational authority, certify enforcement, or claim
  live compatibility;
- reconstruct the bodies of the three unavailable historical reports; or
- modify the normative specification, acceptance matrix, milestone files, or
  supplied reference metadata.

Any missing external capability remains `BLOCKED_EXTERNAL` or `UNSUPPORTED`.
Neither a fixture nor a local unit test can turn it into a live pass.

## Expected file effects

Only new AD-00-owned files are expected:

- `pyproject.toml`;
- `src/autodev/**`;
- `tests/**`;
- `fixtures/**`;
- `templates/environment-manifest.json`;
- `docs/plans/AD-00-plan.md`;
- `docs/baseline/**`;
- `docs/evidence/**`; and
- after implementation and test execution, `docs/verification/AD-00.md`.

No path outside `autodev-v2/` is an implementation output. Local, Git-excluded
`.omx/` planning state is workflow metadata, not a product deliverable. The effect
audit is an instrumented local test over exercised code paths; it is not an OS
sandbox or proof about unobserved external processes.

## Acceptance contract

| ID | Required evidence |
| --- | --- |
| AD-00-AC1 | `autodev` imports; global CLI help exits 0; the complete local unit suite exits 0. |
| AD-00-AC2 | S1–S3 retain exact IDs, titles, filenames, and SHA-256 identities; record bodies are unavailable and not live-verified. |
| AD-00-AC3 | The baseline enumerates unresolved compatibility categories for Hermes, GJC, runtimes, routes/accounts, profiles, scheduling, messaging, host/process lifecycle, and enforcement. |
| AD-00-AC4 | Instrumented help/placeholder execution records zero subprocess, network, or live-path effects; changed paths remain in the expected repository-local set. |
| AD-00-AC5 | Every future command is absent or, as chosen here, an explicit non-passing placeholder with the exact contract below. |
| F63 | An unavailable external service/API/capability is classified `BLOCKED_EXTERNAL` or `UNSUPPORTED`, with no fabricated live `PASS`. |

Evidence classes have distinct meanings in AD-00:

- `PROVIDED_FILE`: a fact read from a repository file supplied to this task;
- `SIMULATED`: an intentionally synthetic fixture, never a live observation;
- `NOT_RUN`: a check or operation not attempted; and
- `BLOCKED_EXTERNAL`: a live check that requires unavailable or unauthorized
  external access. It is not a pass.

## Exact future-command placeholder contract

The complete placeholder set is:

`init`, `approve`, `doctor`, `preflight`, `onboard`, `validate`, `enable`,
`disable`, `cycle`, `repair`, `recover`, `status`, and `list`.

For every direct placeholder invocation:

1. The process exits exactly `7`, meaning unsupported capability.
2. No command-specific option is accepted or interpreted and no command behavior
   is implemented.
3. The command performs no repository discovery, live probing, file mutation,
   process inspection, subprocess invocation, credential or account inspection,
   network/model call, Hermes/GJC/broker/cron interaction, or native session
   creation.
4. Global `--help` may list the names and exit `0`; that listing does not make any
   command supported.
5. Standard output is deterministic JSON containing at least:

```json
{
  "schema_version": 1,
  "command": "<invoked placeholder>",
  "outcome": "UNSUPPORTED",
  "implemented": false,
  "evidence_class": "NOT_RUN",
  "live_verified": false
}
```

Tests invoke all 13 names and require this exact fail-closed behavior.

## Implementation sequence

1. Preserve this plan before source edits and keep all work inside the expected
   file-effect set.
2. Add `pyproject.toml`, `src/autodev/__init__.py`, `src/autodev/__main__.py`, and
   a standard-library CLI implementing import/help/version plus the exact
   placeholder contract.
3. Add S1–S3 identity-only evidence records from the bounded
   `reference/SOURCES.md` selection in the canonical context snapshot; do not
   recreate absent report text or inspect sources outside that selection.
4. Add a sanitized human-readable baseline and machine-readable inventory based
   only on provided files. Mark all live observations `NOT_RUN` or
   `BLOCKED_EXTERNAL` and enumerate later compatibility unknowns.
5. Add six inert lifecycle fixtures (READY, active, uncertain, verifying,
   human-blocked, completed) and a manifest. Label every fixture `SIMULATED` and
   `live_verified: false`.
6. Add `templates/environment-manifest.json` with unknown/null values for future
   authorized probing; do not seed historical machine-specific defaults.
7. Add narrow evidence/redaction helpers and an instrumented local effect harness.
   Do not describe that harness as security isolation.
8. Add `unittest` coverage for import/help, all placeholders, evidence identities,
   baseline completeness, fixture labels, redaction canaries, effect capture, and
   F63 classification.
9. Run the verification commands, inspect changed paths, and only then write the
   separate milestone verification report with the snapshot-required changed
   files, commands, exit codes, acceptance evidence, effects, limits, and handoff.

## Verification commands

Run from `autodev-v2/`:

```bash
PYTHONPATH=src python -c "import autodev; print(autodev.__version__)"
PYTHONPATH=src python -m autodev --help
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```

Then run `git diff --check`, inspect `git status --short`, and audit every changed
path. `pytest` is optional only when already present and is not a dependency or
required proof.

## ADR: explicit fail-closed placeholders

### Decision

Build a small standard-library package whose future commands exist only as
explicit unsupported placeholders. Pair it with identity-only source evidence,
a provided-file-only baseline, synthetic fixtures, deterministic tests, and a
separate verification record.

### Drivers

- Direct, repeatable evidence for AD-00-AC1 through AC5 and F63.
- Minimal local blast radius and no new dependency.
- A useful AD-01 handoff without prematurely implementing schema, authority, or
  native integration behavior.

### Alternatives considered

- **Omit future commands.** This is smaller, but proves AC5 only through parser
  rejection and gives operators less explicit guidance.
- **Implement rich JSON stubs.** Rejected because command-specific semantics would
  leak work from later milestones and could appear supported.
- **Use minimal fail-closed placeholders.** Chosen because exit 7 plus explicit
  unsupported JSON gives a directly testable boundary without native behavior.

### Consequences

The CLI surface is larger than an import-only scaffold, but every future command
is visibly non-passing. Later milestones must replace placeholders only under
their own acceptance criteria. AD-00 can be code-verified locally but cannot be
live-certified.

### Follow-ups

AD-01 may implement the real schema/state contracts after AD-00 verification.
Later, separately authorized milestones may perform installed-version and live
environment probes. No such follow-up is authorized by this plan.

## Accepted consensus-review improvements

The approved review tightened the initial proposal by freezing all 13 placeholder
names; choosing exit code 7; requiring deterministic minimal JSON; prohibiting
command options and behavior; tying verification to the bounded snapshot's
evidence contract; and documenting that the local effect harness is not OS-level proof.
These constraints are normative for this milestone and must not be relaxed to make
tests pass.
