# Using Prokron

A working guide: the commands, the workflows your agent runs, and what to do
on an ordinary day. The [README](../README.md) explains why Prokron exists and
[`SPEC.md`](SPEC.md) defines the records; this is how you drive it.

Every command and flag below was run against a real installation before it was
written down.

---

## Install

From the root of your project:

```sh
curl -fsSL https://raw.githubusercontent.com/qomero/prokron/main/install.sh | sh
```

That adds one directory, `.prokron/`, and the files an agent host reads by a
fixed address — `AGENTS.md`, `CLAUDE.md`, and command files for Codex, Claude
Code and OpenCode. It also puts a `prokron` launcher on your `PATH`, so the
command works from any subdirectory.

| You want | Run |
|---|---|
| An existing project, recording from now on | `… \| sh` |
| A new project, from a product specification | `… \| sh -s -- new` |
| Install into another directory | `sh install.sh /path/to/project` |
| Skip the `PATH` launcher | `… \| sh -s -- --no-link` |

Without the launcher, every `prokron` below is `.prokron/prokron`. Both always
work; the launcher just saves typing.

**Upgrading** is the same command. It replaces the tool, preserves every
record, refreshes the generated views, and tells you what it preserved.

---

## The commands

### Asking where the project stands

```console
$ prokron status
App — phase P1
  tasks        1 / 2
  acceptance   1 / 2 criteria passing
  validation   1 / 2 reviewed or verified
  gates        0 / 0 green
  P1           1 / 2 · ACTIVE

  WIP       none
  Ready     T-002
  Blocked   none
  Next      T-002 (critical path)
```

`--limit N` caps how many obstacles it prints.

This is the command to run first, every time. If it disagrees with what you
believe, one of the two is wrong and it is worth finding out which.

### Asking about one task

```console
$ prokron explain T-002
T-002 — Next step
  phase P1 · TODO · UNTESTED

  Dependencies
    ✓ T-001

  Acceptance
    ○ AC-T-002-01 [TEST] Given foundation, When extended, Then it holds.

  Evidence: none recorded
  Source:   TASKS.md → T-002
```

`--json` gives the same thing as data. A `✓` is a satisfied dependency, a `○`
is a criterion with no evidence yet.

### Handing an agent exactly what it needs

```sh
prokron context T-002                   # the builder's packet
prokron context T-002 --role reviewer   # the reviewer's packet, with the finding taxonomy
```

Emits the intent, phase, task, dependencies and whether they are met, the
acceptance criteria and their states, inherited invariants, governing
decisions, evidence and handoff — and nothing about any other task. Paste it
into an agent that has never seen the repository and it can start.

### Checking and rebuilding

```sh
prokron validate     # authority is internally consistent
prokron compile      # rebuild project.json and the Markdown views
prokron graph        # rebuild the six Mermaid views
prokron dashboard    # rebuild the browsable page
```

`validate` takes `--quiet` for errors only. `compile` takes `--force` to
compile despite validation errors, which you want roughly never.

`compile` does not write the diagrams or the page — `graph` and `dashboard`
do. After editing the chronicle by hand, the full refresh is:

```sh
prokron compile && prokron graph && prokron dashboard
```

`prokron dashboard --open` opens it in a browser.

### Moving an older installation

```sh
prokron migrate           # report what it would do
prokron migrate --apply   # do it
```

Handles a v0.1 chronicle (a rewrite, originals archived) and a v0.2 one (a
relocation, records moved byte for byte). It exits non-zero when there is
nothing to migrate, which is the normal case.

### Running from elsewhere

`-C /path/to/project` runs as if started there. `--version` reports the
runtime's version, never the version of the project you are tracking.

---

## The workflows your agent runs

These are prompts, not code. Each one is a Markdown file in
`.prokron/commands/`, and any capable agent can follow it directly.

| Purpose | Claude Code / OpenCode | Codex | Anything else |
|---|---|---|---|
| Initialize | `/prokron-init [new\|existing]` | `$prokron init [new\|existing]` | Read `AGENTS.md`, follow `.prokron/commands/prokron-init.md` |
| Start or continue a task | `/prokron-work [task]` | `$prokron work [task]` | `prokron-work.md` |
| Record or change a decision | `/prokron-decide [decision]` | `$prokron decide [decision]` | `prokron-decide.md` |
| Save a handoff | `/prokron-checkpoint` | `$prokron checkpoint` | `prokron-checkpoint.md` |
| Recover current work | `/prokron-resume` | `$prokron resume` | `prokron-resume.md` |
| Record decisions an existing codebase already depends on | `/prokron-baseline` | `$prokron baseline` | `prokron-baseline.md` |

**You will not need these most of the time.** The rules installed into
`AGENTS.md` ask an agent to create the task, write its contract, record a
decision and keep progress current as part of ordinary work. The commands exist
for when you want to invoke a step deliberately — most often `/prokron-resume`
at the start of a session and `/prokron-checkpoint` before you stop.

---

## An ordinary day

**Starting.** Open a session and ask it to resume, or just read the dashboard
yourself. A cold agent should be able to state the goal, the active task, the
governing decisions and the next action before it reads any code. If it cannot,
the chronicle is missing something — that is worth fixing before the work.

**Working.** Ask for what you want in plain language. You should see, before
implementation: a task in `TASKS.md`, a contract in `ACCEPTANCE.md`, and
`INTENT.md` naming that one task. If a material choice gets made along the way,
an ADR should appear without you asking for one.

**Checking.** `prokron status`, or open the dashboard. Click a task to see its
contract, every criterion, and the evidence behind each. `DONE` with a criterion
still `NOT_RUN` is a validation error, and the tool will say so.

**Stopping.** Ask for a checkpoint, or let the rules fire. What you want in
`HANDOFF.md` is the exact stopping point and the next action — not a summary of
the conversation.

**Changing your mind.** Say so. The old ADR stays and a new one supersedes it.
The reason the previous decision was replaced is usually what the next person
actually needs.

---

## When something looks wrong

| Symptom | Cause | Fix |
|---|---|---|
| A new feature seems missing from the dashboard | The page was written by an older release | `prokron dashboard` |
| `status` says views were written by another version | Same | `prokron compile && prokron graph && prokron dashboard` |
| `prokron: command not found` | No launcher on `PATH` | `.prokron/prokron …`, or reinstall without `--no-link` |
| `No .prokron/ in … or any parent directory` | Running outside an installed project | `cd` into it, or install there |
| `status` reports an empty project | `existing` mode starts empty on purpose | Work normally; it records from now on. To capture decisions the code already depends on, ask for `/prokron-baseline` |
| The compiler refuses to compile | Validation errors | `prokron validate` names the file and anchor |
| The diagram is unreadable | It opened fitted, or the library is unreachable | Zoom, drag, hover to trace a chain; offline it falls back to diagram source |
| Something disagrees with the code | The chronicle records intent, the code records what exists | Reconcile deliberately; do not silently trust either |

---

## Rules worth knowing before you fight them

- **`.prokron/chronicle/` is authority. `.prokron/compiled/` is output.** Delete
  the second and rebuild it; never hand-edit it.
- **A contract freezes when its task starts.** Changing it takes an Acceptance
  Change Request, not an edit. This is the rule that makes "done" mean anything.
- **`DONE` is not `HUMAN_VERIFIED`.** Completion and confidence are separate
  columns, and only a named human can record the top one.
- **Nothing is invented.** No duration unless someone recorded one, no date
  unless someone set one, `UNKNOWN` the rest of the time.
- **Prokron owns project understanding, not execution.** It schedules nothing
  and runs nothing. Your agents and you do the work.

---

## Further

- [README](../README.md) — what it is and why
- [`SPEC.md`](SPEC.md) — records, lifecycle, invariants, scope
- [`PRODUCT-THESIS.md`](PRODUCT-THESIS.md) — the argument behind the design
- [`CONTRIBUTING.md`](../CONTRIBUTING.md) — how a change is accepted here
- [continuity pilot](SPEC.md#handoff-pilot) — the procedure for testing a host
