Project:

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

No phases yet. Create the first phase when the project's first maturity stage is
agreed with the developer.

---

# Gates

No gates yet. Record a gate when an invariant or release condition must pass
before a phase may exit.

---

# Milestones

No milestones yet. They are optional and never block a phase.
