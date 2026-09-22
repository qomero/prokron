# Contributing to Prokron

Prokron tracks its own development with Prokron. Contributing here means using
the thing you are changing, which is the fastest way to find out whether it
works.

## Before anything else

Run it:

```sh
git clone https://github.com/qomero/prokron.git
cd prokron
.prokron/prokron status
.prokron/prokron dashboard && open .prokron/compiled/dashboard.html
```

That is the whole project's state, computed from the Markdown in
`.prokron/chronicle/`. If something there is wrong or unclear, that is already
worth an issue.

## The shape of a change

Every change follows the same four steps, and they are the same steps the
installed workflow asks of an agent.

**1. A task exists before the work does.** Add it to
`.prokron/chronicle/TASKS.md` with a phase — or `P-NONE` for repository chores —
its dependencies, and a reference to its contract.

**2. A contract says what done means.** Add it to
`.prokron/chronicle/ACCEPTANCE.md` before you start. Each criterion is written
as Given / When / Then, carries one evidence class (`TEST`, `MUTATION`,
`INSPECTION`, `RUNTIME`, `MANUAL`), and starts at `NOT_RUN`.

The contract freezes when the task becomes `WIP`. If a criterion turns out to
be wrong, raise an Acceptance Change Request in the same file. Do not quietly
reword it to match what you built — that is the single failure this project
exists to prevent.

**3. A decision that is material gets an ADR.** Append it to
`.prokron/chronicle/ADR/`, numbered in sequence, and link the tasks it affects.
Changing your mind later means a new ADR that supersedes the old one. Never
edit an accepted ADR to change what it says.

**4. Evidence, then `DONE`.** Record what you actually ran and what it showed,
against the criterion it satisfies. `DONE` means every mandatory criterion has
evidence — not that the code looks finished.

Then:

```sh
.prokron/prokron validate
.prokron/prokron compile && .prokron/prokron graph && .prokron/prokron dashboard
python3 -m unittest discover -s tests
sh tests/install.sh
```

Commit the regenerated `.prokron/compiled/` with your change. CI deletes that
directory, rebuilds it, and fails if the result differs from what you committed,
so a stale or hand-edited file is caught before review.

## What CI checks

| Job | What it proves |
|---|---|
| tests | The unit and installer suites pass on Linux and macOS, across supported Python versions |
| invariants | The chronicle validates, and compiled output regenerates byte for byte |
| no network, no dependencies | The runtime imports nothing outside the standard library |

The supported Python floor is whatever the matrix proves, not what this file
claims.

## House rules

- **Standard library only.** No dependencies, no build step, no package to
  install. ADR-016. If a change needs a library, it probably belongs outside the
  runtime.
- **Deterministic.** The same authored documents produce the same output every
  time. No model provider, no network, no wall-clock in a computed value.
- **Authority is `.prokron/chronicle/`.** `.prokron/compiled/` is generated and
  disposable. Never hand-edit it, and never let a generated view decide a
  question an authored document answers.
- **Do not invent facts.** A duration only when someone recorded one, a date
  only when someone set one, `UNKNOWN` the rest of the time.
- **Records are append-only where it matters.** Journal entries and ADRs stay.
  Intent and handoff describe the present and are overwritten.

## Disagreement

Reviewers and contributors will disagree. This project resolves it by a stated
order rather than by seniority, highest first:

```text
1. Product and domain authority
2. The explicit acceptance contract
3. Invariants
4. Accepted decisions in .prokron/chronicle/ADR/
5. Reproducible tests and evidence
6. Existing code convention
7. Reviewer preference
```

A reviewer's preference is not an acceptance criterion. A reviewer who believes
the contract is wrong raises an Acceptance Change Request.

Findings that block completion: `ACCEPTANCE_FAILURE`, `INVARIANT_VIOLATION`,
`REGRESSION`, `MISSING_EVIDENCE`. Findings that are recorded and do not block:
`RISK`, `MAINTAINABILITY`, `ARCHITECTURE_PREFERENCE`, `STYLE`,
`FUTURE_IMPROVEMENT`.

## Reporting a gap rather than fixing one

The most useful reports are about an agent or a person failing to understand a
project from its chronicle. Open a **chronicle gap** issue with the host and
model, the request you made, what was recorded, and what could not be
understood from it. Remove private project details first.

The [continuity pilot](docs/SPEC.md#handoff-pilot) is the procedure; the last
run is in [`docs/pilot-2026-09-22.md`](docs/pilot-2026-09-22.md). Running it
against a host we have not tried is a genuine contribution on its own.

## Documentation

The README, [`docs/GUIDE.md`](docs/GUIDE.md), [`docs/SPEC.md`](docs/SPEC.md)
and [`docs/PRODUCT-THESIS.md`](docs/PRODUCT-THESIS.md) are the published set, and
tests hold them to their own facts: every relative link resolves, no `rm -rf`
names anything but the compiled directory, and the release the README cites
matches `VERSION`.

Phase specifications are internal working documents and are not published
(ADR-026). Keep anything not yet built described as not yet built.

## Scope

Prokron owns project understanding, not project execution. It schedules
nothing, assigns nothing and runs nothing. A change that would decide what
happens next on its own does not belong here; a change that helps a participant
understand what is already true might.
