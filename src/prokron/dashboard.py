"""Static dashboard generation.

One self-contained HTML file. The compiled project and the Mermaid sources are
embedded, so the page opens straight from the filesystem with no server and no
network. Mermaid renders the diagrams when it is reachable; when it is not, the
page shows the diagram source instead of an empty box.

The dashboard is read-only by construction: it carries no control that writes.
Its six tabs, theme, and filters are presentation state kept in the URL hash and
localStorage; none of it reaches authority (ADR-044).
"""

from __future__ import annotations

import html
import json
import re

from .analytics import Report
from .model import STATUSES, VALIDATIONS, Project
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
/* Colours are tokens. The reader's explicit choice sets data-theme on <html>;
   without one the head script copies the operating system preference, and
   without script the media query below does (ADR-044). */
:root, :root[data-theme="light"] {
  color-scheme: light;
  --bg: #f6f6f3; --panel: #ffffff; --panel-raised: #fbfbf9; --ink: #1a1a18;
  --muted: #66665f; --line: #e2e2db; --accent: #3a5a40; --good: #2e7d32;
  --warn: #a8600a; --bad: #a4343a; --shadow: 0 1px 2px rgba(20, 20, 16, 0.05);
  --radius: 10px;
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --bg: #141518; --panel: #1c1e22; --panel-raised: #23262b; --ink: #e8e8e3;
  --muted: #9a9a92; --line: #2e3238; --accent: #8fb996; --good: #7fc08a;
  --warn: #e0a458; --bad: #e08585; --shadow: none;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    color-scheme: dark;
    --bg: #141518; --panel: #1c1e22; --panel-raised: #23262b; --ink: #e8e8e3;
    --muted: #9a9a92; --line: #2e3238; --accent: #8fb996; --good: #7fc08a;
    --warn: #e0a458; --bad: #e08585; --shadow: none;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.55 ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif;
}
main { max-width: 1160px; margin: 0 auto; padding: 28px 16px 96px; }
header.top { display: flex; gap: 16px; align-items: flex-start; justify-content: space-between;
             flex-wrap: wrap; padding-bottom: 16px; }
h1 { font-size: 26px; margin: 0 0 6px; letter-spacing: -0.01em; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em;
     color: var(--muted); margin: 32px 0 12px; font-weight: 600; }
.panel > h2:first-child, .panel > .focus + h2 { margin-top: 24px; }
.sub { color: var(--muted); margin: 0; }
button { font: inherit; color: inherit; }

/* Theme control */
.theme { display: inline-flex; border: 1px solid var(--line); border-radius: 999px;
         padding: 2px; background: var(--panel); }
.theme button { border: 0; background: none; cursor: pointer; font-size: 13px;
                padding: 4px 12px; border-radius: 999px; color: var(--muted); }
.theme button[aria-pressed="true"] { background: var(--panel-raised); color: var(--ink);
                box-shadow: inset 0 0 0 1px var(--line); }

/* Top-level tabs. Without script every panel shows, one after another. */
.toptabs { position: sticky; top: 0; z-index: 5; background: var(--bg);
           display: flex; gap: 2px; overflow-x: auto; white-space: nowrap;
           border-bottom: 1px solid var(--line); margin: 0 -16px; padding: 0 16px;
           scrollbar-width: thin; }
html:not(.js) .toptabs { display: none; }
.toptabs button { border: 0; background: none; cursor: pointer; padding: 11px 14px 10px;
           color: var(--muted); font-size: 14px; border-bottom: 2px solid transparent;
           flex: 0 0 auto; }
.toptabs button:hover { color: var(--ink); }
.toptabs button[aria-selected="true"] { color: var(--ink); border-bottom-color: var(--accent);
           font-weight: 600; }
.toptabs button:focus-visible, .tasklink:focus-visible, tr[data-task]:focus-visible,
summary:focus-visible, .chips button:focus-visible, .theme button:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px; }
html.js .panel { display: none; }
html.js[data-tab="overview"] #panel-overview,
html.js[data-tab="execution"] #panel-execution,
html.js[data-tab="graph"] #panel-graph,
html.js[data-tab="governance"] #panel-governance,
html.js[data-tab="decisions"] #panel-decisions,
html.js[data-tab="tasks"] #panel-tasks { display: block; }
.panel { padding-top: 8px; }
.panel:focus { outline: none; }

/* Cards */
.grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
.card { background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow);
        border-radius: var(--radius); padding: 14px 16px; min-width: 0; }
.card .k { color: var(--muted); font-size: 12px; text-transform: uppercase;
           letter-spacing: 0.06em; }
.card .v { font-size: 24px; font-variant-numeric: tabular-nums; margin-top: 4px; }
.bar { height: 4px; background: var(--line); border-radius: 2px; margin-top: 10px; overflow: hidden; }
.bar > i { display: block; height: 100%; background: var(--accent); }

/* The focus strip answers "where are we" before anything else. */
.focus { display: grid; gap: 12px; margin-top: 18px;
         grid-template-columns: repeat(4, minmax(0, 1fr)); }
.focus .card { border-top: 3px solid var(--accent); }
.focus .card.alert { border-top-color: var(--warn); }
.focus .v { font-size: 16px; line-height: 1.35; overflow-wrap: anywhere; }
.focus .more { color: var(--muted); font-size: 13px; margin-top: 8px; }

/* Phases */
.phases { display: grid; gap: 10px; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); }
.phase { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
         padding: 12px 14px; box-shadow: var(--shadow); min-width: 0; }
.phase.current { border-color: var(--accent); box-shadow: inset 3px 0 0 var(--accent), var(--shadow); }
.phase header { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.phase .outcome { color: var(--muted); font-size: 13px; margin: 6px 0 8px; }

/* Tables */
.tablewrap { overflow: auto; border: 1px solid var(--line); border-radius: var(--radius);
             background: var(--panel); }
.tablewrap.tall { max-height: 70vh; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; color: var(--muted); font-weight: 600; font-size: 12px;
     text-transform: uppercase; letter-spacing: 0.05em; padding: 8px 10px;
     border-bottom: 1px solid var(--line); background: var(--panel); white-space: nowrap; }
.tablewrap th { position: sticky; top: 0; z-index: 1; }
td { padding: 9px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
tbody tr:last-child td { border-bottom: 0; }
tbody tr[data-task] { cursor: pointer; }
tbody tr[data-task]:hover { background: color-mix(in srgb, var(--accent) 8%, transparent); }
td.num { font-variant-numeric: tabular-nums; text-align: right; white-space: nowrap; }

.pill { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px;
        border: 1px solid var(--line); color: var(--muted); white-space: nowrap; }
.pill.DONE, .pill.GREEN, .pill.PASS, .pill.COMPLETE { color: var(--good);
        border-color: color-mix(in srgb, var(--good) 40%, transparent); }
.pill.WIP, .pill.ACTIVE, .pill.EXIT_PENDING { color: var(--warn);
        border-color: color-mix(in srgb, var(--warn) 40%, transparent); }
.pill.RED, .pill.FAIL, .pill.BLOCKED { color: var(--bad);
        border-color: color-mix(in srgb, var(--bad) 40%, transparent); }
.pill.RECONSTRUCTED, .pill.PROPOSED { color: var(--warn);
        border-color: color-mix(in srgb, var(--warn) 40%, transparent); }
.pill.current { color: var(--accent); border-color: var(--accent); }

.tasklink { border: 0; background: none; padding: 0; cursor: pointer; text-align: left;
            color: var(--ink); }
.tasklink:hover { text-decoration: underline; text-underline-offset: 3px; }

ul.plain { list-style: none; padding: 0; margin: 0; }
ul.plain li { padding: 9px 0; border-bottom: 1px solid var(--line); }
ul.plain li:last-child { border-bottom: 0; }
code, .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
.box { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
       padding: 4px 16px; box-shadow: var(--shadow); }

/* Obstacle groups and decisions disclose on demand. */
details.group { background: var(--panel); border: 1px solid var(--line);
                border-radius: var(--radius); margin-bottom: 10px; box-shadow: var(--shadow); }
details.group > summary { cursor: pointer; padding: 10px 16px; font-weight: 600; list-style: none; }
details.group > summary::-webkit-details-marker { display: none; }
details.group > summary::before { content: "▸"; display: inline-block; width: 1em; color: var(--muted); }
details.group[open] > summary::before { content: "▾"; }
details.group > .note, details.group > ul { padding: 0 16px 10px; }
.count { color: var(--muted); font-weight: 400; margin-left: 6px; font-variant-numeric: tabular-nums; }

/* The critical path reads top to bottom. */
ol.chain { list-style: none; margin: 0; padding: 0; }
ol.chain li { position: relative; padding: 8px 12px; background: var(--panel);
              border: 1px solid var(--line); border-radius: 8px; display: flex; gap: 8px;
              align-items: baseline; flex-wrap: wrap; }
ol.chain li + li { margin-top: 22px; }
ol.chain li + li::before { content: "↓"; position: absolute; left: 18px; top: -21px;
              color: var(--muted); line-height: 20px; }
ol.chain li.done { opacity: 0.6; }

/* Filters */
.controls { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 10px; }
.controls input[type="search"], .controls select {
  font: inherit; font-size: 14px; color: var(--ink); background: var(--panel);
  border: 1px solid var(--line); border-radius: 8px; padding: 6px 10px; }
.controls input[type="search"] { flex: 1 1 240px; min-width: 0; }
.chips { display: inline-flex; gap: 4px; flex-wrap: wrap; }
.chips button { cursor: pointer; font-size: 13px; padding: 4px 10px; border-radius: 999px;
  background: var(--panel); color: var(--muted); border: 1px solid var(--line); }
.chips button[aria-pressed="true"] { color: var(--ink); border-color: var(--accent); }
.shown { color: var(--muted); font-size: 13px; margin-left: auto; }

details.adr { border-bottom: 1px solid var(--line); }
details.adr:last-child { border-bottom: 0; }
details.adr > summary { cursor: pointer; padding: 9px 0; display: flex; gap: 8px;
                        align-items: baseline; flex-wrap: wrap; }
details.adr dl { margin: 0 0 10px 18px; }
details.adr dt { color: var(--muted); font-size: 12px; text-transform: uppercase;
                 letter-spacing: 0.05em; margin-top: 6px; }
details.adr dd { margin: 2px 0 0; }

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

@media (max-width: 900px) {
  .focus { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 560px) {
  main { padding-top: 18px; }
  h1 { font-size: 22px; }
  .focus { grid-template-columns: minmax(0, 1fr); }
  .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .phases { grid-template-columns: minmax(0, 1fr); }
  .shown { margin-left: 0; width: 100%; }
  .canvas { height: 60vh; }
}
"""

_SCRIPT = """
const DATA = JSON.parse(document.getElementById('project-data').textContent);
const DIAGRAMS = JSON.parse(document.getElementById('diagram-data').textContent);
const NODE_MAP = JSON.parse(document.getElementById('node-map').textContent);
const NODE_KEY = Object.fromEntries(
  Object.entries(NODE_MAP).map(([drawn, taskId]) => [taskId, drawn]));
const byId = Object.fromEntries(DATA.tasks.map(t => [t.id, t]));
const decisionById = Object.fromEntries(DATA.decisions.map(d => [d.id, d]));

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
      ${task.decisions.length ? `<dt>Decisions</dt><dd>${task.decisions.map(d => `<code>${esc(d)}</code>${decisionById[d] && decisionById[d].origin === 'RECONSTRUCTED' ? ' ' + pill('RECONSTRUCTED') : ''}`).join(', ')}</dd>` : ''}
      <dt>Schedule</dt><dd>${task.schedule ? esc(JSON.stringify(task.schedule)) : '<span class="note">Unscheduled</span>'}</dd>
      <dt>Source</dt><dd><code>${esc(DATA.project.authority)}/${esc(task.source.file)} → ${esc(task.source.anchor)}</code></dd>
    </dl>`;
  document.getElementById('detail').showModal();
}

// A task opens from any element that names it: a table row, a link in the
// focus strip, a step on the critical path. All read the one embedded project.
document.addEventListener('click', event => {
  const opener = event.target.closest('[data-task]');
  if (opener) showTask(opener.dataset.task);
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Enter' && event.key !== ' ') return;
  const row = event.target.closest && event.target.closest('tr[data-task]');
  if (!row) return;
  event.preventDefault();
  showTask(row.dataset.task);
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
  // The zoom controls sit on the canvas. Capturing the pointer for them would
  // deliver their click to the canvas, and the button would never fire.
  if (event.target.closest && event.target.closest('.zoom')) return;
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
// The canvas captures the pointer so a drag can leave it, and a captured
// pointer's click is delivered to the canvas, not the node under it. The node
// is therefore found from where the click landed.
function nodeAt(event) {
  const direct = event.target.closest && event.target.closest('g.node[data-id]');
  if (direct) return direct;
  const under = document.elementFromPoint(event.clientX, event.clientY);
  return under && under.closest ? under.closest('g.node[data-id]') : null;
}
canvas.addEventListener('click', event => {
  if (panned) return;
  const node = nodeAt(event);
  const id = node ? NODE_MAP[node.dataset.id] : null;
  if (id) showTask(id);
});

function markOpenable() {
  stage.querySelectorAll('g.node[data-id]').forEach(node =>
    node.classList.toggle('opens', Boolean(NODE_MAP[node.dataset.id])));
}

// --- Rendering ---------------------------------------------------------
// A diagram is drawn only once its tab is visible: laid out inside a hidden
// panel, every measurement Mermaid takes would be zero (ADR-044).

const graphPanel = document.getElementById('panel-graph');
let currentDiagram = 'task-graph.mmd';
let drawn = false;

function graphVisible() { return graphPanel.getBoundingClientRect().width > 0; }

function mermaidTheme() {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'neutral';
}

function draw() {
  // Mermaid sizes each label from the rendered text. Under a scaled stage it
  // would measure the scaled size and draw every label that much too small.
  view.k = 1; view.x = 0; view.y = 0;
  applyView();
  target.textContent = DIAGRAMS[currentDiagram];
  target.removeAttribute('data-processed');
  traced = null;
  clearTrace();
  drawn = true;
  const ready = () => { openView(); markOpenable(); };
  const done = window.mermaid.run({ nodes: [target] });
  if (done && typeof done.then === 'function') done.then(ready, ready);
  else ready();
}

const tabs = document.querySelectorAll('.tabs button');
tabs.forEach(button => button.addEventListener('click', () => {
  tabs.forEach(other => other.setAttribute('aria-selected', String(other === button)));
  currentDiagram = button.dataset.diagram;
  if (window.mermaid) draw();
  else target.textContent = DIAGRAMS[currentDiagram];
}));

if (window.mermaid) {
  window.mermaid.initialize({ startOnLoad: false, maxTextSize: 200000, theme: mermaidTheme() });
  traceNote.textContent = HINT;
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

function graphShown() {
  if (!window.mermaid) return;
  if (!drawn) draw();
  else if (!adjusted) openView();
}

// --- Top-level tabs ----------------------------------------------------
// Which tab is open is presentation state. It lives in the URL hash, so a
// reload or a shared link opens the same view, and it never touches authority.

const TOP = ['overview', 'execution', 'graph', 'governance', 'decisions', 'tasks'];
const topTabs = [...document.querySelectorAll('.toptabs [role="tab"]')];

function selectTab(name, { focus = false, record = true } = {}) {
  if (!TOP.includes(name)) name = 'overview';
  document.documentElement.dataset.tab = name;
  topTabs.forEach(tab => {
    const on = tab.dataset.tab === name;
    tab.setAttribute('aria-selected', String(on));
    tab.tabIndex = on ? 0 : -1;
    if (on && focus) tab.focus();
  });
  if (record && location.hash !== '#' + name) history.replaceState(null, '', '#' + name);
  if (name === 'graph') graphShown();
}

topTabs.forEach(tab => tab.addEventListener('click', () => selectTab(tab.dataset.tab)));
document.querySelector('.toptabs').addEventListener('keydown', event => {
  const at = topTabs.findIndex(tab => tab.dataset.tab === document.documentElement.dataset.tab);
  const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
  let next = null;
  if (step) next = (at + step + topTabs.length) % topTabs.length;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = topTabs.length - 1;
  if (next === null) return;
  event.preventDefault();
  selectTab(topTabs[next].dataset.tab, { focus: true });
});
addEventListener('hashchange', () => selectTab(location.hash.slice(1), { record: false }));
selectTab(location.hash.slice(1) || 'overview', { record: Boolean(location.hash) });

// --- Theme -------------------------------------------------------------
// The reader's explicit choice is kept in localStorage. Until they make one,
// the operating system preference decides, and keeps deciding if it changes.

const THEME_KEY = 'prokron-theme';
const themeButtons = document.querySelectorAll('[data-theme-choice]');

function storedTheme() {
  try { return localStorage.getItem(THEME_KEY); } catch (error) { return null; }
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeButtons.forEach(button =>
    button.setAttribute('aria-pressed', String(button.dataset.themeChoice === theme)));
  if (!window.mermaid) return;
  window.mermaid.initialize({ startOnLoad: false, maxTextSize: 200000, theme: mermaidTheme() });
  if (drawn && graphVisible()) draw();
  else drawn = false;
}

themeButtons.forEach(button => button.addEventListener('click', () => {
  try { localStorage.setItem(THEME_KEY, button.dataset.themeChoice); } catch (error) {}
  applyTheme(button.dataset.themeChoice);
}));
applyTheme(document.documentElement.dataset.theme || 'light');
const osDark = matchMedia('(prefers-color-scheme: dark)');
const followOs = () => {
  const stored = storedTheme();
  if (stored !== 'light' && stored !== 'dark') applyTheme(osDark.matches ? 'dark' : 'light');
};
if (osDark.addEventListener) osDark.addEventListener('change', followOs);

// --- Filters -----------------------------------------------------------
// Filtering hides rows already on the page. It computes nothing new.

function filterable(rows, controls, countEl, test) {
  const run = () => {
    let shown = 0;
    rows.forEach(row => { const on = test(row); row.hidden = !on; if (on) shown += 1; });
    countEl.textContent = `${shown} of ${rows.length}`;
  };
  controls.forEach(control => control.addEventListener('input', run));
  run();
  return run;
}

const taskRows = [...document.querySelectorAll('#task-registry tbody tr[data-task]')];
const taskSearch = document.getElementById('task-search');
const taskPhase = document.getElementById('task-phase');
const taskStatus = document.getElementById('task-status');
const taskValidation = document.getElementById('task-validation');
filterable(taskRows, [taskSearch, taskPhase, taskStatus, taskValidation],
  document.getElementById('task-shown'), row => {
    const q = taskSearch.value.trim().toLowerCase();
    return (!q || row.dataset.text.includes(q))
      && (!taskPhase.value || row.dataset.phase === taskPhase.value)
      && (!taskStatus.value || row.dataset.status === taskStatus.value)
      && (!taskValidation.value || row.dataset.validation === taskValidation.value);
  });

const adrs = [...document.querySelectorAll('#decision-list details.adr')];
const adrSearch = document.getElementById('decision-search');
const chips = [...document.querySelectorAll('#decision-chips button')];
let adrFilter = '';
const runAdrs = filterable(adrs, [adrSearch], document.getElementById('decision-shown'), item => {
  const q = adrSearch.value.trim().toLowerCase();
  const matches = !adrFilter
    || (adrFilter === 'reconstructed' ? item.dataset.origin === 'RECONSTRUCTED'
                                      : item.dataset.status === adrFilter);
  return matches && (!q || item.dataset.text.includes(q));
});
chips.forEach(chip => chip.addEventListener('click', () => {
  adrFilter = chip.dataset.filter;
  chips.forEach(other => other.setAttribute('aria-pressed', String(other === chip)));
  runAdrs();
}));
"""


def _metric_card(label: str, progress: dict) -> str:
    percent = round(progress["fraction"] * 100)
    return (
        f'<div class="card"><div class="k">{label}</div>'
        f'<div class="v">{progress["done"]} <span class="note">/ {progress["total"]}</span></div>'
        f'<div class="bar"><i style="width:{percent}%"></i></div></div>'
    )


def _pill(value: object, extra: str = "") -> str:
    classes = f"pill {esc(value)} {extra}".strip()
    return f'<span class="{classes}">{esc(value)}</span>'


TOP_TABS = (
    ("overview", "Overview"),
    ("execution", "Execution"),
    ("graph", "Graph"),
    ("governance", "Governance"),
    ("decisions", "Decisions"),
    ("tasks", "All Tasks"),
)

# Obstacles in the order a reader acts on them. Dependency blockers come last
# and are split by whether the work they wait on can start now (ADR-044).
_OBSTACLE_GROUPS = (
    ("ACCEPTANCE_BLOCKER", "Acceptance blockers"),
    ("GATE_BLOCKER", "Gate blockers"),
    ("PHASE_BLOCKER", "Phase blockers"),
    ("VALIDATION_GAP", "Validation gaps"),
    ("SCHEDULE_BLOCKER", "Schedule blockers"),
)
_OBSTACLE_RANK = {kind: rank for rank, (kind, _) in enumerate(_OBSTACLE_GROUPS)}
_OBSTACLE_RANK["DEPENDENCY_BLOCKER"] = len(_OBSTACLE_GROUPS)

# Head script: runs before the stylesheet paints, so the page never flashes
# the wrong theme or the wrong tab. Everything it sets is presentation state.
_BOOT = """(function () {
  var root = document.documentElement, theme = null;
  root.className += ' js';
  try { theme = localStorage.getItem('prokron-theme'); } catch (error) {}
  if (theme !== 'light' && theme !== 'dark') {
    theme = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  root.setAttribute('data-theme', theme);
  var tab = location.hash.slice(1);
  var known = ['overview', 'execution', 'graph', 'governance', 'decisions', 'tasks'];
  root.setAttribute('data-tab', known.indexOf(tab) >= 0 ? tab : 'overview');
})();"""


def _phase_gates(compiled: dict, phase_id: str) -> list[dict]:
    """Gates whose `Blocks` names this phase, read from compiled state."""
    return [
        gate
        for gate in compiled["gates"]
        if any(phase_id in re.split(r"[^A-Za-z0-9\-]+", entry) for entry in gate["blocks"])
    ]


def _main_blocker(compiled: dict) -> dict | None:
    """The obstacle on the work in hand, else the most direct one.

    A selection from compiled obstacles, never a new one: the work in flight
    and the head of the critical path come first, then obstacle type.
    """
    focus = set(compiled["wip"]) | set(compiled["criticalPath"][:1])
    ranked = sorted(
        enumerate(compiled["obstacles"]),
        key=lambda item: (
            item[1]["subject"] not in focus,
            _OBSTACLE_RANK.get(item[1]["type"], 99),
            item[0],
        ),
    )
    return ranked[0][1] if ranked else None


def render(project: Project, report: Report, compiled: dict) -> str:
    metrics = compiled["metrics"]
    diagrams = mermaid.render_all(project, report)
    # The drawing names its nodes by a sanitized identifier. The map back to
    # task identifiers is built here, from the same function that drew them,
    # so the page never has to re-derive the rule (ADR-025).
    node_map = {mermaid.node_id(task.id): task.id for task in project.tasks}
    tasks = {task["id"]: task for task in compiled["tasks"]}
    phases = {phase["id"]: phase for phase in compiled["phases"]}
    current_id = compiled["project"]["currentPhase"]
    current = phases.get(current_id) if current_id else None

    def ref(task_id: str | None) -> str:
        if not task_id:
            return '<span class="note">none</span>'
        task = tasks.get(task_id)
        if task is None:
            return f"<code>{esc(task_id)}</code>"
        return (
            f'<button type="button" class="tasklink" data-task="{esc(task_id)}">'
            f"<code>{esc(task_id)}</code> {esc(task['title'])}</button>"
        )

    def task_rows(ids: list[str], registry: bool = False) -> str:
        rows = ""
        for task_id in ids:
            task = tasks.get(task_id)
            if task is None:
                continue
            filters = (
                f' data-phase="{esc(task["phase"])}" data-status="{esc(task["status"])}"'
                f' data-validation="{esc(task["validation"])}"'
                f' data-text="{esc((task["id"] + " " + task["title"]).lower())}"'
                if registry
                else ""
            )
            rows += (
                f'<tr data-task="{esc(task["id"])}" tabindex="0"{filters}>'
                f'<td><code>{esc(task["id"])}</code></td>'
                f"<td>{esc(task['title'])}</td><td>{esc(task['phase'])}</td>"
                f"<td>{_pill(task['status'])}</td><td>{_pill(task['validation'])}</td></tr>"
            )
        return rows or '<tr><td colspan="5" class="note">Nothing here.</td></tr>'

    table_head = (
        "<thead><tr><th>Task</th><th>Title</th><th>Phase</th><th>Status</th>"
        "<th>Validation</th></tr></thead>"
    )

    # --- Overview: the focus strip ------------------------------------------
    # Future derived signals (attention, risk) belong beside these values; the
    # cards hold none today because the compiled project carries none.
    if current:
        phase_card = (
            f'<div class="v"><code>{esc(current["id"])}</code> · {esc(current["name"])}</div>'
            f'<div class="more">{_pill(current["status"])} '
            f'{current["progress"]["done"]} / {current["progress"]["total"]} tasks done</div>'
        )
    else:
        phase_card = '<div class="v">No phase is active</div>'

    wip = compiled["wip"]
    upcoming = [t for t in compiled["criticalPath"] if t not in wip and t in tasks]
    if wip:
        active_card = f'<div class="v">{ref(wip[0])}</div>'
        if len(wip) > 1:
            active_card += f'<div class="more">and {len(wip) - 1} more in flight</div>'
    elif compiled["ready"]:
        active_card = (
            '<div class="v">Nothing in flight</div>'
            f'<div class="more">Ready to start: {ref(compiled["ready"][0])}</div>'
        )
    else:
        active_card = '<div class="v">Nothing in flight</div>'
    if upcoming:
        active_card += f'<div class="more">Next on the critical path: {ref(upcoming[0])}</div>'

    blocker = _main_blocker(compiled)
    if blocker:
        blocker_card = (
            f'<div class="v">{ref(blocker["subject"])}</div>'
            f'<div class="more">{_pill(blocker["type"])} {esc(blocker["detail"])}</div>'
        )
        if len(compiled["obstacles"]) > 1:
            blocker_card += (
                f'<div class="more">{len(compiled["obstacles"]) - 1} more obstacles under Execution</div>'
            )
    else:
        blocker_card = '<div class="v">No obstacles</div>'

    if current:
        exit_task = tasks.get(current["exitAuthority"] or "")
        gate_card = (
            f'<div class="v">{ref(current["exitAuthority"])}</div>'
            + (
                f'<div class="more">Exit authority for {esc(current["id"])} · {_pill(exit_task["status"])}</div>'
                if exit_task
                else f'<div class="more">{esc(current["id"])} names no exit authority</div>'
            )
        )
        phase_gates = _phase_gates(compiled, current["id"])
        if phase_gates:
            gate_card += '<div class="more">' + " ".join(
                f'{_pill(g["status"])} {esc(g["id"])}' for g in phase_gates
            ) + "</div>"
    else:
        gate_card = '<div class="v">No phase exit pending</div>'

    focus = (
        '<div class="focus">'
        f'<div class="card"><div class="k">Current phase</div>{phase_card}</div>'
        f'<div class="card"><div class="k">In flight</div>{active_card}</div>'
        f'<div class="card{" alert" if blocker else ""}"><div class="k">Main blocker</div>{blocker_card}</div>'
        f'<div class="card"><div class="k">Next gate</div>{gate_card}</div>'
        "</div>"
    )

    cards = "".join(
        [
            _metric_card("Task completion", metrics["taskCompletion"]),
            _metric_card("Acceptance", metrics["acceptanceCompletion"]),
            _metric_card("Validation coverage", metrics["validationCoverage"]),
            _metric_card("Gate readiness", metrics["gateReadiness"]),
            _metric_card("Critical path", metrics["criticalPathCompletion"]),
        ]
    )

    phase_cards = "".join(
        f'<article class="phase{" current" if phase["id"] == current_id else ""}">'
        f'<header><strong><code>{esc(phase["id"])}</code> {esc(phase["name"])}</strong> '
        f'{_pill(phase["status"])}'
        + (' <span class="pill current">Current</span>' if phase["id"] == current_id else "")
        + "</header>"
        f'<div class="outcome">{esc(phase["outcome"])}</div>'
        f'<div class="mono">{phase["progress"]["done"]} / {phase["progress"]["total"]} tasks'
        + (f' · exit authority {esc(phase["exitAuthority"])}' if phase["exitAuthority"] else "")
        + f'</div><div class="bar"><i style="width:{round(phase["progress"]["fraction"] * 100)}%"></i></div>'
        "</article>"
        for phase in compiled["phases"]
    ) or '<p class="note">No phases recorded.</p>'

    # --- Execution ---------------------------------------------------------
    def obstacle_item(item: dict) -> str:
        return (
            f'<li>{_pill(item["type"])} {ref(item["subject"])}<br>'
            f'<span class="note">{esc(item["detail"])}</span></li>'
        )

    blocked = set(compiled["blocked"])
    groups = []
    for kind, label in _OBSTACLE_GROUPS:
        items = [o for o in compiled["obstacles"] if o["type"] == kind]
        if items:
            groups.append((label, items, True, ""))
    dependency = [o for o in compiled["obstacles"] if o["type"] == "DEPENDENCY_BLOCKER"]
    direct = [o for o in dependency if any(b not in blocked for b in o["blockers"])]
    downstream = [o for o in dependency if o not in direct]
    if direct:
        groups.append(("Waiting on work that can move now", direct, True, ""))
    if downstream:
        groups.append((
            "Waiting on work that is itself blocked", downstream, False,
            '<p class="note">Each of these clears once the obstacles above do.</p>',
        ))
    known_kinds = {kind for kind, _ in _OBSTACLE_GROUPS} | {"DEPENDENCY_BLOCKER"}
    other = [o for o in compiled["obstacles"] if o["type"] not in known_kinds]
    if other:
        groups.append(("Other obstacles", other, True, ""))
    obstacles = "".join(
        f'<details class="group"{" open" if opened else ""}><summary>{esc(label)}'
        f'<span class="count">{len(items)}</span></summary>{note}'
        f'<ul class="plain">{"".join(obstacle_item(o) for o in items)}</ul></details>'
        for label, items, opened, note in groups
    ) or '<p class="note">No obstacles. Everything open is startable.</p>'

    critical = "".join(
        f'<li class="{"done" if tasks.get(t, {}).get("status") == "DONE" else ""}">'
        f'{_pill(tasks[t]["status"]) if t in tasks else ""} {ref(t)}</li>'
        for t in compiled["criticalPath"]
    )
    critical = (
        f'<ol class="chain">{critical}</ol>' if critical
        else '<p class="note">No open work.</p>'
    )

    # --- Graph -------------------------------------------------------------
    diagram_tabs = "".join(
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

    # --- Governance --------------------------------------------------------
    gates = "".join(
        f'<li>{_pill(gate["status"])} <strong>{esc(gate["id"])}</strong> — {esc(gate["name"])}'
        + (f' <span class="note">blocks {esc(", ".join(gate["blocks"]))}</span>' if gate["blocks"] else "")
        + f'<br><span class="note">{esc(gate["description"])}</span></li>'
        for gate in compiled["gates"]
    ) or '<li class="note">No gates recorded.</li>'
    total_tasks = len(compiled["tasks"])
    validation_rows = "".join(
        f"<tr><td>{_pill(state)}</td><td class=\"num\">{count}</td>"
        f'<td class="num">{(count / total_tasks * 100) if total_tasks else 0:.0f}%</td>'
        f'<td style="width:40%"><div class="bar"><i style="width:{(count / total_tasks * 100) if total_tasks else 0:.1f}%"></i></div></td></tr>'
        for state, count in sorted(metrics["validationBreakdown"].items())
    )

    # --- Decisions ---------------------------------------------------------
    all_decisions = compiled["decisions"]
    superseded_by: dict[str, list[str]] = {}
    for decision in all_decisions:
        for earlier in decision["supersedes"]:
            superseded_by.setdefault(earlier, []).append(decision["id"])
    reconstructed_count = sum(1 for d in all_decisions if d["origin"] == "RECONSTRUCTED")

    # A reconstructed decision was inferred after the fact (ADR-037). It is
    # labelled wherever it appears, so it is never read as a record of a
    # decision the project watched being made.
    def decision_item(decision: dict) -> str:
        reconstructed = decision["origin"] == "RECONSTRUCTED"
        detail = []
        if decision["supersedes"]:
            detail.append(("Supersedes", ", ".join(decision["supersedes"])))
        if superseded_by.get(decision["id"]):
            detail.append(("Superseded by", ", ".join(superseded_by[decision["id"]])))
        if decision["affects"]:
            detail.append(("Affects", ", ".join(decision["affects"])))
        if reconstructed:
            detail.append(("Inferred from", decision["evidence"] or "nothing cited"))
        detail.append((
            "Source", f'{compiled["project"]["authority"]}/{decision["source"]["file"]}'
        ))
        body = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in detail)
        return (
            f'<details class="adr" data-status="{esc(decision["status"])}"'
            f' data-origin="{esc(decision["origin"])}"'
            f' data-text="{esc((decision["id"] + " " + decision["title"]).lower())}">'
            f'<summary><code>{esc(decision["id"])}</code> {_pill(decision["status"])}'
            + (' <span class="pill RECONSTRUCTED">RECONSTRUCTED</span>' if reconstructed else "")
            + f" {esc(decision['title'])}</summary><dl>{body}</dl></details>"
        )

    decision_items = "".join(decision_item(d) for d in all_decisions)
    statuses = sorted({d["status"] for d in all_decisions})
    chip_values = [("", "All")] + [(s, s) for s in statuses]
    if reconstructed_count:
        chip_values.append(("reconstructed", "Reconstructed"))
    decision_chips = "".join(
        f'<button type="button" data-filter="{esc(value)}" aria-pressed="{str(value == "").lower()}">'
        f"{esc(label)}</button>"
        for value, label in chip_values
    ) if len(chip_values) > 2 else ""
    decision_summary = (
        f'{len(all_decisions)} {"decision" if len(all_decisions) == 1 else "decisions"}'
        + (f" · {reconstructed_count} reconstructed" if reconstructed_count else "")
    )

    # --- All tasks ---------------------------------------------------------
    phase_order = [p["id"] for p in compiled["phases"]]
    present_phases = sorted(
        {t["phase"] for t in compiled["tasks"]},
        key=lambda p: (phase_order.index(p) if p in phase_order else len(phase_order), p),
    )
    present_statuses = [s for s in STATUSES if any(t["status"] == s for t in compiled["tasks"])]
    present_validations = [
        v for v in VALIDATIONS if any(t["validation"] == v for t in compiled["tasks"])
    ]

    def select(element_id: str, label: str, values: list[str]) -> str:
        options = "".join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in values)
        return (
            f'<select id="{element_id}" aria-label="{label}">'
            f'<option value="">{label}: all</option>{options}</select>'
        )

    tab_buttons = "".join(
        f'<button type="button" role="tab" id="tab-{name}" data-tab="{name}"'
        f' aria-controls="panel-{name}" aria-selected="{str(name == "overview").lower()}"'
        f' tabindex="{0 if name == "overview" else -1}">{label}</button>'
        for name, label in TOP_TABS
    )

    def panel(name: str, body: str) -> str:
        return (
            f'<section class="panel" id="panel-{name}" role="tabpanel"'
            f' aria-labelledby="tab-{name}" tabindex="0">{body}</section>'
        )

    overview = panel("overview", f"""
  {focus}
  <h2>Progress</h2>
  <div class="grid">{cards}</div>
  <h2>Phases</h2>
  <div class="phases">{phase_cards}</div>
""")
    execution = panel("execution", f"""
  <h2>In flight</h2>
  <div class="tablewrap"><table>{table_head}<tbody>{task_rows(compiled["wip"])}</tbody></table></div>
  <h2>Ready</h2>
  <div class="tablewrap"><table>{table_head}<tbody>{task_rows(compiled["ready"])}</tbody></table></div>
  <h2>Obstacles</h2>
  {obstacles}
  <h2>Critical path</h2>
  {critical}
""")
    graph = panel("graph", f"""
  <h2>Views</h2>
  <div class="tabs">{diagram_tabs}</div>
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
""")
    governance = panel("governance", f"""
  <h2>Gates</h2>
  <div class="box"><ul class="plain">{gates}</ul></div>
  <h2>Validation</h2>
  <div class="tablewrap"><table><thead><tr><th>Strength</th><th>Tasks</th><th>Share</th><th></th></tr></thead>
  <tbody>{validation_rows}</tbody></table></div>
  <p class="note">Validation strength is separate from completion: a task can be DONE and still UNTESTED.</p>
""")
    decisions = panel("decisions", f"""
  <h2>Decisions</h2>
  <div class="controls">
    <input type="search" id="decision-search" placeholder="Search decision ID or title…" aria-label="Search decisions">
    <div class="chips" id="decision-chips" role="group" aria-label="Filter decisions">{decision_chips}</div>
    <span class="shown" id="decision-shown" aria-live="polite">{decision_summary}</span>
  </div>
  <div class="box" id="decision-list">{decision_items or '<p class="note">No decisions recorded.</p>'}</div>
""")
    registry = panel("tasks", f"""
  <h2>All tasks</h2>
  <div class="controls">
    <input type="search" id="task-search" placeholder="Search task ID or title…" aria-label="Search tasks">
    {select("task-phase", "Phase", present_phases)}
    {select("task-status", "Status", present_statuses)}
    {select("task-validation", "Validation", present_validations)}
    <span class="shown" id="task-shown" aria-live="polite">{total_tasks} of {total_tasks}</span>
  </div>
  <div class="tablewrap tall"><table id="task-registry">{table_head}
  <tbody>{task_rows([t.id for t in project.tasks], registry=True)}</tbody></table></div>
""")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(project.name)} — project state</title>
<script>{_BOOT}</script>
<style>{_STYLE}</style>
</head>
<body>
<main>
  <header class="top">
    <div>
      <h1>{esc(project.name)}</h1>
      <p class="sub">
        Current phase <strong>{esc(compiled["project"]["currentPhase"] or "none")}</strong> ·
        {metrics["taskCompletion"]["done"]} of {metrics["taskCompletion"]["total"]} tasks done ·
        compiled from <code>{esc(compiled["project"]["authority"])}/</code>
      </p>
    </div>
    <div class="theme" role="group" aria-label="Theme">
      <button type="button" data-theme-choice="light" aria-pressed="false">Light</button>
      <button type="button" data-theme-choice="dark" aria-pressed="false">Dark</button>
    </div>
  </header>

  <nav class="toptabs" role="tablist" aria-label="Report sections">{tab_buttons}</nav>
{overview}
{execution}
{graph}
{governance}
{decisions}
{registry}
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
