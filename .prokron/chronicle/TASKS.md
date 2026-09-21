# Tasks

## T-V01-01: Harden typed parsers and integrity validation
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: none
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-01
- Evidence: 14 unittest cases and compileall passed on 2026-09-15.
- Governed by: ADR-001, ADR-002

## T-V01-02: Complete initialization and adoption
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-01
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-02
- Evidence: 15 unittest cases plus live repeated init/adopt checks passed on 2026-09-15.
- Governed by: ADR-001

## T-V01-03: Complete deterministic context and checkpoint continuity
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-01
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-03
- Evidence: Context and checkpoint integration checks passed in tests/test_cli.py on 2026-09-15.
- Governed by: ADR-001

## T-V01-04: Add adapters and realistic example
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-02, T-V01-03
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-04
- Evidence: Example doctor and 16 unittest cases passed on 2026-09-15.
- Governed by: ADR-001

## T-V01-05: Validate and hand off v0.1
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-04
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-05
- Evidence: Ruff, strict mypy, 17 unittests, wheel/sdist build, clean-wheel milestone fixture, and example doctor passed on 2026-09-15.
- Governed by: ADR-001

## T-V01-06: Publish Prokron identity and project documentation
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-05
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V01-06
- Evidence: Legacy-name scan is empty; Ruff, strict mypy, 26 unittests, package build, CLI health checks, and documentation link checks pass.
- Governed by: ADR-001, ADR-003

## T-V011-01: Correct the governing license for the next release
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V01-06
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V011-01
- Evidence: Canonical Apache-2.0 text verified; 0.1.1 wheel metadata reports License-Expression Apache-2.0 and includes LICENSE, NOTICE, and TRADEMARKS.md; Ruff, strict mypy, 26 unittests, package build, and Prokron doctor pass.
- Governed by: ADR-004

## T-V011-02: Verify the v0.1.1 release artifact
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V011-01
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V011-02
- Evidence: 27 unittests, Ruff, strict mypy, build, and doctor pass; clean wheel and sdist installations report 0.1.1; fresh init, repeat init, status, next, graph, and three-commit adoption smoke tests pass outside the source checkout.
- Governed by: ADR-004

## T-V02-01: Establish the adoption boundary
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V011-02
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V02-01
- Evidence: 29 unittests, Ruff, strict mypy, package build in an isolated output directory, installed-wheel dry-run smoke test, and Prokron doctor pass on 2026-09-15.
- Governed by: ADR-001

## T-V02-02: Align adoption semantics with the v2 supplement
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V02-01
- Owner: codex/primary
- Claimed: 2026-09-15
- AC: AC-T-V02-02
- Evidence: 33 unittests, Ruff, strict mypy, isolated wheel/sdist build, installed-wheel dry-run smoke test, Git diff check, and Prokron doctor pass on 2026-09-15.
- Governed by: ADR-001

## T-V02-03: Add the interactive adoption interview
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V02-02
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-V02-03
- Evidence: Ruff, strict mypy, 49 unittests, wheel/sdist build, installed-wheel non-interactive and interactive adoption, apply and doctor smoke tests, K-Ledger six-question dogfood, and Git diff check passed; commit cb65c19 was pushed to origin/main on 2026-09-16.
- Governed by: ADR-001, ADR-005

## T-V02-04: Consolidate the current-state adoption review
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-V02-03
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-V02-04
- Evidence: Ruff, strict mypy, 51 unittests, wheel/sdist build, installed-wheel K-Ledger grouped-confirmation and apply smoke tests, Prokron doctor, and Git diff check passed on 2026-09-16.
- Governed by: ADR-005

## T-HARNESS-01: Extract the deterministic state harness
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: none
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-HARNESS-01
- Evidence: Deterministic adoption, integrity, fresh-process resume, and stale-state regressions pass; the semantic fallback was removed under ADR-007.
- Governed by: ADR-006

## T-HARNESS-02: Clean up the deterministic adoption implementation
- Status: DONE
- Phase: P0
- Validation: SYNTHETIC
- Dependencies: T-HARNESS-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-HARNESS-02
- Evidence: The full suite, Ruff, strict mypy, doctor, build, and CodeGraph status pass. CodeGraph traced the primary adoption path and verified the index is current. Read paths skip publication-only Markdown round trips.
- Governed by: ADR-006

## T-WORKFLOW-01: Reduce Prokron to the chronicle workflow
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: none
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-WORKFLOW-01
- Evidence: New- and existing-repository template smoke checks, README link checks, Codex skill metadata validation, requirement scans, and Git whitespace checks pass; the prospective repository contains no application runtime.
- Governed by: ADR-008

## T-DOCS-01: Rewrite the GitHub documentation
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-WORKFLOW-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-DOCS-01
- Evidence: All 10 README links resolve; required workflow concepts and legal files are present; no runtime paths are tracked; legal files have no diff; Git whitespace checks pass.
- Governed by: ADR-008

## T-INSTALL-01: Add one-command repository setup
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-DOCS-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-INSTALL-01
- Evidence: POSIX syntax and local installer checks pass for both modes, all workflows and adapters, repeat installation, preservation, and invalid input. The exact authenticated command published in the README installed successfully from private GitHub `main` into a disposable repository.
- Governed by: ADR-008, ADR-009

## T-HOSTS-01: Support model-neutral agent hosts
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-INSTALL-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-HOSTS-01
- Evidence: All five OpenCode command files have valid frontmatter; local installer checks cover every host adapter and generic output; the exact published private-GitHub command installed `AGENTS.md` and all OpenCode commands into a disposable repository; documentation links and Git checks pass.
- Governed by: ADR-008, ADR-010

## T-CLEANUP-01: Remove repository CodeGraph state
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-HOSTS-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-CLEANUP-01
- Evidence: CodeGraph `uninit` removed `.codegraph/`; the ignore rule is gone; product files contain no CodeGraph reference; Git checks pass.
- Governed by: ADR-008

## T-CONTINUITY-01: Make task, decision, and limit capture automatic
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-CLEANUP-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-CONTINUITY-01
- Evidence: Local installer checks and the exact published private-GitHub install confirm that fresh repositories receive automatic pre-implementation task capture, immediate material-decision ADR capture, and early checkpoint rules for known or estimated context, token, time, session, rate, and quota limits.
- Governed by: ADR-008

## T-READINESS-01: Close workflow readiness gaps
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: T-CONTINUITY-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-READINESS-01
- Evidence: `sh tests/install.sh` passes both fresh modes, byte-for-byte record and custom-instruction preservation on reinstall, incomplete installation repair, decision argument delivery, linked-path rejection, and invalid input. Shell syntax, whitespace, and legal-file preservation checks pass. Repeat init protection is an agent instruction; real-session compliance and limit handling remain unverified, with a pilot procedure in docs/SPEC.md.
- Governed by: ADR-008, ADR-009, ADR-010, ADR-011

## T-DOCS-02: Make the GitHub introduction clear and compelling
- Status: DONE
- Phase: P1
- Validation: AI_REVIEWED
- Dependencies: T-READINESS-01
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-DOCS-02
- Evidence: Rewritten README includes a repository-owned SVG banner, Mermaid workflow, illustrative handoff, setup, commands, upgrade guidance, and accurate continuity limits. All 15 local links/anchors and SVG XML pass validation; the banner was rendered in an isolated browser and visually inspected. Git whitespace and legal-file preservation checks pass.
- Governed by: ADR-008, ADR-010, ADR-011

## T-DOCS-03: Position Prokron as shared project understanding
- Status: DONE
- Phase: P1
- Validation: AI_REVIEWED
- Dependencies: T-DOCS-02
- Owner: codex/primary
- Claimed: 2026-09-16
- AC: AC-T-DOCS-03
- Evidence: README, SVG banner, Mermaid diagram, specification purpose, and installed guide now explain shared project understanding across people and AI. The illustrative example traces a changed decision; the pilot includes a human comprehension check. All 15 local links/anchors, SVG XML, whitespace, and legal-file preservation checks pass. The banner was rendered in an isolated browser and visually inspected.
- Governed by: ADR-008, ADR-012

## T-REMOTE-01: Update origin URL
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: none
- Owner: codex/primary
- Claimed: 2026-09-17
- AC: AC-T-REMOTE-01
- Evidence: git remote -v confirms the requested URL for both fetch and push.
- Governed by: ADR-008

## T-GIT-NAME-01: Set global Git username
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: none
- Owner: codex/primary
- Claimed: 2026-09-17
- AC: AC-T-GIT-NAME-01
- Evidence: git config --global --get user.name returned qomero.
- Governed by: ADR-008

## T-RENAME-01: Point installation at the renamed GitHub owner
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: none
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-RENAME-01
- Evidence: No reference to the previous owner remains in `install.sh` or `README.md`. Anonymous install from `https://raw.githubusercontent.com/qomero/prokron/main/install.sh` completed against a disposable repository. 104 unit tests and the installer suite pass.
- Governed by: ADR-021

## T-AUTHOR-01: Attribute the history to the owning account
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-RENAME-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-AUTHOR-01
- Evidence: All 32 commits on `main` carry the owner as author and committer, with an address verified on the owning account, and the GitHub API resolves each sampled commit to the `qomero` account. The six version tags were re-pointed and force-pushed. Content is unchanged: `git diff` against the pre-rewrite backup is empty, 105 unit tests pass and validation is clean.
- Governed by: ADR-023

## T-GATEVIEW-01: Repair the gate diagram identifier
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-P2-10
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-GATEVIEW-01
- Evidence: `_node` now replaces every character outside `[0-9A-Za-z_]`, so `Gate A` becomes `Gate_A`. The regenerated `gates.mmd` parses and the Gates tab renders six gates and their phase-exit edges in headless Chrome. A regression test asserts every identifier in the gate view, including the `class` line; reverting the fix fails it. Task identifiers are unchanged. 105 unit tests and the installer suite pass.
- Governed by: ADR-016

## T-DOCS-04: Rewrite the public documentation around project management
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-DOCS-03
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-DOCS-04
- Evidence: README rewritten to lead with project management and to show generated output. Four screenshots captured from the compiled dashboard at `.prokron/dashboard.html` with headless Chrome at a 1.5 device scale factor. Every quoted figure comes from `prokron status` and `prokron explain` run against the chronicle as committed. All 28 local links and anchors resolve; 105 unit tests and the installer suite pass.
- Governed by: ADR-012, ADR-022

## T-P2-PLAN-01: Plan Phase 2 into the chronicle
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: none
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-PLAN-01
- Evidence: ADR-013 through ADR-016 recorded; tasks T-P2-01 through T-P2-14 recorded with the trunk order acceptance, phase, compiler, analytics, renderer; task graph and state synchronized.
- Governed by: ADR-013

## T-P2-01: Migrate to the authored and compiled layout
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: none
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-01
- Evidence: Authority moved to `prokron/` with history preserved; ADRs split into sixteen files with a supersession index; installer, templates, host adapters, AGENTS.md, README.md, and docs/SPEC.md updated; `sh tests/install.sh` passes with new assertions that authority never lands in `.prokron/`; repository scan finds no stale authority path.
- Governed by: ADR-014, ADR-015

## T-P2-02: Build the acceptance foundation
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-01
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-02
- Evidence: `prokron/ACCEPTANCE.md` defines criterion identity, Given/When/Then structure, five evidence classes, three criterion states, four inherited contracts, the finding taxonomy, and the frozen-contract and change-request rules; the schema ships as a template and is asserted by the installer suite.
- Governed by: ADR-013, ADR-015

## T-P2-03: Migrate task acceptance to contract references
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-02
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-03
- Evidence: Forty tasks migrated in one pass; zero `Acceptance:` fields and forty `AC:` references remain; twenty-five historical contracts preserve their original wording and evidence class; authority switched atomically.
- Governed by: ADR-015

## T-P2-04: Formalize the builder and reviewer contract
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-03
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-04
- Evidence: `AGENTS.md` carries the completion rule, frozen-contract rule, builder and reviewer contracts, blocking and informative finding classes, and the seven-level arbitration hierarchy; commands and the skill carry the same rules.
- Governed by: ADR-013, ADR-015

## T-P2-05: Add the phase primitive
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-03
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-05
- Evidence: `prokron/PHASES.md` records P0, P1, and P2 with exactly seven fields each, lists no tasks, and defines six gates and four milestones separately; all forty tasks name a phase or `P-NONE`; every phase names an exit authority.
- Governed by: ADR-015

## T-P2-06: Establish the deterministic runtime foundation
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-05
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-06
- Evidence: Standard-library-only `src/prokron/` package with typed parsers, `validate`, and `compile`; installed and exercised in a fresh repository by `sh tests/install.sh`; a test proves nothing outside `.prokron/` is written. ADR-017 records how the runtime ships.
- Governed by: ADR-013, ADR-016

## T-P2-07: Compile project.json
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-06
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-07
- Evidence: `prokron compile` writes `.prokron/project.json` with all twelve sections and per-object provenance; compiling twice and compiling after `rm -rf .prokron` are byte-identical on this repository and in the fixture suite.
- Governed by: ADR-014, ADR-016

## T-P2-08: Validate authority across documents
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-07
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-08
- Evidence: `prokron validate` detects all eleven listed error conditions and three warning conditions, each covered by a test; `compile` refuses to run while errors exist unless forced.
- Governed by: ADR-013

## T-P2-09: Compute project analytics and obstacles
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-08
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-09
- Evidence: Ready, blocked, obstacles, critical path, phase and acceptance progress, validation coverage, and gate readiness computed with no model provider; obstacles carry the fixed taxonomy; `status` and `explain` report them.
- Governed by: ADR-013

## T-P2-10: Render Mermaid views
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-09
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-10
- Evidence: `prokron graph` writes six Mermaid views; headless Chrome rendered the task graph to SVG; rendering is deterministic and the files hold no state absent from authority.
- Governed by: ADR-016

## T-P2-11: Generate the static dashboard
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-10
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-11
- Evidence: `prokron dashboard` writes one self-contained page; headless Chrome verified rendering, every section, Mermaid SVG, the task drill-down dialog, and the offline fallback; tests assert the page carries no control that writes.
- Governed by: ADR-016

## T-P2-12: Separate dependency ordering from calendar scheduling
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-11
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-12
- Evidence: Dependency timeline claims no dates and bands by depth; calendar Gantt dates only tasks with a start plus an estimate or end and reports the rest unscheduled; no duration is ever inferred.
- Governed by: ADR-013

## T-P2-13: Compile agent context packets
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-09
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-13
- Evidence: Cold start tested against the Codex CLI with no repository. The first run refused and exposed that packets carried project narrative about other tasks, disproving AC-T-P2-13-02 as recorded; packets were scoped to their own task under ADR-018. The retry answered "CAN I START: yes" and "nothing to begin", restating the task, its criteria, invariants, dependency state and first actions from a 2.6 KB packet alone. 91 tests pass.
- Governed by: ADR-013

## T-P2-14: Prove regeneration and close Phase 2
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-12, T-P2-13
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-14
- Evidence: Regeneration and authority resolution are asserted against the real chronicle, not a fixture. Gate E was run for real: Codex and Claude each audited the same scheduling implementation against the same reviewer packet. Round one produced a genuine disagreement — Codex returned ACCEPTANCE_FAILURE on AC-T-P2-12-01 where Claude had recorded PASS — settled at level 5 of the arbitration hierarchy by rendering both Gantt variants in headless Chrome, which showed unscheduled work inheriting a date. The defect was real and is fixed. Round two: both agents PASS all three criteria with no blocking findings, differing only in non-blocking preference. Definition-of-done sweep passes all ten items. 91 tests and the installer suite pass.
- Governed by: ADR-013, ADR-014

## T-P2-AUDIT-01: Audit the Phase 2 runtime before release
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-12
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-P2-AUDIT-01
- Evidence: Seven defects found and fixed with regression tests: JSON island broken by `</script>`, unescaped authored text in generated markup and in the drill-down, raw inline Mermaid injection, substring phase matching in gate blockers, a criterion missing its evidence class swallowing later criteria, a DONE task passing on an empty contract, and WIP double-reported as ready. Headless Chrome re-verified rendering. 80 unit tests and the installer suite pass.
- Governed by: ADR-013, ADR-016

## T-PILOT-01: Run the continuity pilot
- Status: TODO
- Phase: P1
- Validation: UNTESTED
- Dependencies: T-READINESS-01
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-PILOT-01
- Evidence: —
- Governed by: ADR-008, ADR-011, ADR-020
- Note: Parked at step 3 of 7 under ADR-020, not abandoned. Steps 1 and 2 ran against Codex CLI 0.155.0 with Prokron 0.2.1 in a disposable project on 2026-09-21; two of seven criteria carry PASS in the contract and the observations are in `docs/pilot-2026-09-21.md`. Task evidence stays empty because the task is not complete. The contract froze when this task first went WIP and stays frozen; no criterion is weakened or dropped. It resumes at the P3 exit audit, run against the Phase 3 build itself.

## T-MIGRATE-01: Migrate a v0.1 chronicle to the v0.2 layout
- Status: DONE
- Phase: P2
- Validation: AI_REVIEWED
- Dependencies: T-P2-01
- Owner: claude/primary
- Claimed: 2026-09-21
- AC: AC-T-MIGRATE-01
- Evidence: `prokron migrate` reports by default and applies only with --apply, archiving every original unchanged. Moves tasks, decisions, intent and journal to prokron/, converts prose acceptance into contracts with original wording, splits DECISIONS.md into prokron/ADR/ with a supersession index, rescues STATE.md prose into HANDOFF.md, and drops the derivable TASK_GRAPH.md. The installer and `prokron status` both detect a stranded v0.1 chronicle and name the command. Task completion now counts phase-independent work, which had made a migrated project report 0 / 0. 104 unit tests and the installer suite pass.
- Governed by: ADR-014, ADR-015

## T-LAYOUT-01: Install into one directory
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-MIGRATE-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-LAYOUT-01
- Evidence: Installing now adds one directory Prokron chose, `.prokron/`, holding `chronicle/`, `compiled/`, `commands/`, `runtime/` and the `prokron` command; everything else it writes is a path an agent host reads by fixed address. The installer suite compares the target's whole root listing against that set. `prokron migrate` relocates a v0.2 installation byte for byte, repoints the host command files, and still migrates a v0.1 one. 114 unit tests and the installer suite pass, and this repository tracks itself in the new layout.
- Governed by: ADR-024

## T-GRAPHVIEW-01: Make the task graph legible
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-GATEVIEW-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-GRAPHVIEW-01
- Evidence: Every diagram now opens at a legible scale rather than shrunk to the panel, with zoom, pan, pinch, a percentage readout and Fit. Hovering a task in the task graph marks its transitive dependencies and dependents and dims the rest; the chain is walked over the compiled `deps` and `blocks`, so it agrees with `explain` — 13, 2 and 11 for T-P2-14, T-AUTHOR-01 and T-GRAPHVIEW-01, confirmed against an independent traversal of `project.json`. With the diagram library unreachable the page falls back to diagram source and every number still reports. 118 unit tests and the installer suite pass, and rendering the page twice gives the same bytes.
- Governed by: ADR-025

## T-GRAPHVIEW-02: Open a task from the graph
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-GRAPHVIEW-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-GRAPHVIEW-02
- Evidence: Clicking a task in any diagram opens the detail dialog the task tables open, verified in headless Chrome to produce the same heading by both routes. A pan does not count as a click: movement beyond three pixels marks the gesture and suppresses it. Only nodes the node map names as tasks carry a pointer cursor and respond; `Gate_A` on the gate view does neither. 119 unit tests and the installer suite pass.
- Governed by: ADR-025

## T-SAFETY-01: Remove a destructive command from the published documentation
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-LAYOUT-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-SAFETY-01
- Evidence: The README told readers to run `rm -rf .prokron && prokron compile`. That was accurate until v0.3.0 moved the installation into `.prokron/`, after which it deleted the chronicle, the runtime and the command. The instruction now names `.prokron/compiled/` and was run to confirm it still demonstrates the regeneration claim. The stale test count beside it was corrected to 119.
- Governed by: ADR-024

## T-DOCS-05: Lead the public documentation with the problem
- Status: DONE
- Phase: P-NONE
- Validation: SYNTHETIC
- Dependencies: T-SAFETY-01
- Owner: claude/primary
- Claimed: 2026-09-22
- AC: AC-T-DOCS-05
- Evidence: The README now opens with the problem — a session ends and the next participant loses what the code meant — before naming any record, and shows both projections of project state instead of asserting them: the dashboard for a person, an abridged `prokron context` packet for an agent. Implemented, designed and unproven claims are separated in the README and labelled per claim in a new `docs/PRODUCT-THESIS.md`. `docs/SPEC.md` was corrected where it contradicted the shipped product: it listed the CLI and dashboard as out of scope, cited a v0.1 file, and named a moved directory. All five images are preserved, unmodified and unrenamed. Three new tests hold the documentation to its own facts; 122 unit tests and the installer suite pass.
- Governed by: ADR-026
