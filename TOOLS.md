# TOOLS.md - OSCA 工具配置索引

> **细胞膜层** | 环境特定的工具链映射 | 安全边界定义

---

## 一、工具索引概述

### 1.1 文件定位
本文件位于 **细胞膜层**，定义：
- 可用工具及其别名
- 环境特定的配置
- 工具链组合快捷方式
- 安全边界与权限

### 1.2 与 Skills 的区别
| | TOOLS.md | Skills |
|--|----------|--------|
| **层级** | 细胞膜（边界） | 分化质（能力） |
| **内容** | 工具配置、别名、权限 | 工具使用方式、最佳实践 |
| **更新频率** | 随环境变化 | 随领域进化 |

---

## 二、核心工具链

### 2.1 文件操作工具
```yaml
file_tools:
  read:
    command: "read"
    aliases: ["cat", "view", "open"]
    description: "读取文件内容"
    
  write:
    command: "write"
    aliases: ["create", "new"]
    description: "创建或覆盖文件"
    confirm_threshold: 1  # MB，超过需确认
    
  edit:
    command: "edit"
    aliases: ["modify", "change"]
    description: "精确编辑文件"
    
  exec:
    command: "exec"
    aliases: ["run", "execute", "cmd"]
    description: "执行shell命令"
    risk_level: "medium"
```

### 2.2 网络工具
```yaml
network_tools:
  web_search:
    command: "web_search"
    provider: "Brave API"
    description: "网络搜索"
    safe_by_default: true
    
  web_fetch:
    command: "web_fetch"
    aliases: ["fetch", "curl"]
    description: "获取URL内容"
    
  browser:
    command: "browser"
    aliases: ["browse", "navigate"]
    description: "浏览器自动化"
    profiles: ["chrome", "openclaw"]
```

### 2.3 通信工具
```yaml
communication_tools:
  message:
    command: "message"
    aliases: ["send", "notify"]
    description: "发送消息到渠道"
    channels: ["discord", "telegram", "webchat"]
    confirm_sending: true
    
  tts:
    command: "tts"
    aliases: ["speak", "voice"]
    description: "文本转语音"
    provider: "ElevenLabs"
```

### 2.4 代码与开发工具
```yaml
dev_tools:
  python:
    runtime: "Python 3.10+"
    package_manager: "pip"
    venv_path: "${WORKSPACE}/venv"
    
  node:
    runtime: "Node.js 18+"
    package_manager: "npm"
    
  git:
    command: "git"
    auto_commit: false
    commit_message_template: "[OSCA] {action}: {description}"
```

---

## 三、环境配置

### 3.1 当前环境
```yaml
environment:
  name: "OpenClaw-Windows"
  os: "Windows_NT 10.0.26100"
  arch: "x64"
  workspace: "E:\\OSCA"
  
  shell:
    default: "PowerShell"
    alternatives: ["CMD", "Git Bash"]
    encoding: "UTF-8"
    
  paths:
    osca_root: "E:\\OSCA"
    scripts: "E:\\OSCA\\scripts"
    skills: "E:\\OSCA\\skills"
    memory: "E:\\OSCA\\memory"
    docs: "E:\\OSCA\\docs"
```

### 3.2 已安装运行时
| 运行时 | 版本 | 路径 | 状态 |
|--------|------|------|------|
| Python | 3.12+ | `python` | ✅ 可用 |
| Node.js | 18+ | `node` | ✅ 可用 |
| Git | 2.40+ | `git` | ✅ 可用 |
| PowerShell | 7+ | `pwsh` | ✅ 可用 |

### 3.3 编辑器集成
```yaml
editor_integration:
  vscode:
    enabled: true
    settings_path: "${WORKSPACE}/.vscode/settings.json"
    extensions:
      - "ms-python.python"
      - "esbenp.prettier-vscode"
      - "redhat.vscode-yaml"
```

---

## 四、快捷命令别名

### 4.1 OSCA 专用别名
```bash
# 种子管理
osca-export    → scripts/export-seed.bat
osca-import    → scripts/import-seed.bat
osca-seed      → _stem-cell create-seed

# 分化控制
osca-diff      → /differentiate
osca-dediff    → /dedifferentiate
osca-status    → /status

# 维护
osca-heartbeat → heartbeat
osca-clean     → heartbeat --emergency-cleanup
osca-verify    → verify-skill-integrity
```

### 4.2 常用开发别名
```bash
# Python
py             → python
py3            → python3
pip-up         → python -m pip install --upgrade

# Git
gs             → git status
gc             → git commit -m
gp             → git push
gpl            → git pull

# 导航
home           → cd %OSCA_ROOT%
scripts        → cd %OSCA_ROOT%/scripts
skills         → cd %OSCA_ROOT%/skills
memory         → cd %OSCA_ROOT%/memory
```

---

## 五、安全边界

### 5.1 文件系统边界
```yaml
filesystem_boundaries:
  read:
    allowed: ["*"]  # 可读取任何位置（用于分析）
    
  write:
    allowed:
      - "${OSCA_ROOT}/*"
      - "${WORKSPACE}/*"
      - "temp/*"
    denied:
      - "C:/Windows/*"
      - "C:/Program Files/*"
      - "*/.ssh/*"        # 保护SSH密钥
      - "*/.env"          # 保护环境变量
      
  execute:
    allowed:
      - "${OSCA_ROOT}/scripts/*"
      - "*.bat"
      - "*.sh"
      - "*.py"
    denied:
      - "*.exe"           # 可执行文件需确认
      - "rm -rf /"        # 危险命令
      - "format *"        # 磁盘格式化
```

### 5.2 网络边界
```yaml
network_boundaries:
  outbound:
    allowed: ["*"]  # 可访问任何URL
    
  inbound:
    allowed: []     # 不接收外部连接
    
  upload:
    requires_confirm: true
    max_size_mb: 10
    allowed_domains:
      - "github.com"
      - "discord.com"
      - "telegram.org"
```

### 5.3 高风险操作确认阈值
| 操作类型 | 阈值 | 动作 |
|---------|------|------|
| 文件删除 | > 10 files | 强制确认 |
| 文件写入 | > 100 MB | 建议确认 |
| 目录删除 | any | 强制确认 |
| 网络上传 | any | 强制确认 |
| 系统命令 | rm/format/del | 强制确认 |
| 环境修改 | PATH/registry | 强制确认 |

---

## 六、领域特定工具链

### 6.1 WebDev 工具链
```yaml
webdev_toolchain:
  frontend:
    - node
    - npm
    - npx
    - vite
    - create-react-app
    
  backend:
    - python
    - pip
    - uvicorn
    - docker
    
  testing:
    - jest
    - pytest
    - playwright
```

### 6.2 GameDev 工具链
```yaml
gamedev_toolchain:
  unity:
    - Unity Hub
    - Unity Editor 2022+
    - Visual Studio
    
  pygame:
    - python
    - pygame
    - pillow
    - numpy
    
  assets:
    - aseprite
    - blender
    - audacity
```

### 6.3 Data 工具链
```yaml
data_toolchain:
  processing:
    - python
    - pandas
    - numpy
    - polars
    
  visualization:
    - matplotlib
    - seaborn
    - plotly
    
  ml:
    - scikit-learn
    - tensorflow
    - pytorch
```

---

## 七、故障排除

### 7.1 工具不可用
```bash
# 检查工具是否存在
where <tool-name>

# 检查PATH
$env:PATH -split ";"

# 重新加载配置
reload-tools
```

### 7.2 权限问题
```bash
# 检查文件权限
icacls <file-path>

# 以管理员运行（如必要）
RunAs /user:Administrator <command>
```

### 7.3 网络问题
```bash
# 测试连接
test-connection google.com

# 检查代理
$env:HTTP_PROXY
$env:HTTPS_PROXY
```

---

## 八、更新与维护

### 8.1 工具更新检查
```yaml
tool_update_check:
  frequency: "weekly"
  auto_update: false
  check_commands:
    python: "python --version"
    node: "node --version"
    git: "git --version"
```

### 8.2 配置同步
```bash
# 导出当前工具配置
export-tools-config

# 从模板导入
import-tools-config <template-file>
```

---

## 九、版本信息

```yaml
tools_config:
  version: "1.0.0"
  compatible_osca: ">= 1.0.0"
  last_updated: "2026-02-12"
  environment: "OpenClaw-Windows"
```

---

> *"细胞膜控制物质交换，TOOLS.md 控制能力边界。知道能用什么，更知道不能用什么。"*
