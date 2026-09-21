"""Mermaid renderers.

Generated views carry no state that is not derivable from authority. The two
timeline renderers are deliberately different: one expresses ordering, the
other expresses dates, and only real metadata produces the second.
"""

from __future__ import annotations

from .analytics import Report
from .model import Project

_SHAPE = {
    "DONE": ("[", "]"),
    "WIP": ("([", "])"),
    "BLOCKED": ("{{", "}}"),
    "TODO": ("(", ")"),
}


def _node(task_id: str) -> str:
    return task_id.replace("-", "_")


def _label(text: str) -> str:
    return text.replace('"', "'")


def task_graph(project: Project, report: Report) -> str:
    lines = ["flowchart LR"]
    for phase in [*project.phases, None]:
        phase_id = phase.id if phase else "P-NONE"
        tasks = project.tasks_in(phase_id)
        if not tasks:
            continue
        title = f"{phase.id} {phase.name}" if phase else "Phase-independent"
        lines.append(f'    subgraph {_node(phase_id)}["{_label(title)}"]')
        for task in tasks:
            open_bracket, close_bracket = _SHAPE.get(task.status, _SHAPE["TODO"])
            lines.append(
                f"        {_node(task.id)}{open_bracket}"
                f'"{_label(task.id)}<br/>{_label(task.title)}"{close_bracket}'
            )
        lines.append("    end")
    for task in project.tasks:
        for dependency in task.dependencies:
            if project.task(dependency):
                lines.append(f"    {_node(dependency)} --> {_node(task.id)}")
    lines.append("    classDef done fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;")
    lines.append("    classDef wip fill:#fff8e1,stroke:#f9a825,color:#7f6000;")
    lines.append("    classDef blocked fill:#ffebee,stroke:#c62828,color:#8e0000;")
    for status, style in (("DONE", "done"), ("WIP", "wip")):
        members = [_node(t.id) for t in project.tasks if t.status == status]
        if members:
            lines.append(f"    class {','.join(members)} {style};")
    blocked = [_node(task_id) for task_id in report.blocked]
    if blocked:
        lines.append(f"    class {','.join(blocked)} blocked;")
    return "\n".join(lines) + "\n"


def critical_path(project: Project, report: Report) -> str:
    if not report.critical_path:
        return "flowchart LR\n    none[\"No open work\"]\n"
    lines = ["flowchart LR"]
    for task_id in report.critical_path:
        task = project.task(task_id)
        title = _label(task.title) if task else task_id
        lines.append(f'    {_node(task_id)}["{task_id}<br/>{title}"]')
    for left, right in zip(report.critical_path, report.critical_path[1:]):
        lines.append(f"    {_node(left)} --> {_node(right)}")
    return "\n".join(lines) + "\n"


def phase_flow(project: Project, report: Report) -> str:
    lines = ["flowchart TD"]
    for phase in project.phases:
        progress = report.phase_progress[phase.id]
        lines.append(
            f'    {_node(phase.id)}["{phase.id} {_label(phase.name)}<br/>'
            f'{progress} · {phase.status}"]'
        )
    for left, right in zip(project.phases, project.phases[1:]):
        lines.append(f"    {_node(left.id)} --> {_node(right.id)}")
    return "\n".join(lines) + "\n"


def gate_graph(project: Project) -> str:
    lines = ["flowchart LR"]
    for gate in project.gates:
        mark = "✓" if gate.status == "GREEN" else "✗"
        lines.append(
            f'    {_node(gate.id)}{{"{_label(gate.id)}<br/>'
            f'{_label(gate.name)} {mark}"}}'
        )
    for phase in project.phases:
        lines.append(f'    {_node(phase.id)}["{phase.id} exit"]')
        for gate in project.gates:
            if any(entry.split()[:1] == [phase.id] for entry in gate.blocks if entry.split()):
                lines.append(f"    {_node(gate.id)} --> {_node(phase.id)}")
    lines.append("    classDef green fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;")
    lines.append("    classDef red fill:#ffebee,stroke:#c62828,color:#8e0000;")
    for status, style in (("GREEN", "green"), ("RED", "red")):
        members = [_node(g.id) for g in project.gates if g.status == status]
        if members:
            lines.append(f"    class {','.join(members)} {style};")
    return "\n".join(lines) + "\n"


def dependency_timeline(project: Project, report: Report) -> str:
    """Ordering only. Every task sits in a depth band; no date is implied."""
    depth: dict[str, int] = {}

    def level(task_id: str, seen: frozenset[str]) -> int:
        """Bands count open work only, so the first startable task is step 1."""
        if task_id in depth:
            return depth[task_id]
        task = project.task(task_id)
        if task is None or task_id in seen:
            return 0
        parents = [
            level(dependency, seen | {task_id})
            for dependency in task.dependencies
            if project.task(dependency) and not project.task(dependency).done
        ]
        depth[task_id] = max(parents, default=-1) + 1
        return depth[task_id]

    for task in project.tasks:
        level(task.id, frozenset())

    lines = [
        "---",
        "displayMode: compact",
        "---",
        "gantt",
        "    title Dependency ordering, not a calendar",
        "    dateFormat X",
        "    axisFormat step %s",
    ]
    bands: dict[int, list[str]] = {}
    for task in project.tasks:
        if task.done:
            continue
        bands.setdefault(depth.get(task.id, 0), []).append(task.id)
    for band in sorted(bands):
        lines.append(f"    section Step {band + 1}")
        for task_id in bands[band]:
            task = project.task(task_id)
            marker = "active, " if task and task.status == "WIP" else ""
            lines.append(f"    {task_id} : {marker}{band}, {band + 1}")
    if not bands:
        lines.append("    section Complete")
        lines.append("    No open work : 0, 1")
    return "\n".join(lines) + "\n"


def calendar_gantt(project: Project, report: Report) -> str:
    """Dates only where real metadata exists. Nothing here is inferred."""
    lines = ["gantt", "    title Scheduled work", "    dateFormat YYYY-MM-DD"]
    if not report.scheduled:
        lines.append("    section Unscheduled")
        lines.append(
            f"    {len(report.unscheduled)} open "
            f"{'task has' if len(report.unscheduled) == 1 else 'tasks have'} "
            "no schedule metadata : milestone, 0d"
        )
        return "\n".join(lines) + "\n"
    by_phase: dict[str, list[dict[str, str]]] = {}
    for entry in report.scheduled:
        task = project.task(entry["id"])
        by_phase.setdefault(task.phase if task else "P-NONE", []).append(entry)
    for phase_id, entries in by_phase.items():
        lines.append(f"    section {phase_id}")
        for entry in entries:
            tail = entry.get("end") or entry.get("estimate")
            lines.append(f"    {entry['id']} : {entry['start']}, {tail}")
    if report.unscheduled:
        lines.append("    section Unscheduled")
        lines.append(
            f"    {len(report.unscheduled)} "
            f"{'task' if len(report.unscheduled) == 1 else 'tasks'} "
            "without schedule metadata : milestone, 0d"
        )
    return "\n".join(lines) + "\n"


def render_all(project: Project, report: Report) -> dict[str, str]:
    return {
        "task-graph.mmd": task_graph(project, report),
        "critical-path.mmd": critical_path(project, report),
        "phases.mmd": phase_flow(project, report),
        "gates.mmd": gate_graph(project),
        "timeline.mmd": dependency_timeline(project, report),
        "gantt.mmd": calendar_gantt(project, report),
    }
