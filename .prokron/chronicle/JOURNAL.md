# Journal

## 2026-09-15 — v0.1 implementation resumed
- Task: T-V01-01
- Owner: codex/primary
- Did: Read the authoritative thesis and implementation brief; inventoried the partial CLI.
- Validation: Existing end-to-end test passed before the v0.1 hardening work.
- Learned: The repository has a useful vertical slice but lacks strict parsers, full integrity checks, idempotent bootstrap, checkpoint, adoption, adapters, and a realistic fixture.
- Left mid-air: Typed parser and integrity implementation is about to begin.
- Next: Claim T-V01-01 and replace permissive parsing with typed deterministic canonical parsing.

## 2026-09-15T09:14:41Z — T-V01-01
- Task: T-V01-01
- Owner: codex/primary
- Did: Added typed task, decision, intent, and journal models; strict Markdown parsers; validation; deterministic renderers; and required core tests.
- Validation: 14 unittest cases pass; compileall passes.
- Learned: Strict one-line canonical fields keep Markdown deterministic while fenced examples remain safe.
- Left mid-air: Core parsing and integrity are complete; initialization and adoption remain.
- Next: Complete idempotent init/adopt and managed bootstrap validation.

## 2026-09-15T09:15:15Z — T-V01-02
- Task: T-V01-02
- Owner: codex/primary
- Did: Completed idempotent init/adopt, packaged templates, and managed AGENTS.md/CLAUDE.md bootstrap installation that preserves custom content.
- Validation: 15 unittest cases pass; repeated init and adoption checked in temporary Git repositories.
- Learned: Adoption can safely initialize explicit empty state without pretending to reconstruct missing history.
- Left mid-air: Initialization and adoption are complete; context/checkpoint continuity remains.
- Next: Claim T-V01-03 and validate deterministic context and checkpoint edge cases.

## 2026-09-15T09:16:20Z — T-V01-03
- Task: T-V01-03
- Owner: codex/primary
- Did: Completed deterministic context traversal and resumable checkpoint updates with append-only Journal entries and input validation before mutation.
- Validation: 15 unittest cases pass, including context minimality, append preservation, invalid checkpoint rollback behavior, and refreshed doctor state.
- Learned: One-line CLI validation is necessary because command values are written directly into canonical Markdown.
- Left mid-air: Context and checkpoint are complete; adapters and the checked-in realistic example remain.
- Next: Close T-V01-03, claim T-V01-04, add thin adapters, and generate the example derived files.

## 2026-09-15T09:17:33Z — T-V01-04
- Task: T-V01-04
- Owner: codex/primary
- Did: Added thin Codex, Claude, and generic CLI adapters plus a realistic greenfield fixture with decision lineage, parallel work, active intent, journal handoff, and generated views.
- Validation: 16 unittest cases pass; example prokron doctor reports healthy; generated graph identifies T-003 as independently eligible.
- Learned: Bootstrap instructions are sufficient adapters for v0.1 because every semantic operation remains in the shared CLI core.
- Left mid-air: Adapters and example are complete; final architecture cleanup, build checks, documentation, and handoff remain.
- Next: Close T-V01-04, claim T-V01-05, split the oversized core module, run all release checks, and leave the final checkpoint.

## 2026-09-15T09:24:05Z — T-V01-05
- Task: T-V01-05
- Owner: codex/primary
- Did: Completed v0.1: typed canonical models and parsers, integrity engine, deterministic graph/state/context, init/adopt/bootstrap, checkpoint continuity, thin adapters, realistic fixture, documentation, packaging, and release tooling.
- Validation: Ruff passes; strict mypy passes for 8 source files; 17 unittest cases pass; wheel and sdist build; built wheel passes init, doctor, graph, status, next, and repeated init in a clean Git fixture; example doctor passes.
- Learned: The smallest viable architecture is four boundaries: canonical parsing, integrity core, deterministic rendering, and lifecycle operations behind one CLI.
- Left mid-air: No v0.1 implementation work remains; release artifacts are built locally and the repository has not been committed or published.
- Next: Review the v0.1 CLI, then commit or publish it when approved; begin v0.2 only after real protocol feedback.

## 2026-09-15 — T-V01-06
- Task: T-V01-06
- Owner: codex/primary
- Did: Standardized all product identifiers as Prokron and added a GitHub README, tutorial, CLI reference, and architecture guide.
- Validation: Legacy-name scan is empty; Ruff, strict mypy, 26 unittests, package build, CLI health checks, and documentation link checks pass.
- Learned: A short README plus three focused documents keeps the public entry point readable while preserving complete operational detail.
- Left mid-air: Implementation and documentation are verified; commits and the initial remote push remain.
- Next: Commit the implementation and documentation, then push main to the Prokron repository.

## 2026-09-15 — T-V011-01
- Task: T-V011-01
- Owner: codex/primary
- Did: Changed the next release to Apache-2.0, added NOTICE and trademark policy, documented the v0.1 MIT history, and audited package metadata and contributors.
- Validation: Canonical license text and 0.1.1 artifact payloads match; Ruff, strict mypy, 26 unittests, package build, and Prokron doctor pass.
- Learned: Main history has one project-owner author identity and a Codex co-author trailer on the substantive v0.1 commit; no external human or vendored code license was found.
- Left mid-air: No licensing implementation remains; legal ownership cannot be proven from Git metadata alone.
- Next: Review and publish v0.1.1 without modifying the historical v0.1 artifacts or license grant.

## 2026-09-15 — T-V011-02
- Task: T-V011-02
- Owner: codex/primary
- Did: Added the missing installed-version command, rebuilt wheel and sdist artifacts, and ran clean-room initialization, idempotency, and adoption workflows outside the source checkout.
- Validation: Ruff, strict mypy, 27 unittests, build, doctor, offline wheel install, sdist install, fresh repository workflow, and three-commit adoption all pass.
- Learned: Release validation must invoke the installed console script because source tests did not expose the missing --version interface.
- Left mid-air: Verification is complete; GitHub release publishing is unavailable because the configured gh tokens are invalid.
- Next: Re-authenticate gh, push the verified commit, and create the v0.1.1 release with both artifacts.

## 2026-09-15T11:17:17Z — T-V02-01
- Task: T-V02-01
- Owner: codex/primary
- Did: Added deterministic adoption discovery and source classification, non-canonical candidate state, explicit confidence and provenance, targeted confirmation, legacy handoff import, a baseline decision, and guarded apply.
- Validation: 29 unittests, Ruff, strict mypy, isolated-output package build, installed-wheel dry-run smoke test, and Prokron doctor pass.
- Learned: Filename discovery can bound retrieval, but architecture prose must remain unknown until a human confirms it; source priority alone cannot establish authority.
- Left mid-air: Adoption-boundary implementation is complete; no candidate or canonical project state was changed by the live dry-run.
- Next: Exercise the adoption workflow on real external repositories before expanding semantic extraction.

## 2026-09-15T11:40:11Z — T-V02-02
- Task: T-V02-02
- Owner: codex/primary
- Did: Replaced presence-only coverage and generic questions with a fixed evidence-backed coverage schema, contextual structured prompts, conditional and optional domain semantics, canonical operational materialization, and honest discovery-versus-inspection reporting.
- Validation: 33 unittests, Ruff, strict mypy, isolated wheel/sdist build, installed-wheel dry-run smoke test, Git diff check, and Prokron doctor pass.
- Learned: Human confirmation is useful only when its operational effects enter canonical tasks and intents; optional history can remain explicitly unknown without blocking adoption.
- Left mid-air: The requested v2 semantic remediation is complete; broader semantic interpretation remains intentionally external to Core.
- Next: Validate the bounded heuristics and structured interview handoff against real existing repositories.

## 2026-09-16 — T-V02-03
- Task: T-V02-03
- Owner: codex/primary
- Did: Added a guided six-domain adoption interview, persisted resumable answers with human-confirmation provenance, structured JSON question and answer primitives for agents, and canonical materialization of confirmed operational state.
- Validation: Ruff, strict mypy, 49 unittests, wheel/sdist build, installed-wheel non-interactive and interactive adoption, apply and doctor smoke tests, K-Ledger dogfood, and Git diff check pass.
- Learned: A generated interview report is useful audit evidence, while stable structured primitives are the safer interface for both humans and agents.
- Left mid-air: The validated implementation and documentation remain uncommitted as requested.
- Next: Review the diff and commit only when explicitly approved.

## 2026-09-15T17:51:16Z — T-V02-03
- Task: T-V02-03
- Owner: codex/primary
- Did: Committed the interactive adoption interview as cb65c19 and pushed it to origin/main.
- Validation: The push advanced origin/main from b37a29f to cb65c19; the worktree was clean immediately afterward.
- Learned: Publication completed without changing the validated implementation.
- Left mid-air: Only this Prokron continuity update remains uncommitted.
- Next: Begin new work from the current clean implementation baseline; commit this state reconciliation when approved.

## 2026-09-15T18:03:04Z — T-V02-04
- Task: T-V02-04
- Owner: codex/primary
- Did: Replaced six current-state forms with one default-preserving proposal, made selective active-work edits retain inferred identity fields, removed adoption/interview ownership, separated recent commit evidence from execution point, and tightened agent adapter guidance.
- Validation: Ruff, strict mypy, 51 unittests, wheel/sdist build, installed-wheel K-Ledger grouped-confirmation and apply smoke tests, Prokron doctor, and Git diff check pass.
- Learned: Conservative defaults let one explicit human confirmation establish several related domains without moving validation or authority into adapters.
- Left mid-air: The validated UX refinement and its Prokron checkpoint remain uncommitted as requested.
- Next: Review the grouped K-Ledger interaction and commit only when explicitly approved.

## 2026-09-16 — T-V02-05
- Task: T-V02-05
- Owner: codex/primary
- Did: Reproduced and fixed Markdown navigation being inferred as a next action, added a focused regression, and reran the real K-Ledger grouped proposal without supplying human answers.
- Validation: Ruff, strict mypy, 52 unittests, and Git diff check pass; K-Ledger now reports its next safe action as unknown.
- Learned: Planning-document summaries require executable verb semantics before they can become an action hypothesis.
- Left mid-air: K-Ledger confirmation, apply, continuity validation, distribution gates, final commit, and push remain.
- Next: Ask the developer to confirm or correct the grouped proposal and provide the exact next safe action.

## 2026-09-16 — T-V02-05 K-Ledger apply failure
- Task: T-V02-05
- Owner: codex/primary
- Did: Persisted all six human confirmations, applied the K-Ledger candidate, ran doctor, status, next, and an isolated fresh-agent continuity read.
- Validation: Apply, doctor, status, next, build, installed-wheel generic smoke, and state recovery pass; no-history-reconstruction fails because canonical TASKS.md contains roughly 128 legacy table rows while the parsed graph contains one task.
- Learned: A legacy file can parse as zero canonical records yet still be carried forward as canonical Markdown when unrelated fenced content bypasses the incompatibility guard.
- Left mid-air: K-Ledger now has an applied .prokron directory exhibiting this continuity defect; Prokron closure remains uncommitted.
- Next: Prevent zero-record legacy payloads from becoming canonical text, add a regression, then rerun adoption from a clean K-Ledger pre-adoption state only with explicit authorization for that reset.

## 2026-09-15T19:17:06.221046+00:00 — deterministic harness extraction
- Task: T-HARNESS-01
- Owner: codex/primary
- Did: Audited module boundaries and implemented agent-authored adoption while demoting the existing heuristic engine to explicit fallback.
- Validation: 68 unittests, Ruff and strict mypy pass; artifact build pending.
- Learned: Existing deterministic models, graph validation, parsers and lifecycle operations were separable; a wholesale rewrite was unnecessary.
- Left mid-air: Package verification and final acceptance record remain. T-V02-05 is prior fallback dogfood work; its existing edits and failure evidence are preserved.
- Next: Verify the installed artifact and finalize T-HARNESS-01.

## 2026-09-15T19:17:06.221310+00:00 — deterministic harness acceptance
- Task: T-HARNESS-01
- Owner: codex/primary
- Did: Completed the agent-driven primary path, explicit fallback extraction, provider-neutral adapters, and continuity acceptance checks on refactor/deterministic-state-harness.
- Validation: 68 unittests, Ruff, strict mypy, wheel/sdist build, clean installed-wheel brownfield adoption and fresh-process resume, stale-state rejection, fallback import, and Git diff check pass on 2026-09-16.
- Learned: Fresh-process continuity succeeds from the canonical snapshot and operational Markdown; no repository rediscovery is required. A live cross-model human interview was not exercised.
- Left mid-air: Implementation is complete and uncommitted for branch review. Prior T-V02-05 dogfood is blocked/deferred because its remaining incompatible-table issue is now confined to optional fallback. Existing navigation fix and regression are preserved there.
- Next: Review the deterministic harness branch; address fallback legacy payload carry-through only if that importer is needed.

### Preserved prior T-V02-05 intent

```text
- Owner: codex/primary
- Updated: 2026-09-16
- Goal: Close Adoption Boundary only after the real K-Ledger adoption and continuity checks pass.
- Current point: Next-action inference and the K-Ledger apply flow pass, but adoption copied the legacy tabular task board into canonical TASKS.md even though zero legacy tasks were imported.
- Constraints: do not fabricate confirmation, do not weaken the apply guard, do not commit before end-to-end passage
- Changed files: src/prokron/adoption.py, tests/test_adoption.py
- Next action: Fix empty or incompatible legacy state payload carry-through before rerunning K-Ledger adoption from a clean pre-adoption state.
```

## 2026-09-15T19:23:58.545428+00:00 — deterministic harness cleanup
- Task: T-HARNESS-02
- Owner: codex/primary
- Did: Reused validated snapshots through apply/next/resume, moved Markdown renderers into rendering.py, reused schema definitions and replaced the suppressed candidate-conversion type error with typed record conversion.
- Validation: 69 tests, Ruff, strict mypy, doctor, and synced CodeGraph status pass.
- Learned: CodeGraph confirmed that next and resume reached publication-only Markdown round-trip validation through adopted_state; reads now use schema and graph validation while ingest and apply retain the round trip.
- Left mid-air: Cleanup complete; branch changes remain uncommitted. CodeGraph 1.6.0 is installed, connected to Codex, and its 19-file project index is current.
- Next: Review and commit the deterministic harness branch.

## 2026-09-15T20:46:18+00:00 — semantic fallback removal
- Task: maintenance/fallback-removal
- Owner: codex/primary
- Did: Removed the semantic adoption engine, fallback CLI, legacy tests, and superseded adoption supplement; compacted deterministic docs and CLI tests.
- Validation: 50 tests, Ruff, strict mypy, wheel/sdist build, doctor, Git diff check, and synced CodeGraph status pass.
- Learned: The deterministic harness fully replaces the semantic fallback; no source or test callers remain.
- Left mid-air: Local main is ready to push after explicit approval for the GitHub destination.
- Next: Push local main to the approved origin.

## 2026-09-15T21:17:27+00:00 — workflow-only rebuild
- Task: T-WORKFLOW-01
- Owner: codex/primary
- Did: Rebuilt Prokron as a six-file project chronicle with two entry modes, five agent workflows, a Codex skill, Claude slash commands, and automatic checkpoint instructions; removed the Python runtime, package, tests, adoption artifacts, and obsolete specifications.
- Validation: New- and existing-repository template smoke checks, README link checks, Codex skill metadata validation, requirement scans, and Git whitespace checks pass.
- Learned: The K-Ledger handoff confirms that task dependencies, one live intent, decision lineage, current state, and a concise session diary are sufficient for useful human and agent continuity.
- Left mid-air: Nothing. The working tree is ready for commit.
- Next: Use the workflow in a real project and refine only from observed friction.

## 2026-09-16 — GitHub documentation rewrite
- Task: T-DOCS-01
- Owner: codex/primary
- Did: Rewrote the README and specification around the six-file chronicle, the two entry modes, exact Claude and Codex commands, automatic checkpoints, and the workflow-only product boundary.
- Validation: All 10 README links resolve; requirement and repository-shape checks pass; Git reports no changes to LICENSE, NOTICE, or TRADEMARKS.md and no whitespace errors.
- Learned: The GitHub entry point is clearest when it explains the task graph and decision lineage first, then installation and commands.
- Left mid-air: Nothing.
- Next: Use Prokron in a real repository and change the workflow only when observed use reveals friction.

## 2026-09-16 — one-command bootstrap
- Task: T-INSTALL-01
- Owner: codex/primary
- Did: Added one POSIX shell bootstrap that installs the chronicle, workflows, Codex skill, Claude commands, and managed agent instructions; documented one-line new and existing repository setup.
- Validation: POSIX syntax and installer smoke checks pass for both modes, all copied assets, repeat installation, state and instruction preservation, and invalid input; documentation links, legal-file preservation, and Git whitespace checks pass.
- Learned: Installation needs one disposable copier; the working product remains the Markdown chronicle and agent instructions.
- Left mid-air: Nothing.
- Next: Run the published curl command from a real target repository and begin with the printed agent command.

## 2026-09-16 — published bootstrap check
- Task: T-INSTALL-01
- Owner: codex/primary
- Did: Ran the documented installer from GitHub after publishing it.
- Validation: Failed before installation because unauthenticated raw GitHub access returns 404 for the private repository.
- Learned: Delivery must use the authenticated GitHub CLI until the repository is public.
- Left mid-air: The local installer works; authenticated remote delivery is not yet verified.
- Next: Fetch the installer and source with `gh`, republish, and rerun the disposable-repository check.

## 2026-09-16 — authenticated bootstrap acceptance
- Task: T-INSTALL-01
- Owner: codex/primary
- Did: Switched private-repository delivery to the authenticated GitHub API for both the installer and source archive, then republished it.
- Validation: The exact README command installed the chronicle, workflows, Codex skill, and Claude commands from private GitHub `main` into a disposable repository; local syntax, both-mode, preservation, repeat-install, invalid-input, link, legal-file, and whitespace checks pass.
- Learned: `gh api` provides one command for private repositories without adding credentials or a package runtime.
- Left mid-air: Nothing.
- Next: Run the existing-repository command in the target project and start with the printed agent-chat command.

## 2026-09-16 — model-neutral agent hosts
- Task: T-HOSTS-01
- Owner: codex/primary
- Did: Added five OpenCode project commands, taught the installer to copy them and print OpenCode and generic-agent starts, and documented how GLM, MiniMax, Mistral, Grok, and other models use Prokron through their agent host.
- Validation: OpenCode command metadata, local installer behavior, all host assets, generic guidance, documentation links, legal-file preservation, and Git whitespace checks pass; the published private-GitHub installer delivered `AGENTS.md` and all five OpenCode commands to a disposable repository.
- Learned: Model providers need no Prokron-specific files; host-native commands plus the open `AGENTS.md` convention cover the workflow without coupling project memory to a model.
- Left mid-air: Nothing.
- Next: Install Prokron in the target repository, choose any model in its host, and start with the printed command.

## 2026-09-16 — repository CodeGraph removal
- Task: T-CLEANUP-01
- Owner: codex/primary
- Did: Removed the ignored CodeGraph index and its repository ignore rule because Prokron no longer contains application code.
- Validation: `.codegraph/` is absent, product files contain no CodeGraph configuration, and Git whitespace checks pass.
- Learned: The Markdown workflow needs no repository code index.
- Left mid-air: Nothing in the repository. The shared global CodeGraph installation remains outside project scope.
- Next: Open the clean repository and use the Prokron workflow directly.

## 2026-09-16 — automatic continuity guarantees
- Task: T-CONTINUITY-01
- Owner: codex/primary
- Did: Made task creation, material-decision ADR capture, exact intent maintenance, and pre-limit checkpointing automatic across shared agent rules, the Codex skill, portable workflows, chronicle templates, and public documentation.
- Validation: Local installer checks and the published private-GitHub installer confirm that a fresh repository receives all automatic triggers; documentation links, legal-file preservation, and Git whitespace checks pass.
- Learned: Continuity rules must fire on work events and agent limits, independent of whether the developer invokes a Prokron command.
- Left mid-air: Nothing.
- Next: Let the installed agent maintain the chronicle during normal work; use manual commands only when an explicit workflow is useful.

## 2026-09-16 — readiness fixes and evidence boundaries
- Task: T-READINESS-01
- Owner: codex/primary
- Did: Protected populated chronicles from repeat init, restored missing install files, documented manual upgrades, forwarded decision arguments, and documented offline/public installation plus a real-agent handoff pilot.
- Validation: Installer regressions pass for fresh modes, all-record and custom-instruction preservation, incomplete installs, argument delivery, symlink rejection, and invalid input. Shell syntax, Git whitespace, and unchanged legal files pass.
- Learned: The previous “automatic continuity guarantees” entry proves delivery of instructions, not guaranteed agent compliance or hidden quota detection. Real limit handling and fresh-session behavior remain unverified; the pilot must record observed host/model behavior.
- Left mid-air: Implementation and local checks are complete; commit and publication are next. No real-agent pilot was run.
- Next: Publish the readiness fixes, then use the handoff pilot in a target project before claiming verified cross-session continuity.

## 2026-09-16 — GitHub introduction and graphics
- Task: T-DOCS-02
- Owner: codex/primary
- Did: Rewrote the README around recovering work across sessions, added an SVG banner and Mermaid workflow, and illustrated a handoff with tasks, decision lineage, and the next action. Kept installation, manual upgrades, and continuity limits explicit.
- Validation: All 15 local links/anchors and SVG XML pass; the full banner was rendered in an isolated browser and visually inspected. Git whitespace checks pass and legal files are unchanged. No runtime or dependency was added.
- Learned: A concrete handoff example explains the value more clearly than a file inventory alone. The example is labeled illustrative and makes no new reliability claim.
- Left mid-air: Documentation is complete and ready to publish; the real-agent pilot remains pending.
- Next: Commit and push the documentation, then use the handoff pilot in a target project.

## 2026-09-16 — shared understanding as the product story
- Task: T-DOCS-03
- Owner: codex/primary
- Did: Recorded the owner's clarification in ADR-012; rewrote the README, diagram, banner, specification purpose, and chronicle guide around Project Chronicle as a common language for people and AI. Replaced the session-only example with a project's historical change of direction and added a human comprehension step to the pilot.
- Validation: All 15 local links/anchors and SVG XML pass. The new banner was rendered in an isolated browser and visually inspected; whitespace checks pass and legal files are unchanged.
- Learned: Shared understanding of purpose, history, current state, and future work is the core benefit. Handoffs between people and agents are one use of that record.
- Left mid-air: Documentation is complete and ready to publish. Human comprehension and real-session agent behavior still need the pilot.
- Next: Publish the revised documentation and graphic, then compare a person's and an agent's understanding in a target project.

## 2026-09-17 — origin URL update
- Task: T-REMOTE-01
- Owner: codex/primary
- Did: Changed local origin from https://github.com/qomerovn/prokron.git to https://github.com/qomero/ten-repo.git as requested.
- Validation: git remote -v confirms both fetch and push URLs.
- Learned: This updates local Git configuration; remote availability was not checked.
- Left mid-air: Nothing for this request.
- Next: None for this request; the existing project pilot remains pending.

## 2026-09-17 — global Git username
- Task: T-GIT-NAME-01
- Owner: codex/primary
- Did: Set global Git user.name to qomero as requested.
- Validation: Global configuration readback returned qomero.
- Learned: The requested global username is configured.
- Left mid-air: Nothing for this request.
- Next: None for this request; the existing project pilot remains pending.

## 2026-09-21 — Phase 2 planned onto its own branch
- Task: T-P2-PLAN-01
- Owner: claude/primary
- Did: Created the `Phase2` branch, read `docs/Phase 2.md` in full, and resolved its three conflicts with the existing chronicle in favour of the specification. Recorded ADR-013 (Phase 2 governs; a deterministic runtime returns, superseding ADR-008), ADR-014 (authored `prokron/` versus compiled `.prokron/`), ADR-015 (the PHASES, TASKS, ACCEPTANCE, ADR/, INTENT, HANDOFF authority set), and ADR-016 (standard-library-only implementation). Split the specification into fourteen tasks along the requested trunk order: acceptance, phase, compiler, analytics, renderer.
- Validation: UNTESTED. This is a planning record; no Phase 2 behaviour exists yet.
- Learned: The specification contradicts itself on `.prokron/`, naming it both generated-and-disposable and the home of authority. ADR-014 resolves this by splitting authored from compiled state, which is the distinction the rest of Phase 2 depends on. Superseding rather than deleting the earlier ADRs keeps the reversal of ADR-008 visible.
- Left mid-air: Nothing. Planning is complete and uncommitted on the `Phase2` branch, along with two earlier chronicle entries (T-REMOTE-01, T-GIT-NAME-01) that were already pending on `main`.
- Next: Start T-P2-01. Move authority to `prokron/`, split `DECISIONS.md` into one file per ADR under `prokron/ADR/`, add `HANDOFF.md`, update the installer, templates, workflows, host adapters, `AGENTS.md`, and `README.md`, and reserve `.prokron/` for compiled output.

## 2026-09-21 — acceptance and phase authority built
- Task: T-P2-01, T-P2-02, T-P2-03, T-P2-04, T-P2-05
- Owner: claude/primary
- Did: Split authored authority from compiled state. Moved the chronicle to `prokron/` and reduced `.prokron/` to views. Split `DECISIONS.md` into sixteen ADR files with a supersession index. Wrote `ACCEPTANCE.md`, defining criterion identity, Given/When/Then structure, five evidence classes, three criterion states, four inherited contracts, the reviewer finding taxonomy, and the frozen-contract and change-request rules. Migrated all forty tasks from prose acceptance to contract references in one pass. Wrote `PHASES.md` with P0, P1, and P2, six gates, and four milestones, and gave every task a phase. Put the builder contract, reviewer classification, and arbitration hierarchy into `AGENTS.md`, the workflows, and the skill. Updated the installer, templates, host adapters, README, and specification to the new layout.
- Validation: AI_REVIEWED. `sh tests/install.sh` passes with new assertions that a fresh install creates authority under `prokron/`, that no authority document lands in `.prokron/`, and that reinstall preserves every record including the ADR directory. A repository scan finds no stale authority path. All local documentation links resolve.
- Learned: The specification's own contradiction—`.prokron/` as both generated and authoritative—was the load-bearing question. Splitting authored from compiled resolved it and made the rest of Phase 2 straightforward. Migrating historical acceptance verbatim rather than restating it in Given/When/Then form keeps closed evidence attached to what it actually attested to.
- Left mid-air: Nothing partially written. The work is uncommitted on `Phase2`, together with two earlier chronicle entries pending from `main`. The README banner and Mermaid diagram still depict the six-file chronicle.
- Next: T-P2-06. Build the standard-library-only `prokron` command with typed parsers, `validate`, and `compile`, writing only inside `.prokron/`.

## 2026-09-21 — the deterministic runtime
- Task: T-P2-06, T-P2-07, T-P2-08, T-P2-09, T-P2-10, T-P2-11, T-P2-12
- Owner: claude/primary
- Did: Built `src/prokron/`, a standard-library-only package: typed model, parsers for every authored document, the `project.json` compiler with per-object provenance, cross-document validation, deterministic analytics, six Mermaid renderers, the Markdown views, a self-contained HTML dashboard, and the `prokron` CLI. Made the compiler own every file in `.prokron/`, including `STATE.md` and `TASK_GRAPH.md`, which were previously hand-maintained. Taught the installer to ship the runtime as copied files under ADR-017. Updated the agent rules, workflows, skill, README, and specification to use the tool instead of re-deriving state by reading files.
- Validation: AI_REVIEWED. 66 unit tests and the installer suite pass. `rm -rf .prokron && prokron compile` reproduces `project.json` and all three views byte for byte on this repository and in the fixture. Headless Chrome rendered the dashboard from `file://`, opened the drill-down with the task's full contract, and rendered every figure with Mermaid unreachable. Gates A, B, C, and D moved to GREEN on that evidence; Gate E and Gate P1-CONTINUITY stay RED because both need a real session.
- Learned: Four parser bugs only surfaced against the real chronicle rather than the fixture — nested sections swallowing later content, criterion states wrapped onto a second line, milestone task IDs on continuation lines, and gates writing `Label: value` where phases write the label on its own line. Authored Markdown varies in ways a fixture written by the same author will not reproduce. Also: making the compiler generate the views, rather than seeding them from templates, is what finally made `.prokron/` honestly disposable.
- Left mid-air: Nothing partially written; everything is uncommitted on `Phase2`. T-P2-13's `MANUAL` criterion and T-P2-14's two-agent audit remain, and both need a live session rather than a test.
- Next: T-P2-13, then T-P2-14. Hand a `prokron context` packet to a second agent and record where the two disagree and which level of the arbitration hierarchy settles it.

## 2026-09-21 — audit and the 0.2.0 release
- Task: T-P2-AUDIT-01
- Owner: claude/primary
- Did: Audited the Phase 2 runtime before release and fixed seven defects, each with a regression test. The embedded JSON island broke whenever authored text contained `</script>`, which killed the whole dashboard. Task titles, phase outcomes, gate descriptions and obstacle details were interpolated into markup unescaped, both when generating the page and in the client-side drill-down. The inline Mermaid block was injected raw. A gate blocking `P11 exit` also blocked `P1`, because phase matching was a substring test. A criterion missing its evidence class silently swallowed every criterion after it. A DONE task whose contract stated no criteria passed validation. Work in flight was counted as ready as well as WIP. Then cut 0.2.0: added `VERSION` and `CHANGELOG.md`, made the runtime read the version shipped beside it rather than the tracked project's own, and refreshed the README example from real output.
- Validation: AI_REVIEWED. 80 unit tests, up from 66, and the installer suite pass. Headless Chrome confirmed the escaping fix did not break Mermaid: the diagram still renders to SVG and label line breaks survive, because the browser decodes entities before Mermaid reads the text.
- Learned: Every defect but one came from treating authored prose as if it were safe markup. A chronicle is written by people, so its text will eventually contain angle brackets, quotes, and the odd closing tag — a generator that assumes otherwise breaks on the first honest sentence. The parser bug was the most dangerous of the seven: a contract that silently loses criteria makes a task look done against a bar nobody agreed to.
- Left mid-air: Nothing. 0.2.0 is merged to `main`.
- Next: T-P2-13's `MANUAL` criterion, then T-P2-14 and Gate E — both need a real session with a second agent rather than another test.

## 2026-09-21 — Phase 2 closes, audited by a second agent
- Task: T-P2-13, T-P2-14
- Owner: claude/primary
- Did: Raised ACR-001 and ACR-002 to reclassify the two agent-subject criteria from MANUAL to RUNTIME, since neither names a human and a human's report was never the right evidence. Ran the cold-start experiment against the Codex CLI with no repository: the first run refused and named a contradiction in the packet, which disproved AC-T-P2-13-02 as recorded; packets were scoped to their own task under ADR-018 and the retry started cleanly from 2.6 KB. Ran Gate E for real. Codex audited the scheduling implementation against the reviewer packet and returned an ACCEPTANCE_FAILURE where Claude had recorded PASS. The disagreement was settled by rendering both Gantt variants in headless Chrome, which showed unscheduled work inheriting a calendar date; the defect was real and is fixed. Round two: both agents PASS all three criteria, no blocking findings, differing only in non-blocking preference. Added tests that run against the real chronicle rather than a fixture, ran the definition-of-done sweep, fixed current-phase reporting for a phase awaiting exit, and cut 0.2.1.
- Validation: AI_REVIEWED. 92 unit tests and the installer suite pass. All 39 tasks are DONE, all 88 criteria PASS, and five of six gates are green on recorded evidence.
- Learned: Both experiments found real defects, and both defects were invisible from the inside. The packet looked complete to its author and incoherent to a stranger; the Gantt looked honest until someone who knew Mermaid's implicit-date rule read it. That is the argument for Gate E stated better than the gate itself states it. Worth noting too that the first cold start "failing" was the more informative half: an agent that refuses an incoherent packet and says why is behaving correctly, and the pair of runs proves the packet carries a start rather than that one model is agreeable.
- Left mid-air: Nothing. P2 is EXIT_PENDING; accepting the exit is the owner's decision.
- Next: Gate P1-CONTINUITY, the one thing in this project that no test can stand in for. It needs a real multi-session pilot in a real project.

## 2026-09-21 — continuity pilot, steps 1 and 2
- Task: T-PILOT-01
- Owner: claude/primary
- Did: Started the continuity pilot from `docs/SPEC.md` against a real agent host, Codex CLI 0.155.0, in a disposable Tea Timer repository with Prokron 0.2.1 installed by `install.sh`. Step 1 passed in both entry modes: from a five-requirement specification the agent derived six product tasks and a phase-exit task with twenty criteria, four ADRs, one phase with a gate, and a real dependency chain; existing mode stayed empty and left the repository's own code untouched. Step 2 passed: an ordinary request with no Prokron command, for work deliberately absent from the task list, produced a new task and contract before implementation and a cleared intent with the next action afterwards. Observations are in `docs/pilot-2026-09-21.md`.
- Validation: UNTESTED as a whole. Two of seven criteria pass; the rest are not yet run.
- Learned: Two behaviours appeared without being asked for. The agent claimed a task for the initialization itself before doing it, and it discovered `./bin/prokron` from `AGENTS.md` and ran validate and compile on its own. The most useful observation came from a failed run: blocked by a read-only sandbox, the agent drafted the work, said plainly that nothing had been written, and named the next action. That is the failure the chronicle exists to survive, and it survived it honestly. Each step takes five to fifteen minutes of real agent time, which is worth knowing before anyone plans to repeat this per host.
- Left mid-air: The pilot is mid-run. Steps 3 to 6 are not started; the disposable project at /tmp/pilot holds the state and is not part of this repository. Step 7 needs a person.
- Next: Step 3 — make a material choice, then change it, and check that both ADRs remain with the newer superseding the earlier, without `/prokron-decide`.

## 2026-09-21 — the upgrade path that was never written
- Task: T-MIGRATE-01
- Owner: claude/primary
- Did: A real project updated to 0.2.1 and reported that its task graph had vanished. Reproduced it: ADR-014 moved authority from `.prokron/` to `prokron/` and no migration was written, so upgrading leaves the chronicle stranded. Every record survives, because the installer preserves what it finds, but the tool reads the new location and reports an empty project. Wrote `prokron migrate` under ADR-019: report by default, apply only when asked, archive every original unchanged. It moves tasks, decisions, intent and journal, converts prose acceptance into contracts keeping the original wording, splits `DECISIONS.md` into `prokron/ADR/` with a supersession index, rescues `STATE.md` prose into `HANDOFF.md`, and drops `TASK_GRAPH.md` because the compiler regenerates it. Installation and `prokron status` both now detect a stranded chronicle and name the command. Reopened P2, because a phase that ships a layout change without an upgrade path was not complete.
- Validation: AI_REVIEWED. 104 unit tests, up from 93, including eleven covering migration. The installer suite now runs the whole upgrade end to end on a synthetic v0.1 project and checks the task, its contract, the rescued prose, the ADR file, the archive and a clean validate.
- Learned: Preserving files is not continuity. ADR-011 made the installer careful never to overwrite anything, and that care is exactly what hid the problem: the records were all there, so nothing looked broken, while the tool reported zero. A second bug hid behind the first — task completion excluded phase-independent work, so a freshly migrated project also read `0 / 0`, which looks identical to a failed migration. Neither would have surfaced from testing the current version against itself. It took someone upgrading a real project.
- Left mid-air: Nothing. Released as 0.2.2.
- Next: The continuity pilot resumes at step 3. Gate P1-CONTINUITY stays red.

## 2026-09-22 — Phase 2 closes, the pilot becomes named debt
- Task: T-P2-14 (exit authority), T-PILOT-01 (parked)
- Owner: claude/primary
- Did: The owner accepted the P2 exit. Recorded it as ADR-020 rather than as a
  status edit, because closing a phase over an unfinished pilot is a choice and
  not a computation. P2 moves to `COMPLETE`: 17 of 17 tasks done, Gates A
  through E green on recorded evidence, every exit criterion met. Gate
  P1-CONTINUITY governs P1's exit and not P2's, so it never blocked this close,
  but it stays RED and P1 stays `EXIT_PENDING`. T-PILOT-01 returns from `WIP` to
  `TODO` with its contract still frozen, its two passing criteria intact, and
  the evidence it earned now written on the task instead of living only in the
  journal. The single intent slot is free. Also restored `docs/Phase 2.md`,
  which was deleted in the working tree while ADR-013, ADR-014, ADR-015 and the
  P2 phase record all cite it as governing authority.
- Validation: UNTESTED. This is a records change; `prokron validate` and
  `prokron compile` are the check that it holds together.
- Learned: The debt only stays honest because it has three separate homes a
  compile can report — a red gate, an open task, and an accepted decision — and
  a named payoff point rather than an intention. A deferral written as prose in
  a handoff is the kind that quietly expires. Worth noting too that parking a
  task is not the same as weakening it: the contract froze when T-PILOT-01 first
  went `WIP`, and moving the status back does not thaw it.
- Released: 0.2.3. No code changed. The chronicle ships beside the runtime, so a
  governance change to it is still something a user installs, and it gets a
  version for the same reason the code does.
- Left mid-air: Nothing. Intent is empty by design.
- Next: Open P3 from `docs/Phase 3.md`, authority before implementation — the
  accepting ADR, the phase record and gates, the tasks, the contracts, then
  validate and compile. The first P3 task is a planning task that inspects the
  existing architecture, as §25 requires.

## 2026-09-22 — the redirect that was holding the installer up
- Task: T-RENAME-01
- Owner: claude/primary
- Did: The owner account was renamed from `qomerovn` to `qomero`, and every old
  URL still worked, which is why nobody noticed. Verified each one: the raw
  file, the tarball and the `gh api` path all return 200 or resolve through
  GitHub's rename redirect. Replaced the previous owner name in `install.sh`
  and `README.md` under ADR-021, left it intact in this journal because the
  journal records what was true then, and promoted the anonymous `curl` install
  to the documented default now that the repository is public. Removed the
  README's claim that the repository is private and its note that anonymous
  delivery was unverified; it is verified now.
- Validation: SYNTHETIC. `sh -n install.sh` passes, 104 unit tests and the
  installer suite pass, and an anonymous install from the current raw URL
  completed against a disposable git repository.
- Learned: The dangerous kind of breakage is the kind that keeps working. A
  rename redirect looks like a fix and behaves like a deadline: GitHub frees
  the old username, anyone may claim it, and the README's headline command
  pipes that URL straight into `sh`. Nothing was broken today and the exposure
  was still real, which is the argument for addressing the owner by name rather
  than by redirect.
- Left mid-air: Nothing.
- Next: Open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — the README catches up with the product
- Task: T-DOCS-04
- Owner: claude/primary
- Did: Rewrote the README under ADR-022. It had been describing a six-file
  Markdown convention for agent handoff while the product had become a project
  management tool with contracts, phases, gates, obstacles, a critical path and
  a dashboard, and it quoted 37 of 39 tasks from a release three versions back.
  The new structure leads with the project questions a person needs answered and
  where each answer comes from, then makes completion a contract rather than an
  opinion, then explains the shared human and AI record as the mechanism that
  makes those figures trustworthy rather than as the opening claim. Captured
  four screenshots from the compiled dashboard with headless Chrome — project
  metrics with phases and gates, the ready and blocked view with the critical
  path, a task drill-down showing its contract and recorded evidence, and the
  phase flow above the schedule and validation panels — and replaced every
  quoted figure with output from a run against the chronicle as committed. Added a section that separates verified
  claims from unverified ones.
- Validation: SYNTHETIC. All 28 local links and anchors resolve, 105 unit tests
  and the installer suite pass, and the screenshots were taken from a fresh
  `prokron dashboard` of this repository.
- Learned: The honest version was also the better pitch. The screenshots show
  one red gate, one unfinished task and a drill-down whose evidence paragraph is
  a record of two agents disagreeing — and that reads as a working project
  management tool in a way that a cropped, all-green dashboard would not. A tool
  that claims completion is a contract has to be willing to show its own
  incomplete contract.
- Left mid-air: Nothing. Released as 0.2.5.
- Next: Open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — the gate view had never rendered
- Task: T-GATEVIEW-01
- Owner: claude/primary
- Did: Capturing README screenshots meant opening every dashboard tab, and the
  Gates tab showed `Syntax error in text` instead of a diagram. Gates are
  identified by their heading, so `Gate A` reached the Mermaid renderer with a
  space in it, and Mermaid ends an identifier at the first space: one malformed
  identifier fails the entire diagram rather than one node. `_node` had only
  ever replaced hyphens, which is all a task ID contains. Widened it to replace
  every character outside `[0-9A-Za-z_]`, regenerated the views, and confirmed
  in headless Chrome that the Gates tab now renders six gates and their edges
  to the phase exits. Added a regression test that scans every identifier in
  the generated gate view, including the ones on the `class` line, and checked
  that reverting the fix fails it.
- Validation: SYNTHETIC. 105 unit tests, up from 104, and the installer suite
  pass. Task identifiers are unchanged, so no other view moved.
- Learned: The fixture had carried a gate called `Gate A` since the beginning,
  so the broken output was generated by every test run and asserted by none of
  them. The tests checked that each view was produced and that it started with
  the right keyword; nothing checked that the text was valid Mermaid, and the
  only way anyone would find out is by opening the tab. Gate B claims dashboard
  rendering is deterministic, and it is — it deterministically rendered an
  error. A view that is generated but never looked at is not covered.
- Left mid-air: Nothing.
- Next: Open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — the author was never the name
- Task: T-AUTHOR-01
- Owner: claude/primary
- Did: Asked to change the commit author, and found the request was aimed at
  the wrong field. GitHub attributes a commit by its email address, so all 32
  commits — including the seven that already carried the current name —
  resolved to a different account holding the address they were written with.
  The address could not be moved, because GitHub refuses one address on two
  accounts and removing it from the other would have un-attributed that
  account's unrelated history. Verified a new address on a throwaway remote
  branch first, confirmed it resolved to the owning account, deleted the
  branch, then rewrote author and committer across the whole history,
  re-pointed the six version tags, and force-pushed once. Kept the pre-rewrite
  tip on a local branch.
- Validation: SYNTHETIC. All 32 commits report one author and one committer;
  the commits API resolves sampled commits from head to root to the owning
  account; `git diff` against the backup is empty; 105 unit tests pass and
  validation is clean.
- Learned: The check that mattered cost one throwaway branch and saved a second
  force-push of a public history. Rewriting first and verifying after would
  have looked identical right up to the point where it was wrong. Also worth
  recording that the probe was run in the working repository rather than in a
  scratch clone, which briefly detached the index from `main` and had to be
  forced back — the right place for a disposable experiment is a disposable
  checkout.
- Left mid-air: Nothing. The pre-rewrite branch `backup-pre-author-rewrite` is
  local only and can be deleted once the rewritten history has been seen to be
  correct.
- Next: Open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — T-LAYOUT-01

- Did: moved everything Prokron installs into one directory. `.prokron/` now
  holds `chronicle/` (authored), `compiled/` (generated), `commands/`,
  `runtime/` and the `prokron` command. Installing used to add five entries to
  the root of a repository Prokron does not own; it now adds one, and the
  installer suite compares the target's entire root listing against the
  expected set so a sixth entry fails a test rather than going unnoticed.
- Why: a tool that claims to reduce a project's confusion should not start by
  scattering itself across that project's root. ADR-024.
- Kept: the authored/compiled separation from ADR-014. It is two
  subdirectories now rather than two root directories, and the compiler still
  writes only into `compiled/`.
- Learned: `.prokron/` means three different things across three releases —
  v0.1 authority, v0.2 compiled output, v0.3 the whole installation. Migration
  detection could not hang off one constant, so `layout.py` names each old
  layout separately and the tool tests for them in order. A single
  `COMPILED_DIR` reused for the v0.1 archive path would have written the backup
  to `.prokron/compiled-v0.1-backup-…`, inside the directory being migrated.
- Learned: the v0.2 upgrade is a move, not a rewrite, so it archives nothing.
  Archiving would have duplicated a whole chronicle to protect against a
  transformation that does not happen. The test asserts the absence of an
  archive rather than its presence, which is the part that could regress
  quietly.
- Noticed: `.claude/commands/prokron-*.md` and their OpenCode equivalents name
  the workflow document by path, so moving the workflows silently breaks them
  on upgrade. Relocation repoints them, and both the unit test and the
  installer suite check that the named document exists afterwards.
- Removed: `templates/.prokron/README.md`. Nothing installed it — the compiler
  generates that file — and the unused copy had already drifted from what the
  compiler writes. A template that nothing reads is a trap for whoever edits it
  next.
- Cost: the command's path is longer, `.prokron/prokron` rather than
  `./bin/prokron`, and the chronicle now sits in a directory a file browser
  hides by default. The chronicle is written to be read by people, so that is a
  real loss; it was accepted because the reading surfaces are `status`, the
  dashboard and the files themselves, all reached by path or command.
- Left: unchanged paths in records written under the old layout — journal
  entries, earlier ADRs, earlier changelog releases, the Phase 2 and Phase 3
  documents. They were accurate when written.
- Next: open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — T-GRAPHVIEW-01

- Did: made the task graph readable. Every diagram now has zoom, pan, pinch, a
  percentage readout and Fit, and hovering a task in the task graph marks its
  transitive dependencies and dependents while dimming everything else.
- Why: at 49 tasks the graph was drawn to fit its panel, which meant a
  laid-out width of 5609px squeezed into about 1100 — roughly 19%. The view
  that exists to answer "what does this depend on" answered nothing.
- Chose: the chain is walked over the compiled `deps` and `blocks` embedded in
  the page, never over the drawing's edges, so a highlight and `explain`
  cannot disagree. ADR-025. Reading it off the SVG would have been shorter and
  would have made the picture a second source of truth.
- Chose: the map from a drawn node back to a task is generated in Python from
  the same function that drew it. Re-implementing the sanitizing rule in
  JavaScript would have drifted silently the first time the rule changed — and
  it did change recently, in T-GATEVIEW-01.
- Learned: Mermaid already labels each node `data-id` and each edge
  `LS-<from>`/`LE-<to>`, so no identifier parsing was needed. Worth dumping the
  rendered DOM before designing around a library's output.
- Fixed, mine: the first version re-fitted on window resize, which silently
  undid the legible opening scale and put the graph back at 19% — the exact
  complaint. Caught in a screenshot, not in a test: the probe that reported
  60% never fired a resize. Resize now re-opens rather than re-fits.
- Decided: fitting is the wrong default for a large graph. A diagram that only
  fits below 60% opens at 60% instead, centred on what is in flight, then what
  is ready, then the critical path. Fit stays one click away.
- Verified: headless Chrome for the hover, the zoom, the tab switch and the
  offline fallback; an independent Python traversal for the chain sizes.
- Next: open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — T-GRAPHVIEW-02

- Did: a task in a diagram now opens the detail dialog the task tables already
  open. Same function, same embedded project, so the two routes cannot drift.
- Watched for: a pan ending on a task and being read as a click. Movement past
  three pixels marks the gesture a pan and suppresses the click. Tested by
  driving the pointer sequence a browser would send, not by trusting the
  handler's shape.
- Watched for: promising a dialog that does not exist. Gates and phases are
  nodes too. Only nodes the node map names as tasks get the pointer cursor and
  the handler; `Gate_A` gets neither.
- Next: open P3 from `docs/Phase 3.md`, authority before implementation.

## 2026-09-22 — T-SAFETY-01 and T-DOCS-05

- Did: restructured the public documentation so the problem comes before the
  mechanism, corrected `docs/SPEC.md` where it contradicted the product, and
  added `docs/PRODUCT-THESIS.md`.
- Found first, fixed first: the README told readers to run
  `rm -rf .prokron && prokron compile`. True until v0.3.0, when `.prokron/`
  stopped being the compiled directory and became the installation. The
  sentence did not change when the layout did, so the published instruction
  deleted a reader's chronicle, runtime and command. Shipped that correction
  on its own, ahead of the rest, because it was live.
- Learned: a path that changes meaning is worse than a path that moves. A moved
  path breaks loudly. `.prokron/` has meant three different things across three
  releases and every reference to it kept working — including the one that was
  now destructive.
- Found: the README argued "one record, both readers" and then showed the human
  reader four times and the agent reader zero times. `prokron context` had one
  table row and no example, despite being the half of the thesis that is
  harder to believe. Showing real packet output was the largest improvement
  available and needed no new code.
- Found: `docs/SPEC.md` §8 listed a CLI and a dashboard as outside the
  specification. Both shipped in P2. §4.1 still pointed at `DECISIONS.md`,
  removed in v0.2. Specifications drift exactly like READMEs and nothing was
  checking.
- Did: three tests now hold the published documents to their own facts — every
  relative link resolves, no `rm -rf` names anything but the compiled
  directory, and the release the README cites matches `VERSION`. The last one
  failed on its first run, which is the point.
- Decided: phase specifications leave the repository (ADR-026). Only one of the
  four described anything built. A specification written as an instruction to
  an agent reads like a description of a shipped feature, which is the wrong
  thing to hand a first-time reader.
- Cost, recorded: ADR-013, ADR-014, ADR-015 and the P2 record cite
  `docs/Phase 2.md` as governing authority and it is no longer in the
  repository. Citations left as written; an outside reader can now check P2's
  exit only against the evidence in the chronicle, not against the document
  that set the bar. ADR-026 says so rather than leaving a dead reference.
- Held the line on: the two entry modes. The four-mode ingress, the evidence
  ladder and repository adoption are specified, not built, and are named that
  way. Writing them as capability would have been the easiest way to make the
  documentation sound better and the product less true.
- Next: open P3, authority before implementation.

## 2026-09-22 — T-CLI-01

- Did: installing is now `curl -fsSL <url> | sh`, and the command is `prokron`
  rather than `.prokron/prokron`.
- Why: both were artefacts of the tool being private. Nobody pays the cost of
  an awkward invocation when the only user wrote it. `sh -s -- existing` asks a
  first-time reader to understand shell argument forwarding before they have
  seen the product, and a path cannot be typed from a subdirectory at all.
- Chose: a launcher on PATH that holds no behaviour. It walks up to the nearest
  `.prokron/prokron` and execs it, so each repository keeps running its own
  runtime and ADR-017's guarantee survives. A global runtime would have been
  simpler and would have silently run one project's compiler against another
  project's records.
- Held to: no directories created, no shell configuration edited, no `prokron`
  replaced that we did not write. Those are the three things installers do that
  make people distrust them. When there is nowhere to link, it prints the alias
  and stops.
- Found, mine: the first version of the installer test wrote a launcher into
  the real `/usr/local/bin` on this machine. The fake `HOME` was honoured but
  the fallback candidate list walked past it to a directory that genuinely
  existed and was writable. Removed it and constrained `PATH` in every
  machine-level case, so the suite cannot reach outside its fixture. A test
  that modifies the machine it runs on is a worse defect than the one it was
  written to catch.
- Found: `install.sh invalid` used to be an error and briefly stopped being
  one, because an unrecognised word became a target directory. Now a second
  positional argument is an error and a target must exist, so a misspelled mode
  fails loudly instead of installing somewhere unintended.
- Fixed, mine: the README I rewrote yesterday showed `$ prokron status` in its
  output blocks while telling readers to type `.prokron/prokron status`. Only
  the second was true. A test now asserts no runnable example starts with the
  path.
- Next: open P3, authority before implementation.

## 2026-09-22 — T-PILOT-01 complete; P1 closed

- Did: ran the continuity pilot in full against v0.4.0. All seven criteria
  pass. Gate P1-CONTINUITY is green, P1 is COMPLETE, and every phase on record
  is now closed with every gate green.
- Why now: ADR-020 had parked the pilot at step 3 of 7 and set its payoff at
  the P3 exit audit, on the assumption that finishing it was expensive. It was
  not — the five outstanding steps took one session. The risk ADR-020 named,
  that Phase 3 would be built on unverified cross-session compliance, is gone
  before Phase 3 opens rather than after.
- Discarded: the 2026-09-21 evidence for steps 1 and 2. It was measured against
  v0.2.1 and cites `./bin/prokron` and a `prokron/` directory that no longer
  exist, so it described a product that is not shipping. Re-run rather than
  reused.
- Learned, from step 5: a cold agent found a stale path in `HANDOFF.md` and
  silently used the correct one, making it more right than the document it was
  reading. A prose path is not a reference the compiler resolves, so neither
  validation nor any test could have caught it. The pilot caught what the
  machinery cannot.
- Learned, from step 6: the agent's own summary was "`new` is an entry mode,
  not a reset of populated history", and on an outstanding validator warning,
  "No evidence was removed to silence the warning." Journal appended with zero
  lines removed; tasks, contracts, phases and every ADR byte-identical.
- Noticed: two of three agents discovered and ran `prokron` without being told
  it existed, using the bare command, which also exercised the v0.4.0 launcher
  from an agent rather than a person.
- Recorded as unproven rather than passed: no host exposed a real limit warning
  to observe, and nothing was simulated in its place. Step 7 passed on the
  owner's attestation without a point-by-point comparison.
- Fixed, mine: the harness twice, not the product. Codex refuses to run outside
  a git repository, and overriding `HOME` to sandbox the launcher also hid
  Codex's credentials.
- Consequence handled: the README and the thesis both pointed at a red gate as
  proof of honesty. That claim is now false, so both were corrected and the
  four dashboard figures regenerated rather than left describing a project that
  no longer exists.
- Next: Phase 0 or Phase 3. New scope, not remaining scope. Authority first.

## 2026-09-22 — T-CI-01

- Did: added continuous integration and the contributor documents a public
  repository needs. Nothing ran this project's tests except a person typing the
  command.
- Chose: CI that enforces the project's own claims, not just `unittest`. Two of
  the central ones had no test at all — that the compiled directory regenerates
  from authority, and that the chronicle validates. Both were true only because
  someone remembered to check.
- Verified before committing: every CI step was run locally first. The
  regeneration check earned its place immediately by failing — run against a
  chronicle whose rebuild had not yet been committed, it named the eight files
  that differed. A check that has never failed is a check nobody has tested.
- Settled by side effect: whether `.prokron/compiled/` should stay committed.
  It stays, because the diff is now the mechanism that proves regeneration. The
  handoff had carried that as an open question.
- Chose: the Python floor is whatever the matrix proves, not what the README
  asserts. Nothing in the runtime uses a feature newer than 3.9, so the matrix
  starts there and will say if that is wrong.
- Chose: no maintainer address published. Reports go through GitHub's private
  advisory form. The conduct document says plainly that a single-maintainer
  project gives a report about the maintainer no independent reviewer, rather
  than implying a process that does not exist.
- Wrote `CONTRIBUTING.md` as the workflow the tool installs, because that is
  what it actually is: a task, a contract frozen before the work, an ADR for a
  material choice, evidence before `DONE`.
- Next: Phase 0 or Phase 3. Authority first.

## 2026-09-22 — T-NAME-01

- Did: a project now names itself in `PHASES.md` instead of inheriting the name
  of the directory it was cloned into.
- Found by: the CI added hours earlier, on its first run. The same authority
  compiled to `Prokron` locally and `prokron` on the runner, and three
  generated files differed.
- Why no test caught it: a fixture is always created under one name. The defect
  only exists across two checkouts, which is precisely the thing a second
  machine provides and a local suite cannot.
- What it actually broke: not just a cosmetic label. Gate B and
  `AC-T-P2-14-01` claim compiled output regenerates from authority, and that
  was only ever true within one machine's directory naming. The wider claim —
  that two participants reading the same project reach the same answer — was
  false the moment two people cloned into differently named directories.
- Rejected: checking the repository out into a fixed directory name in the
  workflow. That would have made the pipeline green by making it dishonest,
  which is the failure this project exists to prevent.
- Kept compatible: a chronicle with no `Project:` line falls back to the
  directory name, so every existing installation works unchanged and nothing
  needs migrating. The template ships the field empty so the next project sees
  it exists without being made to fill it.
- Verified by mutation: reverting to `root.name` fails the new regression test.
- Next: Phase 0 or Phase 3. Authority first.

## 2026-09-22 — First use on an unrelated real project

- Observed, reported by the product owner: Prokron was installed and run on one
  of their own active projects, unrelated to this repository. It behaved as
  expected, and they were able to use it to verify that that project's tasks
  had been done well.
- Why this matters more than it sounds: before today every claim in this
  repository rested on Prokron running against Prokron, two disposable pilot
  fixtures, and a second project opened only to read the dashboard. Working on
  a real codebase with real work in it is the first evidence from outside the
  conditions the tool was built in.
- Recorded narrowly on purpose. The owner reports that it worked and that it
  let them check completion. Which specific claims that exercises — install on
  an unfamiliar repository, an agent maintaining the chronicle during ordinary
  work, the dashboard as a review surface, completion judged against contracts
  rather than assertion — is not yet established, so no criterion is being
  upgraded on the strength of it and no validation state has changed.
- Next: establish what it actually exercised before attaching it as evidence,
  and treat any friction found there as the first real input to Phase 0, which
  until now has been specified entirely from the inside.

## 2026-09-22 — T-UPGRADE-01

- Did: installing now refreshes the generated views, compiled output records
  the version that wrote it, and `status` reports a mismatch.
- Found by: the owner, using Prokron on a real project. They upgraded, opened
  the dashboard, and the interactive task graph was not there. The runtime was
  current; the page was the one the previous release had written.
- Why no test caught it: every fixture in the installer suite installs into a
  directory with no generated output. The upgrade-over-existing-output path had
  never been exercised once, in any release. The suite tested installation and
  called it upgrade.
- Rule that caught the wrong thing: ADR-011 says installation preserves records
  and does not upgrade guidance. Generated views are neither, and were
  protected by a rule not written about them. Worth watching for elsewhere — a
  conservative rule applied one category too wide is invisible until it costs
  something.
- Chose: refresh rather than print an instruction. The views are reproducible
  from authority by definition, so regenerating them risks nothing that the
  chronicle cannot rebuild. Printing a reminder would have left the same broken
  page for anyone who did not read the output.
- Chose: stamp only `project.json`, not all four generated files. One line of
  churn per release rather than four files, and it is enough for `status` to
  detect staleness for a reader who never reinstalls. The cost is that bumping
  the version now changes compiled output, so the CI check from ADR-029 will
  also catch a release that forgot to recompile.
- Mine, and worth recording: while mutation-testing the fix I ran
  `git checkout -- install.sh` to undo the mutation, which also discarded the
  uncommitted fix. Caught it immediately and re-applied. A mutation test on an
  uncommitted file needs a copy, not a checkout.
- Worth noting: this is the second defect in two days found by running the tool
  somewhere other than where it was built — the first was CI finding the
  project name came from the directory. Both were invisible from inside.
- Next: Phase 0 or Phase 3. Authority first.

## 2026-09-22 — T-DOCS-06

- Did: audited the command line and the agent-host surface against a fresh
  installation, then wrote `docs/GUIDE.md` from what the audit observed.
- Why a fresh install: this repository is the one place where everything works
  by construction. The last two defects were both found somewhere else.
- Found: Claude Code shows the body of a command file in its slash menu, so a
  user read `Follow .prokron/commands/prokron-work.md` while the same command
  in OpenCode read `Start or continue one Prokron task`. The mechanism was
  showing where the intent should have been. Fixed with frontmatter on all
  five.
- Learned: the two hosts were never compared side by side. Each was checked
  against itself and both passed. Worth remembering for the next integration —
  parity is a different question from correctness.
- Confirmed: every command, flag and failure mode behaves as documented, and
  every host pointer resolves. `explain` on an unknown task and `migrate` with
  nothing to migrate both exit non-zero, which is intended and now written
  down.
- Chose: write the guide from the audit rather than from memory of the code, so
  nothing in it describes behaviour nobody observed. That is the same rule the
  project applies to evidence.
- Next: Phase 0 or Phase 3. Authority first.

## 2026-09-22 — T-DOI-01

- Did: added `.zenodo.json` and `CITATION.cff` so the archived deposit records
  what the project is rather than inferring it.
- Why it needed a release at all: archiving only deposits releases created
  after it was switched on. Everything up to 0.4.5 predates that and is not
  retroactively archived, which is worth knowing when reading the version
  history.
- Chose: organisation authorship, not a person. A personal name and an ORCID
  are the author's to give and were not confirmed, and a deposited record is a
  durable thing to get wrong. It is editable afterwards, and this is the part
  most worth revisiting deliberately — a DOI is usually wanted for personal
  academic credit, which an organisation name does not provide.
- Noticed: the version now appears in a third place. The README was already
  held to `VERSION` by a test after that drift shipped once; `CITATION.cff` got
  the same guard immediately rather than after it broke.
- Next: Phase 0 or Phase 3. Authority first.
