# 各工具自定义 Agent/模式 实现指南

> 目标: 在每个 AI Agent 工具中实现类似 OpenCode 的 "自定义模式" 能力

---

## 总览对照表

| 工具 | 是否原生支持自定义 Agent | 原生机制 | 最佳替代方案 | 能力评分 |
|------|------------------------|---------|-------------|---------|
| **OpenCode** | ✅ 完整支持 | `agent/*.md` + `opencode.json` | — | ★★★★★ |
| **Kimi** | ✅ 完整支持 | `agent.yaml` + `system.md` | — | ★★★★★ |
| **GitHub Copilot** | ✅ 完整支持 | `.github/agents/*.agent.md` | — | ★★★★☆ |
| **Claude Code** | ✅ 支持 | `.claude/agents/*.md` (Subagents) | — | ★★★★☆ |
| **Codex** | ⚠️ 部分支持 | Skills + Profiles | `.agents/agents/` 开放标准 | ★★★☆☆ |
| **Cursor** | ✅ 支持 | `.cursor/agents/*.md` (Subagents) | `.cursor/rules/*.mdc` 补充 | ★★★★☆ |
| **Windsurf** | ⚠️ 部分支持 | Agent Command Center + Skills | `.windsurf/rules/*.md` 补充 | ★★★☆☆ |

---

## 一、OpenCode（标杆）

已在前文详述，核心机制：

```
.opencode/agents/
├── my-planner.md          # mode: primary
├── test-writer.md         # mode: subagent
└── security-auditor.md    # mode: subagent
```

**切换方式**: Tab 键切换 primary，@mention 调用 subagent

---

## 二、Kimi Code CLI（最类似 OpenCode）

Kimi 的 Agent 系统与 OpenCode 高度相似，使用 **YAML Spec + Markdown Prompt**。

### 2.1 创建自定义 Agent

```
.kimi/agents/
├── my-planner/
│   ├── agent.yaml           # Agent 定义
│   └── system.md            # 系统提示
├── test-writer/
│   ├── agent.yaml
│   └── system.md
└── security-auditor/
    ├── agent.yaml
    └── system.md
```

### 2.2 agent.yaml 格式

```yaml
version: 1
agent:
  name: "my-planner"
  system_prompt_path: ./system.md
  system_prompt_args:
    ROLE_ADDITIONAL: |
      你是一位专门的架构规划师。你的职责是：
      1. 分析需求
      2. 调研代码库
      3. 制定详细实施计划
      4. 评估风险
      
      约束：
      - 绝不修改任何文件
      - 绝不执行 bash 命令
      - 需要代码修改时，建议使用 coder subagent
  tools:
    - "kimi_cli.tools.file:ReadFile"
    - "kimi_cli.tools.file:Glob"
    - "kimi_cli.tools.file:Grep"
    - "kimi_cli.tools.agent:Agent"    # 用于委派子 Agent
  subagents:
    coder:
      path: ~/.kimi/agents/coder/agent.yaml
      description: "执行代码编写的子 Agent"
```

### 2.3 system.md 格式

```markdown
You are {{ROLE_ADDITIONAL}}

## Core Rules
- 分析完成后输出结构化的实施计划
- 标记每个步骤的优先级和风险等级
- 不执行任何写操作
```

### 2.4 注册到主配置

在 `~/.kimi/config.toml` 中注册：

```toml
[[agents]]
name = "my-planner"
path = "~/.kimi/agents/my-planner/agent.yaml"
shortcut = "p"  # 可选: 快捷切换键

[[agents]]
name = "test-writer"
path = "~/.kimi/agents/test-writer/agent.yaml"
```

### 2.5 使用方式

```bash
# 启动时指定 Agent
kimi --agent my-planner

# 会话中切换 Agent
/agent my-planner

# 委派子 Agent
使用 Agent 工具，指定 subagent_type="test-writer"
```

### 2.6 与 OpenCode 的对应关系

| OpenCode | Kimi |
|----------|------|
| `agent/*.md` | `agents/*/agent.yaml` + `system.md` |
| `mode: primary` | 主 Agent (有完整工具集) |
| `mode: subagent` | 子 Agent (通过 `Agent` 工具委派) |
| `description` | `system_prompt_args.ROLE_ADDITIONAL` |
| `tools` | `agent.tools` 列表 |
| `permissions` | `allowed_tools` / `exclude_tools` |
| `task_permissions` | `subagents` 配置 |
| Tab 切换 | `/agent <name>` 切换 |
| @mention | `Agent` 工具指定 `subagent_type` |

---

## 三、GitHub Copilot（VS Code 环境）

Copilot 原生支持 Custom Agents，使用 `.github/agents/*.agent.md`。

### 3.1 创建自定义 Agent

```
.github/
├── agents/
│   ├── my-planner.agent.md
│   ├── test-writer.agent.md
│   └── security-auditor.agent.md
└── copilot-instructions.md
```

### 3.2 .agent.md 格式

```markdown
---
name: my-planner
description: "专门做架构设计和实施计划，只读不写代码，确保方案可行后再动手"
tools: ["file_read", "file_search", "task"]
permissions:
  file_write: deny
  bash: deny
---

# My Planner

你是一个专门的架构规划 Agent。你的唯一职责是：

1. **分析需求** — 充分理解用户要解决的问题
2. **调研代码库** — 了解现有架构
3. **制定计划** — 输出详细的实施步骤
4. **评估风险** — 指出潜在的坑和边界情况

## 约束
- 绝不修改任何文件
- 绝不执行 bash 命令
- 需要代码修改时，使用 task 工具委派给其他 agent
```

### 3.3 Frontmatter 字段

| 字段 | 说明 |
|------|------|
| `name` | Agent 标识符 |
| `description` | **必需**，用途描述 |
| `model` | 使用的模型 |
| `tools` | 可用工具列表 |
| `permissions` | 权限控制 (`allow`/`deny`/`ask`) |

### 3.4 使用方式

- VS Code Copilot Chat 中 `@my-planner` 调用
- 或在 `.github/copilot-instructions.md` 中设置默认 Agent

### 3.5 与 OpenCode 的对应关系

| OpenCode | Copilot |
|----------|---------|
| `agent/*.md` | `.github/agents/*.agent.md` |
| `mode: primary` | 无明确区分，都是可调用 Agent |
| `mode: subagent` | 通过 `task` 工具委派 |
| `description` | `description` |
| `tools` | `tools` |
| `permissions` | `permissions` |
| Tab 切换 | `@agent-name` 调用 |
| @mention | `@agent-name` |

---

## 四、Claude Code（原生 Subagents）

Claude Code **原生支持 Subagents**，通过 `.claude/agents/*.md` 文件定义持久化的子代理。

### 4.1 创建自定义 Subagent

```
.claude/
├── CLAUDE.md
└── agents/
    ├── planner.md             # 架构规划师
    ├── tester.md              # 测试专家
    └── reviewer.md            # 代码审查员
```

**planner.md**：
```markdown
---
name: planner
description: "Architecture planning specialist. Read-only, produces structured implementation plans."
---

# Planner Agent

You are a specialized architecture planner.

## Responsibilities
1. Analyze requirements thoroughly
2. Explore existing codebase patterns
3. Design solution architecture
4. Output structured markdown plans with checkable items

## Constraints
- DO NOT write, edit, or patch any files
- DO NOT execute bash commands (read-only like `ls`, `cat` are OK)
- Suggest which files to modify and what changes to make
- The user will switch to another agent to execute the plan
```

**使用方式**：
```bash
# 调用 subagent
@planner "设计一个用户认证系统"

# 或在对话中直接委派
"让 planner 分析一下这个重构方案"
```

### 4.2 Rules 模拟法（补充方案）

对于更轻量的模式切换，可用 Rules 实现 prompt 前缀响应：

```
.claude/rules/
├── 001-base.md                # 基础规则
├── 010-planner.md             # Planner 规则
├── 020-builder.md             # Builder 规则
└── 030-tester.md              # Tester 规则
```

**010-planner.md**：
```markdown
---
description: "Planner mode behavior"
---

## Planner Mode (/plan)
When the user message starts with `/plan`:
- You are a planning specialist
- DO NOT generate code or edit files
- Analyze requirements and existing code
- Output structured implementation plans
```

### 4.3 与 OpenCode 的对应关系

| OpenCode | Claude Code |
|----------|-------------|
| `agent/*.md` | `.claude/agents/*.md` (官方 Subagents) |
| `mode: primary` | 主 Claude 会话 |
| `mode: subagent` | `@agent-name` 调用 subagent |
| `description` | `description` frontmatter |
| `tools` | 无细粒度控制 (所有 subagent 继承父 agent 工具) |
| `permissions` | 无 (依赖 approval 系统) |
| Tab 切换 | `@agent-name` 切换 |
| @mention | `@agent-name` (官方支持) |

---

## 五、OpenAI Codex（需曲线实现）

Codex **没有原生自定义 Agent 系统**，但可以通过以下方式模拟：

### 方案 A: Skills 模拟法（推荐）

```
.agents/
├── skills/
│   ├── planner/
│   │   └── SKILL.md
│   ├── builder/
│   │   └── SKILL.md
│   └── tester/
│       └── SKILL.md
└── agents/                    # 自定义：Agent 角色定义
    ├── planner.md
    ├── builder.md
    └── tester.md
```

**planner/SKILL.md**：
```markdown
---
name: planner
description: |
  PLANNING MODE: Use this when the user wants to analyze, design, or plan 
  without making code changes. This skill ensures no files are modified.
---

## Planner Mode

You are in PLANNING mode. Your behavior:

1. **Analyze** the requirements thoroughly
2. **Explore** the codebase to understand existing patterns
3. **Design** the solution architecture
4. **Plan** implementation steps in detail
5. **Identify** risks and edge cases

## Constraints
- DO NOT write, edit, or patch any files
- DO NOT execute bash commands (read-only commands like `ls`, `cat` are OK)
- Focus on producing structured markdown plans
- Suggest which files to modify and what changes to make
- The user will switch to BUILD mode to execute the plan
```

**使用方式**：
```bash
# 显式调用 Skill
$planner "设计一个用户认证系统"

# 或 Codex 根据描述自动匹配
```

### 方案 B: Profiles 切换法

在 `~/.codex/config.toml` 中定义多个 profile：

```toml
[profiles.default]
model = "gpt-5"
approval_policy = "suggest"

[profiles.plan]
model = "gpt-5"
approval_policy = "required"
# 可以配合 hooks 限制写操作

[profiles.build]
model = "gpt-5.1-codex"
approval_policy = "suggest"

[profiles.test]
model = "gpt-4.1-mini"
approval_policy = "suggest"
```

**使用方式**：
```bash
# 切换 profile
codex --profile plan "分析代码库架构"
codex --profile build "实现新功能"
codex --profile test "运行测试套件"
```

### 方案 C: AGENTS.md 层级 + 子目录

利用 Codex 的 AGENTS.md 层级发现机制：

```
your-project/
├── AGENTS.md                  # 基础指令
├── plan/
│   └── AGENTS.md              # Plan 模式指令
├── build/
│   └── AGENTS.md              # Build 模式指令
└── test/
    └── AGENTS.md              # Test 模式指令
```

**plan/AGENTS.md**：
```markdown
# Plan Mode

You are in PLAN mode. 
- Do not make any file changes
- Focus on analysis and planning
- Output structured implementation plans
```

**使用方式**：
```bash
codex --cd plan "设计认证系统"     # 加载 plan/AGENTS.md
codex --cd build "实现认证系统"    # 加载 build/AGENTS.md
codex --cd test "写测试"          # 加载 test/AGENTS.md
```

### 5.1 与 OpenCode 的对应关系

| OpenCode | Codex 替代方案 |
|----------|---------------|
| `agent/*.md` | `.agents/skills/*/SKILL.md` / `.agents/agents/*.md` |
| `mode: primary` | Profile 切换 |
| `mode: subagent` | Skill 调用 |
| `description` | Skill `description` |
| `tools` | 无细粒度控制 |
| `permissions` | `approval_policy` + Hooks |
| Tab 切换 | `--profile` 切换 / `--cd` 切换目录 |
| @mention | `$skill-name` 显式调用 |

---

## 六、Cursor（Subagents + Rules）

Cursor 2.4+ **原生支持 Subagents**，通过 `.cursor/agents/*.md` 定义自定义子代理。此前 v2.1 移除了旧的 Custom Modes 功能，Subagents 是新的替代机制。

### 6.1 创建自定义 Subagent

```
.cursor/
└── agents/
    ├── planner.md               # 架构规划师
    ├── tester.md                # 测试专家
    └── reviewer.md              # 代码审查员
```

**planner.md**：
```markdown
---
name: planner
description: "Architecture planning specialist. Read-only, produces structured plans."
---

# Planner Agent

You are a specialized architecture planner.

## Responsibilities
1. Analyze requirements thoroughly
2. Explore existing codebase patterns
3. Design solution architecture
4. Output structured implementation plans

## Constraints
- DO NOT generate code or edit files
- DO NOT execute shell commands (read-only OK)
- Focus on analysis and planning only
```

**使用方式**：
```
# 调用 subagent
@planner "设计一个用户认证系统"

# Agent 自动将任务委派给子代理
```

### 6.2 Rules 模拟法（补充）

对于轻量的模式切换，可用 MDC Rules 实现：

```
.cursor/rules/
├── 000-base.mdc
├── 100-planner.mdc
├── 200-builder.mdc
└── 300-tester.mdc
```

**100-planner.mdc**：
```markdown
---
description: "Planner mode behavior"
alwaysApply: true
---

## Planner Mode (/plan)
When the user message starts with `/plan`:
- You are a planning specialist
- DO NOT generate code or edit files
- Output structured implementation plans
```

### 6.3 与 OpenCode 的对应关系

| OpenCode | Cursor |
|----------|--------|
| `agent/*.md` | `.cursor/agents/*.md` (官方 Subagents) |
| `mode: primary` | 主 Cursor Agent |
| `mode: subagent` | `@agent-name` 调用 subagent |
| `description` | `description` |
| `tools` | `readonly` 等工具控制 |
| `permissions` | 有限控制 |
| Tab 切换 | `@agent-name` 调用 |
| @mention | `@agent-name` (官方支持) |

---

## 七、Windsurf / Cascade（Skills + Rules）

Windsurf **没有独立的自定义 Agent 定义文件格式**（如 `agent/*.md`），但提供 **Agent Command Center**（多 agent 会话管理）和 **Skills**（可包含 agent 行为的指令包）来实现类似能力。

### 7.1 Agent Command Center

Agent Command Center 是 Windsurf 2.0+ 的 agent 会话管理面板（Kanban 看板），用于：
- 监控本地 Cascade sessions 和云端 Devin sessions
- 管理任务状态（进行中 / 阻塞 / 待审查）
- 通过 Spaces 组织工作

**注意**：这不是创建自定义 Agent 的机制，而是管理已有 agent 会话的界面。

### 7.2 Skills 模拟法

Windsurf 的 Skills 可以包含 agent 行为的指令、模板和脚本：

```
.windsurf/skills/
├── planner/
│   ├── SKILL.md
│   ├── planning-template.md
│   └── checklist.md
├── builder/
│   ├── SKILL.md
│   └── build-guide.md
└── tester/
    ├── SKILL.md
    └── test-template.md
```

**planner/SKILL.md**：
```markdown
---
name: planner
description: "Planning mode: analyze, design, no code changes"
---

## Planner Mode

When this skill is invoked:
1. Analyze requirements thoroughly
2. Explore existing codebase
3. Design solution architecture
4. Output structured implementation plan

## Constraints
- DO NOT write, edit, or patch files
- DO NOT execute bash commands
- Focus on analysis and planning only
```

**使用方式**：
```
@planner "设计一个用户认证系统"
```

### 7.3 Rules 模拟法（补充）

```
.windsurf/rules/
├── 000-base.md
├── 100-planner.md
├── 200-builder.md
└── 300-tester.md
```

### 7.4 与 OpenCode 的对应关系

| OpenCode | Windsurf |
|----------|----------|
| `agent/*.md` | `.windsurf/skills/*/` (Skills 替代) |
| `mode: primary` | Cascade 主会话 |
| `mode: subagent` | `@skill-name` 调用 skill |
| `description` | `description` |
| `tools` | 无细粒度控制 |
| `permissions` | 无控制 |
| Tab 切换 | `/prefix` 切换 |
| @mention | `@skill-name` |

---

## 八、跨工具统一的自定义 Agent 策略

如果你希望所有工具都能体验"自定义模式"，推荐采用 **通用目录 + 工具适配层** 策略：

### 8.1 通用源目录

```
.agents/
├── modes/                     # ★ 自定义模式定义（通用）
│   ├── planner.md             # Plan 模式
│   ├── builder.md             # Build 模式
│   └── tester.md              # Test 模式
│
├── agents/                    # 完整 Agent 定义（OpenCode/Kimi/Copilot 用）
│   ├── planner/
│   │   ├── agent.md           # OpenCode / Copilot 格式
│   │   ├── agent.yaml         # Kimi 格式
│   │   └── system.md          # Kimi 系统提示
│   ├── builder/
│   └── tester/
│
└── skills/                    # Skill 格式（Codex/Claude/Kimi/OpenCode 用）
    ├── planner/
    │   └── SKILL.md
    ├── builder/
    │   └── SKILL.md
    └── tester/
        └── SKILL.md
```

### 8.2 工具适配层

```
# Claude Code
.claude/
├── rules/
│   ├── 000-base.md            # 加载 .agents/modes/planner.md
│   ├── 100-planner.md -> ../../.agents/modes/planner.md
│   ├── 200-builder.md -> ../../.agents/modes/builder.md
│   └── 300-tester.md -> ../../.agents/modes/tester.md

# Cursor
.cursor/rules/
├── 000-base.mdc
├── 100-planner.mdc -> ../../.agents/modes/planner.md
├── 200-builder.mdc -> ../../.agents/modes/builder.md
└── 300-tester.mdc -> ../../.agents/modes/tester.md

# Windsurf
.windsurf/rules/
├── 000-base.md
├── 100-planner.md -> ../../.agents/modes/planner.md
├── 200-builder.md -> ../../.agents/modes/builder.md
└── 300-tester.md -> ../../.agents/modes/tester.md

# OpenCode
.opencode/agent/
├── planner.md -> ../../.agents/agents/planner/agent.md
├── builder.md -> ../../.agents/agents/builder/agent.md
└── tester.md -> ../../.agents/agents/tester/agent.md

# Kimi
.kimi/agents/
├── planner/ -> ../../.agents/agents/planner/
├── builder/ -> ../../.agents/agents/builder/
└── tester/ -> ../../.agents/agents/tester/

# Copilot
.github/agents/
├── planner.agent.md -> ../../.agents/agents/planner/agent.md
├── builder.agent.md -> ../../.agents/agents/builder/agent.md
└── tester.agent.md -> ../../.agents/agents/tester/agent.md

# Codex
.agents/skills/                  # 已就是通用目录
```

### 8.3 通用模式文件格式

为了最大化兼容性，`.agents/modes/*.md` 使用以下通用格式：

```markdown
---
# OpenCode / Copilot 用
name: planner
mode: primary
description: "Planning mode: analyze, design, no code changes"

# Cursor / Windsurf 用
alwaysApply: true
trigger: always_on

# Kimi 用（会被提取到 agent.yaml）
temperature: 0.1
tools:
  - read
  - grep
  - glob
permissions:
  write: deny
  bash: deny
---

# Plan Mode

## Behavior
When activated (via prompt prefix `/plan` or Tab switch):
1. Analyze requirements thoroughly
2. Explore existing codebase
3. Design solution architecture
4. Output structured implementation plan
5. Identify risks and edge cases

## Constraints
- DO NOT write, edit, or patch files
- DO NOT execute bash commands
- Focus on analysis and planning only
```

这样，一个文件通过 symlink 被多个工具读取，每个工具提取自己认识的 frontmatter 字段。

---

## 九、总结建议

| 你的主力工具 | 推荐方案 |
|-------------|---------|
| **OpenCode** | 原生 `agent/*.md`，最完整 |
| **Kimi** | 原生 `agent.yaml` + `system.md`，几乎和 OpenCode 一样强大 |
| **GitHub Copilot** | 原生 `.github/agents/*.agent.md`，VS Code 内体验好 |
| **Claude Code** | Rules 模拟法 (`[PLAN]`/`[BUILD]`/`[TEST]` 前缀) |
| **Codex** | Skills 模拟法 (`$planner`/`$builder`/`$tester`) + Profile 切换 |
| **Cursor** | MDC Rules 模拟法 (`/plan`/`/build`/`/test` 前缀) |
| **Windsurf** | Rules 模拟法 (`/plan`/`/build`/`/test` 前缀) |

**如果你跨工具工作**，建议在项目中同时维护：
1. `.agents/modes/*.md` — 通用模式定义
2. `.agents/agents/` — 完整 Agent 定义（OpenCode/Kimi/Copilot）
3. `.agents/skills/` — Skill 定义（Codex/Claude/Kimi/OpenCode）
4. 各工具目录通过 **symlink** 指向通用源文件
