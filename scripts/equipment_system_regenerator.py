#!/usr/bin/env python3
"""Regenerate equipment_management_system.html from JSON data files."""
import json, os

SYS_JSON = os.path.expanduser("~/.hermes/scripts/equipment_system_data.json")
ANOMALY_JSON = os.path.expanduser("~/.hermes/scripts/equipment_anomaly_data.json")
TEMPLATE = "/tmp/equip_db/equipment_management_system.html"
OUT_HTML = os.path.expanduser("~/.hermes/scripts/equipment_management_system.html")

if not os.path.exists(TEMPLATE):
    print(f"❌ Template not found: {TEMPLATE}")
    exit(1)

with open(SYS_JSON) as f: sys_data = json.load(f)
with open(ANOMALY_JSON) as f: anomaly_data = json.load(f)
with open(TEMPLATE) as f: html = f.read()

html = html.replace("__SYS_DATA__", json.dumps(sys_data, ensure_ascii=False))
html = html.replace("__ANOMALY_DATA__", json.dumps(anomaly_data, ensure_ascii=False))

with open(OUT_HTML, "w") as f: f.write(html)
print(f"✅ Regenerated: {OUT_HTML} ({len(html):,} bytes)")
