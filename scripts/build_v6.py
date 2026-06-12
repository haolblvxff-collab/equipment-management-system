#!/usr/bin/env python3
"""Build equipment_management_v6.html from JSON data files + interactive features."""

import json, os

SCRIPTS = os.path.expanduser("~/.hermes/scripts")

def load_json(name):
    path = os.path.join(SCRIPTS, name)
    with open(path) as f:
        return json.load(f)

# Load all data
enhanced = load_json("equipment_enhanced_data.json")
spare = load_json("equipment_spare_parts.json")
pm = load_json("equipment_pm_enhanced.json")
ledger = load_json("equipment_ledger_enhanced.json")
anomaly = load_json("equipment_anomaly_data.json")
pdca = load_json("equipment_pdca_orders.json")
kb = load_json("equipment_knowledge_base.json")
bs_data = load_json("equipment_blackswan.json")

# Read the build template
with open(os.path.join(SCRIPTS, "build_v6.py"), "r") as f:
    pass  # placeholder — we're generating HTML below

# Build HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>设备管理系统 v6.0 | 全交互·PDCA闭环·知识库·溯源分析</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--dim:#8b949e;--red:#ff4444;--orange:#ffa500;--green:#00b050;--blue:#58a6ff;--purple:#bc8cff;--cyan:#39d2c0;--yellow:#ffc000}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);padding:20px;min-height:100vh}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--border)}}
.header h1{{font-size:1.4rem}}.header .sub{{color:var(--dim);font-size:.72rem}}
.tabs{{display:flex;gap:3px;margin-bottom:20px;flex-wrap:wrap;background:var(--card);border-radius:12px;padding:4px;border:1px solid var(--border)}}
.tab{{padding:9px 12px;border-radius:8px;cursor:pointer;font-size:.74rem;font-weight:600;color:var(--dim);transition:.2s;border:none;background:none;white-space:nowrap}}
.tab:hover{{color:var(--text);background:rgba(255,255,255,.03)}}
.tab.active{{background:var(--blue);color:#fff}}
.content{{display:none}}.content.active{{display:block}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:16px}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px}}
.kpi .lbl{{color:var(--dim);font-size:.66rem;margin-bottom:3px}}.kpi .val{{font-size:1.35rem;font-weight:700}}.kpi .sub{{font-size:.6rem;color:var(--dim)}}
.status-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin-bottom:16px}}
.status-card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px;border-left:4px solid var(--border);transition:.2s}}
.status-card:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.4)}}
table{{width:100%;border-collapse:collapse;font-size:.74rem}}
th{{background:var(--card);color:var(--dim);padding:10px 12px;text-align:left;font-weight:600;border-bottom:2px solid var(--border);position:sticky;top:0;z-index:1}}
td{{padding:8px 12px;border-bottom:1px solid var(--border)}}tr:hover td{{background:rgba(88,166,255,.04)}}
.badge{{padding:2px 8px;border-radius:10px;font-size:.63rem;font-weight:600;display:inline-block}}
.badge-red{{background:rgba(255,68,68,.15);color:var(--red)}}.badge-orange{{background:rgba(255,165,0,.15);color:var(--orange)}}.badge-green{{background:rgba(0,176,80,.15);color:var(--green)}}.badge-blue{{background:rgba(88,166,255,.15);color:var(--blue)}}.badge-purple{{background:rgba(188,140,255,.15);color:var(--purple)}}.badge-cyan{{background:rgba(57,210,192,.15);color:var(--cyan)}}
.scroll-table{{max-height:500px;overflow-y:auto;border-radius:8px;border:1px solid var(--border)}}
.filter-bar{{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}}
.filter-bar input,.filter-bar select{{background:var(--card);color:var(--text);border:1px solid var(--border);padding:5px 10px;border-radius:6px;font-size:.74rem}}
.filter-bar input:focus,.filter-bar select:focus{{outline:none;border-color:var(--blue)}}
.insight-box{{background:linear-gradient(135deg,#161b22,#0d1117);border:1px solid var(--border);border-radius:10px;padding:14px;margin-bottom:14px}}
.insight-box h3{{color:var(--blue);font-size:.76rem;margin-bottom:6px}}.insight-box p{{color:var(--dim);font-size:.7rem;line-height:1.6}}
.detail-panel{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;margin-top:12px}}
.detail-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.74rem}}
.detail-grid div{{color:var(--dim)}}.detail-grid div span{{color:var(--text);font-weight:600}}
.footer{{text-align:center;color:var(--dim);font-size:.6rem;padding-top:16px;margin-top:16px;border-top:1px solid var(--border)}}
.role-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.role-col{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px}}
.role-col h3{{font-size:.78rem;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.role-item{{padding:6px 0;font-size:.7rem;border-bottom:1px solid rgba(48,54,61,.5)}}.role-item .val{{font-weight:700;float:right}}
.chart-box{{position:relative;max-height:420px;overflow:hidden;margin-bottom:16px}}
.chart-box canvas{{max-height:400px!important}}
.kb-card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px}}
.kb-card .kb-title{{font-size:.78rem;font-weight:700;margin-bottom:4px}}
.kb-card .kb-meta{{font-size:.64rem;color:var(--dim)}}
.kb-steps{{font-size:.68rem;color:var(--text);margin-top:6px;padding-left:16px}}
@media(min-width:1024px){{.chart-box{{max-height:480px}}.chart-box canvas{{max-height:460px!important}}}}

/* v6.0 交互模式 */
.modal-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);z-index:1000;display:flex;align-items:center;justify-content:center}}
.modal-box{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;max-width:600px;width:90%;max-height:85vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.6)}}
.modal-box h3{{font-size:.9rem;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.modal-row{{display:flex;gap:8px;margin-bottom:8px;flex-wrap:wrap;align-items:center}}
.modal-row label{{font-size:.68rem;color:var(--dim);min-width:70px;padding-top:5px}}
.modal-row input,.modal-row select,.modal-row textarea{{flex:1;min-width:120px;background:var(--bg);color:var(--text);border:1px solid var(--border);padding:6px 10px;border-radius:6px;font-size:.72rem;font-family:inherit}}
.modal-row textarea{{min-height:60px;resize:vertical}}
.modal-row input:focus,.modal-row select:focus,.modal-row textarea:focus{{outline:none;border-color:var(--blue)}}
.modal-row input[type=checkbox]{{min-width:auto;width:auto}}
.modal-btns{{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}}
.btn-primary{{background:var(--blue);color:#fff;border:none;padding:7px 18px;border-radius:6px;font-size:.72rem;font-weight:600;cursor:pointer}}
.btn-danger{{background:var(--red);color:#fff;border:none;padding:7px 18px;border-radius:6px;font-size:.72rem;font-weight:600;cursor:pointer}}
.btn-secondary{{background:var(--border);color:var(--text);border:none;padding:7px 18px;border-radius:6px;font-size:.72rem;font-weight:600;cursor:pointer}}
.btn-sm{{padding:3px 8px;font-size:.62rem;border-radius:4px;cursor:pointer;border:none;font-weight:600;color:#fff}}
.btn-edit{{background:var(--blue)}}.btn-status{{background:var(--purple)}}
.status-group{{margin-bottom:16px}}
.status-group h3{{font-size:.78rem;color:var(--dim);margin-bottom:8px;padding:4px 0;border-bottom:1px solid var(--border)}}
.pdca-board{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:12px}}
.pdca-col{{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:8px;min-height:120px}}
.pdca-col h4{{font-size:.66rem;text-align:center;margin-bottom:6px;padding-bottom:4px;border-bottom:1px solid var(--border)}}
.pdca-card{{background:var(--card);border:1px solid var(--border);border-radius:6px;padding:6px;margin-bottom:4px;font-size:.62rem;cursor:pointer;transition:.15s}}
.pdca-card:hover{{transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.3)}}
.pdca-card .pc-machine{{font-weight:700;font-size:.66rem}}
.pdca-card .pc-cat{{color:var(--dim);margin-top:2px}}
.pdca-card .pc-urg{{float:right;font-size:.56rem;padding:1px 4px;border-radius:3px}}
.checklist-item{{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border);font-size:.7rem}}
.checklist-item input[type=checkbox]{{width:auto}}
.checklist-item .check-label{{flex:1}}
.checklist-item .check-result select{{font-size:.64rem;background:var(--bg);color:var(--text);border:1px solid var(--border);padding:2px 6px;border-radius:4px}}
.inventory-log{{font-size:.64rem;max-height:200px;overflow-y:auto;margin-top:8px}}
.inventory-log tr td{{padding:3px 6px;font-size:.62rem}}
.toast{{position:fixed;top:20px;right:20px;background:var(--green);color:#fff;padding:10px 20px;border-radius:8px;font-size:.74rem;font-weight:600;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1}}
@media(max-width:1200px){{.pdca-board{{grid-template-columns:repeat(3,1fr)}}}}
@media(max-width:768px){{.pdca-board{{grid-template-columns:1fr}}.role-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>

<div class="header">
  <div><h1>⚙️ 设备管理系统 v6.0</h1><div class="sub">全交互 · 决策-行动双引擎 · PDCA闭环 · 知识库 · 溯源分析</div></div>
  <span class="badge badge-blue" id="clock">🕐</span>
</div>

<div class="tabs">
  <button class="tab active" onclick="switchTab('role',this)">🎯 角色仪表盘</button>
  <button class="tab" onclick="switchTab('status',this)">📊 设备状态</button>
  <button class="tab" onclick="switchTab('trace',this)">🔍 事件溯源</button>
  <button class="tab" onclick="switchTab('workorder',this)">🔧 PDCA工单</button>
  <button class="tab" onclick="switchTab('pm',this)">🛡️ 保养</button>
  <button class="tab" onclick="switchTab('spareparts',this)">📦 备件</button>
  <button class="tab" onclick="switchTab('ledger',this)">📋 台账</button>
  <button class="tab" onclick="switchTab('knowledge',this)">📚 知识库</button>
  <button class="tab" onclick="switchTab('blackswan',this)">🦢 黑天鹅</button>
</div>

<!-- Tabs content -->
<div class="content active" id="tab-role"><div class="insight-box"><h3>🎯 角色仪表盘</h3><p>基于德鲁克原则：第一屏应是"今天需要关注什么"。三种角色三种视图。</p></div><div class="role-grid" id="roleGrid"></div></div>

<div class="content" id="tab-status">
  <div class="kpi-grid" id="statusKPIs"></div>
  <div class="filter-bar"><input type="text" placeholder="🔍 搜索..." oninput="renderStatus()" id="statusSearch"><select onchange="renderStatus()" id="statusFilter"><option value="">全部状态</option><option>正常</option><option>注意</option><option>异常</option><option>维修中</option><option>待保养</option></select><select onchange="renderStatus()" id="typeFilter"><option value="">全部类型</option></select></div>
  <div id="statusCards"></div>
</div>

<div class="content" id="tab-trace">
  <div class="kpi-grid" id="traceKPIs"></div>
  <div class="insight-box"><h3>🔍 设备事件溯源分析</h3><p>追踪设备异常模式：哪台机器最近异常激增？哪种故障类型在蔓延？基于录入数据动态分析。</p></div>
  <div class="chart-box"><h3>📊 设备异常次数排名 (近30天)</h3><canvas id="cEventRank"></canvas></div>
  <div class="chart-box"><h3>🏷️ 故障类别分布</h3><canvas id="cCategoryShift"></canvas></div>
  <div class="filter-bar"><input type="text" placeholder="🔍 搜索机台..." oninput="renderTrace()" id="traceSearch"><select onchange="renderTrace()" id="traceType"><option value="">全部类型</option></select></div>
  <div class="scroll-table" id="traceTable"></div>
</div>

<div class="content" id="tab-workorder">
  <div class="kpi-grid" id="woKPIs"></div>
  <div class="insight-box"><h3>🔄 PDCA闭环工单 — 六阶段严格流转</h3><p>报修→排查→定因→处理→验证→结案。点击看板卡片推进阶段，每阶段强制记录时间和责任人。</p></div>
  <div id="pdcaBoard"></div>
  <div class="filter-bar">
    <input type="text" placeholder="🔍 搜索机台/工单..." oninput="renderWO()" id="woSearch">
    <select onchange="renderWO()" id="woStage"><option value="">全部阶段</option><option>报修</option><option>排查</option><option>定因</option><option>处理</option><option>验证</option><option>结案</option></select>
    <label style="color:var(--dim);font-size:.72rem"><input type="checkbox" onchange="renderWO()" id="woOverdue">仅超期</label>
  </div>
  <div class="scroll-table"><table><thead><tr><th>工单号</th><th>机台</th><th>类别</th><th>紧急</th><th>阶段</th><th>根因</th><th>验证</th><th>耗时</th><th>操作</th></tr></thead><tbody id="woBody"></tbody></table></div>
</div>

<div class="content" id="tab-pm"><div class="kpi-grid" id="pmKPIs"></div><div class="filter-bar"><input type="text" placeholder="🔍 搜索..." oninput="renderPM()" id="pmSearch"><select onchange="renderPM()" id="pmStatus"><option value="">全部</option><option>超期</option><option>本周</option><option>正常</option></select></div><div id="pmTable"></div></div>

<div class="content" id="tab-spareparts"><div class="kpi-grid" id="spKPIs"></div><div class="filter-bar"><input type="text" placeholder="🔍 搜索..." oninput="renderSP()" id="spSearch"><select onchange="renderSP()" id="spStatus"><option value="">全部</option><option>正常</option><option>低库存</option><option>缺货</option></select><label style="color:var(--dim);font-size:.7rem"><input type="checkbox" onchange="renderSP()" id="spCritical">仅关键件</label></div><div id="spTable"></div></div>

<div class="content" id="tab-ledger"><div class="kpi-grid" id="ledgerKPIs"></div><div class="filter-bar"><input type="text" placeholder="🔍 搜索..." oninput="renderLedger()" id="ledgerSearch"><select onchange="renderLedger()" id="ledgerType"><option value="">全部类型</option></select></div><div id="ledgerTable"></div></div>

<div class="content" id="tab-knowledge">
  <div class="kpi-grid" id="kbKPIs"></div>
  <div class="insight-box"><h3>📚 设备维修知识库 — 可编辑</h3><p>基于塔勒布原则：每次故障让组织变得更强。所有条目可编辑，支持新增。可检索、可复用。</p></div>
  <div class="filter-bar">
    <input type="text" placeholder="🔍 搜索根因/症状/机台..." oninput="renderKB()" id="kbSearch">
    <select onchange="renderKB()" id="kbMachine"><option value="">全部机台</option></select>
    <select onchange="renderKB()" id="kbCategory"><option value="">全部分类</option><option>设备装置异常</option><option>工艺条件异常</option><option>耗材消耗</option><option>PM</option></select>
  </div>
  <div id="kbList"></div>
</div>

<div class="content" id="tab-blackswan">
  <div class="kpi-grid" id="bsKPIs"></div>
  <div class="insight-box"><h3>🦢 黑天鹅仪表盘 — 反脆弱层</h3><p>基于塔勒布原则：追踪未知的未知。结合用户录入数据进行动态分析。</p></div>
  <div class="chart-box"><h3>📊 错误预算消耗 (本月)</h3><canvas id="cErrorBudget"></canvas></div>
  <div class="chart-box"><h3>📈 异常类别月度突变</h3><canvas id="cClusterMutation"></canvas></div>
  <h3 style="font-size:.8rem;color:var(--dim);margin:16px 0 8px">🔴 本月黑天鹅事件</h3>
  <div id="bsEvents"></div>
  <h3 style="font-size:.8rem;color:var(--dim);margin:16px 0 8px">🔥 故障演练记录</h3>
  <div class="scroll-table"><table><thead><tr><th>日期</th><th>机台</th><th>演练场景</th><th>检测(s)</th><th>响应(min)</th><th>发现问题</th><th>评分</th></tr></thead><tbody id="bsDrillBody"></tbody></table></div>
</div>

<div class="modal-overlay" id="modalOverlay" style="display:none" onclick="if(event.target===this)closeModal()"><div class="modal-box" id="modalBox"></div></div>
<div class="toast" id="toast"></div>
<div class="footer">设备管理系统 v6.0 · 全交互 · 决策-行动双引擎 · PDCA闭环 · 事件溯源 · 知识库 · 黑天鹅</div>

<script>const ENHANCED={json.dumps(enhanced, ensure_ascii=False)}</script>
<script>const SPARE_PARTS={json.dumps(spare, ensure_ascii=False)}</script>
<script>const PM={json.dumps(pm, ensure_ascii=False)}</script>
<script>const LEDGER={json.dumps(ledger, ensure_ascii=False)}</script>
<script>const ANOMALY={json.dumps(anomaly, ensure_ascii=False)}</script>
<script>const PDCA={json.dumps(pdca, ensure_ascii=False)}</script>
<script>const KB={json.dumps(kb, ensure_ascii=False)}</script>
<script>const BS={json.dumps(bs_data, ensure_ascii=False)}</script>

<script>
setInterval(()=>document.getElementById('clock').textContent='🕐 '+new Date().toLocaleString('zh-CN'),1000);

// Chart.js实例追踪
const chartInstances=[];
function destroyCharts(){{chartInstances.forEach(c=>{{try{{c.destroy()}}catch(e){{}}}});chartInstances.length=0;}}
function switchTab(name,el){{
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.content').forEach(c=>c.classList.remove('active'));
  (el||event.target).classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
  destroyCharts();
  const fns={{role:renderRole,status:renderStatus,trace:renderTrace,workorder:renderWO,pm:renderPM,spareparts:renderSP,ledger:renderLedger,knowledge:renderKB,blackswan:renderBlackSwan}};
  if(fns[name])fns[name]();
}}

// ═══ localStorage ═══
const LSK='eq_v6';
function loadData(){{try{{const d=localStorage.getItem(LSK);return d?JSON.parse(d):{{machineStatus:{{}},workOrders:[],pmChecklists:{{}},pmRecords:[],spareMovements:[],spareStock:{{}},ledgerDevices:[],kbRecords:[]}}}}catch(e){{return{{machineStatus:{{}},workOrders:[],pmChecklists:{{}},pmRecords:[],spareMovements:[],spareStock:{{}},ledgerDevices:[],kbRecords:[]}}}}}}
function saveData(d){{try{{localStorage.setItem(LSK,JSON.stringify(d))}}catch(e){{}}}}
function showToast(msg){{const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000);}}
function openModal(html){{document.getElementById('modalBox').innerHTML=html;document.getElementById('modalOverlay').style.display='flex'}}
function closeModal(){{document.getElementById('modalOverlay').style.display='none'}}

// ─── 数据合并 ───
function getMergedStatus(){{const ms=JSON.parse(JSON.stringify(ENHANCED.machine_status||{{}}));const ud=loadData();Object.entries(ud.machineStatus||{{}}).forEach(([k,v])=>{{if(ms[k])Object.assign(ms[k],v)}});return ms}}
function getMergedWO(){{const wos=[...(PDCA||[]).map(w=>({{...w,_source:'system'}}))];const ud=loadData();(ud.workOrders||[]).forEach(w=>wos.push({{...w,_source:'user'}}));return wos}}
function getMergedSpare(){{const sp=JSON.parse(JSON.stringify(SPARE_PARTS||[]));const ud=loadData();sp.forEach(s=>{{if(ud.spareStock&&ud.spareStock[s.name]!==undefined)s.current_stock=ud.spareStock[s.name]}});return sp}}
function getMergedLedger(){{const ledger=JSON.parse(JSON.stringify(LEDGER||{{}}));const ud=loadData();(ud.ledgerDevices||[]).forEach(d=>{{if(d._deleted){{delete ledger[d.machine];return}}ledger[d.machine]={{...ledger[d.machine],...d}}}});return ledger}}
function getMergedKB(){{const kbs=[...(KB||[]).map(k=>({{...k,_source:'system'}}))];const ud=loadData();(ud.kbRecords||[]).forEach(k=>kbs.push({{...k,_source:'user'}}));return kbs}}

// ═══ TAB 0: 角色仪表盘 ═══
function renderRole(){{
  const wos=getMergedWO(),pmData=PM||[],sp=getMergedSpare(),kbs=getMergedKB();
  const overdueWO=wos.filter(w=>w.is_overdue).length,overduePM=pmData.filter(p=>p.status==='超期').length;
  const lowStock=sp.filter(s=>s.current_stock<s.safety_stock).length;
  const sc={{}};Object.values(getMergedStatus()).forEach(m=>{{sc[m.status]=sc[m.status]||0;sc[m.status]++}});
  document.getElementById('roleGrid').innerHTML=
  '<div class="role-col"><h3>🔧 设备工程师</h3>'+
    '<div class="role-item">🔴 超期工单<span class="val" style="color:var(--red)">'+overdueWO+'</span></div>'+
    '<div class="role-item">🛡️ PM到期/超期<span class="val" style="color:var(--orange)">'+overduePM+'</span></div>'+
    '<div class="role-item">📦 备件库存不足<span class="val" style="color:var(--orange)">'+lowStock+'</span></div>'+
    '<div class="role-item">🔧 待处理工单<span class="val">'+wos.filter(w=>w.stage!=='结案').length+'</span></div>'+
    '<div class="role-item">📚 知识库条目<span class="val">'+kbs.length+'</span></div>'+
  '</div>'+
  '<div class="role-col"><h3>📊 维修主管</h3>'+
    '<div class="role-item">📝 待报修<span class="val">'+wos.filter(w=>w.stage==='报修').length+'</span></div>'+
    '<div class="role-item">🔍 排查中<span class="val" style="color:var(--orange)">'+wos.filter(w=>w.stage==='排查').length+'</span></div>'+
    '<div class="role-item">⚙️ 处理中<span class="val" style="color:var(--purple)">'+wos.filter(w=>w.stage==='处理').length+'</span></div>'+
    '<div class="role-item">🔵 待验证<span class="val" style="color:var(--blue)">'+wos.filter(w=>w.stage==='验证').length+'</span></div>'+
    '<div class="role-item">✅ 本月结案<span class="val" style="color:var(--green)">'+wos.filter(w=>w.stage==='结案').length+'</span></div>'+
  '</div>'+
  '<div class="role-col"><h3>🏭 管理层</h3>'+
    '<div class="role-item">🔴 异常机台<span class="val" style="color:var(--red)">'+(sc['异常']||0)+'</span></div>'+
    '<div class="role-item">📊 工单总数<span class="val">'+wos.length+'</span></div>'+
    '<div class="role-item">🔧 维修中<span class="val" style="color:var(--purple)">'+(sc['维修中']||0)+'</span></div>'+
    '<div class="role-item">📚 知识复用率<span class="val">'+(kbs.length>0?Math.round(wos.filter(w=>w.kb_linked).length/wos.length*100):0)+'%</span></div>'+
    '<div class="role-item">⏱️ 累计停机<span class="val">'+(ANOMALY?.summary?.total_downtime_hours||'-')+'h</span></div>'+
  '</div>';
}}

// ═══ TAB 1: 设备状态 v6.0 ═══
function renderStatus(){{
  const ms=getMergedStatus();const sc={{}};Object.values(ms).forEach(m=>{{sc[m.status]=sc[m.status]||0;sc[m.status]++}});
  document.getElementById('statusKPIs').innerHTML='<div class="kpi"><div class="lbl">📋 总数</div><div class="val">'+Object.keys(ms).length+'</div></div>'+['正常','注意','异常','维修中','待保养'].map((s,i)=>'<div class="kpi" style="border-left:3px solid var('+['green','orange','red','purple','blue'][i]+')"><div class="lbl">'+s+'</div><div class="val" style="color:var('+['green','orange','red','purple','blue'][i]+')">'+(sc[s]||0)+'</div></div>').join('');
  const search=(document.getElementById('statusSearch')?.value||'').toLowerCase(),sf=(document.getElementById('statusFilter')?.value||''),tf=(document.getElementById('typeFilter')?.value||'');
  const types=[...new Set(Object.values(ms).map(m=>m.type_name))].sort();document.getElementById('typeFilter').innerHTML='<option value="">全部类型</option>'+types.map(t=>'<option>'+t+'</option>').join('');
  let filtered=Object.values(ms).filter(m=>{{if(search&&!m.machine.toLowerCase().includes(search)&&!m.type_name.includes(search))return false;if(sf&&m.status!==sf)return false;if(tf&&m.type_name!==tf)return false;return true}});
  const groups={{}};filtered.forEach(m=>{{if(!groups[m.type_name])groups[m.type_name]=[];groups[m.type_name].push(m)}});
  let html='';Object.keys(groups).sort().forEach(g=>{{
    html+='<div class="status-group"><h3>📂 '+g+' ('+groups[g].length+')</h3><div class="status-grid">';
    groups[g].forEach(m=>{{
      html+='<div class="status-card" style="border-left-color:'+m.status_color+'"><div style="display:flex;justify-content:space-between;align-items:start"><div><div style="font-size:1rem;font-weight:700">'+m.machine+'</div><div style="font-size:.7rem;color:var(--dim)">'+m.type_name+'</div></div><div style="display:flex;gap:4px;flex-direction:column;align-items:flex-end"><span class="badge" style="background:'+m.status_color+'22;color:'+m.status_color+'">'+m.status+'</span><button class="btn-sm btn-status" onclick="event.stopPropagation();changeStatus(\\''+m.machine+'\\')">⚙ 更改</button></div></div><div style="display:flex;gap:8px;margin-top:8px;font-size:.66rem"><span style="background:rgba(255,255,255,.03);padding:3px 8px;border-radius:4px">异常<span style="font-weight:700;margin-left:3px">'+(m.total_events||0)+'</span></span><span style="background:rgba(255,255,255,.03);padding:3px 8px;border-radius:4px">最近<span style="font-weight:700;margin-left:3px">'+(m.last_event_date||'-')+'</span></span></div></div>';
    }});
    html+='</div></div>';
  }});
  document.getElementById('statusCards').innerHTML=html||'<p style="color:var(--dim);padding:20px">无匹配设备</p>';
}}

function changeStatus(machine){{
  const ms=getMergedStatus(),m=ms[machine];if(!m)return;
  const statuses=['正常','注意','异常','维修中','待保养'];
  openModal('<h3>⚙ 更改设备状态: '+machine+'</h3><div class="modal-row"><label>当前状态</label><span class="badge" style="background:'+m.status_color+'22;color:'+m.status_color+'">'+m.status+'</span></div><div class="modal-row"><label>新状态</label><select id="newStatus">'+statuses.map(s=>'<option '+(s===m.status?'selected':'')+'>'+s+'</option>').join('')+'</select></div><div class="modal-row"><label>备注</label><input id="statusNote" placeholder="状态变更原因..."></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveStatus(\\''+machine+'\\')">✅ 保存</button></div>');
}}

function saveStatus(machine){{
  const s=document.getElementById('newStatus').value,colors={{'正常':'#00b050','注意':'#f59e0b','异常':'#ef4444','维修中':'#bc8cff','待保养':'#58a6ff'}};
  const ud=loadData();ud.machineStatus[machine]={{status:s,status_color:colors[s]}};saveData(ud);
  closeModal();renderStatus();showToast('✅ '+machine+' 状态已更新为 '+s);
}}

// ═══ TAB 2: 事件溯源 ═══
function renderTrace(){{
  const ms=getMergedStatus(),an=ANOMALY||{{}};
  const machines=Object.entries(ms).sort((a,b)=>b[1].total_events-a[1].total_events);
  const topMachine=machines[0]?.[1];
  document.getElementById('traceKPIs').innerHTML=
    '<div class="kpi"><div class="lbl">📊 设备总数</div><div class="val">'+machines.length+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--red)"><div class="lbl">🔴 最高故障</div><div class="val" style="font-size:1rem;color:var(--red)">'+(topMachine?.machine||'-')+'</div><div class="sub">'+(topMachine?.total_events||0)+'次</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--orange)"><div class="lbl">🏷️ 主要类别</div><div class="val" style="font-size:1rem;color:var(--orange)">'+(an.summary?.top_category?.[0]||'-')+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--purple)"><div class="lbl">⏱️ 总停机</div><div class="val">'+(an.summary?.total_downtime_hours||0)+'h</div></div>';
  const types=[...new Set(machines.map(([_,d])=>d.type_name))];document.getElementById('traceType').innerHTML='<option value="">全部类型</option>'+types.map(t=>'<option>'+t+'</option>').join('');
  const search=(document.getElementById('traceSearch')?.value||'').toLowerCase(),type=(document.getElementById('traceType')?.value||'');
  let data=machines.filter(([m,d])=>{{if(search&&!m.toLowerCase().includes(search))return false;if(type&&d.type_name!==type)return false;return true}});
  document.getElementById('traceTable').innerHTML='<table><thead><tr><th>机台</th><th>类型</th><th>异常次数</th><th>装置异常</th><th>PM</th><th>主要故障</th><th>最近异常</th><th>状态</th></tr></thead><tbody>'+data.map(([m,d])=>'<tr><td><strong>'+m+'</strong></td><td>'+d.type_name+'</td><td><span class="badge '+(d.total_events>50?'badge-red':d.total_events>20?'badge-orange':'badge-green')+'">'+d.total_events+'</span></td><td>'+d.device_anomaly_count+'</td><td>'+d.pm_count+'</td><td>'+d.top_category+'</td><td>'+d.last_event_date+'</td><td><span class="badge" style="background:'+d.status_color+'22;color:'+d.status_color+'">'+d.status+'</span></td></tr>').join('')+'</tbody></table>';
  setTimeout(()=>{{
    const top15=machines.slice(0,15);
    const cats=Object.entries(an.categories||{{}}).sort((a,b)=>b[1]-a[1]).slice(0,6);
    chartInstances.push(new Chart(document.getElementById('cEventRank'),{{type:'bar',data:{{labels:top15.map(([m])=>m),datasets:[{{data:top15.map(([,d])=>d.total_events),backgroundColor:top15.map(([,d])=>d.total_events>50?'#ff4444':d.total_events>20?'#ffa500':'#58a6ff')}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,resizeDelay:100,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:'#8b949e'}}}},y:{{ticks:{{color:'#8b949e',font:{{size:9}}}}}}}}}}}}));
    chartInstances.push(new Chart(document.getElementById('cCategoryShift'),{{type:'doughnut',data:{{labels:cats.map(c=>c[0]),datasets:[{{data:cats.map(c=>c[1]),backgroundColor:['#ff4444','#ffa500','#58a6ff','#00b050','#bc8cff','#39d2c0']}}]}},options:{{responsive:true,maintainAspectRatio:true,resizeDelay:100,plugins:{{legend:{{position:'right',labels:{{color:'#8b949e',font:{{size:9}},padding:6}}}}}}}}}}));
  }},100);
}}

// ═══ TAB 3: PDCA工单 v6.0 ═══
const PDCA_STAGES=['报修','排查','定因','处理','验证','结案'];
const PDCA_COLORS=['#ff4444','#ffa500','#ffc000','#bc8cff','#58a6ff','#00b050'];

function renderWO(){{
  const wos=getMergedWO();
  document.getElementById('woKPIs').innerHTML='<div class="kpi"><div class="lbl">📝 工单总数</div><div class="val">'+wos.length+'</div><div class="sub">超期 '+wos.filter(w=>w.is_overdue).length+' 条</div></div>'+PDCA_STAGES.map((s,i)=>'<div class="kpi" style="border-left:2px solid '+PDCA_COLORS[i]+'"><div class="lbl">'+s+'</div><div class="val" style="color:'+PDCA_COLORS[i]+'">'+wos.filter(w=>w.stage===s).length+'</div></div>').join('');
  // 看板
  let board='<div class="pdca-board">';
  PDCA_STAGES.forEach((s,i)=>{{
    const items=wos.filter(w=>w.stage===s).slice(0,12);
    board+='<div class="pdca-col"><h4 style="color:'+PDCA_COLORS[i]+'">'+s+' ('+items.length+')</h4>';
    items.forEach(w=>{{
      const urgColor=w.urgency==='特急'?'#ff4444':w.urgency==='紧急'?'#ffa500':'#00b050';
      board+='<div class="pdca-card" onclick="advanceWO(\\''+w.id+'\\',\\''+s+'\\')"><div class="pc-machine">'+w.machine+'</div><div class="pc-cat">'+w.category+'</div><span class="pc-urg" style="background:'+urgColor+'22;color:'+urgColor+'">'+w.urgency+'</span>'+(w.is_overdue?' 🔴':'')+'</div>';
    }});
    board+='</div>';
  }});
  board+='</div>';
  document.getElementById('pdcaBoard').innerHTML=board;
  // 表格
  const search=(document.getElementById('woSearch')?.value||'').toLowerCase(),stageF=(document.getElementById('woStage')?.value||''),overdueOnly=document.getElementById('woOverdue')?.checked;
  let data=wos.filter(w=>{{if(search&&!w.machine.toLowerCase().includes(search)&&!w.id.toLowerCase().includes(search))return false;if(stageF&&w.stage!==stageF)return false;if(overdueOnly&&!w.is_overdue)return false;return true}}).slice(0,50);
  document.getElementById('woBody').innerHTML=data.map(w=>'<tr style="'+(w.is_overdue?'background:rgba(255,68,68,.05)':'')+'"><td style="font-family:monospace;font-size:.66rem">'+w.id+'</td><td><strong>'+w.machine+'</strong></td><td><span class="badge badge-blue">'+w.category+'</span></td><td><span class="badge '+(w.urgency==='特急'?'badge-red':w.urgency==='紧急'?'badge-orange':'badge-green')+'">'+w.urgency+'</span></td><td><span class="badge" style="background:'+(PDCA_COLORS[PDCA_STAGES.indexOf(w.stage)]||'#30363d')+'22;color:'+(PDCA_COLORS[PDCA_STAGES.indexOf(w.stage)]||'#30363d')+'">'+w.stage+'</span></td><td style="font-size:.68rem">'+(w.root_cause||'-')+'</td><td>'+(w.verify_result?'<span class="badge '+(w.verify_result==='通过'?'badge-green':'badge-red')+'">'+w.verify_result+'</span>':'-')+'</td><td>'+w.duration_h+'h</td><td><button class="btn-sm btn-edit" onclick="advanceWO(\\''+w.id+'\\',\\''+w.stage+'\\')">▶推进</button></td></tr>').join('');
}}

function newWorkOrder(){{
  const machines=Object.keys(getMergedStatus()).sort();
  openModal('<h3>🔧 新建故障报修工单</h3><div class="modal-row"><label>机台</label><select id="nwoMachine">'+machines.map(m=>'<option>'+m+'</option>').join('')+'</select></div><div class="modal-row"><label>故障类别</label><select id="nwoCat"><option>设备装置异常</option><option>工艺条件异常</option><option>耗材消耗</option><option>PM</option><option>软件异常</option><option>其他</option></select></div><div class="modal-row"><label>紧急度</label><select id="nwoUrg"><option>普通</option><option>紧急</option><option selected>特急</option></select></div><div class="modal-row"><label>故障描述</label><textarea id="nwoDesc" placeholder="详细描述故障现象..."></textarea></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-danger" onclick="createWO()">🚨 提交报修</button></div>');
}}

function createWO(){{
  const m=document.getElementById('nwoMachine').value,desc=document.getElementById('nwoDesc').value.trim();
  if(!m||!desc){{showToast('⚠️ 请填写机台和故障描述');return}}
  const ud=loadData(),id='WO-'+Date.now().toString(36).toUpperCase();
  ud.workOrders.push({{id,machine:m,category:document.getElementById('nwoCat').value,urgency:document.getElementById('nwoUrg').value,stage:'报修',description:desc,root_cause:'',verify_result:'',duration_h:0,kb_linked:false,is_overdue:false,_source:'user',created:new Date().toISOString().split('T')[0]}});
  saveData(ud);closeModal();renderWO();showToast('🚨 报修工单 '+id+' 已创建');
}}

function advanceWO(woId,curStage){{
  const idx=PDCA_STAGES.indexOf(curStage);
  if(idx>=5){{showToast('⚠️ 已是最终阶段');return}}
  const nextStage=PDCA_STAGES[idx+1];
  const forms={{
    '排查':'<div class="modal-row"><label>排查过程</label><textarea id="woDiag" placeholder="详细排查步骤..."></textarea></div>',
    '定因':'<div class="modal-row"><label>根因分析</label><input id="woRoot" placeholder="根本原因"><br><label>故障类别</label><select id="woCat"><option>设备装置异常</option><option>工艺条件异常</option><option>耗材消耗</option><option>PM</option><option>软件异常</option><option>其他</option></select></div>',
    '处理':'<div class="modal-row"><label>处理方法</label><textarea id="woSolution" placeholder="处理步骤描述..."></textarea><br><label>处理人</label><input id="woHandler"><br><label>耗时(h)</label><input type="number" id="woHours" value="0.5" step="0.5"></div>',
    '验证':'<div class="modal-row"><label>验证结果</label><select id="woVerify"><option>通过</option><option>不通过(退回处理)</option></select><br><label>验证人</label><input id="woVerifier"></div>',
    '结案':'<div class="modal-row"><label>结案备注</label><textarea id="woClose"></textarea></div>'
  }};
  openModal('<h3>'+woId+' → '+nextStage+'</h3>'+(forms[nextStage]||'')+'<div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveWOAdvance(\\''+woId+'\\',\\''+nextStage+'\\')">✅ 推进到 '+nextStage+'</button></div>');
}}

function saveWOAdvance(woId,stage){{
  const ud=loadData();let wo=ud.workOrders.find(w=>w.id===woId);
  if(!wo){{wo={{id:woId,_source:'edited'}};ud.workOrders.push(wo)}}
  wo.stage=stage;wo.stage_changed=new Date().toISOString().split('T')[0];
  if(stage==='排查')wo.diagnosis=document.getElementById('woDiag')?.value||'';
  if(stage==='定因'){{wo.root_cause=document.getElementById('woRoot')?.value||'';wo.category=document.getElementById('woCat')?.value||wo.category}}
  if(stage==='处理'){{wo.solution=document.getElementById('woSolution')?.value||'';wo.handler=document.getElementById('woHandler')?.value||'';wo.duration_h=parseFloat(document.getElementById('woHours')?.value)||0}}
  if(stage==='验证'){{wo.verify_result=document.getElementById('woVerify')?.value||'';wo.verifier=document.getElementById('woVerifier')?.value||''}}
  if(stage==='结案')wo.closed_date=new Date().toISOString().split('T')[0];
  saveData(ud);closeModal();renderWO();showToast('✅ '+woId+' → '+stage);
}}

// ═══ TAB 4: 保养 ═══
function renderPM(){{
  if(!PM||!PM.length)return;
  const ud=loadData(),pmRecords=ud.pmRecords||[];
  const overdue=PM.filter(p=>p.status==='超期').length;
  document.getElementById('pmKPIs').innerHTML='<div class="kpi"><div class="lbl">📋 计划</div><div class="val">'+PM.length+'</div></div><div class="kpi" style="border-left:3px solid var(--red)"><div class="lbl">🔴 超期</div><div class="val" style="color:var(--red)">'+overdue+'</div></div><div class="kpi" style="border-left:3px solid var(--green)"><div class="lbl">✅ 已完成(月)</div><div class="val" style="color:var(--green)">'+pmRecords.length+'</div></div>';
  const search=(document.getElementById('pmSearch')?.value||'').toLowerCase(),status=(document.getElementById('pmStatus')?.value||'');
  let data=PM.filter(p=>{{if(search&&!p.machine.toLowerCase().includes(search))return false;if(status&&p.status!==status)return false;return true}});
  let html='<div style="margin-bottom:8px;display:flex;gap:6px"><button class="btn-primary" onclick="newPMChecklist()">📋 新建保养Checklist</button></div>';
  html+='<table><thead><tr><th>机台</th><th>类型</th><th>保养</th><th>下次</th><th>剩余</th><th>负责人</th><th>状态</th><th>操作</th></tr></thead><tbody>';
  html+=data.map(p=>'<tr><td><strong>'+p.machine+'</strong></td><td>'+p.type_name+'</td><td>'+p.pm_type+'</td><td>'+p.next_pm_date+'</td><td style="font-weight:700;color:'+(p.days_until_pm<0?'var(--red)':'var(--green)')+'">'+(p.days_until_pm<0?'超期'+Math.abs(p.days_until_pm)+'天':p.days_until_pm+'天')+'</td><td>'+p.responsible+'</td><td><span class="badge '+(p.status==='超期'?'badge-red':p.status==='本周'?'badge-orange':'badge-green')+'">'+p.status+'</span></td><td style="display:flex;gap:3px"><button class="btn-sm btn-edit" onclick="execPM(\\''+p.machine+'\\',\\''+p.pm_type+'\\')">✅执行</button><button class="btn-sm btn-status" onclick="editPMChecklist(\\''+p.machine+'\\')">📋清单</button></td></tr>').join('');
  html+='</tbody></table>';
  if(pmRecords.length>0){{
    html+='<h4 style="margin-top:12px;font-size:.7rem;color:var(--dim)">📋 最近PM执行记录</h4><div class="scroll-table" style="max-height:200px"><table><tr><th>日期</th><th>机台</th><th>类型</th><th>执行人</th></tr>'+pmRecords.slice(-10).reverse().map(r=>'<tr><td>'+r.date+'</td><td>'+r.machine+'</td><td>'+r.pm_type+'</td><td>'+r.executor+'</td></tr>').join('')+'</table></div>';
  }}
  document.getElementById('pmTable').innerHTML=html;
}}

function newPMChecklist(){{
  const machines=Object.keys(getMergedStatus()).sort();
  openModal('<h3>📋 新建保养Checklist</h3><div class="modal-row"><label>机台</label><select id="pmclMachine">'+machines.map(m=>'<option>'+m+'</option>').join('')+'</select></div><div class="modal-row"><label>PM类型</label><select id="pmclType"><option>周检</option><option>月检</option><option>季检</option><option>年检</option></select></div><div class="modal-row"><label>检查项(每行一项)</label><textarea id="pmclItems" placeholder="外观检查\\n功能测试\\n耗材更换\\n参数校准"></textarea></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="savePMChecklist()">✅ 创建</button></div>');
}}

function savePMChecklist(){{
  const m=document.getElementById('pmclMachine').value,itemsStr=document.getElementById('pmclItems').value.trim();
  if(!m||!itemsStr){{showToast('⚠️ 请填写机台和检查项');return}}
  const items=itemsStr.split('\\n').filter(s=>s.trim()).map(s=>({{name:s.trim(),checked:false,result:'',note:''}}));
  const ud=loadData();ud.pmChecklists[m+'_'+document.getElementById('pmclType').value]={{machine:m,pm_type:document.getElementById('pmclType').value,items,created:new Date().toISOString().split('T')[0]}};saveData(ud);
  closeModal();showToast('✅ Checklist已创建');
}}

function editPMChecklist(machine){{
  const ud=loadData(),keys=Object.keys(ud.pmChecklists||{{}}).filter(k=>k.startsWith(machine+'_'));
  if(!keys.length){{showToast('⚠️ 该机台无checklist，请先创建');return}}
  const key=keys[0],cl=ud.pmChecklists[key];
  let itemsHtml=cl.items.map((it,i)=>'<div class="checklist-item"><input type="checkbox" '+(it.checked?'checked':'')+' id="pmi_'+i+'"><span class="check-label">'+it.name+'</span><div class="check-result"><select id="pmir_'+i+'"><option '+(it.result==='正常'?'selected':'')+'>正常</option><option '+(it.result==='异常'?'selected':'')+'>异常</option><option '+(it.result==='待观察'?'selected':'')+'>待观察</option></select></div><input style="width:80px;font-size:.62rem" id="pmin_'+i+'" placeholder="备注" value="'+(it.note||'')+'"></div>').join('');
  openModal('<h3>📋 '+machine+' — '+cl.pm_type+' Checklist</h3>'+itemsHtml+'<div class="modal-row" style="margin-top:8px"><label>执行人</label><input id="pmExecutor" placeholder="工程师姓名"></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="savePMExec(\\''+key+'\\')">✅ 保存执行记录</button></div>');
}}

function savePMExec(key){{
  const ud=loadData(),cl=ud.pmChecklists[key];if(!cl)return;
  cl.items.forEach((it,i)=>{{it.checked=document.getElementById('pmi_'+i)?.checked||false;it.result=document.getElementById('pmir_'+i)?.value||'';it.note=document.getElementById('pmin_'+i)?.value||''}});
  ud.pmRecords.push({{checklist_key:key,machine:cl.machine,pm_type:cl.pm_type,items:JSON.parse(JSON.stringify(cl.items)),executor:document.getElementById('pmExecutor')?.value||'',date:new Date().toISOString().split('T')[0]}});
  saveData(ud);closeModal();renderPM();showToast('✅ PM执行记录已保存');
}}

function execPM(machine,pmType){{
  const ud=loadData();ud.pmRecords.push({{machine,pm_type:pmType,items:[],executor:'',date:new Date().toISOString().split('T')[0],_quick:true}});saveData(ud);renderPM();showToast('✅ '+machine+' PM快速确认完成');
}}

// ═══ TAB 5: 备品备件 ═══
function renderSP(){{
  const sp=getMergedSpare();
  const low=sp.filter(s=>s.current_stock<s.safety_stock).length,out=sp.filter(s=>s.current_stock<=0).length;
  document.getElementById('spKPIs').innerHTML='<div class="kpi"><div class="lbl">📦 种类</div><div class="val">'+sp.length+'</div></div><div class="kpi" style="border-left:3px solid var(--orange)"><div class="lbl">⚠️ 低库存</div><div class="val" style="color:var(--orange)">'+low+'</div></div><div class="kpi" style="border-left:3px solid var(--red)"><div class="lbl">❌ 缺货</div><div class="val" style="color:var(--red)">'+out+'</div></div>';
  const search=(document.getElementById('spSearch')?.value||'').toLowerCase(),status=(document.getElementById('spStatus')?.value||''),critical=document.getElementById('spCritical')?.checked;
  let data=sp.filter(s=>{{if(search&&!s.name.toLowerCase().includes(search))return false;if(status==='正常'&&s.current_stock<s.safety_stock)return false;if(status==='低库存'&&s.current_stock>=s.safety_stock)return false;if(status==='缺货'&&s.current_stock>0)return false;if(critical&&!s.is_critical)return false;return true}});
  let html='<div style="margin-bottom:8px;display:flex;gap:6px"><button class="btn-sm btn-edit" onclick="spareIn()">📥 入库</button><button class="btn-sm" style="background:var(--orange);color:#fff" onclick="spareOut()">📤 出库</button></div>';
  html+='<table><thead><tr><th>备件</th><th>型号</th><th>库存</th><th>安全</th><th>关键件</th><th>状态</th><th>操作</th></tr></thead><tbody>';
  html+=data.map(s=>'<tr><td><strong>'+s.name+'</strong></td><td>'+s.model+'</td><td style="font-weight:700;color:'+(s.current_stock<s.safety_stock?'var(--red)':'var(--green)')+'">'+s.current_stock+'</td><td>'+s.safety_stock+'</td><td>'+(s.is_critical?'⭐关键':'普通')+'</td><td><span class="badge '+(s.current_stock<=0?'badge-red':s.current_stock<s.safety_stock?'badge-orange':'badge-green')+'">'+(s.current_stock<=0?'缺货':s.current_stock<s.safety_stock?'低库存':'正常')+'</span></td><td><button class="btn-sm btn-edit" onclick="spareAdjust(\''+s.name+'\','+s.current_stock+')">✏调整</button></td></tr>').join('');
  html+='</tbody></table>';
  const ud=loadData(),movs=(ud.spareMovements||[]).slice(-20).reverse();
  if(movs.length>0)html+='<h4 style="margin-top:12px;font-size:.7rem;color:var(--dim)">📋 最近出入库记录</h4><div class="inventory-log"><table><tr><th>时间</th><th>备件</th><th>类型</th><th>数量</th><th>经手人</th></tr>'+movs.map(mv=>'<tr><td>'+mv.date+'</td><td>'+mv.name+'</td><td style="color:'+(mv.type==='入库'?'var(--green)':'var(--orange)')+'">'+mv.type+'</td><td>'+mv.qty+'</td><td>'+mv.handler+'</td></tr>').join('')+'</table></div>';
  document.getElementById('spTable').innerHTML=html;
}}

function spareIn(){{
  const sp=getMergedSpare();
  openModal('<h3>📥 备件入库</h3><div class="modal-row"><label>备件</label><select id="siName">'+sp.map(s=>'<option>'+s.name+'</option>').join('')+'</select></div><div class="modal-row"><label>数量</label><input type="number" id="siQty" value="1" min="1"></div><div class="modal-row"><label>经手人</label><input id="siHandler"></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveSpareIn()">✅ 确认入库</button></div>');
}}

function saveSpareIn(){{
  const name=document.getElementById('siName').value,qty=parseInt(document.getElementById('siQty').value)||0,handler=document.getElementById('siHandler').value.trim();
  if(!qty||!handler){{showToast('⚠️ 请填写数量和经手人');return}}
  const ud=loadData();ud.spareStock[name]=(ud.spareStock[name]||(SPARE_PARTS.find(s=>s.name===name)?.current_stock||0))+qty;
  ud.spareMovements.push({{name,type:'入库',qty,handler,date:new Date().toISOString().split('T')[0]}});
  saveData(ud);closeModal();renderSP();showToast('📥 '+name+' 入库 +'+qty);
}}

function spareOut(){{
  const sp=getMergedSpare();
  openModal('<h3>📤 备件出库</h3><div class="modal-row"><label>备件</label><select id="soName">'+sp.map(s=>'<option>'+s.name+'</option>').join('')+'</select></div><div class="modal-row"><label>数量</label><input type="number" id="soQty" value="1" min="1"></div><div class="modal-row"><label>机台</label><select id="soMachine"><option value="">通用</option>'+Object.keys(getMergedStatus()).sort().map(m=>'<option>'+m+'</option>').join('')+'</select></div><div class="modal-row"><label>经手人</label><input id="soHandler"></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveSpareOut()">✅ 确认出库</button></div>');
}}

function saveSpareOut(){{
  const name=document.getElementById('soName').value,qty=parseInt(document.getElementById('soQty').value)||0,handler=document.getElementById('soHandler').value.trim(),machine=document.getElementById('soMachine').value;
  if(!qty||!handler){{showToast('⚠️ 请填写数量和经手人');return}}
  const ud=loadData();ud.spareStock[name]=(ud.spareStock[name]||(SPARE_PARTS.find(s=>s.name===name)?.current_stock||0))-qty;
  ud.spareMovements.push({{name,type:'出库',qty,handler,machine,date:new Date().toISOString().split('T')[0]}});
  saveData(ud);closeModal();renderSP();showToast('📤 '+name+' 出库 -'+qty);
}}

function spareAdjust(name,curStock){{
  openModal('<h3>✏ 调整库存: '+name+'</h3><div class="modal-row"><label>当前库存</label><span>'+curStock+'</span></div><div class="modal-row"><label>新库存</label><input type="number" id="saStock" value="'+curStock+'"></div><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveSpareAdj(\''+name+'\')">✅ 保存</button></div>');
}}

function saveSpareAdj(name){{
  const val=parseInt(document.getElementById('saStock').value);if(isNaN(val)){{showToast('⚠️ 请输入有效数字');return}}
  const ud=loadData();ud.spareStock[name]=val;saveData(ud);closeModal();renderSP();showToast('✅ '+name+' 库存已更新为 '+val);
}}

// ═══ TAB 6: 设备台账 ═══
function renderLedger(){{
  const ledger=getMergedLedger(),machines=Object.entries(ledger);
  const types=[...new Set(machines.map(([_,d])=>d.type_group))];document.getElementById('ledgerType').innerHTML='<option value="">全部类型</option>'+types.map(t=>'<option>'+t+'</option>').join('');
  const search=(document.getElementById('ledgerSearch')?.value||'').toLowerCase(),type=(document.getElementById('ledgerType')?.value||'');
  let data=machines.filter(([m,d])=>{{if(search&&!m.toLowerCase().includes(search)&&!(d.manufacturer||'').toLowerCase().includes(search))return false;if(type&&d.type_group!==type)return false;return true}});
  document.getElementById('ledgerKPIs').innerHTML='<div class="kpi"><div class="lbl">📋 在册</div><div class="val">'+machines.length+'</div></div><div class="kpi"><div class="lbl">✅ 运行</div><div class="val" style="color:var(--green)">'+machines.filter(([_,d])=>d.status==='运行').length+'</div></div>';
  let html='<div style="margin-bottom:8px"><button class="btn-primary" onclick="newDevice()">➕ 新增设备</button></div>';
  html+='<table><thead><tr><th>编号</th><th>名称</th><th>型号</th><th>厂商</th><th>S/N</th><th>位置</th><th>负责人</th><th>进厂</th><th>状态</th><th>操作</th></tr></thead><tbody>';
  html+=data.map(([m,d])=>'<tr><td><strong>'+m+'</strong></td><td>'+d.type_name+'</td><td>'+(d.model||'-')+'</td><td>'+(d.manufacturer||'-')+'</td><td style="font-size:.62rem;font-family:monospace">'+(d.serial_no||'-')+'</td><td>'+(d.location||'-')+'</td><td>'+(d.responsible||'-')+'</td><td>'+(d.purchase_date||'-')+'</td><td><span class="badge '+(d.status==='运行'?'badge-green':'badge-purple')+'">'+(d.status||'-')+'</span></td><td style="display:flex;gap:3px"><button class="btn-sm btn-edit" onclick="editDevice(\''+m+'\')">✏编辑</button><button class="btn-sm" style="background:var(--red)" onclick="deleteDevice(\''+m+'\')">🗑</button></td></tr>').join('');
  html+='</tbody></table>';
  document.getElementById('ledgerTable').innerHTML=html;
}}

function newDevice(){{
  openModal('<h3>➕ 新增设备</h3>'+
    '<div class="modal-row"><label>设备编号</label><input id="edId" placeholder="如: AICP03"></div>'+
    '<div class="modal-row"><label>设备名称</label><input id="edName" placeholder="如: ICP刻蚀"></div>'+
    '<div class="modal-row"><label>型号</label><input id="edModel" placeholder="如: ICP-300"></div>'+
    '<div class="modal-row"><label>厂商</label><input id="edMfr" placeholder="如: 应用材料"></div>'+
    '<div class="modal-row"><label>S/N</label><input id="edSN" placeholder="序列号"></div>'+
    '<div class="modal-row"><label>位置</label><input id="edLoc" placeholder="如: FabA-L2-03"></div>'+
    '<div class="modal-row"><label>负责人</label><input id="edResp"></div>'+
    '<div class="modal-row"><label>进厂时间</label><input type="date" id="edDate"></div>'+
    '<div class="modal-row"><label>设备状态</label><select id="edStatus"><option>运行</option><option>停机</option><option>调试</option><option>报废</option></select></div>'+
    '<div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveDevice()">✅ 新增</button></div>');
}}

function saveDevice(){{
  const id=document.getElementById('edId').value.trim();if(!id){{showToast('⚠️ 请填写设备编号');return}}
  const ud=loadData();
  ud.ledgerDevices.push({{machine:id,type_name:document.getElementById('edName').value,model:document.getElementById('edModel').value,manufacturer:document.getElementById('edMfr').value,serial_no:document.getElementById('edSN').value,location:document.getElementById('edLoc').value,responsible:document.getElementById('edResp').value,purchase_date:document.getElementById('edDate').value,status:document.getElementById('edStatus').value,type_group:'',qr_code:'EQ-'+id}});
  saveData(ud);closeModal();renderLedger();showToast('✅ 设备 '+id+' 已录入');
}}

function editDevice(machine){{
  const ledger=getMergedLedger(),d=ledger[machine]||{{}};
  openModal('<h3>✏ 编辑设备: '+machine+'</h3>'+
    '<div class="modal-row"><label>设备名称</label><input id="edName" value="'+(d.type_name||'')+'"></div>'+
    '<div class="modal-row"><label>型号</label><input id="edModel" value="'+(d.model||'')+'"></div>'+
    '<div class="modal-row"><label>厂商</label><input id="edMfr" value="'+(d.manufacturer||'')+'"></div>'+
    '<div class="modal-row"><label>S/N</label><input id="edSN" value="'+(d.serial_no||'')+'"></div>'+
    '<div class="modal-row"><label>位置</label><input id="edLoc" value="'+(d.location||'')+'"></div>'+
    '<div class="modal-row"><label>负责人</label><input id="edResp" value="'+(d.responsible||'')+'"></div>'+
    '<div class="modal-row"><label>进厂时间</label><input type="date" id="edDate" value="'+(d.purchase_date||'')+'"></div>'+
    '<div class="modal-row"><label>设备状态</label><select id="edStatus"><option '+(d.status==='运行'?'selected':'')+'>运行</option><option '+(d.status==='停机'?'selected':'')+'>停机</option><option '+(d.status==='调试'?'selected':'')+'>调试</option><option '+(d.status==='报废'?'selected':'')+'>报废</option></select></div>'+
    '<div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveDeviceEdit(\''+machine+'\')">✅ 保存</button></div>');
}}

function saveDeviceEdit(machine){{
  const ud=loadData();let d=ud.ledgerDevices.find(d=>d.machine===machine);if(!d){{d={{machine}};ud.ledgerDevices.push(d)}}
  d.type_name=document.getElementById('edName').value;d.model=document.getElementById('edModel').value;d.manufacturer=document.getElementById('edMfr').value;d.serial_no=document.getElementById('edSN').value;d.location=document.getElementById('edLoc').value;d.responsible=document.getElementById('edResp').value;d.purchase_date=document.getElementById('edDate').value;d.status=document.getElementById('edStatus').value;
  saveData(ud);closeModal();renderLedger();showToast('✅ '+machine+' 信息已更新');
}}

function deleteDevice(machine){{
  openModal('<h3>⚠️ 确认删除</h3><p style="color:var(--dim);margin:8px 0">确定要删除设备 <strong>'+machine+'</strong> 吗？</p><div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-danger" onclick="confirmDeleteDevice(\''+machine+'\')">🗑 确认删除</button></div>');
}}

function confirmDeleteDevice(machine){{
  const ud=loadData();let d=ud.ledgerDevices.find(d=>d.machine===machine);if(!d){{d={{machine}};ud.ledgerDevices.push(d)}}d._deleted=true;saveData(ud);closeModal();renderLedger();showToast('🗑 '+machine+' 已移除');
}}

// ═══ TAB 7: 知识库 ═══
function renderKB(){{
  const kbs=getMergedKB();
  document.getElementById('kbKPIs').innerHTML='<div class="kpi"><div class="lbl">📚 条目总数</div><div class="val">'+kbs.length+'</div></div><div class="kpi" style="border-left:3px solid var(--blue)"><div class="lbl">👤 用户条目</div><div class="val" style="color:var(--blue)">'+kbs.filter(k=>k._source==='user').length+'</div></div><div class="kpi" style="border-left:3px solid var(--purple)"><div class="lbl">✏ 可编辑</div><div class="val">'+kbs.length+'</div></div>';
  const machines=[...new Set(kbs.map(k=>k.machine))];document.getElementById('kbMachine').innerHTML='<option value="">全部机台</option>'+machines.sort().map(m=>'<option>'+m+'</option>').join('');
  const search=(document.getElementById('kbSearch')?.value||'').toLowerCase(),machine=(document.getElementById('kbMachine')?.value||''),category=(document.getElementById('kbCategory')?.value||'');
  let data=kbs.filter(k=>{{if(search&&!(k.root_cause||'').toLowerCase().includes(search)&&!(k.symptoms||'').toLowerCase().includes(search)&&!k.machine.toLowerCase().includes(search))return false;if(machine&&k.machine!==machine)return false;if(category&&k.category!==category)return false;return true}}).slice(0,30);
  let html='<div style="margin-bottom:8px"><button class="btn-primary" onclick="newKBEntry()">➕ 新增知识条目</button></div>';
  html+=data.map(k=>'<div class="kb-card"><div class="kb-title">'+k.machine+' — '+(k.root_cause||k.symptoms||'')+' <span class="badge badge-blue">'+(k.category||'')+'</span> '+(k._source==='user'?'<span class="badge badge-purple">👤用户</span>':'')+'</div><div class="kb-meta">📅 '+(k.date||'')+' · 👤 '+(k.handler||'')+' · ⏱️ '+(k.duration_h||0)+'h</div><div style="font-size:.66rem;color:var(--dim);margin-top:4px">症状: '+(k.symptoms||'-')+'</div><div class="kb-steps">'+((k.solution_steps||[]).map(s=>'<li>'+s+'</li>').join('')||'')+'</div><div style="font-size:.64rem;color:var(--yellow);margin-top:4px">💡 '+(k.advice_for_next||'')+'</div><div style="margin-top:4px"><button class="btn-sm btn-edit" onclick="editKB(\''+k.id+'\')">✏ 编辑</button></div></div>').join('');
  document.getElementById('kbList').innerHTML=html||'<p style="color:var(--dim);padding:20px">无匹配结果</p>';
}}

function newKBEntry(){{
  const machines=Object.keys(getMergedStatus()).sort();
  openModal('<h3>📚 新增知识条目 — 故障记录模板</h3>'+
    '<div class="modal-row"><label>机台</label><select id="nkbMachine">'+machines.map(m=>'<option>'+m+'</option>').join('')+'</select></div>'+
    '<div class="modal-row"><label>日期</label><input type="date" id="nkbDate" value="'+new Date().toISOString().split('T')[0]+'"></div>'+
    '<div class="modal-row"><label>故障类别</label><select id="nkbCat"><option>设备装置异常</option><option>工艺条件异常</option><option>耗材消耗</option><option>PM</option><option>软件异常</option><option>其他</option></select></div>'+
    '<div class="modal-row"><label>故障现象</label><textarea id="nkbSymp" placeholder="描述故障现象..."></textarea></div>'+
    '<div class="modal-row"><label>根因分析</label><input id="nkbRoot" placeholder="根本原因"></div>'+
    '<div class="modal-row"><label>解决步骤(每行一步)</label><textarea id="nkbSteps" placeholder="步骤1: ...\\n步骤2: ..."></textarea></div>'+
    '<div class="modal-row"><label>预防建议</label><textarea id="nkbAdvice" placeholder="下次如何避免..."></textarea></div>'+
    '<div class="modal-row"><label>处理人</label><input id="nkbHandler" placeholder="工程师姓名"></div>'+
    '<div class="modal-row"><label>耗时(h)</label><input type="number" id="nkbHours" value="1" step="0.5"></div>'+
    '<div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveKBEntry()">✅ 保存条目</button></div>');
}}

function saveKBEntry(){{
  const m=document.getElementById('nkbMachine').value,symp=document.getElementById('nkbSymp').value.trim(),root=document.getElementById('nkbRoot').value.trim();
  if(!m||!symp||!root){{showToast('⚠️ 请填写机台、故障现象和根因');return}}
  const ud=loadData();
  ud.kbRecords.push({{id:'KB-'+Date.now().toString(36).toUpperCase(),machine:m,date:document.getElementById('nkbDate').value,category:document.getElementById('nkbCat').value,symptoms:symp,root_cause:root,solution_steps:document.getElementById('nkbSteps').value.split('\\n').filter(s=>s.trim()),advice_for_next:document.getElementById('nkbAdvice').value,handler:document.getElementById('nkbHandler').value,duration_h:parseFloat(document.getElementById('nkbHours').value)||0,_source:'user'}});
  saveData(ud);closeModal();renderKB();showToast('📚 知识条目已保存');
}}

function editKB(kbId){{
  const kbs=getMergedKB(),k=kbs.find(k=>k.id===kbId);if(!k)return;
  const steps=(k.solution_steps||[]).join('\\n');
  openModal('<h3>✏ 编辑知识条目: '+kbId+'</h3>'+
    '<div class="modal-row"><label>机台</label><input id="ekbMachine" value="'+(k.machine||'')+'"></div>'+
    '<div class="modal-row"><label>故障类别</label><select id="ekbCat"><option '+(k.category==='设备装置异常'?'selected':'')+'>设备装置异常</option><option '+(k.category==='工艺条件异常'?'selected':'')+'>工艺条件异常</option><option '+(k.category==='耗材消耗'?'selected':'')+'>耗材消耗</option><option '+(k.category==='PM'?'selected':'')+'>PM</option><option '+(k.category==='软件异常'?'selected':'')+'>软件异常</option><option '+(k.category==='其他'?'selected':'')+'>其他</option></select></div>'+
    '<div class="modal-row"><label>故障现象</label><textarea id="ekbSymp">'+(k.symptoms||'')+'</textarea></div>'+
    '<div class="modal-row"><label>根因分析</label><input id="ekbRoot" value="'+(k.root_cause||'')+'"></div>'+
    '<div class="modal-row"><label>解决步骤</label><textarea id="ekbSteps">'+steps+'</textarea></div>'+
    '<div class="modal-row"><label>预防建议</label><textarea id="ekbAdvice">'+(k.advice_for_next||'')+'</textarea></div>'+
    '<div class="modal-btns"><button class="btn-secondary" onclick="closeModal()">取消</button><button class="btn-primary" onclick="saveKBEdit(\''+kbId+'\')">✅ 保存</button></div>');
}}

function saveKBEdit(kbId){{
  const ud=loadData();let k=ud.kbRecords.find(k=>k.id===kbId);if(!k){{k={{id:kbId,_source:'edited'}};ud.kbRecords.push(k)}}
  k.machine=document.getElementById('ekbMachine').value;k.category=document.getElementById('ekbCat').value;k.symptoms=document.getElementById('ekbSymp').value;k.root_cause=document.getElementById('ekbRoot').value;k.solution_steps=document.getElementById('ekbSteps').value.split('\\n').filter(s=>s.trim());k.advice_for_next=document.getElementById('ekbAdvice').value;
  saveData(ud);closeModal();renderKB();showToast('✅ 知识条目已更新');
}}

// ═══ TAB 8: 黑天鹅 ═══
function renderBlackSwan(){{
  if(!BS){{document.getElementById('bsEvents').innerHTML='<p style="color:var(--dim);padding:20px">数据加载中...</p>';return}}
  const s=BS.summary||{{}},eb=BS.error_budgets||[],cm=BS.cluster_mutations||[],be=BS.blackswan_events||[],cd=BS.chaos_drills||[];
  const criticalEbs=eb.filter(e=>e.status==='critical').length;
  document.getElementById('bsKPIs').innerHTML=
    '<div class="kpi" style="border-left:3px solid var(--red)"><div class="lbl">🔴 未知异常(月)</div><div class="val" style="color:var(--red)">'+(s.unknown_anomalies_this_month||0)+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--orange)"><div class="lbl">🆕 首次故障</div><div class="val" style="color:var(--orange)">'+(s.first_occurrence_count||0)+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--red)"><div class="lbl">💣 预算告急</div><div class="val" style="color:var(--red)">'+criticalEbs+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--yellow)"><div class="lbl">🔥 演练完成</div><div class="val">'+(s.chaos_drill_completed||0)+'</div></div>'+
    '<div class="kpi" style="border-left:3px solid var(--blue)"><div class="lbl">⚠️ 安静水面</div><div class="val" style="font-size:.9rem">'+(BS.longest_clean_run?.machine||'-')+' '+(BS.longest_clean_run?.days_without_failure||0)+'天</div></div>';
  // 动态分析: 合并用户录入数据
  const ud=loadData(),userWOs=wos=getMergedWO();
  const userEvents=userWOs.filter(w=>w._source==='user').length;
  if(userEvents>0)document.getElementById('bsKPIs').insertAdjacentHTML('beforeend','<div class="kpi" style="border-left:3px solid var(--cyan)"><div class="lbl">📝 用户录入</div><div class="val" style="color:var(--cyan)">'+userEvents+'</div><div class="sub">条工单/记录</div></div>');
  // Charts
  setTimeout(()=>{{
    chartInstances.push(new Chart(document.getElementById('cErrorBudget'),{{type:'bar',data:{{labels:eb.map(e=>e.machine),datasets:[{{label:'已消耗(h)',data:eb.map(e=>e.consumed_h),backgroundColor:eb.map(e=>e.status==='critical'?'#ff4444':e.status==='warning'?'#ffa500':'#58a6ff')}},{{label:'剩余(h)',data:eb.map(e=>e.remaining_h),backgroundColor:'#30363d'}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,resizeDelay:100,plugins:{{legend:{{position:'bottom',labels:{{color:'#8b949e',font:{{size:9}}}}}}}},scales:{{x:{{stacked:true,ticks:{{color:'#8b949e',callback:v=>v+'h'}}}},y:{{stacked:true,ticks:{{color:'#8b949e',font:{{size:9}}}}}}}}}}}}));
    chartInstances.push(new Chart(document.getElementById('cClusterMutation'),{{type:'bar',data:{{labels:cm.map(c=>c.category),datasets:[{{label:'上月',data:cm.map(c=>c.last_month),backgroundColor:'#30363d'}},{{label:'本月',data:cm.map(c=>c.this_month),backgroundColor:'#58a6ff'}}]}},options:{{responsive:true,maintainAspectRatio:false,resizeDelay:100,plugins:{{legend:{{position:'bottom',labels:{{color:'#8b949e',font:{{size:9}}}}}}}},scales:{{x:{{ticks:{{color:'#8b949e',font:{{size:8}},maxRotation:25}}}},y:{{ticks:{{color:'#8b949e'}}}}}}}}}}));
  }},100);
  document.getElementById('bsEvents').innerHTML=be.map(e=>'<div class="kb-card" style="border-left:3px solid var(--red)"><div class="kb-title">🦢 '+e.machine+' — '+(e.event||'').substring(0,40)+'... <span class="badge badge-red">'+(e.swan_type==='unknown_unknown'?'未知未知':e.swan_type==='stealth_failure'?'隐蔽故障':e.swan_type==='pattern_shift'?'模式突变':'首次发生')+'</span></div><div class="kb-meta">📅 '+e.date+' · 🏷️ '+e.category+' · ⏱️ 影响'+e.impact+'</div><div style="font-size:.68rem;margin-top:4px">🔧 '+e.resolution+'</div><div style="font-size:.64rem;color:var(--yellow);margin-top:2px">💡 教训: '+e.learned+'</div></div>').join('');
  document.getElementById('bsDrillBody').innerHTML=cd.map(d=>'<tr><td>'+d.date+'</td><td><strong>'+d.machine+'</strong></td><td style="font-size:.66rem">'+d.scenario+'</td><td style="font-weight:700;color:'+(d.detection_time_s<30?'var(--green)':'var(--orange)')+'">'+d.detection_time_s+'s</td><td>'+d.response_time_min+'min</td><td style="font-size:.62rem;color:var(--orange)">'+((d.issues_found||[]).slice(0,2).join('; ')||'无')+'</td><td><span class="badge '+(d.score.startsWith('A')?'badge-green':d.score.startsWith('B')?'badge-blue':'badge-orange')+'">'+d.score+'</span></td></tr>').join('');
}}

renderRole();
</script>
</body>
</html>'''

# Write output
output_path = os.path.expanduser("~/.hermes/scripts/equipment_management_v6.html")
with open(output_path, "w") as f:
    f.write(html)

print(f"✅ v6.0 built: {output_path}")
print(f"   Size: {len(html):,} bytes")
print(f"   Lines: {html.count(chr(10))}")
