# Kimi Code CLI 完整项目目录设计

> 参考: https://moonshotai.github.io/kimi-cli/en/
> 参考: https://github.com/MoonshotAI/kimi-cli
> 参考: Kimi 自身源码结构 (src/kimi_cli/)

---

## 一、设计哲学

Kimi Code CLI 的目录设计围绕五个核心概念：

1. **AGENTS.md 子树作用域** — 每个 AGENTS.md 管理其所在目录及子树的上下文
2. **Skill 跨工具兼容** — Skills 兼容 Claude、Codex 等工具的开放标准 (`agentskills.io`)
3. **双组发现机制** — Brand 组 (`.kimi/`, `.claude/`, `.codex/`) + Generic 组 (`.agents/`)
4. **Agent Spec YAML** — 通过 YAML 定义 Agent 的行为、工具集、子 Agent
5. **Plan Mode** — 显式的计划模式，用于非平凡任务的架构设计和实现规划

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.kimi/
├── config.toml                  # ★ Kimi 主配置文件
├── skills/                      # Brand 组: Kimi 专属 Skills
│   ├── my-skill/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── quick-tip.md             # 扁平 Skill (name = "quick-tip")
│
├── agents/                      # 全局 Agent 定义 (可选)
│   └── default/
│       ├── agent.yaml
│       └── system.md
│
├── prompts/                     # 提示词模板
│   ├── compact.md               # 上下文压缩提示
│   └── init.md                  # 初始化提示
│
├── hooks/                       # 生命周期钩子脚本存放目录 (可选)
│   ├── pre_tool_use.py          # 实际 hooks 通过 ~/.kimi/config.toml 的 [[hooks]] 数组配置
│   └── post_tool_use.py         # .kimi/hooks/ 只是存放脚本的可选位置
│
├── sessions/                    # 会话存储
│   └── <session-id>/
│       ├── messages.jsonl
│       └── subagents/
│           └── <agent_id>/
│               ├── wire.log
│               └── context.json
│
└── logs/                        # 日志
    └── kimi-cli.log

~/.claude/skills/                # Brand 组: Claude 兼容 (自动加载)
~/.codex/skills/                 # Brand 组: Codex 兼容 (自动加载)

~/.config/agents/skills/         # Generic 组: 通用 Agent Skills (推荐)
~/.agents/skills/                # Generic 组: 通用兼容路径
```

### 2.2 项目层级 (仓库级)

```
your-project/
├── AGENTS.md                    # ★ 项目级指令 (注入到系统提示中)
├── .kimi/
│   ├── skills/                  # 项目级 Kimi Skills
│   │   └── deploy/
│   │       └── SKILL.md
│   ├── agents/                  # 项目级 Agent 定义
│   │   └── custom/
│   │       ├── agent.yaml
│   │       └── system.md
│   └── config.toml              # 项目级 Kimi 配置
│
├── .claude/
│   └── skills/                  # 项目级 Claude 兼容 Skills
│
├── .codex/
│   └── skills/                  # 项目级 Codex 兼容 Skills
│
├── .agents/
│   └── skills/                  # 项目级通用 Skills
│
└── README.md
```

### 2.3 子目录 AGENTS.md

```
your-project/
├── AGENTS.md                    # 根级 (全局)
├── src/
│   ├── auth/
│   │   └── AGENTS.md            # 子目录级 (在该目录及子树生效)
│   └── api/
│       └── AGENTS.md            # 子目录级
└── docs/
    └── AGENTS.md                # 子目录级
```

### 2.4 Kimi CLI 自身源码结构 (参考)

```
src/kimi_cli/
├── agents/                      # ★ 内置 Agent Specs
│   ├── default/
│   │   ├── agent.yaml           # 主 Agent 定义
│   │   ├── coder.yaml           # Coder 子 Agent
│   │   ├── explore.yaml         # Explore 子 Agent
│   │   ├── plan.yaml            # Plan 子 Agent
│   │   └── system.md            # 系统提示模板
│   └── okabe/
│       └── agent.yaml           # 其他 Agent 变体
│
├── prompts/                     # ★ 提示词模板
│   ├── compact.md               # 上下文压缩
│   └── init.md                  # 初始化
│
├── tools/                       # ★ 内置工具定义
│   ├── agent/                   # Agent 工具 (创建/恢复子 Agent)
│   │   ├── __init__.py
│   │   └── description.md
│   ├── ask_user/                # 提问工具
│   ├── background/              # 后台任务工具
│   │   ├── list.md
│   │   ├── output.md
│   │   └── stop.md
│   ├── dmail/                   # DMail 工具 (checkpointed replies)
│   ├── file/                    # 文件操作工具
│   │   ├── glob.md
│   │   ├── grep.md
│   │   ├── read.md
│   │   ├── read_media.md
│   │   ├── replace.md
│   │   └── write.md
│   ├── plan/                    # Plan Mode 工具
│   │   ├── description.md
│   │   ├── enter_description.md
│   │   └── enter.py
│   ├── shell/                   # Shell 工具
│   │   ├── bash.md
│   │   └── powershell.md
│   ├── think/                   # Think 工具
│   ├── todo/                    # Todo 工具
│   └── web/                     # Web 搜索工具
│
├── soul/                        # 核心运行时
│   ├── agent.py                 # Runtime, Agent, LaborMarket
│   ├── kimisoul.py              # 主 Agent 循环
│   ├── context.py               # 对话历史 + checkpoints
│   ├── compaction.py            # 上下文压缩
│   ├── approval.py              # 审批系统
│   ├── slash.py                 # Slash 命令
│   └── toolset.py               # 工具加载和运行
│
├── ui/                          # UI 前端
│   ├── shell/                   # TUI Shell
│   ├── print/                   # 打印模式
│   ├── acp/                     # ACP 服务器
│   └── wire/                    # 事件传输
│
├── wire/                        # 事件类型和传输
├── mcp.py                       # MCP 工具管理
├── app.py                       # KimiCLI 主入口
├── config.py                    # 配置系统
└── llm.py                       # LLM 提供者
```

---

## 三、各组成部分详解

### 3.1 AGENTS.md (核心指令文件)

**发现机制**：
- 从项目根目录开始，向下到当前工作目录
- **每个目录的 AGENTS.md 作用域是该目录及其子树**
- **更深层嵌套的 AGENTS.md 在冲突时优先**
- 直接系统/开发者/用户指令优先于 AGENTS.md 指令
- 根级 AGENTS.md 和从 CWD 到根路径上的目录内容自动注入开发者消息

**Kimi 特有的系统变量注入**：
Kimi 的 system prompt 通过模板变量注入环境信息：
- `${KIMI_NOW}` — 当前时间
- `${KIMI_WORK_DIR}` — 工作目录
- `${KIMI_WORK_DIR_LS}` — 工作目录列表
- `${KIMI_AGENTS_MD}` — 所有适用的 AGENTS.md 内容
- `${KIMI_SKILLS}` — 可用 Skills 列表
- `${KIMI_OS}` — 操作系统
- `${KIMI_SHELL}` — Shell 类型

### 3.2 Agent Spec YAML (`agent.yaml`)

Kimi 使用 YAML 文件定义 Agent 的行为、工具集和子 Agent：

```yaml
version: 1
agent:
  name: ""
  system_prompt_path: ./system.md        # 系统提示模板路径
  system_prompt_args:
    ROLE_ADDITIONAL: ""                # 注入到 system.md 的变量
  tools:                                 # 可用工具列表
    - "kimi_cli.tools.agent:Agent"
    - "kimi_cli.tools.ask_user:AskUserQuestion"
    - "kimi_cli.tools.todo:SetTodoList"
    - "kimi_cli.tools.shell:Shell"
    - "kimi_cli.tools.background:TaskList"
    - "kimi_cli.tools.file:ReadFile"
    - "kimi_cli.tools.file:WriteFile"
    - "kimi_cli.tools.web:SearchWeb"
    - "kimi_cli.tools.plan:ExitPlanMode"
    - "kimi_cli.tools.plan.enter:EnterPlanMode"
  subagents:                             # 子 Agent 定义
    coder:
      path: ./coder.yaml
      description: "Good at general software engineering tasks."
    explore:
      path: ./explore.yaml
      description: "Fast codebase exploration with prompt-enforced read-only behavior."
    plan:
      path: ./plan.yaml
      description: "Read-only implementation planning and architecture design."
```

**子 Agent 定义示例** (`plan.yaml`)：
```yaml
version: 1
agent:
  extend: ./agent.yaml                   # 继承主 Agent
  system_prompt_args:
    ROLE_ADDITIONAL: |
      You are now running as a subagent...
  when_to_use: |
    Use this agent when the parent agent needs a step-by-step implementation plan...
  allowed_tools:                         # 白名单工具
    - "kimi_cli.tools.file:ReadFile"
    - "kimi_cli.tools.file:Glob"
    - "kimi_cli.tools.web:SearchWeb"
  exclude_tools:                         # 黑名单工具
    - "kimi_cli.tools.shell:Shell"
    - "kimi_cli.tools.file:WriteFile"
```

### 3.3 Skills (`.kimi/skills/` / `.agents/skills/`)

**发现层级** (优先级从高到低)：
```
Project > User > Extra > Built-in
```

#### Project 级别
| 组 | 路径 | 优先级 |
|----|------|--------|
| Brand | `.kimi/skills/` | 1 (最高) |
| Brand | `.claude/skills/` | 2 |
| Brand | `.codex/skills/` | 3 |
| Generic | `.agents/skills/` | 通用 |

#### User 级别
| 组 | 路径 | 优先级 |
|----|------|--------|
| Brand | `~/.kimi/skills/` | 1 |
| Brand | `~/.claude/skills/` | 2 |
| Brand | `~/.codex/skills/` | 3 |
| Generic | `~/.config/agents/skills/` | 推荐 |
| Generic | `~/.agents/skills/` | 兼容 |

**合并行为**：
```toml
# ~/.kimi/config.toml
merge_all_available_skills = true   # 默认: 合并所有 brand 目录
merge_all_available_skills = false  # 仅使用最高优先级存在的 brand 目录
```

同名 Skill 优先级: **kimi > claude > codex**

**Extra Skills**：
```toml
extra_skill_dirs = [
    "~/my-skills-collection",
    ".claude/plugins/my-skills",
    "/opt/team-shared/skills"
]
```

### 3.4 Plan Mode (计划模式)

Kimi 有显式的 **Plan Mode**，通过 `EnterPlanMode` / `ExitPlanMode` 工具控制：

**使用场景**：
- 非平凡任务 (3+ 步骤或架构决策)
- 需要实施计划、关键文件识别、架构权衡分析

**Plan Agent** 特点：
- 只读行为，不修改代码
- 可以推荐父 Agent 使用 explore agent 调研
- 输出应包含：已知信息、未回答问题、实施计划

### 3.5 Subagents (子 Agent)

Kimi 支持通过 `Agent` 工具创建/恢复子 Agent 实例：
- 子 Agent 在独立上下文中运行
- 父 Agent 只能看到子 Agent 的最后一条消息
- 子 Agent 实例持久化存储在 `session/subagents/<agent_id>/`
- 支持 resume 已有实例

**内置子 Agent 类型**：
- `coder` — 通用软件工程任务
- `explore` — 快速代码库探索 (强制只读)
- `plan` — 实施计划和架构设计 (只读)

### 3.6 Hooks

Kimi 支持生命周期钩子 (与 Claude Code 兼容)：
- `pre_tool_use` — 工具调用前
- `post_tool_use` — 工具调用后
- `session_start` — 会话开始时
- `pre_compact` — 上下文压缩前

### 3.7 Config (`~/.kimi/config.toml`)

```toml
# 模型配置
model = "kimi-k2"

# Skill 配置
merge_all_available_skills = true
extra_skill_dirs = [
    "~/my-skills",
    "/opt/team-skills"
]

# MCP 服务器
[[mcp.servers]]
name = "filesystem"
transport = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem"]

# 其他配置
share_dir = "~/.kimi"              # 会话、日志存储位置
```

### 3.8 Prompts (`src/kimi_cli/prompts/`)

Kimi 内置的提示词模板：
- `compact.md` — 上下文压缩时使用的提示
- `init.md` — 初始化时使用的提示

---

## 四、关键文件命名规范

| 文件/目录 | 作用域 | 是否提交git | 说明 |
|-----------|--------|------------|------|
| `AGENTS.md` | 项目/子目录 | 是 | 核心指令文件 |
| `.kimi/skills/` | 项目 Skills | 是 | Kimi 专属 |
| `.kimi/agents/` | 项目 Agents | 是 | 自定义 Agent |
| `~/.kimi/config.toml` | 用户配置 | 否 | 主配置文件 |
| `~/.kimi/skills/` | 用户 Skills | 否 | 全局 Skills |
| `.claude/skills/` | 兼容 Skills | 是 | 自动加载 |
| `.agents/skills/` | 通用 Skills | 是 | 开放标准 |
| `agent.yaml` | Agent 定义 | 是 | YAML Spec |
| `system.md` | 系统提示 | 是 | 模板文件 |

---

## 五、Slash 命令

Kimi 支持丰富的 slash 命令：

| 命令 | 用途 |
|------|------|
| `/skill:<name>` | 加载 Skill |
| `/flow:<name>` | 执行 Flow Skill |
| `/task` | 后台任务管理 |
| `/plan` | 进入/退出计划模式 |

---

## 六、转换到其他工具时的映射

| Kimi | 通用 | Claude | Codex | OpenCode |
|------|------|--------|-------|----------|
| `AGENTS.md` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| `.kimi/skills/` | `.agents/skills/` | `.claude/skills/` | `.agents/skills/` | `.opencode/skills/` |
| `.kimi/agents/` | `.agents/agents/` | `.claude/agents/` | `~/.codex/agents/` | `.opencode/agents/` |
| `agent.yaml` | `.agents/agent.yaml` | 无直接等价 | 无直接等价 | `.opencode/opencode.json` |
| `system.md` | `.agents/prompts/system.md` | `.claude/output-styles/` | `~/.codex/prompts/` | `.opencode/prompts/` |
| `plan mode` | `.agents/plans/` | Plan Mode | `PLANS.md` | `.opencode/commands/` |
| `subagents` | `.agents/subagents/` | Claude subagents | Codex subagents | `.opencode/agents/subagents/` |
| `~/.kimi/config.toml` | `.agents/config.toml` | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.config/opencode/config.json` |
