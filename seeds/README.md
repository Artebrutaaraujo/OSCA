# Seeds 目录

> **OSCA 三层架构 - Seed 层**

## 架构位置

```
Seed (职能定义) ──→ Cell (Skill 清单) ──→ Skills (执行单元)
   ↑
你在这里
```

## 什么是 Seed

Seed (`.seed.yaml` 文件) 是 OSCA 三层架构的顶层：

- **Seed** 定义"我是谁" (身份、边界、配置、触发器)
- **Cell** 记录从该 Seed 分化需要哪些 Skills
- **Skills** 提供细粒度执行能力

## Seed 文件结构

```yaml
seed:
  meta:
    version: "1.0.0"
    seed_id: "unique-id"
  
  identity:
    name: "OSCA-Name"
    domain: "domain-name"
    specializations: [...]
  
  nucleus:
    inherits: ["AGENTS.md", "SOUL.md"]
    differentiation_triggers: {...}
  
  cytoplasm:
    tech_stack: {...}
    capabilities: [...]
  
  membrane:
    filesystem: {...}
    network: {...}
  
  # 引用 Cell 文件
  cell:
    cell_file: "cells/cell-name.cell"
    cell_type: "skill_manifest"
```

## 目录结构

```
seeds/
├── exported/       # 导出的种子文件
├── imported/       # 导入的种子文件
├── templates/      # 种子模板
└── README.md       # 本文件
```

## 使用方式

### 导出种子

```bash
python scripts/export_seed.py seed-name
```

### 导入种子

```bash
python scripts/import_seed.py seeds/exported/seed-name.seed.yaml [--activate]
```

### 验证种子

```bash
python scripts/validate_seed.py seeds/exported/seed-name.seed.yaml
```

## 分化流程

```
1. 导入 Seed 文件
        ↓
2. Seed 加载对应的 Cell 文件
        ↓
3. Cell 根据分化指令选择 Skill 模板
        ↓
4. 加载模板中列出的细粒度 Skills
        ↓
5. 完成分化
```

## 文件命名

- `{domain-name}.seed.yaml` - 领域种子
- 例: `intelligent-retrieval.seed.yaml`

## 相关目录

- `../cells/` - Cell 文件 (Skill 清单)
- `../skills/` - 细粒度 Skills
