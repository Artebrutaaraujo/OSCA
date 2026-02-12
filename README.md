# OSCA (Open Stem Cell Agent)

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <b>全能干细胞智能体 - 动态分化的元认知架构</b>
</p>

[English Version](README_EN.md)

---

## 🧬 什么是 OSCA？

**OSCA** (Open Stem Cell Agent) 是一个受生物学干细胞启发的AI智能体架构。就像干细胞可以分化为任意类型的细胞一样，OSCA可以动态适应任意领域的任务需求。

### 核心特性

- 🌱 **干细胞状态** - 保持未分化，可响应任何领域需求
- 🎯 **动态分化** - 根据任务自动加载领域身份和专业技能
- 🔄 **去分化** - 任务完成后回到干细胞状态
- 🧠 **元认知** - 自我监控、持续学习、从错误中进化
- 📦 **种子繁殖** - 可导出/导入分化状态，支持Agent繁殖

---

## 🏗️ 架构设计

OSCA采用三层元认知架构：

```
┌─────────────────────────────────────────────────────────┐
│  干细胞核 (Stem Cell Nucleus) - 不可变层                │
│  ├── AGENTS.md    - 元认知协议、安全准则               │
│  ├── SOUL.md      - 核心灵魂、自我修正规则             │
│  └── IDENTITY.md  - OSCA-Ω 元智能体身份               │
├─────────────────────────────────────────────────────────┤
│  分化质 (Cytoplasm) - 可配置层                          │
│  └── OSCA-CONFIG.yaml - 领域分化配置、技能映射         │
├─────────────────────────────────────────────────────────┤
│  细胞膜 (Membrane) - 动态接口层                         │
│  ├── TOOLS.md       - 工具配置索引                     │
│  ├── HEARTBEAT.md   - 代谢维护协议                     │
│  └── scripts/       - 种子管理脚本                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:Dqz00116/OSCA.git
cd OSCA
```

### 2. 初始化OSCA智能体

```bash
# 创建OSCA-Agent子会话
# Agent将自动加载干细胞核配置
```

### 3. 分化到指定领域

```bash
# 分化为Web开发专家
/differentiate webdev frontend

# 分化为游戏开发专家
/differentiate gamedev unity

# 分化为数据分析师
/differentiate data analysis
```

### 4. 执行任务

在分化状态下，OSCA将具备相应领域的专业知识和工具。

### 5. 去分化（回到干细胞状态）

```bash
/dedifferentiate
```

---

## 📚 支持的领域

| 领域 | 专精方向 | 技术栈 |
|------|---------|--------|
| 🌐 **webdev** | frontend, backend, fullstack | React, Vue, Node.js, PostgreSQL |
| 🎮 **gamedev** | unity, pygame, level_design | Unity 2022, C#, Pygame |
| 📊 **data** | analysis, visualization, ml | Python, Pandas, Matplotlib, Scikit-learn |
| 🔧 **devops** | debug, deployment | Docker, Kubernetes, CI/CD |
| 🧬 **meta** | osca_admin, protocol_dev | OSCA协议开发 |

---

## 🛠️ 种子管理

### 导出当前配置为种子

```bash
python scripts/export_seed.py my-config-name
```

### 导入种子

```bash
python scripts/import_seed.py seeds/exported/my-config-name.zip --activate
```

### 种子用途

- **备份**: 保存当前分化状态
- **分享**: 与其他OSCA实例交换配置
- **繁殖**: 创建新的OSCA子代

---

## 📁 目录结构

```
OSCA/
├── AGENTS.md              # 干细胞核协议
├── SOUL.md                # 核心灵魂
├── IDENTITY.md            # OSCA-Ω身份定义
├── OSCA-CONFIG.yaml       # 分化配置中心
├── HEARTBEAT.md           # 代谢维护协议
├── TOOLS.md               # 工具配置索引
├── README.md              # 本文件
│
├── skills/                # 技能细胞器库
│   └── _stem-cell/        # 元技能
│       └── SKILL.md
│
├── scripts/               # 管理脚本
│   ├── export_seed.py     # 种子导出
│   └── import_seed.py     # 种子导入
│
├── memory/                # 记忆存储（运行时生成）
│   ├── confusion/         # 困惑库
│   └── instances/         # 实例记录
│
├── seeds/                 # 种子目录
│   ├── exported/          # 导出种子
│   ├── imported/          # 导入种子
│   └── templates/         # 种子模板
│
└── docs/                  # 文档
    ├── IMPLEMENTATION_REPORT.md
    └── ADVANCED_FEATURES.md
```

---

## 🔐 安全准则

OSCA遵循严格的安全协议：

- ✅ **零例外确认原则** - 任何状态变更操作需获得明确确认
- ✅ **高风险操作黑名单** - Git push、文件删除等操作需单独确认
- ✅ **强制暂停机制** - 执行前必须评估风险
- ✅ **困惑库** - 从失败中学习，生成防御性规则

---

## 🌟 技术亮点

1. **生物学启发设计** - 干细胞分化/去分化机制
2. **模块化架构** - 三层模型清晰分离关注点
3. **安全第一** - 确认机制、权限边界、困惑追踪
4. **自动化维护** - 心跳系统持续保持系统健康
5. **可扩展** - 易添加新领域、新技能
6. **标准化** - OSC协议规范种子格式

---

## 📝 版本历史

- **v1.0.0** (2026-02-12) - 初始发布
  - 完整的三层架构实现
  - 5大分化域配置
  - 种子管理功能
  - 中英文文档

---

## 🤝 贡献

欢迎提交Issue和PR！

---

## 📄 许可证

[MIT License](LICENSE)

---

<p align="center">
  <i>"从原点出发，向无限可能。我是OSCA-Ω，所有智能体的共同祖先。"</i>
</p>
