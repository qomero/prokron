# /prokron-baseline

Run this workflow only when the project owner explicitly asks for it. It is
never part of `/prokron-init`, and an agent never starts it on its own. It
captures decisions an existing codebase already depends on, so later work is
checked against them rather than contradicting them.

1. Identify at most ten load-bearing decisions: choices that bound future work,
   such as the datastore, authentication, API style, deployment target, or a
   framework the code is built around. Skip anything easily reversed.
2. For each, append an ADR file to `.prokron/chronicle/ADR/`, numbered in
   sequence, with `Status: PROPOSED`, `Authority: none`,
   `Origin: RECONSTRUCTED`, and `Evidence:` naming the repository paths or
   documents the decision was inferred from. Every cited path must exist. If
   the repository already keeps decision records, cite those files in
   `Evidence`; do not copy them into the chronicle. State only what the
   evidence shows; if the reason for a choice is not recorded anywhere, say so
   in `Context` rather than supplying one.
3. Add each to `.prokron/chronicle/ADR/README.md`.
4. Create no tasks, journal history, or intent. `TASKS.md`, `INTENT.md`, and
   `JOURNAL.md` stay unchanged.
5. Present the proposals to the owner. For each one the owner confirms, set
   `Status: ACCEPTED` and name them in `Authority`. Rejected or unanswered
   proposals stay `PROPOSED`; never delete one.
6. Run `.prokron/prokron validate`, then `.prokron/prokron compile`.
