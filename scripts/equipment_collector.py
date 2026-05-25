#!/usr/bin/env python3
"""Equipment Anomaly Collector — reads CSVs, generates analysis JSON + dashboard HTML."""
import csv, json, os
from collections import Counter, defaultdict
from datetime import datetime

DB = "/tmp/equip_db"
SRC = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Hermes/04-Knowledge/YE/08-equipment issue")
OUT_JSON = os.path.expanduser("~/.hermes/scripts/equipment_anomaly_data.json")
OUT_HTML = os.path.expanduser("~/.hermes/scripts/equipment_anomaly_dashboard.html")
OUT_SYS = os.path.expanduser("~/.hermes/scripts/equipment_system_data.json")

def regenerate_from_excel():
    """Full regeneration from Excel sources — slow, use only when source data changed."""
    import subprocess, sys
    # Check if CSVs already exist
    core = os.path.join(DB, "设备异常记录_设备异常记录2024-11-01-2024-11-30.csv")
    if os.path.exists(core):
        return  # Use existing CSVs
    
    print("No CSVs found, extracting from Excel...")
    # Re-run the extraction
    os.makedirs(DB, exist_ok=True)
    # This is handled by a separate extraction call if needed
    return

def collect():
    os.makedirs(DB, exist_ok=True)
    
    core_file = os.path.join(DB, "设备异常记录_设备异常记录2024-11-01-2024-11-30.csv")
    if not os.path.exists(core_file):
        print(f"❌ Core CSV not found: {core_file}")
        print("   Run Excel extraction first: terminal extraction script required")
        return False
    
    # Read core records
    records = []
    with open(core_file, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    
    # ---- Compute Statistics ----
    categories = Counter()
    machines = Counter()
    total_downtime = 0
    valid_downtime = 0
    
    for r in records:
        cat = r.get('故障类别', '').strip()
        mach = r.get('机台', '').strip()
        if cat: categories[cat] += 1
        if mach: machines[mach] += 1
        try:
            total_downtime += float(r.get('耗时(h)', '0').strip())
            valid_downtime += 1
        except: pass
    
    total = len(records)
    top_machines = machines.most_common(15)
    top_categories = categories.most_common(10)
    
    # Monthly trend
    monthly = defaultdict(lambda: defaultdict(int))
    for r in records:
        try:
            dt = datetime.strptime(r.get('开始时间', '').strip()[:10], '%Y-%m-%d')
            month_key = dt.strftime('%Y-%m')
            cat = r.get('故障类别', '').strip()
            monthly[month_key][cat] += 1
            monthly[month_key]['_total'] += 1
        except: pass
    
    monthly_sorted = sorted(monthly.items())
    monthly_labels = [m[0] for m in monthly_sorted]
    monthly_totals = [m[1]['_total'] for m in monthly_sorted]
    monthly_cats = {}
    all_cats = set()
    for _, cats in monthly_sorted:
        all_cats.update(k for k in cats if k != '_total')
    for cat in all_cats:
        monthly_cats[cat] = [monthly[m][cat] for m in monthly_labels]
    
    # Heatmap
    heatmap = defaultdict(lambda: defaultdict(int))
    for r in records:
        cat = r.get('故障类别', '').strip()
        mach = r.get('机台', '').strip()
        if cat and mach:
            heatmap[cat][mach] += 1
    
    # Machine downtime
    machine_downtime = defaultdict(float)
    machine_downtime_count = defaultdict(int)
    for r in records:
        mach = r.get('机台', '').strip()
        try:
            h = float(r.get('耗时(h)', '0').strip())
            machine_downtime[mach] += h
            machine_downtime_count[mach] += 1
        except: pass
    
    top_machines_dt = sorted(machine_downtime.items(), key=lambda x: -x[1])[:15]
    
    # ---- Build JSON ----
    data = {
        "summary": {
            "total_records": total,
            "total_downtime_hours": round(total_downtime, 1),
            "avg_downtime_per_event_hours": round(total_downtime / valid_downtime, 2) if valid_downtime else 0,
            "unique_machines": len(machines),
            "unique_categories": len(categories),
            "top_machine": list(top_machines[0]) if top_machines else ["N/A", 0],
            "top_category": list(top_categories[0]) if top_categories else ["N/A", 0],
            "top_machine_pct": round(top_machines[0][1]/total*100, 1) if top_machines else 0,
            "top_category_pct": round(top_categories[0][1]/total*100, 1) if top_categories else 0,
        },
        "categories": dict(top_categories),
        "machines": dict(top_machines),
        "category_pct": {k: round(v/total*100, 1) for k, v in categories.items()},
        "monthly_trend": {
            "labels": monthly_labels,
            "totals": monthly_totals,
            "categories": monthly_cats
        },
        "machine_downtime_top15": [
            {"machine": m, "count": machine_downtime_count[m], "hours": round(h, 1)}
            for m, h in top_machines_dt
        ],
        "heatmap_cats": sorted(heatmap.keys()),
        "heatmap_machines": sorted(set(m for cat_data in heatmap.values() for m in cat_data)),
        "_heatmap_raw": {cat: dict(mach_counts) for cat, mach_counts in heatmap.items()},
        "insight": "",  # Will be filled by regenerator or kept from last generation
    }
    
    # Load existing insight if available
    if os.path.exists(OUT_JSON):
        try:
            with open(OUT_JSON) as f:
                old = json.load(f)
            if old.get("insight"):
                data["insight"] = old["insight"]
        except: pass
    
    # Save JSON
    with open(OUT_JSON, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ---- Generate HTML ----
    html_template = os.path.join(DB, "equipment_anomaly_dashboard.html")
    if os.path.exists(html_template):
        with open(html_template) as f:
            html = f.read()
        html = html.replace("__DATA_PLACEHOLDER__", json.dumps(data, ensure_ascii=False))
        with open(OUT_HTML, "w") as f:
            f.write(html)
    
    print(f"✅ Equipment collector: {total} records, {len(machines)} machines, {round(total_downtime, 1)}h downtime → {OUT_JSON} ({OUT_HTML})")
    
    # Also regenerate the management system HTML (v3)
    import subprocess
    regen = os.path.expanduser("~/.hermes/scripts/equipment_system_regenerator.py")
    subprocess.run(["python3", regen], capture_output=True)
    
    # Regenerate v3 with enhanced data
    v3_gen = os.path.expanduser("~/.hermes/scripts/equipment_v3_regenerator.py")
    if os.path.exists(v3_gen):
        subprocess.run(["python3", v3_gen], capture_output=True)
    
    print(f"   → system HTMLs regenerated")
    
    return True

if __name__ == "__main__":
    collect()
