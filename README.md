# 设备管理与异常追踪系统

> Equipment Management & Anomaly Tracking System

半导体工厂设备管理系统，支持五阶段工作流：巡检 → 报修 → 派单 → 维修 → 确认。

## 📖 功能

- **设备巡检** — 周期性检查记录
- **异常报修** — 设备故障登记与分类
- **派单管理** — 维修任务分配
- **维修追踪** — 维修进度与耗时统计
- **确认闭环** — 维修后验收确认
- **数据分析** — 异常分类占比、Uptime/OEE、年度对比

## 🏗️ 架构

```
equipment-system/
├── scripts/           # Python 数据处理脚本
│   ├── equipment_collector.py        # CSV → JSON + 仪表盘生成
│   ├── equipment_v3_regenerator.py   # 模板 + JSON → HTML v3
│   └── equipment_system_regenerator.py  # 模板 + JSON → HTML
├── templates/         # HTML 源模板（含占位符）
│   ├── equipment_management_v3.html
│   ├── equipment_management_system.html
│   ├── jdy_replica.html
│   └── equipment_anomaly_dashboard.html
└── data/              # 示例 CSV 数据
```

### 数据流

```
CSV 源数据  →  equipment_collector.py  →  JSON 数据文件
                                            ↓
HTML 模板   →  *_regenerator.py         →  最终 HTML 页面
```

### 模板占位符

- `equipment_management_v3.html`: `__ENHANCED__`, `__SYS__`, `__ANOMALY__`
- `equipment_management_system.html`: `__SYS_DATA__`, `__ANOMALY_DATA__`

## 🚀 使用

```bash
# 1. 准备 CSV 数据放入 data/ 目录

# 2. 运行数据收集
python scripts/equipment_collector.py

# 3. 生成 HTML 页面
python scripts/equipment_v3_regenerator.py
python scripts/equipment_system_regenerator.py
```

## 📊 数据格式

CSV 需包含设备异常记录，含以下字段：
- 设备名称 / 装置
- 异常类型 / 分类
- 发生时间 / 修复时间
- 处理人 / 确认人
- 异常描述 / 处理措施

## 🛠️ 技术栈

- Python 3.9+
- 纯 Python 标准库（csv, json, collections）
- 自包含 HTML（数据内嵌 JSON，无需后端服务器）
