# /prokron-init

Create `.prokron/chronicle/` with `README.md`, `PHASES.md`, `TASKS.md`, `ACCEPTANCE.md`,
`ADR/`, `INTENT.md`, `HANDOFF.md`, and `JOURNAL.md` if absent, and `.prokron/compiled/`
for compiled views.

If the chronicle already contains tasks, decisions, intent, or journal entries,
preserve them all and follow `.prokron/commands/prokron-resume.md`. Neither `new` nor
`existing` resets a chronicle. Add only missing files; never replace populated
records with empty templates. The entry modes below apply only to a fresh,
empty chronicle.

For a new repository, read the product specification, work with the developer on
material ambiguity, then create the first phase, the initial tasks and their
dependencies, and an acceptance contract for each task. Record the initial
product choices as ADRs.

For an existing repository, leave tasks and history empty. Record only work and
decisions made from this session onward. Do not inspect the repository to invent
a historical chronicle.
