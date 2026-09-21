# Prokron Phase 0 --- Project Inception

## 0. Purpose

Phase 0 is the ingress layer into Prokron.

Its responsibility is to establish the first trustworthy canonical
project state regardless of how mature, documented, or structured the
project is when Prokron first encounters it.

A project may enter Prokron as:

``` text
A. IDEA INITIATION
   idea exists
   repository may not exist
   project documentation does not yet exist

B. GREENFIELD WITH DOCUMENTATION
   repository exists or is being created
   product/specification documents exist
   implementation is absent or minimal

C. BROWNFIELD WITH DOCUMENTATION
   active implementation exists
   documentation exists but may be fragmented,
   inconsistent, stale, duplicated, or incomplete

D. BROWNFIELD WITHOUT DOCUMENTATION
   active implementation exists
   useful project documentation is absent,
   minimal, or insufficient to explain intent
```

Phase 0 must not force these four situations through the same inference
process.

Instead, it must first determine the **inception mode**, then use the
appropriate evidence and human-interaction strategy to establish
canonical Prokron state.

The output of every mode is the same:

``` text
TRUSTWORTHY INITIAL PROJECT MODEL
                ↓
        HUMAN CONFIRMATION
                ↓
      CANONICAL PROKRON STATE
                ↓
           NORMAL LOOP
```

------------------------------------------------------------------------

## 1. Core Principle

Phase 0 exists to answer:

> **What project are we actually managing?**

before Prokron attempts to manage it.

The amount and type of evidence may vary radically.

Therefore:

``` text
NO EVIDENCE
    ≠
BAD EVIDENCE
    ≠
INCOMPLETE EVIDENCE
    ≠
CONFLICTING EVIDENCE
```

They require different treatment.

Phase 0 must never manufacture certainty merely to produce a
complete-looking project model.

------------------------------------------------------------------------

## 2. The Four Inception Modes

### Mode A --- IDEA INITIATION

#### Situation

The human has an idea but there is not yet a meaningful project
artifact.

Examples:

``` text
"I want to build an accounting system
for small B2B distributors."

"I have an idea for an AI tool that converts
domain documents into professional language learning."

"I need a lightweight system for PTs to
record client training through Telegram."
```

There may be:

``` text
no repository
no README
no product thesis
no architecture
no tasks
no phases
no implementation
```

This is not adoption.

It is **project formation**.

#### Objective

Transform human intent into an explicit, reviewable initial project
definition without pretending that exploratory ideas are already settled
requirements.

Preferred flow:

``` text
HUMAN IDEA
    ↓
INTENT ELICITATION
    ↓
PROBLEM FRAMING
    ↓
PRODUCT HYPOTHESIS
    ↓
SCOPE / CONSTRAINTS
    ↓
OPEN QUESTIONS
    ↓
CANDIDATE PROJECT MODEL
    ↓
HUMAN CONFIRMATION
    ↓
INITIAL CANONICAL STATE
```

The LLM may actively interview the human.

However, questioning should be **progressive**, not a fixed onboarding
questionnaire.

Ask only questions whose answers materially affect project structure.

#### Important distinction

Human statements during brainstorming may represent:

``` text
IDEA
HYPOTHESIS
PREFERENCE
CONSTRAINT
REQUIREMENT
DECISION
UNKNOWN
```

Do not automatically convert:

> "Maybe Telegram would work."

into:

``` text
DECISION:
Use Telegram.
```

Likewise:

> "Eventually this could support hospitals."

must not become an MVP requirement.

#### Expected initial outputs

Depending on project maturity:

``` text
Product context
Problem statement
Target user / actor
Core outcome
Initial scope
Explicit non-goals
Known constraints
Initial decisions
Open questions
Candidate phases
Candidate tasks
Candidate acceptance conditions
Initial intent
```

Do not force artificial completeness.

An idea-stage project may legitimately contain many unknowns.

------------------------------------------------------------------------

### Mode B --- GREENFIELD WITH DOCUMENTATION

#### Situation

The project has not meaningfully entered implementation, but useful
project documentation already exists.

Examples:

``` text
README.md
PRODUCT-THESIS.md
SPEC.md
architecture.md
MVP.md
research-notes.md
```

There may be scaffolding or prototypes, but the repository is primarily
**prospective** rather than historical.

#### Objective

Convert existing design intent into initial Prokron state while
preserving distinctions between:

``` text
decided
proposed
exploratory
required
optional
deferred
unknown
```

Preferred flow:

``` text
DOCUMENTS
    ↓
DISCOVER
    ↓
SEMANTIC EXTRACTION
    ↓
NORMALIZE
    ↓
IDENTIFY AUTHORITY
    ↓
BUILD CANDIDATE PROJECT MODEL
    ↓
SURFACE GAPS / CONFLICTS
    ↓
HUMAN CONFIRMATION
    ↓
CANONICAL STATE
```

#### Key characteristic

Unlike brownfield adoption, implementation reconciliation should be
lightweight.

Absence of implementation is expected.

For example:

``` text
SPEC:
Authentication is required.

CODE:
No authentication implementation exists.
```

This is not a conflict.

It is expected greenfield state.

Phase 0 should derive candidate implementation work where supported by
the specification.

#### Documentation rules

Filename and directory names are hints only.

A document may contain multiple semantic types:

``` text
requirements
decisions
constraints
tasks
future ideas
acceptance conditions
non-goals
```

Extract at fragment level.

Do not classify entire documents as one semantic type.

------------------------------------------------------------------------

### Mode C --- BROWNFIELD WITH DOCUMENTATION

#### Situation

The repository contains meaningful implementation and meaningful
documentation.

However, reality may look like:

``` text
README.md

docs/
  architecture.md
  architecture-v2.md
  roadmap-old.md
  product-thesis.md

notes/
  telegram.md
  september-review.md
  random-thoughts.md

handoff.md
TODO.md
TASKS-old.md

src/
migrations/
tests/
```

The documentation may be:

``` text
incomplete
duplicated
contradictory
superseded
informal
partially maintained
```

#### Objective

Perform **semantic archaeology**.

Preferred flow:

``` text
REPOSITORY
    ↓
EVIDENCE DISCOVERY
    ↓
SEMANTIC EXTRACTION
    ↓
PROVENANCE
    ↓
NORMALIZATION
    ↓
AUTHORITY REASONING
    ↓
TEMPORAL RECONCILIATION
    ↓
DOC ↔ IMPLEMENTATION RECONCILIATION
    ↓
CONFLICTS / UNKNOWNS
    ↓
CANDIDATE PROJECT MODEL
    ↓
ADOPTION REVIEW
    ↓
HUMAN CONFIRMATION
    ↓
CANONICAL STATE
```

This retains the major architecture of the original Project Adoption
specification.

#### Critical invariant

Always preserve:

``` text
RAW EVIDENCE
      ≠
EXTRACTED CLAIM
      ≠
DERIVED INTERPRETATION
      ≠
CANDIDATE STATE
      ≠
CANONICAL STATE
```

#### Documentation vs implementation

Implementation is evidence of **what exists**, not automatically
evidence of:

``` text
why it exists
whether it is correct
whether it is complete
whether it is accepted
whether it remains intended
```

Example:

``` text
Documentation:
T-020 TODO

Repository:
migration exists
service exists
tests exist
UI exists
```

Valid conclusion:

``` text
DOCUMENTED_STATUS: TODO
IMPLEMENTATION_EVIDENCE: PRESENT
INTERPRETATION: POSSIBLY_IMPLEMENTED
VALIDATION: REQUIRED
```

Not:

``` text
T-020 DONE
```

------------------------------------------------------------------------

### Mode D --- BROWNFIELD WITHOUT DOCUMENTATION

This is the most epistemically constrained mode.

#### Situation

There is substantial implementation but insufficient documentation to
explain the project.

The repository may contain:

``` text
src/
apps/
packages/
database/
migrations/
tests/
package.json
config/
CI workflows
```

but little beyond a generic or outdated README.

#### Objective

Reconstruct **observable current state** without fabricating product
intent or project history.

Preferred flow:

``` text
IMPLEMENTATION
      ↓
STRUCTURAL DISCOVERY
      ↓
OBSERVABLE CAPABILITIES
      ↓
IMPLEMENTATION EVIDENCE
      ↓
CANDIDATE CURRENT-STATE MODEL
      ↓
INTENT GAPS
      ↓
TARGETED HUMAN INTERVIEW
      ↓
RECONCILIATION
      ↓
CANDIDATE PROJECT MODEL
      ↓
HUMAN CONFIRMATION
      ↓
CANONICAL STATE
```

This mode must maintain a strict distinction between:

#### Observation

``` text
Supabase dependency exists.

There are 14 API routes.

Authentication middleware exists.

Three migrations define invoice-related tables.

Tests cover invoice creation.
```

#### Inference

``` text
The repository appears to contain
an invoice-management capability.
```

#### Unknown intent

``` text
Why Supabase was selected: UNKNOWN

Whether invoice management is MVP scope: UNKNOWN

Whether authentication implementation
matches intended requirements: UNKNOWN
```

The LLM must not reconstruct fictional rationale.

------------------------------------------------------------------------

## 3. Mode Detection

Phase 0 should begin with cheap inspection.

Conceptually:

``` text
                    START
                      │
                      ↓
             Repository exists?
                 /         \
               NO           YES
               │             │
          IDEA MODE      inspect repo
                             │
                  ┌──────────┴──────────┐
                  │                     │
          meaningful docs?       meaningful code?
                  │                     │
             YES / NO               YES / NO
```

Typical interpretation:

  Evidence                             Mode
  ------------------------------------ -------------------------
  Human idea only                      IDEA INITIATION
  Docs + little/no implementation      GREENFIELD WITH DOCS
  Docs + implementation                BROWNFIELD WITH DOCS
  Implementation + insufficient docs   BROWNFIELD WITHOUT DOCS

But mode detection is a **candidate classification**, not an
irreversible decision.

Hybrid projects exist.

If uncertain, ask one concise question.

------------------------------------------------------------------------

## 4. Unified Evidence Model

All modes should converge on the same evidence architecture.

Evidence may originate from:

``` text
HUMAN
DOCUMENT
NOTE
CODE
TEST
MIGRATION
CONFIG
COMMIT_METADATA
GENERATED_OBSERVATION
```

A conceptual fragment:

``` ts
interface EvidenceFragment {
  id: string

  source: {
    kind:
      | "HUMAN"
      | "DOCUMENT"
      | "NOTE"
      | "CODE"
      | "TEST"
      | "MIGRATION"
      | "CONFIG"
      | "COMMIT_METADATA"
      | "OTHER"

    path?: string
    range?: EvidenceRange
  }

  semanticType:
    | "PRODUCT"
    | "REQUIREMENT"
    | "TASK"
    | "STATUS_CLAIM"
    | "PHASE"
    | "DEPENDENCY"
    | "ACCEPTANCE"
    | "GATE"
    | "DECISION"
    | "CONSTRAINT"
    | "RISK"
    | "INTENT"
    | "HYPOTHESIS"
    | "IDEA"
    | "OBSERVATION"
    | "UNKNOWN"

  claim: string

  epistemicState:
    | "EXPLICIT"
    | "STRONGLY_DERIVED"
    | "WEAKLY_DERIVED"
    | "CONFLICTING"
    | "UNKNOWN"
}
```

The important addition is that **human conversation itself can be
evidence** in Idea Initiation.

But human brainstorming must still be semantically classified rather
than treated wholesale as canonical truth.

------------------------------------------------------------------------

## 5. Evidence Hierarchy Is Contextual

Do not create a universal ranking such as:

``` text
code > docs > notes > human
```

That is incorrect.

Different evidence answers different questions.

For example:

``` text
"What currently exists?"
→ implementation evidence may dominate.

"What should the product do?"
→ current product specification may dominate.

"Why was architecture X chosen?"
→ ADR or human confirmation may dominate.

"What is the current task?"
→ active intent/handoff may dominate.
```

Authority must therefore be resolved **per subject and claim**, not
globally per file.

------------------------------------------------------------------------

## 6. Candidate Project Model

Every inception mode should eventually construct:

``` text
CandidateProject
│
├── identity
├── product context
├── actors / users
├── capabilities
├── requirements
├── phases
├── tasks
├── dependencies
├── acceptance
├── gates
├── decisions
├── constraints
├── risks
├── current intent
├── implementation evidence
├── conflicts
├── unknowns
└── provenance
```

Not every field must be populated.

Missing information must remain missing.

------------------------------------------------------------------------

## 7. Different Modes Require Different Human Roles

Human interaction should change depending on inception mode.

### Idea Initiation

Human is primarily:

> **Source of intent**

LLM asks:

``` text
What problem are we solving?
For whom?
What outcome matters?
What constraints already exist?
What has actually been decided?
```

### Greenfield + Docs

Human is primarily:

> **Authority resolver**

LLM asks:

``` text
These two specifications disagree.
Which is current?

Is this item committed scope or exploratory?
```

### Brownfield + Docs

Human is primarily:

> **Reconciler**

LLM asks:

``` text
The roadmap says TODO but implementation exists.
Should this be validated as completed?

These architecture documents conflict.
Which represents current intent?
```

### Brownfield without Docs

Human is primarily:

> **Intent restorer**

LLM asks:

``` text
The repository appears to implement X.
Is X still intended?

I can observe Y but cannot determine why it exists.
What role does it play?

What is currently being worked on?
```

This avoids a generic onboarding questionnaire.

------------------------------------------------------------------------

## 8. Selective Human Confirmation

Across all modes:

> **Human verification of uncertainty, not manual transcription.**

Do not ask humans to approve every extracted fact.

Escalate when there is material uncertainty around:

``` text
project purpose
scope
authority
phase
task status
dependency
acceptance
decision
constraint
current intent
conflicting evidence
weakly derived entities
```

Batch explicit, uncontested evidence where safe.

------------------------------------------------------------------------

## 9. Idea Initiation Must Not Over-Architect

A special safety rule is required for Mode A.

An LLM can very easily turn:

> "I have an idea..."

into:

``` text
8 phases
74 tasks
microservice architecture
event bus
analytics
RBAC
CI/CD
observability
```

That would make Prokron an **overengineering generator**.

Therefore Idea Initiation must prefer:

``` text
problem clarity
    ↓
product hypothesis
    ↓
smallest meaningful scope
    ↓
critical constraints
    ↓
first validation milestone
    ↓
only enough tasks to begin
```

Do not extrapolate an entire product roadmap from thin intent.

------------------------------------------------------------------------

## 10. Brownfield Without Docs Must Not Invent History

Mode D has an equally important rule.

Never infer:

``` text
"We chose PostgreSQL because..."

"Phase 1 focused on..."

"The original architecture intended..."

"The team decided..."
```

from implementation structure alone.

Instead:

``` text
OBSERVED:
PostgreSQL is currently configured.

RATIONALE:
UNKNOWN.

HISTORY:
UNKNOWN.
```

Prokron chronology begins when trustworthy chronology becomes available.

------------------------------------------------------------------------

## 11. Canonicalization Boundary

No mode may directly write inferred state into canonical Prokron
records.

Always:

``` text
INPUT
  ↓
EVIDENCE
  ↓
INTERPRETATION
  ↓
CANDIDATE MODEL
  ↓
REVIEW
  ↓
HUMAN CONFIRMATION
  ↓
CANONICAL STATE
```

Never:

``` text
idea/docs/repo
      ↓
     LLM
      ↓
 canonical TASKS.md
```

without a reviewable boundary.

------------------------------------------------------------------------

## 12. Determinism Boundary

Phase 0 contains both deterministic and semantic components.

Do not require fresh LLM inference to be byte-identical.

Require deterministic behavior for:

``` text
evidence inventory
content fingerprinting
schema validation
stable identities
confirmed decisions
canonical compilation
persistence
generated deterministic views
```

LLM interpretation may vary.

Therefore:

> **LLM-derived candidate interpretation must be traceable, schema-valid
> and non-authoritative. Canonical state must be reproducible from
> accepted evidence and confirmed decisions.**

------------------------------------------------------------------------

## 13. Unified User Experience

The user should not need to understand the four modes before starting.

The top-level experience should remain simple:

``` bash
prokron init
```

Phase 0 inspects the available environment and responds appropriately.

### Idea

``` text
I don't see an established project yet.

Let's establish what you're building before
creating project state.
```

### Greenfield + docs

``` text
I found an early-stage project with substantial
product documentation and minimal implementation.

I can initialize Prokron from these sources.
```

### Brownfield + docs

``` text
I found an active project with both documentation
and implementation.

Some sources disagree. I will build an adoption
review before creating canonical state.
```

### Brownfield without docs

``` text
I found an active implementation but insufficient
documentation to establish project intent safely.

I can reconstruct observable current state, then
I'll need your input for the missing intent.
```

The user may override detected mode.

------------------------------------------------------------------------

## 14. Internal Pipelines

The four modes share components but not necessarily the same sequence.

``` text
IDEA INITIATION

human
  ↓
elicit
  ↓
structure
  ↓
candidate
  ↓
confirm
```

``` text
GREENFIELD + DOCS

discover
  ↓
extract
  ↓
normalize
  ↓
candidate
  ↓
confirm
```

``` text
BROWNFIELD + DOCS

discover
  ↓
extract
  ↓
normalize
  ↓
authority
  ↓
temporal reconciliation
  ↓
implementation reconciliation
  ↓
candidate
  ↓
confirm
```

``` text
BROWNFIELD - DOCS

discover implementation
  ↓
observe
  ↓
infer capabilities
  ↓
identify intent gaps
  ↓
human elicitation
  ↓
candidate
  ↓
confirm
```

Then all converge:

``` text
                 CANONICAL
                    │
                    ▼
             PHASE 1 — STATE
                    │
                    ▼
          PHASE 2 — MANAGEMENT
                    │
                    ▼
           PHASE 3 — EXECUTION
```

------------------------------------------------------------------------

## 15. Phase 0 Outputs

Phase 0 should produce only the artifacts necessary to establish and
audit initial state.

Conceptually:

``` text
prokron/
  inception/
    evidence.json
    candidate-project.json
    review.md
```

Additional conflict/provenance views may be derived rather than
persisted as separate sources of truth.

Avoid turning every internal representation into another Markdown file.

After confirmation, the accepted state populates normal canonical
Prokron records.

------------------------------------------------------------------------

## 16. Refresh Semantics

After initial inception, Prokron may rescan new evidence.

However, this is no longer "Phase 0 again" in the conceptual sense.

It is **state reconciliation** against an established canonical project.

A refresh may identify:

``` text
new evidence
new conflicts
new candidate tasks
documentation drift
implementation drift
possibly superseded decisions
```

It must not overwrite confirmed canonical decisions automatically.

------------------------------------------------------------------------

## 17. Acceptance Criteria

Phase 0 is successful when Prokron can correctly enter all four
situations.

### A. Idea Initiation

Given only a human idea, Prokron can establish:

``` text
what problem is being explored
who it is for
what outcome is intended
what is decided
what is hypothetical
what constraints exist
what remains unknown
what the smallest actionable next scope is
```

without fabricating requirements or over-architecting.

### B. Greenfield with Docs

Given product documentation and little implementation, Prokron can
establish:

``` text
product intent
requirements
decisions
constraints
phases
candidate tasks
acceptance
open questions
```

while distinguishing committed scope from proposals.

### C. Brownfield with Docs

Given implementation plus messy documentation, Prokron can establish:

``` text
current evidence
candidate authority
historical/superseded material
explicit tasks
derived tasks
implementation mismatches
conflicts
unknowns
current intent
```

with full provenance.

### D. Brownfield without Docs

Given implementation but insufficient documentation, Prokron can
establish:

``` text
observable architecture
observable capabilities
implementation evidence
likely but non-authoritative interpretations
missing product intent
missing historical rationale
questions requiring human input
```

without pretending implementation reveals undocumented intent.

------------------------------------------------------------------------

## 18. Non-Goals

Phase 0 does not:

``` text
implement the project
modify application code
clean up documentation automatically
delete stale documentation
invent missing history
invent acceptance criteria
invent product requirements
generate speculative backlog filler
orchestrate agents
route models
perform full program verification
become a semantic-search platform
become a Git intelligence platform
```

Its job ends when trustworthy initial canonical state exists.

------------------------------------------------------------------------

## 19. Critical Invariant

Across all four inception modes:

``` text
WHAT EXISTS
     ≠
WHAT WAS INTENDED
     ≠
WHAT IS CURRENTLY INTENDED
     ≠
WHAT PROKRON INFERS
     ≠
WHAT THE HUMAN CONFIRMS
```

Prokron must preserve these distinctions.

------------------------------------------------------------------------

## 20. Product Definition

Phase 0 changes the product relationship from:

``` text
"Prepare your project so Prokron can understand it."
```

to:

> **"Show Prokron what you have."**

That may be:

``` text
an idea
a specification
a messy repository
a mature undocumented codebase
```

Prokron's first responsibility is to determine **what is known, what is
inferred, what conflicts, and what still requires human judgment**.

Only then does project management begin.

------------------------------------------------------------------------

## Final Principle

The defining principle of Phase 0 is:

> **Prokron meets the project where it is.**

Architecturally:

``` text
IDEA ────────────────┐
                     │
GREENFIELD + DOCS ───┤
                     ├──▶ PHASE 0
BROWNFIELD + DOCS ───┤      │
                     │      ▼
BROWNFIELD - DOCS ───┘  TRUSTWORTHY
                       INITIAL STATE
                            │
                            ▼
                       PROKRON LOOP
```

Phase 0 is not merely an importer for legacy projects.

It is the **universal ingress layer of Prokron**.
