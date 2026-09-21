# Prokron specification

## 1. Purpose

Prokron is short for Project Chronicle. It is a working agreement that gives
people and AI a common language for understanding a project: why it exists,
the historical decisions that shaped it, its present state, and its future work.
A newcomer should be able to understand that story before reading implementation
code.

The task graph answers **what can happen next**. Decision lineage answers **why
the project has its current shape**. Together they form the spine of the project
chronicle.

The same record supports discussion, advice, review, and continuity among
people and agents. Session handoff is one use of this shared understanding.

Prokron consists of authored Markdown records, agent instructions, reusable
command prompts, and a deterministic compiler over those records. The compiler
reads `.prokron/chronicle/` and writes only `.prokron/compiled/`; it uses the
Python standard library and needs no network or model provider. See ADR-013,
ADR-016, ADR-017, ADR-024, and `docs/PRODUCT-THESIS.md`.

Phase specifications are internal working documents and are not published
(ADR-026). Decisions taken against them cite them by name; the record of what
was decided, what it had to satisfy and what evidence was produced lives in
this repository's own chronicle.

## 2. Chronicle

Everything Prokron owns lives in one `.prokron/` directory (ADR-024). Within
it, every participating repository has one authored `chronicle/` directory and
one compiled `compiled/` directory. Only the first is authoritative.

| File in `.prokron/chronicle/` | Role |
|---|---|
| `PHASES.md` | Phase outcome, entry, exit, exit authority, status, and gates |
| `TASKS.md` | Canonical tasks, phase, dependencies, ownership, contract reference, and evidence |
| `ACCEPTANCE.md` | Completion contracts, evidence classes, and change requests |
| `ADR/` | Append-only decision history and supersession lineage, one file per ADR |
| `INTENT.md` | Zero or one task currently being attempted |
| `HANDOFF.md` | Current implementation continuity, overwritten each checkpoint |
| `JOURNAL.md` | Append-only session diary and handoff history |

| File in `.prokron/compiled/` | Role |
|---|---|
| `project.json` | The whole compiled project, with provenance for every object |
| `STATE.md` | Short snapshot of the project now |
| `TASK_GRAPH.md` | Current dependency and eligibility view derived from tasks |
| `*.mmd` | Mermaid views: task graph, critical path, phases, gates, timelines |
| `dashboard.html` | The same state as one browsable page |

Every compiled file is disposable. Deleting the directory and compiling again
reproduces all of them byte for byte.

The product specification records intended behavior. The chronicle records
current project truth. When they disagree, the agent surfaces and reconciles
the difference.

## 3. Entry modes

Prokron has exactly two entry modes.

### 3.1 New repository

The developer supplies a product specification. The agent works with the
developer to:

1. resolve material ambiguity;
2. create the initial tasks and hard dependencies;
3. render the task graph;
4. record material product and implementation decisions as ADRs;
5. write the current state;
6. leave intent empty until work starts; and
7. append the first journal entry.

The chronicle must explain the project before implementation begins.

### 3.2 Existing repository

The agent installs an empty chronicle. It does not scan the repository to infer
past tasks, decisions, or intent. The current request becomes the first task
when work starts, and later sessions maintain the chronicle as part of normal
work.

A developer may explicitly request historical reconstruction. It is outside the
default workflow.

### 3.3 Bootstrap

A single POSIX shell command installs the static chronicle, workflows, and agent
adapters into the current repository. It takes no arguments: `existing` is the
default mode and `new` remains available, as does an optional target directory.
It preserves an existing chronicle and project instructions, and prints the
matching command to start in the agent chat. The bootstrap is installation
tooling, not a project runtime.

The installer also writes a launcher named `prokron` into a directory already
on the reader's `PATH`, so the command is `prokron` rather than a path
(ADR-027). The launcher carries no behaviour: it finds the nearest
`.prokron/prokron` by walking up from the working directory and execs it, so
every repository runs its own runtime. It creates no directory, edits no shell
configuration, and never replaces a `prokron` it did not write; `--no-link`
skips it. `.prokron/prokron` remains valid and is what the installed agent
instructions use, because an agent may run with a different `PATH`.

Repeated initialization preserves populated records and resumes. Reinstallation
restores missing files, preserves existing guidance, and points to the manual
merge instructions for upgrades; it never resets project history.

## 4. Working lifecycle

### 4.1 Resume

Read, in order:

1. `STATE.md`;
2. `TASK_GRAPH.md`;
3. the active or selected entry in `TASKS.md`;
4. its governing entries in `ADR/`;
5. `INTENT.md`; and
6. only the recent journal entries needed for the handoff.

State the current goal and exact next action. Read specifications or code only
after the chronicle points to the relevant work.

### 4.2 Work

Create a task immediately when new work appears if the request has none; do not
wait for a Prokron command. Work on one task at a time. Mark it `WIP`, record its
owner and claim date, and overwrite `INTENT.md` with the exact execution point.
Refresh intent after meaningful progress and before long-running work.

Update the chronicle whenever project truth changes. `DONE` means the acceptance
condition is met and evidence is recorded. Validation is separate and uses one
of these values:

- `UNTESTED`
- `SYNTHETIC`
- `AI_REVIEWED`
- `HUMAN_VERIFIED`

Only a named human may record `HUMAN_VERIFIED`.

### 4.3 Decide

As soon as a material choice is made, accepted, or acted on, append an ADR with
its date, authority, context, decision, consequences, affected tasks, and any
decision it supersedes. Do not wait for a Prokron command. Never edit or delete
an earlier ADR to change its meaning. Follow the supersession chain for the
current rule.

### 4.4 Checkpoint

Before another person or agent takes over:

1. update task status, validation, evidence, and governing ADRs;
2. synchronize `TASK_GRAPH.md` and `STATE.md`;
3. update the single active intent, or clear it if the task is complete; and
4. append a journal entry with work done, validation, learning, work left
   mid-air, and the exact next action.

## 5. Automatic continuity

Chronicle maintenance happens during work. The agent checkpoints early enough
to finish writing, without waiting for the developer, when the agent or host
reports or estimates that:

- any context, input, output, or token budget is nearly exhausted;
- any time, session, rate, or quota window is nearly exhausted, including
  five-hour and seven-day windows;
- context compaction is approaching; or
- the session is stopping, pausing, or handing off.

Agent instructions cannot read quota counters that the host does not expose.
Without a host signal, the agent checkpoints after meaningful milestones,
before long-running work, and before ending so an abrupt cutoff loses little
project state.

This is an instruction-based contract, not a quota monitor. A host must expose
a warning early enough for the agent to write. Sudden termination can lose
changes since the last checkpoint; installation tests cannot prove agent compliance.

## 6. Commands

The portable workflows are:

- `/prokron-init [new|existing]`
- `/prokron-work [task]`
- `/prokron-decide`
- `/prokron-checkpoint`
- `/prokron-resume`

Claude Code and OpenCode expose these as project slash commands. Codex exposes
the same workflows through `$prokron <mode>`. Every installation provides
`AGENTS.md` and the portable Markdown files in `.prokron/commands/`, which any
capable agent can follow directly. Adapters select workflows, never model providers;
provider credentials and model selection remain in the agent host.

## 7. Invariants

- `TASKS.md` is the source of hard task dependencies.
- `TASK_GRAPH.md` mirrors tasks; suggested order never becomes a hidden dependency.
- At most one intent exists.
- Every `DONE` task has acceptance evidence.
- ADRs and journal entries remain in history.
- A changed decision gets a new, superseding ADR.
- State and intent describe the present and are overwritten as truth changes.
- Entries use stable IDs and absolute dates.

## 8. Scope

Prokron owns project understanding, not project execution. It provides the
chronicle format, the agent workflow, and a deterministic compiler and CLI over
the records, including the generated dashboard. The working agent does the
reasoning and file editing; Git keeps file history.

Outside this specification: a service, a database, a semantic repository
scanner, an inference engine, a schema framework, a locking system, a model API,
and automatic historical migration. Nothing here schedules work, assigns work,
or decides what happens next.

ADR-008 removed an earlier runtime and made Prokron a workflow convention;
ADR-013 reinstated a deterministic compiler under the constraint that it reason
about nothing and invent nothing. A CLI and a dashboard are therefore in scope
as projections of authored records, and out of scope as sources of fact.

## 9. Acceptance

1. Given a product specification, an agent and developer can create a chronicle
   another agent can use before reading code.
2. In an existing repository, initialization starts empty and records the first
   session without fabricated history.
3. A fresh agent can recover current work, hard dependencies, governing
   decisions, validation, unfinished work, and the exact next action from the
   chronicle.
4. A superseding decision leaves the earlier ADR intact and discoverable.
5. A host limit or session-ending signal triggers a checkpoint; without a
   signal, milestone checkpoints preserve continuity.
6. A human reading the same files reaches the same project-level understanding.

### Handoff pilot

Run in a disposable project with the host and model you intend to use:

1. Install in `new` mode and supply a small specification; check that the first
   tasks and dependencies reflect it. Separately install in `existing` mode;
   verify it creates no invented history.
2. Make an ordinary work request without a Prokron command. Check that a task
   and single intent appear before implementation, with the graph kept in sync.
3. Make a material choice, then change it. Check that both ADRs remain and the
   newer one supersedes the earlier one, without requiring `/prokron-decide`.
4. Pause partway through a task. Check state, intent, and journal for the exact
   stopping point and next action. Try an exposed limit warning if available;
   label any simulated warning as simulated, not proof of quota detection.
5. Start a fresh agent session without the previous chat. Ask it to resume and
   explain the project goal, active task, governing decisions, and next action
   before reading code. Compare with the saved handoff.
6. Run init again; check that tasks, ADRs, and journal history remain intact.
7. Ask a person who did not do the work to read the same chronicle and explain
   the project's purpose, a changed decision and its reason, current state,
   and next priority. Compare their account with the agent's; record gaps or
   disagreements for clarification. Only the participating human can mark this
   check `HUMAN_VERIFIED`.

Record host/model, date, observed results, and any gaps. Repeat for each host
you claim to have verified. This pilot is not covered by `tests/install.sh`.
