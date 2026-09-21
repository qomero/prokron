# Changelog

Prokron records its own history in `prokron/JOURNAL.md` and its decisions in
`prokron/ADR/`. This file is the short version, for people arriving from a
release page.

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
