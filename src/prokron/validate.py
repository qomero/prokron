"""Cross-document validation.

Errors are structural facts that make compiled state untrustworthy. Warnings
are conditions worth seeing that do not. Neither is a matter of taste: a
reviewer's preference never becomes a finding here.
"""

from __future__ import annotations

import re
from pathlib import Path

from .layout import AUTHORITY_DIR
from .model import (
    CRITERION_STATES,
    DEBT_STATUSES,
    DECISION_ORIGINS,
    DOMAINS,
    TRIGGER_STATES,
    EVENT_OUTCOMES,
    EVENT_TYPES,
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


# A backticked, repository-relative file path: at least one directory, and a
# last segment with an extension. Branch names (`feature/work`), commands, and
# directories do not match, which keeps the check quiet about prose.
_CITED_PATH = re.compile(r"`((?:[\w.\-]+/)+[\w\-][\w.\-]*\.[A-Za-z0-9]+)`")


def stale_references(project: Project) -> list[Finding]:
    """Paths the current-state documents cite that no longer exist.

    Handoff and intent are prose, so nothing else resolves what they point at;
    the continuity pilot found a handoff sending agents to a moved path. This
    is the one check that reads the filesystem, and it only warns.
    """
    root = Path(project.root)
    authority = root / AUTHORITY_DIR
    findings: list[Finding] = []
    for name, text in (("HANDOFF.md", project.handoff), ("INTENT.md", project.intent)):
        seen: set[str] = set()
        for cited in _CITED_PATH.findall(text):
            if cited in seen or cited.startswith("../") or "//" in cited:
                continue
            seen.add(cited)
            if not ((root / cited).exists() or (authority / cited).exists()):
                findings.append(
                    Finding("warning", "stale-reference", f"cites `{cited}`, which does not exist", name)
                )
    return findings


# Values that look like credentials. A trace is evidence for review; it must
# never become the place a token is published (ADR-045).
_SECRET = re.compile(
    r"(ghp_|gho_|ghs_|github_pat_|xox[abprs]-|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_\-]{16,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY|\b(?:password|passwd|secret|token|api[_-]?key)\s*[=:]\s*\S+)",
    re.IGNORECASE,
)
_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$")


def domain_findings(project: Project) -> list[Finding]:
    """Domain validity and execution structure (ADR-045)."""
    findings: list[Finding] = []
    exit_authorities = {p.exit_authority: p.id for p in project.phases if p.exit_authority}
    for task in project.tasks:
        where = f"{task.source.file}#{task.id}"
        if task.declared_domain and task.declared_domain not in DOMAINS:
            findings.append(Finding(
                "error", "invalid-domain",
                f"'{task.declared_domain}' is not a domain; use execution or operations", where,
            ))
        elif task.domain_source == "unresolved":
            findings.append(Finding(
                "warning", "ambiguous-domain",
                "phase-independent task with no Domain; counted as execution until one is declared",
                where,
            ))
        if not task.execution and not task.phase_independent:
            findings.append(Finding(
                "warning", "operations-in-phase",
                f"operations task names phase {task.phase}; it is not counted in that phase's progress",
                where,
            ))
        if not task.execution and task.id in exit_authorities:
            findings.append(Finding(
                "warning", "operations-exit-authority",
                f"operations task is the exit authority of {exit_authorities[task.id]}", where,
            ))
    return findings


def trace_findings(project: Project) -> list[Finding]:
    """Trace consistency. Strict about the trace's own structure, lenient about
    what it names, so a project can start recording without its history first
    being perfect."""
    findings: list[Finding] = []
    ids: set[str] = set()
    known = (
        {t.id for t in project.tasks}
        | {g.id for g in project.gates}
        | {p.id for p in project.phases}
        | {d.id for d in project.decisions}
        | set(project.contracts)
        | {c.id for contract in project.contracts.values() for c in contract.criteria}
    )
    event_ids = {e.id for e in project.events}
    for event in project.events:
        where = f"{event.source.file}#{event.id}"
        if event.id in ids:
            findings.append(Finding("error", "duplicate-event", f"event {event.id} is defined more than once", where))
        ids.add(event.id)
        if event.type not in EVENT_TYPES:
            findings.append(Finding("error", "invalid-event-type", f"'{event.type}' is not an event type", where))
        if event.outcome not in EVENT_OUTCOMES:
            findings.append(Finding("error", "invalid-event-outcome", f"'{event.outcome}' is not an outcome", where))
        for field_name, reference in (("Parent", event.parent), ("Retry of", event.retry_of)):
            if reference and reference not in event_ids:
                findings.append(Finding(
                    "error", "unknown-event-reference", f"{field_name} names {reference}, which is not an event", where,
                ))
            if reference == event.id:
                findings.append(Finding("error", "self-referencing-event", f"{field_name} names the event itself", where))
        if event.task and event.task not in {t.id for t in project.tasks}:
            findings.append(Finding("warning", "unknown-event-task", f"names task {event.task}, which does not exist", where))
        for reference in event.affects:
            if reference not in known:
                findings.append(Finding("warning", "unknown-event-affects", f"affects {reference}, which is not in the chronicle", where))
        if event.time and not _TIME.match(event.time):
            findings.append(Finding("warning", "invalid-event-time", f"'{event.time}' is not an ISO date or time", where))
        text = " ".join(filter(None, (
            event.title, event.tool, event.target, event.error, event.artifact, event.evidence, event.agent,
        )))
        if _SECRET.search(text):
            findings.append(Finding(
                "warning", "possible-secret", "event text looks like it contains a credential; remove it", where,
            ))
    return findings


def debt_findings(project: Project) -> list[Finding]:
    """Technical debt lifecycle and lineage (ADR-046)."""
    findings: list[Finding] = []
    task_ids = {t.id for t in project.tasks}
    decision_ids = {d.id for d in project.decisions}
    seen: set[str] = set()
    for debt in project.debts:
        where = f"{debt.source.file}#{debt.id}"

        def error(code: str, message: str) -> None:
            findings.append(Finding("error", code, message, where))

        def warn(code: str, message: str) -> None:
            findings.append(Finding("warning", code, message, where))

        if debt.id in seen:
            error("duplicate-debt", f"debt {debt.id} is defined more than once")
        seen.add(debt.id)
        if debt.status not in DEBT_STATUSES:
            error("invalid-debt-status", f"'{debt.status}' is not a debt status")
        if debt.trigger_state not in TRIGGER_STATES:
            error("invalid-trigger-state", f"'{debt.trigger_state}' is not a trigger state")
        if not debt.debt:
            error("debt-without-description", "debt states no Debt")
        if not debt.exit_condition:
            error("debt-without-exit", "debt states no Exit condition, so it can never be resolved")
        if not debt.trigger and debt.status not in ("OPEN", "RESOLVED", "INVALIDATED"):
            warn("debt-without-trigger", "carried debt states no Trigger for when it stops being acceptable")
        if debt.status == "SCHEDULED" and not debt.linked_tasks:
            error("scheduled-debt-without-task", "SCHEDULED debt links no repayment task")
        if debt.closed and not debt.resolution:
            error("closed-debt-without-resolution", f"{debt.status} debt records no Resolution")
        for reference in debt.introduced_by:
            if reference.startswith("ADR-") and reference not in decision_ids:
                error("unknown-debt-reference", f"introduced by {reference}, which has no ADR file")
            elif reference.startswith("T-") and reference not in task_ids:
                error("unknown-debt-reference", f"introduced by {reference}, which is not a task")
        for task_id in debt.linked_tasks:
            if task_id not in task_ids:
                error("unknown-debt-reference", f"links {task_id}, which is not a task")
        if debt.status == "RESOLVED":
            open_tasks = [t for t in debt.linked_tasks if project.task(t) and not project.task(t).done]
            if open_tasks:
                warn("resolved-debt-open-task", f"RESOLVED while {', '.join(open_tasks)} is still open")
        if debt.trigger_state == "REACHED" and debt.status in ("OPEN", "ACCEPTED"):
            warn("debt-trigger-reached", "trigger reached but no repayment is scheduled")
    return findings


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
    module_ids = {module.id for module in project.modules}

    # The hierarchy (ADR-035): one thesis, modules in known phases, and tasks
    # owned by modules. A chronicle that has not adopted it yet stays readable
    # and compilable, with the conversion made visible (ADR-036).
    thesis_at = f"{project.thesis.source.file}#{project.thesis.source.anchor}"
    if not project.thesis.statement:
        if project.uses_modules:
            error("missing-thesis", "modules exist but THESIS.md has no Statement", thesis_at)
        elif project.tasks:
            warn("missing-thesis",
                 "no product thesis; author THESIS.md before converting tasks to modules",
                 thesis_at)
    seen_modules: set[str] = set()
    for module in project.modules:
        where = f"{module.source.file}#{module.id}"
        if module.id in seen_modules:
            error("duplicate-module", f"module {module.id} is defined more than once", where)
        seen_modules.add(module.id)
        if module.phase not in phase_ids:
            error("unknown-module-phase", f"module names unknown phase '{module.phase}'", where)

    for task in project.tasks:
        where = f"{task.source.file}#{task.id}"
        if task.module:
            if task.module not in module_ids:
                error("unknown-module", f"task names unknown module '{task.module}'", where)
            if task.legacy_phase:
                error("duplicate-phase-authority",
                      "task authors both Module and Phase; its phase comes from its module",
                      where)
        else:
            warn("legacy-task-phase",
                 f"task names phase {task.legacy_phase} directly; convert it to a Module", where)
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
        if not task.module and task.phase not in phase_ids:
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

    findings.extend(domain_findings(project))
    findings.extend(trace_findings(project))
    findings.extend(debt_findings(project))
    findings.extend(stale_references(project))
    return findings


def errors(findings: list[Finding]) -> list[Finding]:
    return [finding for finding in findings if finding.severity == "error"]
