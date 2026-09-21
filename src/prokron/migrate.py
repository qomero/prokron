"""Migrate a v0.1 chronicle to the v0.2 authored/compiled layout.

v0.1 kept authority in `.prokron/`. ADR-014 moved it to `prokron/` and left
`.prokron/` for compiled output. Updating the tool alone does not move the
records, so a project that upgrades keeps its history but reports nothing.

This moves it. It never deletes: the originals are archived untouched, and the
migration refuses to run over authority that already holds work.

Two files are treated differently from the rest:

- `TASK_GRAPH.md` is dropped, because every fact in it is derivable from
  `TASKS.md` and the compiler regenerates it on every run. Keeping a
  hand-written copy in the compiled directory would only invite it to go stale.
- `STATE.md` is not dropped, because its risks and next steps are judgement
  rather than derivation. That prose moves into `HANDOFF.md`, where authored
  narrative belongs. Losing it would be the one genuinely destructive thing a
  naive migration could do.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .compile import AUTHORITY_DIR, COMPILED_DIR

LEGACY_FILES = (
    "TASKS.md",
    "DECISIONS.md",
    "STATE.md",
    "TASK_GRAPH.md",
    "INTENT.md",
    "JOURNAL.md",
    "README.md",
)


class MigrationError(Exception):
    """Raised when migrating would lose or overwrite something."""


@dataclass
class Plan:
    root: Path
    tasks: int = 0
    decisions: int = 0
    contracts: int = 0
    archive: Path | None = None
    steps: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def render(self) -> str:
        lines = [f"Migration plan for {self.root}", ""]
        lines += [f"  {step}" for step in self.steps]
        if self.notes:
            lines += ["", "Notes:"]
            lines += [f"  {note}" for note in self.notes]
        return "\n".join(lines)


def _legacy_dir(root: Path) -> Path:
    return root / COMPILED_DIR


def needs_migration(root: Path) -> bool:
    """True when a v0.1 chronicle holds work that the v0.2 layout cannot see."""
    legacy_tasks = _legacy_dir(root) / "TASKS.md"
    if not legacy_tasks.is_file():
        return False
    if not re.search(r"(?m)^## T-", legacy_tasks.read_text()):
        return False
    current = root / AUTHORITY_DIR / "TASKS.md"
    if not current.is_file():
        return True
    return not re.search(r"(?m)^## T-", current.read_text())


def _split_entries(text: str, pattern: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(pattern, text, re.M))
    out = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        out.append((match.group(1), text[match.start() : end].rstrip() + "\n"))
    return out


def _evidence_class(evidence: str) -> str:
    """Classify recorded evidence by what it actually describes."""
    low = evidence.lower()
    if any(word in low for word in ("test", "unittest", "suite", "check")):
        return "TEST"
    if any(word in low for word in ("rendered", "browser", "ran ", "observed")):
        return "RUNTIME"
    return "INSPECTION"


def _migrate_tasks(text: str, phase: str) -> tuple[str, str, int]:
    """Rewrite tasks to reference contracts, and build those contracts.

    The prose acceptance statement becomes the criterion, worded as it was
    written. Restating a closed contract after the fact would change what its
    recorded evidence attests to.
    """
    entries = _split_entries(text, r"^## (T-[A-Za-z0-9.\-]+):")
    if not entries:
        return text, "", 0
    rewritten = [text[: text.index(entries[0][1])].rstrip()]
    contracts: list[str] = []

    for task_id, body in entries:
        acceptance = re.search(r"(?m)^- Acceptance: (.+(?:\n(?!- )[^\n]+)*)", body)
        status = re.search(r"(?m)^- Status: (\w+)", body)
        evidence = re.search(r"(?m)^- Evidence: (.+(?:\n(?!- )[^\n]+)*)", body)
        evidence_text = " ".join(evidence.group(1).split()) if evidence else ""

        if acceptance:
            statement = " ".join(acceptance.group(1).split())
            state = "PASS" if status and status.group(1) == "DONE" else "NOT_RUN"
            cls = _evidence_class(evidence_text)
            contracts.append(
                f"## AC-{task_id}\n\n"
                f"- `AC-{task_id}-01` — {statement} `{cls}` · `{state}`\n"
                + (f"  - Evidence: {evidence_text}\n" if evidence_text else "")
            )
            body = body.replace(acceptance.group(0), f"- AC: AC-{task_id}", 1)
        else:
            contracts.append(
                f"## AC-{task_id}\n\n"
                f"- `AC-{task_id}-01` — This task predates acceptance contracts and "
                f"recorded no acceptance statement. Replace this criterion with what "
                f"must be demonstrated. `INSPECTION` · `NOT_RUN`\n"
            )
            body = re.sub(
                r"(?m)^(- Status: [^\n]*\n)", rf"\1- AC: AC-{task_id}\n", body, count=1
            )

        if not re.search(r"(?m)^- Phase: ", body):
            body = re.sub(r"(?m)^(- Status: [^\n]*\n)", rf"\1- Phase: {phase}\n", body, count=1)
        rewritten.append(body.rstrip())

    header = (
        "# Acceptance\n\n"
        "Completion-contract authority. A task is done when its frozen contract\n"
        "has sufficient evidence.\n\n"
        "These contracts were migrated from prose acceptance statements written\n"
        "before this file existed. Their wording is preserved as it stood, because\n"
        "restating a closed contract would change what its evidence attests to.\n\n"
        "---\n\n# Contracts\n\n"
    )
    return "\n\n".join(rewritten) + "\n", header + "\n".join(contracts), len(entries)


def _migrate_decisions(text: str) -> dict[str, str]:
    files: dict[str, str] = {}
    for adr_id, body in _split_entries(text, r"^## (ADR-[0-9]+):"):
        files[f"{adr_id}.md"] = body.replace(f"## {adr_id}", f"# {adr_id}", 1)
    return files


def _adr_index(files: dict[str, str]) -> str:
    lines = [
        "# Decisions",
        "",
        "Accepted engineering decision authority. One file per ADR, append-only.",
        "A decision that changes is superseded by a new ADR; the earlier file stays,",
        "with its original status intact.",
        "",
    ]
    superseded: dict[str, list[str]] = {}
    meta: dict[str, tuple[str, str]] = {}
    for name, body in sorted(files.items()):
        adr_id = name[:-3]
        title = re.match(r"# ADR-[0-9]+: (.+)", body)
        status = re.search(r"- Status: (\w+)", body)
        meta[adr_id] = (title.group(1) if title else adr_id, status.group(1) if status else "UNKNOWN")
        for target in re.findall(r"- Supersedes: (.+)", body):
            for ref in re.findall(r"ADR-[0-9]+", target):
                superseded.setdefault(ref, []).append(adr_id)
    for adr_id, (title, status) in sorted(meta.items()):
        note = f" — superseded by {', '.join(superseded[adr_id])}" if adr_id in superseded else ""
        lines.append(f"- [{adr_id}]({adr_id}.md) — {title} ({status}){note}")
    return "\n".join(lines) + "\n"


def _handoff_from_state(state: str) -> str:
    return (
        "# Handoff\n\n"
        "Current implementation continuity. Overwritten, never appended.\n\n"
        "## Migrated from STATE.md\n\n"
        "The v0.1 chronicle kept risks, position and next steps in `STATE.md`.\n"
        "`.prokron/STATE.md` is now generated from compiled facts, so this prose —\n"
        "which is judgement, not derivation — was moved here rather than lost.\n"
        "Rewrite it as an ordinary handoff when convenient.\n\n"
        "---\n\n" + state.strip() + "\n"
    )


def plan(root: Path, phase: str = "P-NONE") -> Plan:
    legacy = _legacy_dir(root)
    authority = root / AUTHORITY_DIR
    result = Plan(root=root)

    if not needs_migration(root):
        raise MigrationError(
            f"Nothing to migrate: no v0.1 chronicle with tasks found in "
            f"{legacy}, or {authority} already holds work."
        )

    stamp = date.today().isoformat()
    result.archive = root / f"{COMPILED_DIR}-v0.1-backup-{stamp}"
    if result.archive.exists():
        raise MigrationError(f"Archive already exists: {result.archive}")

    tasks_text = (legacy / "TASKS.md").read_text()
    _, contracts, count = _migrate_tasks(tasks_text, phase)
    result.tasks = count
    result.contracts = len(re.findall(r"(?m)^## AC-", contracts))

    decisions_path = legacy / "DECISIONS.md"
    adrs = _migrate_decisions(decisions_path.read_text()) if decisions_path.is_file() else {}
    result.decisions = len(adrs)

    result.steps = [
        f"move {count} tasks to {AUTHORITY_DIR}/TASKS.md, each referencing a contract",
        f"write {result.contracts} contracts to {AUTHORITY_DIR}/ACCEPTANCE.md from prose acceptance",
        f"split {len(adrs)} decisions into {AUTHORITY_DIR}/ADR/ with an index",
        f"move INTENT.md and JOURNAL.md to {AUTHORITY_DIR}/",
        f"move STATE.md prose into {AUTHORITY_DIR}/HANDOFF.md",
        f"drop TASK_GRAPH.md, which the compiler regenerates",
        f"archive the originals unchanged to {result.archive.name}/",
    ]
    result.notes = [
        f"every task is marked phase {phase}; v0.1 had no phases, so none are invented",
        "no file is deleted; the archive keeps the originals byte for byte",
    ]
    if phase == "P-NONE":
        result.notes.append(
            "phase-independent work is excluded from phase progress — create a phase "
            f"in {AUTHORITY_DIR}/PHASES.md and reassign tasks when you are ready"
        )
    return result


def apply(root: Path, phase: str = "P-NONE") -> Plan:
    result = plan(root, phase)
    legacy = _legacy_dir(root)
    authority = root / AUTHORITY_DIR
    (authority / "ADR").mkdir(parents=True, exist_ok=True)

    tasks, contracts, _ = _migrate_tasks((legacy / "TASKS.md").read_text(), phase)
    (authority / "TASKS.md").write_text(tasks)
    (authority / "ACCEPTANCE.md").write_text(contracts)

    decisions_path = legacy / "DECISIONS.md"
    if decisions_path.is_file():
        adrs = _migrate_decisions(decisions_path.read_text())
        for name, body in adrs.items():
            (authority / "ADR" / name).write_text(body)
        (authority / "ADR" / "README.md").write_text(_adr_index(adrs))

    for name in ("INTENT.md", "JOURNAL.md"):
        source = legacy / name
        if source.is_file():
            (authority / name).write_text(source.read_text())

    state = legacy / "STATE.md"
    if state.is_file():
        (authority / "HANDOFF.md").write_text(_handoff_from_state(state.read_text()))

    assert result.archive is not None
    result.archive.mkdir()
    for name in LEGACY_FILES:
        source = legacy / name
        if source.is_file():
            shutil.move(str(source), str(result.archive / name))
    return result
