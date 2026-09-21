# Prokron Phase 3 — Execution Intelligence

You are continuing development of **Prokron**.

Phase 1 established the project-state / chronicle foundation.

Phase 2 established the compiled project-management layer:

* canonical task state
* dependency graph
* phase state
* acceptance state
* validation state
* gates
* blockers
* ready tasks
* critical path
* Mermaid views
* offline HTML project dashboard
* schedule-awareness without inventing dates or durations

The current generated dashboard already answers:

* What exists?
* What is done?
* What is unfinished?
* What is ready?
* What is blocked?
* What depends on what?
* What phase are we in?
* Which gates are passing/failing?
* What is the dependency critical path?
* What validation strength exists?
* What schedule data actually exists?

Phase 3 must answer the next layer:

> **Given the current canonical project state, what should happen next, why, and what will that action unlock or reduce?**

This phase is **Execution Intelligence**.

---

# 1. Core principle

Do NOT turn Prokron into an autonomous project manager.

Prokron must remain:

> deterministic facts first, explicit reasoning second, human/agent decision last.

The system may derive structural recommendations from project state.

It must NOT invent:

* business priorities
* missing requirements
* task durations
* deadlines
* effort estimates
* developer availability
* task complexity
* agent capabilities
* risk severity
* urgency
* schedule dates
* undocumented dependencies

unless those facts are explicitly represented in authoritative project metadata.

When evidence is absent, return `UNKNOWN`, `UNSPECIFIED`, or omit the claim.

Never silently convert an inference into a project fact.

---

# 2. Objective

Build an execution-planning layer over the canonical Prokron state.

It should derive:

1. recommended next tasks
2. why each task is recommended
3. downstream unlock impact
4. critical-path relevance
5. gate relevance
6. blocker-removal impact
7. parallel-safe workstreams
8. validation requirements
9. execution risk signals
10. agent/model suitability **only when policy metadata exists**
11. changes since the previous compiled state
12. active intent / execution context when available
13. decisions relevant to the recommended work
14. unresolved questions that prevent confident execution

The output must be useful both to:

* a human project owner
* a newly started coding agent with no session history

---

# 3. Architectural constraint

Do NOT build another heuristic inference engine that tries to understand the project from filenames, naming conventions, or guessed semantics.

Phase 3 operates on the **already-normalized Prokron canonical state**.

Preferred architecture:

```text
project sources
    ↓
Prokron ingest / compiler
    ↓
canonical project state
    ↓
dependency + acceptance + validation analysis
    ↓
execution intelligence
    ↓
execution packet
    ├── human dashboard
    ├── agent handoff
    └── machine-readable JSON
```

Structural conclusions should be deterministic whenever possible.

LLM interpretation, if used, must sit on top of the deterministic evidence layer and must never mutate canonical facts.

---

# 4. Introduce an Execution Intelligence model

Create a machine-readable representation, conceptually similar to:

```ts
interface ExecutionRecommendation {
  taskId: string;

  reasons: ExecutionReason[];

  dependencyImpact: {
    directlyUnlocks: string[];
    downstreamUnlockCount: number;
  };

  criticalPath: {
    onCriticalPath: boolean;
    position?: number;
  };

  gateImpact: {
    gates: string[];
  };

  blockerImpact: {
    resolvesFor: string[];
  };

  validation: {
    currentStrength?: ValidationStrength;
    requiredStrength?: ValidationStrength;
    missing?: string[];
  };

  parallelism: {
    parallelSafeWith: string[];
    conflictsWith?: string[];
  };

  evidence: EvidenceReference[];

  confidence: "FACT" | "DERIVED" | "UNKNOWN";
}
```

Exact schema names may differ if the repository conventions suggest better names.

Do not add fields whose values cannot be supported by project state.

---

# 5. Recommendation engine

Build a deterministic candidate ranking system.

Important:

This is NOT a generic numerical productivity score.

Avoid meaningless composite scores such as:

```text
priority = blockers * 5 + criticalPath * 8 + gates * 3
```

unless such weighting is explicitly configurable and visible to the user.

Prefer explainable ordering based on rules.

Suggested ordering hierarchy:

### A. Explicit project priority

If authoritative project metadata explicitly marks something as:

* urgent
* priority
* milestone-critical
* required next
* human-selected

that wins.

### B. Critical path

Ready tasks on the current critical path should be surfaced prominently.

### C. Gate unblockers

Ready tasks required to turn a currently failing phase gate into passing state should be surfaced.

### D. High dependency unlock

Ready tasks that unlock substantial blocked branches should be identified.

Do not equate unlock count with business importance.

Expose the number as evidence rather than pretending it is an objective priority score.

### E. Phase relevance

Prefer work belonging to the current active phase unless:

* another task is explicitly authorized cross-phase work, or
* it is a prerequisite of the active phase.

### F. Parallel-safe work

Identify independent ready branches that can be executed concurrently.

Example:

```text
Recommended parallel batch

Lane A
T-070
→ finance dependency chain

Lane B
T-020
→ assessment dependency chain

Lane C
T-007
→ service-role / Telegram tenancy prerequisite
```

Only mark tasks parallel-safe when the dependency graph actually supports that conclusion.

---

# 6. Explain every recommendation

Never produce:

```text
Recommended: T-070
```

Produce:

```text
T-070 — payment_schedules schema + use-cases

Why now
- READY
- first unresolved node on the current critical path
- required by T-071 and T-072

Direct unlocks
- T-071
- T-072

Downstream dependency reach
- N unresolved tasks

Gate relevance
- contributes toward ...

Validation
- current: UNTESTED
- required: ...

Evidence
- task graph
- acceptance entry
- relevant project source references
```

A new agent should be able to understand *why* without reopening the entire project history.

---

# 7. Add "Next Execution" to the dashboard

Add a high-value section near the top of the generated project dashboard:

```text
NEXT EXECUTION
```

Suggested contents:

### Recommended next

Top structurally relevant ready tasks.

### Parallel lanes

Tasks that can proceed concurrently without dependency conflict.

### Critical-path entry

First unresolved executable node on the current critical path.

### Gate unblockers

Ready tasks contributing directly to failing gates.

### High-leverage unlockers

Tasks with meaningful downstream dependency reach.

Do not overload the dashboard.

The purpose is to answer:

> "I just opened this project. What can I responsibly work on now?"

within seconds.

---

# 8. Add "Why this task?" drill-down

Clicking a recommended task should expose its execution reasoning.

Example:

```text
T-020

Status
READY

Why surfaced
- current phase P1
- 7 unresolved descendants
- starts assessment branch

Direct dependents
T-021
T-022
T-024

Affected gate
Gate B — Structured assessments

Parallel-safe with
T-007
T-070
T-080
...

Evidence
...
```

Do not display unsupported claims such as:

* "easy"
* "high risk"
* "should take 2 hours"
* "best task for Claude"

unless corresponding metadata exists.

---

# 9. Change Intelligence

Phase 3 must introduce state-diff capability.

Given two compiled Prokron snapshots, derive:

```text
WHAT CHANGED SINCE LAST STATE
```

At minimum detect:

* task created
* task removed
* status changed
* task became READY
* task became BLOCKED
* dependency added
* dependency removed
* acceptance changed
* validation changed
* gate state changed
* phase state changed
* critical path changed
* blocker introduced
* blocker resolved

Produce both:

```text
machine-readable diff
```

and concise human output.

Example:

```text
Since previous compile

+ T-070 became READY
+ Gate C changed RED → GREEN
+ T-072 now blocked only by T-070
- blocker on T-059 resolved

Critical path changed:
old: ...
new: ...
```

Do not treat regenerated formatting differences as project changes.

---

# 10. Intent integration

Prokron already exists in an environment where agents may use `intent.md` / execution intent.

Phase 3 should support intent as first-class execution context **if present**.

Intent represents:

> what the current worker intends to change during the active unit of work.

Do NOT treat intent as authoritative project state.

Model it separately:

```text
canonical project state
≠
execution intent
```

Possible state:

```ts
interface ExecutionIntent {
  actor?: string;
  targetTasks?: string[];
  objective: string;
  status?: "PLANNED" | "ACTIVE" | "PAUSED" | "COMPLETED";
  startedAt?: string;
  notes?: string[];
}
```

If intent exists, the dashboard should show:

```text
CURRENT INTENT
```

and reconcile it with canonical task state.

Detect situations such as:

```text
intent targets blocked task
intent references completed task
intent references unknown task
intent has no active target
```

Do not auto-correct intent.

Report the inconsistency.

---

# 11. Decision context

If the repository has ADRs, decision logs, chronicle decisions, or equivalent authoritative records, link relevant decisions to recommendations.

Example:

```text
T-095
Relevant decision:
ADR-018 — Whisper default STT provider
```

Do not summarize arbitrary old discussions.

Only surface decisions materially related to the task.

---

# 12. Execution Packet

Create a compact machine/human-readable output designed for a fresh agent session.

Suggested generated artifact:

```text
prokron/generated/execution.md
```

and preferably:

```text
prokron/generated/execution.json
```

The packet should include:

```text
Project
Current phase

Current project state
- completion
- acceptance
- validation
- gate readiness

Current intent
(if present)

Recommended next work

Parallel-safe lanes

Critical-path entry

Relevant blockers

Recently changed state

Relevant decisions

Validation requirements

Open questions / unknowns
```

This should allow a new coding agent to start useful work without loading the entire project documentation corpus.

However:

The execution packet is a **navigation/context artifact**, not a replacement for authoritative specifications.

Explicitly point the agent to authoritative source files needed for the selected task.

---

# 13. Agent/model routing — metadata only

We may later use multiple coding agents/models in parallel.

Build support for execution profiles, but do NOT hard-code assumptions such as:

```text
Terra = cheap builder
Sol = fixer
Opus = auditor
Astra = escalation
```

Instead support optional project configuration such as:

```yaml
execution_profiles:
  builder:
    preferred_agents:
      - terra
  security_sensitive:
    preferred_agents:
      - sol
    review_required: true
  audit:
    preferred_agents:
      - opus
```

Tasks may optionally declare:

```yaml
execution:
  profile: security_sensitive
```

If no execution metadata exists:

```text
Suggested agent: UNSPECIFIED
```

Do not infer agent quality from task names.

---

# 14. Human overrides

Execution intelligence must remain overridable.

Support explicit human decisions such as:

```text
focus task T-020
defer T-070
pause branch finance
prefer assessment branch
```

Human overrides should be represented explicitly and visibly.

They must not rewrite dependency truth.

Example:

```text
T-070
READY
critical path
HUMAN-DEFERRED
```

is valid.

Do not convert it to BLOCKED.

---

# 15. Separate these concepts rigorously

Do not collapse:

```text
READY
RECOMMENDED
PRIORITIZED
ACTIVE
WIP
BLOCKED
DEFERRED
```

Definitions:

### READY

All required dependencies are satisfied.

### RECOMMENDED

Execution intelligence surfaces the task based on current structural evidence.

### PRIORITIZED

Explicit project/human metadata says it has priority.

### ACTIVE / WIP

Someone is actually working on it.

### BLOCKED

A required condition prevents execution.

### DEFERRED

Human/project policy intentionally chooses not to execute it now.

A READY task may be DEFERRED.

A READY task may not be RECOMMENDED.

A RECOMMENDED task is not automatically WIP.

---

# 16. Risk intelligence

Only derive objective structural risk signals.

Allowed examples:

```text
- task lies on current critical path
- task blocks N unresolved tasks
- task affects RED gate
- task has no validation
- acceptance criteria missing
- unresolved dependency reference
- task references unknown artifact
- intent and task state disagree
```

Do NOT invent subjective labels such as:

```text
high technical risk
complex implementation
likely difficult
```

unless explicitly recorded.

Prefer:

```text
Risk signals:
- critical-path node
- UNTESTED
- 12 unresolved downstream dependents
```

over:

```text
Risk: HIGH
```

---

# 17. Open questions

Generate actionable questions only where missing information prevents responsible execution.

Examples:

```text
T-070 has no acceptance criteria.
Human confirmation required before implementation.

T-080 has conflicting dependency declarations.
Resolve TASKS vs phase specification.

Current intent targets T-091, but T-091 is dependency-blocked.
```

Do not generate generic PM questions just to fill a section.

---

# 18. CLI

Expose a coherent CLI consistent with existing Prokron conventions.

Exact command naming should follow the repository's current style.

Capabilities should include equivalents of:

```bash
prokron execution
prokron next
prokron diff
prokron dashboard
```

Possible examples:

```bash
prokron next
```

prints:

```text
Recommended next

1. T-070
   critical-path entry
   directly unlocks T-071, T-072

2. T-020
   opens assessment branch
   directly unlocks T-021, T-022, T-024

Parallel-safe:
T-070 + T-020 + T-007
```

And:

```bash
prokron execution --json
```

returns structured output suitable for another agent.

Do not introduce duplicate commands if existing CLI architecture already provides equivalent entry points.

Inspect first.

---

# 19. Dashboard evolution

Extend the existing Phase 2 dashboard rather than rewriting it.

Preserve:

* offline usability
* light/dark mode
* deterministic project metrics
* Mermaid views
* existing task drilldown
* no fake scheduling

Add:

```text
Current Intent
Next Execution
Parallel Work
Recent Changes
Execution Risks
Open Questions
```

Only include sections when relevant.

Avoid visual noise.

The dashboard should remain a control surface, not become Jira.

---

# 20. Provenance

Execution recommendations must be explainable.

Where practical, retain provenance pointing to:

* canonical task entry
* dependency edge
* acceptance record
* validation record
* gate definition
* phase definition
* intent
* decision / ADR

A recommendation without explainable evidence is not acceptable.

---

# 21. Determinism

Given identical canonical project state and configuration:

```text
execution.json
```

must be identical.

Do not use:

* current wall-clock time
* random ordering
* LLM-generated ranking
* environmental nondeterminism

to determine structural recommendations.

LLM-generated explanatory prose may exist as an optional presentation layer, but it must not influence canonical execution output.

---

# 22. Tests

Add meaningful tests for at least:

### Recommendation

* ready critical-path node surfaced
* blocked task never recommended as executable
* explicit human priority respected
* deferred task remains READY but not execution-selected
* direct unlocks correct
* downstream reach correct

### Parallelism

* independent tasks identified as parallel-safe
* dependency-linked tasks not marked parallel-safe

### Gates

* gate unblocker detected
* unrelated task not labeled gate-relevant

### Diff

* TODO → DONE
* BLOCKED → READY
* dependency added
* dependency removed
* gate RED → GREEN
* critical path changed
* no semantic changes produces empty diff

### Intent

* valid active intent
* intent targeting blocked task
* intent referencing unknown task
* paused intent

### Integrity

* no task duration inferred
* no schedule inferred
* no agent assignment inferred without metadata
* deterministic output across repeated runs

---

# 23. Acceptance criteria

Phase 3 is complete when a fresh agent can open the generated execution output and answer all of these without reconstructing the project graph manually:

1. What phase is active?
2. What work is executable now?
3. Which tasks are most structurally relevant to execute next?
4. Why were they surfaced?
5. What does each one directly unlock?
6. Which ready tasks can run in parallel?
7. What is the first unresolved executable critical-path node?
8. Which tasks can help resolve failing gates?
9. What changed since the previous project state?
10. Is there an active execution intent?
11. Does that intent conflict with canonical project state?
12. Which decisions are relevant to the intended work?
13. What validation is still required?
14. What information is genuinely unknown?
15. Which authoritative documents should the agent read before implementation?

And all answers must be traceable to project evidence.

---

# 24. Non-goals

Do NOT build in Phase 3:

* autonomous task execution
* multi-agent orchestration runtime
* token routing
* model API integrations
* agent spawning
* worktree management
* automatic commits
* automatic PRs
* arbitrary LLM project planning
* estimated completion dates
* inferred task durations
* developer productivity scoring
* Jira/Linear replacement
* chat interface
* vector database
* semantic repo search engine

Those may be future phases.

Phase 3 is the **reasoning/control layer between project state and execution**, not the execution runtime itself.

---

# 25. Implementation approach

Before modifying code:

1. inspect the existing Prokron architecture
2. identify the Phase 2 compiler/state/dashboard boundaries
3. identify authoritative schemas
4. identify current CLI conventions
5. identify existing tests
6. identify whether snapshots/history already exist
7. identify current intent/decision formats if present

Then write a concise implementation plan.

Prefer extending existing abstractions over creating parallel subsystems.

Do not rewrite stable Phase 1/2 functionality unless required.

After implementation:

1. run the full existing test suite
2. run new Phase 3 tests
3. compile Prokron against the current AuxVol project
4. generate the dashboard
5. generate execution JSON/Markdown
6. verify recommendations manually against the actual dependency graph
7. verify repeated runs are deterministic
8. report any unsupported assumptions instead of hiding them

---

# 26. Example target output

For the current AuxVol state, output may conceptually look like:

```text
NEXT EXECUTION

Critical-path entry
T-070 — payment_schedules schema + use-cases
Why:
- READY
- first unresolved executable node on current critical path
Direct unlock:
- T-071
- T-072

Parallel branch
T-020 — client_assessments
Why:
- READY
- opens unresolved assessment branch
Direct unlock:
- T-021
- T-022
- T-024

Infrastructure
T-007 — withTrainer() service-role wrapper
Why:
- READY
- required by T-091
- tenancy/security boundary

PARALLEL-SAFE SET
T-070
T-020
T-007

FAILING GATES
Gate A
Gate B
Gate E

RECENT CHANGES
...

CURRENT INTENT
...

OPEN QUESTIONS
...
```

This is illustrative only.

The implementation must derive the actual result from canonical project state rather than hard-coding this example.

---

# Final requirement

The core product idea of Phase 3 is:

> **Prokron should not merely tell an agent what the project looks like. It should give the agent a defensible starting point for the next unit of work.**

But every recommendation must preserve the distinction between:

```text
project fact
derived structural conclusion
human decision
agent intent
unknown information
```

That separation is non-negotiable.

Build Phase 3 accordingly.
