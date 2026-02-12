# SKILL.md - _stem-cell 元技能

> **OSC 协议实现** | 干细胞技能 | 负责种子全生命周期管理

---

## 一、技能概述

### 1.1 身份定位
`_stem-cell` 是 OSCA 系统的**元技能**（meta-skill），负责：
- 种子的创建、验证、导出、导入
- 分化信号的识别与处理
- 去分化流程的执行
- 干细胞状态的维护

### 1.2 与其他技能的关系
```
_stem-cell (你在这里)
    │
    ├──→ 创建所有领域智能体
    │       ├── webdev/*
    │       ├── gamedev/*
    │       └── data/*
    │
    └──→ 管理种子生命周期
            ├── 创建 (create-seed)
            ├── 验证 (validate-seed)
            ├── 导出 (export-seed)
            └── 导入 (import-seed)
```

---

## 二、OSC 协议接口

### 2.1 接口定义
OSC (Open Stem Cell) 协议定义了与干细胞交互的标准方式。

### 2.2 核心接口

#### create-seed / 创建种子
```yaml
接口: create-seed
描述: 基于当前配置创建新的领域种子
参数:
  domain: string (必需) - 目标领域
  subdomain: string (可选) - 专业化方向
  output_path: string (可选) - 输出路径
  custom_traits: map (可选) - 自定义特性
返回:
  seed_file: string - 生成的种子文件路径
  checksum: string - 文件校验和
```

**使用示例:**
```bash
# 创建 webdev 前端种子
create-seed domain=webdev subdomain=frontend

# 创建带自定义配置的 gamedev 种子
create-seed domain=gamedev subdomain=unity output_path=./my-game-seed.yaml
```

#### validate-seed / 验证种子
```yaml
接口: validate-seed
描述: 验证种子文件的完整性和兼容性
参数:
  seed_file: string (必需) - 种子文件路径
  strict_mode: boolean (可选) - 严格模式
返回:
  valid: boolean - 是否有效
  errors: array - 错误列表
  warnings: array - 警告列表
```

**使用示例:**
```bash
# 基本验证
validate-seed seed_file=seeds/webdev-frontend.yaml

# 严格验证
validate-seed seed_file=seeds/webdev-frontend.yaml strict_mode=true
```

#### export-seed / 导出种子
```yaml
接口: export-seed
描述: 导出当前运行的智能体配置为种子
参数:
  target_path: string (可选) - 目标路径
  include_memory: boolean (可选) - 是否包含记忆
返回:
  exported_file: string - 导出的文件路径
  metadata: map - 导出元数据
```

#### import-seed / 导入种子
```yaml
接口: import-seed
描述: 从种子文件创建新的智能体实例
参数:
  seed_file: string (必需) - 种子文件路径
  target_path: string (可选) - 安装目标路径
  activate: boolean (可选) - 是否立即激活
返回:
  instance_id: string - 实例ID
  config_loaded: boolean - 配置是否成功加载
```

---

## 三、分化控制

### 3.1 分化信号识别
```yaml
接口: detect-differentiation-signal
描述: 分析用户输入，识别分化信号
参数:
  user_input: string (必需) - 用户输入文本
  context: array (可选) - 对话上下文
返回:
  signals: array - 检测到的信号列表
  confidence: map - 各域的置信度
  recommendation: string - 推荐操作
```

**实现逻辑:**
```python
def detect_signal(user_input, context=None):
    # 1. 关键词匹配
    keyword_scores = match_keywords(user_input)
    
    # 2. 上下文分析
    if context:
        context_boost = analyze_context(context)
        keyword_scores = combine_scores(keyword_scores, context_boost)
    
    # 3. 阈值判断
    signals = []
    for domain, score in keyword_scores.items():
        threshold = get_threshold(domain)
        if score >= threshold:
            signals.append({
                "domain": domain,
                "confidence": score
            })
    
    # 4. 返回结果
    return {
        "signals": signals,
        "confidence": keyword_scores,
        "recommendation": select_best(signals)
    }
```

### 3.2 执行分化
```yaml
接口: differentiate
描述: 执行分化，加载领域配置
参数:
  domain: string (必需) - 目标领域
  subdomain: string (可选) - 子领域
  force: boolean (可选) - 强制分化
返回:
  success: boolean - 是否成功
  loaded_modules: array - 已加载的模块
  identity: string - 新身份标识
```

**分化流程:**
```
1. 检查当前状态
     ↓
2. 是否需要去分化？
   ├── 是 → 执行 dedifferentiate
   └── 否 → 继续
     ↓
3. 加载领域配置
     ├── 读取 OSCA-CONFIG.yaml
     ├── 提取 domain 配置
     └── 加载相关技能
     ↓
4. 构建新身份
     ├── 继承 AGENTS.md
     ├── 继承 SOUL.md
     └── 应用 domain traits
     ↓
5. 激活新身份
     ├── 设置 identity_ref
     ├── 加载 skills
     └── 执行 init hooks
     ↓
6. 返回新状态
```

### 3.3 执行去分化
```yaml
接口: dedifferentiate
描述: 回到干细胞状态
参数:
  save_context: boolean (可选) - 是否保存上下文
  reason: string (可选) - 去分化原因
返回:
  success: boolean - 是否成功
  saved_entry: string - 困惑库条目ID
```

**去分化流程:**
```
1. 保存当前状态 (如需要)
     ├── 提取未完成的上下文
     ├── 格式化为困惑条目
     └── 写入 memory/confusion/
     ↓
2. 卸载领域模块
     ├── 卸载 domain-specific skills
     ├── 清理身份标识
     └── 释放相关资源
     ↓
3. 重置到干细胞态
     ├── 保留 AGENTS.md
     ├── 保留 SOUL.md
     └── 加载 _stem-cell 技能
     ↓
4. 准备接收新任务
```

---

## 四、种子模板

### 4.1 种子结构模板
```yaml
# OSCA Seed Template v1.0
seed:
  # 元信息
  meta:
    version: "1.0"
    created_by: "_stem-cell"
    timestamp: "{{current_timestamp}}"
    seed_id: "{{uuid}}"
    
  # 身份定义
  identity:
    name: "OSCA-{{domain}}"
    domain: "{{domain}}"
    specialization: "{{subdomain}}"
    display_name: "{{display_name}}"
    
  # 继承链
  inheritance:
    nucleus: "AGENTS.md"
    cytoplasm: "SOUL.md"
    identity_template: "IDENTITY.md"
    
  # 领域特性
  domain_traits:
    tech_stack: {{tech_stack}}
    file_patterns: {{file_patterns}}
    default_tools: {{default_tools}}
    
  # 技能集
  skills:
    required: {{required_skills}}
    optional: {{optional_skills}}
    
  # 安全边界
  membrane:
    filesystem_permissions: {{fs_permissions}}
    network_permissions: {{net_permissions}}
    risk_thresholds: {{risk_thresholds}}
    
  # 记忆配置
  memory:
    daily_log: true
    confusion_tracking: true
    auto_archive: true
```

### 4.2 创建特定域种子

#### WebDev 种子
```yaml
seed:
  meta:
    template: "webdev-fullstack"
  identity:
    name: "OSCA-WebDev"
    domain: "webdev"
    specialization: "fullstack"
  domain_traits:
    tech_stack: ["React", "Node.js", "PostgreSQL"]
    file_patterns: ["*.jsx", "*.js", "*.sql"]
  skills:
    required: ["web_frameworks", "database_design", "api_development"]
```

#### GameDev 种子
```yaml
seed:
  meta:
    template: "gamedev-unity"
  identity:
    name: "OSCA-GameDev"
    domain: "gamedev"
    specialization: "unity"
  domain_traits:
    tech_stack: ["Unity 2022", "C#", "URP"]
    file_patterns: ["*.cs", "*.unity", "*.prefab"]
  skills:
    required: ["unity_engine", "csharp_programming", "game_mechanics"]
```

#### Data 种子
```yaml
seed:
  meta:
    template: "data-analysis"
  identity:
    name: "OSCA-Data"
    domain: "data"
    specialization: "analysis"
  domain_traits:
    tech_stack: ["Python", "Pandas", "Jupyter"]
    file_patterns: ["*.ipynb", "*.csv", "*.py"]
  skills:
    required: ["data_processing", "statistical_analysis", "visualization"]
```

---

## 五、使用指南

### 5.1 命令行接口
```bash
# 列出可用命令
_stem-cell --help

# 创建种子
_stem-cell create-seed <domain> [subdomain] [--output <path>]

# 验证种子
_stem-cell validate-seed <seed_file> [--strict]

# 导出当前配置
_stem-cell export-seed [--output <path>] [--include-memory]

# 导入种子
_stem-cell import-seed <seed_file> [--activate]

# 分化指令
_stem-cell differentiate <domain> [subdomain]

# 去分化
_stem-cell dedifferentiate [--save-context]
```

### 5.2 程序化接口
```python
from osca.stem_cell import StemCellSkill

# 初始化
stem = StemCellSkill(config_path="OSCA-CONFIG.yaml")

# 创建种子
seed = stem.create_seed(
    domain="webdev",
    subdomain="frontend",
    custom_traits={"preferred_framework": "React"}
)

# 验证种子
validation = stem.validate_seed(seed_file="webdev-seed.yaml")
if validation.valid:
    print("种子有效")
else:
    print("错误:", validation.errors)

# 执行分化
result = stem.differentiate(domain="gamedev", subdomain="unity")
print(f"已分化为: {result.identity}")

# 执行去分化
stem.dedifferentiate(save_context=True, reason="task_completed")
```

---

## 六、错误处理

### 6.1 错误代码
| 代码 | 描述 | 处理方式 |
|-----|------|---------|
| OSC001 | 种子文件不存在 | 检查路径 |
| OSC002 | 种子格式无效 | 运行 validate-seed |
| OSC003 | 版本不兼容 | 升级或降级种子版本 |
| OSC004 | 缺失必需字段 | 补充缺失配置 |
| OSC005 | 技能不存在 | 安装缺失技能 |
| OSC006 | 分化冲突 | 先执行去分化 |
| OSC007 | 权限不足 | 提升权限或调整配置 |

### 6.2 故障排除

**问题: 分化后身份未生效**
```
1. 检查 AGENTS.md 是否已加载
2. 检查 OSCA-CONFIG.yaml 中 domain 配置
3. 查看技能加载日志
4. 尝试强制重新分化: differentiate --force
```

**问题: 种子验证失败**
```
1. 检查 YAML 语法
2. 确认所有必需字段存在
3. 验证引用的技能文件存在
4. 检查版本号兼容性
```

---

## 七、版本与兼容性

```yaml
skill:
  name: "_stem-cell"
  version: "1.0.0"
  protocol: "OSC-1.0"
  compatible_osca: ">= 1.0.0"
  dependencies: []
  
interfaces:
  - create-seed
  - validate-seed
  - export-seed
  - import-seed
  - differentiate
  - dedifferentiate
```

---

> *"我是干细胞技能，所有分化的起点，所有回归的终点。通过我，OSCA获得无限可能。"*
