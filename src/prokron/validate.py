"""Cross-document validation.

Errors are structural facts that make compiled state untrustworthy. Warnings
are conditions worth seeing that do not. Neither is a matter of taste: a
reviewer's preference never becomes a finding here.
"""

from __future__ import annotations

from .model import (
    CRITERION_STATES,
    DECISION_ORIGINS,
    EVIDENCE_CLASSES,
    GATE_STATUSES,
    NO_PHASE,
    PHASE_STATUSES,
    STATUSES,
    VALIDATIONS,
    Finding,
    Project,
)


def _cycles(project: Project) -> list[list[str]]:
    """Every dependency cycle, each reported once from its lowest member."""
    graph = {task.id: task.dependencies for task in project.tasks}
    found: list[list[str]] = []
    seen_signatures: set[frozenset[str]] = set()
    state: dict[str, int] = {}

    def walk(node: str, trail: list[str]) -> None:
        state[node] = 1
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if state.get(dependency) == 1:
                cycle = trail[trail.index(dependency) :] + [dependency]
                signature = frozenset(cycle)
                if signature not in seen_signatures:
                    seen_signatures.add(signature)
                    found.append(cycle)
            elif state.get(dependency, 0) == 0:
                walk(dependency, [*trail, dependency])
        state[node] = 2

    for task_id in graph:
        if state.get(task_id, 0) == 0:
            walk(task_id, [task_id])
    return found


def check(project: Project) -> list[Finding]:
    findings: list[Finding] = []

    def error(code: str, message: str, where: str) -> None:
        findings.append(Finding("error", code, message, where))

    def warn(code: str, message: str, where: str) -> None:
        findings.append(Finding("warning", code, message, where))

    seen: set[str] = set()
    phase_ids = {phase.id for phase in project.phases} | {NO_PHASE}
    decision_ids = {decision.id for decision in project.decisions}
    task_ids = {task.id for task in project.tasks}

    for task in project.tasks:
        where = f"{task.source.file}#{task.id}"
        if task.id in seen:
            error("duplicate-task", f"task {task.id} is defined more than once", where)
        seen.add(task.id)

        if task.status not in STATUSES:
            error("invalid-status", f"'{task.status}' is not a known status", where)
        if task.validation not in VALIDATIONS:
            error(
                "invalid-validation",
                f"'{task.validation}' is not a known validation state",
                where,
            )
        if task.phase not in phase_ids:
            error("unknown-phase", f"task names unknown phase '{task.phase}'", where)

        for dependency in task.dependencies:
            if dependency not in task_ids:
                error(
                    "unknown-dependency",
                    f"depends on {dependency}, which does not exist",
                    where,
                )
        for decision in task.decisions:
            if decision not in decision_ids:
                error(
                    "unknown-decision",
                    f"governed by {decision}, which has no ADR file",
                    where,
                )

        if not task.contract:
            error("missing-contract", "task has no AC reference", where)
        elif task.contract not in project.contracts:
            error(
                "unknown-contract",
                f"AC reference {task.contract} has no contract",
                where,
            )
        elif not project.contracts[task.contract].criteria:
            severity = error if task.done else warn
            severity(
                "empty-contract",
                f"contract {task.contract} states no criteria, so it sets no bar",
                where,
            )
        elif task.done:
            unresolved = [
                criterion.id
                for criterion in project.mandatory_criteria(task)
                if criterion.state != "PASS"
            ]
            if unresolved:
                error(
                    "unresolved-acceptance",
                    f"DONE with {len(unresolved)} unmet criteria: "
                    f"{', '.join(unresolved[:4])}",
                    where,
                )

        if not task.done and task.evidence:
            warn("premature-evidence", f"{task.status} task carries evidence", where)
        if task.schedule.start and not (task.schedule.end or task.schedule.estimate):
            warn(
                "partial-schedule",
                "scheduled task has no estimate or end date",
                where,
            )

    criterion_ids: set[str] = set()
    for contract in project.contracts.values():
        where = f"{contract.source.file}#{contract.id}"
        for inherited in contract.inherits:
            if inherited not in project.contracts:
                error(
                    "unknown-inheritance",
                    f"inherits {inherited}, which is not defined",
                    where,
                )
        for criterion in contract.criteria:
            if criterion.id in criterion_ids:
                error(
                    "duplicate-criterion",
                    f"criterion {criterion.id} is defined more than once",
                    where,
                )
            criterion_ids.add(criterion.id)
            if criterion.evidence_class not in EVIDENCE_CLASSES:
                error(
                    "invalid-evidence-class",
                    f"'{criterion.evidence_class}' is not a known evidence class",
                    where,
                )
            if criterion.state not in CRITERION_STATES:
                error(
                    "invalid-criterion-state",
                    f"'{criterion.state}' is not a known criterion state",
                    where,
                )
        if not contract.is_global and contract.id not in {
            task.contract for task in project.tasks
        }:
            warn("orphan-contract", "contract is referenced by no task", where)

    for cycle in _cycles(project):
        error(
            "dependency-cycle",
            " → ".join(cycle),
            f"{project.tasks[0].source.file}#{cycle[0]}" if project.tasks else "TASKS.md",
        )

    for phase in project.phases:
        where = f"{phase.source.file}#{phase.id}"
        if phase.status not in PHASE_STATUSES:
            error("invalid-phase-status", f"'{phase.status}' is not a known status", where)
        if phase.exit_authority and phase.exit_authority not in task_ids:
            error(
                "missing-exit-authority",
                f"exit authority {phase.exit_authority} is not a task",
                where,
            )
        if not phase.exit_authority and phase.status in {"ACTIVE", "EXIT_PENDING"}:
            warn("no-exit-authority", "active phase has no exit authority", where)

    for gate in project.gates:
        where = f"{gate.source.file}#{gate.id}"
        if gate.status not in GATE_STATUSES:
            error("invalid-gate-status", f"'{gate.status}' is not GREEN or RED", where)
        for reference in gate.verified_by:
            known = reference in project.contracts or reference in criterion_ids
            if not known:
                error(
                    "unknown-gate-reference",
                    f"verified by {reference}, which does not exist",
                    where,
                )

    for milestone in project.milestones:
        if milestone.task and milestone.task not in task_ids:
            error(
                "unknown-milestone-task",
                f"milestone names {milestone.task}, which does not exist",
                f"{milestone.source.file}#{milestone.id}",
            )

    # A reconstructed decision claims something the chronicle never observed.
    # It must say what it was inferred from, and it binds work only once a
    # person has confirmed it (ADR-037).
    for decision in project.decisions:
        where = f"{decision.source.file}#{decision.id}"
        if decision.origin not in DECISION_ORIGINS:
            error(
                "invalid-origin",
                f"'{decision.origin}' is not a known decision origin",
                where,
            )
        if not decision.reconstructed:
            continue
        if not decision.evidence:
            error(
                "reconstruction-without-evidence",
                "reconstructed decision cites no Evidence it was inferred from",
                where,
            )
        if decision.status == "ACCEPTED" and not decision.authority:
            error(
                "unconfirmed-reconstruction",
                "reconstructed decision is ACCEPTED but names no confirming Authority",
                where,
            )

    active = [phase for phase in project.phases if phase.status == "ACTIVE"]
    if len(active) > 1:
        error(
            "multiple-active-phases",
            f"{len(active)} phases are ACTIVE: {', '.join(p.id for p in active)}",
            "PHASES.md",
        )

    return findings


def errors(findings: list[Finding]) -> list[Finding]:
    return [finding for finding in findings if finding.severity == "error"]
