#!/usr/bin/env python3
"""Regenerate equipment_management_v3.html from 3 JSON data files."""
import json, os

paths = {
    "enhanced": os.path.expanduser("~/.hermes/scripts/equipment_enhanced_data.json"),
    "sys": os.path.expanduser("~/.hermes/scripts/equipment_system_data.json"),
    "anomaly": os.path.expanduser("~/.hermes/scripts/equipment_anomaly_data.json"),
}
template = "/tmp/equip_db/equipment_management_v3.html"
out = os.path.expanduser("~/.hermes/scripts/equipment_management_v3.html")

if not os.path.exists(template):
    print(f"❌ Template missing: {template}")
    exit(1)

data = {}
for key, path in paths.items():
    with open(path) as f:
        data[key] = json.load(f)

with open(template) as f:
    html = f.read()

html = html.replace("__ENHANCED__", json.dumps(data["enhanced"], ensure_ascii=False))
html = html.replace("__SYS__", json.dumps(data["sys"], ensure_ascii=False))
html = html.replace("__ANOMALY__", json.dumps(data["anomaly"], ensure_ascii=False))

with open(out, "w") as f:
    f.write(html)

print(f"✅ V3 regenerated: {out} ({len(html):,} bytes)")
