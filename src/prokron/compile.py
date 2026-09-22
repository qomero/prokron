"""Compile authored documents into one normalized project.

The compiler reads only the chronicle and writes only the compiled directory.
It never modifies authority, and its output is disposable: deleting the
compiled directory and running again reproduces it exactly.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import analytics, views
from .layout import AUTHORITY_DIR, COMPILED_DIR
from .model import Project
from .parse import (
    ParseError,
    parse_acceptance,
    parse_decisions,
    parse_phases,
    parse_project_name,
    parse_tasks,
    read_text,
)


class LayoutError(Exception):
    """Raised when a repository has no authored chronicle to compile."""


def locate(start: Path | None = None) -> Path:
    """Find the repository root by walking up to the authored directory."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / AUTHORITY_DIR / "TASKS.md").is_file():
            return candidate
    raise LayoutError(
        f"No {AUTHORITY_DIR}/TASKS.md found in {current} or any parent directory."
    )


def load(root: Path) -> Project:
    authority = root / AUTHORITY_DIR
    phases, gates, milestones = parse_phases(authority / "PHASES.md")
    # A project that names itself compiles the same in every checkout. One that
    # does not falls back to its directory, which is where the name used to
    # come from always.
    project = Project(
        name=parse_project_name(authority / "PHASES.md") or root.name,
        root=str(root),
        current_phase=None,
        phases=phases,
        tasks=parse_tasks(authority / "TASKS.md"),
        contracts=parse_acceptance(authority / "ACCEPTANCE.md"),
        gates=gates,
        milestones=milestones,
        decisions=parse_decisions(authority / "ADR"),
        intent=read_text(authority / "INTENT.md"),
        handoff=read_text(authority / "HANDOFF.md"),
    )
    # A phase whose work is finished but whose exit has not been accepted is
    # still where the project stands. Reporting "none" would lose that.
    for status in ("ACTIVE", "EXIT_PENDING"):
        standing = [phase for phase in project.phases if phase.status == status]
        if standing:
            project.current_phase = standing[-1].id
            break
    return project


def as_json(project: Project) -> dict[str, object]:
    """The normalized shape. Every object keeps provenance where practical."""
    report = analytics.report(project)
    return {
        "project": {
            "name": project.name,
            "currentPhase": project.current_phase,
            "generator": "prokron compile",
            "authority": AUTHORITY_DIR,
        },
        "phases": [
            {
                "id": phase.id,
                "name": phase.name,
                "outcome": phase.outcome,
                "entry": phase.entry,
                "exit": phase.exit,
                "exitAuthority": phase.exit_authority,
                "status": phase.status,
                "progress": report.phase_progress[phase.id].as_json(),
                "source": phase.source.as_json(),
            }
            for phase in project.phases
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "phase": task.phase,
                "status": task.status,
                "validation": task.validation,
                "deps": task.dependencies,
                "blocks": report.downstream.get(task.id, []),
                "ac": task.contract,
                "owner": task.owner,
                "claimed": task.claimed,
                "evidence": task.evidence,
                "decisions": task.decisions,
                "schedule": task.schedule.as_json(),
                "ready": task.id in report.ready,
                "blocked": task.id in report.blocked,
                "source": task.source.as_json(),
            }
            for task in project.tasks
        ],
        "acceptance": {
            contract.id: {
                "title": contract.title,
                "inherits": contract.inherits,
                "evidence": contract.evidence,
                "criteria": [
                    {
                        "id": criterion.id,
                        "text": criterion.text,
                        "evidenceClass": criterion.evidence_class,
                        "state": criterion.state,
                        "evidence": criterion.evidence,
                        "source": criterion.source.as_json(),
                    }
                    for criterion in contract.criteria
                ],
                "source": contract.source.as_json(),
            }
            for contract in project.contracts.values()
            if not contract.is_global
        },
        "invariants": [
            {
                "id": contract.id,
                "title": contract.title,
                "criteria": [
                    {
                        "id": criterion.id,
                        "text": criterion.text,
                        "evidenceClass": criterion.evidence_class,
                        "state": criterion.state,
                    }
                    for criterion in contract.criteria
                ],
                "appliesTo": [
                    task.id
                    for task in project.tasks
                    if contract.id
                    in getattr(project.contracts.get(task.contract or ""), "inherits", [])
                ],
                "source": contract.source.as_json(),
            }
            for contract in project.invariants
        ],
        "gates": [
            {
                "id": gate.id,
                "name": gate.name,
                "description": gate.description,
                "blocks": gate.blocks,
                "verifiedBy": gate.verified_by,
                "status": gate.status,
                "source": gate.source.as_json(),
            }
            for gate in project.gates
        ],
        "milestones": [
            {
                "id": milestone.id,
                "text": milestone.text,
                "task": milestone.task,
                "reached": bool(
                    milestone.task
                    and project.task(milestone.task)
                    and project.task(milestone.task).done
                ),
                "source": milestone.source.as_json(),
            }
            for milestone in project.milestones
        ],
        "decisions": [
            {
                "id": decision.id,
                "title": decision.title,
                "status": decision.status,
                "supersedes": decision.supersedes,
                "affects": decision.affects,
                "source": decision.source.as_json(),
            }
            for decision in project.decisions
        ],
        "obstacles": [obstacle.as_json() for obstacle in report.obstacles],
        "criticalPath": report.critical_path,
        "schedule": {
            "scheduled": report.scheduled,
            "unscheduled": report.unscheduled,
        },
        "metrics": report.metrics(),
        "ready": report.ready,
        "blocked": report.blocked,
        "wip": report.wip,
        "handoff": {"intent": project.intent, "handoff": project.handoff},
        "sources": {
            "authority": AUTHORITY_DIR,
            "documents": [
                "PHASES.md",
                "TASKS.md",
                "ACCEPTANCE.md",
                "ADR/",
                "INTENT.md",
                "HANDOFF.md",
            ],
        },
    }


def write(root: Path, project: Project) -> Path:
    """Write project.json and the Markdown views. Nothing else touches them."""
    compiled = root / COMPILED_DIR
    compiled.mkdir(parents=True, exist_ok=True)
    target = compiled / "project.json"
    target.write_text(json.dumps(as_json(project), indent=2, sort_keys=False) + "\n")
    for name, text in views.render_all(project, analytics.report(project)).items():
        (compiled / name).write_text(text)
    return target


__all__ = [
    "AUTHORITY_DIR",
    "COMPILED_DIR",
    "LayoutError",
    "ParseError",
    "as_json",
    "load",
    "locate",
    "write",
]
