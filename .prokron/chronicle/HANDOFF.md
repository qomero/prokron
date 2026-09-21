# Handoff

Current implementation continuity. Overwritten, never appended. It holds what
the next person or agent needs in order to continue right now. Closed history
belongs in `JOURNAL.md`.

## Position
- Release 0.4.1. P0, P1 and P2 are all `COMPLETE`. Every gate is green.
- 53 of 53 tasks done, 146 of 146 criteria passing. Nothing in flight, nothing
  ready, no obstacles.
- Everything Prokron installs lives in `.prokron/` (ADR-024). Installing takes
  one line with no arguments and the command is `prokron` (ADR-027).

## What is true now
- The continuity pilot ran in full against v0.4.0 on 2026-09-22 and all seven
  criteria pass, recorded in `docs/pilot-2026-09-22.md`. Three participants
  across two disposable projects: Codex CLI 0.155.1, a cold Gemini 3.8 Flash
  session, and the product owner. ADR-028 closed the debt ADR-020 had carried.
- Gate E is green because Codex and Claude audited the same implementation
  against the same contract, disagreed on one criterion, and the disagreement
  was settled at level 5 of the arbitration hierarchy. The defect Codex found
  was real.
- T-PILOT-01 is the first and only `HUMAN_VERIFIED` task in the project.

## What is still not proven
- **Checkpointing against a real host limit.** No host exposed a limit warning
  to observe during the pilot, and nothing was simulated in its place. Prokron
  cannot read a quota counter it is not shown. Untested, not passed.
- **The human reading, in detail.** Step 7 passed on the owner's attestation
  across two projects. No point-by-point account was recorded and no comparison
  against an agent's reading of the same chronicle was made.
- `.prokron/compiled/` is committed so the README can link to it as a live
  example. That puts a large dashboard and JSON in every diff touching
  authority. Nobody has decided whether to keep it that way.
- One validator warning is worth revisiting: `premature-evidence` fires on a
  `WIP` task carrying partial evidence, which the pilot showed is a reasonable
  thing for an agent to record mid-task.

## Repository identity
- Commits are authored as `qomero`, with an address verified on that account,
  set repository-locally under ADR-023. `git config --local user.email` shows it. The whole history was rewritten to match on 2026-09-22 and
  force-pushed, so every hash before that date is dead. `backup-pre-author-rewrite`
  holds the pre-rewrite tip locally and is safe to delete.

## Next action
Open Phase 0 or Phase 3 from their internal specifications in `next_plan/`,
which are not published (ADR-026). Both are new scope rather than remaining
scope, and neither is accepted as governing yet.

Authority first, in this order: an ADR accepting the specification, the phase
record and its gates in `PHASES.md`, its tasks in `TASKS.md`, their contracts
in `ACCEPTANCE.md`, then `validate` and `compile`. Only then claim the first
task, which should be a planning task that inspects the existing architecture
before any code changes — what T-P2-PLAN-01 was for P2.

Three things to settle before opening Phase 0: it cannot be called `P0`, which
is the finished executable state harness; it needs an LLM, which Gate B's
wording must be read against; and `SPEC.md` §3.2 currently states the opposite
of what Phase 0 does.
