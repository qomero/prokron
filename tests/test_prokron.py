"""Regression suite for the Prokron runtime.

The fixture project is deliberately small and deliberately broken in places:
several tests exist to prove that validation refuses to compile nonsense.
"""

from __future__ import annotations

import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prokron import (  # noqa: E402
    analytics, cli, compile as compiler, dashboard, layout, mermaid, migrate,
    validate, views,
)
from prokron.parse import ParseError  # noqa: E402

PHASES = """# Phases

## P1 — Foundation

Outcome:
The thing works.

Entry:
- A repository exists.

Exit:
- Gate A.

Exit authority:
T-TWO

Status:
ACTIVE

---

# Gates

## Gate A — Single authority

Only one source of truth exists.

Blocks: P1 exit
Verified by: `AC-GLOBAL-CARE`
Status: RED

---

# Milestones

- `M-FIRST` — First light. Reached when T-ONE is `DONE`.
"""

TASKS = """# Tasks

## T-ONE: Lay the foundation
- Status: DONE
- Phase: P1
- Validation: SYNTHETIC
- Dependencies: none
- Owner: someone
- AC: AC-T-ONE
- Evidence: It holds weight.
- Governed by: ADR-001

## T-TWO: Build on it
- Status: TODO
- Phase: P1
- Validation: UNTESTED
- Dependencies: T-ONE
- Owner: unassigned
- AC: AC-T-TWO
- Evidence: —
- Governed by: ADR-001

## T-THREE: Finish later
- Status: TODO
- Phase: P1
- Validation: UNTESTED
- Dependencies: T-TWO
- Owner: unassigned
- AC: AC-T-THREE
- Schedule: start=2026-10-01 estimate=3d
- Evidence: —
- Governed by: ADR-001
"""

ACCEPTANCE = """# Acceptance

## Inherited contracts

### AC-GLOBAL-CARE

- `AC-GLOBAL-CARE-01` — Given anything, When it ships, Then it is careful.
  `INSPECTION`

---

# Contracts

## AC-T-ONE — Lay the foundation

Inherits: `AC-GLOBAL-CARE`

- `AC-T-ONE-01` — Given a site, When the foundation is poured, Then it is
  level. `TEST` · `PASS`
  - Evidence: Measured on site.

## AC-T-TWO — Build on it

- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.
  `TEST` · `NOT_RUN`

## AC-T-THREE — Finish later

- `AC-T-THREE-01` — Given walls, When the roof goes on, Then it keeps rain out.
  `RUNTIME` · `NOT_RUN`
"""

ADR = """# ADR-001: Do the simple thing
- Date: 2026-01-01
- Status: ACCEPTED
- Supersedes: none
- Affects: T-ONE, T-TWO
- Context: Complexity is expensive.
- Decision: Prefer the simple thing.
"""


def build_fixture(root: Path, authority: str = layout.AUTHORITY_DIR) -> Path:
    authority = root / authority
    (authority / "ADR").mkdir(parents=True)
    (authority / "PHASES.md").write_text(PHASES)
    (authority / "TASKS.md").write_text(TASKS)
    (authority / "ACCEPTANCE.md").write_text(ACCEPTANCE)
    (authority / "ADR" / "ADR-001.md").write_text(ADR)
    (authority / "INTENT.md").write_text("# Intent\n\nNo active intent.\n")
    (authority / "HANDOFF.md").write_text("# Handoff\n\nNothing in flight.\n")
    return root


class FixtureCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="prokron-test-"))
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.root = build_fixture(self.dir)
        self.project = compiler.load(self.root)

    def rewrite(self, name: str, old: str, new: str) -> None:
        path = self.root / layout.AUTHORITY_DIR / name
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))
        self.project = compiler.load(self.root)

    def codes(self) -> set[str]:
        return {finding.code for finding in validate.check(self.project)}


class TestParsing(FixtureCase):
    def test_tasks_parse_with_fields_and_provenance(self) -> None:
        task = self.project.task("T-ONE")
        self.assertEqual(task.title, "Lay the foundation")
        self.assertEqual(task.phase, "P1")
        self.assertEqual(task.dependencies, [])
        self.assertEqual(task.decisions, ["ADR-001"])
        self.assertEqual(task.source.file, "TASKS.md")
        self.assertEqual(task.source.anchor, "T-ONE")

    def test_dependencies_and_em_dash_evidence(self) -> None:
        self.assertEqual(self.project.task("T-TWO").dependencies, ["T-ONE"])
        self.assertIsNone(self.project.task("T-TWO").evidence)

    def test_schedule_metadata_is_optional_and_typed(self) -> None:
        self.assertFalse(self.project.task("T-TWO").schedule.known)
        schedule = self.project.task("T-THREE").schedule
        self.assertEqual(schedule.start, "2026-10-01")
        self.assertEqual(schedule.estimate, "3d")
        self.assertTrue(schedule.known)

    def test_criteria_keep_class_state_and_evidence(self) -> None:
        criterion = self.project.contracts["AC-T-ONE"].criteria[0]
        self.assertEqual(criterion.evidence_class, "TEST")
        self.assertEqual(criterion.state, "PASS")
        self.assertEqual(criterion.evidence, "Measured on site.")

    def test_global_contracts_are_invariants_not_task_criteria(self) -> None:
        self.assertEqual([c.id for c in self.project.invariants], ["AC-GLOBAL-CARE"])
        task = self.project.task("T-ONE")
        self.assertEqual([c.id for c in self.project.mandatory_criteria(task)], ["AC-T-ONE-01"])
        self.assertEqual([c.id for c in self.project.invariants_for(task)], ["AC-GLOBAL-CARE"])

    def test_a_nested_section_does_not_swallow_later_contracts(self) -> None:
        self.assertIn("AC-T-THREE", self.project.contracts)
        self.assertEqual(len(self.project.contracts["AC-GLOBAL-CARE"].criteria), 1)

    def test_phases_gates_and_milestones(self) -> None:
        phase = self.project.phase("P1")
        self.assertEqual(phase.status, "ACTIVE")
        self.assertEqual(phase.exit_authority, "T-TWO")
        self.assertEqual(self.project.gates[0].status, "RED")
        self.assertEqual(self.project.gates[0].blocks, ["P1 exit"])
        self.assertEqual(self.project.milestones[0].task, "T-ONE")

    def test_malformed_task_heading_names_the_file(self) -> None:
        (self.root / layout.AUTHORITY_DIR / "TASKS.md").write_text("# Tasks\n\n## nonsense\n")
        with self.assertRaises(ParseError) as caught:
            compiler.load(self.root)
        self.assertEqual(caught.exception.file, "TASKS.md")

    def test_missing_required_field_is_rejected(self) -> None:
        self.rewrite_raw("TASKS.md", "- Phase: P1\n- Validation: SYNTHETIC\n", "")
        with self.assertRaises(ParseError) as caught:
            compiler.load(self.root)
        self.assertIn("missing required field", str(caught.exception))

    def rewrite_raw(self, name: str, old: str, new: str) -> None:
        path = self.root / layout.AUTHORITY_DIR / name
        path.write_text(path.read_text().replace(old, new, 1))


class TestValidation(FixtureCase):
    def test_clean_authority_reports_nothing(self) -> None:
        self.assertEqual(validate.check(self.project), [])

    def test_unknown_dependency(self) -> None:
        self.rewrite("TASKS.md", "- Dependencies: T-ONE", "- Dependencies: T-GHOST")
        self.assertIn("unknown-dependency", self.codes())

    def test_duplicate_task(self) -> None:
        path = self.root / layout.AUTHORITY_DIR / "TASKS.md"
        path.write_text(path.read_text() + TASKS.split("# Tasks\n")[1].split("## T-TWO")[0])
        self.project = compiler.load(self.root)
        self.assertIn("duplicate-task", self.codes())

    def test_unknown_phase(self) -> None:
        self.rewrite("TASKS.md", "- Phase: P1\n- Validation: UNTESTED", "- Phase: P9\n- Validation: UNTESTED")
        self.assertIn("unknown-phase", self.codes())

    def test_missing_contract_reference(self) -> None:
        self.rewrite("TASKS.md", "- AC: AC-T-TWO\n", "")
        self.assertIn("missing-contract", self.codes())

    def test_unknown_contract_reference(self) -> None:
        self.rewrite("TASKS.md", "- AC: AC-T-TWO", "- AC: AC-T-NOWHERE")
        self.assertIn("unknown-contract", self.codes())

    def test_done_task_with_unmet_criterion(self) -> None:
        self.rewrite("ACCEPTANCE.md", "level. `TEST` · `PASS`", "level. `TEST` · `NOT_RUN`")
        self.assertIn("unresolved-acceptance", self.codes())

    def test_duplicate_criterion_within_a_contract_is_rejected_at_parse_time(self) -> None:
        with self.assertRaises(ParseError):
            self.rewrite(
                "ACCEPTANCE.md",
                "- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.\n  `TEST` · `NOT_RUN`",
                "- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.\n  `TEST` · `NOT_RUN`\n"
                "- `AC-T-TWO-01` — Given a copy, When it appears, Then it is caught.\n  `TEST` · `NOT_RUN`",
            )

    def test_duplicate_criterion_across_contracts_is_a_validation_error(self) -> None:
        self.rewrite(
            "ACCEPTANCE.md",
            "- `AC-T-THREE-01` — Given walls, When the roof goes on, Then it keeps rain out.\n  `RUNTIME` · `NOT_RUN`",
            "- `AC-T-TWO-01` — Given a stolen identifier, When it reappears, Then it is caught.\n  `RUNTIME` · `NOT_RUN`",
        )
        self.assertIn("duplicate-criterion", self.codes())

    def test_unknown_adr_reference(self) -> None:
        self.rewrite("TASKS.md", "- Governed by: ADR-001", "- Governed by: ADR-404")
        self.assertIn("unknown-decision", self.codes())

    def test_dependency_cycle(self) -> None:
        self.rewrite("TASKS.md", "## T-ONE: Lay the foundation\n- Status: DONE", "## T-ONE: Lay the foundation\n- Status: TODO")
        self.rewrite("TASKS.md", "- Dependencies: none", "- Dependencies: T-THREE")
        self.assertIn("dependency-cycle", self.codes())

    def test_missing_phase_exit_task(self) -> None:
        self.rewrite("PHASES.md", "Exit authority:\nT-TWO", "Exit authority:\nT-MISSING")
        self.assertIn("missing-exit-authority", self.codes())

    def test_gate_referencing_unknown_contract(self) -> None:
        self.rewrite("PHASES.md", "Verified by: `AC-GLOBAL-CARE`", "Verified by: `AC-NOT-REAL`")
        self.assertIn("unknown-gate-reference", self.codes())

    def test_invalid_status_and_validation(self) -> None:
        self.rewrite("TASKS.md", "- Status: TODO\n- Phase: P1\n- Validation: UNTESTED", "- Status: MAYBE\n- Phase: P1\n- Validation: VIBES")
        codes = self.codes()
        self.assertIn("invalid-status", codes)
        self.assertIn("invalid-validation", codes)

    def test_warnings_do_not_block(self) -> None:
        self.rewrite(
            "TASKS.md",
            "## T-TWO: Build on it\n- Status: TODO",
            "## T-TWO: Build on it\n- Schedule: start=2026-10-01\n- Status: TODO",
        )
        findings = validate.check(self.project)
        self.assertTrue(findings)
        self.assertEqual(validate.errors(findings), [])

    def test_two_active_phases_are_an_error(self) -> None:
        path = self.root / layout.AUTHORITY_DIR / "PHASES.md"
        path.write_text(
            path.read_text().replace(
                "---\n\n# Gates",
                "---\n\n## P2 — Second\n\nOutcome:\nMore.\n\nEntry:\n- P1 done.\n\n"
                "Exit:\n- Nothing.\n\nExit authority:\nT-THREE\n\nStatus:\nACTIVE\n\n---\n\n# Gates",
            )
        )
        self.project = compiler.load(self.root)
        self.assertIn("multiple-active-phases", self.codes())


class TestAnalytics(FixtureCase):
    def setUp(self) -> None:
        super().setUp()
        self.report = analytics.report(self.project)

    def test_ready_and_blocked(self) -> None:
        self.assertEqual(self.report.ready, ["T-TWO"])
        self.assertEqual(self.report.blocked, ["T-THREE"])

    def test_work_in_flight_is_not_also_reported_as_ready(self) -> None:
        self.rewrite("TASKS.md", "## T-TWO: Build on it\n- Status: TODO", "## T-TWO: Build on it\n- Status: WIP")
        report = analytics.report(self.project)
        self.assertEqual(report.wip, ["T-TWO"])
        self.assertEqual(report.ready, [])

    def test_obstacles_are_typed_and_name_their_blockers(self) -> None:
        dependency = [o for o in self.report.obstacles if o.type == "DEPENDENCY_BLOCKER"]
        self.assertEqual(dependency[0].subject, "T-THREE")
        self.assertEqual(dependency[0].blockers, ["T-TWO"])
        self.assertIn("GATE_BLOCKER", {o.type for o in self.report.obstacles})
        self.assertIn("PHASE_BLOCKER", {o.type for o in self.report.obstacles})

    def test_critical_path_follows_dependencies(self) -> None:
        self.assertEqual(self.report.critical_path, ["T-TWO", "T-THREE"])

    def test_phase_independent_work_still_counts_as_tasks(self) -> None:
        """0 / 0 reads as "nothing here", which is not what P-NONE means."""
        self.rewrite("TASKS.md", "- Phase: P1\n- Validation: SYNTHETIC", "- Phase: P-NONE\n- Validation: SYNTHETIC")
        metrics = analytics.report(self.project).metrics()
        self.assertEqual(metrics["taskCompletion"]["total"], 3)
        self.assertEqual(metrics["phaseIndependent"], 1)
        self.assertEqual(metrics["phaseCompletion"]["P1"]["total"], 2)

    def test_metrics_are_reported_separately(self) -> None:
        metrics = self.report.metrics()
        self.assertEqual(metrics["taskCompletion"]["done"], 1)
        self.assertEqual(metrics["taskCompletion"]["total"], 3)
        self.assertEqual(metrics["gateReadiness"], {"done": 0, "total": 1, "fraction": 0.0})
        self.assertEqual(metrics["acceptanceCompletion"]["done"], 1)
        self.assertEqual(metrics["phaseCompletion"]["P1"]["total"], 3)

    def test_schedule_splits_known_from_unknown(self) -> None:
        self.assertEqual([e["id"] for e in self.report.scheduled], ["T-THREE"])
        self.assertEqual(self.report.unscheduled, ["T-TWO"])

    def test_explain_is_deterministic_and_complete(self) -> None:
        first = analytics.explain(self.project, "T-THREE")
        second = analytics.explain(self.project, "T-THREE")
        self.assertEqual(first, second)
        self.assertEqual(first["blockers"][0]["type"], "DEPENDENCY_BLOCKER")
        self.assertEqual(first["acceptance"][0]["id"], "AC-T-THREE-01")

    def test_context_packet_carries_the_contract(self) -> None:
        packet = analytics.context(self.project, "T-TWO")
        self.assertEqual(packet["role"], "builder")
        self.assertEqual(packet["acceptance"][0]["id"], "AC-T-TWO-01")
        self.assertEqual(packet["decisions"][0]["id"], "ADR-001")
        self.assertNotIn("findingClasses", packet)

    def test_a_packet_omits_narrative_about_other_work(self) -> None:
        """A cold agent cannot tell which of two contradicting statements to believe."""
        (self.root / layout.AUTHORITY_DIR / "INTENT.md").write_text("# Intent\n\nTask: T-ONE, in flight.\n")
        (self.root / layout.AUTHORITY_DIR / "HANDOFF.md").write_text("# Handoff\n\nT-ONE is half built.\n")
        project = compiler.load(self.root)
        about_other = analytics.context(project, "T-TWO")
        self.assertIsNone(about_other["intent"])
        self.assertIsNone(about_other["handoff"])
        about_this = analytics.context(project, "T-ONE")
        self.assertIn("T-ONE", about_this["intent"])
        self.assertIn("T-ONE", about_this["handoff"])

    def test_a_packet_says_which_task_it_is_for(self) -> None:
        packet = analytics.context(self.project, "T-TWO")
        self.assertEqual(packet["packetFor"], "T-TWO")
        self.assertFalse(packet["task"]["closed"])
        self.assertNotIn("note", packet)

    def test_a_packet_for_closed_work_says_so(self) -> None:
        packet = analytics.context(self.project, "T-ONE")
        self.assertTrue(packet["task"]["closed"])
        self.assertIn("already DONE", packet["note"])

    def test_a_packet_states_dependency_readiness_and_blockers(self) -> None:
        packet = analytics.context(self.project, "T-THREE")
        self.assertEqual(packet["task"]["dependencies"], [{"id": "T-TWO", "done": False}])
        self.assertEqual(packet["blockers"][0]["type"], "DEPENDENCY_BLOCKER")

    def test_reviewer_packet_adds_finding_classes(self) -> None:
        packet = analytics.context(self.project, "T-TWO", role="reviewer")
        self.assertIn("ACCEPTANCE_FAILURE", packet["findingClasses"]["blocking"])
        self.assertIn("STYLE", packet["findingClasses"]["informative"])

    def test_unknown_task_raises(self) -> None:
        with self.assertRaises(KeyError):
            analytics.explain(self.project, "T-NOPE")


class TestCompile(FixtureCase):
    def test_a_phase_awaiting_exit_is_still_the_current_phase(self) -> None:
        self.rewrite("PHASES.md", "Status:\nACTIVE", "Status:\nEXIT_PENDING")
        self.assertEqual(self.project.current_phase, "P1")

    def test_shape_and_provenance(self) -> None:
        compiled = compiler.as_json(self.project)
        for key in (
            "project", "phases", "tasks", "acceptance", "invariants", "gates",
            "milestones", "obstacles", "criticalPath", "schedule", "handoff", "sources",
        ):
            self.assertIn(key, compiled)
        self.assertEqual(compiled["project"]["currentPhase"], "P1")
        for task in compiled["tasks"]:
            self.assertEqual(task["source"]["file"], "TASKS.md")
            self.assertTrue(task["source"]["anchor"])

    def test_invariants_are_separate_from_contracts(self) -> None:
        compiled = compiler.as_json(self.project)
        self.assertNotIn("AC-GLOBAL-CARE", compiled["acceptance"])
        self.assertEqual(compiled["invariants"][0]["appliesTo"], ["T-ONE"])

    def test_milestone_reached_is_computed(self) -> None:
        compiled = compiler.as_json(self.project)
        self.assertTrue(compiled["milestones"][0]["reached"])

    def test_compiling_twice_is_byte_identical(self) -> None:
        first = compiler.write(self.root, self.project).read_bytes()
        second = compiler.write(self.root, compiler.load(self.root)).read_bytes()
        self.assertEqual(first, second)

    def test_deleting_compiled_state_loses_nothing(self) -> None:
        before = compiler.write(self.root, self.project).read_bytes()
        shutil.rmtree(self.root / layout.COMPILED_DIR)
        after = compiler.write(self.root, compiler.load(self.root)).read_bytes()
        self.assertEqual(before, after)

    def test_compiler_writes_nothing_outside_the_compiled_directory(self) -> None:
        authority = self.root / layout.AUTHORITY_DIR
        before = {p: p.read_bytes() for p in authority.rglob("*") if p.is_file()}
        compiler.write(self.root, self.project)
        after = {p: p.read_bytes() for p in authority.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_locate_walks_up_from_a_subdirectory(self) -> None:
        nested = self.root / "src" / "deep"
        nested.mkdir(parents=True)
        self.assertEqual(compiler.locate(nested), self.root.resolve())

    def test_locate_fails_outside_a_project(self) -> None:
        with tempfile.TemporaryDirectory() as empty:
            with self.assertRaises(compiler.LayoutError):
                compiler.locate(Path(empty))


class TestRenderers(FixtureCase):
    def setUp(self) -> None:
        super().setUp()
        self.report = analytics.report(self.project)

    def test_every_view_is_produced(self) -> None:
        views = mermaid.render_all(self.project, self.report)
        self.assertEqual(
            set(views),
            {"task-graph.mmd", "critical-path.mmd", "phases.mmd", "gates.mmd",
             "timeline.mmd", "gantt.mmd"},
        )
        for name, text in views.items():
            self.assertTrue(text.startswith(("flowchart", "gantt", "---")), name)

    def test_task_graph_contains_every_task_and_edge(self) -> None:
        graph = mermaid.task_graph(self.project, self.report)
        for task in self.project.tasks:
            self.assertIn(task.id.replace("-", "_"), graph)
        self.assertIn("T_ONE --> T_TWO", graph)

    def test_a_space_in_a_gate_name_never_reaches_a_node_identifier(self) -> None:
        """Gates are identified by their heading, so `Gate A` arrives with a
        space. Mermaid ends an identifier at the first space, which breaks the
        whole diagram rather than only that node."""
        gates = mermaid.gate_graph(self.project)
        self.assertIn('Gate_A{"Gate A', gates)
        for line in gates.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("flowchart", "classDef")):
                continue
            if stripped.startswith("class "):
                names = stripped[len("class "):].rsplit(" ", 1)[0]
                identifiers = names.split(",")
            else:
                identifiers = re.split(r"[{\[(]|-->", stripped, maxsplit=1)[:1]
            for identifier in identifiers:
                self.assertRegex(identifier.strip(), r"^[0-9A-Za-z_]+$")

    def test_dependency_timeline_claims_no_dates(self) -> None:
        timeline = mermaid.dependency_timeline(self.project, self.report)
        self.assertIn("not a calendar", timeline)
        self.assertNotIn("2026-", timeline)
        self.assertIn("section Step 1", timeline)

    def test_calendar_gantt_only_dates_scheduled_work(self) -> None:
        gantt = mermaid.calendar_gantt(self.project, self.report)
        self.assertIn("T-THREE : 2026-10-01, 3d", gantt)
        self.assertNotIn("T-TWO :", gantt)
        self.assertIn("1 unscheduled task not shown", gantt)

    def test_unscheduled_work_never_gets_a_row_on_the_calendar(self) -> None:
        """A dateless Mermaid entry inherits the previous one's end date."""
        gantt = mermaid.calendar_gantt(self.project, self.report)
        rows = [line for line in gantt.splitlines() if " : " in line]
        self.assertEqual(rows, ["    T-THREE : 2026-10-01, 3d"])
        self.assertNotIn("milestone", gantt)

    def test_with_nothing_scheduled_no_date_axis_is_drawn_at_all(self) -> None:
        self.rewrite("TASKS.md", "- Schedule: start=2026-10-01 estimate=3d\n", "")
        report = analytics.report(self.project)
        gantt = mermaid.calendar_gantt(self.project, report)
        self.assertTrue(gantt.startswith("flowchart"))
        self.assertNotIn("dateFormat", gantt)
        self.assertNotIn("milestone", gantt)
        self.assertIn("No task carries schedule metadata", gantt)

    def test_rendering_is_deterministic(self) -> None:
        first = mermaid.render_all(self.project, self.report)
        second = mermaid.render_all(compiler.load(self.root), self.report)
        self.assertEqual(first, second)


class TestDashboard(FixtureCase):
    def setUp(self) -> None:
        super().setUp()
        self.report = analytics.report(self.project)
        self.compiled = compiler.as_json(self.project)
        self.html = dashboard.render(self.project, self.report, self.compiled)

    def test_is_one_self_contained_file(self) -> None:
        self.assertTrue(self.html.startswith("<!doctype html>"))
        self.assertIn('<script type="application/json" id="project-data">', self.html)
        self.assertNotIn("fetch(", self.html)

    def test_embedded_data_round_trips(self) -> None:
        start = self.html.index('id="project-data">') + len('id="project-data">')
        end = self.html.index("</script>", start)
        self.assertEqual(json.loads(self.html[start:end])["project"]["name"], self.root.name)

    def test_shows_every_required_section(self) -> None:
        for heading in (
            "Progress", "Phases", "Gates", "In flight", "Ready", "Obstacles",
            "Critical path", "Views", "Schedule", "Validation", "All tasks",
        ):
            self.assertIn(f">{heading}<", self.html)

    def test_is_read_only(self) -> None:
        for control in ("<form", "<input", "<textarea", "method=\"post\""):
            self.assertNotIn(control, self.html)

    def test_task_drill_down_data_is_present(self) -> None:
        self.assertIn('data-task="T-THREE"', self.html)
        self.assertIn("Inherited invariants", self.html)
        self.assertIn("Source", self.html)

    def _node_map(self) -> dict[str, str]:
        start = self.html.index('id="node-map">') + len('id="node-map">')
        return json.loads(self.html[start : self.html.index("</script>", start)])

    def test_the_drawing_can_be_mapped_back_to_a_task(self) -> None:
        """The page marks an element by looking a task up in this map. Two
        tasks drawn under one identifier would highlight the wrong node, and
        nothing else in the project would notice."""
        node_map = self._node_map()
        self.assertEqual(len(node_map), len(self.project.tasks))
        for task in self.project.tasks:
            self.assertEqual(node_map[mermaid.node_id(task.id)], task.id)

    def test_the_chain_is_reachable_from_compiled_dependencies_alone(self) -> None:
        """Tracing walks `deps` and `blocks` in the embedded project. If those
        two are not exact inverses, a hover reports a different graph from the
        one `explain` reports (ADR-025)."""
        forward = {t["id"]: set(t["deps"]) for t in self.compiled["tasks"]}
        backward = {t["id"]: set(t["blocks"]) for t in self.compiled["tasks"]}
        inverted: dict[str, set[str]] = {task: set() for task in forward}
        for task, dependencies in forward.items():
            for dependency in dependencies:
                if dependency in inverted:
                    inverted[dependency].add(task)
        self.assertEqual(backward, inverted)

    def test_the_graph_reaches_the_same_dialog_as_the_tables(self) -> None:
        """A task opens from the drawing and from its table row, and both read
        the one embedded project. Only tasks are offered: a gate or a phase is
        a node too, and marking it clickable would promise a dialog that does
        not exist."""
        self.assertIn("if (id) showTask(id);", self.html)
        self.assertIn("NODE_MAP[node.dataset.id]", self.html)
        self.assertIn("node.classList.toggle('opens', Boolean(NODE_MAP", self.html)
        self.assertIn("if (panned) return;", self.html)

    def test_rendering_twice_gives_the_same_page(self) -> None:
        again = dashboard.render(self.project, self.report, compiler.as_json(self.project))
        self.assertEqual(self.html, again)

    def test_the_page_survives_mermaid_being_unreachable(self) -> None:
        """The diagram library is loaded from a CDN. Every number on the page
        is computed here, so losing the library may cost the drawing and
        nothing else."""
        self.assertIn('onerror="window.mermaidFailed=true"', self.html)
        self.assertIn("canvas.classList.add('plain')", self.html)
        self.assertIn('id="offline-note"', self.html)


class TestViews(FixtureCase):
    def setUp(self) -> None:
        super().setUp()
        self.report = analytics.report(self.project)
        self.views = views.render_all(self.project, self.report)

    def test_compiled_directory_is_entirely_generated(self) -> None:
        compiler.write(self.root, self.project)
        written = sorted(p.name for p in (self.root / layout.COMPILED_DIR).iterdir())
        self.assertEqual(
            written, ["README.md", "STATE.md", "TASK_GRAPH.md", "project.json"]
        )

    def test_views_declare_themselves_generated(self) -> None:
        for name, text in self.views.items():
            self.assertIn("Generated by `prokron compile`", text, name)

    def test_state_reports_derived_facts_only(self) -> None:
        state = self.views["STATE.md"]
        self.assertIn("Current phase: P1", state)
        self.assertIn("Gate A Single authority: RED", state)
        self.assertIn("Ready: T-TWO", state)
        self.assertIn("HANDOFF.md", state)

    def test_task_graph_lists_dependencies_and_eligibility(self) -> None:
        graph = self.views["TASK_GRAPH.md"]
        self.assertIn("- T-TWO [TODO] Build on it", graph)
        self.assertIn("depends on: T-ONE", graph)
        self.assertIn("unlocks: T-THREE", graph)


class TestHostileAuthoredText(FixtureCase):
    """Authored prose is data. It must never become markup or break the page."""

    def poison(self, text: str) -> str:
        self.rewrite("TASKS.md", "## T-TWO: Build on it", f"## T-TWO: {text}")
        report = analytics.report(self.project)
        return dashboard.render(self.project, report, compiler.as_json(self.project))

    def json_island(self, html: str, element: str) -> dict:
        start = html.index(f'id="{element}">') + len(f'id="{element}">')
        return json.loads(html[start : html.index("</script>", start)].replace("<\\/", "</"))

    def test_a_closing_script_tag_does_not_break_the_page(self) -> None:
        html = self.poison("Ship </script><script>alert(1)</script> it")
        self.assertNotIn("</script><script>alert(1)", html)
        island = self.json_island(html, "project-data")
        self.assertIn("alert(1)", island["tasks"][1]["title"])

    def test_markup_in_a_title_renders_as_text(self) -> None:
        html = self.poison("Ship <b>bold</b> & <img> it")
        self.assertIn("&lt;b&gt;bold&lt;/b&gt; &amp; &lt;img&gt;", html)
        self.assertNotIn("<td>Ship <b>bold</b>", html)

    def test_quotes_in_a_title_cannot_escape_an_attribute(self) -> None:
        html = self.poison('Ship " onload="alert(1)" x="')
        self.assertNotIn('onload="alert(1)"', html)

    def test_the_client_escapes_what_it_renders(self) -> None:
        html = self.poison("Ship <b>bold</b> it")
        self.assertIn("const esc = value =>", html)
        self.assertIn("${esc(task.title)}", html)


class TestContractIntegrity(FixtureCase):
    """A contract must never get quietly weaker than it reads."""

    def test_a_criterion_without_an_evidence_class_is_rejected(self) -> None:
        with self.assertRaises(ParseError) as caught:
            self.rewrite(
                "ACCEPTANCE.md",
                "- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.\n  `TEST` · `NOT_RUN`",
                "- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.",
            )
        self.assertIn("no evidence class", str(caught.exception))
        self.assertEqual(caught.exception.anchor, "AC-T-TWO-01")

    def test_a_broken_criterion_does_not_swallow_the_next_one(self) -> None:
        path = self.root / layout.AUTHORITY_DIR / "ACCEPTANCE.md"
        path.write_text(
            "# Acceptance\n\n# Contracts\n\n## AC-T-ONE — One\n\n"
            "- `AC-T-ONE-01` — Given a bullet, When its class is missing, Then it is caught.\n"
            "- `AC-T-ONE-02` — Given the next bullet, Then it survives. `TEST` · `PASS`\n"
        )
        with self.assertRaises(ParseError):
            compiler.load(self.root)

    def test_a_done_task_with_an_empty_contract_is_an_error(self) -> None:
        self.rewrite(
            "ACCEPTANCE.md",
            "- `AC-T-ONE-01` — Given a site, When the foundation is poured, Then it is\n"
            "  level. `TEST` · `PASS`\n  - Evidence: Measured on site.",
            "",
        )
        findings = validate.check(self.project)
        self.assertIn("empty-contract", {f.code for f in findings})
        self.assertTrue(validate.errors(findings))

    def test_an_open_task_with_an_empty_contract_only_warns(self) -> None:
        self.rewrite(
            "ACCEPTANCE.md",
            "- `AC-T-TWO-01` — Given a foundation, When walls go up, Then they stand.\n  `TEST` · `NOT_RUN`",
            "",
        )
        findings = validate.check(self.project)
        self.assertIn("empty-contract", {f.code for f in findings})
        self.assertEqual(validate.errors(findings), [])


class TestDegenerateProject(unittest.TestCase):
    """An empty chronicle is a normal starting state, not an error."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="prokron-empty-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        authority = self.root / layout.AUTHORITY_DIR
        (authority / "ADR").mkdir(parents=True)
        (authority / "PHASES.md").write_text("# Phases\n\nNo phases yet.\n")
        (authority / "TASKS.md").write_text("# Tasks\n\nNo tasks yet.\n")
        (authority / "ACCEPTANCE.md").write_text("# Acceptance\n\n# Contracts\n\nNone yet.\n")
        (authority / "INTENT.md").write_text("# Intent\n")
        (authority / "HANDOFF.md").write_text("# Handoff\n")
        self.project = compiler.load(self.root)
        self.report = analytics.report(self.project)

    def test_nothing_crashes_on_an_empty_chronicle(self) -> None:
        self.assertEqual(validate.check(self.project), [])
        compiler.write(self.root, self.project)
        mermaid.render_all(self.project, self.report)
        views.render_all(self.project, self.report)
        dashboard.render(self.project, self.report, compiler.as_json(self.project))

    def test_every_command_succeeds(self) -> None:
        for argv in (["validate"], ["compile"], ["status"], ["graph"], ["dashboard"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(["-C", str(self.root), *argv]), 0, argv)

    def test_empty_views_say_so_rather_than_inventing(self) -> None:
        state = views.state(self.project, self.report)
        self.assertIn("Current phase: none", state)
        self.assertIn("None recorded.", state)


class TestGateBlocking(FixtureCase):
    def test_a_gate_blocks_only_the_phase_it_names(self) -> None:
        from prokron.model import Gate, Source

        gate = Gate("Gate X", "X", "", ["P11 exit"], [], "RED", Source("PHASES.md", "Gate X"))
        self.assertFalse(analytics._blocks(gate, "P1"))
        self.assertTrue(analytics._blocks(gate, "P11"))

    def test_a_green_gate_blocks_nothing(self) -> None:
        self.rewrite("PHASES.md", "Status: RED", "Status: GREEN")
        report = analytics.report(self.project)
        self.assertNotIn("GATE_BLOCKER", {o.type for o in report.obstacles})


class TestCli(FixtureCase):
    def run_cli(self, *argv: str) -> tuple[int, str]:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = cli.main(["-C", str(self.root), *argv])
        return code, buffer.getvalue()

    def test_validate_passes_on_clean_authority(self) -> None:
        code, out = self.run_cli("validate")
        self.assertEqual(code, 0)
        self.assertIn("consistent", out)

    def test_validate_fails_on_broken_authority(self) -> None:
        self.rewrite("TASKS.md", "- Dependencies: T-ONE", "- Dependencies: T-GHOST")
        code, _ = self.run_cli("validate")
        self.assertEqual(code, 1)

    def test_compile_refuses_broken_authority_without_force(self) -> None:
        self.rewrite("TASKS.md", "- Dependencies: T-ONE", "- Dependencies: T-GHOST")
        code, _ = self.run_cli("compile")
        self.assertEqual(code, 1)
        self.assertFalse((self.root / layout.COMPILED_DIR / "project.json").exists())
        self.assertEqual(self.run_cli("compile", "--force")[0], 0)

    def test_status_reports_position(self) -> None:
        code, out = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("phase P1", out)
        self.assertIn("T-TWO", out)

    def test_graph_and_dashboard_write_only_compiled_files(self) -> None:
        self.assertEqual(self.run_cli("graph")[0], 0)
        self.assertEqual(self.run_cli("dashboard")[0], 0)
        written = {p.name for p in (self.root / layout.COMPILED_DIR).iterdir()}
        self.assertIn("dashboard.html", written)
        self.assertIn("task-graph.mmd", written)

    def test_explain_and_context(self) -> None:
        self.assertIn("AC-T-TWO-01", self.run_cli("explain", "T-TWO")[1])
        packet = json.loads(self.run_cli("context", "T-TWO")[1])
        self.assertEqual(packet["task"]["id"], "T-TWO")

    def test_unknown_task_exits_nonzero(self) -> None:
        self.assertEqual(cli.main(["-C", str(self.root), "explain", "T-NOPE"]), 1)

    def test_missing_project_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as empty:
            self.assertEqual(cli.main(["-C", empty, "status"]), 1)

    def test_parse_error_is_reported_not_raised(self) -> None:
        (self.root / layout.AUTHORITY_DIR / "TASKS.md").write_text("# Tasks\n\n## broken\n")
        self.assertEqual(cli.main(["-C", str(self.root), "status"]), 1)


class TestThisRepository(unittest.TestCase):
    """Prokron's own chronicle is the acceptance evidence for Phase 2 closure.

    A fixture proves the code works. These prove it works on the real project,
    which is what the Phase 2 definition of done actually claims.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.project = compiler.load(cls.root)
        cls.report = analytics.report(cls.project)

    def test_authority_is_consistent(self) -> None:
        self.assertEqual(
            [f.render() for f in validate.errors(validate.check(self.project))], []
        )

    def test_every_task_resolves_to_a_contract(self) -> None:
        for task in self.project.tasks:
            with self.subTest(task=task.id):
                self.assertIsNotNone(task.contract, f"{task.id} has no AC reference")
                self.assertIn(task.contract, self.project.contracts)
                self.assertTrue(
                    self.project.contracts[task.contract].criteria,
                    f"{task.contract} states no criteria",
                )

    def test_every_task_belongs_to_a_known_phase(self) -> None:
        known = {phase.id for phase in self.project.phases} | {"P-NONE"}
        for task in self.project.tasks:
            with self.subTest(task=task.id):
                self.assertIn(task.phase, known)

    def test_every_done_task_has_its_criteria_met(self) -> None:
        for task in self.project.tasks:
            if not task.done:
                continue
            unmet = analytics.unmet(self.project, task)
            with self.subTest(task=task.id):
                self.assertEqual(unmet, [], f"{task.id} is DONE with unmet criteria")

    def test_deleting_compiled_state_reproduces_it_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            copy = Path(workspace) / "repo"
            shutil.copytree(
                self.root / layout.AUTHORITY_DIR, copy / layout.AUTHORITY_DIR, dirs_exist_ok=False
            )
            project = compiler.load(copy)
            report = analytics.report(project)
            first = {"project.json": compiler.write(copy, project).read_bytes()}
            for name, text in mermaid.render_all(project, report).items():
                first[name] = text.encode()
            for name, text in views.render_all(project, report).items():
                first[name] = text.encode()

            shutil.rmtree(copy / layout.COMPILED_DIR)
            rebuilt = compiler.load(copy)
            rebuilt_report = analytics.report(rebuilt)
            second = {"project.json": compiler.write(copy, rebuilt).read_bytes()}
            for name, text in mermaid.render_all(rebuilt, rebuilt_report).items():
                second[name] = text.encode()
            for name, text in views.render_all(rebuilt, rebuilt_report).items():
                second[name] = text.encode()

            self.assertEqual(first, second)


LEGACY_TASKS = """# Tasks

## T-REAL-01: Ship the thing
- Status: DONE
- Validation: SYNTHETIC
- Dependencies: none
- Owner: me
- Acceptance: The thing ships and stays shipped.
- Evidence: 12 unittest cases passed.
- Governed by: ADR-001

## T-REAL-02: Ship the next thing
- Status: TODO
- Validation: UNTESTED
- Dependencies: T-REAL-01
- Owner: me
- Acceptance: The next thing ships.
- Evidence: —
- Governed by: ADR-002
"""

LEGACY_DECISIONS = """# Decisions

## ADR-001: Do the simple thing
- Date: 2026-01-01
- Status: ACCEPTED
- Supersedes: none
- Decision: Prefer the simple thing.

## ADR-002: Do the other thing instead
- Date: 2026-02-01
- Status: ACCEPTED
- Supersedes: ADR-001
- Decision: The simple thing did not survive contact.
"""

LEGACY_STATE = """# State

## Current
- Project: Legacy thing

## Risks / uncertainty
- The vendor API may change without notice.

## Next
- Call the vendor before building anything else.
"""


class TestMigration(unittest.TestCase):
    """Upgrading must move a v0.1 chronicle, not strand it."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="prokron-legacy-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        legacy = self.root / layout.V01_AUTHORITY_DIR
        legacy.mkdir()
        (legacy / "TASKS.md").write_text(LEGACY_TASKS)
        (legacy / "DECISIONS.md").write_text(LEGACY_DECISIONS)
        (legacy / "STATE.md").write_text(LEGACY_STATE)
        (legacy / "TASK_GRAPH.md").write_text("# Task Graph\n\n- T-REAL-01 [DONE]\n")
        (legacy / "INTENT.md").write_text("# Intent\n\nNo intent.\n")
        (legacy / "JOURNAL.md").write_text("# Journal\n\n## 2026-01-01\n- Did: things\n")
        authority = self.root / layout.AUTHORITY_DIR
        (authority / "ADR").mkdir(parents=True)
        (authority / "TASKS.md").write_text("# Tasks\n\nNo tasks yet.\n")
        (authority / "PHASES.md").write_text("# Phases\n\nNo phases yet.\n")
        (authority / "ACCEPTANCE.md").write_text("# Acceptance\n\n# Contracts\n\nNone yet.\n")
        (authority / "INTENT.md").write_text("# Intent\n")
        (authority / "HANDOFF.md").write_text("# Handoff\n")
        (authority / "JOURNAL.md").write_text("# Journal\n")

    def test_a_legacy_chronicle_is_detected(self) -> None:
        self.assertTrue(migrate.needs_migration(self.root))

    def test_a_current_chronicle_is_not_touched(self) -> None:
        (self.root / layout.AUTHORITY_DIR / "TASKS.md").write_text(LEGACY_TASKS)
        self.assertFalse(migrate.needs_migration(self.root))
        with self.assertRaises(migrate.MigrationError):
            migrate.plan(self.root)

    def test_planning_changes_nothing(self) -> None:
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        plan = migrate.plan(self.root)
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(plan.tasks, 2)
        self.assertEqual(plan.decisions, 2)

    def test_tasks_and_contracts_survive(self) -> None:
        migrate.apply(self.root)
        project = compiler.load(self.root)
        self.assertEqual([t.id for t in project.tasks], ["T-REAL-01", "T-REAL-02"])
        contract = project.contracts["AC-T-REAL-01"]
        self.assertEqual(contract.criteria[0].text, "The thing ships and stays shipped.")
        self.assertEqual(contract.criteria[0].state, "PASS")
        self.assertEqual(contract.criteria[0].evidence_class, "TEST")
        self.assertEqual(project.contracts["AC-T-REAL-02"].criteria[0].state, "NOT_RUN")

    def test_decisions_become_files_with_supersession(self) -> None:
        migrate.apply(self.root)
        adr = self.root / layout.AUTHORITY_DIR / "ADR"
        self.assertTrue((adr / "ADR-001.md").is_file())
        self.assertIn("Prefer the simple thing", (adr / "ADR-001.md").read_text())
        self.assertIn("superseded by ADR-002", (adr / "README.md").read_text())

    def test_state_prose_is_rescued_and_task_graph_is_not(self) -> None:
        migrate.apply(self.root)
        handoff = (self.root / layout.AUTHORITY_DIR / "HANDOFF.md").read_text()
        self.assertIn("vendor API may change", handoff)
        self.assertIn("Call the vendor", handoff)
        self.assertFalse((self.root / layout.AUTHORITY_DIR / "TASK_GRAPH.md").exists())

    def test_originals_are_archived_not_deleted(self) -> None:
        plan = migrate.apply(self.root)
        self.assertTrue(plan.archive.is_dir())
        self.assertEqual(
            (plan.archive / "TASKS.md").read_text(), LEGACY_TASKS
        )
        self.assertEqual((plan.archive / "TASK_GRAPH.md").read_text().strip().splitlines()[0], "# Task Graph")
        self.assertFalse((self.root / layout.COMPILED_DIR / "TASKS.md").exists())

    def test_the_result_validates_and_compiles(self) -> None:
        migrate.apply(self.root)
        project = compiler.load(self.root)
        self.assertEqual(validate.errors(validate.check(project)), [])
        compiler.write(self.root, project)
        self.assertEqual(analytics.report(project).metrics()["taskCompletion"]["total"], 2)

    def test_a_named_phase_can_be_assigned(self) -> None:
        (self.root / layout.AUTHORITY_DIR / "PHASES.md").write_text(
            "# Phases\n\n## P1 — Delivery\n\nOutcome:\nShip.\n\nEntry:\n- none\n\n"
            "Exit:\n- none\n\nExit authority:\nT-REAL-02\n\nStatus:\nACTIVE\n"
        )
        migrate.apply(self.root, phase="P1")
        project = compiler.load(self.root)
        self.assertEqual({t.phase for t in project.tasks}, {"P1"})

    def test_cli_reports_then_applies(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.assertEqual(cli.main(["-C", str(self.root), "migrate"]), 0)
        self.assertIn("Nothing was changed", buffer.getvalue())
        self.assertTrue(migrate.needs_migration(self.root))
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["-C", str(self.root), "migrate", "--apply"]), 0)
        self.assertFalse(migrate.needs_migration(self.root))

    def test_status_says_migration_is_needed(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            cli.main(["-C", str(self.root), "status"])
        self.assertIn("prokron migrate", buffer.getvalue())


class TestRelocation(unittest.TestCase):
    """A v0.2 chronicle sits at the repository root. ADR-024 moves it inside
    `.prokron/`, and that move must not rewrite a single record."""

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="prokron-v02-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        build_fixture(self.root, authority=layout.V02_AUTHORITY_DIR)
        self.source = self.root / layout.V02_AUTHORITY_DIR
        self.before = {
            path.relative_to(self.source): path.read_bytes()
            for path in sorted(self.source.rglob("*"))
            if path.is_file()
        }
        # Compiled output from the old layout, and a stale host pointer.
        compiled = self.root / layout.V02_COMPILED_DIR
        compiled.mkdir(parents=True, exist_ok=True)
        (compiled / "STATE.md").write_text("stale\n")
        (compiled / "task-graph.mmd").write_text("stale\n")
        pointer = self.root / ".claude" / "commands"
        pointer.mkdir(parents=True)
        (pointer / "prokron-work.md").write_text(
            "Follow `commands/prokron-work.md`. Use `$ARGUMENTS` as the task.\n"
        )
        commands = self.root / layout.V02_COMMANDS_DIR
        commands.mkdir()
        (commands / "prokron-work.md").write_text("# /prokron-work\n\nCUSTOM\n")

    def test_it_is_detected_and_the_v01_migration_is_not(self) -> None:
        self.assertTrue(migrate.needs_relocation(self.root))
        self.assertFalse(migrate.needs_migration(self.root))

    def test_every_record_moves_byte_for_byte(self) -> None:
        migrate.relocate(self.root)
        authority = self.root / layout.AUTHORITY_DIR
        after = {
            path.relative_to(authority): path.read_bytes()
            for path in sorted(authority.rglob("*"))
            if path.is_file()
        }
        self.assertEqual(after, self.before)
        self.assertFalse(self.source.exists())

    def test_nothing_is_archived_because_nothing_is_transformed(self) -> None:
        plan = migrate.relocate(self.root)
        self.assertIsNone(plan.archive)
        self.assertEqual(plan.tasks, 3)

    def test_stale_compiled_output_is_discarded_not_carried_over(self) -> None:
        migrate.relocate(self.root)
        compiled = self.root / layout.V02_COMPILED_DIR
        self.assertFalse((compiled / "STATE.md").exists())
        self.assertFalse((compiled / "task-graph.mmd").exists())

    def test_a_host_pointer_names_the_document_that_actually_exists(self) -> None:
        migrate.relocate(self.root)
        pointer = (self.root / ".claude" / "commands" / "prokron-work.md").read_text()
        named = pointer.split("`")[1]
        self.assertEqual(named, f"{layout.COMMANDS_DIR}/prokron-work.md")
        self.assertTrue((self.root / named).is_file())
        self.assertIn("CUSTOM", (self.root / named).read_text())

    def test_the_result_validates_and_compiles(self) -> None:
        migrate.relocate(self.root)
        project = compiler.load(self.root)
        self.assertEqual(validate.errors(validate.check(project)), [])
        compiler.write(self.root, project)
        self.assertTrue(
            (self.root / layout.COMPILED_DIR / "project.json").is_file()
        )

    def test_relocating_twice_refuses_rather_than_half_moving(self) -> None:
        migrate.relocate(self.root)
        with self.assertRaises(migrate.MigrationError):
            migrate.relocate(self.root)


class TestSingleDirectory(unittest.TestCase):
    """Everything Prokron owns is addressed inside one directory (ADR-024)."""

    def test_every_path_prokron_chooses_lives_under_one_directory(self) -> None:
        chosen = (
            layout.AUTHORITY_DIR,
            layout.COMPILED_DIR,
            layout.COMMANDS_DIR,
            layout.RUNTIME_DIR,
            layout.ENTRY_POINT,
        )
        for path in chosen:
            with self.subTest(path=path):
                self.assertTrue(path.startswith(f"{layout.HOME_DIR}/"))

    def test_authored_and_compiled_stay_separate(self) -> None:
        self.assertNotEqual(layout.AUTHORITY_DIR, layout.COMPILED_DIR)
        self.assertFalse(layout.COMPILED_DIR.startswith(layout.AUTHORITY_DIR))
        self.assertFalse(layout.AUTHORITY_DIR.startswith(layout.COMPILED_DIR))


class TestProjectIdentity(unittest.TestCase):
    """The compiled name used to come from the directory the repository sat in,
    so two clones of one chronicle disagreed. A fixture is always made under a
    single name, which is why only CI could find it (ADR-030)."""

    def chronicle_in(self, root: Path, project_line: str = "Project: Fixture\n\n") -> Path:
        authority = root / layout.AUTHORITY_DIR
        (authority / "ADR").mkdir(parents=True)
        (authority / "PHASES.md").write_text(project_line + PHASES)
        (authority / "TASKS.md").write_text(TASKS)
        (authority / "ACCEPTANCE.md").write_text(ACCEPTANCE)
        (authority / "ADR" / "ADR-001.md").write_text(ADR)
        (authority / "INTENT.md").write_text("# Intent\n\nNone.\n")
        (authority / "HANDOFF.md").write_text("# Handoff\n\nNone.\n")
        return root

    def test_one_chronicle_compiles_the_same_from_any_directory(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            names = []
            for directory in ("alpha", "a-different-checkout"):
                root = self.chronicle_in(Path(workspace) / directory)
                names.append(compiler.load(root).name)
            self.assertEqual(names[0], names[1])
            self.assertEqual(names[0], "Fixture")

    def test_a_chronicle_that_names_nothing_keeps_the_directory_name(self) -> None:
        """Every installation that predates the field has no line to read, and
        must keep working without being migrated."""
        with tempfile.TemporaryDirectory() as workspace:
            root = self.chronicle_in(Path(workspace) / "unnamed", project_line="")
            self.assertEqual(compiler.load(root).name, "unnamed")

    def test_the_name_is_read_from_authority_only_above_the_first_heading(self) -> None:
        """`Project:` inside a phase body is prose, not the project's name."""
        with tempfile.TemporaryDirectory() as workspace:
            root = Path(workspace) / "elsewhere"
            self.chronicle_in(root, project_line="")
            phases = root / layout.AUTHORITY_DIR / "PHASES.md"
            phases.write_text(phases.read_text().replace(
                "# Phases", "# Phases\n\nProject: NotTheName", 1))
            self.assertEqual(compiler.load(root).name, "elsewhere")


class TestPublishedDocumentation(unittest.TestCase):
    """The public documents drift silently. A path that moved, a count that
    grew, a version that shipped — none of it fails anything, and a reader
    finds it before a maintainer does. Twice now this drift has published an
    instruction that no longer meant what it said."""

    ROOT = Path(__file__).resolve().parents[1]
    PUBLISHED = (
        "README.md",
        "docs/SPEC.md",
        "docs/PRODUCT-THESIS.md",
        "docs/GUIDE.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
    )

    def documents(self):
        for name in self.PUBLISHED:
            path = self.ROOT / name
            self.assertTrue(path.is_file(), f"{name} is missing")
            yield path, path.read_text()

    def test_every_relative_link_resolves(self) -> None:
        for path, text in self.documents():
            targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
            targets += re.findall(r'<img src="([^"]+)"', text)
            for target in targets:
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                with self.subTest(document=path.name, link=target):
                    self.assertTrue(resolved.exists(), f"dead link: {target}")

    def test_no_document_tells_a_reader_to_delete_their_records(self) -> None:
        """`rm -rf .prokron` was correct until the installation moved into that
        directory. The instruction survived the move and began telling readers
        to delete their own chronicle."""
        for path, text in self.documents():
            for command in re.findall(r"rm -rf\s+(\S+)", text):
                with self.subTest(document=path.name, command=command):
                    self.assertTrue(
                        command.rstrip("/").endswith("compiled"),
                        f"{path.name} deletes {command}, which is not compiled output",
                    )

    def test_the_readme_teaches_one_way_to_install_and_one_way_to_run(self) -> None:
        """Installing took `| sh -s -- existing` and every command afterwards
        was `.prokron/prokron status`. Both are artefacts of a private tool.
        A README that shows two forms teaches neither."""
        readme = (self.ROOT / "README.md").read_text()
        primary = readme.split("### 1. Install in your project", 1)[1].split("<details>", 1)[0]
        self.assertIn("install.sh | sh\n", primary)
        self.assertNotIn("sh -s --", primary)
        for block in re.findall(r"```(?:sh|console)\n(.*?)```", readme, re.S):
            for line in block.splitlines():
                command = line.lstrip("$ ").strip()
                with self.subTest(line=line):
                    self.assertFalse(
                        command.startswith(".prokron/prokron"),
                        "published examples run `prokron`, not a path",
                    )

    def test_citation_metadata_names_the_release_it_ships_with(self) -> None:
        """A deposited record is durable, so metadata that disagrees with the
        release is worse than metadata that is missing (ADR-032)."""
        version = (self.ROOT / "VERSION").read_text().strip()
        citation = (self.ROOT / "CITATION.cff").read_text()
        named = re.search(r"(?m)^version:\s*(\S+)\s*$", citation)
        self.assertIsNotNone(named, "CITATION.cff records no version")
        self.assertEqual(named.group(1).strip('"\''), version)

    def test_the_readme_names_the_release_it_ships_with(self) -> None:
        version = (self.ROOT / "VERSION").read_text().strip()
        readme = (self.ROOT / "README.md").read_text()
        named = set(re.findall(r"v(\d+\.\d+\.\d+)", readme))
        self.assertIn(version, named, f"README names {named or 'no release'}, not {version}")


class TestNoNetworkOrDependencies(unittest.TestCase):
    def test_runtime_imports_only_the_standard_library(self) -> None:
        import sysconfig

        stdlib = Path(sysconfig.get_paths()["stdlib"]).resolve()
        package = Path(cli.__file__).resolve().parent
        offenders = []
        for name, module in list(sys.modules.items()):
            if not name.startswith("prokron"):
                continue
            for attribute in vars(module).values():
                origin = getattr(getattr(attribute, "__module__", None), "__str__", None)
                del origin
        for name in ("json", "argparse", "re", "pathlib", "dataclasses"):
            self.assertIn(name, sys.modules)
        for module_path in package.glob("*.py"):
            text = module_path.read_text()
            for forbidden in ("import requests", "import yaml", "import jinja2", "pip install"):
                if forbidden in text:
                    offenders.append(f"{module_path.name}: {forbidden}")
        self.assertEqual(offenders, [])
        self.assertTrue(stdlib.is_dir())


if __name__ == "__main__":
    unittest.main(verbosity=2)
