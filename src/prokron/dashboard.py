"""Static dashboard generation.

One self-contained HTML file. The compiled project and the Mermaid sources are
embedded, so the page opens straight from the filesystem with no server and no
network. Mermaid renders the diagrams when it is reachable; when it is not, the
page shows the diagram source instead of an empty box.

The dashboard is read-only by construction: it carries no control that writes.
"""

from __future__ import annotations

import html
import json

from .analytics import Report
from .model import Project
from . import mermaid

MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"


def esc(value: object) -> str:
    """Escape authored text before it becomes markup.

    Titles, outcomes and evidence are prose written by people. A stray angle
    bracket or ampersand must render as itself, not as markup.
    """
    return html.escape("" if value is None else str(value), quote=True)


def embed(data: object) -> str:
    """Serialize for a <script> island.

    A `</script>` sequence anywhere in authored text would otherwise close the
    island early and take the whole page down with it.
    """
    return json.dumps(data).replace("</", "<\\/").replace("\u2028", "\\u2028")

_STYLE = """
:root {
  color-scheme: light dark;
  --bg: #fbfbfa; --panel: #ffffff; --ink: #1a1a18; --muted: #6b6b66;
  --line: #e4e4df; --accent: #3a5a40; --warn: #b4690e; --bad: #a4343a;
  --good: #2e7d32; --radius: 10px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16171a; --panel: #1e2024; --ink: #e9e9e4; --muted: #9a9a92;
    --line: #2e3238; --accent: #8fb996; --warn: #e0a458; --bad: #e08585;
    --good: #7fc08a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.55 ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif;
}
main { max-width: 1100px; margin: 0 auto; padding: 32px 16px 96px; }
header.top { border-bottom: 1px solid var(--line); padding-bottom: 20px; margin-bottom: 28px; }
h1 { font-size: 28px; margin: 0 0 6px; letter-spacing: -0.01em; }
h2 { font-size: 15px; text-transform: uppercase; letter-spacing: 0.08em;
     color: var(--muted); margin: 36px 0 14px; font-weight: 600; }
.sub { color: var(--muted); margin: 0; }
.grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
.card { background: var(--panel); border: 1px solid var(--line);
        border-radius: var(--radius); padding: 14px 16px; }
.card .k { color: var(--muted); font-size: 12px; text-transform: uppercase;
           letter-spacing: 0.06em; }
.card .v { font-size: 24px; font-variant-numeric: tabular-nums; margin-top: 4px; }
.bar { height: 4px; background: var(--line); border-radius: 2px; margin-top: 10px; overflow: hidden; }
.bar > i { display: block; height: 100%; background: var(--accent); }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; color: var(--muted); font-weight: 600; font-size: 12px;
     text-transform: uppercase; letter-spacing: 0.05em; padding: 8px 10px;
     border-bottom: 1px solid var(--line); }
td { padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
tbody tr { cursor: pointer; }
tbody tr:hover { background: color-mix(in srgb, var(--accent) 8%, transparent); }
.pill { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px;
        border: 1px solid var(--line); color: var(--muted); white-space: nowrap; }
.pill.DONE, .pill.GREEN, .pill.PASS { color: var(--good);
        border-color: color-mix(in srgb, var(--good) 40%, transparent); }
.pill.WIP { color: var(--warn); border-color: color-mix(in srgb, var(--warn) 40%, transparent); }
.pill.RED, .pill.FAIL { color: var(--bad);
        border-color: color-mix(in srgb, var(--bad) 40%, transparent); }
ul.plain { list-style: none; padding: 0; margin: 0; }
ul.plain li { padding: 9px 0; border-bottom: 1px solid var(--line); }
ul.plain li:last-child { border-bottom: 0; }
code, .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
.diagram { background: var(--panel); border: 1px solid var(--line);
           border-radius: var(--radius); padding: 16px; overflow: auto; }
.diagram pre { margin: 0; white-space: pre-wrap; color: var(--muted); font-size: 12px; }
.tabs { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
.tabs button { font: inherit; font-size: 13px; padding: 5px 12px; cursor: pointer;
  background: var(--panel); color: var(--muted); border: 1px solid var(--line);
  border-radius: 999px; }
.tabs button[aria-selected="true"] { color: var(--ink); border-color: var(--accent); }
dialog { border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel);
  color: var(--ink); max-width: 640px; width: calc(100% - 32px); padding: 0; }
dialog::backdrop { background: rgba(0,0,0,0.45); }
dialog .body { padding: 22px 24px 26px; }
dialog h3 { margin: 0 0 4px; font-size: 19px; }
dialog dt { color: var(--muted); font-size: 12px; text-transform: uppercase;
            letter-spacing: 0.05em; margin-top: 14px; }
dialog dd { margin: 4px 0 0; }
dialog button.close { position: sticky; top: 0; float: right; margin: 10px 12px 0 0;
  background: none; border: 0; color: var(--muted); font-size: 22px; cursor: pointer; }
.note { color: var(--muted); font-size: 13px; }
footer { color: var(--muted); font-size: 12px; margin-top: 48px;
         border-top: 1px solid var(--line); padding-top: 14px; }
"""

_SCRIPT = """
const DATA = JSON.parse(document.getElementById('project-data').textContent);
const DIAGRAMS = JSON.parse(document.getElementById('diagram-data').textContent);
const byId = Object.fromEntries(DATA.tasks.map(t => [t.id, t]));

// Authored prose becomes markup here too, so it is escaped here too.
const esc = value => String(value == null ? '' : value).replace(
  /[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function pill(value) { return `<span class="pill ${esc(value)}">${esc(value)}</span>`; }

function showTask(id) {
  const task = byId[id];
  if (!task) return;
  const contract = DATA.acceptance[task.ac] || { criteria: [], inherits: [] };
  const criteria = contract.criteria.map(c =>
    `<li>${pill(c.state)} <code>${esc(c.id)}</code> <span class="note">${esc(c.class || c.evidenceClass)}</span><br>${esc(c.text)}</li>`
  ).join('') || '<li class="note">No criteria recorded.</li>';
  const deps = task.deps.length
    ? task.deps.map(d => `<code>${esc(d)}</code> ${pill(byId[d] ? byId[d].status : 'MISSING')}`).join('<br>')
    : '<span class="note">None</span>';
  const blocks = task.blocks.length
    ? task.blocks.map(d => `<code>${esc(d)}</code>`).join(', ')
    : '<span class="note">Nothing downstream</span>';
  const obstacles = DATA.obstacles.filter(o => o.subject === id);
  document.querySelector('#detail .body').innerHTML = `
    <h3>${esc(task.id)} — ${esc(task.title)}</h3>
    <p class="sub">${pill(task.status)} ${pill(task.validation)}
       <span class="pill">${esc(task.phase)}</span>
       ${task.owner ? `<span class="pill">${esc(task.owner)}</span>` : ''}</p>
    <dl>
      <dt>Dependencies</dt><dd>${deps}</dd>
      <dt>Blocks</dt><dd>${blocks}</dd>
      <dt>Acceptance — ${esc(task.ac || 'none')}</dt><dd><ul class="plain">${criteria}</ul></dd>
      ${contract.inherits.length ? `<dt>Inherited invariants</dt><dd>${contract.inherits.map(i => `<code>${esc(i)}</code>`).join(', ')}</dd>` : ''}
      ${obstacles.length ? `<dt>Obstacles</dt><dd>${obstacles.map(o => `${pill(o.type)} ${esc(o.detail)}`).join('<br>')}</dd>` : ''}
      <dt>Evidence</dt><dd>${task.evidence ? esc(task.evidence) : '<span class="note">None recorded</span>'}</dd>
      ${task.decisions.length ? `<dt>Decisions</dt><dd>${task.decisions.map(d => `<code>${esc(d)}</code>`).join(', ')}</dd>` : ''}
      <dt>Schedule</dt><dd>${task.schedule ? esc(JSON.stringify(task.schedule)) : '<span class="note">Unscheduled</span>'}</dd>
      <dt>Source</dt><dd><code>${esc(DATA.project.authority)}/${esc(task.source.file)} → ${esc(task.source.anchor)}</code></dd>
    </dl>`;
  document.getElementById('detail').showModal();
}

document.addEventListener('click', event => {
  const row = event.target.closest('tr[data-task]');
  if (row) showTask(row.dataset.task);
});
document.querySelector('#detail .close').addEventListener('click',
  () => document.getElementById('detail').close());

const tabs = document.querySelectorAll('.tabs button');
tabs.forEach(button => button.addEventListener('click', () => {
  tabs.forEach(other => other.setAttribute('aria-selected', String(other === button)));
  const target = document.getElementById('diagram');
  target.removeAttribute('data-processed');
  target.textContent = DIAGRAMS[button.dataset.diagram];
  if (window.mermaid) {
    window.mermaid.run({ nodes: [target] });
  }
}));

if (window.mermaid) {
  window.mermaid.initialize({
    startOnLoad: true,
    theme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'neutral',
  });
} else {
  document.querySelectorAll('.mermaid').forEach(node => {
    const source = document.createElement('pre');
    source.textContent = node.textContent;
    node.replaceWith(source);
  });
  document.getElementById('offline-note').hidden = false;
}
"""


def _metric_card(label: str, progress: dict) -> str:
    percent = round(progress["fraction"] * 100)
    return (
        f'<div class="card"><div class="k">{label}</div>'
        f'<div class="v">{progress["done"]} <span class="note">/ {progress["total"]}</span></div>'
        f'<div class="bar"><i style="width:{percent}%"></i></div></div>'
    )


def render(project: Project, report: Report, compiled: dict) -> str:
    metrics = compiled["metrics"]
    diagrams = mermaid.render_all(project, report)

    cards = "".join(
        [
            _metric_card("Task completion", metrics["taskCompletion"]),
            _metric_card("Acceptance", metrics["acceptanceCompletion"]),
            _metric_card("Validation coverage", metrics["validationCoverage"]),
            _metric_card("Gate readiness", metrics["gateReadiness"]),
            _metric_card("Critical path", metrics["criticalPathCompletion"]),
        ]
    )

    phases = "".join(
        f'<li><strong>{esc(phase["id"])} {esc(phase["name"])}</strong> '
        f'<span class="pill {esc(phase["status"])}">{esc(phase["status"])}</span><br>'
        f'<span class="note">{esc(phase["outcome"])}</span><br>'
        f'<span class="mono">{phase["progress"]["done"]} / {phase["progress"]["total"]} tasks'
        + (f' · exit authority {esc(phase["exitAuthority"])}' if phase["exitAuthority"] else "")
        + "</span></li>"
        for phase in compiled["phases"]
    )

    gates = "".join(
        f'<li><span class="pill {esc(gate["status"])}">{esc(gate["status"])}</span> '
        f'<strong>{esc(gate["id"])}</strong> — {esc(gate["name"])}<br>'
        f'<span class="note">{esc(gate["description"])}</span></li>'
        for gate in compiled["gates"]
    ) or '<li class="note">No gates recorded.</li>'

    def task_rows(ids: list[str]) -> str:
        rows = ""
        for task_id in ids:
            task = project.task(task_id)
            if task is None:
                continue
            rows += (
                f'<tr data-task="{esc(task.id)}"><td><code>{esc(task.id)}</code></td>'
                f"<td>{esc(task.title)}</td><td>{esc(task.phase)}</td>"
                f'<td><span class="pill {esc(task.status)}">{esc(task.status)}</span></td>'
                f'<td><span class="pill">{esc(task.validation)}</span></td></tr>'
            )
        return rows or '<tr><td colspan="5" class="note">Nothing here.</td></tr>'

    obstacles = "".join(
        f'<li><span class="pill">{esc(item["type"])}</span> '
        f'<code>{esc(item["subject"])}</code><br>{esc(item["detail"])}</li>'
        for item in compiled["obstacles"]
    ) or '<li class="note">No obstacles. Everything open is startable.</li>'

    critical = " → ".join(f"<code>{esc(t)}</code>" for t in compiled["criticalPath"]) or (
        '<span class="note">No open work.</span>'
    )

    validation_rows = "".join(
        f"<tr><td>{esc(state)}</td><td>{count}</td></tr>"
        for state, count in sorted(metrics["validationBreakdown"].items())
    )

    tabs = "".join(
        f'<button data-diagram="{name}" aria-selected="{str(index == 0).lower()}">{label}</button>'
        for index, (name, label) in enumerate(
            [
                ("task-graph.mmd", "Task graph"),
                ("critical-path.mmd", "Critical path"),
                ("phases.mmd", "Phases"),
                ("gates.mmd", "Gates"),
                ("timeline.mmd", "Dependency timeline"),
                ("gantt.mmd", "Calendar Gantt"),
            ]
        )
    )

    scheduled = len(compiled["schedule"]["scheduled"])
    unscheduled = len(compiled["schedule"]["unscheduled"])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project.name)} — project state</title>
<style>{_STYLE}</style>
</head>
<body>
<main>
  <header class="top">
    <h1>{esc(project.name)}</h1>
    <p class="sub">
      Current phase <strong>{esc(compiled["project"]["currentPhase"] or "none")}</strong> ·
      {metrics["taskCompletion"]["done"]} of {metrics["taskCompletion"]["total"]} tasks done ·
      compiled from <code>{esc(compiled["project"]["authority"])}/</code>
    </p>
  </header>

  <h2>Progress</h2>
  <div class="grid">{cards}</div>

  <h2>Phases</h2>
  <ul class="plain">{phases}</ul>

  <h2>Gates</h2>
  <ul class="plain">{gates}</ul>

  <h2>In flight</h2>
  <table><thead><tr><th>Task</th><th>Title</th><th>Phase</th><th>Status</th><th>Validation</th></tr></thead>
  <tbody>{task_rows(compiled["wip"])}</tbody></table>

  <h2>Ready</h2>
  <table><thead><tr><th>Task</th><th>Title</th><th>Phase</th><th>Status</th><th>Validation</th></tr></thead>
  <tbody>{task_rows(compiled["ready"])}</tbody></table>

  <h2>Obstacles</h2>
  <ul class="plain">{obstacles}</ul>

  <h2>Critical path</h2>
  <p>{critical}</p>

  <h2>Views</h2>
  <div class="tabs">{tabs}</div>
  <div class="diagram"><div class="mermaid" id="diagram">{esc(diagrams["task-graph.mmd"])}</div></div>
  <p class="note" id="offline-note" hidden>
    Mermaid could not be loaded, so diagram source is shown instead. The page and
    every number on it work offline.
  </p>

  <h2>Schedule</h2>
  <p class="note">
    {scheduled} {"task carries" if scheduled == 1 else "tasks carry"} real schedule
    metadata; {unscheduled} {"is" if unscheduled == 1 else "are"} unscheduled. Dependency
    ordering is shown separately from calendar dates, and no duration is inferred.
  </p>

  <h2>Validation</h2>
  <table><thead><tr><th>Strength</th><th>Tasks</th></tr></thead>
  <tbody>{validation_rows}</tbody></table>

  <h2>All tasks</h2>
  <table><thead><tr><th>Task</th><th>Title</th><th>Phase</th><th>Status</th><th>Validation</th></tr></thead>
  <tbody>{task_rows([t.id for t in project.tasks])}</tbody></table>

  <footer>
    Generated by <code>prokron dashboard</code>. This page is derived and read-only:
    it reports authority and cannot change it. Edit
    <code>{esc(compiled["project"]["authority"])}/</code> and compile again.
  </footer>
</main>

<dialog id="detail"><button class="close" aria-label="Close">×</button><div class="body"></div></dialog>

<script type="application/json" id="project-data">{embed(compiled)}</script>
<script type="application/json" id="diagram-data">{embed(diagrams)}</script>
<script src="{MERMAID_CDN}" onerror="window.mermaidFailed=true"></script>
<script>{_SCRIPT}</script>
</body>
</html>
"""
