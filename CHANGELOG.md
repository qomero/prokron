# Changelog

Prokron records its own history in `.prokron/chronicle/JOURNAL.md` and its
decisions in `.prokron/chronicle/ADR/`. This file is the short version, for
people arriving from a release page.

## 0.4.2 — 2026-09-22

Nothing ran the tests except a person typing the command. Now something does.

### Added

- **Continuous integration** ([`ci.yml`](.github/workflows/ci.yml)) that
  enforces this project's own claims rather than only running `unittest`:
  - `tests` — the unit and installer suites on Ubuntu and macOS, Python 3.9
    through 3.13, with no dependency installed.
  - `invariants` — validates the real chronicle, then deletes
    `.prokron/compiled/`, rebuilds it, and fails if the result differs from
    what is committed. This makes Gate B and `AC-T-P2-14-01` continuously
    enforced instead of periodically remembered.
  - `no network, no dependencies` — asserts the runtime imports nothing outside
    the standard library.
- **[`CONTRIBUTING.md`](CONTRIBUTING.md)** — how a change is accepted here: a
  task, a contract frozen before the work, an ADR for a material choice, and
  evidence before `DONE`. The same workflow the tool installs.
- **[`SECURITY.md`](SECURITY.md)** — the four parts of the surface worth
  attacking, and three things that are not vulnerabilities.
- **[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)**, issue templates for a
  chronicle gap and a bug, and a pull request template that asks for the task,
  the contract and the evidence.

Reports route through GitHub's private advisory form; no maintainer address is
published. ADR-029.

### Decided

- `.prokron/compiled/` stays committed. The diff is now the mechanism that
  proves regeneration, which settles an open question the handoff had carried.

## 0.4.1 — 2026-09-22

The continuity pilot ran in full. Every phase is closed and every gate is green.

### Changed

- **Gate P1-CONTINUITY is green and P1 is COMPLETE.** The pilot ran end to end
  against v0.4.0 across two disposable projects and three participants — Codex
  CLI 0.155.1 for install, uncommanded work, a reversed decision, a mid-task
  stop and re-initialization; a cold Gemini 3.8 Flash session for resume; the
  product owner for the human reading. All seven criteria pass. Results in
  [`docs/pilot-2026-09-22.md`](docs/pilot-2026-09-22.md). ADR-028.
- The partial run of 2026-09-21 is superseded rather than reused: it was
  measured against v0.2.1 and cites an entry point and a directory that no
  longer exist.
- **The documentation no longer points at a red gate as proof of honesty**,
  because there isn't one. The README and the product thesis were corrected and
  the four dashboard figures regenerated.

### Still not proven, and still said so

- No host exposed a real limit warning to observe during the pilot, and nothing
  was simulated in its place. Checkpointing against an actual quota boundary is
  untested, not passed.
- The human reading passed on the owner's attestation across two projects,
  without a point-by-point account or a comparison against an agent's reading
  of the same chronicle.

### Fixed

- `HANDOFF.md` directed the next agent at a path that moved when phase
  specifications became internal. Found by a cold agent during the pilot, which
  silently used the correct location — a prose path is not a reference the
  compiler resolves, so no test could have caught it.

## 0.4.0 — 2026-09-22

Installing and running Prokron both got shorter.

### Changed

- **Installing takes one line with no arguments.**

  ```sh
  curl -fsSL https://raw.githubusercontent.com/qomero/prokron/main/install.sh | sh
  ```

  `existing` is the default mode; `new` and a target directory are still
  accepted. A misspelled mode is now an error rather than being read as a
  target directory.
- **The command is `prokron`.** The installer writes a small launcher into a
  directory already on your `PATH`, so it works from anywhere in the project
  instead of `.prokron/prokron` from the root only. The launcher carries no
  behaviour: it finds the nearest project and runs that project's own runtime,
  so two repositories on different releases stay independent. ADR-027.

  It creates no directories, changes no shell configuration, and never replaces
  a `prokron` it did not write. `--no-link` skips it, and `.prokron/prokron`
  keeps working — which is still what the installed agent instructions use,
  since an agent may run with a different `PATH`.

### Fixed

- The README showed `prokron status` in its examples while telling readers to
  type `.prokron/prokron status`. A test now holds the published examples to
  one form.

## 0.3.3 — 2026-09-22

Documentation only. No behaviour changed.

### Fixed

- **A destructive instruction in the README.** It told readers to run
  `rm -rf .prokron && prokron compile` to demonstrate that compiled output
  regenerates. That was accurate until v0.3.0 moved the whole installation into
  `.prokron/`; afterwards it deleted the chronicle, the runtime and the command.
  It now names `.prokron/compiled/`.
- **`docs/SPEC.md` contradicted the product.** §8 listed a CLI and a dashboard
  as out of scope, both shipped in P2. §4.1 cited `DECISIONS.md`, removed in
  v0.2. §6 named a directory that moved in v0.3. The compiled-file table was
  missing `project.json`, the Mermaid views and the dashboard.
- A dead link to `commands/`, a stale test count, and a stale release number.

### Changed

- **The README leads with the problem.** A session ends and the next
  participant — another agent, another model, a teammate — loses what the code
  meant. That comes before any record, command or file is named.
- **Both projections of project state are shown rather than asserted.** The
  dashboard for a person, and real `prokron context` output for an agent, from
  this repository.
- **What is implemented, what is designed, and what is unproven are separated.**
  Nothing specified-only is described as available.
- Phase specifications are internal working documents and are no longer
  published (ADR-026).

### Added

- [`docs/PRODUCT-THESIS.md`](docs/PRODUCT-THESIS.md) — why shared project state,
  and how the model is built. Every claim labelled implemented, designed, or
  thesis.
- Three tests holding the published documents to their own facts: every
  relative link resolves, no `rm -rf` names anything but the compiled
  directory, and the release the README cites matches `VERSION`.

Every existing image is preserved, unmodified and unrenamed.

## 0.3.2 — 2026-09-22

### Added

- **Clicking a task in a diagram opens its detail.** The same dialog the task
  tables open, reading the same embedded project, so the two routes cannot
  show different things. Panning does not count as a click, and nodes that are
  not tasks — gates, phases — are neither offered as clickable nor respond to
  one.

## 0.3.1 — 2026-09-22

### Added

- **The task graph is legible.** Every diagram opens at a readable scale
  instead of being shrunk to fit its panel, with zoom, pan, trackpad pinch, a
  percentage readout and a Fit button. A graph that only fits below 60% opens
  at 60% centred on what is in flight, then what is ready, then the critical
  path.
- **Hovering a task traces its chain.** The hovered task, everything it
  transitively depends on, and everything that transitively depends on it stay
  lit; the rest dims. The chain is walked over the compiled dependencies
  embedded in the page, never over the drawing, so it cannot disagree with
  `prokron explain`. ADR-025.

### Fixed

- Resizing the window no longer collapses the diagram back to a fit-to-panel
  scale.

The page remains one deterministic file, and still falls back to diagram
source with every number intact when the diagram library cannot be loaded.

## 0.3.0 — 2026-09-22

Installing Prokron used to put five entries at the root of a repository it does
not own. It now puts one.

### Changed

- **One directory.** Everything Prokron installs lives under `.prokron/`:
  `chronicle/` for the authored records, `compiled/` for generated state,
  `runtime/` for the tool's code, `commands/` for the workflows, and `prokron`
  as the command. The separation between authored authority and compiled output
  is unchanged — it is two subdirectories now instead of two root directories,
  and the compiler still writes only into `compiled/`. ADR-024.
- **Outside that directory, only fixed addresses.** `AGENTS.md`, `CLAUDE.md`,
  `.claude/commands/`, `.opencode/commands/` and `.agents/skills/prokron/` are
  read by agent hosts at paths Prokron does not choose. Nothing else is written.
- **The command moved** from `./bin/prokron` to `.prokron/prokron`.

### Added

- **`prokron migrate` relocates a v0.2 installation.** Coming from v0.2 the
  records move byte for byte and nothing is archived, because nothing is
  transformed. Coming from v0.1 it still rewrites and archives as before. Host
  command files are repointed at the workflows' new location.

### Removed

- `templates/.prokron/README.md`, a template nothing installed. The compiled
  directory's README is generated, and the unused copy had already drifted from
  what the compiler writes.

## 0.2.5 — 2026-09-22

Rewrites the README around what Prokron actually is now: project tracking and
project management, read by a person in a browser and by an agent as text.

### Fixed

- **The Gates view never rendered.** Gates are identified by their heading, so
  `Gate A` reached Mermaid with a space in it, and Mermaid ends an identifier
  at the first space — failing the whole diagram rather than one node. Node
  identifiers now drop every character outside `[0-9A-Za-z_]`. Task identifiers
  are unchanged. Found by opening every dashboard tab while capturing the
  README screenshots, which no test had ever done.

### Changed

- **The README leads with project management.** Phase 2 shipped contracts,
  phases, gates, obstacles, a critical path and a dashboard, and the previous
  README still described a six-file Markdown convention for agent continuity.
  People and AI sharing one record is now presented as the mechanism that makes
  the state trustworthy, rather than as the headline. ADR-022 records the
  reframing and what it costs.
- **It shows the product instead of describing it.** Four screenshots of the
  generated dashboard: project metrics with phases and gates, the ready and
  blocked view with the critical path, a task drill-down with its contract and
  recorded evidence, and the dependency graph.
- **Every figure is current and real.** The `status` and `explain` blocks are
  copied from runs against the committed chronicle. The previous README quoted
  37 of 39 tasks from an earlier release.
- A new section separates what is verified — the deterministic compiler, 104
  tests, byte-for-byte regeneration, two agents auditing one contract — from
  what is not, which is cross-session agent behaviour. This repository's own red
  gate and unfinished task stay visible in both the text and the screenshots.

## 0.2.4 — 2026-09-22

Stops installation depending on a GitHub rename redirect.

### Fixed

- **Installation addresses the owner by its current name.** The account was
  renamed from `qomerovn` to `qomero`, and every old URL kept working through
  GitHub's redirect, which is why it went unnoticed. A freed GitHub username is
  claimable by anyone, and the README's headline command pipes that URL into
  `sh`, so a stale owner name in an installer hands code execution to whoever
  claims the abandoned name. `install.sh` and `README.md` now use the current
  name. ADR-021 records the rule: redirects are a migration convenience with an
  expiry nobody controls, never an address.

### Changed

- The anonymous `curl` install is now the documented default, since the
  repository is public. The GitHub CLI command remains as an alternative. The
  README no longer says the repository is private or that anonymous delivery is
  unverified; it was verified against a disposable repository.

## 0.2.3 — 2026-09-22

Closes Phase 2 and writes down what it left unfinished. No code changed; this
release is a governance record, and it is versioned because the chronicle
shipped beside the runtime is part of what a user installs.

### Changed

- **Phase 2 is `COMPLETE`.** All 17 tasks done, Gates A through E green on
  recorded evidence, every exit criterion met. The exit was accepted by the
  owner rather than computed, so it is recorded as ADR-020 rather than as a
  status edit.
- **The continuity pilot is parked, not dropped.** T-PILOT-01 returns to `TODO`
  at step 3 of 7 with its contract still frozen and its two passing criteria
  intact. Gate P1-CONTINUITY stays RED and P1 stays `EXIT_PENDING`; the gate
  never governed P2's exit. ADR-020 names where the debt is paid: the Phase 3
  exit audit runs the pilot procedure against the Phase 3 build itself, in a
  real repository across real sessions, instead of restarting it in a
  disposable project.
- The accepted risk is stated in the decision rather than implied: Phase 3 gets
  built on a workflow whose cross-session agent compliance is unverified, and a
  pilot failure at that audit lands against work already written.

### Fixed

- Restored `docs/Phase 2.md`, which had been deleted from the working tree
  while ADR-013, ADR-014, ADR-015 and the P2 phase record all cite it as
  governing authority.

### Added

- `docs/Phase 3.md` — the Phase 3 specification, Execution Intelligence. Not
  yet accepted as governing authority; that is a decision P3 opens with.

## 0.2.2 — 2026-09-21

Fixes the upgrade path. 0.2.0 moved authority from `.prokron/` to `prokron/`
and shipped without a migration, so a real project that updated kept every
record and reported an empty project. Preserving files is not the same as
carrying a project forward.

### Added

- **`prokron migrate`.** Moves a v0.1 chronicle into the v0.2 layout: tasks,
  decisions, intent and journal to `prokron/`, prose acceptance converted into
  contracts with their original wording, `DECISIONS.md` split into
  `prokron/ADR/` with a supersession index. It reports by default and changes
  nothing without `--apply`. Every original file is archived unchanged; nothing
  is deleted. `--phase` assigns a phase when you have one.
- Installation and `prokron status` both detect a stranded v0.1 chronicle and
  name the command to run.

### Fixed

- Task completion counts every task. Excluding phase-independent work made a
  freshly migrated project report `0 / 0`, which reads as "nothing here" rather
  than "none of this belongs to a phase yet". Phase-independent work now has its
  own line, and the phase split stays in phase completion.

### Notes

`TASK_GRAPH.md` is not carried over: it is wholly derivable and the compiler
regenerates it. `STATE.md` is — its risks and next steps are judgement rather
than derivation, so that prose moves into `HANDOFF.md`. That is the one thing a
careless migration would actually have destroyed.

## 0.2.1 — 2026-09-21

Phase 2 closes. Every task resolves to a contract, every criterion passes, and
five of six gates are green on recorded evidence.

### Fixed

- **The calendar Gantt no longer dates unscheduled work.** A dateless Mermaid
  milestone inherits the previous entry's end date, so the "unscheduled" row was
  quietly given a calendar position — the exact fabrication the two-renderer
  split exists to prevent. Unscheduled work is now counted in the title and
  never drawn; with nothing scheduled, the output has no date axis at all. Found
  by an independent Codex audit and confirmed by rendering both variants in a
  browser.
- **Context packets are scoped to their own task** (ADR-018). `INTENT.md` and
  `HANDOFF.md` are included only when they mention the task. A packet that
  carried narrative about other work handed a cold agent contradictory
  statements, and it refused to start — correctly. Packets now also state which
  task they are for, whether it is closed, which dependencies are met, and what
  blocks it.
- A phase awaiting exit is reported as the current phase rather than "none".

### Changed

- `AC-T-P2-13-03` and `AC-T-P2-14-03` reclassified from `MANUAL` to `RUNTIME`
  through the change-request mechanism (ACR-001, ACR-002). Both name an agent as
  their subject, so a human's report was never the right evidence. The
  requirements are unchanged.

### Notes

Gate E is green: two different coding agents audited the same implementation
against the same contract, disagreed once, and the disagreement was settled by
reproducible evidence rather than by seniority. Gate P1-CONTINUITY remains red —
it needs a real multi-session pilot, and nothing else will do.

## 0.2.0 — 2026-09-21

Phase 2: the chronicle becomes machine-readable. Project state, completion
authority, progression, blockers, and evidence can now be compiled and reported
deterministically, without a model in the loop.

### Added

- **Acceptance contracts.** `prokron/ACCEPTANCE.md` is the completion authority.
  A task is done when its frozen contract has sufficient evidence, not when
  someone says so. Criteria carry stable identifiers, one of five evidence
  classes, and a state. Contracts freeze when work starts and change only
  through an accepted change request.
- **Phases and gates.** `prokron/PHASES.md` records each phase's outcome, entry,
  exit, exit authority, and status. Gates are explicit release conditions that
  can block a phase exit. Every task names a phase or is marked `P-NONE`.
- **A deterministic runtime.** `prokron validate | compile | status | graph |
  dashboard | explain | context`. Standard-library Python, no dependencies, no
  package to install, no network, no model provider.
- **Compiled project state.** `.prokron/project.json` with provenance on every
  object, plus generated Markdown views, six Mermaid diagrams, and a
  self-contained HTML dashboard with task drill-down.
- **Analytics.** Ready work, blockers, a typed obstacle taxonomy, critical path,
  and six progress metrics reported separately rather than rolled into one
  invented number.
- **Agent context packets.** `prokron context <task>` emits the minimal packet an
  agent needs to start, with a reviewer variant carrying the finding taxonomy.
- **A builder and reviewer contract** in `AGENTS.md`, including which findings
  block completion and a seven-level hierarchy for settling disagreements.

### Changed

- **Authored and compiled state are now separate.** Authority lives in
  `prokron/`; `.prokron/` is generated and safe to delete. Deleting it and
  recompiling reproduces every file byte for byte.
- `DECISIONS.md` became one file per ADR under `prokron/ADR/`, with an index
  that records supersession without editing history.
- `STATE.md` and `TASK_GRAPH.md` are generated rather than hand-maintained.
- Task acceptance moved from prose in `TASKS.md` to a contract reference.

### Notes

Two gates are deliberately red. Agent interoperability and the continuity pilot
need a real multi-session run, not a test, and neither is claimed until then.

## 0.1.1 — 2026-09-15

Relicensed to Apache-2.0 with a separate trademark policy. The v0.1 MIT grant
and its artifacts remain unchanged.

## 0.1 — 2026-09-15

First release: the Markdown chronicle, agent instructions, host adapters, and a
one-command installer.
