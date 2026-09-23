"""Domain resolution: is a task project execution or project operations?

Execution is work that advances the project toward its deliverables and gates.
Operations maintains, operates, inspects, or changes the environment that work
happens in (ADR-045). Everything downstream — phase progress, the critical
path, gates, the focus strip — reads the domain resolved here, so this is the
only place the distinction is made.

Resolution never reads a title or an id. An authored `Domain:` decides.
Without one, structure can show a task is execution: it belongs to a phase, it
is a phase's exit authority, or a gate is verified by its contract. Nothing in
the structure can show a task is operations, so operations is always declared.
A task with no evidence either way resolves to execution — the reading earlier
releases gave it — and is marked `unresolved` for validation to report.
"""

from __future__ import annotations

from .model import DOMAINS, NO_PHASE, Project


def resolve(project: Project) -> None:
    exit_authorities = {p.exit_authority for p in project.phases if p.exit_authority}
    gate_references = {ref for gate in project.gates for ref in gate.verified_by}
    for task in project.tasks:
        if task.declared_domain in DOMAINS:
            task.domain, task.domain_source = task.declared_domain, "declared"
            continue
        task.domain = "execution"
        contract = project.contracts.get(task.contract or "")
        verifies_gate = bool(contract) and (
            contract.id in gate_references
            or any(c.id in gate_references for c in contract.criteria)
        )
        if task.phase != NO_PHASE:
            task.domain_source = "phase"
        elif task.id in exit_authorities:
            task.domain_source = "exit-authority"
        elif verifies_gate:
            task.domain_source = "gate"
        else:
            task.domain_source = "unresolved"
