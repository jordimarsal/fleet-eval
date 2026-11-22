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

// Returns the items currently shown based on the selected tab. The active-tab set is also what the rest of the table reads from.
function applyTabFilter(items) {
  return items.filter((p) => p.archived === (state.tab === "arxivats"));
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

function renderSummary() {
  const list = applyTabFilter(state.items);
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
  const allOption = el("option", "", "tipus: tots");
  allOption.value = "";
  select.appendChild(allOption);
  for (const kind of kinds) {
    const opt = el("option", "", kind);
    opt.value = kind;
    select.appendChild(opt);
  }
  if (kinds.includes(current)) select.value = current; else select.value = "";
}

async function triggerAction(pid, action, confirmProtected) {
  // Keep the F3 handler as-is in app code path: ask before acting on protected projects, then POST and refresh.
  let needsConfirm = Boolean(confirmProtected);
  if (needsConfirm) {
    if (!window.confirm(`Confirmes que vols executar «${action}» en aquest projecte? Pot ser destructiu.`)) return;
  }
  try {
    await fetch(`/api/projects/${encodeURIComponent(pid)}/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ confirm: needsConfirm }),
    });
  } catch (err) {
    console.error("action failed", err);
  }
  await refresh();
}

// Archive / unarchive from inside the detail drawer. Refreshes after success and reselects nothing; the server state drives the tab UI through renderAll.
async function toggleArchive(item) {
  const endpoint = item.archived ? "unarchive" : "archive";
  try {
    await fetch(`/api/projects/${encodeURIComponent(item.id)}/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
  } catch (err) {
    console.error("toggleArchive failed", err);
    return;
  }
  // Move immediately to the other tab where this project will actually live after the switch.
  state.tab = item.archived ? "actius" : "arxivats";
  setActiveTabUI();
  state.selected = null;
  hideDrawer();
  await refresh();
}

function hideDrawer() {
  const drawer = document.getElementById("detail");
  if (!drawer) return;
  drawer.classList.remove("vis");
  setTimeout(() => drawer.classList.add("hidden"), 240);
}

function buildStatusPill(status) {
  return el("span", "status-pill " + status, status === "up" ? "amunt" : "avall");
}

function buildMetaRow(label, value) {
  const row = el("div", "meta-row");
  row.appendChild(el("dt", "meta-key", label));
  row.appendChild(el("dd", "meta-value", value === undefined || value === null ? "—" : String(value)));
  return row;
}

function appendActionButtons(body, item) {
  // Actions section — kept compatible with the F3 UI path via `item.actions`.
  const actions = Array.isArray(item.actions) ? item.actions : [];
  body.appendChild(el("h3", "section action-heading", "Accions"));
  if (!actions.length) {
    body.appendChild(el("p", "muted empty-note", "Sense accions declarades al dashboard.yaml."));
    return;
  }
  for (const entry of actions) {
    let info = null;
    if (typeof entry === "string" && /^\w+:/.test(entry)) info = { name: entry.split(":")[0].trim() };
    else if (entry && typeof entry === "object") info = { name: entry.name || "", protected: Boolean(entry.protected ?? item.protected) };
    if (!info || !info.name) continue;
    const btn = el("button", "action-btn" + (item.protected ? " protected" : ""), "▶ " + info.name);
    btn.type = "button";
    btn.addEventListener("click", () => triggerAction(item.id, info.name, item.protected));
    body.appendChild(btn);
  }
}

function appendArchiveButton(body, item) {
  body.appendChild(el("h3", "section archive-heading", "Arxiu"));
  const wrap = el("div", "archive-actions");
  const label = item.archived ? "Desarxivar projecte" : "Arxivar projecte";
  const button = el("button", "archive-btn" + (item.archived ? " restore" : " move"), label);
  button.type = "button";
  button.setAttribute("aria-pressed", String(item.archived === true));
  button.addEventListener("click", () => toggleArchive(item));
  wrap.appendChild(button);
  body.appendChild(wrap);
}

async function loadDetailBody(pid) {
  let payload = null;
  try {
    const res = await fetch(`/api/projects/${encodeURIComponent(pid)}`);
    if (!res.ok) return null;
    payload = await res.json();
  } catch (err) {
    console.error("detail load failed", err);
    return null;
  }
  return payload;
}

function populateDrawer(saved) {
  state.selected_payload = saved || {};
  document.getElementById("detail-name").textContent = (state.selected_payload && state.selected_payload.name) || "Detall";
}

async function openDetail(id) {
  const item = state.items.find((p) => p.id === id);
  if (!item) return;
  // Keep cached identity for archive button wiring even if re-rendered.
  const cacheItem = Object.assign({}, item);
  state.selected = id;
  setActiveRowState();

  const drawer = document.getElementById("detail");
  const body = document.getElementById("detail-body");
  drawer.classList.remove("hidden");
  requestAnimationFrame(() => drawer.classList.add("vis"));
  body.textContent = "";
  body.appendChild(buildStatusPill(cacheItem.status));

  const meta = el("dl", "meta");
  meta.appendChild(buildMetaRow("Tipus", cacheItem.type));
  meta.appendChild(buildMetaRow("Port", cacheItem.port == null ? "—" : String(cacheItem.port)));
  meta.appendChild(buildMetaRow("Uptime", fmtUptime(cacheItem.uptime === undefined ? null : cacheItem.uptime)));
  meta.appendChild(buildMetaRow("Protegit", cacheItem.protected ? "sí" : "no"));
  meta.appendChild(buildMetaRow("Arxivat", cacheItem.archived ? "sí" : "no"));
  body.appendChild(meta);

  appendActionButtons(body, cacheItem);
  appendArchiveButton(body, cacheItem);

  // Richer context (git/readme/log) is loaded best-effort from the detail endpoint.
  loadDetailBody(id).then((payload) => {
    if (!state.selected || state.selected !== id) return;
    const extra = el("div", "extra-details");
    const gitData = payload && payload.git ? payload.git : null;
    if (payload && Array.isArray(payload.actions)) {
      // Only render actions we don't know yet — use the server list for naming truth.
    }
    if (gitData && typeof gitData === "object") {
      extra.appendChild(el("h3", "section section-git", "Git"));
      const info = [];
      if (gitData.branch) info.push(`branca ${gitData.branch}`);
      if (gitData.commit && gitData.commit.short_hash) info.push(String(gitData.commit.short_hash));
      else if (gitData.sha) info.push(String(gitData.sha));
      let commitMsg = "";
      if (gitData.commit && typeof gitData.commit === "object" && gitData.commit.message) commitMsg = String(gitData.commit.message);
      if (info.length || commitMsg) {
        const text = [...info];
        if (commitMsg) text.push(`— ${commitMsg}`);
        extra.appendChild(el("p", "muted meta-value", text.join(" ")));
      }
    }
    if (payload && Array.isArray(payload.log) && payload.log.length) {
      extra.appendChild(el("h3", "section section-logs", "Últimes línies de log"));
      for (const line of payload.log.slice(0, 20)) {
        extra.appendChild(el("pre", "mono mono-line", String(line)));
      }
    }
    if (extra.childNodes.length) body.appendChild(extra);
  }).catch(() => {});
}

function setActiveRowState() {
  for (const row of document.querySelectorAll("#rows tr[tabindex]")) {
    const active = Boolean(state.selected) && row.dataset.id === state.selected;
    row.classList.toggle("selected", active);
    row.setAttribute("aria-pressed", String(active));
  }
}

function renderTable() {
  const tbody = document.getElementById("rows");
  tbody.textContent = "";
  const visible = applyFilters(state.items);
  const empty = document.getElementById("empty");
  if (empty) empty.classList.toggle("hidden", visible.length > 0);
  for (const p of visible) {
    const tr = el("tr");
    tr.tabIndex = 0;
    tr.dataset.id = p.id;
    if (p.id === state.selected) tr.classList.add("selected");

    const nameTd = el("td");
    nameTd.appendChild(el("span", "mono mono-name", p.name));
    // keep path as secondary text inside the same cell so scanning stays easy
    const sub = el("div", "row-sub mono", p.path || "");
    nameTd.appendChild(sub);

    const typeTd = el("td", "", p.type);
    const statusTd = el("td");
    statusTd.appendChild(buildStatusPill(p.status));
    const portTd = el("td", "", p.port == null ? "—" : String(p.port));
    const uptimeTd = el("td", "", fmtUptime(p.uptime));
    const protectedTd = el("td", "", p.protected ? "protegida" : "");

    tr.appendChild(nameTd);
    tr.appendChild(typeTd);
    tr.appendChild(statusTd);
    tr.appendChild(portTd);
    tr.appendChild(uptimeTd);
    tr.appendChild(protectedTd);

    tr.addEventListener("click", () => openDetail(p.id));
    tr.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openDetail(p.id);
      }
    });
    tbody.appendChild(tr);
  }
}

function renderAll() {
  setActiveTabUI();
  renderCounters();
  renderSummary();
  renderTypes(state.items);
  renderTable();
  // Re-open drawer content if it is still relevant after a refresh/search change with the same selected project.
  if (state.selected && state.selected !== null) {
    const kept = applyFilters(state.items).find((p) => p.id === state.selected);
    if (!kept) {
      state.selected = null;
      hideDrawer();
    } else {