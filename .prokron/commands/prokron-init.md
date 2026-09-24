# /prokron-init

Create `.prokron/chronicle/` with `README.md`, `THESIS.md`, `PHASES.md`, `MODULES.md`,
`TASKS.md`, `ACCEPTANCE.md`,
`ADR/`, `INTENT.md`, `HANDOFF.md`, and `JOURNAL.md` if absent, and `.prokron/compiled/`
for compiled views.

If the chronicle already contains tasks, decisions, intent, or journal entries,
preserve them all and follow `.prokron/commands/prokron-resume.md`. Neither `new` nor
`existing` resets a chronicle. Add only missing files; never replace populated
records with empty templates. The entry modes below apply only to a fresh,
empty chronicle.

For a new repository, find the product thesis first: take it from the product
specification, or elicit it from the developer, and author it in `THESIS.md`.
Then work in the order thesis → phases → modules → tasks: create the first
phase, the modules that deliver it (or `P-NONE` modules for phase-independent
work), the initial tasks, each naming one module, with their dependencies, and
an acceptance contract for each task. Record the initial
product choices as ADRs.

For an existing repository, author the product thesis with the owner if one
is stated, and otherwise leave `THESIS.md` for the owner; leave modules, tasks,
and history empty. Record only work and
decisions made from this session onward. Do not inspect the repository to invent
a historical chronicle. If the owner wants the decisions the code already
depends on recorded, they can ask for `.prokron/commands/prokron-baseline.md`
separately; initialization never runs it.
