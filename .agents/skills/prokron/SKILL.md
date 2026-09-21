---
name: prokron
description: Maintain or resume a repository's Prokron project chronicle. Use for Prokron init, work, decision, checkpoint, and resume requests.
---

# Prokron

Read `prokron/README.md`. Run `./bin/prokron status` for compiled state and
`./bin/prokron validate` after editing authority. Interpret the first argument as `init`, `work`,
`decide`, `checkpoint`, or `resume`, then follow the matching
`commands/prokron-<argument>.md` workflow. Pass remaining arguments through:
`init` receives the entry mode, `work` the requested task, and `decide` the
decision details. Repeated `init` preserves populated records and resumes work.

Maintain the chronicle without waiting for an explicit Prokron request. Create
or claim every new task before implementation, give it a phase and an acceptance
contract, and append an ADR to `prokron/ADR/` as soon as a material decision is
made or acted on. Keep the single intent at the exact execution point. A task is
done only when its frozen contract in `ACCEPTANCE.md` has sufficient evidence.

Checkpoint automatically before a handoff, compaction, session ending, or any
known or estimated context, token, time, rate, or quota limit. Without telemetry,
checkpoint after meaningful milestones and before long-running work.
