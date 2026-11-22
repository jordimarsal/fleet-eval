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
    // If the selected item was archived, close the drawer or update it
    if (state.selected === pid) {
        // We don't have the full object here easily without re-fetching, 
        // but since we call fetchData(), the next interaction will be correct.
        // To improve UX, we could re-select or close. Let's just refresh state.
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