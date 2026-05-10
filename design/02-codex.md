# OpenAI Codex 完整项目目录设计

> 参考: https://developers.openai.com/codex/
> 参考: https://github.com/openai/codex
> 参考: https://kirill-markin.com/articles/codex-rules-for-ai/

---

## 一、设计哲学

Codex 的目录设计围绕四个核心概念：

1. **AGENTS.md 指令链** — 从全局到局部逐层拼接，后出现的覆盖先出现的
2. **32 KiB 大小限制** — `project_doc_max_bytes` 默认限制，防止上下文膨胀
3. **Skill 按需加载** — 通过名称+描述预加载列表，使用时才读取完整 SKILL.md
4. **开放标准兼容** — 支持 `.agents/skills/` 通用路径，跨工具可移植

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.codex/
├── AGENTS.md                    # 全局个人默认偏好
├── AGENTS.override.md           # 全局临时覆盖 (优先于 AGENTS.md)
├── config.toml                  # ★ Codex 主配置文件
├── hooks.json                   # 生命周期钩子配置 (JSON)
│   # ⚠️ 注意: Codex 的 hooks 通过 hooks.json 或 config.toml 内联 [hooks] 配置，
│   #    不是 .sh 文件目录。支持事件: SessionStart, PreToolUse, PermissionRequest,
│   #    PostToolUse, UserPromptSubmit, Stop
├── skills/                      # 全局 Skills
│   ├── skill-creator/
│   │   └── SKILL.md
│   ├── plan/
│   │   └── SKILL.md
│   └── my-global-skill/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
├── prompts/                     # 提示词模板 (可选) ⚠️ 未在官方文档中确认
│   └── default.md
└── plans/                       # 计划模板 (可选) ⚠️ 官方文档中不存在该目录概念
    └── template.md
```

### 2.2 项目层级 (仓库级)

```
your-project/
├── AGENTS.md                    # ★ 仓库级共享指令
├── PLANS.md                     # 执行计划模板 (多步骤工作)
├── .codex/                      # Codex 专用配置目录
│   ├── AGENTS.md                # (备选位置)
│   └── skills/                  # 项目级 Skills
│       └── release/
│           └── SKILL.md
│
├── services/
│   ├── payments/
│   │   ├── AGENTS.md            # 子目录规则
│   │   └── AGENTS.override.md   # 支付服务特定覆盖
│   └── search/
│       └── AGENTS.md            # 搜索服务规则
│
├── .agents/                     # ★ 通用 Agent 兼容目录
│   └── skills/                  # 通用 Skills (所有支持开放标准的工具)
│       ├── code-review/
│       │   └── SKILL.md
│       └── testing/
│           └── SKILL.md
│
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot 兼容
└── README.md
```

### 2.3 复杂项目结构示例

```
your-project/
├── AGENTS.md                    # 根级基础指令
├── PLANS.md                     # 执行计划模板
├── opencode.json                # OpenCode 兼容配置
├── .codex/
│   ├── config.toml              # 项目级 Codex 配置
│   └── skills/
│
├── .agents/                     # 通用 Agent 目录
│   ├── skills/                  # 跨工具 Skills
│   ├── rules/                   # 通用规则
│   ├── hooks/                   # 通用钩子
│   ├── prompts/                 # 通用提示词
│   └── plans/                   # 通用计划模板
│
├── packages/
│   ├── api/
│   │   └── AGENTS.md            # Monorepo 子包指令
│   └── web/
│       └── AGENTS.md
│
└── docs/
    └── AGENTS.md                # 文档目录特定指令
```

---

## 三、各组成部分详解

### 3.1 AGENTS.md (核心指令文件)

**发现顺序** (指令链拼接)：
1. **Global scope**: `~/.codex/AGENTS.override.md` → `~/.codex/AGENTS.md` (只取第一个非空文件)
2. **Project scope**: 从项目根目录向下遍历到当前工作目录
   - 每层检查: `AGENTS.override.md` → `AGENTS.md` → fallback filenames
   - 每层最多包含一个文件
3. **Merge order**: 从上到下拼接，用空行连接
   - **越靠近当前目录的文件，在拼接结果中越靠后**
   - 后出现的指令覆盖前面的指令

**配置参数** (`~/.codex/config.toml`)：
```toml
project_doc_max_bytes = 32768                    # 指令链大小限制 (默认 32 KiB)
project_doc_fallback_filenames = ["TEAM_GUIDE.md", "PROJECT_RULES.md"]

# Skill 配置
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false

# 模型和推理配置
model = "gpt-5"
reasoning_effort = "medium"
approval_policy = "suggest"
sandbox = "containerized"
```

### 3.2 PLANS.md (执行计划)

Codex 支持 `PLANS.md` 或执行计划模板，用于**长时间运行或多步骤工作**：

```markdown
# Execution Plan: Feature Implementation

## Phase 1: Research & Design
- [ ] Explore existing codebase patterns
- [ ] Identify integration points
- [ ] Design API contract

## Phase 2: Implementation
- [ ] Scaffold new module
- [ ] Implement core logic
- [ ] Add error handling

## Phase 3: Validation
- [ ] Write unit tests
- [ ] Run integration tests
- [ ] Manual verification
```

通过 `/plan` 或 `update_plan` 工具跟踪进度。

**Plan 使用时机**：
- 非平凡任务，需要多个步骤
- 有逻辑阶段或依赖关系
- 工作有模糊性，需要勾勒高层目标
- 需要中间检查点获取反馈

### 3.3 Skills (`.agents/skills/<name>/SKILL.md`)

Skill 是**可复用的多步骤能力包**，使用开放标准格式。

**发现层级**：
| Scope | 路径 | 说明 |
|-------|------|------|
| REPO | `$CWD/.agents/skills/` | 当前工作目录 |
| REPO | `$CWD/../.agents/skills/` | 父目录 (monorepo共享) |
| REPO | `$REPO_ROOT/.agents/skills/` | 仓库根级 |
| USER | `$HOME/.agents/skills/` | 用户全局 |
| ADMIN | `/etc/codex/skills` | 系统级 |
| SYSTEM | 内置 | OpenAI 自带 |

**Skill 目录结构**：
```
my-skill/
├── SKILL.md              # 必需: 指令 + 元数据
├── scripts/              # 可选: 可执行脚本
├── references/           # 可选: 参考文档
├── assets/               # 可选: 模板、资源
└── agents/
    └── openai.yaml       # 可选: UI元数据、依赖声明
```

**SKILL.md 格式**：
```markdown
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
license: MIT
compatibility: Requires Node.js >= 18
---

Skill instructions for Codex to follow.
```

**openai.yaml 配置**：
```yaml
interface:
  display_name: "Skill Display Name"
  short_description: "User-facing description"
  icon_small: "./assets/small-logo.svg"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt"

policy:
  allow_implicit_invocation: true  # false = 只显式调用

dependencies:
  tools:
    - type: "mcp"
      value: "serverName"
      description: "MCP server dependency"
```

**调用方式**：
- 显式: `$skill-name` 或 `/skills`
- 隐式: AI 根据 `description` 判断相关性自动调用

### 3.4 Hooks

Codex 支持生命周期钩子，通过 `hooks.json` 或 `config.toml` 内联 `[hooks]` 配置：

| 事件 | 触发时机 | 用途 |
|------|---------|------|
| `SessionStart` | 会话开始时 | 初始化环境 |
| `PreToolUse` | 工具使用前 | 验证参数、安全检查 |
| `PermissionRequest` | 需要权限确认时 | 自定义审批逻辑 |
| `PostToolUse` | 工具使用后 | 日志记录、后处理 |
| `UserPromptSubmit` | 用户提交 prompt 时 | 预处理、格式化 |
| `Stop` | 会话结束时 | 清理、报告生成 |

### 3.5 Config (`~/.codex/config.toml`)

完整配置示例：
```toml
# 模型配置
model = "gpt-5"
reasoning_effort = "medium"

# 沙盒和审批
approval_policy = "suggest"        # never / suggest / required
sandbox = "containerized"          # none / containerized

# 项目文档
project_doc_max_bytes = 32768
project_doc_fallback_filenames = ["TEAM_GUIDE.md"]

# 多 Profile 支持
[profiles.production]
model = "gpt-5"
approval_policy = "required"

[profiles.quick]
model = "gpt-4.1-mini"
approval_policy = "never"

# MCP 服务器
[[mcp.servers]]
name = "filesystem"
transport = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path"]

# Skill 配置
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = true
```

### 3.6 Prompts (`~/.codex/prompts/`)

模型特定的提示词变体，用于自定义系统提示的基础行为。

---

## 四、关键文件命名规范

| 文件 | 作用域 | 是否提交git | 说明 |
|------|--------|------------|------|
| `~/.codex/AGENTS.md` | 全局 | 否 | 个人跨项目默认 |
| `~/.codex/AGENTS.override.md` | 全局覆盖 | 否 | 临时全局覆盖 |
| `AGENTS.md` | 仓库级 | 是 | 团队共享指令 |
| `*/AGENTS.md` | 子目录 | 是 | 局部规则 |
| `*/AGENTS.override.md` | 子目录覆盖 | 视情况 | 局部覆盖 |
| `PLANS.md` | 仓库级 | 是 | 执行计划模板 |
| `.agents/skills/*/SKILL.md` | 项目 Skill | 是 | 开放标准 Skill |
| `~/.codex/skills/*/SKILL.md` | 全局 Skill | 否 | 个人 Skill |
| `~/.codex/config.toml` | 全局配置 | 否 | 主配置文件 |

---

## 五、AGENTS.md 内容规范

### 推荐内容
- 仓库布局和重要目录
- 如何运行项目
- 构建、测试、lint 命令
- 工程规范和 PR 期望
- 约束和禁止事项
- "完成"的定义和验证方式

### 最佳实践
- 保持简短准确
- 从基础开始，发现重复错误后才添加规则
- 当 Codex 重复犯错时，要求回顾并更新 AGENTS.md
- 如果文件太大，拆分到子目录或引用专门的 markdown 文件
- 使用 `PLANS.md` 模板处理多步骤工作

---

## 六、快速初始化

```bash
# 创建全局 AGENTS.md
mkdir -p ~/.codex
codex --ask-for-approval never "Summarize the current instructions."

# 初始化项目 AGENTS.md
codex /init

# 安装社区 Skill
$skill-installer linear
```

---

## 七、转换到其他工具时的映射

| Codex | 通用 | Claude | Kimi | OpenCode |
|-------|------|--------|------|----------|
| `~/.codex/AGENTS.md` | `~/.agents/skills/global-guide/SKILL.md` | `~/.claude/CLAUDE.md` | `~/.kimi/skills/global-guide/` | `~/.config/opencode/skills/global-guide/` |
| `AGENTS.md` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| `AGENTS.override.md` | `.agents/override.md` | `CLAUDE.local.md` | 子目录 `AGENTS.md` | `opencode.json` 配置 |
| `.agents/skills/*/` | `.agents/skills/*/` | `.claude/skills/*/` | `.kimi/skills/*/` | `.opencode/skills/*/` |
| `~/.codex/config.toml` | `.agents/config.toml` | `~/.claude/settings.json` | `~/.kimi/config.toml` | `~/.config/opencode/config.json` |
| `PLANS.md` | `.agents/plans/` | Plan Mode | `plan mode` | `.opencode/command/` |
| `~/.codex/hooks/` | `.agents/hooks/` | `.claude/settings.json` (hooks) | `~/.kimi/hooks/` | `.opencode/hooks/` |
| `~/.codex/prompts/` | `.agents/prompts/` | `.claude/output-styles/` | `~/.kimi/prompts/` | `.opencode/prompts/` |
