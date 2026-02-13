# Seed Library

> **OSCA 种子库** - 领域种子存储中心

## 目录结构

```
seeds/library/
├── webdev.seed.yaml              # Web开发领域
├── gamedev.seed.yaml             # 游戏开发领域
├── data.seed.yaml                # 数据分析领域
├── devops.seed.yaml              # DevOps与调试领域
├── meta.seed.yaml                # 元系统领域
├── intelligent-retrieval.seed.yaml # 智能信息检索领域
└── README.md                     # 本文件
```

## 什么是种子库

种子库是 OSCA 2.0 架构的核心组件，存储所有领域种子文件：

- **种子 (Seed)**: 定义分化细胞的职能、身份、边界
- **种子库**: 集中管理所有种子，支持动态加载
- **OSCA-CONFIG.yaml**: 只记录种子引用，不存储完整配置

## 种子文件格式

```yaml
seed:
  meta:
    version: "1.0.0"
    seed_id: "osca-{domain}-001"
    name: "{domain}"
    display_name: "Domain Name"
    icon: "🌐"
  
  identity:
    name: "OSCA-Domain"
    domain: "{domain}"
    specializations: [...]
  
  nucleus:
    inherits: ["AGENTS.md", "SOUL.md"]
    differentiation_triggers:
      keywords: [...]
      confidence_threshold: 0.7
  
  cytoplasm:
    specializations:
      spec-name:
        name: "Specialization Name"
        tech_stack: [...]
        file_patterns: [...]
  
  membrane:
    filesystem: {...}
  
  skills:
    universal: ["_stem-cell"]
    domain: [...]
  
  cell:
    cell_file: "cells/{domain}.cell"
    cell_type: "skill_manifest"
```

## 添加新种子

### 1. 创建种子文件

```bash
# 复制模板
cp templates/seed-template.yaml library/{domain}.seed.yaml

# 编辑种子文件
vim library/{domain}.seed.yaml
```

### 2. 注册种子

在 `OSCA-CONFIG.yaml` 中添加引用：

```yaml
seed_library:
  seeds:
    {domain}:
      seed_file: "{domain}.seed.yaml"
      version: "1.0.0"
      description: "描述"
```

### 3. 添加触发器映射

```yaml
differentiation:
  triggers:
    mapping:
      {domain}: "seeds/library/{domain}.seed.yaml"
```

### 4. 验证种子

```bash
python scripts/validate_seed.py seeds/library/{domain}.seed.yaml
```

## 使用种子

### 分化到某个领域

```bash
/differentiate {domain-name}
```

系统会：
1. 从 `OSCA-CONFIG.yaml` 找到种子引用
2. 从 `seeds/library/` 加载种子文件
3. 种子引用对应的 Cell 文件
4. Cell 加载所需的 Skills
5. 完成分化

### 查看可用种子

```python
# Python API
from osca.seed_library import SeedLibrary

lib = SeedLibrary()
seeds = lib.list_seeds()
for seed_id, seed_info in seeds.items():
    print(f"{seed_id}: {seed_info['description']}")
```

## 种子导入/导出

### 导出种子

```bash
python scripts/export_seed.py {domain} --output seeds/exported/
```

### 导入种子

```bash
python scripts/import_seed.py {path-to-seed}.seed.yaml
# 自动注册到种子库
```

## 版本管理

种子版本遵循语义化版本：

- `MAJOR`: 不兼容的架构变更
- `MINOR`: 新增功能（向后兼容）
- `PATCH`: Bug 修复

## 设计原则

1. **单一职责**: 每个种子只定义一个领域
2. **自包含**: 种子文件包含完整的领域定义
3. **可复用**: 种子可在不同 OSCA 实例间共享
4. **版本兼容**: 支持种子版本管理和迁移

## 相关文档

- `../README.md` - Seed 层说明
- `../templates/seed-template.yaml` - 种子模板
- `../../cells/README.md` - Cell 层说明
- `../../OSCA-CONFIG.yaml` - 全局配置
