"""Typed objects for one compiled project.

Nothing here reads or writes files. Parsers build these; everything downstream
consumes them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

STATUSES = ("TODO", "WIP", "DONE", "BLOCKED")
VALIDATIONS = ("UNTESTED", "SYNTHETIC", "AI_REVIEWED", "HUMAN_VERIFIED")
EVIDENCE_CLASSES = ("TEST", "MUTATION", "INSPECTION", "RUNTIME", "MANUAL")
CRITERION_STATES = ("PASS", "FAIL", "NOT_RUN")
PHASE_STATUSES = ("PLANNED", "ACTIVE", "EXIT_PENDING", "COMPLETE")
GATE_STATUSES = ("GREEN", "RED")
# A decision is recorded when it is made, or reconstructed afterwards from what
# the repository already depends on (ADR-037). Absent means contemporaneous.
DECISION_ORIGINS = ("CONTEMPORANEOUS", "RECONSTRUCTED")
NO_PHASE = "P-NONE"
# Every task is either work that advances the project itself, or work that
# maintains the environment it is built in (ADR-045). There is no third value.
DOMAINS = ("execution", "operations")
# How a task's domain was decided: authored, or inferred from structure. A
# task with no structural evidence is `unresolved`; it counts as execution and
# validation says so, rather than a guess being made from its title.
DOMAIN_SOURCES = ("declared", "phase", "exit-authority", "gate", "unresolved")
# Operational trace events (TRACE.md). An event is evidence, never a task.
EVENT_TYPES = (
    "tool-call", "command", "action", "mutation", "failure", "retry", "validation", "note",
)
EVENT_OUTCOMES = ("success", "failure", "partial", "unknown")
# Technical debt is a liability, not work (ADR-046). It has no domain; the
# task that repays it has one.
DEBT_STATUSES = ("OPEN", "ACCEPTED", "SCHEDULED", "RESOLVED", "INVALIDATED")
DEBT_CLOSED = ("RESOLVED", "INVALIDATED")
TRIGGER_STATES = ("NOT_REACHED", "APPROACHING", "REACHED")

OBSTACLE_TYPES = (
    "DEPENDENCY_BLOCKER",
    "ACCEPTANCE_BLOCKER",
    "GATE_BLOCKER",
    "PHASE_BLOCKER",
    "VALIDATION_GAP",
    "SCHEDULE_BLOCKER",
)


@dataclass(frozen=True)
class Source:
    """Where a compiled object came from, so a reader can reach authority."""

    file: str
    anchor: str

    def as_json(self) -> dict[str, str]:
        return {"file": self.file, "anchor": self.anchor}


@dataclass
class Criterion:
    id: str
    text: str
    evidence_class: str
    state: str
    evidence: str | None
    source: Source

    @property
    def satisfied(self) -> bool:
        return self.state == "PASS"


@dataclass
class Contract:
    """One task's completion contract, or an inherited AC-GLOBAL-* contract."""

    id: str
    title: str
    inherits: list[str]
    criteria: list[Criterion]
    evidence: str | None
    source: Source

    @property
    def is_global(self) -> bool:
        return self.id.startswith("AC-GLOBAL-")


@dataclass
class Schedule:
    start: str | None = None
    end: str | None = None
    estimate: str | None = None

    @property
    def known(self) -> bool:
        """True only when a real calendar bar can be drawn without inventing."""
        return bool(self.start and (self.end or self.estimate))

    def as_json(self) -> dict[str, str] | None:
        data = {k: v for k, v in vars(self).items() if v}
        return data or None


@dataclass
class Task:
    id: str
    title: str
    phase: str
    status: str
    validation: str
    dependencies: list[str]
    owner: str | None
    claimed: str | None
    contract: str | None
    evidence: str | None
    decisions: list[str]
    schedule: Schedule
    source: Source
    declared_domain: str | None = None
    domain: str = "execution"
    domain_source: str = "unresolved"
    # Optional implementation anchors (ADR-049): where the code for this task
    # lives, to seed a code-structure query. Never required, never derived.
    files: list[str] = field(default_factory=list)
    symbols: list[str] = field(default_factory=list)

    @property
    def done(self) -> bool:
        return self.status == "DONE"

    @property
    def execution(self) -> bool:
        return self.domain == "execution"

    @property
    def phase_independent(self) -> bool:
        return self.phase == NO_PHASE


@dataclass
class Phase:
    id: str
    name: str
    outcome: str
    entry: list[str]
    exit: list[str]
    exit_authority: str | None
    status: str
    source: Source


@dataclass
class Gate:
    id: str
    name: str
    description: str
    blocks: list[str]
    verified_by: list[str]
    status: str
    source: Source


@dataclass
class Milestone:
    id: str
    text: str
    task: str | None
    source: Source


@dataclass
class Decision:
    id: str
    title: str
    status: str
    supersedes: list[str]
    affects: list[str]
    source: Source
    origin: str = "CONTEMPORANEOUS"
    evidence: str | None = None
    authority: str | None = None

    @property
    def reconstructed(self) -> bool:
        return self.origin == "RECONSTRUCTED"


@dataclass
class TraceEvent:
    """One operational event: a tool call, command, mini-action, mutation,
    failure, retry, or validation run. Evidence about work, not work."""

    id: str
    title: str
    type: str
    time: str | None
    task: str | None
    agent: str | None
    tool: str | None
    target: str | None
    outcome: str
    error: str | None
    retry_of: str | None
    parent: str | None
    affects: list[str]
    artifact: str | None
    evidence: str | None
    source: Source

    @property
    def failed(self) -> bool:
        return self.outcome == "failure" or self.type == "failure"

    def as_json(self) -> dict[str, object]:
        return {
            "id": self.id, "title": self.title, "type": self.type, "time": self.time,
            "task": self.task, "agent": self.agent, "tool": self.tool,
            "target": self.target, "outcome": self.outcome, "error": self.error,
            "retryOf": self.retry_of, "parent": self.parent, "affects": self.affects,
            "artifact": self.artifact, "evidence": self.evidence,
            "source": self.source.as_json(),
        }


@dataclass
class TechDebt:
    """A known compromise: what it is, why it exists, what it costs, and what
    would retire it."""

    id: str
    title: str
    status: str
    introduced_by: list[str]
    areas: list[str]
    debt: str | None
    reason: str | None
    interest: str | None
    trigger: str | None
    trigger_state: str
    exit_condition: str | None
    evidence: str | None
    linked_tasks: list[str]
    resolution: str | None
    source: Source

    @property
    def closed(self) -> bool:
        return self.status in DEBT_CLOSED

    @property
    def needs_attention(self) -> bool:
        """Open to act on: a trigger reached or approaching, or not yet decided."""
        return not self.closed and (
            self.trigger_state in ("REACHED", "APPROACHING") or self.status == "OPEN"
        )

    def as_json(self) -> dict[str, object]:
        return {
            "id": self.id, "title": self.title, "status": self.status,
            "introducedBy": self.introduced_by, "areas": self.areas, "debt": self.debt,
            "reason": self.reason, "interest": self.interest, "trigger": self.trigger,
            "triggerState": self.trigger_state, "exitCondition": self.exit_condition,
            "evidence": self.evidence, "linkedTasks": self.linked_tasks,
            "resolution": self.resolution, "source": self.source.as_json(),
        }


@dataclass
class Obstacle:
    type: str
    subject: str
    blockers: list[str]
    detail: str
    domain: str = "execution"

    def as_json(self) -> dict[str, object]:
        return {
            "type": self.type,
            "subject": self.subject,
            "blockers": self.blockers,
            "detail": self.detail,
            "domain": self.domain,
        }


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Finding:
    severity: Severity
    code: str
    message: str
    where: str

    def render(self) -> str:
        return f"{self.severity}: {self.code}: {self.message} ({self.where})"


@dataclass
class Project:
    """The whole compiled project. Derived, disposable, never authoritative."""

    name: str
    root: str
    current_phase: str | None
    phases: list[Phase] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    contracts: dict[str, Contract] = field(default_factory=dict)
    gates: list[Gate] = field(default_factory=list)
    milestones: list[Milestone] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    intent: str = ""
    handoff: str = ""
    events: list[TraceEvent] = field(default_factory=list)
    debts: list[TechDebt] = field(default_factory=list)

    def debts_for(self, record_id: str) -> list[TechDebt]:
        """Debt a task or decision introduced, or a task repays."""
        return [d for d in self.debts if record_id in d.introduced_by or record_id in d.linked_tasks]

    @property
    def execution_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.execution]

    @property
    def operations_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.execution]

    def execution_in(self, phase_id: str) -> list[Task]:
        """A phase's own work: its execution tasks, never its operations."""
        return [t for t in self.tasks if t.phase == phase_id and t.execution]

    def task(self, task_id: str) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def phase(self, phase_id: str) -> Phase | None:
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        return None

    def tasks_in(self, phase_id: str) -> list[Task]:
        return [t for t in self.tasks if t.phase == phase_id]

    def mandatory_criteria(self, task: Task) -> list[Criterion]:
        """The criteria that decide whether this one task may be DONE.

        Inherited AC-GLOBAL-* contracts are project invariants, not per-task
        criteria: one task cannot carry evidence for a property of the whole
        project. They are reported separately and gate phases, not tasks.
        """
        contract = self.contracts.get(task.contract or "")
        return list(contract.criteria) if contract else []

    def invariants_for(self, task: Task) -> list[Contract]:
        contract = self.contracts.get(task.contract or "")
        if contract is None:
            return []
        return [
            self.contracts[name]
            for name in contract.inherits
            if name in self.contracts
        ]

    @property
    def invariants(self) -> list[Contract]:
        return [c for c in self.contracts.values() if c.is_global]
