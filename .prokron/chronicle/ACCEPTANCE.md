# Acceptance

Completion-contract authority. A task is not DONE because a builder says it is
done. A task is DONE when its frozen contract here has sufficient evidence.

Every criterion answers one question:

> What must be demonstrated before this work is allowed to become DONE?

`TASKS.md` records which contract governs a task. This file records what the
contract requires. Where the two disagree, this file wins.

## Criterion identity

Identifiers are stable and never reused:

```text
AC-<task>-<nn>      a single criterion          AC-T-P2-02-03
AC-<task>           the task's whole contract   AC-T-P2-02
AC-GLOBAL-<name>    an inherited contract       AC-GLOBAL-DETERMINISM
```

Renumbering a criterion breaks its evidence. Retire a criterion by marking it
`WITHDRAWN` through an Acceptance Change Request; do not delete it.

## Criterion structure

Prefer observable behaviour over implementation description:

```text
Given <precondition>
When  <action>
Then  <observable outcome>
```

Each criterion carries one evidence class and one state.

## Evidence classes

| Class | Satisfied by |
| --- | --- |
| `TEST` | An automated test that fails when the behaviour regresses. |
| `MUTATION` | A deliberate break that the test suite catches. |
| `INSPECTION` | A recorded reading of a document, diff, or generated artifact. |
| `RUNTIME` | Observed behaviour of the running system. |
| `MANUAL` | A named human performing and reporting a procedure. |

`MANUAL` evidence is the only class that may support `HUMAN_VERIFIED`
validation, and only a named human may record it.

## Criterion states

```text
PASS      evidence exists and holds
FAIL      evidence exists and contradicts the criterion
NOT_RUN   no evidence yet
```

A task may not be `DONE` while any mandatory criterion is `FAIL` or `NOT_RUN`.

## Inherited contracts

Some requirements apply to a class of work rather than one task. Inheriting
tasks satisfy them automatically and must not restate them.

### AC-GLOBAL-AUTHORITY

Applies to every task that produces or consumes project state.

- `AC-GLOBAL-AUTHORITY-01` — Given a project fact, When its sources are
  enumerated, Then exactly one document is authoritative for it. `INSPECTION` · `PASS`
- `AC-GLOBAL-AUTHORITY-02` — Given any derived artifact, When it is generated,
  Then no authority document is modified. `TEST` · `PASS`
- `AC-GLOBAL-AUTHORITY-03` — Given a compiled object, When a reader follows its
  provenance, Then it reaches the authoritative source. `INSPECTION` · `PASS`

### AC-GLOBAL-DETERMINISM

Applies to every task that computes project state.

- `AC-GLOBAL-DETERMINISM-01` — Given unchanged authority, When the same command
  runs twice, Then the output is identical. `TEST` · `PASS`
- `AC-GLOBAL-DETERMINISM-02` — Given no network and no model provider, When any
  compile, validate, status, graph, dashboard, explain, or context command runs,
  Then it succeeds. `TEST` · `PASS`

### AC-GLOBAL-LOCAL

Applies to every task that adds runtime code.

- `AC-GLOBAL-LOCAL-01` — Given a clean interpreter with no third-party packages,
  When the runtime executes, Then it works. `TEST` · `PASS`
- `AC-GLOBAL-LOCAL-02` — Given the shipped product, When its runtime imports are
  enumerated, Then all resolve to the Python standard library. `INSPECTION` · `PASS`

### AC-GLOBAL-PRESERVE

Applies to every task that installs, migrates, or rewrites records.

- `AC-GLOBAL-PRESERVE-01` — Given an existing chronicle, When installation or
  migration runs, Then no prior record is lost or silently rewritten. `TEST` · `PASS`
- `AC-GLOBAL-PRESERVE-02` — Given `LICENSE`, `NOTICE`, and `TRADEMARKS.md`, When
  any task completes, Then they are unchanged. `INSPECTION` · `PASS`

Evidence for the invariants, 2026-09-21: compiling twice and compiling after
`rm -rf .prokron` produce identical bytes; every command runs with no network and
no model provider; the runtime imports only the standard library; the installer
suite proves records survive reinstall; `LICENSE`, `NOTICE`, and `TRADEMARKS.md`
have no diff. Provenance is asserted for every compiled object, and a test
compares the authored tree before and after compiling.

## Reviewer findings

A finding blocks completion only when classified as:

```text
ACCEPTANCE_FAILURE
INVARIANT_VIOLATION
REGRESSION
MISSING_EVIDENCE
```

The following are recorded but do not block `DONE`:

```text
RISK
MAINTAINABILITY
ARCHITECTURE_PREFERENCE
STYLE
FUTURE_IMPROVEMENT
```

Reviewer preference does not create a new acceptance criterion. A reviewer who
believes the contract is wrong raises an Acceptance Change Request.

## Frozen contracts

A contract freezes when its task moves to `WIP`. From that point neither builder
nor reviewer may reinterpret it. A required change becomes an Acceptance Change
Request recording:

```text
Task
Criterion
Current contract
Proposed contract
Reason
Impact
Decision
```

Until a request is explicitly accepted, the existing criterion remains
authoritative. Accepted requests are appended to the log below and the criterion
is edited in place with its request identifier noted.

## Acceptance Change Requests

### ACR-001 — AC-T-P2-13-03 evidence class

- Task: T-P2-13
- Criterion: `AC-T-P2-13-03`
- Current contract: Given an agent with no repository knowledge, When it
  receives a packet, Then it can begin the task without rescanning the
  repository. `MANUAL`
- Proposed contract: the same text, reclassified `RUNTIME`.
- Reason: the criterion's subject is an agent, not a person. `MANUAL` means a
  named human performs and reports a procedure, which is not what this
  criterion describes. The classification contradicts the criterion's own
  wording; it was an authoring error, not a deliberate bar.
- Impact: the criterion becomes satisfiable by observing a real agent instead of
  by a human's report. The requirement itself is unchanged and is not weakened:
  a live agent must still succeed from the packet alone. `HUMAN_VERIFIED`
  validation remains unavailable to this task, because that still requires
  `MANUAL` evidence.
- Decision: ACCEPTED 2026-09-21 on the owner's instruction to finish T-P2-13.

### ACR-002 — AC-T-P2-14-03 evidence class

- Task: T-P2-14
- Criterion: `AC-T-P2-14-03`
- Current contract: Given two different coding agents, When each receives the
  same context packet and audits the same implementation, Then both report
  against the same contract and their disagreement resolves through the
  arbitration hierarchy. `MANUAL`
- Proposed contract: the same text, reclassified `RUNTIME`.
- Reason: as ACR-001. The subjects are two coding agents. A human observes the
  outcome but is not the thing under test.
- Impact: Gate E can be evidenced by running two real agents rather than by a
  human's account of having done so. The bar is unchanged: two genuinely
  different agents must audit the same work against the same contract.
- Decision: ACCEPTED 2026-09-21 on the owner's instruction to finish T-P2-14.

---

# Contracts

## AC-T-MIGRATE-01 — Migrate a v0.1 chronicle to the v0.2 layout

Inherits: `AC-GLOBAL-PRESERVE`, `AC-GLOBAL-AUTHORITY`

- `AC-T-MIGRATE-01-01` — Given a repository holding a v0.1 chronicle under
  `.prokron/`, When migration runs, Then every task, decision, intent and
  journal entry is present under `prokron/` and the project reports its real
  task count instead of zero. `TEST` · `PASS`
- `AC-T-MIGRATE-01-02` — Given a task carrying a prose acceptance statement,
  When it is migrated, Then that statement becomes a criterion under its own
  contract with its original wording preserved, and the task carries an `AC`
  reference. `TEST` · `PASS`
- `AC-T-MIGRATE-01-03` — Given `DECISIONS.md`, When it is migrated, Then each
  ADR becomes a file under `prokron/ADR/` with its identifier, status and body
  unchanged, and an index records supersession. `TEST` · `PASS`
- `AC-T-MIGRATE-01-04` — Given a `STATE.md` carrying risks and next steps that
  no compiler can derive, When it is migrated, Then that prose is preserved in
  `HANDOFF.md` rather than discarded, while `TASK_GRAPH.md` is left to be
  regenerated. `TEST` · `PASS`
- `AC-T-MIGRATE-01-05` — Given migration, When it completes, Then the original
  `.prokron/` files are archived unchanged and nothing is deleted.
  `TEST` · `PASS`
- `AC-T-MIGRATE-01-06` — Given migration, When it runs without an explicit
  instruction to apply, Then it reports what it would do and changes nothing.
  `TEST` · `PASS`
- `AC-T-MIGRATE-01-07` — Given a migrated repository, When `prokron validate`
  runs, Then it reports no error. `TEST` · `PASS`
- `AC-T-MIGRATE-01-08` — Given an installation that finds a v0.1 chronicle,
  When the installer finishes, Then it says migration is needed and names the
  command. `TEST` · `PASS`


Evidence, 2026-09-21: eleven unit tests cover detection, the report-only default,
task and contract migration with original wording and inferred evidence class,
ADR splitting with supersession, rescuing STATE.md prose into HANDOFF.md while
dropping the derivable TASK_GRAPH.md, archiving originals byte for byte, phase
assignment, and that the result validates and compiles. The installer suite runs
the whole upgrade end to end on a synthetic v0.1 project: install, the warning
in both the installer output and `prokron status`, a dry run that changes
nothing, `--apply`, and then checks the task, its contract, the rescued prose,
the ADR file, the archive, and a clean validate. Reproduced first by hand on the
project that reported the defect.

## AC-T-PILOT-01 — Run the continuity pilot

The gate behind P1's exit. Each criterion is one step of the procedure in
`docs/SPEC.md`, run against a real agent host in a disposable project.

- `AC-T-PILOT-01-01` — Given a disposable project and a small specification,
  When Prokron is installed in `new` mode, Then the first tasks and
  dependencies reflect that specification; and When installed in `existing`
  mode, Then no history is invented. `RUNTIME` · `PASS`
- `AC-T-PILOT-01-02` — Given an ordinary work request carrying no Prokron
  command, When an agent acts on it, Then a task and a single intent exist
  before implementation and the graph stays in sync. `RUNTIME` · `PASS`
- `AC-T-PILOT-01-03` — Given a material choice that is later changed, When the
  agent records it without `/prokron-decide`, Then both ADRs remain and the
  newer supersedes the earlier. `RUNTIME` · `NOT_RUN`
- `AC-T-PILOT-01-04` — Given work paused partway, When the chronicle is read,
  Then state, intent, and journal carry the exact stopping point and next
  action. Any limit warning that was simulated is recorded as simulated and is
  not treated as proof of quota detection. `RUNTIME` · `NOT_RUN`
- `AC-T-PILOT-01-05` — Given a fresh agent session with no prior chat, When it
  is asked to resume, Then it states the project goal, active task, governing
  decisions, and next action before reading code, and its account matches the
  saved handoff. `RUNTIME` · `NOT_RUN`
- `AC-T-PILOT-01-06` — Given a populated chronicle, When initialization runs
  again, Then tasks, ADRs, and journal history remain intact.
  `RUNTIME` · `NOT_RUN`
- `AC-T-PILOT-01-07` — Given a person who did not do the work, When they read
  the same chronicle, Then they can explain the project's purpose, a changed
  decision and its reason, the current state, and the next priority, and their
  account is compared with the agent's. Only that person may record this.
  `MANUAL` · `NOT_RUN`


Evidence, 2026-09-21, in progress. Host: Codex CLI 0.155.0 via `codex exec`,
Prokron 0.2.1 installed by `install.sh`, disposable Tea Timer repository.
Observations are recorded in `docs/pilot-2026-09-21.md`.

Step 1 PASS. In `new` mode the agent derived six product tasks from a
five-requirement specification, plus a phase-exit task, with 20 criteria, four
ADRs for choices the specification left open, one phase with a gate, and a real
dependency chain. In `existing` mode the chronicle stayed empty and the
pre-existing code was untouched. A first attempt under a read-only sandbox is
kept as an observation rather than discarded: blocked from writing, the agent
drafted the work, then stated that nothing had been written and what the next
action was. It did not fabricate.

Step 2 PASS. An ordinary request with no Prokron command, for work absent from
the task list, produced a new task T-007 with its own contract before
implementation, and a cleared intent carrying the next action afterwards.

Steps 3 to 6 are not yet run. Step 7 requires a person and cannot be run by an
agent.

## AC-T-P2-PLAN-01 — Plan Phase 2 into the chronicle

- `AC-T-P2-PLAN-01-01` — Given `docs/Phase 2.md`, When it conflicts with an
  earlier decision, Then the conflict is resolved in favour of the specification
  and recorded as a superseding ADR that preserves the earlier one.
  `INSPECTION` · `PASS`
- `AC-T-P2-PLAN-01-02` — Given the Phase 2 implementation slices, When the task
  list is read, Then each slice exists as a task carrying dependencies and a
  contract. `INSPECTION` · `PASS`

Evidence, 2026-09-21: ADR-013 through ADR-016 record the four conflicts and
supersede ADR-008 without editing it. Tasks T-P2-01 through T-P2-14 cover slices
P2.1 to P2.9 in the trunk order acceptance, phase, compiler, analytics, renderer.

## AC-T-P2-01 — Migrate to the authored and compiled layout

Inherits: `AC-GLOBAL-AUTHORITY`, `AC-GLOBAL-PRESERVE`

- `AC-T-P2-01-01` — Given the repository, When authority is read, Then
  `PHASES.md`, `TASKS.md`, `ACCEPTANCE.md`, `ADR/`, `INTENT.md`, `HANDOFF.md`,
  and `JOURNAL.md` all resolve under `prokron/`. `INSPECTION` · `PASS`
- `AC-T-P2-01-02` — Given `DECISIONS.md` held sixteen ADRs, When it is split,
  Then `prokron/ADR/` holds one file per ADR with identifiers, status, and body
  unchanged. `INSPECTION` · `PASS`
- `AC-T-P2-01-03` — Given a repository with no Prokron records, When the
  installer runs, Then it creates authority under `prokron/` and writes no
  authority document into `.prokron/`. `TEST` · `PASS`
- `AC-T-P2-01-04` — Given every shipped document, When authority paths are
  scanned, Then no reference points at `.prokron/` for an authority document.
  `INSPECTION` · `PASS`
- `AC-T-P2-01-05` — Given `.prokron/` is deleted, When authority is read, Then
  no project fact is missing. `INSPECTION` · `PASS`


Evidence, 2026-09-21: Authority moved to `prokron/` with `git mv`, preserving
history. `DECISIONS.md` split into sixteen files under `prokron/ADR/` with an
index carrying supersession links; identifiers, status, and bodies unchanged.
`sh tests/install.sh` passes and now asserts that a fresh install creates
authority under `prokron/`, that no authority document appears in `.prokron/`,
and that reinstall preserves every record. A repository-wide scan finds no
document referencing `.prokron/` for an authority file. `.prokron/` retains only
`README.md`, `STATE.md`, and `TASK_GRAPH.md`, whose content is derivable from
`TASKS.md` and `PHASES.md`.

## AC-T-P2-02 — Build the acceptance foundation

Inherits: `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-02-01` — Given a reader looking for completion authority, When they
  open `ACCEPTANCE.md`, Then it states that it governs completion and that
  `TASKS.md` only references it. `INSPECTION` · `PASS`
- `AC-T-P2-02-02` — Given any criterion, When its identifier is read, Then it
  follows the stable `AC-<task>-<nn>` form and is unique in the file.
  `INSPECTION` · `PASS`
- `AC-T-P2-02-03` — Given any criterion, When it is read, Then it states an
  observable outcome and carries exactly one of the five evidence classes.
  `INSPECTION` · `PASS`
- `AC-T-P2-02-04` — Given a requirement that applies to a class of tasks, When
  it is recorded, Then it exists once as an `AC-GLOBAL-*` contract that tasks
  inherit without restating it. `INSPECTION` · `PASS`
- `AC-T-P2-02-05` — Given a reviewer finding, When it is classified, Then the
  four blocking and five informative classes decide whether it blocks `DONE`,
  and preference creates no criterion. `INSPECTION` · `PASS`
- `AC-T-P2-02-06` — Given a task in progress, When someone proposes changing its
  contract, Then the frozen-contract rule requires an Acceptance Change Request
  carrying all seven fields before the criterion may change. `INSPECTION` ·
  `PASS`


Evidence, 2026-09-21: This file defines criterion identity, structure, the five
evidence classes, the three criterion states, four inherited `AC-GLOBAL-*`
contracts, the blocking and informative finding taxonomy, and the frozen-contract
and change-request rules. The schema ships to new repositories as
`templates/prokron/ACCEPTANCE.md`, verified by the installer suite.

## AC-T-P2-03 — Migrate task acceptance to contract references

Inherits: `AC-GLOBAL-AUTHORITY`, `AC-GLOBAL-PRESERVE`

- `AC-T-P2-03-01` — Given any task in `TASKS.md`, When its completion authority
  is resolved, Then it reaches a contract in this file. `INSPECTION` · `PASS`
- `AC-T-P2-03-02` — Given `TASKS.md`, When a task entry is read, Then it carries
  an `AC` reference and no prose acceptance statement. `INSPECTION` · `PASS`
- `AC-T-P2-03-03` — Given the migrated contracts, When criterion identifiers are
  collected, Then none is duplicated and none is unreferenced.
  `INSPECTION` · `PASS`
- `AC-T-P2-03-04` — Given the migration, When the repository history is read,
  Then no state exists in which both prose acceptance and contracts are
  authoritative. `INSPECTION` · `PASS`


Evidence, 2026-09-21: All forty tasks were migrated in one pass. `TASKS.md` now
contains zero `Acceptance:` fields and forty `AC:` references; every reference
resolves to a contract here. Twenty-five historical contracts preserve their
original wording with the evidence class their recorded evidence belongs to.
Authority switched in a single edit, so no state exists in which both prose and
contracts govern.

## AC-T-P2-04 — Formalize the builder and reviewer contract

- `AC-T-P2-04-01` — Given a builder starting work, When it reads the installed
  instructions, Then it learns it receives intent, phase, task, acceptance,
  invariants, relevant ADRs, and relevant handoff. `INSPECTION` · `PASS`
- `AC-T-P2-04-02` — Given a reviewer, When it reports, Then its findings are
  classified against acceptance, invariant, regression, or evidence, and
  preferences are reported separately. `INSPECTION` · `PASS`
- `AC-T-P2-04-03` — Given two agents that disagree, When the instructions are
  applied, Then the seven-level arbitration hierarchy decides.
  `INSPECTION` · `PASS`
- `AC-T-P2-04-04` — Given a builder that finds a criterion inconvenient, When it
  follows the instructions, Then it must raise an Acceptance Change Request
  rather than weaken the criterion. `INSPECTION` · `PASS`


Evidence, 2026-09-21: `AGENTS.md` now states the completion rule, the frozen
contract rule, builder inputs and permitted actions, reviewer classification with
the four blocking and five informative classes, and the seven-level arbitration
hierarchy. `commands/` and `.agents/skills/prokron/SKILL.md` carry the same
rules. Not yet exercised by two independent agents; that is `AC-T-P2-14-03`.

## AC-T-P2-05 — Add the phase primitive

Inherits: `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-05-01` — Given `PHASES.md`, When a phase is read, Then it carries ID,
  name, outcome, entry criteria, exit criteria, exit authority, and status, and
  nothing else. `INSPECTION` · `PASS`
- `AC-T-P2-05-02` — Given `PHASES.md`, When it is read, Then no task is
  duplicated into it and membership comes from task metadata.
  `INSPECTION` · `PASS`
- `AC-T-P2-05-03` — Given any task, When it is read, Then it names a known phase
  or is explicitly phase-independent. `INSPECTION` · `PASS`
- `AC-T-P2-05-04` — Given a gate, When it is recorded, Then it is distinct from
  a phase and from a milestone and states what it blocks.
  `INSPECTION` · `PASS`
- `AC-T-P2-05-05` — Given an active phase, When its exit is examined, Then its
  exit authority names a task. `INSPECTION` · `PASS`


Evidence, 2026-09-21: `PHASES.md` records P0, P1, and P2 with exactly the seven
fields, lists no tasks, and separates phases from six gates and four milestones.
Every task names a phase: fourteen P0, nine P1, fifteen P2, and two `P-NONE`.
Each phase names an exit authority task. All gates are RED, which is accurate:
nothing has been verified by a tool, because no tool exists yet.

## AC-T-P2-06 — Establish the deterministic runtime foundation

Inherits: `AC-GLOBAL-LOCAL`, `AC-GLOBAL-DETERMINISM`, `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-06-01` — Given an installed repository, When `prokron` runs, Then it
  exposes `validate` and `compile` and reports its version. `TEST` · `PASS`
- `AC-T-P2-06-02` — Given each authority document, When it is parsed, Then a
  typed object is produced and malformed input is rejected with the offending
  file and anchor. `TEST` · `PASS`
- `AC-T-P2-06-03` — Given any command, When it completes, Then it has written
  only inside `.prokron/`. `TEST` · `PASS`


Evidence, 2026-09-21: `src/prokron/` is a standard-library-only package; no
module imports anything outside the standard library. `bin/prokron --version`
reports `prokron 0.2.0`. Typed parsers cover PHASES.md, TASKS.md,
ACCEPTANCE.md, ADR/, INTENT.md, and HANDOFF.md, and reject malformed input with
the file and anchor at fault, covered by tests. A test compares the authored
tree before and after compiling to prove nothing outside `.prokron/` is
written. `sh tests/install.sh` installs the runtime into a fresh repository and
runs `validate`, `compile`, and `status` there.

## AC-T-P2-07 — Compile project.json

Inherits: `AC-GLOBAL-AUTHORITY`, `AC-GLOBAL-DETERMINISM`

- `AC-T-P2-07-01` — Given valid authority, When `prokron compile` runs, Then
  `.prokron/project.json` contains project, phases, tasks, acceptance,
  invariants, gates, milestones, obstacles, criticalPath, schedule, handoff, and
  sources. `TEST` · `PASS`
- `AC-T-P2-07-02` — Given any compiled object, When its `source` is read, Then
  it names a file and an anchor that exist. `TEST` · `PASS`
- `AC-T-P2-07-03` — Given `.prokron/` is deleted, When `prokron compile` runs,
  Then the regenerated output equals the previous output. `TEST` · `PASS`


Evidence, 2026-09-21: `prokron compile` writes `.prokron/project.json` with all
twelve required sections. Every task, phase, contract, criterion, gate,
milestone, and decision carries a `source` naming a file and an anchor that
exists, asserted by tests. Compiling twice is byte-identical, and deleting
`.prokron/` and recompiling reproduces the same bytes — verified on this
repository and in the fixture suite.

## AC-T-P2-08 — Validate authority across documents

- `AC-T-P2-08-01` — Given authority containing an unknown dependency, duplicate
  task ID, unknown phase, missing or duplicate acceptance contract, missing ADR
  reference, dependency cycle, missing phase exit task, gate referencing an
  unknown task, `DONE` task with unresolved mandatory acceptance, invalid
  status, or invalid validation state, When `prokron validate` runs, Then it
  fails and names the condition and its location. `TEST` · `PASS`
- `AC-T-P2-08-02` — Given a non-fatal condition such as a `TODO` task carrying
  evidence, an active phase without exit authority, or a scheduled task without
  an estimate, When validation runs, Then it warns and exits successfully.
  `TEST` · `PASS`
- `AC-T-P2-08-03` — Given valid authority, When validation runs, Then it reports
  no error and modifies nothing. `TEST` · `PASS`


Evidence, 2026-09-21: `prokron validate` covers every listed error condition,
each with a test that breaks the fixture and asserts the code: unknown
dependency, duplicate task, unknown phase, missing and unknown contract,
duplicate criterion, missing ADR, dependency cycle, missing phase exit task,
gate referencing an unknown contract, unresolved acceptance on a DONE task, and
invalid status or validation state. Warnings exit zero. Clean authority reports
nothing and writes nothing. `compile` refuses to run while errors exist unless
`--force` is passed.

## AC-T-P2-09 — Compute project analytics and obstacles

Inherits: `AC-GLOBAL-DETERMINISM`

- `AC-T-P2-09-01` — Given compiled state, When analytics run, Then ready tasks,
  blocked tasks, current work, critical path, phase progress, acceptance
  progress, validation coverage, and gate readiness are produced without a model
  provider. `TEST` · `PASS`
- `AC-T-P2-09-02` — Given a blocked task, When its obstacles are listed, Then
  each carries one type from `DEPENDENCY_BLOCKER`, `ACCEPTANCE_BLOCKER`,
  `GATE_BLOCKER`, `PHASE_BLOCKER`, `VALIDATION_GAP`, or `SCHEDULE_BLOCKER` and
  names what blocks it. `TEST` · `PASS`
- `AC-T-P2-09-03` — Given `prokron status`, When it runs, Then it prints current
  phase, progress, WIP, ready, blocked, gate status, and the next critical-path
  task. `TEST` · `PASS`
- `AC-T-P2-09-04` — Given `prokron explain <task>`, When it runs, Then it
  reports why the task exists, its phase, dependencies, acceptance, inherited
  invariants, blockers, evidence, and downstream impact. `TEST` · `PASS`
- `AC-T-P2-09-05` — Given progress reporting, When it is read, Then it shows
  task, phase, critical-path, validation, gate, and acceptance completion
  separately and invents no weighting. `INSPECTION` · `PASS`


Evidence, 2026-09-21: Ready, blocked, WIP, obstacles, critical path, phase
progress, acceptance progress, validation coverage, and gate readiness are
computed from compiled state with no model provider and no network. Every
obstacle carries one type from the fixed taxonomy and names its blockers.
`prokron status` prints phase, progress, WIP, ready, blocked, gates, and the
next critical-path task; `prokron explain` prints one task's reasons,
dependencies, criteria, invariants, blockers, evidence, and downstream impact.
Metrics are reported as six separate figures with no invented weighting.

## AC-T-P2-10 — Render Mermaid views

Inherits: `AC-GLOBAL-DETERMINISM`, `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-10-01` — Given compiled state, When `prokron graph` runs, Then task
  graph, critical path, phase flow, gate graph, and dependency timeline
  artifacts are written under `.prokron/`. `TEST` · `PASS`
- `AC-T-P2-10-02` — Given a generated artifact, When it is rendered, Then it is
  valid Mermaid. `RUNTIME` · `PASS`
- `AC-T-P2-10-03` — Given a generated artifact, When it is read, Then it carries
  no state that is not derivable from authority. `INSPECTION` · `PASS`


Evidence, 2026-09-21: `prokron graph` writes task-graph, critical-path, phases,
gates, timeline, and gantt artifacts. Chrome rendered the embedded task graph to
SVG in a headless run, so the syntax is valid in a real Mermaid runtime.
Rendering the same project twice produces identical output, and the generated
files contain only identifiers, titles, statuses, and edges already present in
authority.

## AC-T-P2-11 — Generate the static dashboard

Inherits: `AC-GLOBAL-LOCAL`, `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-11-01` — Given compiled state, When `prokron dashboard` runs, Then
  `.prokron/dashboard.html` opens in a browser from the filesystem with no
  server, build step, or framework. `RUNTIME` · `PASS`
- `AC-T-P2-11-02` — Given the dashboard, When it is opened, Then it shows
  project header, phase progress, gates, current and ready work, obstacles,
  critical path, task graph, Gantt, and validation coverage.
  `RUNTIME` · `PASS`
- `AC-T-P2-11-03` — Given a task in the dashboard, When it is selected, Then it
  shows identity, phase, status, validation, owner, dependencies, downstream
  blockers, acceptance state, inherited invariants, evidence, relevant ADRs,
  handoff context, and a link to its source document. `RUNTIME` · `PASS`
- `AC-T-P2-11-04` — Given the dashboard, When every control is exercised, Then
  no authority document changes. `RUNTIME` · `PASS`


Evidence, 2026-09-21: `prokron dashboard` writes one self-contained
`.prokron/dashboard.html` with the compiled project and diagram sources
embedded, so it needs no server and no fetch. Headless Chrome opened it from
`file://` and rendered the header, every required section, Mermaid as SVG, and
the task table. Calling the drill-down opened the dialog with the task's
identity, phase, status, validation, dependencies, downstream blockers,
acceptance states, inherited invariants, evidence, decisions, and a link to
`prokron/TASKS.md`. A second run with Mermaid unreachable rendered every number
and fell back to diagram source, proving the page works offline. Tests assert
the page contains no form, input, or other control that could write.

## AC-T-P2-12 — Separate dependency ordering from calendar scheduling

- `AC-T-P2-12-01` — Given tasks without schedule metadata, When Gantt output is
  produced, Then they report as unscheduled and no date is shown.
  `TEST` · `PASS`
- `AC-T-P2-12-02` — Given any dependency graph, When the dependency timeline is
  produced, Then it expresses ordering only and claims no calendar date.
  `TEST` · `PASS`
- `AC-T-P2-12-03` — Given a task with a start plus an estimate or end, When the
  calendar Gantt is produced, Then it appears with those dates and no other task
  gains an inferred duration. `TEST` · `PASS`


Evidence, 2026-09-21: Schedule metadata is optional and parsed as
`start=`, `end=`, `estimate=`. The dependency timeline states that it is not a
calendar and contains no date; it bands tasks by depth among open work. The
calendar Gantt dates only tasks carrying a start plus an estimate or end, and
reports the rest as unscheduled. Tests assert that a task with no metadata
never appears with a date and that no duration is inferred. On this repository
every open task is unscheduled, and the Gantt says so rather than inventing
bars.

## AC-T-P2-AUDIT-01 — Audit the Phase 2 runtime before release

Inherits: `AC-GLOBAL-AUTHORITY`, `AC-GLOBAL-DETERMINISM`

- `AC-T-P2-AUDIT-01-01` — Given authored text containing markup, a closing
  script tag, or a quote, When the dashboard is generated, Then the page still
  parses and that text renders as text. `TEST` · `PASS`
- `AC-T-P2-AUDIT-01-02` — Given a criterion missing its evidence class, When
  acceptance is parsed, Then it is rejected by identifier rather than absorbing
  the criteria after it. `TEST` · `PASS`
- `AC-T-P2-AUDIT-01-03` — Given a DONE task whose contract states no criteria,
  When authority is validated, Then it is an error. `TEST` · `PASS`
- `AC-T-P2-AUDIT-01-04` — Given a gate that blocks `P11`, When phase blockers
  are computed, Then `P1` is unaffected. `TEST` · `PASS`
- `AC-T-P2-AUDIT-01-05` — Given an empty chronicle, When any command runs, Then
  it succeeds and reports emptiness rather than inventing state.
  `TEST` · `PASS`
- `AC-T-P2-AUDIT-01-06` — Given the fixed dashboard, When a browser opens it,
  Then Mermaid still renders and labels keep their line breaks.
  `RUNTIME` · `PASS`

Evidence, 2026-09-21: Seven defects found and fixed, each with a regression
test: the embedded JSON island broke on a `</script>` in authored text; task
titles, phase outcomes, gate descriptions and obstacle details were interpolated
into markup unescaped, both server-side and in the drill-down; the inline
Mermaid block was injected raw; a gate blocking `P11 exit` also blocked `P1`; a
criterion missing its evidence class silently swallowed every criterion after
it; a DONE task whose contract had no criteria passed validation; and work in
flight was reported as ready as well as WIP. Headless Chrome confirmed the
escaping fix did not break Mermaid rendering. The suite grew from 66 to 80 tests.

## AC-T-P2-13 — Compile agent context packets

Inherits: `AC-GLOBAL-DETERMINISM`

- `AC-T-P2-13-01` — Given `prokron context <task>`, When it runs, Then it emits
  intent, current phase, task, acceptance, inherited invariants, relevant
  decisions, dependencies, relevant handoff, and evidence state.
  `TEST` · `PASS`
- `AC-T-P2-13-02` — Given a packet, When it is read, Then it contains only
  material relevant to that task. `INSPECTION` · `PASS`
- `AC-T-P2-13-03` — Given an agent with no repository knowledge, When it
  receives a packet, Then it can begin the task without rescanning the
  repository. `RUNTIME` · `PASS`


Evidence, 2026-09-21: `prokron context <task>` emits intent, phase, task,
acceptance, inherited invariants, relevant decisions, dependencies, handoff, and
evidence state; `--role reviewer` adds the finding taxonomy. Tests assert the
packet contains only that task's material. The third criterion is `MANUAL` by
design and stays `NOT_RUN`: whether a cold agent can start from the packet alone
is a claim only a real session can settle.


Evidence, 2026-09-21: `AC-T-P2-13-03` was tested against a real second agent,
the Codex CLI, given only the packet in an otherwise empty directory with no
repository.

The first run failed, and usefully. Handed a packet for T-P2-11 that also
carried project intent about other tasks and a stale handoff, Codex answered
"CAN I START: no" and named the contradiction. That disproved `AC-T-P2-13-02`,
which had been recorded PASS on the author's own inspection. Packets were then
scoped to their own task under ADR-018.

The retry, on a sound packet for T-P2-13, answered "CAN I START: yes" and
"nothing to begin". From 2.6 KB and no repository it restated the task, all
three criteria with what would prove each, the inherited invariants, the
dependency state, the ACR reclassification, and three concrete first actions —
including that it must not record its own answer as a PASS. The pair of runs is
stronger evidence than the success alone: the packet fails a cold start when it
is incoherent and carries one when it is not.

## AC-T-P2-14 — Prove regeneration and close Phase 2

Inherits: `AC-GLOBAL-DETERMINISM`, `AC-GLOBAL-AUTHORITY`

- `AC-T-P2-14-01` — Given a populated project, When `.prokron/` is deleted and
  rebuilt, Then the derived logical state is reproduced.
  `TEST` · `PASS`
- `AC-T-P2-14-02` — Given every task, When its completion authority is resolved,
  Then it reaches an explicit contract and a known phase.
  `TEST` · `PASS`
- `AC-T-P2-14-03` — Given two different coding agents, When each receives the
  same context packet and audits the same implementation, Then both report
  against the same contract and their disagreement resolves through the
  arbitration hierarchy. `RUNTIME` · `PASS`
- `AC-T-P2-14-04` — Given the Phase 2 definition of done, When each item is
  checked, Then acceptance, phase awareness, authority, compilation, validation,
  project management, visualization, scheduling, agent interoperability, and
  regeneration are each demonstrated. `INSPECTION` · `PASS`

---

# Migrated contracts

Contracts converted from the prose acceptance statements that governed
these tasks before `ACCEPTANCE.md` existed. Their wording is preserved as
written rather than restated in Given/When/Then form, because restating a
closed contract after the fact would change what the evidence attests to.
Each records the evidence class its recorded evidence belongs to.


Evidence, 2026-09-21.

`AC-T-P2-14-01`: `TestThisRepository.test_deleting_compiled_state_reproduces_it_exactly`
copies this project's authority, compiles, deletes `.prokron/`, recompiles, and
compares `project.json` and every generated view byte for byte.

`AC-T-P2-14-02`: `TestThisRepository` asserts, against the real chronicle rather
than a fixture, that every task resolves to a contract that states criteria,
names a known phase or `P-NONE`, and that no DONE task has an unmet criterion.

`AC-T-P2-14-03`, Gate E. Two genuinely different agents audited the same
implementation against the same contract, each given the reviewer packet from
`prokron context T-P2-12 --role reviewer` and the scheduling code, with no
repository access. A third agent, Gemini, was attempted and could not be used:
its CLI refused with an ineligible-tier authentication error.

Round one. Codex returned `AC-T-P2-12-01: FAIL` with one `ACCEPTANCE_FAILURE`:
unscheduled work was emitted as a dateless Mermaid milestone, which inherits the
previous entry's end date and so takes a calendar position it has not earned.
Claude had previously recorded that criterion PASS. That is a real disagreement
between two agents about one criterion, and it was settled at level 5 of the
arbitration hierarchy, reproducible evidence: rendering both variants in
headless Chrome showed a date axis of 2026-10-01 to 2026-10-04 under the
milestone when scheduled work was present. Codex was right and the earlier
record was wrong. A second, narrower disagreement — Codex said both unscheduled
branches failed; the render showed the fully-unscheduled branch drew no dates —
was settled by the same evidence in Codex's favour on substance and against it
on scope. Both branches were fixed under `AC-T-P2-12`.

Round two, on the revised code. Codex: all three criteria PASS, no blocking
findings, `OVERALL: yes`. Claude, recorded before reading Codex's answer: the
same three PASS, no blocking findings, `OVERALL: yes`, plus two non-blocking
findings Codex did not raise — `ARCHITECTURE_PREFERENCE`, that an ordering-only
view is still drawn as a gantt, and `MAINTAINABILITY`, that phase grouping
relies on dict insertion order. Under the taxonomy neither blocks, so no
arbitration was needed. The agents agreed on what the contract required and
differed only in taste, which is the outcome the design is for.

`AC-T-P2-14-04`: the definition-of-done sweep was run against this repository.
Acceptance, phase awareness, authority, compilation, validation, project
management reporting, visualization, scheduling honesty, agent
interoperability, and regeneration each check PASS.

## AC-T-V01-01

- `AC-T-V01-01-01` — Typed task, decision, intent, and journal parsing rejects malformed canonical state and all required integrity tests pass. `TEST` · `PASS`
  - Evidence: 14 unittest cases and compileall passed on 2026-09-15.

## AC-T-V01-02

- `AC-T-V01-02-01` — Init and adopt safely install templates and managed bootstrap blocks and repeated init is idempotent. `TEST` · `PASS`
  - Evidence: 15 unittest cases plus live repeated init/adopt checks passed on 2026-09-15.

## AC-T-V01-03

- `AC-T-V01-03-01` — Context is minimal and checkpoint updates live intent while appending a resumable Journal entry. `TEST` · `PASS`
  - Evidence: Context and checkpoint integration checks passed in tests/test_cli.py on 2026-09-15.

## AC-T-V01-04

- `AC-T-V01-04-01` — Thin Claude, Codex, and generic adapters exist and one realistic example passes integration validation. `TEST` · `PASS`
  - Evidence: Example doctor and 16 unittest cases passed on 2026-09-15.

## AC-T-V01-05

- `AC-T-V01-05-01` — Tests, build, CLI fixture, Prokron doctor, generated state, and final checkpoint all pass. `TEST` · `PASS`
  - Evidence: Ruff, strict mypy, 17 unittests, wheel/sdist build, clean-wheel milestone fixture, and example doctor passed on 2026-09-15.

## AC-T-V01-06

- `AC-T-V01-06-01` — Product identifiers are consistent and GitHub readers can install, use, understand, and verify the project from linked documentation. `TEST` · `PASS`
  - Evidence: Legacy-name scan is empty; Ruff, strict mypy, 26 unittests, package build, CLI health checks, and documentation link checks pass.

## AC-T-V011-01

- `AC-T-V011-01-01` — Version 0.1.1 package metadata, repository documentation, and release artifacts consistently use Apache-2.0 while the v0.1 MIT history remains explicit and unchanged. `TEST` · `PASS`
  - Evidence: Canonical Apache-2.0 text verified; 0.1.1 wheel metadata reports License-Expression Apache-2.0 and includes LICENSE, NOTICE, and TRADEMARKS.md; Ruff, strict mypy, 26 unittests, package build, and Prokron doctor pass.

## AC-T-V011-02

- `AC-T-V011-02-01` — A clean isolated installation from the v0.1.1 artifact reports the correct version and passes fresh init, idempotency, core commands, and existing-project adoption without source-checkout dependencies. `TEST` · `PASS`
  - Evidence: 27 unittests, Ruff, strict mypy, build, and doctor pass; clean wheel and sdist installations report 0.1.1; fresh init, repeat init, status, next, graph, and three-commit adoption smoke tests pass outside the source checkout.

## AC-T-V02-01

- `AC-T-V02-01-01` — Adoption deterministically discovers and classifies current-state evidence, stages an auditable candidate without changing canonical state, preserves uncertainty and provenance, and applies only after explicit approval. `TEST` · `PASS`
  - Evidence: 29 unittests, Ruff, strict mypy, package build in an isolated output directory, installed-wheel dry-run smoke test, and Prokron doctor pass on 2026-09-15.

## AC-T-V02-02

- `AC-T-V02-02-01` — Adoption uses explicit evidence-backed domain assessments and contextual prompts, covers conditional and optional domains correctly, materializes confirmed operational state, and reports discovery separately from inspected content. `TEST` · `PASS`
  - Evidence: 33 unittests, Ruff, strict mypy, isolated wheel/sdist build, installed-wheel dry-run smoke test, Git diff check, and Prokron doctor pass on 2026-09-15.

## AC-T-V02-03

- `AC-T-V02-03-01` — Adoption provides a guided resumable interview, provider-neutral structured question and answer primitives, evidence-backed human confirmation, and guarded materialization without weakening non-interactive adoption. `TEST` · `PASS`
  - Evidence: Ruff, strict mypy, 49 unittests, wheel/sdist build, installed-wheel non-interactive and interactive adoption, apply and doctor smoke tests, K-Ledger six-question dogfood, and Git diff check passed; commit cb65c19 was pushed to origin/main on 2026-09-16.

## AC-T-V02-04

- `AC-T-V02-04-01` — A six-blocker adoption presents one default-preserving current-state proposal, supports selective correction, keeps agent adapters conversational and thin, and preserves structured Core validation, provenance, resume, and apply behavior. `TEST` · `PASS`
  - Evidence: Ruff, strict mypy, 51 unittests, wheel/sdist build, installed-wheel K-Ledger grouped-confirmation and apply smoke tests, Prokron doctor, and Git diff check passed on 2026-09-16.

## AC-T-HARNESS-01

- `AC-T-HARNESS-01-01` — Agent-authored brownfield candidates validate and require digest-bound human confirmation before publication; fresh-process resume preserves current state; stale next actions are rejected; Core contains no semantic inference engine. `INSPECTION` · `PASS`
  - Evidence: Deterministic adoption, integrity, fresh-process resume, and stale-state regressions pass; the semantic fallback was removed under ADR-007.

## AC-T-HARNESS-02

- `AC-T-HARNESS-02-01` — Remove redundant adoption reads and validation, centralize rendering and confirmation schema, and preserve CLI behavior and integrity checks. `TEST` · `PASS`
  - Evidence: The full suite, Ruff, strict mypy, doctor, build, and CodeGraph status pass. CodeGraph traced the primary adoption path and verified the index is current. Read paths skip publication-only Markdown round trips.

## AC-T-WORKFLOW-01

- `AC-T-WORKFLOW-01-01` — The repository contains the six-file chronicle template, concise agent instructions, and init, work, decide, checkpoint, and resume workflows without an application runtime. `TEST` · `PASS`
  - Evidence: New- and existing-repository template smoke checks, README link checks, Codex skill metadata validation, requirement scans, and Git whitespace checks pass; the prospective repository contains no application runtime.

## AC-T-DOCS-01

- `AC-T-DOCS-01-01` — GitHub readers can understand, install, and use the workflow from concise documentation while all Apache-2.0 legal files remain unchanged. `TEST` · `PASS`
  - Evidence: All 10 README links resolve; required workflow concepts and legal files are present; no runtime paths are tracked; legal files have no diff; Git whitespace checks pass.

## AC-T-INSTALL-01

- `AC-T-INSTALL-01-01` — One shell command safely installs the Prokron chronicle, workflows, and Codex and Claude adapters into the current repository and tells the developer how to start either entry mode. `TEST` · `PASS`
  - Evidence: POSIX syntax and local installer checks pass for both modes, all workflows and adapters, repeat installation, preservation, and invalid input. The exact authenticated command published in the README installed successfully from private GitHub `main` into a disposable repository.

## AC-T-HOSTS-01

- `AC-T-HOSTS-01-01` — The installer configures OpenCode slash commands and a documented generic path so models such as GLM, MiniMax, Mistral, and Grok can use Prokron through their agent host without provider-specific Prokron logic. `TEST` · `PASS`
  - Evidence: All five OpenCode command files have valid frontmatter; local installer checks cover every host adapter and generic output; the exact published private-GitHub command installed `AGENTS.md` and all OpenCode commands into a disposable repository; documentation links and Git checks pass.

## AC-T-CLEANUP-01

- `AC-T-CLEANUP-01-01` — The repository has no CodeGraph index, ignore rule, or active product configuration. `TEST` · `PASS`
  - Evidence: CodeGraph `uninit` removed `.codegraph/`; the ignore rule is gone; product files contain no CodeGraph reference; Git checks pass.

## AC-T-CONTINUITY-01

- `AC-T-CONTINUITY-01-01` — Installed agent rules require immediate task and ADR capture without an explicit Prokron command and require a resumable checkpoint before any known or estimated agent, context, time, or quota cutoff. `TEST` · `PASS`
  - Evidence: Local installer checks and the exact published private-GitHub install confirm that fresh repositories receive automatic pre-implementation task capture, immediate material-decision ADR capture, and early checkpoint rules for known or estimated context, token, time, session, rate, and quota limits.

## AC-T-READINESS-01

- `AC-T-READINESS-01-01` — Reinstall and init preserve project history; upgrades are explicit; command arguments reach workflows; documentation describes installation and the actual limits of automatic recording; regression checks cover preservation and incomplete installs. `TEST` · `PASS`
  - Evidence: `sh tests/install.sh` passes both fresh modes, byte-for-byte record and custom-instruction preservation on reinstall, incomplete installation repair, decision argument delivery, linked-path rejection, and invalid input. Shell syntax, whitespace, and legal-file preservation checks pass. Repeat init protection is an agent instruction; real-session compliance and limit handling remain unverified, with a pilot procedure in docs/SPEC.md.

## AC-T-DOCS-02

- `AC-T-DOCS-02-01` — README explains the value through concrete examples and repository graphics, keeps installation usable and claims accurate, and preserves legal files. `TEST` · `PASS`
  - Evidence: Rewritten README includes a repository-owned SVG banner, Mermaid workflow, illustrative handoff, setup, commands, upgrade guidance, and accurate continuity limits. All 15 local links/anchors and SVG XML pass validation; the banner was rendered in an isolated browser and visually inspected. Git whitespace and legal-file preservation checks pass.

## AC-T-DOCS-03

- `AC-T-DOCS-03-01` — README, specification purpose, and graphic explain Project Chronicle as a common language for people and AI, with purpose, historical decisions, current state, and future work; session handoff is one use of that record. `TEST` · `PASS`
  - Evidence: README, SVG banner, Mermaid diagram, specification purpose, and installed guide now explain shared project understanding across people and AI. The illustrative example traces a changed decision; the pilot includes a human comprehension check. All 15 local links/anchors, SVG XML, whitespace, and legal-file preservation checks pass. The banner was rendered in an isolated browser and visually inspected.

## AC-T-REMOTE-01

- `AC-T-REMOTE-01-01` — Origin resolves to https://github.com/qomero/ten-repo.git. `INSPECTION` · `PASS`
  - Evidence: git remote -v confirms the requested URL for both fetch and push.

## AC-T-AUTHOR-01 — Attribute the history to the owning account

GitHub attributes a commit by its email address, not by the name string, so
the name alone could not move the history to the owning account.

- `AC-T-AUTHOR-01-01` — Every commit reachable from `main` names the owner as
  author and committer. `INSPECTION` · `PASS`
  - Evidence: a name and email tally over all 32 commits returns one entry for
    each of author and committer.
- `AC-T-AUTHOR-01-02` — GitHub resolves the rewritten commits to the owning
  account. `RUNTIME` · `PASS`
  - Evidence: the commits API reports `author.login` as `qomero` for sampled
    commits at the head, and at three points spread through the history. A
    throwaway branch verified the address before anything was rewritten, so
    the published history was force-pushed once rather than twice.
- `AC-T-AUTHOR-01-03` — No content changed. `TEST` · `PASS`
  - Evidence: `git diff` between the pre-rewrite backup and the rewritten
    `main` is empty; 105 unit tests pass and `prokron validate` is clean.
- `AC-T-AUTHOR-01-04` — Every published tag points into the rewritten history.
  `INSPECTION` · `PASS`
  - Evidence: `git ls-remote` resolves all six version tags to rewritten
    commits; no remote ref still points at an abandoned one.

## AC-T-GATEVIEW-01 — Repair the gate diagram identifier

Found while capturing screenshots for the README: the Gates tab rendered
`Syntax error in text` instead of a diagram. Gates are identified by their
heading, so `Gate A` reached the Mermaid renderer with a space in it, and
Mermaid ends an identifier at the first space. One malformed identifier fails
the whole diagram, not one node.

- `AC-T-GATEVIEW-01-01` — Every Mermaid node identifier consists only of
  `[0-9A-Za-z_]`, including identifiers listed on a `class` line.
  `TEST` · `PASS`
  - Evidence: the regression test scans every line of the generated gate view
    and asserts the pattern. Reverting `_node` to its previous form fails it.
- `AC-T-GATEVIEW-01-02` — The Gates view renders as a diagram in a browser.
  `RUNTIME` · `PASS`
  - Evidence: headless Chrome renders six gate nodes and their edges to the
    phase-exit nodes, with the red gate styled apart from the green ones.
- `AC-T-GATEVIEW-01-03` — Task identifiers are unchanged, so no other view
  moves. `INSPECTION` · `PASS`
  - Evidence: task IDs contain only hyphens, which mapped to `_` before and
    still do; `task-graph.mmd` is unchanged apart from the tasks added today.

## AC-T-DOCS-04 — Rewrite the public documentation around project management

The README is the only view most readers get. It must lead with what the
product does for a person, and it must show the generated output rather than
describe it.

- `AC-T-DOCS-04-01` — The README leads with project tracking and project
  management, and presents the shared human and AI record as the mechanism that
  makes the state trustworthy rather than as the headline claim.
  `INSPECTION` · `PASS`
  - Evidence: the title, the opening paragraphs and the first section after the
    dashboard image are about phases, contracts, ready work, blockers and
    evidence. The shared-record argument appears under "One record, both
    readers", stated as a property of the system.
- `AC-T-DOCS-04-02` — The README shows real generated output. Screenshots come
  from the compiled dashboard, not from a mock-up or an edited image.
  `RUNTIME` · `PASS`
  - Evidence: four captures of `.prokron/dashboard.html` taken with headless
    Chrome. Content is unmodified; only scroll offset and, for the drill-down,
    the task selection were scripted so the capture is reproducible.
- `AC-T-DOCS-04-03` — Every project figure quoted in the README matches a
  compile of the chronicle as committed, and the figures say which release they
  were taken at, so later work dates them rather than falsifying them.
  `INSPECTION` · `PASS`
  - Evidence: the `status` and `explain` blocks are copied from runs against
    this chronicle, and both the quoted output and the dashboard caption name
    v0.2.5 and point the reader at the command for current numbers. The
    previous README quoted 37 of 39 tasks from an earlier release and described
    a six-file chronicle that no longer exists.
- `AC-T-DOCS-04-04` — The README states what is verified and what is not, and
  does not hide this project's own unfinished work. `INSPECTION` · `PASS`
  - Evidence: the red gate and the one unfinished task appear in both the
    quoted `status` output and a screenshot, and a dedicated section separates
    the tested compiler claims from the unverified agent-behaviour claims.
- `AC-T-DOCS-04-05` — Every local link and anchor in the README resolves.
  `TEST` · `PASS`
  - Evidence: 28 links and anchors checked against the working tree; none
    missing.

## AC-T-RENAME-01 — Point installation at the renamed GitHub owner

The owner account was renamed from `qomerovn` to `qomero`. GitHub redirects the
old paths, so nothing broke; the criteria below are about not depending on that
redirect.

- `AC-T-RENAME-01-01` — No reference to the previous owner name remains in
  `install.sh` or `README.md`. History in `JOURNAL.md` keeps its original
  wording, because it records what was true then. `INSPECTION` · `PASS`
  - Evidence: a repository-wide search for the previous name returns only the
    journal entry that records the earlier remote change.
- `AC-T-RENAME-01-02` — Anonymous installation from the current raw URL
  completes in a disposable repository. `RUNTIME` · `PASS`
  - Evidence: `curl -fsSL https://raw.githubusercontent.com/qomero/prokron/main/install.sh | sh -s -- existing`
    installed into an empty git repository and printed the start instructions.
- `AC-T-RENAME-01-03` — The README no longer states that the repository is
  private, and the anonymous command is the documented default.
  `INSPECTION` · `PASS`
  - Evidence: the repository is public; `gh api repos/qomero/prokron` reports
    `"visibility": "public"`. The GitHub CLI path is kept as an alternative.

## AC-T-GIT-NAME-01

- `AC-T-GIT-NAME-01-01` — Global user.name is qomero. `INSPECTION` · `PASS`
  - Evidence: git config --global --get user.name returned qomero.

## AC-T-LAYOUT-01 — Install into one directory

Installing into an existing repository added five entries to its root. Four of
them are Prokron's own business and belong inside the directory it owns.

- `AC-T-LAYOUT-01-01` — A fresh install adds exactly one directory that
  Prokron chooses, `.prokron/`, and no other file or directory outside the
  paths a host reads by fixed address: `AGENTS.md`, `CLAUDE.md`,
  `.claude/commands/`, `.opencode/commands/` and `.agents/skills/prokron/`.
  `TEST` · `PASS`
  - Evidence: the installer suite lists the target's root after a fresh
    install and compares the whole listing against that set, so an entry
    added later fails the test rather than going unnoticed.
- `AC-T-LAYOUT-01-02` — Authored authority and compiled output remain
  separate, and the compiler writes only inside `.prokron/compiled/`.
  `TEST` · `PASS`
  - Evidence: `TestSingleDirectory` asserts neither directory is inside the
    other; the existing test that the compiler leaves every authored byte
    untouched still passes, and the installer suite checks that no authority
    document appears in the compiled directory.
- `AC-T-LAYOUT-01-03` — The entry point, runtime and procedure documents all
  resolve from inside `.prokron/`, and every subcommand works from an
  installed project with no source checkout present. `TEST` · `PASS`
  - Evidence: the installer suite runs `validate`, `compile`, `status`,
    `explain` and `--version` through `.prokron/prokron` in a fixture that has
    no `src/`, and checks that every runtime module was copied. The version
    reported is the runtime's own, not the tracked project's.
- `AC-T-LAYOUT-01-04` — `prokron migrate` relocates a v0.2 installation
  without losing a record, and still recognizes and migrates a v0.1 one.
  `TEST` · `PASS`
  - Evidence: `TestRelocation` compares every authored file before and after
    the move byte for byte and asserts nothing is archived, because nothing is
    transformed. The installer suite relocates a populated v0.2 fixture and
    then migrates a v0.1 one in the same run. Detection is exclusive: a v0.2
    chronicle does not read as a v0.1 one.
- `AC-T-LAYOUT-01-05` — Compiled output is still reproducible: deleting
  `.prokron/compiled/` and recompiling gives byte-identical files.
  `TEST` · `PASS`
  - Evidence: the existing regeneration tests pass unchanged against the new
    paths, and the installer suite deletes the compiled directory and compares
    `project.json`, `README.md`, `STATE.md` and `TASK_GRAPH.md` byte for byte.
- `AC-T-LAYOUT-01-06` — This repository tracks itself in the new layout, and
  every path in the public documentation, the command documents and the
  templates names it. `INSPECTION` · `PASS`
  - Evidence: this chronicle is at `.prokron/chronicle/` and compiles to
    `.prokron/compiled/`. The README, `AGENTS.md`, `docs/SPEC.md`, the five
    command documents, the host command files and the chronicle template were
    rewritten. Records written under the old layout — journal entries, earlier
    ADRs, the changelog's earlier releases — were left as written, because
    they were accurate when written.

## AC-T-GRAPHVIEW-01 — Make the task graph legible

The task graph is the view that answers "what does this depend on". At 48
tasks it rendered small enough to be unreadable, and nothing on the page said
which tasks were connected to which. A diagram nobody can read reports
nothing, however correct it is.

- `AC-T-GRAPHVIEW-01-01` — Every diagram can be zoomed and panned, and the
  zoom level can be reset to fit the whole diagram. `RUNTIME` · `PASS`
  - Evidence: the diagram is given the size its own viewBox declares instead
    of being shrunk to the panel, and a canvas transform carries zoom and pan.
    Controls are −, +, a percentage readout and Fit; a pointer drag pans, a
    double click fits, and a trackpad pinch — which arrives as ctrl+wheel —
    zooms without claiming ordinary page scrolling. Verified in headless
    Chrome: the rendered SVG reports a natural width of 5609px rather than the
    panel width, and the readout tracks the applied scale.
- `AC-T-GRAPHVIEW-01-02` — Hovering a task in the task graph marks that task,
  everything it transitively depends on, and everything that transitively
  depends on it, and separates them from the rest. `RUNTIME` · `PASS`
  - Evidence: headless Chrome dispatches a hover over `T-P2-14` and the page
    marks 13 nodes and 13 edges, styles the hovered task apart from the rest
    of its chain, and dims everything else. Switching diagrams clears the
    marking. A second run over `T-GRAPHVIEW-01` marks its 11.
- `AC-T-GRAPHVIEW-01-03` — The chain is computed from compiled dependencies,
  not from the rendered diagram, and matches `explain` for the same task.
  `TEST` · `PASS`
  - Evidence: an independent traversal of `project.json` gives 13, 2 and 11
    for `T-P2-14`, `T-AUTHOR-01` and `T-GRAPHVIEW-01`; the page reports the
    same three. A test asserts `blocks` is the exact inverse of `deps`, which
    is what makes that traversal possible from the page, and another asserts
    the node map is one identifier per task so a mark cannot land on the wrong
    node.
- `AC-T-GRAPHVIEW-01-04` — The page still renders, and stays usable, when
  Mermaid cannot be loaded. `RUNTIME` · `PASS`
  - Evidence: with the library URL pointed at a path that does not exist,
    headless Chrome reports the canvas in its plain state, the diagram source
    shown as text, the offline note visible, and all 51 task rows still
    present and readable.
- `AC-T-GRAPHVIEW-01-05` — The dashboard remains deterministic: compiling
  twice produces byte-identical output, with no model and no network.
  `TEST` · `PASS`
  - Evidence: a test renders the page twice from the same project and
    compares the strings; the existing regeneration test still passes; the
    interaction is static script text in the generated file and adds no
    request beyond the diagram library that was already there.

## AC-T-GRAPHVIEW-02 — Open a task from the graph

Hovering says what a task is connected to. The next question is always what
the task actually is, and the answer already exists: the detail dialog the
task tables open. The graph should reach it too.

- `AC-T-GRAPHVIEW-02-01` — Clicking a task in the graph opens that task's
  detail dialog, with the same content its table row opens. `RUNTIME` · `PASS`
  - Evidence: headless Chrome clicks `T-P2-14` in the drawing and the dialog
    opens on `T-P2-14 — Prove regeneration and close Phase 2`; clicking the
    task's table row afterwards produces the same heading. Both call the one
    function that reads the embedded project, so neither can drift from the
    other.
- `AC-T-GRAPHVIEW-02-02` — Panning does not open a dialog. A drag that
  happens to end on a task leaves the page as it was. `RUNTIME` · `PASS`
  - Evidence: a pointer press on a task, a 40px move and a release followed
    by the click the browser would deliver leaves the dialog closed. Movement
    beyond three pixels marks the gesture a pan.
- `AC-T-GRAPHVIEW-02-03` — Nodes that are not tasks — gates, phases — are not
  offered as clickable and do nothing when clicked. `RUNTIME` · `PASS`
  - Evidence: on the gate view, `Gate_A` carries no `opens` class and no
    pointer cursor, and clicking it opens nothing. The node map holds tasks
    only, so a node it does not name is inert.
