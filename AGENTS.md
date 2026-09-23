<!-- project-prokron:start -->

# Prokron

Everything Prokron owns is inside `.prokron/`. `.prokron/chronicle/` is this
repository's project chronicle: read `.prokron/chronicle/README.md` before
substantial work and follow its read order. `.prokron/compiled/` is compiled
output: read it for convenience, never edit it, and never treat it as
authority.

The repository ships a deterministic tool. Use it rather than re-deriving state
by reading files:

```sh
.prokron/prokron status          # phase, progress, ready, blocked, gates, next
.prokron/prokron explain T-123   # one task: deps, criteria, blockers, evidence
.prokron/prokron context T-123   # the minimal packet needed to start that task
.prokron/prokron validate        # check authority before and after editing it
.prokron/prokron compile         # refresh compiled/ after changing chronicle/
.prokron/prokron dashboard       # a browsable page of the same state
```

Run `validate` after editing authority and `compile` before finishing. The tool
never edits `.prokron/chronicle/`; it only reads it.

Recognize these workflows:

- `/prokron-init [new|existing]` → `.prokron/commands/prokron-init.md`
- `/prokron-work [task]` → `.prokron/commands/prokron-work.md`
- `/prokron-decide` → `.prokron/commands/prokron-decide.md`
- `/prokron-checkpoint` → `.prokron/commands/prokron-checkpoint.md`
- `/prokron-resume` → `.prokron/commands/prokron-resume.md`
- `/prokron-baseline` → `.prokron/commands/prokron-baseline.md` (only when the owner asks)

Maintain the chronicle automatically; do not wait for a Prokron command. Before
starting newly requested work, create or claim its task, give it a phase from
`PHASES.md` or mark it `P-NONE` and a `Domain:` of `execution` or `operations`,
write its acceptance contract in
`ACCEPTANCE.md`, and set the single `INTENT.md` entry. When a material project
choice is made, accepted, or acted on, append its ADR to `.prokron/chronicle/ADR/`
immediately and link affected tasks. Supersede decisions instead of overwriting
them. Keep the compiled views synchronized.

## Completion

A task is not done because you say it is done. It is done when every mandatory
criterion of its contract in `ACCEPTANCE.md` holds and its evidence is recorded.

A contract freezes when its task becomes `WIP`. If a criterion is wrong, raise
an Acceptance Change Request; never weaken, reinterpret, or quietly drop one.

## Builder

You receive intent, phase, task, acceptance contract, inherited invariants,
governing ADRs, and current handoff. You may implement, test, produce evidence,
raise an Acceptance Change Request, and update the handoff.

## Reviewer

You receive the same contract plus the implementation and its evidence. Classify
every finding. These block completion:

```text
ACCEPTANCE_FAILURE  INVARIANT_VIOLATION  REGRESSION  MISSING_EVIDENCE
```

These are recorded and do not block completion:

```text
RISK  MAINTAINABILITY  ARCHITECTURE_PREFERENCE  STYLE  FUTURE_IMPROVEMENT
```

Your preference is not an acceptance criterion.

## Disagreement

Agents will disagree. Resolve against project authority in this order, highest
first:

```text
1. Product and domain authority
2. The explicit acceptance contract
3. Invariants
4. Accepted decisions in .prokron/chronicle/ADR/
5. Reproducible tests and evidence
6. Existing code convention
7. Reviewer preference
```

The goal is not agreement. The goal is that a disagreement is decidable.

## Checkpoint

Checkpoint early enough to finish writing whenever the agent or host approaches
any context, token, time, session, rate, or quota limit, including five-hour and
seven-day windows, or before compaction or handoff. If no meter is exposed,
checkpoint after each meaningful milestone, before a long-running step, and
before ending. Preserve the active task, exact stopping point, unfinished work,
and next action.

<!-- project-prokron:end -->
