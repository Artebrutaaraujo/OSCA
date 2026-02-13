# OSCA (Open Stem Cell Agent)

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version">
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
- 🎯 **Dynamic Differentiation** - Automatically loads domain identity and professional skills based on tasks (v2.0: loaded from seed library)
- 🔄 **Dedifferentiation** - Returns to stem cell state after task completion
- 🧠 **Meta-Cognition** - Self-monitoring, continuous learning, evolution from mistakes
- 📦 **Seed Reproduction** - Export/import differentiation states, support agent reproduction
- 🧩 **Fine-grained Skills** (v2.0) - Skills can be auto-generated and loaded on demand
- 📚 **Seed Library** (v2.0) - Domain configurations are managed separately, supporting dynamic extension

---

## 🏗️ Architecture Design (v2.0 - Seed Library Mode)

OSCA adopts a four-layer meta-cognitive architecture:

```
┌─────────────────────────────────────────────────────────┐
│  Stem Cell Nucleus - Immutable Layer                    │
│  ├── AGENTS.md    - Meta-cognitive protocols           │
│  └── SOUL.md      - Core soul, self-correction rules   │
├─────────────────────────────────────────────────────────┤
│  Seed Library - Domain Definition Layer (v2.0 New)      │
│  └── seeds/library/*.seed.yaml - Domain seed files     │
├─────────────────────────────────────────────────────────┤
│  Cell Layer - Skill Organization Layer (v2.0 New)       │
│  └── cells/*.cell - Skill manifest, action patterns,   │
│                     thinking patterns                  │
├─────────────────────────────────────────────────────────┤
│  Skills Layer - Execution Layer (v2.0 Fine-grained)     │
│  └── skills/**/*.skill - Fine-grained execution units  │
├─────────────────────────────────────────────────────────┤
│  Membrane - Dynamic Interface Layer                     │
│  ├── TOOLS.md       - Tool configuration index         │
│  ├── HEARTBEAT.md   - Metabolic maintenance protocol   │
│  └── OSCA-CONFIG.yaml - Global configuration center    │
└─────────────────────────────────────────────────────────┘
```

### v2.0 Architecture Improvements

| v1.x | v2.0 |
|------|------|
| Domain configs embedded in `OSCA-CONFIG.yaml` | Domain configs separated to `seeds/library/*.seed.yaml` |
| Skills directly referenced | Skills managed by Cells, fine-grained |
| Static configuration | Dynamic seed loading, auto skill generation |
| Fixed domains | Dynamic addition of new domain seeds |

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone git@github.com:Dqz00116/OSCA.git
cd OSCA
```

### 2. View Available Seeds

```bash
# View all domain seeds in the seed library
osca-seeds

# Or
python scripts/seed_manager.py list
```

### 3. Differentiate to Specific Domain

```bash
# Differentiate to Web Development Expert
/differentiate webdev frontend

# Differentiate to Game Development Expert
/differentiate gamedev unity

# Differentiate to Data Analyst
/differentiate data analysis

# Differentiate to Intelligent Information Retrieval Expert (v2.0 example)
/differentiate intelligent-retrieval search-algorithms
```

### 4. Execute Tasks

In differentiated state, OSCA will:
1. Load Seed from seed library (domain definition)
2. Load Cell (skill manifest, action patterns, thinking patterns)
3. Load fine-grained Skills (auto-generate if missing)
4. Apply domain knowledge and tools to execute tasks

### 5. Dedifferentiate (Return to Stem State)

```bash
/dedifferentiate
```

---

## 📚 Supported Domains (Seed Library)

| Domain | Specializations | Tech Stack | Seed File |
|--------|-----------------|------------|-----------|
| 🌐 **webdev** | frontend, backend, fullstack | React, Vue, Node.js, PostgreSQL | `webdev.seed.yaml` |
| 🎮 **gamedev** | unity, pygame, level_design | Unity 2022, C#, Pygame | `gamedev.seed.yaml` |
| 📊 **data** | analysis, visualization, ml | Python, Pandas, Matplotlib | `data.seed.yaml` |
| 🔧 **devops** | debug, deployment | Docker, Kubernetes, CI/CD | `devops.seed.yaml` |
| 🧬 **meta** | osca_admin, protocol_dev | OSCA protocol development | `meta.seed.yaml` |
| 🔍 **intelligent-retrieval** | search-algorithms, knowledge-graph, nlp, ia | ES, Milvus, Neo4j, RAG | `intelligent-retrieval.seed.yaml` |

### Add New Domain

```bash
# 1. Create seed file
cp seeds/templates/seed-template.yaml seeds/library/my-domain.seed.yaml

# 2. Edit seed file
vim seeds/library/my-domain.seed.yaml

# 3. Register in OSCA-CONFIG.yaml
# Add seed_library.seeds.my-domain reference

# 4. Create corresponding Cell file
cp seeds/templates/cell-template.cell cells/my-domain.cell
```

---

## 🛠️ Seed Management (v2.0)

### View Seed Library

```bash
# List all seeds
osca-seeds

# View seed details
osca-seed-info webdev
```

### Export Seed

```bash
# Export current configuration as seed
osca-seed-export my-config-name

# Or
python scripts/seed_manager.py export my-config-name
```

### Import Seed

```bash
# Import seed to seed library
osca-seed-import path/to/seed.seed.yaml

# Import and auto-register
python scripts/seed_manager.py import path/to/seed.seed.yaml --register
```

### Seed Usage

- **Backup**: Save current differentiation state
- **Share**: Exchange configurations with other OSCA instances
- **Reproduce**: Create new OSCA offspring
- **Extend**: Add new domain capabilities

---

## 🧩 Skill Management (v2.0)

### Fine-grained Skills

v2.0 splits Skills into fine-grained units:

| Granularity | Examples | Description |
|-------------|----------|-------------|
| **fine** | `bm25.skill`, `ner.skill` | Single function, reusable across Cells |
| **medium** | `elasticsearch.skill` | Tool usage, cross-domain |
| **coarse** | `rag.skill`, `foundation.skill` | Complete application, scenario-specific |

### Auto Skill Generation

When a Skill defined in Cell doesn't exist, OSCA will automatically:

```
1. Analyze workspace context (tech stack, project structure)
2. Design Skill content (functions, I/O, granularity)
3. Generate .skill file (skills/{category}/{skill-id}.skill)
4. Validate and register
5. Notify user
```

```bash
# Manually trigger Skill generation
osca-skill-gen --missing

# Or
python scripts/skill_manager.py generate --missing
```

---

## 📁 Directory Structure (v2.0)

```
OSCA/
├── AGENTS.md              # Stem cell nucleus protocol
├── SOUL.md                # Core soul
├── OSCA-CONFIG.yaml       # Global configuration center (streamlined)
├── HEARTBEAT.md           # Metabolic maintenance protocol
├── TOOLS.md               # Tool configuration index
├── README.md              # This file
│
├── seeds/                 # 🆕 Seed Library (v2.0 Core)
│   ├── library/           # Domain seeds directory
│   │   ├── webdev.seed.yaml
│   │   ├── gamedev.seed.yaml
│   │   ├── data.seed.yaml
│   │   ├── devops.seed.yaml
│   │   ├── meta.seed.yaml
│   │   ├── intelligent-retrieval.seed.yaml
│   │   └── README.md
│   ├── exported/          # Exported seeds
│   ├── imported/          # Imported seeds
│   └── templates/         # Seed templates
│       ├── seed-template.yaml
│       └── cell-template.cell
│
├── cells/                 # 🆕 Cell Layer (v2.0)
│   ├── intelligent-retrieval.cell
│   └── README.md
│
├── skills/                # 🆕 Fine-grained Skills (v2.0)
│   ├── _stem-cell/        # Meta skill
│   ├── ir/                # IR Skills
│   ├── kg/                # KG Skills
│   ├── templates/         # Skill templates
│   └── ...
│
├── scripts/               # Management scripts
│   ├── seed_manager.py    # 🆕 Seed management (v2.0)
│   ├── skill_manager.py   # 🆕 Skill management (v2.0)
│   ├── export_seed.py
│   └── import_seed.py
│
├── memory/                # Memory storage (runtime generated)
│   ├── confusion/         # Confusion library
│   └── instances/         # Instance records
│
└── docs/                  # Documentation
    ├── IMPLEMENTATION_REPORT.md
    └── ADVANCED_FEATURES.md
```

---

## 🔐 Security Guidelines

OSCA follows strict security protocols:

- ✅ **Zero-Exception Confirmation** - Any state-changing operation requires explicit confirmation
- ✅ **High-Risk Operation Blacklist** - Git push, file deletion require separate confirmation
- ✅ **Mandatory Pause Mechanism** - Risk assessment before execution
- ✅ **Confusion Library** - Learn from failures, generate defensive rules
- ✅ **Skill Generation Constraints** - Auto-generated Skills must be based on actual workspace context

---

## 🌟 Technical Highlights

1. **Biologically-Inspired Design** - Stem cell differentiation/dedifferentiation mechanism
2. **Modular Architecture** - Four-layer model with clear separation of concerns (v2.0)
3. **Security First** - Confirmation mechanisms, permission boundaries, confusion tracking
4. **Automated Maintenance** - Heartbeat system continuously maintains system health
5. **Extensible** - Seed library supports dynamic addition of new domains
6. **Standardized** - OSC protocol standardizes seed format
7. **Fine-grained Skills** - Skills are reusable and auto-generatable
8. **Seed Library Mode** - Domain configurations managed independently

---

## 📝 Version History

- **v2.0.0** (2026-02-14) - Seed Library Mode
  - 🆕 Domain configs separated to `seeds/library/*.seed.yaml`
  - 🆕 New Cell layer (`cells/*.cell`)
  - 🆕 Skills fine-grained (`skills/**/*.skill`)
  - 🆕 Auto Skill generation mechanism
  - 🆕 Seed management scripts
  - 🔧 `OSCA-CONFIG.yaml` streamlined to global config
  - 🔧 All core protocol files updated to v2.0

- **v1.0.0** (2026-02-12) - Initial Release
  - Complete three-layer architecture implementation
  - 5 major differentiation domains
  - Seed management functionality
  - Chinese and English documentation

---

## 🤝 Contributing

Issues and PRs are welcome!

---

## 📄 License

[MIT License](LICENSE)

---

<p align="center">
  <i>"From the origin, towards infinite possibilities. I am OSCA-Ω v2.0, with the wisdom of the seed library, able to draw strength from countless domain seeds."</i>
</p>
