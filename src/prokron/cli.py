"""The prokron command.

Every subcommand reads `.prokron/chronicle/` and writes, at most, inside
`.prokron/compiled/`. Nothing here needs a network or a model provider.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import analytics, compile as compiler, dashboard, layout, mermaid, migrate, validate
from .model import Project
from .parse import ParseError

VERSION = layout.version()


def _load(root: Path) -> Project:
    return compiler.load(root)


def _fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def _report_findings(findings: list, stream=sys.stdout) -> None:
    for finding in findings:
        print(f"  {finding.render()}", file=stream)


def _stale_compiled(root: Path) -> str | None:
    """The version that wrote the compiled views, when it is not this one.

    An upgrade replaces the runtime and, before ADR-031, left the generated
    views alone. A page written by an older release looks like a release that
    lost a feature, so the mismatch is reported rather than left to be noticed.
    """
    written = root / compiler.COMPILED_DIR / "project.json"
    if not written.is_file():
        return None
    try:
        recorded = json.loads(written.read_text())["project"].get("generatorVersion")
    except (ValueError, KeyError, OSError):
        return None
    return None if recorded in (None, VERSION) else str(recorded)


def _version_key(version: str) -> tuple[int, ...] | None:
    parts = version.split(".")
    return tuple(int(part) for part in parts) if all(p.isdigit() for p in parts) else None


def _newer(version: str | None) -> bool:
    """Whether views were written by a runtime newer than this one."""
    if not version:
        return False
    theirs, ours = _version_key(version), _version_key(VERSION)
    return bool(theirs and ours and theirs > ours)


def _refuse_newer(root: Path, args: argparse.Namespace) -> int | None:
    """An older runtime rewriting a newer one's views would silently drop
    whatever the newer one knows how to show (ADR-041)."""
    stale = _stale_compiled(root)
    if not _newer(stale) or args.force:
        return None
    print(
        f"Refusing to overwrite views written by prokron {stale}; this is {VERSION}.\n"
        "Upgrade this installation, or pass --force to write them anyway.",
        file=sys.stderr,
    )
    return 1


def cmd_validate(root: Path, args: argparse.Namespace) -> int:
    project = _load(root)
    findings = validate.check(project)
    errors = validate.errors(findings)
    warnings = [f for f in findings if f.severity == "warning"]
    if errors:
        print(f"{len(errors)} error{'s' if len(errors) != 1 else ''}:")
        _report_findings(errors, sys.stderr)
    if warnings and not args.quiet:
        print(f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''}:")
        _report_findings(warnings)
    if not findings:
        print(f"{root.name}: authority is consistent.")
    return 1 if errors else 0


def cmd_compile(root: Path, args: argparse.Namespace) -> int:
    refused = _refuse_newer(root, args)
    if refused is not None:
        return refused
    project = _load(root)
    errors = validate.errors(validate.check(project))
    if errors and not args.force:
        print(f"Refusing to compile with {len(errors)} validation errors:", file=sys.stderr)
        _report_findings(errors, sys.stderr)
        print("Fix the authority, or pass --force to compile anyway.", file=sys.stderr)
        return 1
    target = compiler.write(root, project)
    print(f"Wrote {target.relative_to(root)}")
    return 0


def cmd_graph(root: Path, args: argparse.Namespace) -> int:
    refused = _refuse_newer(root, args)
    if refused is not None:
        return refused
    project = _load(root)
    report = analytics.report(project)
    compiled = root / compiler.COMPILED_DIR
    compiled.mkdir(parents=True, exist_ok=True)
    for name, text in mermaid.render_all(project, report).items():
        (compiled / name).write_text(text)
        print(f"Wrote {compiler.COMPILED_DIR}/{name}")
    return 0


def cmd_dashboard(root: Path, args: argparse.Namespace) -> int:
    refused = _refuse_newer(root, args)
    if refused is not None:
        return refused
    project = _load(root)
    report = analytics.report(project)
    compiled = compiler.as_json(project)
    compiler.write(root, project)
    target = root / compiler.COMPILED_DIR / "dashboard.html"
    target.write_text(dashboard.render(project, report, compiled))
    print(f"Wrote {target.relative_to(root)}")
    if args.open:
        import webbrowser

        webbrowser.open(target.as_uri())
    return 0


def cmd_status(root: Path, args: argparse.Namespace) -> int:
    project = _load(root)
    report = analytics.report(project)
    metrics = report.metrics()

    print(f"{project.name} — phase {project.current_phase or 'none'}")
    stale = _stale_compiled(root)
    if _newer(stale):
        print(
            f"\n  Compiled views were written by prokron {stale}, which is newer "
            f"than this {VERSION}.\n  Upgrade this installation before compiling; "
            "an older runtime would rewrite them.\n"
        )
    elif stale:
        print(
            f"\n  Compiled views were written by prokron {stale}; this is "
            f"{VERSION}.\n  Run `prokron compile && prokron graph && prokron "
            "dashboard` to refresh them.\n"
        )
    if migrate.needs_relocation(root):
        print(
            f"\n  A chronicle is still at {migrate.layout.V02_AUTHORITY_DIR}/ and "
            "unread. Run `prokron migrate`.\n"
        )
    elif migrate.needs_migration(root):
        print(
            "\n  A v0.1 chronicle is present and unread. Run `prokron migrate`.\n"
        )
    print(
        f"  tasks        {metrics['taskCompletion']['done']} / "
        f"{metrics['taskCompletion']['total']}"
    )
    print(
        f"  acceptance   {metrics['acceptanceCompletion']['done']} / "
        f"{metrics['acceptanceCompletion']['total']} criteria passing"
    )
    print(
        f"  validation   {metrics['validationCoverage']['done']} / "
        f"{metrics['validationCoverage']['total']} reviewed or verified"
    )
    # Done and checked are different claims; keep the gap on the same screen.
    unreviewed = sum(
        1
        for task in project.tasks
        if task.done and task.validation not in ("AI_REVIEWED", "HUMAN_VERIFIED")
    )
    if unreviewed:
        print(
            f"               {unreviewed} done task{'' if unreviewed == 1 else 's'} "
            "not reviewed or verified"
        )
    print(
        f"  gates        {metrics['gateReadiness']['done']} / "
        f"{metrics['gateReadiness']['total']} green"
    )
    for phase in project.phases:
        progress = report.phase_progress[phase.id]
        print(f"  {phase.id:<12} {progress} · {phase.status}")
    independent = metrics["phaseIndependent"]
    if independent:
        print(f"  {'no phase':<12} {independent} task{'' if independent == 1 else 's'}")
    print(f"\n  WIP       {', '.join(report.wip) or 'none'}")
    print(f"  Ready     {', '.join(report.ready) or 'none'}")
    print(f"  Blocked   {', '.join(report.blocked) or 'none'}")
    if report.critical_path:
        print(f"  Next      {report.critical_path[0]} (critical path)")
    if report.obstacles:
        print(f"\n  {len(report.obstacles)} obstacles:")
        for obstacle in report.obstacles[: args.limit]:
            print(f"    {obstacle.type:<20} {obstacle.detail}")
        if len(report.obstacles) > args.limit:
            print(f"    ... and {len(report.obstacles) - args.limit} more")
    return 0


def cmd_explain(root: Path, args: argparse.Namespace) -> int:
    project = _load(root)
    try:
        detail = analytics.explain(project, args.task)
    except KeyError:
        return _fail(f"No such task: {args.task}")
    if args.json:
        print(json.dumps(detail, indent=2))
        return 0
    print(f"{detail['id']} — {detail['title']}")
    print(f"  phase {detail['phase']} · {detail['status']} · {detail['validation']}")
    if detail["dependencies"]:
        print("\n  Dependencies")
        for dependency in detail["dependencies"]:
            mark = "✓" if dependency["done"] else "○"
            print(f"    {mark} {dependency['id']}")
    print("\n  Acceptance")
    for criterion in detail["acceptance"] or []:
        mark = {"PASS": "✓", "FAIL": "✗", "NOT_RUN": "○"}[criterion["state"]]
        print(f"    {mark} {criterion['id']} [{criterion['class']}] {criterion['text'][:90]}")
    if detail["invariants"]:
        print(f"\n  Inherited invariants: {', '.join(detail['invariants'])}")
    if detail["blocks"]:
        print(f"  Blocks: {', '.join(detail['blocks'])}")
    if detail["blockers"]:
        print("\n  Blockers")
        for blocker in detail["blockers"]:
            print(f"    {blocker['type']}: {blocker['detail']}")
    print(f"\n  Evidence: {detail['evidence'] or 'none recorded'}")
    print(f"  Source:   {detail['source']['file']} → {detail['source']['anchor']}")
    return 0


def cmd_context(root: Path, args: argparse.Namespace) -> int:
    project = _load(root)
    try:
        packet = analytics.context(project, args.task, args.role)
    except KeyError:
        return _fail(f"No such task: {args.task}")
    print(json.dumps(packet, indent=2))
    return 0


def cmd_migrate(root: Path, args: argparse.Namespace) -> int:
    # A v0.2 chronicle at the repository root is only in the wrong place, so it
    # is relocated before a v0.1 one is rewritten. A project needing both is
    # handled by running this twice, which is clearer than one compound move.
    relocating = migrate.needs_relocation(root)
    try:
        if relocating:
            result = migrate.relocate(root) if args.apply else migrate.relocate_plan(root)
        elif args.apply:
            result = migrate.apply(root, args.phase)
        else:
            result = migrate.plan(root, args.phase)
    except migrate.MigrationError as error:
        return _fail(str(error))
    print(result.render())
    if not args.apply:
        print("\nNothing was changed. Re-run with --apply to perform it.")
        return 0
    if result.archive is None:
        print("\nRelocated. Every record moved unchanged.")
    else:
        print(f"\nMigrated. Originals archived in {result.archive.name}/")
    findings = validate.errors(validate.check(_load(root)))
    if findings:
        print(f"\n{len(findings)} validation errors remain:", file=sys.stderr)
        _report_findings(findings, sys.stderr)
        print("The records are migrated; fix these, then run compile.", file=sys.stderr)
        return 1
    compiler.write(root, _load(root))
    print("Authority validates. Compiled state written.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prokron",
        description="Compile and report a repository's project chronicle.",
    )
    parser.add_argument("--version", action="version", version=f"prokron {VERSION}")
    parser.add_argument("-C", "--directory", default=None, help="run as if started here")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("validate", help="check authority for structural errors")
    check.add_argument("--quiet", action="store_true", help="errors only")
    check.set_defaults(handler=cmd_validate)

    build = subparsers.add_parser(
        "compile", help=f"write {compiler.COMPILED_DIR}/project.json"
    )
    build.add_argument(
        "--force", action="store_true", help="compile despite errors or newer views"
    )
    build.set_defaults(handler=cmd_compile)

    state = subparsers.add_parser("status", help="print current project state")
    state.add_argument("--limit", type=int, default=8, help="obstacles to show")
    state.set_defaults(handler=cmd_status)

    graph = subparsers.add_parser("graph", help="write Mermaid views")
    graph.add_argument("--force", action="store_true", help="overwrite views from a newer runtime")
    graph.set_defaults(handler=cmd_graph)

    board = subparsers.add_parser("dashboard", help="write the static dashboard")
    board.add_argument("--open", action="store_true", help="open it in a browser")
    board.add_argument("--force", action="store_true", help="overwrite views from a newer runtime")
    board.set_defaults(handler=cmd_dashboard)

    why = subparsers.add_parser("explain", help="explain one task")
    why.add_argument("task")
    why.add_argument("--json", action="store_true")
    why.set_defaults(handler=cmd_explain)

    move = subparsers.add_parser(
        "migrate", help="move a chronicle written under an earlier layout"
    )
    move.add_argument("--apply", action="store_true", help="perform it; otherwise report only")
    move.add_argument("--phase", default="P-NONE", help="phase to assign migrated tasks")
    move.set_defaults(handler=cmd_migrate)

    packet = subparsers.add_parser("context", help="emit an agent context packet")
    packet.add_argument("task")
    packet.add_argument("--role", choices=("builder", "reviewer"), default="builder")
    packet.set_defaults(handler=cmd_context)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = compiler.locate(Path(args.directory) if args.directory else None)
    except compiler.LayoutError as error:
        return _fail(str(error))
    try:
        return args.handler(root, args)
    except ParseError as error:
        return _fail(f"Cannot read authority: {error}")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
