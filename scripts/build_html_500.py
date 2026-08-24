import json

data = json.load(open('/tmp/final_results_500.json'))
data_json = json.dumps(data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>台股前500大上市櫃公司 2026 Q1 vs Q2 財報三率、EPS、本益比、殖利率比較</title>
<style>
  :root {
    --bg: #0b0e14;
    --panel: #12161f;
    --border: #232937;
    --text: #e6e9ef;
    --text-dim: #9aa4b6;
    --accent: #4f8cff;
    --pos: #e5566d;
    --neg: #34c17a;
    --header-bg: #171c27;
    --hover: #1a2030;
    --heart-off: #444b5c;
    --heart-on: #e5566d;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, "Segoe UI", "PingFang TC", "Microsoft JhengHei", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 24px;
  }
  h1 { font-size: 20px; margin: 0 0 4px; font-weight: 600; }
  .subtitle { color: var(--text-dim); font-size: 13px; margin-bottom: 16px; line-height: 1.6; }
  .meta-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 18px;
    font-size: 12.5px;
    color: var(--text-dim);
    line-height: 1.8;
  }
  .meta-box b { color: var(--text); }
  .controls {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
  }
  #search {
    background: var(--panel);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
    width: 240px;
    outline: none;
  }
  #search:focus { border-color: var(--accent); }
  .fav-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--panel);
    border: 1px solid var(--border);
    color: var(--text-dim);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 13px;
    cursor: pointer;
    user-select: none;
  }
  .fav-toggle.active { color: var(--text); border-color: var(--heart-on); }
  .fav-toggle .heart { color: var(--heart-off); }
  .fav-toggle.active .heart { color: var(--heart-on); }
  .count { color: var(--text-dim); font-size: 12.5px; }
  .table-wrap {
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: 10px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 13px;
    min-width: 2020px;
  }
  thead th {
    position: sticky;
    top: 0;
    background: var(--header-bg);
    z-index: 2;
  }
  th, td {
    padding: 9px 10px;
    text-align: right;
    white-space: nowrap;
    border-bottom: 1px solid var(--border);
  }
  th:nth-child(1), td:nth-child(1) {
    text-align: center;
    position: sticky;
    left: 0;
    background: var(--panel);
    min-width: 40px;
  }
  th:nth-child(2), td:nth-child(2),
  th:nth-child(3), td:nth-child(3) {
    text-align: left;
    position: sticky;
    background: var(--panel);
  }
  th:nth-child(2), td:nth-child(2) { left: 40px; min-width: 66px; }
  th:nth-child(3), td:nth-child(3) { left: 106px; min-width: 110px; }
  thead th:nth-child(1), thead th:nth-child(2), thead th:nth-child(3) { background: var(--header-bg); z-index: 3; }
  td.industry { text-align: left; color: var(--text-dim); }
  th {
    cursor: pointer;
    user-select: none;
    font-weight: 600;
    color: var(--text-dim);
    font-size: 12px;
    letter-spacing: 0.2px;
    white-space: normal;
    vertical-align: bottom;
  }
  th:hover { color: var(--text); }
  th .arrow { font-size: 10px; margin-left: 3px; opacity: 0.5; }
  th.sorted .arrow { opacity: 1; color: var(--accent); }
  th .group-label {
    display: block;
    font-size: 10px;
    color: var(--text-dim);
    font-weight: 500;
    margin-bottom: 2px;
  }
  th.col-divider, td.col-divider { border-left: 1px solid var(--border); }
  tbody tr:hover { background: var(--hover); }
  td.code { color: var(--text-dim); font-variant-numeric: tabular-nums; }
  td.name { color: var(--text); font-weight: 500; }
  td.num { font-variant-numeric: tabular-nums; }
  td.pos { color: var(--pos); }
  td.neg { color: var(--neg); }
  td.na { color: #555c6b; }
  .fav-cell { cursor: pointer; font-size: 16px; line-height: 1; text-align: center !important; }
  .fav-cell .heart { color: var(--heart-off); transition: color .12s, transform .12s; display: inline-block; }
  .fav-cell.is-fav .heart { color: var(--heart-on); }
  .fav-cell:hover .heart { transform: scale(1.15); }
  .legend {
    margin-top: 14px;
    font-size: 11.5px;
    color: var(--text-dim);
    line-height: 1.7;
  }
</style>
</head>
<body>

<h1>台股前500大上市櫃公司 2026 Q1 vs Q2 財報三率、EPS、本益比、殖利率比較</h1>
<div class="subtitle">毛利率／營業利益率／稅後純益率 · 單季數字 · 點欄位標題可排序 · 點 ♡ 可加入我的最愛（儲存在瀏覽器 cookie）</div>

<div class="meta-box">
<b>範圍：</b>台灣上市＋上櫃依市值排名前500大公司（排除金融控股／銀行／證券／保險業）。資料日期約 2026/08/21。<br>
<b>三率／EPS：</b>取自 FinMind TaiwanStockFinancialStatements，2026 Q1／Q2 單季數字直接計算，成長率＝Q2三率−Q1三率。<br>
<b>產業分類／本益比：</b>取自 FinMind TaiwanStockInfo／TaiwanStockPER；無意義者顯示「—」。<br>
<b>目前股價：</b>取自 FinMind TaiwanStockPrice 最新收盤價；每日排程自動更新。<br>
<b>今年配息／殖利率：</b>加總除息日在2026年內之現金股利；殖利率＝配息÷股價×100%。<br>
<b>⚠️ 資料完整度：</b>新納入約245家公司中，因API速率限制（每欄位最多重試3次），約150家的三率／EPS／本益比／配息暫缺（顯示「—」），僅代號、名稱、產業、股價較完整。原有255家資料完整。<br>
<b>我的最愛：</b>點左側愛心加入／移除最愛，儲存在瀏覽器 cookie（一年後過期），可用「只顯示最愛」篩選。<br>
第三方彙整資料，僅供參考，正式數字請以公司公告及證交所／櫃買中心資訊為準。
</div>

<div class="controls">
  <input id="search" type="text" placeholder="搜尋代號、名稱或產業...">
  <div class="fav-toggle" id="favToggle"><span class="heart">♥</span><span>只顯示最愛</span></div>
  <span class="count" id="count"></span>
</div>

<div class="table-wrap">
<table id="tbl">
<thead>
<tr>
  <th data-key="fav" data-type="fav" title="我的最愛">♥</th>
  <th data-key="code" data-type="str">代號<span class="arrow">↕</span></th>
  <th data-key="name" data-type="str">名稱<span class="arrow">↕</span></th>
  <th data-key="industry" data-type="str">產業分類<span class="arrow">↕</span></th>
  <th data-key="q1_gm" data-type="num" class="col-divider"><span class="group-label">Q1</span>毛利率%<span class="arrow">↕</span></th>
  <th data-key="q1_om" data-type="num"><span class="group-label">Q1</span>營業利益率%<span class="arrow">↕</span></th>
  <th data-key="q1_nm" data-type="num"><span class="group-label">Q1</span>稅後純益率%<span class="arrow">↕</span></th>
  <th data-key="q2_gm" data-type="num" class="col-divider"><span class="group-label">Q2</span>毛利率%<span class="arrow">↕</span></th>
  <th data-key="q2_om" data-type="num"><span class="group-label">Q2</span>營業利益率%<span class="arrow">↕</span></th>
  <th data-key="q2_nm" data-type="num"><span class="group-label">Q2</span>稅後純益率%<span class="arrow">↕</span></th>
  <th data-key="g_gm" data-type="num" class="col-divider"><span class="group-label">成長(pp)</span>毛利率<span class="arrow">↕</span></th>
  <th data-key="g_om" data-type="num"><span class="group-label">成長(pp)</span>營業利益率<span class="arrow">↕</span></th>
  <th data-key="g_nm" data-type="num"><span class="group-label">成長(pp)</span>稅後純益率<span class="arrow">↕</span></th>
  <th data-key="q1_eps" data-type="num" class="col-divider"><span class="group-label">EPS</span>Q1<span class="arrow">↕</span></th>
  <th data-key="h1_eps" data-type="num"><span class="group-label">EPS</span>H1<span class="arrow">↕</span></th>
  <th data-key="q2_eps" data-type="num"><span class="group-label">EPS</span>Q2<span class="arrow">↕</span></th>
  <th data-key="per" data-type="num" class="col-divider">目前本益比<span class="arrow">↕</span></th>
  <th data-key="price" data-type="num" class="col-divider">目前股價<span class="arrow">↕</span></th>
  <th data-key="dividend" data-type="num">今年配息(元)<span class="arrow">↕</span></th>
  <th data-key="yield" data-type="num">殖利率%<span class="arrow">↕</span></th>
</tr>
</thead>
<tbody id="tbody"></tbody>
</table>
</div>

<div class="legend">紅色＝正值／成長，綠色＝負值／衰退，— 表示資料無法取得。表格預設依股票代號排序，點任一欄標題可切換升冪／降冪排序。</div>

<script>
const DATA = ''' + data_json + ''';
const STR_KEYS = ["code","name","industry"];
const COOKIE_NAME = "tpex500_favorites";
let sortKey = "code";
let sortAsc = true;
let favOnly = false;

function getCookie(name) {
  const m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return m ? decodeURIComponent(m[1]) : '';
}
function setCookie(name, value, days) {
  const d = new Date();
  d.setTime(d.getTime() + days*24*60*60*1000);
  document.cookie = name + '=' + encodeURIComponent(value) + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
}
function loadFavorites() {
  const raw = getCookie(COOKIE_NAME);
  return new Set(raw ? raw.split(',').filter(Boolean) : []);
}
function saveFavorites(set) {
  setCookie(COOKIE_NAME, Array.from(set).join(','), 365);
}
let favorites = loadFavorites();

function toggleFavorite(code) {
  if (favorites.has(code)) favorites.delete(code); else favorites.add(code);
  saveFavorites(favorites);
  applyFilter();
}

function fmtNum(v, key) {
  if (v === null || v === undefined) return '<span class="na">—</span>';
  const cls = v > 0 ? 'pos' : (v < 0 ? 'neg' : '');
  const sign = (key.startsWith('g_') && v > 0) ? '+' : '';
  return `<span class="${cls}">${sign}${v.toFixed(2)}</span>`;
}

function fmtStr(v) {
  if (v === null || v === undefined || v === '') return '<span class="na">—</span>';
  return v;
}

function render(rows) {
  const tbody = document.getElementById('tbody');
  tbody.innerHTML = rows.map(r => {
    const isFav = favorites.has(r.code);
    return `
    <tr>
      <td class="fav-cell${isFav ? ' is-fav' : ''}" data-code="${r.code}"><span class="heart">${isFav ? '♥' : '♡'}</span></td>
      <td class="code">${r.code}</td>
      <td class="name">${r.name}</td>
      <td class="industry">${fmtStr(r.industry)}</td>
      <td class="num col-divider">${fmtNum(r.q1_gm,'q1_gm')}</td>
      <td class="num">${fmtNum(r.q1_om,'q1_om')}</td>
      <td class="num">${fmtNum(r.q1_nm,'q1_nm')}</td>
      <td class="num col-divider">${fmtNum(r.q2_gm,'q2_gm')}</td>
      <td class="num">${fmtNum(r.q2_om,'q2_om')}</td>
      <td class="num">${fmtNum(r.q2_nm,'q2_nm')}</td>
      <td class="num col-divider">${fmtNum(r.g_gm,'g_gm')}</td>
      <td class="num">${fmtNum(r.g_om,'g_om')}</td>
      <td class="num">${fmtNum(r.g_nm,'g_nm')}</td>
      <td class="num col-divider">${fmtNum(r.q1_eps,'q1_eps')}</td>
      <td class="num">${fmtNum(r.h1_eps,'h1_eps')}</td>
      <td class="num">${fmtNum(r.q2_eps,'q2_eps')}</td>
      <td class="num col-divider">${fmtNum(r.per,'per')}</td>
      <td class="num col-divider">${fmtNum(r.price,'price')}</td>
      <td class="num">${fmtNum(r.dividend,'dividend')}</td>
      <td class="num">${fmtNum(r.yield,'yield')}</td>
    </tr>
  `; }).join('');
  document.getElementById('count').textContent = `共 ${rows.length} 家公司（最愛 ${favorites.size} 家）`;
  tbody.querySelectorAll('.fav-cell').forEach(cell => {
    cell.addEventListener('click', () => toggleFavorite(cell.getAttribute('data-code')));
  });
}

function sortData(rows, key, asc) {
  if (key === 'fav') {
    return [...rows].sort((a,b) => {
      const av = favorites.has(a.code) ? 1 : 0;
      const bv = favorites.has(b.code) ? 1 : 0;
      return asc ? bv - av : av - bv;
    });
  }
  const type = STR_KEYS.includes(key) ? 'str' : 'num';
  return [...rows].sort((a,b) => {
    let av = a[key], bv = b[key];
    if (av === null || av === undefined || av === '') return 1;
    if (bv === null || bv === undefined || bv === '') return -1;
    if (type === 'str') {
      return asc ? String(av).localeCompare(String(bv), 'zh-Hant') : String(bv).localeCompare(String(av), 'zh-Hant');
    }
    return asc ? av - bv : bv - av;
  });
}

function applyFilter() {
  const q = document.getElementById('search').value.trim().toLowerCase();
  let rows = DATA;
  if (q) {
    rows = rows.filter(r => r.code.toLowerCase().includes(q) || r.name.toLowerCase().includes(q) || (r.industry || '').toLowerCase().includes(q));
  }
  if (favOnly) {
    rows = rows.filter(r => favorites.has(r.code));
  }
  rows = sortData(rows, sortKey, sortAsc);
  render(rows);
}

document.querySelectorAll('th[data-key]').forEach(th => {
  th.addEventListener('click', () => {
    const key = th.getAttribute('data-key');
    if (sortKey === key) {
      sortAsc = !sortAsc;
    } else {
      sortKey = key;
      sortAsc = key === 'fav' ? true : true;
    }
    document.querySelectorAll('th').forEach(h => h.classList.remove('sorted'));
    th.classList.add('sorted');
    if (th.querySelector('.arrow')) th.querySelector('.arrow').textContent = sortAsc ? '↑' : '↓';
    applyFilter();
  });
});

document.getElementById('favToggle').addEventListener('click', () => {
  favOnly = !favOnly;
  document.getElementById('favToggle').classList.toggle('active', favOnly);
  applyFilter();
});

document.getElementById('search').addEventListener('input', applyFilter);

applyFilter();
</script>

</body>
</html>
'''

with open('/tmp/site_build/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Written, length:", len(html))
