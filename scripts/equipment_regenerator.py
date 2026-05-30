#!/usr/bin/env python3
"""Regenerate equipment management HTML files from JSON data files.

Supports two modes:
  v3  — equipment_management_v3.html  (__ENHANCED__, __SYS__, __ANOMALY__)
  sys — equipment_management_system.html (__SYS_DATA__, __ANOMALY_DATA__)
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────────
V3_PATHS = {
    "enhanced": os.path.expanduser("~/.hermes/scripts/equipment_enhanced_data.json"),
    "sys": os.path.expanduser("~/.hermes/scripts/equipment_system_data.json"),
    "anomaly": os.path.expanduser("~/.hermes/scripts/equipment_anomaly_data.json"),
}
V3_TEMPLATE = "/tmp/equip_db/equipment_management_v3.html"
V3_OUT = os.path.expanduser("~/.hermes/scripts/equipment_management_v3.html")

SYS_JSON = os.path.expanduser("~/.hermes/scripts/equipment_system_data.json")
ANOMALY_JSON = os.path.expanduser("~/.hermes/scripts/equipment_anomaly_data.json")
SYS_TEMPLATE = "/tmp/equip_db/equipment_management_system.html"
SYS_OUT = os.path.expanduser("~/.hermes/scripts/equipment_management_system.html")


def _read_json(path: str) -> dict:
    """Read and return a JSON file, or exit on failure."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Failed to read %s: %s", path, e)
        sys.exit(1)


def _replace_and_write(
    template_path: str,
    out_path: str,
    replacements: dict[str, object],
) -> None:
    """Load template, replace placeholders, write output."""
    if not os.path.exists(template_path):
        logger.error("Template missing: %s", template_path)
        sys.exit(1)

    with open(template_path) as f:
        html = f.read()

    for placeholder, data in replacements.items():
        html = html.replace(placeholder, json.dumps(data, ensure_ascii=False))

    with open(out_path, "w") as f:
        f.write(html)

    logger.info("Regenerated: %s (%s bytes)", out_path, f"{len(html):,}")


def regenerate_v3() -> None:
    """Regenerate equipment_management_v3.html."""
    data: dict[str, dict] = {}
    for key, path in V3_PATHS.items():
        data[key] = _read_json(path)

    _replace_and_write(
        V3_TEMPLATE,
        V3_OUT,
        {"__ENHANCED__": data["enhanced"],
         "__SYS__": data["sys"],
         "__ANOMALY__": data["anomaly"]},
    )


def regenerate_sys() -> None:
    """Regenerate equipment_management_system.html."""
    sys_data = _read_json(SYS_JSON)
    anomaly_data = _read_json(ANOMALY_JSON)

    _replace_and_write(
        SYS_TEMPLATE,
        SYS_OUT,
        {"__SYS_DATA__": sys_data, "__ANOMALY_DATA__": anomaly_data},
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate equipment management HTML from JSON data files.",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["v3", "sys", "all"],
        default="all",
        help="Which HTML to regenerate (default: all)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show debug log messages",
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(message)s")

    if args.mode in ("v3", "all"):
        regenerate_v3()
    if args.mode in ("sys", "all"):
        regenerate_sys()


if __name__ == "__main__":
    main()
