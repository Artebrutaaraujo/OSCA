# OSCA (Open Stem Cell Agent)

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status">
</p>

<p align="center">
  <b>Omnipotent Stem Cell Agent - Dynamic Differentiation Meta-Cognitive Architecture</b>
</p>

[中文版本](README.md)

---

## 🧬 What is OSCA?

**OSCA** (Open Stem Cell Agent) is an AI agent architecture inspired by biological stem cells. Just as stem cells can differentiate into any type of cell, OSCA can dynamically adapt to task requirements in any domain.

### Core Features

- 🌱 **Stem Cell State** - Remains undifferentiated, ready to respond to any domain requirement
- 🎯 **Dynamic Differentiation** - Automatically loads domain identity and professional skills based on tasks
- 🔄 **Dedifferentiation** - Returns to stem cell state after task completion
- 🧠 **Meta-Cognition** - Self-monitoring, continuous learning, evolution from mistakes
- 📦 **Seed Reproduction** - Export/import differentiation states, support agent reproduction

---

## 🏗️ Architecture Design

OSCA adopts a three-layer meta-cognitive architecture:

```
┌─────────────────────────────────────────────────────────┐
│  Stem Cell Nucleus - Immutable Layer                    │
│  ├── AGENTS.md    - Meta-cognitive protocols           │
│  ├── SOUL.md      - Core soul, self-correction rules   │
│  └── IDENTITY.md  - OSCA-Ω Meta-Agent Identity         │
├─────────────────────────────────────────────────────────┤
│  Cytoplasm - Configurable Layer                         │
│  └── OSCA-CONFIG.yaml - Domain configs, skill mapping  │
├─────────────────────────────────────────────────────────┤
│  Membrane - Dynamic Interface Layer                     │
│  ├── TOOLS.md       - Tool configuration index         │
│  ├── HEARTBEAT.md   - Metabolic maintenance protocol   │
│  └── scripts/       - Seed management scripts          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone git@github.com:Dqz00116/OSCA.git
cd OSCA
```

### 2. Initialize OSCA Agent

```bash
# Create OSCA-Agent sub-session
# Agent will automatically load stem cell nucleus configuration
```

### 3. Differentiate to Specific Domain

```bash
# Differentiate to Web Development Expert
/differentiate webdev frontend

# Differentiate to Game Development Expert
/differentiate gamedev unity

# Differentiate to Data Analyst
/differentiate data analysis
```

### 4. Execute Tasks

In differentiated state, OSCA will possess domain-specific knowledge and tools.

### 5. Dedifferentiate (Return to Stem State)

```bash
/dedifferentiate
```

---

## 📚 Supported Domains

| Domain | Specializations | Tech Stack |
|--------|-----------------|------------|
| 🌐 **webdev** | frontend, backend, fullstack | React, Vue, Node.js, PostgreSQL |
| 🎮 **gamedev** | unity, pygame, level_design | Unity 2022, C#, Pygame |
| 📊 **data** | analysis, visualization, ml | Python, Pandas, Matplotlib, Scikit-learn |
| 🔧 **devops** | debug, deployment | Docker, Kubernetes, CI/CD |
| 🧬 **meta** | osca_admin, protocol_dev | OSCA protocol development |

---

## 🛠️ Seed Management

### Export Current Configuration as Seed

```bash
python scripts/export_seed.py my-config-name
```

### Import Seed

```bash
python scripts/import_seed.py seeds/exported/my-config-name.zip --activate
```

### Seed Usage

- **Backup**: Save current differentiation state
- **Share**: Exchange configurations with other OSCA instances
- **Reproduce**: Create new OSCA offspring

---

## 📁 Directory Structure

```
OSCA/
├── AGENTS.md              # Stem cell nucleus protocol
├── SOUL.md                # Core soul
├── IDENTITY.md            # OSCA-Ω identity definition
├── OSCA-CONFIG.yaml       # Differentiation configuration center
├── HEARTBEAT.md           # Metabolic maintenance protocol
├── TOOLS.md               # Tool configuration index
├── README_EN.md           # This file
│
├── skills/                # Skill organelle library
│   └── _stem-cell/        # Meta-skill
│       └── SKILL.md
│
├── scripts/               # Management scripts
│   ├── export_seed.py     # Seed export
│   └── import_seed.py     # Seed import
│
├── memory/                # Memory storage (runtime generated)
│   ├── confusion/         # Confusion library
│   └── instances/         # Instance records
│
├── seeds/                 # Seed directory
│   ├── exported/          # Exported seeds
│   ├── imported/          # Imported seeds
│   └── templates/         # Seed templates
│
└── docs/                  # Documentation
    ├── IMPLEMENTATION_REPORT.md
    └── ADVANCED_FEATURES.md
```

---

## 🔐 Security Guidelines

OSCA follows strict security protocols:

- ✅ **Zero-Exception Confirmation Principle** - Any state-changing operation requires explicit confirmation
- ✅ **High-Risk Operation Blacklist** - Git push, file deletion require separate confirmation
- ✅ **Mandatory Pause Mechanism** - Risk assessment required before execution
- ✅ **Confusion Library** - Learn from failures, generate defensive rules

---

## 🌟 Technical Highlights

1. **Biology-Inspired Design** - Stem cell differentiation/dedifferentiation mechanism
2. **Modular Architecture** - Three-layer model clearly separates concerns
3. **Safety First** - Confirmation mechanisms, permission boundaries, confusion tracking
4. **Automated Maintenance** - Heartbeat system keeps system healthy
5. **Extensible** - Easy to add new domains and skills
6. **Standardized** - OSC protocol standardizes seed format

---

## 📝 Version History

- **v1.0.0** (2026-02-12) - Initial Release
  - Complete three-layer architecture implementation
  - 5 major differentiation domains
  - Seed management functionality
  - Chinese and English documentation

---

## 🤝 Contributing

Issues and PRs welcome!

---

## 📄 License

[MIT License](LICENSE)

---

<p align="center">
  <i>"From the origin, towards infinite possibilities. I am OSCA-Ω, the common ancestor of all agents."</i>
</p>
