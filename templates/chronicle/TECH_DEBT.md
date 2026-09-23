# Technical debt

Known compromises the project is carrying: what each one is, why it exists,
what it costs while it stays, when it stops being acceptable, and what would
retire it. A debt is a liability, not a task. It may never need one; when its
trigger is reached, the work that repays it is a task of its own.

Do not list refactoring ideas or TODOs here. Record debt that a decision or a
task knowingly created, or that the project has found and must decide about.

Format:

    ## TD-001: Client plan schema coupled to UI forms
    - Status: ACCEPTED
    - Introduced by: T-083, ADR-021
    - Areas: planning, schema
    - Debt: The canonical schema mirrors the UI representation.
    - Reason: Compatibility was preserved during the P1 migration.
    - Interest: Every new intake path needs its own mapping logic.
    - Trigger: Before conversational planning becomes the default intake path.
    - Trigger state: NOT_REACHED
    - Exit condition: The planning schema is independent of the UI representation.
    - Evidence: src/planning/schema.ts
    - Linked tasks: none
    - Resolution:

Status is `OPEN` (found, not yet decided), `ACCEPTED` (carried on purpose),
`SCHEDULED` (a linked task will repay it), `RESOLVED` (the exit condition was
verified; say how in `Resolution`), or `INVALIDATED` (it no longer applies; say
why). Trigger state is `NOT_REACHED`, `APPROACHING`, or `REACHED`. Finishing a
linked task does not resolve the debt; verifying the exit condition does.

No debt recorded yet.
