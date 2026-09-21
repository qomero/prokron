# Handoff

Current implementation continuity. Overwritten, never appended. It holds what
the next person or agent needs in order to continue right now. Closed history
belongs in `JOURNAL.md`.

## Position
- Release 0.3.0. P2 is `COMPLETE` as of 2026-09-22, accepted by the owner under
  ADR-020. P0 is `COMPLETE`. P1 is `EXIT_PENDING` behind one red gate.
- Nothing in flight. Intent is empty.
- 47 of 48 tasks done. The one open task is T-PILOT-01, deliberately parked.
- Everything Prokron installs now lives in `.prokron/` (ADR-024). This
  repository's own chronicle moved to `.prokron/chronicle/` and its compiled
  views to `.prokron/compiled/`; the command is `.prokron/prokron`.

## What is true now
- Gates A, B, C, D and E are green on recorded evidence. Gate E is green because
  Codex and Claude audited the same implementation against the same reviewer
  packet, disagreed on one criterion, and the disagreement was settled at level
  5 of the arbitration hierarchy by rendering both Gantt variants in a browser.
  The defect Codex found was real.
- A cold agent starts from a packet alone, verified against Codex with no
  repository access. The first, failed attempt is kept as the control.
- `prokron migrate` gives v0.1 chronicles an upgrade path, which is what
  reopened and then closed P2.

## Carried debt
- **Gate P1-CONTINUITY is RED.** The continuity pilot in `docs/SPEC.md` is two
  steps into seven. Steps 1 and 2 pass, recorded in `docs/pilot-2026-09-21.md`.
  ADR-020 parks the rest and names the payoff: the P3 exit audit runs the
  procedure against the Phase 3 build itself, in this repository, across the
  real multi-session work. Deferred is not passing. P1 stays `EXIT_PENDING`.
- The accepted risk: P3 is built on a workflow whose cross-session agent
  compliance is unverified. A pilot failure at that audit lands against P3 work
  already written. Stated rather than hidden.
- `.prokron/compiled/` is committed so the README can link to it as a live
  example. That puts a large dashboard and JSON in every diff touching
  authority. Nobody has decided whether to keep it that way.
- The chronicle now sits in a directory a file browser hides by default, and
  it is written to be read by people. ADR-024 accepted that cost; whether it
  actually costs anything is worth watching.
- Records written under the older layouts still name the old paths. That is
  deliberate — they were accurate when written — but it means a reader of the
  journal or the earlier ADRs will see `prokron/` and `./bin/prokron`.

## Repository identity
- Commits are authored as `qomero`, with an address verified on that account,
  set repository-locally under ADR-023. `git config --local user.email` shows it. The whole history was rewritten to match on 2026-09-22 and
  force-pushed, so every hash before that date is dead. `backup-pre-author-rewrite`
  holds the pre-rewrite tip locally and is safe to delete.

## Next action
Open P3 from `docs/Phase 3.md`, authority first and in this order: an ADR
accepting the specification as governing, the P3 phase record and its gates in
`PHASES.md`, its tasks in `TASKS.md`, their contracts in `ACCEPTANCE.md`, then
`validate` and `compile`. Only then claim the first task. Phase 3 §25 requires a
planning task that inspects the existing architecture before any code changes,
which is what T-P2-PLAN-01 was for P2.
