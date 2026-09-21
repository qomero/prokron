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
NO_PHASE = "P-NONE"

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

    @property
    def done(self) -> bool:
        return self.status == "DONE"

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


@dataclass
class Obstacle:
    type: str
    subject: str
    blockers: list[str]
    detail: str

    def as_json(self) -> dict[str, object]:
        return {
            "type": self.type,
            "subject": self.subject,
            "blockers": self.blockers,
            "detail": self.detail,
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
