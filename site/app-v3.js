const HEADLINE = document.getElementById('headline');
const SUBHEAD = document.getElementById('subhead');
const COMMIT_INFO = document.getElementById('commit-info');
const CHART = document.getElementById('chart');
const CHART_RANGE = document.getElementById('chart-range');
const CHART_SUMMARY = document.getElementById('chart-summary');
const CATEGORIES = document.getElementById('categories');
const UNITS = document.getElementById('units');
const FILTER = document.getElementById('filter');
const FRONTIER = document.getElementById('frontier');
const RECENT = document.getElementById('recent');

let progressData = null;
let PRET_SHORT = '';

function pct(n, total) {
  return total ? (n * 100 / total).toFixed(2) : '0.00';
}

function statusChip(status) {
  return `<span class="chip chip-${status}">${status.charAt(0).toUpperCase() + status.slice(1)}</span>`;
}

function bar(pctVal) {
  return `<div class="bar"><div class="bar-fill" style="width:${pctVal}%"></div></div>`;
}

function fmtDate(ts) { return new Date(ts * 1000).toISOString().slice(0, 10); }

function renderHeader(p) {
  const m = p.measures;
  HEADLINE.textContent = pct(m.code, m['code/total']) + '% ported';
  let sub = `${m.code.toLocaleString()} / ${m['code/total'].toLocaleString()} code bytes`;
  sub += ` \u00b7 ${m.functions.toLocaleString()} / ${m['functions/total'].toLocaleString()} functions`;
  if (p.gate.present) {
    const v = m.verified_functions > 0
      ? m.verified_functions.toLocaleString() + ' verified'
      : 'verification in progress';
    sub += ` \u00b7 ${v}`;
  } else {
    sub += ' \u00b7 verification not recorded';
  }
  SUBHEAD.textContent = sub;
  let commitHtml = '';
  if (p.commit_url && p.commit) {
    commitHtml = `<a href="${p.commit_url}" target="_blank" rel="noopener">${p.commit}</a>`;
  }
  if (p.pret_commit) {
    commitHtml += (commitHtml ? ' \u00b7 ' : '') + `pret ${p.pret_commit.slice(0, 7)}`;
  }
  commitHtml += (commitHtml ? ' \u00b7 ' : '') + `updated ${fmtDate(p.generated_at)}`;
  COMMIT_INFO.innerHTML = commitHtml;
}

function renderChart(points) {
  if (!points || points.length < 2) {
    CHART.textContent = '';
    return;
  }
  const visible = points.filter((pt, index) => {
    if (index === 0 || index === points.length - 1) return true;
    const previous = points[index - 1];
    return pt.code !== previous.code || pt.code_total !== previous.code_total;
  });
  const BASELINE_TIMESTAMP = 1786493065;
  const baselineIndex = visible.findIndex(pt => pt.timestamp >= BASELINE_TIMESTAMP);
  const focus = visible.slice(baselineIndex >= 0 ? baselineIndex : Math.max(0, visible.length - 90));
  const start = focus[0].code_total ? focus[0].code * 100 / focus[0].code_total : 0;
  const end = focus[focus.length - 1].code_total
    ? focus[focus.length - 1].code * 100 / focus[focus.length - 1].code_total
    : 0;
  const delta = end - start;
  const deltaLabel = delta >= 0 ? `+${delta.toFixed(2)}` : delta.toFixed(2);
  CHART.textContent = `${start.toFixed(2)}% complete \u2192 ${end.toFixed(2)}% complete (${deltaLabel} percentage points)`;
}

function renderCategories(cats) {
  CATEGORIES.innerHTML = cats.map(c => {
    const pp = pct(c.code, c.code_total);
    return `<div class="category">
      <div class="name"><span class="pct">${pp}%</span>${c.name}</div>
      ${bar(pp)}
      <div class="detail">${c.code.toLocaleString()} / ${c.code_total.toLocaleString()} bytes \u00b7 ${c.functions} / ${c.functions_total} functions</div>
    </div>`;
  }).join('');
}

function makeFnRow(f) {
  let extra = '';
  if (f.refs === 0 && f.status === 'todo') extra = ' <span class="chip chip-unreferenced">#unreferenced</span>';
  const link = f.file
    ? `<a href="https://github.com/pret/poketcg/blob/${PRET_SHORT}/${f.file}#L${f.line}" target="_blank" rel="noopener">${f.file}:${f.line}</a>`
    : '\u2014';
  return `<tr>
    <td>${statusChip(f.status)}${f.name}${extra}</td>
    <td style="text-align:right">${f.size}b</td>
    <td style="text-align:left;font-size:0.8rem;color:var(--muted)">${link}</td>
  </tr>`;
}

function renderUnits(unitsData, funcs) {
  const funcByFile = {};
  for (const f of funcs) {
    if (!f.file) continue;
    if (!funcByFile[f.file]) funcByFile[f.file] = [];
    funcByFile[f.file].push(f);
  }
  const tbody = UNITS.querySelector('tbody');
  tbody.innerHTML = '';
  for (const u of unitsData) {
    const pp = pct(u.code, u.code_total);
    const row = document.createElement('tr');
    row.className = 'unit-row';
    row.innerHTML = `<td>${u.file}</td><td style="text-align:right">${pp}%</td><td style="text-align:right">${u.functions}/${u.functions_total}</td><td>${bar(pp)}</td>`;
    row.addEventListener('click', () => {
      const next = row.nextElementSibling;
      if (next && next.classList.contains('fn-list')) {
        next.remove(); row.classList.remove('open');
      } else {
        const fns = funcByFile[u.file] || [];
        const fnTr = document.createElement('tr');
        fnTr.className = 'fn-list open';
        const fnTd = document.createElement('td');
        fnTd.colSpan = 4;
        fnTd.innerHTML = '<table>' + fns.map(makeFnRow).join('') + '</table>';
        fnTr.appendChild(fnTd);
        row.after(fnTr); row.classList.add('open');
      }
    });
    tbody.appendChild(row);
  }
}

function sortUnits(col) {
  const tbody = UNITS.querySelector('tbody');
  if (!tbody) return;
  const rows = Array.from(tbody.querySelectorAll('tr.unit-row'));
  const colIdx = { file: 0, pct: 1, funcs: 2 }[col] || 0;
  const dir = UNITS.dataset.sortCol === col && UNITS.dataset.sortDir === 'asc' ? -1 : 1;
  rows.sort((a, b) => {
    const aText = a.children[colIdx].textContent.trim();
    const bText = b.children[colIdx].textContent.trim();
    const aNum = parseFloat(aText), bNum = parseFloat(bText);
    return (!isNaN(aNum) && !isNaN(bNum)) ? (aNum - bNum) * dir : aText.localeCompare(bText) * dir;
  });
  UNITS.dataset.sortCol = col;
  UNITS.dataset.sortDir = dir > 0 ? 'asc' : 'desc';
  for (const row of rows) {
    const fnList = row.nextElementSibling;
    tbody.appendChild(row);
    if (fnList && fnList.classList.contains('fn-list')) tbody.appendChild(fnList);
  }
}

function renderFrontier(ready) {
  FRONTIER.innerHTML = ready.slice(0, 30).map(f => {
    let extra = '';
    if (f.refs === 0) extra = ' <span class="chip chip-unreferenced">#unreferenced</span>';
    return `<div class="fn-row">${statusChip(f.status)}<span class="size">${f.size}b</span>${f.name}${extra} ${f.file}:${f.line}</div>`;
  }).join('');
}

function renderRecent(entries) {
  if (!entries || !entries.length) { RECENT.innerHTML = ''; return; }
  RECENT.innerHTML = entries.map(e => {
    const label = e.file
      ? `<a href="${progressData.pret_blob}${e.file}" target="_blank" rel="noopener">${e.name}</a>`
      : e.name;
    return `<div class="fn-row"><span class="size">${fmtDate(e.timestamp)}</span>${label}</div>`;
  }).join('');
}

function applyFilter() {
  const q = FILTER.value.toLowerCase();
  for (const row of UNITS.querySelectorAll('tr.unit-row')) {
    row.classList.toggle('hidden', q && !row.textContent.toLowerCase().includes(q));
  }
}

async function main() {
  const [progResp, histResp] = await Promise.all([
    fetch('data/progress.json?v=bar-20260813e'),
    fetch('data/history.jsonl?v=bar-20260813e').catch(() => null),
  ]);
  progressData = await progResp.json();
  PRET_SHORT = progressData.pret_commit.slice(0, 7);

  renderHeader(progressData);
  renderRecent(progressData.recent);
  renderCategories(progressData.categories);
  renderUnits(progressData.units, progressData.functions);

  const ready = progressData.functions.filter(f => f.status === 'todo' && f.ready);
  renderFrontier(ready);

  FILTER.addEventListener('input', () => applyFilter());

  for (const th of document.querySelectorAll('#units th[data-sort]')) {
    th.addEventListener('click', () => sortUnits(th.dataset.sort));
  }

  if (histResp && histResp.ok) {
    const text = await histResp.text();
    const points = text.trim().split('\n').filter(Boolean).map(JSON.parse);
    renderChart(points);
  }
}
main();
