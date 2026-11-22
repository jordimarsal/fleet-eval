=== FILE: web/index.html ===
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atalaia</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <header>
    <h1>Atalaia</h1>
    <div id="summary" class="summary"></div>
  </header>

  <main>
    <section class="controls">
      <input type="text" id="search" placeholder="Cerca projectes...">
      <select id="type"></select>
    </section>

    <nav class="tabs">
      <button id="tab-actius" class="tab active">Actius <span class="count"></span></button>
      <button id="tab-arxivats" class="tab">Arxivats <span class="count"></span></button>
    </nav>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nom</th>
            <th>Tipus</th>
            <th>Estat</th>
            <th>Porta</th>
            <th>Uptime</th>
          </tr>
        </thead>
        <tbody id="rows"></tbody>
        <tbody id="arxivats-rows" class="hidden"></tbody>
      </table>
      <div id="empty" class="empty hidden">No hi ha projectes.</div>
    </div>
  </main>

  <aside id="drawer" class="drawer hidden">
    <button class="close-btn">&times;</button>
    <div id="drawer-content"></div>
  </aside>

  <script src="/static/app.js"></script>
</body>
</html>
=== END FILE ===

=== FILE: web/style.css ===
:root {
  --color-background: #f4f4f9;
  --color-surface: #ffffff;
  --color-text: #333333;
  --color-primary: #007bff;
  --color-accent: #6c757d;
  --color-up: #28a745;
  --color-down: #dc3545;
  --border-radius: 8px;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: var(--color-background);
  color: var(--color-text);
  margin: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  padding: 1rem 2rem;
  background: var(--color-surface);
  box-shadow: var(--shadow);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 { margin: 0; font-size: 1.5rem; }

.summary { font-weight: bold; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; }
.dot.up { background-color: var(--color-up); }
.dot.down { background-color: var(--color-down); }

main { padding: 2rem; flex: 1; overflow-y: auto; max-width: 1200px; margin: 0 auto; width: 100%; box-sizing: border-box; }

.controls { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
input, select { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
#search { flex: 1; }

.tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; border-bottom: 2px solid #ddd; }
.tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  cursor: pointer;
  font-weight: bold;
  color: var(--color-accent);
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}
.tab.active { color: var(--color-primary); border-bottom-color: var(--color-primary); }
.tab .count { font-size: 0.8rem; opacity: 0.6; margin-left: 4px; }

.table-container { background: var(--color-surface); border-radius: var(--border-radius); box-shadow: var(--shadow); overflow: hidden; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th, td { padding: 1rem; border-bottom: 1px solid #eee; }
th { background: #fafafa; font-weight: 600; }
tr:hover { background: #f9f9f9; cursor: pointer; }
tr.selected { background: #e7f1ff; }
.hidden { display: none !important; }

.empty { padding: 3rem; text-align: center; color: var(--color-accent); }

.drawer {
  position: fixed;
  right: 0; top: 0; bottom: 0;
  width: 400px;
  background: var(--color-surface);
  box-shadow: -5px 0 15px rgba(0,0,0,0.1);
  padding: 2rem;
  z-index: 100;
  overflow-y: auto;
}
.drawer.hidden { transform: translateX(100%); transition: transform 0.3s ease; }
.close-btn { position: absolute; top: 1rem; right: 1rem; font-size: 1.5rem; border: none; background: none; cursor: pointer; }

.action-btn {
  display: block; width: 100%; padding: 0.6rem; margin-bottom: 0.5rem;
  border: 1px solid #ddd; border-radius: 4px; background: white;
  text-align: left; cursor: pointer;
}
.action-btn:hover { background: #f0f0f0; }

.archive-section { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; }
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
  return Math.floor(seconds / 86400) + "d " + Math.floor((seconds % 3600) / 3600) + "h";
}

async function fetchData() {
  const res = await fetch("/api/projects");
  state.items = await res.json();
  renderSummary();
  renderTypes();
  updateCounts();
  renderTable();
}

async function toggleArchive(pid, currentStatus) {
  const action = currentStatus ? "unarchive" : "archive";
  const res = await fetch(`/api/projects/${pid}/${action}`, { method: "POST" });
  if (res.ok) {
    await fetchData();
    if (state.selected === pid) {
      // If we archived the selected item, close drawer or re-select? 
      // For simplicity, just refresh.
    }
  }
}

async function triggerAction(pid, actionName) {
  const res = await fetch(`/api/projects/${pid}/${actionName}`, { method: "POST" });
  if (res.ok) {
    await fetchData();
  } else {
    alert("Error executing action");
  }
}

function applyFilters(items) {
  return items.filter((p) => {
    // Tab filtering
    if (state.tab === "actius" && p.archived) return false;
    if (state.tab === "arxivats" && !p.archived) return false;
    
    if (state.status && p.status !== state.status) return false;
    if (state.type && p.type !== state.type) return false;
    
    const needle = state.search.toLowerCase();
    if (needle && !p.name.toLowerCase().includes(needle) && !p.path.toLowerCase().includes(needle)) return false;
    return true;
  });
}

function renderSummary() {
  const up = state.items.filter((p) => p.status === "up").length;
  const summary = document.getElementById("summary");
  summary.textContent = "";
  summary.appendChild(el("span", "dot " + (up > 0 ? "up" : "down")));
  summary.appendChild(document.createTextNode(" " + up + "/" + state.items.length + " amunt"));
}

function renderTypes(items = state.items) {
  const select = document.getElementById("type");
  const current = select.value;
  const kinds = [...new Set(items.map((p) => p.type))].sort();
  select.textContent = "";
  select.appendChild(el("option", "", "tipus: tots")).value = "";
  for (const kind of kinds) {
    select.appendChild(el("option", "", kind)).value = kind;
  }
  if (kinds.includes(current)) select.value = current;
}

function updateCounts() {
  const actiusCount = state.items.filter(p => !p.archived).length;
  const arxivatsCount = state.items.filter(p => p.archived).length;
  
  const tabActius = document.getElementById("tab-actius");
  const tabArxivats = document.getElementById("tab-arxivats");
  
  tabActius.querySelector(".count").textContent = `(${actiusCount})`;
  tabArxivats.querySelector(".count").textContent = `(${arxivatsCount})`;
}

function renderTable() {
  const rowsActius = document.getElementById("rows");
  const rowsArxivats = document.getElementById("arxivats-rows");
  const emptyMsg = document.getElementById("empty");
  
  rowsActius.textContent = "";
  rowsArxivats.textContent = "";
  
  const visible = applyFilters(state.items);
  emptyMsg.classList.toggle("hidden", visible.length > 0);

  // Toggle visibility of the two tbody containers based on active tab
  if (state.tab === "actius") {
    rowsActius.classList.remove("hidden");
    rowsArxivats.classList.add("hidden");
  } else {
    rowsActius.classList.add("hidden");
    rowsArxivats.classList.remove("hidden");
  }

  for (const p of visible) {
    const tr = el("tr");
    tr.tabIndex = 0;
    tr.dataset.id = p.id;
    if (p.id === state.selected) tr.classList.add("selected");

    tr.onclick = () => selectProject(p.id);

    tr.appendChild(el("td", "", p.name));
    tr.appendChild(el("td", "", p.type));
    tr.appendChild(el("td", "", p.status));
    tr.appendChild(el("td", "", p.port || "—"));
    tr.appendChild(el("td", "", fmtUptime(p.uptime)));

    if (state.tab === "actius") {
      rowsActius.appendChild(tr);
    } else {
      rowsArxivats.appendChild(tr);
    }
  }
}

async function selectProject(pid) {
  state.selected = pid;
  const res = await fetch(`/api/projects/${pid}`);
  const data = await res.json();
  renderTable(); // update selection highlight
  showDrawer(data);
}

function showDrawer(project) {
  const drawer = document.getElementById("drawer");
  const content = document.getElementById("drawer-content");
  content.textContent = "";
  
  const title = el("h2", "", project.name);
  content.appendChild(title);

  const info = el("div", "info");
  info.innerHTML = `
    <p><strong>ID:</strong> ${project.id}</p>
    <p><strong>Path:</strong> ${project.path}</p>
    <p><strong>Type:</strong> ${project.type}</p>
    <p><strong>Status:</strong> ${project.status}</p>
  `;
  content.appendChild(info);

  // Actions
  if (project.actions && project.actions.length > 0) {
    const actionHeader = el("h3", "", "Accions");
    content.appendChild(actionHeader);
    for (const act of project.actions) {
      const btn = el("button", "action-btn", act);
      btn.onclick = () => {
        if (window.confirm(`Executar ${act}?`)) triggerAction(project.id, act);
      };
      content.appendChild(btn);
    }
  }

  // Archive section
  const archiveSection = el("div", "archive-section");
  const archiveBtn = el("button", "action-btn", project.archived ? "Desarxivar" : "Arxivar");
  archiveBtn.onclick = () => toggleArchive(project.id, project.archived);
  archiveSection.appendChild(archiveBtn);
  content.appendChild(archiveSection);

  drawer.classList.remove("hidden");
}

// Event Listeners
document.getElementById("search").oninput = (e) => {
  state.search = e.target.value;
  renderTable();
};

document.getElementById("type").onchange = (e) => {
  state.type = e.target.value;
  renderTable();
};

document.getElementById("tab-actius").onclick = () => {
  state.tab = "actius";
  document.getElementById("tab-actius").classList.add("active");
  document.getElementById("tab-arxivats").classList.remove("active");
  renderTable();
};

document.getElementById("tab-arxivats").onclick = () => {
  state.tab = "arxivats";
  document.getElementById("tab-arxivats").classList.add("active");
  document.getElementById("tab-actius").classList.remove("active");
  renderTable();
};

document.querySelector(".close-btn").onclick = () => {
  document.getElementById("drawer").classList.add("hidden");
  state.selected = null;
  renderTable();
};

// Init
fetchData();
=== END FILE ===