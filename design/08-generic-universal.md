# 通用 AI Agent 项目目录设计 (跨工具兼容层)

> 目标: 设计一个所有主流 Agent 工具都能识别和加载的标准化目录结构
> 基于: 各工具的最大公约数 + 行业趋势

---

## 一、核心设计哲学

### 1.1 行业趋势观察

目前行业正在围绕以下趋势收敛：

| 趋势 | 说明 |
|------|------|
| **从单文件到模块化目录** | `.cursorrules` → `.cursor/rules/*.mdc`；`.windsurfrules` → `.windsurf/rules/*.md` |
| **YAML Frontmatter 成为标配** | `alwaysApply`/`trigger`、`globs`、`description` 被所有主流工具支持 |
| **激活模式趋同** | Always On / Glob / Model Decision / Manual 四种模式 |
| **AGENTS.md 成为跨工具桥梁** | 10+ 工具支持，放在任何目录即可生效 |
| **Agent Skills 开放标准** | `agentskills.io` 推动 Skill 目录跨工具可移植 |
| **三层分离成共识** | Foundation（基础指令）↔ Agents（角色专家）↔ Skills/Prompts（执行能力） |
| **Memory 机制兴起** | 自动记忆 + 持久化记忆银行 |
| **企业级治理** | 组织级规则强制下发 |

### 1.2 最大公约数分析

| 工具 | 主指令文件 | Skill 路径 | Agent 定义 | 计划/工作流 | 钩子 | 提示词 |
|------|-----------|-----------|-----------|------------|------|--------|
| Claude Code | `CLAUDE.md` | `.claude/skills/` | `.claude/agents/*.md` | Plan Mode | `settings.json` (hooks) | `.claude/output-styles/` |
| Codex | `AGENTS.md` | `.agents/skills/` | Skill 描述 | `PLANS.md` | `~/.codex/hooks/` | `~/.codex/prompts/` |
| Kimi | `AGENTS.md` | `.kimi/skills/` | `agent.yaml` | Plan Mode | `~/.kimi/hooks/` | `~/.kimi/prompts/` |
| OpenCode | `AGENTS.md` | `.opencode/skills/` | `.opencode/agents/*.md` | `.opencode/commands/` | `.opencode/hooks/` | `.opencode/prompts/` |
| Cursor | `.cursorrules` / `.mdc` | `.cursor/skills/` | `.cursor/agents/*.md` (Subagents) | Plan 模式 | `.cursor/hooks.json` | ✅ 支持 |
| Copilot | `copilot-instructions.md` | `.github/skills/` | `.github/agents/*.agent.md` | `prompts/` | `.github/hooks/*.json` | `.github/prompts/*.prompt.md` |
| Windsurf | `.windsurfrules` / `.md` | `.windsurf/skills/` | Agent Command Center | Skills / Workflows | `.windsurf/hooks.json` | ⚠️ 未确认 |

**最大公约数**: `AGENTS.md` + `.agents/skills/` + `.agents/agents/` + `.agents/hooks/` + `.agents/prompts/` + `.agents/context/`

---

## 二、推荐的通用目录结构

### 2.1 项目根级 (最大化兼容性)

```
your-project/
│
├── AGENTS.md                    # ★ 通用项目指令 (所有工具都支持)
│
├── .agents/                     # ★ 通用 Agent 生态目录
│   ├── skills/                  # 通用 Skills (开放标准)
│   │   ├── code-review/
│   │   │   └── SKILL.md
│   │   ├── git-commit/
│   │   │   └── SKILL.md
│   │   ├── testing/
│   │   │   └── SKILL.md
│   │   └── release/
│   │       └── SKILL.md
│   │
│   ├── agents/                  # 通用 Agent 定义
│   │   ├── coder.md
│   │   ├── reviewer.md
│   │   └── architect.md
│   │
│   ├── rules/                   # 通用规则
│   │   ├── code-style.md
│   │   ├── testing.md
│   │   └── security.md
│   │
│   ├── hooks/                   # 通用生命周期钩子
│   │   ├── pre_tool_use.py
│   │   ├── post_tool_use.py
│   │   └── session_start.py
│   │
│   ├── prompts/                 # 通用提示词模板
│   │   ├── system.md
│   │   ├── compact.md
│   │   └── plan.md
│   │
│   ├── context/                 # 通用领域知识
│   │   ├── core/
│   │   ├── development/
│   │   ├── architecture/
│   │   └── project/
│   │
│   ├── plans/                   # 通用计划模板
│   │   └── feature-template.md
│   │
│   ├── workflows/               # 通用工作流
│   │   ├── self-improvement.md
│   │   └── code-review.md
│   │
│   ├── memory/                  # 通用记忆/学习
│   │   ├── active-context.md
│   │   ├── decision-log.md
│   │   └── progress.md
│   │
│   └── config.toml              # 通用配置
│
├── .github/                     # GitHub Copilot 专用
│   ├── copilot-instructions.md
│   ├── instructions/
│   ├── prompts/
│   ├── agents/
│   └── skills/ → symlink ../.agents/skills/
│
├── .cursor/                     # Cursor 专用
│   └── rules/
│       ├── 001-base.mdc
│       ├── 010-frontend.mdc
│       └── 020-backend.mdc
│
├── .windsurf/                   # Windsurf 专用
│   └── rules/
│       ├── project-overview.md
│       └── coding-standards.md
│
├── .claude/                     # Claude Code 专用
│   ├── CLAUDE.md → symlink ../AGENTS.md
│   └── rules/ → symlink ../.agents/rules/
│
├── .codex/                      # Codex 专用
│   ├── AGENTS.md → symlink ../AGENTS.md
│   └── skills/ → symlink ../.agents/skills/
│
├── .kimi/                       # Kimi 专用
│   ├── skills/ → symlink ../.agents/skills/
│   └── agents/ → symlink ../.agents/agents/
│
├── .opencode/                   # OpenCode 专用
│   ├── opencode.json
│   ├── agent/ → symlink ../.agents/agents/
│   ├── skill/ → symlink ../.agents/skills/
│   ├── hooks/ → symlink ../.agents/hooks/
│   ├── prompts/ → symlink ../.agents/prompts/
│   └── context/ → symlink ../.agents/context/
│
├── .cursorignore
├── .codeiumignore
└── README.md
```

### 2.2 用户全局

```
~/.agents/
├── skills/                      # 用户全局通用 Skills
│   ├── my-code-style/
│   │   └── SKILL.md
│   └── my-workflow/
│       └── SKILL.md
├── agents/                      # 用户全局 Agent 定义
├── rules/                       # 用户全局规则
├── prompts/                     # 用户全局提示词
└── config.toml                  # 用户全局配置

~/.config/agents/
└── skills/                      # XDG 标准路径
    └── shared-team/
        └── SKILL.md
```

---

## 三、跨工具兼容矩阵

### 3.1 路径兼容性

| 通用路径 | Claude | Codex | Kimi | OpenCode | Cursor | Copilot | Windsurf |
|----------|--------|-------|------|----------|--------|---------|----------|
| `AGENTS.md` | ⚠️ 读 | ✅ | ✅ | ✅ | ⚠️ 读 | ✅ | ✅ |
| `.agents/skills/` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `.agents/agents/` | ❌ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `.agents/rules/` | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ |
| `.agents/hooks/` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| `.agents/prompts/` | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ |
| `.agents/context/` | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| `.agents/plans/` | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| `.agents/workflows/` | ❌ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ |
| `.agents/memory/` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

图例: ✅ 原生支持 | ⚠️ 兼容/读取 | ❌ 不支持

### 3.2 文件格式兼容性

| 通用格式 | Claude | Codex | Kimi | OpenCode | Cursor | Copilot | Windsurf |
|----------|--------|-------|------|----------|--------|---------|----------|
| `SKILL.md` (YAML frontmatter) | ⚠️ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `AGENTS.md` (纯 Markdown) | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| `CLAUDE.md` (纯 Markdown) | ✅ | ❌ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| `.mdc` (YAML frontmatter) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `.agent.md` (YAML frontmatter) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `agent.yaml` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 四、通用文件格式规范

### 4.1 通用 AGENTS.md 推荐格式

```markdown
# [Project Name]

Brief description of the project.

## Tech Stack
- **Language**: TypeScript / Python / Go
- **Framework**: Next.js / FastAPI / Gin
- **Database**: PostgreSQL / MongoDB
- **Package Manager**: npm / pnpm / poetry

## Project Structure
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

## Commands
- `npm run dev` - Start development server
- `npm test` - Run tests
- `npm run lint` - Run linter
- `npm run build` - Production build

## Code Conventions
- Naming: camelCase for variables, PascalCase for components
- Exports: Prefer named exports
- Types: Use strict TypeScript, avoid `any`

## Testing
- Unit tests for utilities
- Integration tests for API routes
- Coverage target: >80% for core logic

## Do Not
- Do not commit secrets or API keys
- Do not modify core logic without tests
```

### 4.2 通用 SKILL.md 推荐格式

```markdown
---
name: skill-name
description: Clear description of when and how to use this skill.
license: MIT
compatibility: Optional environment requirements
metadata:
  author: your-name
  version: "1.0"
---

## Purpose

Explain what this skill does and when it should be triggered.

## Instructions

1. Step-by-step workflow
2. Include examples
3. Document edge cases

## Examples

### Example 1: Basic usage
```bash
# command example
```

### Example 2: Advanced usage
```bash
# command example
```

## References

- Link to relevant documentation
- Link to example files in the project
```

### 4.3 通用 Agent 定义格式

```markdown
---
name: agent-name
description: What this agent does and when to use it
model: optional-model-spec
tools: ["file_read", "file_write", "shell"]
---

# Agent Name

## Role
Description of the agent's role.

## Capabilities
- Capability 1
- Capability 2

## Guidelines
- Guideline 1
- Guideline 2

## Output Format
Expected output format.
```

### 4.4 通用 Rule 格式

```markdown
---
description: "Rule description"
paths:
  - "src/**/*.ts"
  - "tests/**/*.ts"
alwaysApply: false
trigger: glob  # always_on | model_decision | glob | manual
---

## Rule Title

- Rule item 1
- Rule item 2
```

---

## 五、完整转换映射表

### 5.1 从通用到各工具

| 通用 | Claude | Codex | Kimi | OpenCode | Cursor | Copilot | Windsurf |
|------|--------|-------|------|----------|--------|---------|----------|
| `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `.cursorrules` / `.cursor/rules/base.mdc` | `.github/copilot-instructions.md` | `.windsurfrules` / `.windsurf/rules/*.md` |
| `.agents/skills/*/` | `.claude/skills/*/` | `.agents/skills/*/` | `.kimi/skills/*/` | `.opencode/skills/*/` | `.cursor/rules/*.mdc` | `.github/skills/*/` | `.windsurf/rules/*.md` |
| `.agents/agents/` | `.claude/agents/` | `~/.codex/agents/` | `.kimi/agents/` | `.opencode/agents/` | `.cursor/agents/` | `.github/agents/` | ⚠️ 不适用 |
| `.agents/rules/` | `.claude/rules/` | `.agents/skills/*/` | `.kimi/skills/*/` | `.opencode/skills/*/` | `.cursor/rules/` | `.github/instructions/` | `.windsurf/rules/` |
| `.agents/hooks/` | `settings.json` (hooks) | `~/.codex/hooks/` (脚本) | `~/.kimi/hooks/` (脚本) | `.opencode/hooks/` | `.cursor/hooks.json` | `.github/hooks/*.json` | `.windsurf/hooks.json` |
| `.agents/prompts/` | `.claude/output-styles/` | `~/.codex/prompts/` | `~/.kimi/prompts/` | `.opencode/prompts/` | ✅ 支持 | `.github/prompts/` | ⚠️ 未确认 |
| `.agents/context/` | `.claude/docs/` | `.agents/context/` | `.kimi/context/` | `.opencode/context/` | 无 | 无 | 无 |
| `.agents/plans/` | Plan Mode | `PLANS.md` | Plan Mode | `.opencode/commands/` | 无 | 无 | 无 |
| `.agents/memory/` | `~/.claude/projects/*/memory/` | 无 | 无 | 无 | 无 | 无 | `memory-bank/` |
| `.agents/workflows/` | `.claude/workflows/` | `PLANS.md` | Plan Mode | `.opencode/commands/` | 无 | 无 | 无 |

### 5.2 从各工具到通用

| Claude | 通用 | Codex | 通用 | Kimi | 通用 |
|--------|------|-------|------|------|------|
| `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| `CLAUDE.local.md` | `.agents/local.md` | `AGENTS.override.md` | `.agents/override.md` | 子目录 AGENTS.md | `.agents/local/` |
| `.claude/rules/*.md` | `.agents/rules/*.md` | `.agents/skills/*/` | `.agents/skills/*/` | `.kimi/skills/*/` | `.agents/skills/*/` |
| `.claude/settings.json` (hooks) | `.agents/hooks/` | `~/.codex/hooks/` | `.agents/hooks/` | `~/.kimi/hooks/` | `.agents/hooks/` |
| `.claude/workflows/*.md` (社区) | `.agents/workflows/*.md` | `PLANS.md` | `.agents/plans/` | Plan Mode | `.agents/plans/` |
| `.claude/skills/*/` | `.agents/skills/*/` | `~/.codex/skills/*/` | `.agents/skills/*/` | `~/.kimi/skills/*/` | `.agents/skills/*/` |
| `.claude/output-styles/` | `.agents/output-styles/` | 无直接等价 | 无直接等价 | 无直接等价 | 无直接等价 |
| `~/.claude/projects/*/memory/` | `.agents/memory/` | 无 | 无 | 无 | 无 |

| OpenCode | 通用 | Cursor | 通用 | Copilot | 通用 | Windsurf | 通用 |
|----------|------|--------|------|---------|------|----------|------|
| `AGENTS.md` | `AGENTS.md` | `.cursorrules` | `AGENTS.md` | `copilot-instructions.md` | `AGENTS.md` | `.windsurfrules` | `AGENTS.md` |
| `.opencode/skills/*/` | `.agents/skills/*/` | `.cursor/rules/*.mdc` | `.agents/rules/*.md` | `.github/skills/*/` | `.agents/skills/*/` | `.windsurf/rules/*.md` | `.agents/rules/*.md` |
| `.opencode/agents/` | `.agents/agents/` | 无 | 无 | `.github/agents/` | `.agents/agents/` | 无 | 无 |
| `.opencode/hooks/` | `.agents/hooks/` | 无 | 无 | 无 | 无 | 无 | 无 |
| `.opencode/prompts/` | `.agents/prompts/` | 无 | 无 | `.github/prompts/` | `.agents/prompts/` | 无 | 无 |
| `.opencode/context/` | `.agents/context/` | 无 | 无 | 无 | 无 | 无 | 无 |
| `.opencode/commands/` | `.agents/workflows/` | 无 | 无 | 无 | 无 | 无 | 无 |

---

## 六、一键切换的设计原则

设计转换工具时应遵循：

### 6.1 核心原则

1. **AGENTS.md 是核心** — 所有工具都支持或可以兼容
2. **Skills 使用开放标准** — `.agents/skills/` 是最大公约数
3. **保留工具特定优化** — 转换后可以同时存在 `.claude/`, `.codex/`, `.kimi/`, `.opencode/`
4. **使用 Symlink 减少重复** — 通用文件通过 symlink 共享
5. **层级映射清晰** — 全局→全局，项目根→项目根，规则→Skill，本地覆盖→Override

### 6.2 转换策略

```
┌─────────────────────────────────────────────────────────────┐
│                    通用源目录 (.agents/)                      │
├─────────────────────────────────────────────────────────────┤
│  AGENTS.md → 所有工具的主指令文件                            │
│  skills/   → 所有支持开放标准的工具                          │
│  agents/   → 有 Agent 系统的工具                             │
│  rules/    → 有规则系统的工具                                │
│  hooks/    → 有钩子系统的工具                                │
│  prompts/  → 有提示词系统的工具                              │
│  context/  → 有上下文系统的工具                              │
│  plans/    → 有计划系统的工具                                │
│  workflows/→ 有工作流系统的工具                              │
│  memory/   → 有记忆系统的工具                                │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │ Claude  │    │  Codex  │    │  Kimi   │
        ├─────────┤    ├─────────┤    ├─────────┤
        │.claude/ │    │.codex/  │    │.kimi/   │
        │CLAUDE.md│    │AGENTS.md│    │skills/  │
        │rules/   │    │skills/  │    │agents/  │
        │skills/  │    │config   │    │config   │
        │agents/  │    └─────────┘    └─────────┘
        │settings │
        └─────────┘
              │               │               │
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │OpenCode │    │ Cursor  │    │ Copilot │
        ├─────────┤    ├─────────┤    ├─────────┤
        │.opencode│    │.cursor/ │    │.github/ │
        │skill/   │    │rules/   │    │skills/  │
        │agent/   │    │.mdc     │    │agents/  │
        │hooks/   │    │         │    │prompts/ │
        └─────────┘    └─────────┘    └─────────┘
```

### 6.3 推荐的项目初始化结构

对于新项目，建议采用以下结构以最大化兼容性：

```bash
# 创建通用目录
mkdir -p .agents/{skills,agents,rules,hooks,prompts,context,plans,workflows,memory}

# 创建主指令文件
touch AGENTS.md

# 创建工具特定目录 (使用 symlink)
mkdir -p .claude .codex .kimi .opencode .cursor .github .windsurf

# Symlink 通用文件到工具特定位置
ln -s ../AGENTS.md .claude/CLAUDE.md
ln -s ../AGENTS.md .codex/AGENTS.md
ln -s ../.agents/skills .claude/skills
ln -s ../.agents/skills .codex/skills
ln -s ../.agents/skills .kimi/skills
ln -s ../.agents/skills .opencode/skills
ln -s ../.agents/agents .opencode/agents
ln -s ../.agents/hooks .opencode/hooks
ln -s ../.agents/prompts .opencode/prompts
ln -s ../.agents/context .opencode/context
# ... 等等
```

这样，所有工具都能读取到统一的配置，同时保留了各自工具特定的扩展能力。
