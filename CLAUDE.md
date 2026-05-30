# 设备管理与异常追踪系统
Equipment Management & Anomaly Tracking System

## 技术栈
- Python 3.9+
- 纯标准库（csv, json, collections, logging, argparse）
- 自包含 HTML（Chart.js CDN，数据内嵌 JSON）

## 目录结构
```
scripts/          # Python 数据处理
  equipment_collector.py           # CSV → JSON + 仪表盘
  equipment_v3_regenerator.py      # 模板 + JSON → HTML v3
  equipment_system_regenerator.py  # 模板 + JSON → HTML (旧版)
templates/        # HTML 源模板（含占位符 __XXX__）
data/             # CSV 源数据
```

## 编码规范
- 所有函数添加类型注解（`from __future__ import annotations`）
- 用 `logging` 模块，不用 `print()`
- 所有脚本支持 `--help`（argparse）
- 不吞异常 — 至少 `logger.warning` 或 `logger.exception`
- 保持向后兼容 — 不改变 JSON 输出格式和 HTML 占位符名称
- 深色主题 UI，中文界面
