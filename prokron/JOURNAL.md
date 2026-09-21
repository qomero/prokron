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
