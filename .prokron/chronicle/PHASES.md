Project: Prokron

# Phases

Phase outcome, entry, exit, and status authority.

A phase answers one question:

> What capability or maturity level must become true before the project moves
> forward?

A phase is not a container of tasks. Membership comes from the `Phase` field on
each task in `TASKS.md`; no task is listed here.

## Vocabulary

Phase, milestone, and gate are separate and are not interchangeable.

| Concept | Meaning |
| --- | --- |
| Phase | A product maturity stage. Has entry, exit, and exit authority. |
| Milestone | A meaningful capability reached inside a phase. Optional, never blocking. |
| Gate | An invariant or release condition that must pass. May block a phase exit. It is not a phase. |

Phase status is one of:

```text
PLANNED
ACTIVE
EXIT_PENDING
COMPLETE
```

Work that belongs to no phase — repository chores, environment fixes,
configuration — is marked `P-NONE` on the task and is never counted in phase
progress.

Closed phases stay recorded. A phase whose product direction was superseded is
marked `COMPLETE` with a note, not deleted; its tasks and evidence are history.

## Phase record

Each phase records exactly these fields and nothing else:

```text
ID
Name
Outcome
Entry criteria
Exit criteria
Exit authority
Status
```

Exit authority names the one task that decides the phase is over. Exit criteria
may name gates; a gate is recorded once under Gates and referenced, never
restated.

---

## P0 — Executable state harness

Outcome:
A deterministic Python tool installs, validates, and maintains project state,
with agent-authored adoption of existing repositories.

Entry:
- A greenfield repository exists.

Exit:
- The tool installs cleanly, adopts an existing repository, and passes its own
  validation.

Exit authority:
T-HARNESS-02

Status:
COMPLETE

Note:
Superseded as a product direction by ADR-008, which replaced the tool with a
Markdown workflow. The phase is retained because its tasks and evidence are
real history. ADR-013 later reinstates a runtime, but as a compiler over
authored authority rather than as the product itself.

## P1 — Shared chronicle workflow

Outcome:
People and agents share one repository-native record of why a project exists,
the decisions that shaped it, its present state, and its next work, installable
into any repository in one command.

Entry:
- A repository exists.

Exit:
- The chronicle, workflows, and agent instructions install into a fresh or
  existing repository without destroying records.
- Public documentation explains the workflow and its real limits.
- Gate P1-CONTINUITY.

Exit authority:
T-READINESS-01

Status:
COMPLETE

Note:
Closed 2026-09-22 under ADR-028. The continuity pilot ran in full against
v0.4.0 and all seven criteria pass; Gate P1-CONTINUITY is green on complete,
current evidence. ADR-020 had parked the pilot at step 3 of 7 and set its
payoff at the P3 exit audit; the remaining steps took one session, so the debt
was paid here instead. Two claims within the pilot remain unproven and are
recorded as unproven rather than passed: behaviour against a real host limit
was never observed, and the human reading passed on the owner's attestation
without a point-by-point comparison.

---

## P2 — From acceptance contracts to project management

Outcome:
Project state, completion authority, progression, blockers, and evidence are
machine-readable and deterministically computable, without replacing the
documents that define the project.

Specified in `docs/Phase 2.md`.

Entry:
- P1 delivery is complete.
- The Phase 2 specification is accepted as governing authority (ADR-013).

Exit:
- Every task resolves to an explicit completion contract.
- Every task belongs to a known phase or is explicitly phase-independent.
- All authority compiles into a normalized `project.json`.
- Broken dependencies, acceptance references, phase references, and authority
  conflicts are detected.
- Current phase, progress, current work, ready work, blockers, obstacles, gates,
  validation coverage, and the critical path are reported deterministically.
- Mermaid views and a static dashboard are generated.
- Gate A, Gate B, Gate C, Gate D, and Gate E.

Exit authority:
T-P2-14

Status:
COMPLETE

Note:
Reopened on 2026-09-21. ADR-014 moved authority from `.prokron/` to `prokron/`
and no migration was written, so updating a real v0.1 project strands its
chronicle: the records survive but the tool reads the new location and reports
an empty project. The phase's own exit criteria were met, but shipping a layout
change without an upgrade path means the work was not done. T-MIGRATE-01 closed
it.

Exit accepted by the owner on 2026-09-22 under ADR-020. Every exit criterion is
met, all 17 tasks are DONE, Gates A through E are green on recorded evidence,
and T-P2-14 is DONE.

Carried debt: the continuity pilot is unfinished. Gate P1-CONTINUITY governs
P1's exit and not this one, so it did not block the close, but it is real and it
is not written off. T-PILOT-01 is parked at step 3 of 7 with its contract frozen
and its two passing criteria intact. ADR-020 sets the payoff point: the P3 exit
audit runs the pilot procedure in `docs/SPEC.md` against the Phase 3 build
itself rather than restarting it in a disposable project. P3 is therefore built
on a workflow whose cross-session compliance is still unverified, and a pilot
failure at that audit lands against work already written. That is the accepted
cost of closing here.

---

# Gates

A gate is green only when its evidence exists. A gate with no evidence is red,
not pending-and-assumed.

## Gate A — Single authority

No mutable project fact has two competing sources of truth.

Blocks: P2 exit
Verified by: `AC-GLOBAL-AUTHORITY`, `AC-T-P2-03-04`
Status: GREEN

Evidence, 2026-09-21: every task resolves to exactly one contract; the compiled
views are generated rather than authored; validation fails on any duplicate or
dangling reference.

## Gate B — Determinism

Task status, phase status, dependency resolution, acceptance state, gate state,
ready work, blockers, critical path, progress metrics, Gantt source data, and
dashboard rendering require no model provider.

Blocks: P2 exit
Verified by: `AC-GLOBAL-DETERMINISM`, `AC-T-P2-09-01`
Status: GREEN

Evidence, 2026-09-21: every reported figure is computed by `prokron` from
authored Markdown with no model provider and no network, and the test suite
covers each computation.

## Gate C — Regeneration

Deleting `.prokron/` and recompiling reproduces the same derived logical state.

Blocks: P2 exit
Verified by: `AC-T-P2-07-03`, `AC-T-P2-14-01`
Status: GREEN

Evidence, 2026-09-21: `rm -rf .prokron && prokron compile` reproduces
`project.json` and all three Markdown views byte for byte, on this repository
and in the fixture suite.

## Gate D — Record preservation

Installation and migration never lose or silently rewrite an existing record,
and the legal files stay unchanged.

Blocks: P1 exit, P2 exit
Verified by: `AC-GLOBAL-PRESERVE`
Status: GREEN

Evidence, 2026-09-21: the installer regression suite proves preservation across
reinstall in both entry modes, including the ADR directory; the layout migration
preserved every record; the legal files have no diff. The compiler writes only
inside `.prokron/`, so it cannot lose a record at all.

## Gate E — Agent interoperability

Two different coding agents receive the same task context packet and audit the
same work against the same completion contract.

Blocks: P2 exit
Verified by: `AC-T-P2-14-03`
Status: GREEN

Evidence, 2026-09-21: Codex and Claude each audited the same scheduling
implementation against the same reviewer packet, with no repository access.
They disagreed on one criterion in round one; the disagreement was settled at
level 5 of the arbitration hierarchy by rendering both Gantt variants in a
browser, and the defect Codex found was real. In round two both returned the
same three verdicts and no blocking findings, differing only in non-blocking
preference. A cold agent also started work from a packet alone.

## Gate P1-CONTINUITY

A real multi-session pilot records observed agent and host behaviour: whether
the chronicle is maintained without explicit commands, whether checkpoints fire
before real limits, and whether a person and an agent reach the same
understanding of the project.

Blocks: P1 exit
Verified by: the pilot procedure in `docs/SPEC.md`
Status: GREEN

Evidence, 2026-09-22: all seven criteria pass, recorded in
`docs/pilot-2026-09-22.md`. The pilot ran against v0.4.0 across two disposable
projects and three participants — Codex CLI 0.155.1 for install, uncommanded
work, a reversed decision, a mid-task stop and re-initialization; a cold Gemini
3.8 Flash session for resume; the product owner for the human reading. It
supersedes the partial 2026-09-21 run, which was measured against v0.2.1 and
cites paths that no longer exist. What the pilot did not establish is recorded
with it: no host exposed a real limit warning to observe, and nothing was
simulated in its place.

---

# Milestones

Optional markers. They never block a phase.

- `M-P2-ACCEPTANCE` — Completion authority lives in contracts. Reached when
  T-P2-03 is `DONE`.
- `M-P2-COMPILE` — All authority compiles to `project.json`. Reached when
  T-P2-07 is `DONE`.
- `M-P2-EXPLAIN` — Prokron explains project state without an LLM. Reached when
  T-P2-09 is `DONE`.
- `M-P2-VISIBLE` — One command produces a complete local dashboard. Reached when
  T-P2-11 is `DONE`.
