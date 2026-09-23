# /prokron-resume

Recover the project from the chronicle alone. Start with
`.prokron/chronicle/INDEX.md` (run `.prokron/prokron compile` if it is
missing) and `.prokron/prokron status`, then read only what the index points
to among `.prokron/compiled/STATE.md`,
`.prokron/chronicle/PHASES.md`, `.prokron/compiled/TASK_GRAPH.md`, the active
or selected task, its contract in `ACCEPTANCE.md`, its governing ADRs,
`INTENT.md`, `HANDOFF.md`, and only the recent journal entries needed for
continuity. State the current goal and exact next
action, then continue. Read implementation code only after the chronicle points
to the work that requires it. Treat the chronicle as current project truth and
the product specification as intended behavior that may require reconciliation.

After merging branches, run `.prokron/prokron compile` (and `graph` and
`dashboard` if they are kept) rather than resolving conflicts in
`.prokron/compiled/`; it is regenerated from authority. `JOURNAL.md` and the
ADR index merge by union, so both sides' entries survive. If `INTENT.md` or
`HANDOFF.md` conflict, resolve `INTENT.md` and `HANDOFF.md` by hand toward the
branch whose work is current: keep at most one intent, and describe the other
branch's unfinished work in the handoff rather than dropping it.
