"""Deterministic project analytics.

Nothing here consults a model. Given the same compiled project, every function
returns the same answer, which is what makes a disagreement about project state
decidable rather than negotiable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import Obstacle, Project, Task


@dataclass
class Progress:
    done: int
    total: int

    @property
    def fraction(self) -> float:
        return self.done / self.total if self.total else 0.0

    def as_json(self) -> dict[str, float | int]:
        return {"done": self.done, "total": self.total, "fraction": round(self.fraction, 4)}

    def __str__(self) -> str:
        return f"{self.done} / {self.total}"


@dataclass
class Report:
    project: Project
    ready: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    wip: list[str] = field(default_factory=list)
    obstacles: list[Obstacle] = field(default_factory=list)
    critical_path: list[str] = field(default_factory=list)
    downstream: dict[str, list[str]] = field(default_factory=dict)
    phase_progress: dict[str, Progress] = field(default_factory=dict)
    scheduled: list[dict[str, str]] = field(default_factory=list)
    unscheduled: list[str] = field(default_factory=list)

    def metrics(self) -> dict[str, object]:
        tasks = self.project.tasks
        # Task completion counts every task. Excluding phase-independent work
        # made a project of nothing but chores report 0 / 0, which reads as
        # "nothing here" rather than "none of this belongs to a phase".
        # The phase split is already carried by phaseCompletion.
        counted = tasks
        in_phases = [t for t in tasks if not t.phase_independent]
        criteria = [
            criterion
            for contract in self.project.contracts.values()
            if not contract.is_global
            for criterion in contract.criteria
        ]
        validated = ("AI_REVIEWED", "HUMAN_VERIFIED")
        return {
            "taskCompletion": Progress(
                sum(1 for t in counted if t.done), len(counted)
            ).as_json(),
            "phaseCompletion": {
                phase_id: progress.as_json()
                for phase_id, progress in self.phase_progress.items()
            },
            "criticalPathCompletion": Progress(
                sum(1 for task_id in self.critical_path if self._done(task_id)),
                len(self.critical_path),
            ).as_json(),
            "validationCoverage": Progress(
                sum(1 for t in counted if t.validation in validated), len(counted)
            ).as_json(),
            "phaseIndependent": len(tasks) - len(in_phases),
            "gateReadiness": Progress(
                sum(1 for g in self.project.gates if g.status == "GREEN"),
                len(self.project.gates),
            ).as_json(),
            "acceptanceCompletion": Progress(
                sum(1 for c in criteria if c.state == "PASS"), len(criteria)
            ).as_json(),
            "validationBreakdown": _counts(t.validation for t in tasks),
            "statusBreakdown": _counts(t.status for t in tasks),
        }

    def _done(self, task_id: str) -> bool:
        task = self.project.task(task_id)
        return bool(task and task.done)


def _counts(values) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def unmet(project: Project, task: Task) -> list[str]:
    """Criteria that stand between this task and DONE."""
    return [
        criterion.id
        for criterion in project.mandatory_criteria(task)
        if criterion.state != "PASS"
    ]


def _dependency_blockers(project: Project, task: Task) -> list[str]:
    """Dependencies that are not done. An unknown dependency always blocks."""
    blockers = []
    for dependency in task.dependencies:
        known = project.task(dependency)
        if known is None or not known.done:
            blockers.append(dependency)
    return blockers


def _critical_path(project: Project) -> list[str]:
    """Longest chain of not-yet-done tasks, following dependencies forward.

    Ordering only. This says nothing about dates; see the schedule split.
    """
    open_tasks = {t.id: t for t in project.tasks if not t.done}
    memo: dict[str, list[str]] = {}

    def chain(task_id: str, seen: frozenset[str]) -> list[str]:
        if task_id in seen:
            return []
        if task_id in memo:
            return memo[task_id]
        best: list[str] = []
        for candidate in open_tasks.values():
            if task_id in candidate.dependencies:
                found = chain(candidate.id, seen | {task_id})
                if len(found) > len(best):
                    best = found
        result = [task_id, *best]
        if not seen:
            memo[task_id] = result
        return result

    longest: list[str] = []
    for task_id, task in open_tasks.items():
        if any(dependency in open_tasks for dependency in task.dependencies):
            continue  # start only from chains that can begin now
        found = chain(task_id, frozenset())
        if len(found) > len(longest):
            longest = found
    return longest


def report(project: Project) -> Report:
    result = Report(project=project)

    for task in project.tasks:
        for dependency in task.dependencies:
            result.downstream.setdefault(dependency, []).append(task.id)

    for task in project.tasks:
        if task.status == "WIP":
            result.wip.append(task.id)
        if task.done:
            continue
        blockers = _dependency_blockers(project, task)
        if blockers:
            result.blocked.append(task.id)
            result.obstacles.append(
                Obstacle(
                    type="DEPENDENCY_BLOCKER",
                    subject=task.id,
                    blockers=blockers,
                    detail=f"{task.id} waits on {', '.join(blockers)}",
                )
            )
        elif task.status == "TODO":
            # Ready means "can start now". Work already in flight is reported as
            # WIP; listing it as ready too would double-count it.
            result.ready.append(task.id)

        if task.status == "WIP":
            outstanding = unmet(project, task)
            if outstanding:
                result.obstacles.append(
                    Obstacle(
                        type="ACCEPTANCE_BLOCKER",
                        subject=task.id,
                        blockers=outstanding,
                        detail=(
                            f"{task.id} cannot complete while "
                            f"{len(outstanding)} criteria are unmet"
                        ),
                    )
                )

    for task in project.tasks:
        if task.done and task.validation == "UNTESTED":
            result.obstacles.append(
                Obstacle(
                    type="VALIDATION_GAP",
                    subject=task.id,
                    blockers=[],
                    detail=f"{task.id} is DONE but its validation strength is UNTESTED",
                )
            )

    for phase in project.phases:
        tasks = project.tasks_in(phase.id)
        result.phase_progress[phase.id] = Progress(
            sum(1 for task in tasks if task.done), len(tasks)
        )
        if phase.status in {"ACTIVE", "EXIT_PENDING"}:
            red = [gate.id for gate in project.gates if _blocks(gate, phase.id)]
            unfinished = [task.id for task in tasks if not task.done]
            if red:
                result.obstacles.append(
                    Obstacle(
                        type="GATE_BLOCKER",
                        subject=phase.id,
                        blockers=red,
                        detail=(
                            f"{phase.id} cannot exit while {', '.join(red)} "
                            f"{'is' if len(red) == 1 else 'are'} red"
                        ),
                    )
                )
            if unfinished:
                result.obstacles.append(
                    Obstacle(
                        type="PHASE_BLOCKER",
                        subject=phase.id,
                        blockers=unfinished,
                        detail=(
                            f"{phase.id} has {len(unfinished)} unfinished "
                            f"task{'s' if len(unfinished) != 1 else ''}"
                        ),
                    )
                )

    for task in project.tasks:
        if task.done:
            continue
        if task.schedule.known:
            result.scheduled.append(
                {
                    "id": task.id,
                    **{k: v for k, v in vars(task.schedule).items() if v},
                }
            )
        else:
            result.unscheduled.append(task.id)
            if task.schedule.start or task.schedule.estimate:
                result.obstacles.append(
                    Obstacle(
                        type="SCHEDULE_BLOCKER",
                        subject=task.id,
                        blockers=[],
                        detail=(
                            f"{task.id} has partial schedule metadata; a calendar "
                            "bar needs a start plus an estimate or end"
                        ),
                    )
                )

    result.critical_path = _critical_path(project)
    result.ready.sort()
    result.blocked.sort()
    return result


def _blocks(gate, phase_id: str) -> bool:
    """A gate blocks a phase when its Blocks entry names that phase exactly.

    Substring matching is wrong here: a gate blocking `P11 exit` would
    otherwise also block `P1`.
    """
    if gate.status == "GREEN":
        return False
    return any(entry.split()[:1] == [phase_id] for entry in gate.blocks if entry.split())


def explain(project: Project, task_id: str) -> dict[str, object]:
    """Everything decidable about one task, with no model in the loop."""
    task = project.task(task_id)
    if task is None:
        raise KeyError(task_id)
    result = report(project)
    contract = project.contracts.get(task.contract or "")
    return {
        "id": task.id,
        "title": task.title,
        "phase": task.phase,
        "status": task.status,
        "validation": task.validation,
        "owner": task.owner,
        "dependencies": [
            {
                "id": dependency,
                "done": bool(
                    project.task(dependency) and project.task(dependency).done
                ),
            }
            for dependency in task.dependencies
        ],
        "blocks": result.downstream.get(task.id, []),
        "acceptance": [
            {"id": c.id, "state": c.state, "class": c.evidence_class, "text": c.text}
            for c in (contract.criteria if contract else [])
        ],
        "invariants": [c.id for c in project.invariants_for(task)],
        "blockers": [o.as_json() for o in result.obstacles if o.subject == task.id],
        "evidence": task.evidence,
        "decisions": task.decisions,
        "schedule": task.schedule.as_json(),
        "source": task.source.as_json(),
    }


def _relevant(narrative: str, task_id: str) -> str | None:
    """Return project narrative only when it actually concerns this task.

    `INTENT.md` and `HANDOFF.md` describe whatever is in flight, which is
    usually something else. Pasting them into every packet hands the reader
    statements that contradict the task it was given, and a cold agent cannot
    tell which to believe. Silence is better than a confident irrelevance.
    """
    return narrative if narrative and task_id in narrative else None


def context(project: Project, task_id: str, role: str = "builder") -> dict[str, object]:
    """The minimal packet an agent needs to start work on one task."""
    task = project.task(task_id)
    if task is None:
        raise KeyError(task_id)
    contract = project.contracts.get(task.contract or "")
    phase = project.phase(task.phase)
    report_now = report(project)
    blockers = [o.as_json() for o in report_now.obstacles if o.subject == task_id]
    packet: dict[str, object] = {
        "role": role,
        "packetFor": task_id,
        "intent": _relevant(project.intent, task_id),
        "phase": (
            {"id": phase.id, "outcome": phase.outcome, "status": phase.status}
            if phase
            else {"id": task.phase}
        ),
        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "validation": task.validation,
            "dependencies": [
                {
                    "id": dependency,
                    "done": bool(
                        project.task(dependency) and project.task(dependency).done
                    ),
                }
                for dependency in task.dependencies
            ],
            "closed": task.done,
        },
        "blockers": blockers,
        "acceptance": [
            {"id": c.id, "text": c.text, "class": c.evidence_class, "state": c.state}
            for c in (contract.criteria if contract else [])
        ],
        "invariants": [
            {"id": inherited.id, "criteria": [c.text for c in inherited.criteria]}
            for inherited in project.invariants_for(task)
        ],
        "decisions": [
            {"id": d.id, "title": d.title, "origin": d.origin}
            for d in project.decisions
            if d.id in task.decisions
        ],
        "evidence": task.evidence,
        "handoff": _relevant(project.handoff, task_id),
    }
    if task.done:
        packet["note"] = (
            f"{task.id} is already DONE. This packet is for review or audit, "
            "not for fresh implementation."
        )
    if role == "reviewer":
        packet["findingClasses"] = {
            "blocking": [
                "ACCEPTANCE_FAILURE",
                "INVARIANT_VIOLATION",
                "REGRESSION",
                "MISSING_EVIDENCE",
            ],
            "informative": [
                "RISK",
                "MAINTAINABILITY",
                "ARCHITECTURE_PREFERENCE",
                "STYLE",
                "FUTURE_IMPROVEMENT",
            ],
        }
    return packet
