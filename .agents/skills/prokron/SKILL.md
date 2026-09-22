---
name: prokron
description: Maintain or resume a repository's Prokron project chronicle. Use for Prokron init, work, decision, checkpoint, resume, and baseline requests.
---

# Prokron

Everything Prokron owns is inside `.prokron/`. Read
`.prokron/chronicle/README.md`. Run `.prokron/prokron status` for compiled
state and `.prokron/prokron validate` after editing authority. Interpret the
first argument as `init`, `work`, `decide`, `checkpoint`, `resume`, or `baseline`, then
follow the matching `.prokron/commands/prokron-<argument>.md` workflow. Pass
remaining arguments through:
`init` receives the entry mode, `work` the requested task, and `decide` the
decision details. Repeated `init` preserves populated records and resumes work. Run `baseline`
only when the owner explicitly asks for it.

Maintain the chronicle without waiting for an explicit Prokron request. Create
or claim every new task before implementation, give it a phase and an acceptance
contract, and append an ADR to `.prokron/chronicle/ADR/` as soon as a material
decision is made or acted on. Keep the single intent at the exact execution point. A task is
done only when its frozen contract in `ACCEPTANCE.md` has sufficient evidence.

Checkpoint automatically before a handoff, compaction, session ending, or any
known or estimated context, token, time, rate, or quota limit. Without telemetry,
checkpoint after meaningful milestones and before long-running work.
