# Changelog

Prokron records its own history in `prokron/JOURNAL.md` and its decisions in
`prokron/ADR/`. This file is the short version, for people arriving from a
release page.

## 0.2.2 — 2026-09-21

Fixes the upgrade path. 0.2.0 moved authority from `.prokron/` to `prokron/`
and shipped without a migration, so a real project that updated kept every
record and reported an empty project. Preserving files is not the same as
carrying a project forward.

### Added

- **`prokron migrate`.** Moves a v0.1 chronicle into the v0.2 layout: tasks,
  decisions, intent and journal to `prokron/`, prose acceptance converted into
  contracts with their original wording, `DECISIONS.md` split into
  `prokron/ADR/` with a supersession index. It reports by default and changes
  nothing without `--apply`. Every original file is archived unchanged; nothing
  is deleted. `--phase` assigns a phase when you have one.
- Installation and `prokron status` both detect a stranded v0.1 chronicle and
  name the command to run.

### Fixed

- Task completion counts every task. Excluding phase-independent work made a
  freshly migrated project report `0 / 0`, which reads as "nothing here" rather
  than "none of this belongs to a phase yet". Phase-independent work now has its
  own line, and the phase split stays in phase completion.

### Notes

`TASK_GRAPH.md` is not carried over: it is wholly derivable and the compiler
regenerates it. `STATE.md` is — its risks and next steps are judgement rather
than derivation, so that prose moves into `HANDOFF.md`. That is the one thing a
careless migration would actually have destroyed.

## 0.2.1 — 2026-09-21

Phase 2 closes. Every task resolves to a contract, every criterion passes, and
five of six gates are green on recorded evidence.

### Fixed

- **The calendar Gantt no longer dates unscheduled work.** A dateless Mermaid
  milestone inherits the previous entry's end date, so the "unscheduled" row was
  quietly given a calendar position — the exact fabrication the two-renderer
  split exists to prevent. Unscheduled work is now counted in the title and
  never drawn; with nothing scheduled, the output has no date axis at all. Found
  by an independent Codex audit and confirmed by rendering both variants in a
  browser.
- **Context packets are scoped to their own task** (ADR-018). `INTENT.md` and
  `HANDOFF.md` are included only when they mention the task. A packet that
  carried narrative about other work handed a cold agent contradictory
  statements, and it refused to start — correctly. Packets now also state which
  task they are for, whether it is closed, which dependencies are met, and what
  blocks it.
- A phase awaiting exit is reported as the current phase rather than "none".

### Changed

- `AC-T-P2-13-03` and `AC-T-P2-14-03` reclassified from `MANUAL` to `RUNTIME`
  through the change-request mechanism (ACR-001, ACR-002). Both name an agent as
  their subject, so a human's report was never the right evidence. The
  requirements are unchanged.

### Notes

Gate E is green: two different coding agents audited the same implementation
against the same contract, disagreed once, and the disagreement was settled by
reproducible evidence rather than by seniority. Gate P1-CONTINUITY remains red —
it needs a real multi-session pilot, and nothing else will do.

## 0.2.0 — 2026-09-21

Phase 2: the chronicle becomes machine-readable. Project state, completion
authority, progression, blockers, and evidence can now be compiled and reported
deterministically, without a model in the loop.

### Added

- **Acceptance contracts.** `prokron/ACCEPTANCE.md` is the completion authority.
  A task is done when its frozen contract has sufficient evidence, not when
  someone says so. Criteria carry stable identifiers, one of five evidence
  classes, and a state. Contracts freeze when work starts and change only
  through an accepted change request.
- **Phases and gates.** `prokron/PHASES.md` records each phase's outcome, entry,
  exit, exit authority, and status. Gates are explicit release conditions that
  can block a phase exit. Every task names a phase or is marked `P-NONE`.
- **A deterministic runtime.** `prokron validate | compile | status | graph |
  dashboard | explain | context`. Standard-library Python, no dependencies, no
  package to install, no network, no model provider.
- **Compiled project state.** `.prokron/project.json` with provenance on every
  object, plus generated Markdown views, six Mermaid diagrams, and a
  self-contained HTML dashboard with task drill-down.
- **Analytics.** Ready work, blockers, a typed obstacle taxonomy, critical path,
  and six progress metrics reported separately rather than rolled into one
  invented number.
- **Agent context packets.** `prokron context <task>` emits the minimal packet an
  agent needs to start, with a reviewer variant carrying the finding taxonomy.
- **A builder and reviewer contract** in `AGENTS.md`, including which findings
  block completion and a seven-level hierarchy for settling disagreements.

### Changed

- **Authored and compiled state are now separate.** Authority lives in
  `prokron/`; `.prokron/` is generated and safe to delete. Deleting it and
  recompiling reproduces every file byte for byte.
- `DECISIONS.md` became one file per ADR under `prokron/ADR/`, with an index
  that records supersession without editing history.
- `STATE.md` and `TASK_GRAPH.md` are generated rather than hand-maintained.
- Task acceptance moved from prose in `TASKS.md` to a contract reference.

### Notes

Two gates are deliberately red. Agent interoperability and the continuity pilot
need a real multi-session run, not a test, and neither is claimed until then.

## 0.1.1 — 2026-09-15

Relicensed to Apache-2.0 with a separate trademark policy. The v0.1 MIT grant
and its artifacts remain unchanged.

## 0.1 — 2026-09-15

First release: the Markdown chronicle, agent instructions, host adapters, and a
one-command installer.
