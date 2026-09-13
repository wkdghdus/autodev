# Sources and limits

## Uploaded incident reports: primary basis

[S1] Lessons Learned from Nous Autonomous Supervisor Setup.
File: `Pasted markdown(2).md`.
SHA-256: `6ace331bbf3f2ee7af23b46f8cbd579290c434e0f3d913a0e0eccc2d035b928d`.

[S2] Hermes + Gajae Automated Onboarding: Lessons from Nous.
File: `Pasted markdown (2).md`.
SHA-256: `d0ea218d74b658f174bd8566c8bf017981b06d7df51a12df4ecb94e997bf052b`.

[S3] Lessons Learned From Nous Autonomous Onboarding.
File: `Pasted markdown (3).md` (begins with an introductory paragraph before the main heading).
SHA-256: `bdac1bb84c3de3f695462d371ee3509e9a98007f9091b2292ad6f83eb2dd43b5`.

These are the user's retrospective accounts. The package treats their incidents as reported observations, not independently reproduced current machine facts. Account IDs, host paths, model names, version numbers, and session IDs in those files are not universal defaults. Original files are not copied into this distributable package.

## External primary-source checks

Consulted while revising the specification on September 12, 2026 (America/Toronto). Documentation is mutable and does not supersede the installed-version compatibility probe.

[W1] Hermes, Scheduled Tasks (Cron).
`https://hermes-agent.nousresearch.com/docs/user-guide/features/cron/`
Relevance: effective job model selection, cron workdir, native paused canaries, scheduling and execution/delivery separation. Use installed capability checks rather than freeze current docs into hardcoded flags.

[W2] Hermes, Credential Pools.
`https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools/`
Relevance: account/credential rotation is a separate route from cross-provider fallback.

[W3] Hermes, Fallback Providers.
`https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers/`
Relevance: primary and auxiliary provider resolution must be audited separately.

[W4] Gajae Code, public repository README.
`https://github.com/Yeachan-Heo/gajae-code`
Relevance: installation distribution matters; standalone binary instructions do not require Bun. This is not a claim about the user's installed distribution.

[W5] Gajae Code, Coordinator MCP bridge.
`https://github.com/Yeachan-Heo/gajae-code/blob/main/docs/hermes-mcp-bridge.md`
Relevance: native Coordinator, setup, managed worktree selector, and durable turns. The historical incident's SDK behavior must be checked against the installed API.

[W6] Claude Help Center, Manage usage credits for paid Claude plans.
`https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans`
Relevance: authentication and subscription membership alone do not prove that usage beyond included limits cannot be charged.

[W7] OpenAI Help Center, Using Credits for Flexible Usage in ChatGPT (Personal plans).
`https://help.openai.com/en/articles/12642688`
Relevance: the account's credit/usage controls need separate inspection from its OAuth credential mechanism. This package does not determine the user's plan-specific billing settings.

[W8] Hermes, Configuration.
`https://hermes-agent.nousresearch.com/docs/user-guide/configuration/`
Relevance: local tools execute with user filesystem access; a cwd/profile is not a sandbox.

## What was not verified

No command was run on the user's laptop. No provider account or credential store was inspected. No live Hermes/GJC integration, broker recovery, cron run, gateway restart, or Discord delivery was performed. No feature in the specification should be reported implemented merely because its source material describes it.
