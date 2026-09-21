# Prokron project chronicle

This directory is shared project memory for people and agents. The product
specification describes what was intended; this chronicle records what is true
now. It should explain the project before anyone reads implementation code.

Prokron means Project Chronicle: a common language for understanding purpose,
historical decisions, current state, and future work. Use it for discussion,
review, advice, and continuity between people as well as agents.

## Authored and compiled

```text
.prokron/chronicle/   authored by people and agents; the only source of truth
.prokron/compiled/    compiled by Prokron; safe to delete and regenerate
```

Nothing in `.prokron/compiled/` is authoritative. Delete it and recompile and
no project fact is lost. Never hand-edit it, and never let a generated view decide a
question that an authored document answers.

## Read order

1. `.prokron/compiled/STATE.md` for the current position.
2. `PHASES.md` for the active phase, its exit conditions, and gate status.
3. `.prokron/compiled/TASK_GRAPH.md` for in-flight, ready, and blocked work.
4. The selected entry in `TASKS.md`.
5. Its contract in `ACCEPTANCE.md`.
6. Its governing entries in `ADR/`.
7. `INTENT.md` for the single task in progress.
8. `HANDOFF.md` for current implementation continuity.
9. Recent `JOURNAL.md` entries when further detail is needed.
10. Read specifications or code only when the selected task requires them.

## Authority

- `PHASES.md` is phase outcome, entry, exit, exit authority, and status.
- `TASKS.md` is task identity, phase, dependency, ownership, execution state,
  validation state, contract reference, and evidence.
- `ACCEPTANCE.md` is the completion contract. A task is not done because someone
  says it is done; it is done when its frozen contract has sufficient evidence.
- `ADR/` is accepted decision authority, one file per ADR, append-only.
- `INTENT.md` is overwritten and holds zero or one current task.
- `HANDOFF.md` is overwritten and holds current implementation continuity.
- `JOURNAL.md` is append-only history and holds no authority.
- `.prokron/compiled/STATE.md` and `.prokron/compiled/TASK_GRAPH.md` are
  views. They report authority and never override it.

## Working rules

1. Record every new work request as a task before implementation without waiting
   for a Prokron command. Give it a phase, or mark it `P-NONE`.
2. Work on one task at a time. Mark it `WIP`, record owner and claim date, and
   keep the exact execution point in `INTENT.md`.
3. Hard dependencies come from `TASKS.md`. Label suggested ordering as a
   suggestion; do not silently turn it into a dependency.
4. A contract freezes when its task becomes `WIP`. Change it only through an
   accepted Acceptance Change Request. A reviewer preference is not a criterion.
5. Mark a task `DONE` only when every mandatory criterion in its contract holds
   and its evidence is recorded. Keep completion separate from validation
   strength: `UNTESTED`, `SYNTHETIC`, `AI_REVIEWED`, or `HUMAN_VERIFIED`.
6. Only a named human may record `HUMAN_VERIFIED`, and only against `MANUAL`
   evidence.
7. Append an ADR as soon as a material choice is made, accepted, or acted on.
   When a decision changes, supersede the earlier ADR and preserve its file.
8. Update `HANDOFF.md` and append a `JOURNAL.md` entry before leaving work
   mid-air. `Left mid-air` and `Next` must be explicit even when the answer is
   "nothing."
9. Keep entries concise. Put product rules in the specification and durable
   implementation choices in ADRs, not in the session diary.

## Checkpoint trigger

Update the chronicle while working. Early enough to finish writing, checkpoint
before a handoff, interruption, compaction, or any known or estimated agent or
host context, token, time, session, rate, or quota limit:

1. update task status, validation, criterion state, evidence, and governing ADRs;
2. synchronize the compiled views;
3. update or clear the single intent;
4. rewrite `HANDOFF.md` and append a journal entry with the exact next action.

If the host cannot report its limits, checkpoint after meaningful milestones,
before long-running work, and before ending. Do not wait until the last message.

## Entry modes

These modes initialize a fresh chronicle. If records already exist, preserve
them and resume; neither mode resets history.

- **New repository:** derive initial phases, tasks, and contracts from the
  product specification with the developer. Record material decisions as ADRs.
- **Existing repository:** start with an empty chronicle and record from the
  current session onward. Do not reconstruct historical tasks or decisions.
