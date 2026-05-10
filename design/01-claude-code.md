# Claude Code 完整项目目录设计

> 参考: https://github.com/abhishekray07/claude-md-templates
> 官方: Anthropic "Claude Code Best Practices", "Memory and Project Configuration", "Hooks Guide"

---

## 一、设计哲学

Claude Code 的目录设计围绕三个核心概念：

1. **注意力预算 (target under 200 lines per CLAUDE.md file)** — 必须精简，每行都竞争注意力
2. **四层层级 (Managed → Global → Project → Local)** — 组织策略、个人偏好、团队规范、本地覆盖逐层叠加
3. **渐进式披露** — 按需加载，避免一次性注入过多上下文
4. **自我改进循环** — 通过 `/memory` 自动记忆 + 手动更新 CLAUDE.md

---

## 二、完整目录结构

### 2.1 全局层级 (用户级，跨所有项目)

```
~/.claude/
├── CLAUDE.md                    # 全局个人偏好 (跨所有项目)
├── rules/                       # 全局规则 (可选)
│   └── my-style.md
├── projects/                    # 自动记忆目录 (Claude 自动维护)
│   └── <project-name>/
│       └── memory/              # 自动发现的构建命令、调试模式、用户纠正
│           ├── MEMORY.md
│           ├── debugging.md
│           └── api-conventions.md
├── skills/                      # Claude Skills (如果支持)
└── settings.json                # Claude Code 应用设置
```

### 2.2 项目层级 (仓库级，提交到 git)

```
your-project/
├── .claude/
│   ├── CLAUDE.md                # ★ 项目主指令文件
│   ├── rules/                   # 模块化规则目录
│   │   ├── code-style.md        # 通用代码风格 (无 globs = 始终加载)
│   │   ├── testing.md           # 测试标准 (路径限定)
│   │   ├── api-design.md        # API 设计规范 (路径限定)
│   │   ├── security.md          # 安全规则
│   │   └── frontend.md          # 前端特定规则
│   ├── skills/                  # 项目级 Skills (开放标准兼容)
│   │   └── my-skill/
│   │       └── SKILL.md
│   ├── agents/                  # 自定义子代理 (Subagents)
│   │   ├── planner.md
│   │   └── reviewer.md
│   ├── output-styles/           # 自定义输出风格
│   │   └── concise.md
│   ├── docs/                    # 共享参考文档 (Skills 可引用)
│   │   ├── coding-standards.md
│   │   └── architecture.md
│   ├── workflows/               # 工作流模板 (社区方案，非官方)
│   │   ├── self-improvement-rules.md
│   │   └── prompting-patterns.md
│   └── settings.json            # 权限、Hooks、环境变量等配置
│
│
├── src/
│   ├── auth/
│   │   └── CLAUDE.md            # 模块级指令 (按需加载)
│   ├── api/
│   │   └── CLAUDE.md            # 模块级指令
│   └── components/
│       └── CLAUDE.md            # 模块级指令
│
├── CLAUDE.local.md              # ★ 本地个人覆盖 (gitignored)
├── .cursorignore                # 排除文件索引 (类 .gitignore)
└── README.md
```

### 2.3 社区扩展结构

```
your-project/
├── .claude/
│   ├── CLAUDE.md
│   ├── rules/
│   ├── workflows/
│   │   ├── self-improvement-rules.md      # 自律规则：Plan Mode、验证、优雅
│   │   ├── prompting-patterns.md          # 11 个可复用提示模板
│   │   ├── planning-template.md           # 计划模板
│   │   └── code-review-checklist.md       # 代码审查清单
│   ├── principles.md                    # 设计原则文档 (内部参考)
│   └── cheatsheet.md                    # 一页速查表
│
├── memory-bank/                         # 社区持久化记忆方案 (可选)
│   ├── activeContext.md
│   ├── productContext.md
│   ├── progress.md
│   └── decisionLog.md
│
└── AGENTS.md                            # 跨工具兼容文件 (Claude 也读取)
```

---

## 三、各组成部分详解

### 3.1 CLAUDE.md (核心指令文件)

**层级顺序** (从上到下加载，后加载的覆盖前面的)：
1. `~/.claude/CLAUDE.md` — 全局个人偏好
2. `.claude/CLAUDE.md` — 项目级共享指令
3. `src/auth/CLAUDE.md` — 子目录模块指令 (仅在该目录工作时加载)
4. `CLAUDE.local.md` — 本地个人覆盖 (始终最后加载)

**加载机制**：所有文件**拼接**到上下文中，不互相覆盖。冲突时，后出现的文件中的指令优先。

**最佳实践**：
- 项目级不超过 **80 行** (HumanLayer 保持 60 行以下)
- 全局级不超过 **15 行**
- 避免人格指令 ("Be a senior engineer")
- 避免 @-mention 文档 (会每次全量注入)
- 不写 formatter/linter 已覆盖的规则

### 3.2 Rules (`.claude/rules/*.md`)

规则使用 **YAML Frontmatter** 定义路径范围：

```markdown
---
description: "React component standards"
paths:
  - "src/components/**/*.tsx"
  - "src/components/**/*.jsx"
---

## React Component Rules
- Functional components only
- Named exports for all components
```

**无 `paths` 的规则 = 全局适用**。

**CLAUDE.md vs Rules**：
- `CLAUDE.md` = 项目级上下文 (技术栈、命令、结构)
- `rules/*.md` = 聚焦标准，应用于特定文件类型或目录

### 3.3 Hooks (通过 `settings.json` 配置)

Claude Code 支持**确定性生命周期钩子** (Deterministic Hooks)，在特定事件发生时自动执行预设动作。与 CLAUDE.md 的"建议性"不同，Hooks 是**100% 强制执行**的。

**配置位置**：`.claude/settings.json` 或 `~/.claude/settings.json` 中的 `hooks` 字段。

**支持的事件**（官方）：

| 事件 | 触发时机 |
|------|---------|
| `SessionStart` | 会话开始时 |
| `Setup` | 初始化阶段 |
| `PreToolUse` | 工具调用前 |
| `PostToolUse` | 工具调用后 |
| `Notification` | 需要通知时 |
| `Stop` | 会话结束时 |

**Hook 类型**：

| 类型 | 说明 |
|------|------|
| `command` | 执行 shell 命令（最常用） |
| `prompt` | 发送 prompt 给 Claude 模型做判断 |
| `agent` | 委派给子 agent 做判断 |
| `http` | 发送 HTTP 请求 |
| `mcp_tool` | 调用 MCP 工具 |

**示例**（`settings.json`）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

> ⚠️ **注意**：Claude Code 没有官方的 `.claude/hooks/` 配置目录。Hooks 只能通过 `settings.json` 配置。你可以在项目中的任意位置存放 shell 脚本，然后在 `command` 中引用它们。

**Hook 与 CLAUDE.md 的区别**：
- `CLAUDE.md` = **建议性** (Advisory)，Claude 可能忽略
- `Hooks` = **确定性** (Deterministic)，100% 执行

### 3.4 Workflows (`.claude/workflows/*.md`)

社区方案，非官方目录，但广泛使用的模式：

- **`self-improvement-rules.md`** — 自律规则：
  - Plan Mode Default (非平凡任务必须计划)
  - Subagent Strategy (利用子 Agent 保持主上下文干净)
  - Self-Improvement Loop (任何纠正后更新 CLAUDE.md)
  - Verification Before Done (证明工作正确才标记完成)
  - Demand Elegance (暂停思考是否有更优雅的方案)
  - Autonomous Bug Fixing (自主修复 bug，不请求指导)

- **`prompting-patterns.md`** — 11 个可复用提示模板

### 3.5 Auto Memory (`~/.claude/projects/<project>/memory/`)

Claude **自动维护**的记忆目录：
- 自动发现的构建命令
- 用户纠正的模式
- 调试洞察

通过 `/memory` 命令查看所有加载的记忆。

**CLAUDE.md vs Auto Memory**：
- 不需要把 Claude 会自己学到的东西放进 CLAUDE.md
- 只放不会自动发现的领域知识

### 3.6 Subagents

Claude Code 支持子 Agent 委托：
- 通过自然语言描述创建子任务
- 子 Agent 在独立上下文中运行
- 用于研究、探索、并行分析

---

## 四、文件类型对照表

| 文件类型 | 扩展名 | 用途 | Frontmatter |
|----------|--------|------|-------------|
| 主指令文件 | `CLAUDE.md` | 项目/模块/全局上下文 | 无 |
| 本地覆盖 | `CLAUDE.local.md` | 个人本地覆盖 | 无 |
| 规则文件 | `.md` (在 rules/) | 路径限定规则 | `description`, `paths` |
| Skills | `SKILL.md` (在 skills/) | 可复用工作流 | `name`, `description`, `tools`, `model` |
| 子代理 | `.md` (在 agents/) | 专用子代理 | `name`, `description`, `tools`, `disallowedTools`, `model` |
| 输出风格 | `.md` (在 output-styles/) | 修改响应风格 | `name`, `description`, `keep-coding-instructions` |
| 参考文档 | `.md` (在 docs/) | Skills 共享参考 | 无 |
| 工作流 | `.md` (在 workflows/) | 自律/提示模板 (社区) | 无 |
| 设置 | `settings.json` | Hooks、权限、环境变量 | JSON Schema |

---

## 五、加载优先级总结

```
~/.claude/CLAUDE.md              (Global)
      ↓
.claude/CLAUDE.md                (Project Root)
      ↓
.claude/rules/*.md               (Rules, always or globs-matched)
      ↓
src/*/CLAUDE.md                  (Module-specific, on-demand)
      ↓
CLAUDE.local.md                  (Local Override, always last)
      ↓
Auto Memory                      (~/.claude/projects/<name>/memory/)
```

---

## 六、转换到其他工具时的映射

| Claude Code | 通用 | Codex | Kimi | OpenCode |
|-------------|------|-------|------|----------|
| `~/.claude/CLAUDE.md` | `~/.agents/skills/global-guide/SKILL.md` | `~/.codex/AGENTS.md` | `~/.kimi/skills/global-guide/` | `~/.config/opencode/skills/global-guide/` |
| `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| `CLAUDE.local.md` | `.agents/local.md` | `AGENTS.override.md` | 子目录 `AGENTS.md` | `opencode.json` 配置 |
| `.claude/rules/*.md` | `.agents/rules/*.md` | `.agents/rules/*.md` | `.agents/rules/*.md` | `.opencode/rules/*.md` |
| `.claude/skills/*/` | `.agents/skills/*/` | `.agents/skills/*/` | `.agents/skills/*/` | `.opencode/skills/*/` |
| `.claude/agents/*.md` | `.agents/agents/*.md` | `.agents/agents/*.md` | `.agents/agents/*.md` | `.opencode/agents/*.md` |
| `.claude/hooks` (settings.json) | `.agents/hooks/` | `~/.codex/hooks/` (如支持) | `~/.kimi/hooks/` (如支持) | `.opencode/hooks/` |
| `.claude/output-styles/*.md` | `.agents/output-styles/*.md` | 无直接等价 | 无直接等价 | 无直接等价 |
| `.claude/docs/*.md` | `.agents/context/*.md` | `.agents/context/*.md` | `.agents/context/*.md` | `.opencode/context/*.md` |
| `.claude/workflows/*.md` | `.agents/workflows/` | `.agents/workflows/` | `.agents/workflows/` | `.opencode/commands/` |
| `src/*/CLAUDE.md` | `src/*/AGENTS.md` | `src/*/AGENTS.md` | `src/*/AGENTS.md` | `src/*/AGENTS.md` |
| `~/.claude/projects/*/memory/` | `.agents/memory/` | 无直接等价 | 无直接等价 | 无直接等价 |
