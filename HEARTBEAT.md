# HEARTBEAT.md - OSCA 代谢与维护协议

> **自动化维护系统** | 每30分钟执行一次代谢检查

---

## 一、心跳概述

### 1.1 什么是心跳
心跳是 OSCA 系统的**代谢机制**，模拟生物体的自主维护功能：
- **清理废物**: 归档旧记忆、压缩困惑库
- **修复损伤**: 验证技能完整性、检查配置一致性
- **监控状态**: 记录系统健康指标
- **预防维护**: 在问题发生前处理潜在风险

### 1.2 触发条件
```yaml
triggers:
  time_based:
    interval: "30 minutes"
    
  event_based:
    - "任务完成后"
    - "身份切换后"
    - "检测到异常后"
    
  manual:
    command: "/heartbeat"
```

---

## 二、心跳任务清单

### 2.1 困惑库维护 (Confusion Library Maintenance)
```yaml
task: check_confusion_lib
priority: P1
description: 检查并清理困惑库

steps:
  1. 读取 memory/confusion/ 目录
  2. 统计条目数量
  3. 检查过期条目 (>30天)
  4. 归档已解决的困惑
  5. 生成统计报告

output:
  total_entries: number
  resolved_count: number
  expired_count: number
  archived_count: number
```

**执行脚本位置**: `scripts/maintain-confusion.bat`

### 2.2 记忆归档 (Memory Archival)
```yaml
task: archive_old_memories
priority: P2
description: 将旧日记忆归档

steps:
  1. 检查 memory/ 目录中的文件
  2. 识别超过7天的日记忆
  3. 提取重要内容到 MEMORY.md
  4. 压缩原始文件到 archive/
  5. 清理重复/临时条目

criteria:
  archive_after: "7 days"
  extract_keywords: ["重要", "记住", "教训", "偏好"]
```

### 2.3 技能完整性检查 (Skill Integrity Check)
```yaml
task: verify_skill_integrity
priority: P1
description: 验证所有技能文件完整

steps:
  1. 扫描 skills/ 目录结构
  2. 检查每个 SKILL.md 是否存在
  3. 验证 YAML/JSON 配置语法
  4. 检查依赖关系
  5. 报告缺失或损坏的文件

checks:
  - file_exists: true
  - valid_syntax: true
  - required_sections: ["概述", "接口", "使用"]
  - dependencies_resolved: true
```

### 2.4 状态报告 (Status Report)
```yaml
task: report_status
priority: P3
description: 生成系统状态摘要

report_content:
  - 当前身份状态
  - 今日任务统计
  - 资源使用情况
  - 待处理的困惑
  - 建议的维护操作

output_format: markdown
output_location: "memory/heartbeat-${YYYYMMDD}.md"
```

---

## 三、困惑库维护详解

### 3.1 困惑条目生命周期
```
[创建] → [分析] → [处理中] → [已解决] → [归档]
  ↓         ↓         ↓          ↓         ↓
新问题   研究中   修正实施    验证完成   历史记录
```

### 3.2 自动处理规则
```yaml
auto_process_rules:
  # 30天未解决的困惑自动归档
  archive_unresolved_after: "30d"
  
  # 已解决困惑3天后归档
  archive_resolved_after: "3d"
  
  # 相似困惑合并
  merge_similar:
    enabled: true
    similarity_threshold: 0.85
    
  # 高频困惑升级为知识库
  promote_to_knowledge:
    threshold: 3  # 出现3次以上
    action: "添加到 skills/_stem-cell/faq.md"
```

### 3.3 困惑条目示例
```yaml
confusion_entry:
  id: "conf-2026-02-12-001"
  timestamp: "2026-02-12T11:46:00+08:00"
  status: "resolved"  # pending/analyzing/resolved/archived
  
  context:
    identity: "webdev-frontend"
    task: "创建React组件"
    
  confusion:
    type: "misunderstanding"
    description: "用户想要函数组件，但我生成了类组件"
    user_clarification: "使用hooks的函数组件"
    
  resolution:
    action: "重新生成函数组件"
    verification: "用户确认符合要求"
    
  lesson_learned:
    - "默认使用函数组件（现代React标准）"
    - "除非明确要求，否则不使用类组件"
    
  metadata:
    resolution_time: "5 minutes"
    similar_entries: ["conf-2026-02-10-003"]
```

---

## 四、手动触发心跳

### 4.1 命令行
```bash
# 完整心跳
heartbeat

# 仅检查困惑库
heartbeat --task confusion

# 仅归档记忆
heartbeat --task archive

# 仅验证技能
heartbeat --task verify

# 详细输出
heartbeat --verbose

# 干运行（不执行修改）
heartbeat --dry-run
```

### 4.2 程序化调用
```python
from osca.heartbeat import HeartbeatManager

hb = HeartbeatManager()

# 执行全部任务
results = hb.run_all()

# 执行特定任务
conf_result = hb.run_task("check_confusion_lib")
print(f"困惑库: {conf_result.total_entries} 条目")

# 获取状态报告
report = hb.generate_report()
```

---

## 五、配置项

### 5.1 心跳配置
```yaml
# OSCA-CONFIG.yaml 中的 heartbeat 部分
heartbeat:
  enabled: true
  interval_minutes: 30
  
  # 任务配置
  tasks:
    check_confusion_lib:
      enabled: true
      priority: "high"
      
    archive_old_memories:
      enabled: true
      days_before_archive: 7
      
    verify_skill_integrity:
      enabled: true
      check_dependencies: true
      
    report_status:
      enabled: true
      output_format: "markdown"
  
  # 通知设置
  notifications:
    on_error: true
    on_warning: true
    on_archive: false
```

### 5.2 困惑库配置
```yaml
confusion_library:
  path: "memory/confusion/"
  max_active_entries: 50
  max_total_entries: 100
  
  auto_archive:
    enabled: true
    archive_resolved_after: "3d"
    archive_unresolved_after: "30d"
    
  promotion:
    enabled: true
    threshold: 3
    target: "skills/_stem-cell/patterns.md"
```

---

## 六、输出与日志

### 6.1 心跳日志位置
```
memory/
├── heartbeat-2026-02-12.md    # 当日心跳日志
├── heartbeat-2026-02-11.md    # 历史日志
└── confusion/
    ├── index.yaml             # 困惑库索引
    ├── conf-001.yaml          # 具体条目
    └── archive/               # 归档条目
        └── 2026-01/
            └── conf-xxx.yaml
```

### 6.2 日志格式示例
```markdown
# Heartbeat Log - 2026-02-12 12:00:00

## Summary
- Status: ✅ Healthy
- Tasks Run: 4
- Issues Found: 1 warning

## Task: check_confusion_lib
- Total entries: 12
- Pending: 2
- Resolved: 8
- Archived: 2 (expired)

## Task: archive_old_memories
- Checked: memory/2026-02-05.md
- Action: Archived to memory/archive/2026-02/

## Task: verify_skill_integrity
- Skills checked: 8
- Status: ✅ All valid

## Task: report_status
- Current identity: webdev-frontend
- Today's tasks: 5 completed
- Token usage: 15,420 / 100,000

## Next Actions
- [ ] Review 2 pending confusion entries
- [ ] Consider upgrading heartbeat interval to 60min
```

---

## 七、故障处理

### 7.1 常见问题

**心跳执行失败**
```
原因: 磁盘空间不足
解决: 清理 memory/archive/ 目录

原因: 文件权限错误
解决: 检查 skills/ 和 memory/ 目录权限

原因: 配置文件损坏
解决: 验证 OSCA-CONFIG.yaml 语法
```

**困惑库膨胀**
```
症状: 困惑条目超过100个
处理: 
  1. 执行紧急归档: heartbeat --task confusion --force-archive
  2. 检查自动归档配置
  3. 手动清理已解决的旧条目
```

### 7.2 紧急维护
```bash
# 停止自动心跳
heartbeat --disable

# 紧急清理
heartbeat --emergency-cleanup

# 重置困惑库（谨慎！）
heartbeat --reset-confusion --backup-first
```

---

## 八、最佳实践

### 8.1 定期检查清单
- [ ] 每周查看困惑库，解决悬而未决的问题
- [ ] 每月归档历史记忆
- [ ] 每季度审查心跳配置效率

### 8.2 优化建议
1. **调整频率**: 高频使用时可设为15分钟，低频使用时60分钟
2. **自定义任务**: 根据需求添加特定检查任务
3. **集成通知**: 重要发现时主动通知用户

---

> *"心跳是OSCA的生命节律，让系统保持清洁、健康、有序。"*
