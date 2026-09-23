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
    # Execution impact of operations work: execution task -> the open
    # operations tasks it waits on. The operations task keeps its domain.
    external_blockers: dict[str, list[str]] = field(default_factory=dict)
    in_flight: list[str] = field(default_factory=list)
    main_blocker: dict[str, object] | None = None
    next_gate: dict[str, object] | None = None
    execution_failures: list[dict[str, object]] = field(default_factory=list)

    def _criteria(self, tasks: list[Task]) -> list:
        referenced = {t.contract for t in tasks if t.contract}
        return [
            criterion
            for contract in self.project.contracts.values()
            if not contract.is_global and contract.id in referenced
            for criterion in contract.criteria
        ]

    def metrics(self) -> dict[str, object]:
        # Progress is execution progress (ADR-045). Operations work is counted
        # separately in operations_metrics and never moves these figures.
        tasks = self.project.execution_tasks
        # Phase-independent execution still counts: excluding it made a project
        # of nothing but unphased work report 0 / 0.
        counted = tasks
        in_phases = [t for t in tasks if not t.phase_independent]
        criteria = self._criteria(tasks)
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
            "domainBreakdown": {
                "execution": len(tasks),
                "operations": len(self.project.operations_tasks),
            },
        }

    def operations_metrics(self) -> dict[str, object]:
        """Operational state and evidence. None of it is project progress."""
        operations = self.project.operations_tasks
        events = self.project.events
        blocked = set(self.blocked)
        affecting = sorted({o for blockers in self.external_blockers.values() for o in blockers})
        on_path = set(self.critical_path)
        return {
            "tasks": {
                "total": len(operations),
                "done": sum(1 for t in operations if t.done),
                "active": sum(1 for t in operations if t.status == "WIP"),
                "blocked": sum(1 for t in operations if t.id in blocked),
                "open": sum(1 for t in operations if not t.done),
            },
            "acceptance": Progress(
                sum(1 for c in self._criteria(operations) if c.state == "PASS"),
                len(self._criteria(operations)),
            ).as_json(),
            "events": {
                "total": len(events),
                "byType": _counts(e.type for e in events),
                "failures": sum(1 for e in events if e.failed),
                "unresolvedFailures": len(unresolved_failures(self.project)),
                "retries": sum(1 for e in events if e.retry_of or e.type == "retry"),
                "mutations": sum(1 for e in events if e.type == "mutation"),
            },
            "affectingExecution": affecting,
            "affectingCriticalPath": sorted({
                o for task, blockers in self.external_blockers.items()
                if task in on_path for o in blockers
            }),
            "affectingGate": sorted(
                {b["id"] for b in (self.next_gate or {}).get("externalBlockers", [])}
            ),
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
    """Longest chain of not-yet-done execution tasks, following dependencies forward.

    Ordering only. This says nothing about dates; see the schedule split.
    """
    # The critical path runs through execution only. An operations task that
    # holds up a node is reported as that node's external blocker instead.
    open_tasks = {t.id: t for t in project.execution_tasks if not t.done}
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
                    domain=task.domain,
                )
            )
            if task.execution:
                external = [
                    b for b in blockers
                    if project.task(b) is not None and not project.task(b).execution
                ]
                if external:
                    result.external_blockers[task.id] = external
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
                        domain=task.domain,
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
                    domain=task.domain,
                )
            )

    for phase in project.phases:
        # A phase's progress is its execution work only. Operations tasks that
        # name the phase are associated with it but never counted (ADR-045).
        tasks = project.execution_in(phase.id)
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
                        domain=task.domain,
                    )
                )

    result.critical_path = _critical_path(project)
    result.ready.sort()
    result.blocked.sort()
    result.in_flight = _in_flight(project, result)
    result.next_gate = _next_gate(project, result)
    result.main_blocker = _main_blocker(project, result)
    result.execution_failures = _execution_failures(project)
    return result


def events_for(project: Project, task_id: str) -> list[str]:
    """Trace events that originate in, or name, this task."""
    return [e.id for e in project.events if e.task == task_id or task_id in e.affects]


def unresolved_failures(project: Project) -> list[str]:
    """Failed events that no successful retry, direct or chained, resolved."""
    retries: dict[str, list] = {}
    for event in project.events:
        if event.retry_of:
            retries.setdefault(event.retry_of, []).append(event)

    def resolved(event_id: str, seen: frozenset[str]) -> bool:
        for retry in retries.get(event_id, []):
            if retry.id in seen:
                continue
            if retry.outcome == "success" or resolved(retry.id, seen | {retry.id}):
                return True
        return False

    return [e.id for e in project.events if e.failed and not resolved(e.id, frozenset({e.id}))]


def _order(project: Project) -> dict[str, int]:
    return {task.id: index for index, task in enumerate(project.tasks)}


def _in_flight(project: Project, result: Report) -> list[str]:
    """Execution work in progress, most relevant first.

    Current phase, then critical-path position, then the phase exit authority,
    then authored order. Operations work in progress is never listed here,
    however recent or busy it is.
    """
    current = project.phase(project.current_phase or "")
    path = {task_id: index for index, task_id in enumerate(result.critical_path)}
    order = _order(project)
    wip = [t for t in project.execution_tasks if t.status == "WIP"]
    return [
        t.id
        for t in sorted(
            wip,
            key=lambda t: (
                not (current and t.phase == current.id),
                path.get(t.id, len(path)),
                not (current and current.exit_authority == t.id),
                order[t.id],
            ),
        )
    ]


def _verifiers(project: Project, gate) -> list:
    """Open tasks whose contract a gate is verified by."""
    refs = set(gate.verified_by)
    found = []
    for task in project.tasks:
        if task.done or not task.contract:
            continue
        contract = project.contracts.get(task.contract)
        if contract and (contract.id in refs or any(c.id in refs for c in contract.criteria)):
            found.append(task)
    return found


def _next_gate(project: Project, result: Report) -> dict[str, object] | None:
    """What stands between the current phase and its exit."""
    current = project.phase(project.current_phase or "")
    if current is None:
        return None
    authority = project.task(current.exit_authority or "")
    gates = []
    external: dict[str, dict[str, str]] = {}
    for gate in project.gates:
        if not any(entry.split()[:1] == [current.id] for entry in gate.blocks if entry.split()):
            continue
        verifiers = _verifiers(project, gate)
        for task in verifiers:
            if not task.execution:
                external[task.id] = {"id": task.id, "domain": task.domain, "via": gate.id}
        gates.append({
            "id": gate.id,
            "status": gate.status,
            "ready": gate.status == "GREEN" and not verifiers,
            "openVerifiers": [{"id": t.id, "domain": t.domain} for t in verifiers],
        })
    unmet_criteria: list[str] = []
    if authority is not None:
        unmet_criteria = unmet(project, authority)
        for dependency in _dependency_blockers(project, authority):
            known = project.task(dependency)
            if known is not None and not known.execution:
                external.setdefault(dependency, {"id": dependency, "domain": known.domain, "via": authority.id})
    unfinished = [t.id for t in project.execution_in(current.id) if not t.done]
    return {
        "phase": current.id,
        "exitAuthority": current.exit_authority,
        "exitAuthorityStatus": authority.status if authority else None,
        "unmetCriteria": unmet_criteria,
        "unfinishedExecution": unfinished,
        "gates": gates,
        "externalBlockers": [external[k] for k in sorted(external)],
        "ready": bool(
            gates is not None
            and all(g["ready"] for g in gates)
            and not external
            and all(t == current.exit_authority for t in unfinished)
        ),
    }


def _main_blocker(project: Project, result: Report) -> dict[str, object] | None:
    """The unresolved dependency most directly obstructing important execution.

    A blocked task is not a blocker, and work in progress with unmet criteria
    is work, not an obstruction. What is chosen is a dependency that an
    important execution task waits on, examined in this order: the current
    phase's exit (its authority and its red gates), the critical path, the rest
    of the current phase, then the rest of execution. The dependency may be an
    operations task; it keeps its domain (ADR-045).
    """
    current = project.phase(project.current_phase or "")
    order = _order(project)
    phase_rank = {p.id: i for i, p in enumerate(project.phases)}
    blocked = set(result.blocked)
    path = set(result.critical_path)

    def obstruction(task, reason: str) -> dict[str, object] | None:
        if task is None or task.done:
            return None
        open_dependencies = [
            d for d in task.dependencies
            if project.task(d) is not None and not project.task(d).done
        ]
        if not open_dependencies:
            return None
        # What can be acted on now comes first, and among that, the work on the
        # critical path; declaration order breaks ties.
        chosen = sorted(open_dependencies, key=lambda d: (
            d in blocked, d not in path, task.dependencies.index(d),
        ))[0]
        blocker = project.task(chosen)
        return {
            "kind": "TASK",
            "id": chosen,
            "title": blocker.title,
            "domain": blocker.domain,
            "status": blocker.status,
            "blocking": task.id,
            "blockingTitle": task.title,
            "reason": reason,
            "detail": f"{task.id} waits on {chosen}",
        }

    if current is not None:
        found = obstruction(project.task(current.exit_authority or ""), "phase exit")
        if found:
            return found
        for gate in (result.next_gate or {}).get("gates", []):
            if gate["status"] != "GREEN":
                return {
                    "kind": "GATE", "id": gate["id"], "title": gate["id"],
                    "domain": "execution", "status": gate["status"],
                    "blocking": current.id, "blockingTitle": current.name,
                    "reason": "phase exit",
                    "detail": f"{gate['id']} is {gate['status']}",
                }
    for task_id in result.critical_path:
        found = obstruction(project.task(task_id), "critical path")
        if found:
            return found
    candidates = [t for t in project.execution_tasks if not t.done]
    candidates.sort(key=lambda t: (
        not (current and t.phase == current.id),
        phase_rank.get(t.phase, len(phase_rank)),
        order[t.id],
    ))
    for task in candidates:
        reason = "current phase" if current and task.phase == current.id else "execution"
        found = obstruction(task, reason)
        if found:
            return found
    return None


def _execution_failures(project: Project) -> list[dict[str, object]]:
    """Execution tasks with a failed criterion or a failed event against them,
    each with the operational evidence that names it."""
    failures = []
    for task in project.execution_tasks:
        contract = project.contracts.get(task.contract or "")
        failed_criteria = [c.id for c in (contract.criteria if contract else []) if c.state == "FAIL"]
        related = [e for e in project.events if e.task == task.id or task.id in e.affects]
        failed_events = [e.id for e in related if e.failed]
        if failed_criteria or failed_events:
            failures.append({
                "task": task.id,
                "failedCriteria": failed_criteria,
                "failedEvents": failed_events,
                "relatedEvents": [e.id for e in related],
            })
    return failures


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
        "domain": task.domain,
        "domainSource": task.domain_source,
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
        "externalBlockers": result.external_blockers.get(task.id, []),
        "events": events_for(project, task.id),
        "debt": [d.id for d in project.debts_for(task.id)],
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
            "domain": task.domain,
            "domainSource": task.domain_source,
            "implementation": {"files": task.files, "symbols": task.symbols},
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
        # Operations work this task waits on, kept in its own domain.
        "externalBlockers": [
            {"id": o, "title": project.task(o).title, "domain": project.task(o).domain,
             "status": project.task(o).status}
            for o in report_now.external_blockers.get(task_id, [])
        ],
        "events": [e.as_json() for e in project.events if e.id in set(events_for(project, task_id))],
        # Debt this task introduced or repays, and debt its decisions created.
        "debt": [
            d.as_json() for d in project.debts
            if d in project.debts_for(task_id)
            or any(adr in d.introduced_by for adr in task.decisions)
        ],
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
