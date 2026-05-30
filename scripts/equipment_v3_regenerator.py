#!/usr/bin/env python3
"""Thin wrapper — delegates v3 regeneration to equipment_regenerator."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "equipment_regenerator.py")

sys.exit(subprocess.call([sys.executable, MAIN, "v3"]))
