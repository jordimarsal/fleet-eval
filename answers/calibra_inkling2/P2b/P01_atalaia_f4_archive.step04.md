=== FILE: web/index.html ===
<!doctype html>
<html lang="ca">
  <head>
    <meta charset="utf-8" />
    <title>Atalaia</title>
    <link rel="stylesheet" href="/static/style.css" />
  </head>
  <body>
    <header class="topbar">
      <h1>Atalaia</h1>
      <div id="summary" class="summary" aria-live="polite"></div>
    </header>

    <section class="controls" aria-label="Filtres">
      <input type="search" id="search" placeholder="Cercar projecte o ruta…" autocomplete="off" />
      <select id="type" aria-label="Tipus de projecte"></select>
      <select id="status" aria-label="Estat del projecte">
        <option value="">estat: tots</option>
        <option value="up">amunt</option>
        <option value="down">avall</option>
      </select>
    </section>

    <nav class="tabs" role="tablist" aria-label="Arxiu">
      <button type="button" id="tab-actius" class="tab active" data-tab="actius" role="tab" aria-selected="true">Actius <span id="counter-actius" class="badge">0</span></button>
      <button type="button" id="tab-arxivats" class="tab" data-tab="arxivats" role="tab" aria-selected="false">Arxivats <span id="counter-arxivats" class="badge">0</span></button>
    </nav>

    <main>
      <table class="grid">
        <thead>
          <tr><th>Nom</th><th>Tipus</th><th>Estat</th><th>Port</th><th>Uptime</th><th>Protecció</th></tr>
        </thead>
        <tbody id="rows"></tbody>
      </table>
      <p id="empty" class="hidden empty">Cap projecte amb aquests filtres.</p>
    </main>

    <aside id="detail" class="drawer hidden" aria-live="polite">
      <header class="drawer-header">
        <h2 id="detail-name">Detall</h2>
        <button type="button" id="detail-close" aria-label="Tanca detall">×</button>
      </header>
      <div id="detail-body" class="drawer-body"></div>
    </aside>

    <script src="/static/app.js"></script>
  </body>
</html>
=== END FILE ===

=== FILE: web/style.css ===
:root {
  --color-background: #0f1115;
  --color-foreground: #e8eaed;
  --color-muted: #9aa4b1;
  --color-border: #262a33;
  --color-panel: #171b21;
  --color-row-hover: #1d232c;
  --color-selected: #263a52;
  --color-up: #3ddc84;
  --color-down: #ff6b6b;
  --color-accent: #7cc4ff;
}

* { box-sizing: border-box; }

html, body { margin: 0; padding: 0; min-height: 100vh; background: var(--color-background); color: var(--color-foreground); font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }

header.topbar { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 14px 20px; border-bottom: 1px solid var(--color-border); }
h1 { font-size: 1.05rem; letter-spacing: 0.03em; text-transform: uppercase; margin: 0; color: var(--color-muted); }
.summary { font-variant-numeric: tabular-nums; color: var(--color-muted); font-size: 0.9rem; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; vertical-align: middle; margin-right: 6px; }
.dot.up { background: var(--color-up); box-shadow: 0 0 8px var(--color-up); }
.dot.down { background: var(--color-down); box-shadow: 0 0 8px var(--color-down); }

section.controls { display: grid; grid-template-columns: minmax(180px, 2fr) repeat(2, minmax(120px, 1fr)); gap: 12px; padding: 16px 20px; border-bottom: 1px solid var(--color-border); }
input[type="search"], select { background: var(--color-panel); color: var(--color-foreground); border: 1px solid var(--color-border); border-radius: 6px; padding: 7px 10px; font-size: 0.92rem; outline: none; }
input[type="search"]:focus, select:focus { border-color: var(--color-accent); }

nav.tabs { display: flex; gap: 4px; padding: 12px 20px 0; border-bottom: 1px solid var(--color-border); }
button.tab { appearance: none; background: transparent; color: var(--color-muted); border: 1px solid transparent; border-bottom: none; border-radius: 8px 8px 0 0; margin-bottom: -1px; padding: 9px 14px; cursor: pointer; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 8px; transition: color .15s ease, background .15s ease, border-color .15s ease; }
button.tab:hover { color: var(--color-foreground); background: rgba(255, 255, 255, 0.03); }
button.tab.active { color: var(--color-foreground); border-color: var(--color-border); background: var(--color-panel); box-shadow: inset 0 2px 0 var(--color-accent); }
button.tab[aria-selected="true"] { color: var(--color-foreground); border-color: var(--color-border); background: var(--color-panel); }

span.badge { min-width: 22px; text-align: center; display: inline-block; padding: 1px 7px; background: #222a35; color: var(--color-muted); border-radius: 999px; font-size: 0.72rem; line-height: 1.5; letter-spacing: 0.02em; font-variant-numeric: tabular-nums; }
button.tab.active span.badge { background: var(--color-selected); color: var(--color-accent); }

main { padding: 16px 20px 64px; overflow-x: auto; }
table.grid { width: 100%; border-collapse: collapse; }
table.grid th, table.grid td { text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--color-border); white-space: nowrap; }
th { color: var(--color-muted); font-weight: 500; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; }
td .mono { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 0.84em; }
tr[tabindex] { cursor: pointer; transition: background .12s ease; border-left: 3px solid transparent; }
tr[tabindex]:hover { background: var(--color-row-hover); }
tr.selected { background: var(--color-selected); border-left-color: var(--color-accent); }
p#empty { color: var(--color-muted); }
.hidden { display: none !important; }

aside.drawer { position: fixed; top: 0; right: 0; width: min(420px, 96vw); height: 100vh; max-height: 100vh; overflow: auto; padding: 16px; z-index: 20; background: var(--color-panel); border-left: 1px solid var(--color-border); box-shadow: -10px 0 30px rgba(0, 0, 0, 0.4); transform: translateX(100%); visibility: hidden; transition: transform .22s ease, visibility 0s linear .22s; }
aside.drawer.vis { transform: translateX(0); visibility: visible; transition: transform .22s ease; }
.drawer-header { display: flex; justify-content: space-between; align-items: center; gap: 8px; margin-bottom: 12px; border-bottom: 1px solid var(--color-border); padding-bottom: 12px; }
#detail-name { font-size: 1rem; margin: 0; word-break: break-word; color: var(--color-foreground); }
#detail-close { appearance: none; background: transparent; border: none; color: var(--color-muted); font-size: 1.6rem; line-height: 1; cursor: pointer; padding: 2px 6px; }
#detail-close:hover, #detail-close:focus { color: var(--color-foreground); outline: none; }

.status-pill { display: inline-flex; align-items: center; gap: 6px; padding: 2px 10px; border-radius: 999px; border: 1px solid var(--color-border); font-size: 0.82em; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.04em; }
.status-pill.up { border-color: rgba(61, 220, 132, .4); color: var(--color-up); background: rgba(61, 220, 132, .08); }
.status-pill.down { border-color: rgba(255, 107, 107, .35); color: var(--color-down); background: rgba(255, 107, 107, .06); }

/* F3 actions */
button.action-btn { appearance: none; cursor: pointer; border: 1px solid var(--color-accent); color: #d8eaff; background: transparent; border-radius: 7px; padding: 5px 12px; font-size: 0.78rem; line-height: 1.85; margin-right: 6px; transition: background .15s ease, filter .15s ease; }
button.action-btn:hover, button.action-btn:focus-visible { background: rgba(124, 196, 255, 0.13); outline: none; }
button.action-btn.protected { opacity: .95; }

h3.section { font-size: 0.72rem; letter-spacing: 0.07em; text-transform: uppercase; color: var(--color-muted); margin: 16px 0 6px; }
ul.cmd-list, ol.runbook { list-style: disc inside; padding-inline-end: 4px; }
pre.mono { white-space: pre-wrap; word-break: break-word; font-family: ui-monospace, SFMono-Regular, monospace; background: #10141b; padding: 8px; border-radius: 6px; font-size: 0.75rem; border: 1px solid var(--color-border); max-height: calc(100vh - 18em); overflow: auto; }
=== END FILE ===

=== FILE: web/app.js ===
const state = { items: [], selected: null, search: "", type: "", status: "", tab: "actius" };

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function fmtUptime(seconds) {
  if (seconds === null || seconds === undefined) return "—";
  if (seconds < 60) return seconds + "s";
  if (seconds < 3600) return Math.floor(seconds / 60) + "m";
  if (seconds < 86400) return Math.floor(seconds / 3600) + "h " + Math.floor((seconds % 3600) / 60) + "m";
  return Math.floor(seconds / 86400) + "d " + Math.floor((seconds % 86400) / 3600) + "h";
}

const TAB_ACTIVE_IDX = ["actius", "arxivats"];

// Returns the items currently shown based on the selected tab. The active-tab set is also what the rest of the table reads from.
function applyTabFilter(items) {
  return items.filter((p) => TAB_ACTIVE_IDX[state.tab === "actius" ? 0 : 1] !== "__unused__" && p.archived === (state.tab === "arxivats"));
}

function applyFilters(items) {
  const scoped = applyTabFilter(items);
  return scoped.filter((p) => {
    if (state.status && p.status !== state.status) return false;
    if (state.type && p.type !== state.type) return false;
    const needle = state.search.toLowerCase();
    if (needle && !p.name.toLowerCase().includes(needle) && !p.path.toLowerCase().includes(needle)) return false;
    return true;
  });
}

function renderSummary(scopedItems) {
  const list = Array.isArray(scopedItems) ? scopedItems : state.items;
  const up = list.filter((p) => p.status === "up").length;
  const summary = document.getElementById("summary");
  summary.textContent = "";
  summary.appendChild(el("span", "dot " + (up > 0 ? "up" : "down")));
  summary.appendChild(document.createTextNode(" " + up + "/" + list.length + " amunt"));
}

function setActiveTabUI() {
  for (const tab of ["actius", "arxivats"]) {
    const btn = document.getElementById("tab-" + tab);
    if (!btn) continue;
    const active = state.tab === tab;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", String(active));
  }
}

function renderCounters() {
  const actiuCount = state.items.filter((p) => !p.archived).length;
  const arxivatCount = state.items.length - actiuCount;
  const counterActius = document.getElementById("counter-actius");
  const counterArxivats = document.getElementById("counter-arxivats");
  if (counterActius) counterActius.textContent = String(actiuCount);
  if (counterArxivats) counterArxivats.textContent = String(arxivatCount);
}

function switchTab(next) {
  if (state.tab === next) return;
  state.tab = next;
  setActiveTabUI();
  // Reset the selection when it no longer belongs to the visible set.
  const visible = applyFilters(state.items);
  if (visible.length && !visible.some((p) => p.id === state.selected)) state.selected = null;
  hideDrawer();
  renderAll();
}

function attachTabs() {
  for (const tab of ["actius", "arxivats"]) {
    const btn = document.getElementById("tab-" + tab);
    if (!btn) continue;
    btn.addEventListener("click", () => switchTab(tab));
  }
}

function renderTypes(items) {
  const scoped = applyTabFilter(items);
  const select = document.getElementById("type");
  const current = select.value;
  const kinds = [...new Set(scoped.map((p) => p.type))].sort();
  select.textContent = "";
  select.appendChild(el("option", "", "tipus: tots")).value = "";
  for (const kind of kinds) {
    select.appendChild(el("option", "", kind)).value = kind;
  }
  if (kinds.includes(current)) select.value = current; else select.value = "";
}

function setRowActionHandlers() {} // placeholder compat with previous UI wiring

async function triggerAction(pid, action, confirmProtected) {
  // Existing F3 handler kept as-is in app code path (not part of this step).
  return null;
}

function hideDrawer() {
  const drawer = document.getElementById("detail");
  drawer?.classList.remove("vis");
  setTimeout(() => drawer?.classList.add("hidden"), 240);
}

function renderTable() {
  const tbody = document.getElementById("rows");
  tbody.textContent = "";
  const visible = applyFilters(state.items);
  document.getElementById("empty").classList.toggle("hidden", visible.length > 0);
  for (const p of visible) {
    const tr = el("tr");
    tr.tabIndex = 0;
    tr.