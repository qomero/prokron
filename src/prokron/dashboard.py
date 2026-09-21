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
           border-radius: var(--radius); position: relative; overflow: hidden; }
.diagram pre { margin: 0; white-space: pre-wrap; color: var(--muted); font-size: 12px; }
.canvas { position: relative; height: clamp(380px, 64vh, 780px); overflow: hidden;
          cursor: grab; touch-action: none; }
.canvas.grabbing { cursor: grabbing; }
/* Without a rendered diagram the canvas holds diagram source, which is read by
   scrolling like any other text. */
.canvas.plain { height: auto; overflow: auto; padding: 16px; cursor: auto; }
.canvas.plain .stage { position: static; transform: none !important; }
.canvas.plain .zoom, .canvas.plain .trace { display: none; }
.stage { position: absolute; top: 0; left: 0; transform-origin: 0 0; }
.stage svg { max-width: none !important; display: block; }
.zoom { position: absolute; right: 10px; top: 10px; z-index: 2; display: flex; gap: 2px;
        align-items: center; background: var(--panel); border: 1px solid var(--line);
        border-radius: 999px; padding: 3px; }
.zoom button { font: inherit; font-size: 13px; line-height: 1; width: 26px; height: 24px;
        cursor: pointer; background: none; border: 0; color: var(--muted); border-radius: 999px; }
.zoom button.wide { width: auto; padding: 0 10px; font-size: 12px; }
.zoom button:hover { color: var(--ink); }
.zoom .level { font-size: 12px; color: var(--muted); min-width: 42px; text-align: center; }
.trace { position: absolute; left: 12px; bottom: 10px; z-index: 2; font-size: 12px;
         color: var(--muted); pointer-events: none; max-width: calc(100% - 140px);
         overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
/* Tracing dims everything outside the hovered task's chain. Opacity is used
   rather than colour so a task's status colour still reads. */
.stage.tracing g.node { opacity: 0.12; }
.stage.tracing g.node.chain { opacity: 1; }
.stage.tracing g.node.focus > rect, .stage.tracing g.node.focus > polygon,
.stage.tracing g.node.focus > path { stroke-width: 3px; }
.stage.tracing .flowchart-link { opacity: 0.06; }
.stage.tracing .flowchart-link.chain { opacity: 1; }
.stage.tracing g.cluster { opacity: 0.45; }
/* Only nodes that are tasks open anything, so only those look clickable. */
.stage g.node.opens { cursor: pointer; }
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
const NODE_MAP = JSON.parse(document.getElementById('node-map').textContent);
const NODE_KEY = Object.fromEntries(
  Object.entries(NODE_MAP).map(([drawn, taskId]) => [taskId, drawn]));
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

// --- The diagram canvas ------------------------------------------------
// A 48-task graph drawn to fit a panel is too small to read, so the diagram
// is given its natural size and the canvas is zoomed and panned instead.

const canvas = document.getElementById('canvas');
const stage = document.getElementById('stage');
const target = document.getElementById('diagram');
const levelText = document.getElementById('zoom-level');
const traceNote = document.getElementById('trace-note');
const view = { k: 1, x: 0, y: 0 };
let adjusted = false;   // the reader has zoomed or panned; stop re-fitting
let drag = null;
let panned = false;
let traced = null;

function applyView() {
  stage.style.transform =
    `translate(${view.x}px, ${view.y}px) scale(${view.k})`;
  levelText.textContent = Math.round(view.k * 100) + '%';
}

function naturalSize() {
  const svg = stage.querySelector('svg');
  if (!svg) return null;
  // Mermaid ships the drawing at width:100% with a max-width, which is what
  // shrinks it. The viewBox carries the size it was actually laid out at.
  const box = svg.viewBox && svg.viewBox.baseVal;
  const width = box && box.width ? box.width : svg.getBoundingClientRect().width;
  const height = box && box.height ? box.height : svg.getBoundingClientRect().height;
  if (!width || !height) return null;
  svg.style.maxWidth = 'none';
  svg.style.width = width + 'px';
  svg.style.height = height + 'px';
  return { width, height };
}

function fitScale(size, box) {
  return Math.min(box.width / size.width, box.height / size.height, 1);
}

function fit() {
  const size = naturalSize();
  if (!size) return;
  const box = canvas.getBoundingClientRect();
  if (!box.width || !box.height) return;
  view.k = fitScale(size, box);
  view.x = (box.width - size.width * view.k) / 2;
  view.y = (box.height - size.height * view.k) / 2;
  adjusted = false;
  applyView();
}

// Fitting a large graph into a panel is what made it unreadable in the first
// place, so a diagram that only fits below this is opened at a legible scale,
// centred on the work that matters now, with Fit one click away.
const LEGIBLE = 0.6;

function openingTask() {
  // What is in flight, else what can start, else the critical path.
  const candidates = [...DATA.wip, ...DATA.ready, ...DATA.criticalPath];
  return candidates.find(id => byId[id]) || null;
}

function centreOn(taskId) {
  const node = taskId && stage.querySelector(
    `g.node[data-id="${NODE_KEY[taskId] || ''}"]`);
  if (!node) return false;
  const nodeBox = node.getBoundingClientRect();
  const canvasBox = canvas.getBoundingClientRect();
  view.x += canvasBox.left + canvasBox.width / 2 - (nodeBox.left + nodeBox.width / 2);
  view.y += canvasBox.top + canvasBox.height / 2 - (nodeBox.top + nodeBox.height / 2);
  applyView();
  return true;
}

function openView() {
  const size = naturalSize();
  if (!size) return;
  const box = canvas.getBoundingClientRect();
  if (!box.width || !box.height) return;
  const fitted = fitScale(size, box);
  if (fitted >= LEGIBLE) { fit(); return; }
  view.k = LEGIBLE;
  view.x = (box.width - size.width * view.k) / 2;
  view.y = (box.height - size.height * view.k) / 2;
  adjusted = false;
  applyView();
  centreOn(openingTask());
}

function zoomAt(factor, cx, cy) {
  const next = Math.min(8, Math.max(0.05, view.k * factor));
  const ratio = next / view.k;
  view.x = cx - (cx - view.x) * ratio;
  view.y = cy - (cy - view.y) * ratio;
  view.k = next;
  adjusted = true;
  applyView();
}

function zoomCentre(factor) {
  const box = canvas.getBoundingClientRect();
  zoomAt(factor, box.width / 2, box.height / 2);
}

document.querySelectorAll('.zoom button').forEach(button =>
  button.addEventListener('click', () => {
    if (button.dataset.zoom === 'fit') fit();
    else zoomCentre(button.dataset.zoom === 'in' ? 1.25 : 1 / 1.25);
  }));

// Plain wheel keeps scrolling the page. A trackpad pinch arrives as
// ctrl+wheel, so pinch-to-zoom works without claiming ordinary scrolling.
canvas.addEventListener('wheel', event => {
  if (!event.ctrlKey && !event.metaKey) return;
  event.preventDefault();
  const box = canvas.getBoundingClientRect();
  zoomAt(Math.exp(-event.deltaY / 240),
         event.clientX - box.left, event.clientY - box.top);
}, { passive: false });

canvas.addEventListener('pointerdown', event => {
  if (event.button !== 0) return;
  drag = { x: event.clientX - view.x, y: event.clientY - view.y,
           fromX: event.clientX, fromY: event.clientY };
  panned = false;
  canvas.setPointerCapture(event.pointerId);
  canvas.classList.add('grabbing');
});
canvas.addEventListener('pointermove', event => {
  if (!drag) return;
  // A click carries a little movement with it. Past this the gesture was a
  // pan, and releasing over a task must not open it.
  if (Math.abs(event.clientX - drag.fromX) > 3 ||
      Math.abs(event.clientY - drag.fromY) > 3) panned = true;
  view.x = event.clientX - drag.x;
  view.y = event.clientY - drag.y;
  adjusted = true;
  applyView();
});
['pointerup', 'pointercancel'].forEach(name =>
  canvas.addEventListener(name, () => {
    drag = null;
    canvas.classList.remove('grabbing');
  }));
canvas.addEventListener('dblclick', fit);
// Re-open rather than re-fit: fitting is what made the graph unreadable,
// and openView() is the rule for what a fresh view should show.
addEventListener('resize', () => { if (!adjusted) openView(); });

// --- Tracing a dependency chain ----------------------------------------
// The chain comes from the compiled dependencies, never from the drawing, so
// a highlight and `prokron explain` cannot disagree (ADR-025).

function chainOf(id) {
  const chain = new Set([id]);
  for (const direction of ['deps', 'blocks']) {
    const queue = [id];
    while (queue.length) {
      const task = byId[queue.pop()];
      if (!task) continue;
      for (const next of task[direction]) {
        if (!chain.has(next)) { chain.add(next); queue.push(next); }
      }
    }
  }
  return chain;
}

function edgeEnd(element, prefix) {
  for (const name of element.classList) {
    if (name.startsWith(prefix)) return NODE_MAP[name.slice(prefix.length)];
  }
  return null;
}

function trace(id) {
  const chain = chainOf(id);
  const task = byId[id];
  stage.classList.add('tracing');
  stage.querySelectorAll('g.node[data-id]').forEach(node => {
    const taskId = NODE_MAP[node.dataset.id];
    node.classList.toggle('chain', chain.has(taskId));
    node.classList.toggle('focus', taskId === id);
  });
  stage.querySelectorAll('.flowchart-link').forEach(edge => {
    const from = edgeEnd(edge, 'LS-');
    const to = edgeEnd(edge, 'LE-');
    edge.classList.toggle('chain', chain.has(from) && chain.has(to));
  });
  const others = chain.size - 1;
  traceNote.textContent = `${id} — ${task ? task.title : ''} · ` +
    (others ? `${others} connected task${others === 1 ? '' : 's'}` : 'nothing connected');
}

function clearTrace() {
  stage.classList.remove('tracing');
  stage.querySelectorAll('.chain, .focus').forEach(
    element => element.classList.remove('chain', 'focus'));
  traceNote.textContent = HINT;
}

const HINT = 'Hover a task to trace its chain · click it for detail · drag to pan · ' +
  'pinch or \u2318/Ctrl-scroll to zoom';

canvas.addEventListener('mousemove', event => {
  if (drag) return;
  const node = event.target.closest && event.target.closest('g.node[data-id]');
  const id = node ? NODE_MAP[node.dataset.id] : null;
  if (id === traced) return;
  traced = id;
  if (id) trace(id); else clearTrace();
});
canvas.addEventListener('mouseleave', () => { traced = null; clearTrace(); });

// The drawing is only how the element is found. What opens is the same dialog
// the task tables open, reading the same compiled project (ADR-025).
canvas.addEventListener('click', event => {
  if (panned) return;
  const node = event.target.closest && event.target.closest('g.node[data-id]');
  const id = node ? NODE_MAP[node.dataset.id] : null;
  if (id) showTask(id);
});

function markOpenable() {
  stage.querySelectorAll('g.node[data-id]').forEach(node =>
    node.classList.toggle('opens', Boolean(NODE_MAP[node.dataset.id])));
}

// --- Rendering ---------------------------------------------------------

function draw() {
  target.removeAttribute('data-processed');
  traced = null;
  clearTrace();
  const ready = () => { openView(); markOpenable(); };
  const done = window.mermaid.run({ nodes: [target] });
  if (done && typeof done.then === 'function') done.then(ready, ready);
  else ready();
}

const tabs = document.querySelectorAll('.tabs button');
tabs.forEach(button => button.addEventListener('click', () => {
  tabs.forEach(other => other.setAttribute('aria-selected', String(other === button)));
  target.textContent = DIAGRAMS[button.dataset.diagram];
  if (window.mermaid) draw();
}));

if (window.mermaid) {
  window.mermaid.initialize({
    startOnLoad: false,
    maxTextSize: 200000,
    theme: matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'neutral',
  });
  traceNote.textContent = HINT;
  draw();
} else {
  // Nothing below depends on a diagram: the page shows the source and every
  // number on it still reports.
  canvas.classList.add('plain');
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
    # The drawing names its nodes by a sanitized identifier. The map back to
    # task identifiers is built here, from the same function that drew them,
    # so the page never has to re-derive the rule (ADR-025).
    node_map = {mermaid.node_id(task.id): task.id for task in project.tasks}

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
  <div class="diagram">
    <div class="canvas" id="canvas">
      <div class="stage" id="stage"><div class="mermaid" id="diagram">{esc(diagrams["task-graph.mmd"])}</div></div>
      <div class="zoom">
        <button type="button" data-zoom="out" aria-label="Zoom out">&minus;</button>
        <span class="level" id="zoom-level">100%</span>
        <button type="button" data-zoom="in" aria-label="Zoom in">+</button>
        <button type="button" class="wide" data-zoom="fit">Fit</button>
      </div>
      <div class="trace" id="trace-note"></div>
    </div>
  </div>
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
<script type="application/json" id="node-map">{embed(node_map)}</script>
<script src="{MERMAID_CDN}" onerror="window.mermaidFailed=true"></script>
<script>{_SCRIPT}</script>
</body>
</html>
"""
