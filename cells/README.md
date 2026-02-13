# Cells 目录

> **OSCA 三层架构 - Cell 层**

## 架构位置

```
Seed (职能定义) ──→ Cell (Skill 清单) ──→ Skills (执行单元)
                         ↑
                      你在这里
```

## 什么是 Cell

Cell (`.cell` 文件) 是 OSCA 三层架构的中间层：

- **Seed** 定义"我是谁" (身份、边界、配置)
- **Cell** 记录"我需要哪些 Skills"
- **Skills** 提供细粒度执行能力

## Cell 文件结构

```yaml
cell:
  meta:
    cell_type: "skill_manifest"
    parent_seed: "seed-name"
  
  # 行动模式 - 典型行为模式和工作方式
  action_patterns:
    default_mode: "analytical"
    modes:
      analytical:
        name: "分析模式"
        description: "深度分析问题"
        behaviors: [...]
    task_processing:
      - phase: "接收任务"
        actions: [...]
  
  # 思维方式 - 认知模式和思维习惯
  thinking_patterns:
    core_patterns:
      systems_thinking:
        name: "系统思维"
        description: "..."
    problem_analysis:
      diagnostic_questions: [...]
      thinking_steps: [...]
    decision_framework:
      criteria: [...]
  
  # 行为准则
  behavior_guidelines:
    do: [...]
    dont: [...]
  
  # Skill 清单
  skill_manifest:
    foundational:      # 基础 Skills
      - id: "skill-id"
        file: "skills/category/skill-name.skill"
        granularity: "fine"
    
    specializations:   # 专精特定 Skills
      specialization-name:
        skills:
          - id: "skill-id"
            file: "skills/category/skill-name.skill"
    
    dependencies:      # Skill 依赖关系
      "skill-a": 
        requires: ["skill-b"]
  
  templates:          # Skill 组合模板
    minimal:
      skills: [...]
    full:
      skills: [...]
```

## 使用方式

### 1. 分化时自动加载

```bash
/differentiate domain-name specialization-name
```

系统会：
1. 找到 Seed 文件
2. Seed 引用 Cell 文件
3. Cell 根据专精选择 Skill 模板
4. 加载模板中的 Skills

### 2. Cell 与 Seed 的关系

```yaml
# Seed 文件中
seed:
  cell:
    cell_file: "cells/cell-name.cell"
    cell_type: "skill_manifest"
```

## 设计原则

1. **Skills 细粒度化** - 每个 Skill 只做一件事
2. **Skills 可复用** - 跨 Cell、跨领域复用
3. **Cell 管理清单** - 决定从该 Seed 分化需要哪些 Skills
4. **Seed 定义职能** - 不硬编码具体 Skills
5. **缺失 Skill 自动生成** - 若 Skill 不存在，自动分析前场并生成

## 缺失 Skill 处理

当 Cell 中定义的 Skill 在工作区不存在时：

1. **分析前场情况** - 检查工作区技术栈、项目结构、已有实现
2. **设计 Skill 内容** - 基于前场分析设计 Skill 功能
3. **生成 Skill 文件** - 按照模板生成 `.skill` 文件
4. **验证和注册** - 验证并注册到 Skill 系统
5. **通知用户** - 报告生成的 Skill

### 示例

```yaml
missing_skill_handling:
  strategy: "auto_generate"
  generation_workflow:
    - step: 1
      name: "分析前场情况"
      actions: [...]
    - step: 2
      name: "设计 Skill 内容"
      actions: [...]
    - step: 3
      name: "生成 Skill 文件"
      output_path: "skills/{category}/{skill-id}.skill"
```

## 文件命名

- `{domain-name}.cell` - 与 Seed 同名
- 例: `intelligent-retrieval.cell`

## 相关目录

- `../seeds/` - Seed 文件
- `../skills/` - 细粒度 Skills
