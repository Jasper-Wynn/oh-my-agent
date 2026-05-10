# OpenCode 完整项目目录设计

> 参考: https://opencode.ai/docs/
> 参考: https://open-code.ai/en/docs/
> 参考: https://github.com/48Nauts-Operator/opencode-baseline
> 参考: https://github.com/wesammustafa/OpenCode-Everything-You-Need-to-Know

---

## 一、设计哲学

OpenCode 的目录设计围绕六个核心概念：

1. **AGENTS.md 项目指引** — 类似 Cursor 的 rules，包含 LLM 上下文指令
2. **`.opencode/` 配置目录** — 完整的 Agent 生态配置中心
3. **向上遍历发现** — 从当前目录向上到 git worktree 根目录加载配置
4. **Agent 专业化** — 支持多种内置和自定义 Agent，不同 Agent 可有不同权限
5. **Skill 多路径兼容** — 同时支持 `.opencode/`, `.claude/`, `.agents/` 路径
6. **`/init` 自动初始化** — 扫描项目并自动生成 AGENTS.md

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.config/opencode/
├── config.json                  # OpenCode 全局配置
├── skills/                      # 全局 Skills
│   └── git-release/
│       └── SKILL.md
└── agents/                      # 全局 Agent 定义 (可选)
    └── my-agent.md

~/.claude/skills/                # Claude 兼容路径
~/.agents/skills/                # 通用 Agent 兼容路径
```

> ⚠️ **免责声明**: 以下 `.opencode/` 目录结构示例主要基于社区项目（如 everything-opencode），
> 部分目录（`context/`、`knowledge/`、`0-category.json`）**非 OpenCode 官方标准**。
> 官方标准路径为: `.opencode/agents/`、`.opencode/commands/`、`.opencode/skills/`。

### 2.2 项目层级 (仓库级) — 核心结构

```
your-project/
├── AGENTS.md                    # ★ 项目级指令 (核心文件)
├── opencode.json                # ★ OpenCode 主配置文件
│
├── .opencode/                   # ★ OpenCode 生态目录
│   ├── opencode.json            # 配置 (可与根级合并)
│   ├── README.md                # 内部文档
│   ├── VERSION                  # 版本号
│   │
│   ├── agents/                  # ★ AI Agent 定义
│   │   ├── AGENT_INTEGRATION.md # Agent 集成指南
│   │   ├── core/                # 主 Agent
│   │   │   ├── 0-category.json  # 分类元数据
│   │   │   ├── openagent.md     # OpenAgent 定义
│   │   │   └── opencoder.md     # OpenCoder 定义
│   │   ├── development/         # 开发专家
│   │   │   ├── 0-category.json
│   │   │   ├── backend-specialist.md
│   │   │   ├── frontend-specialist.md
│   │   │   ├── devops-specialist.md
│   │   │   ├── codebase-agent.md
│   │   │   ├── tdd-orchestrator.md
│   │   │   ├── event-sourcing-architect.md
│   │   │   └── graphql-architect.md
│   │   ├── languages/           # 语言专家
│   │   │   ├── golang-pro.md
│   │   │   ├── javascript-pro.md
│   │   │   ├── python-pro.md
│   │   │   ├── rust-pro.md
│   │   │   ├── sql-pro.md
│   │   │   └── typescript-pro.md
│   │   ├── infrastructure/      # 基础设施专家
│   │   │   ├── devops-troubleshooter.md
│   │   │   ├── performance-engineer.md
│   │   │   ├── security-specialist.md
│   │   │   └── terraform-specialist.md
│   │   ├── content/             # 内容创作
│   │   │   ├── copywriter.md
│   │   │   └── technical-writer.md
│   │   ├── data/                # 数据分析
│   │   │   └── data-analyst.md
│   │   ├── meta/                # 系统构建
│   │   │   └── system-builder.md
│   │   ├── architecture/        # 架构设计
│   │   │   ├── c4-context.md
│   │   │   ├── c4-container.md
│   │   │   ├── c4-component.md
│   │   │   └── c4-code.md
│   │   └── subagents/           # 子 Agent
│   │       ├── code/
│   │       │   ├── build-agent.md
│   │       │   ├── codebase-pattern-analyst.md
│   │       │   ├── coder-agent.md
│   │       │   ├── reviewer.md
│   │       │   └── tester.md
│   │       ├── core/
│   │       │   ├── context-retriever.md
│   │       │   ├── documentation.md
│   │       │   └── task-manager.md
│   │       ├── system-builder/
│   │       │   ├── agent-generator.md
│   │       │   ├── command-creator.md
│   │       │   ├── context-organizer.md
│   │       │   ├── domain-analyzer.md
│   │       │   └── workflow-designer.md
│   │       └── utils/
│   │           └── image-specialist.md
│   │
│   ├── commands/                # ★ Slash 命令定义
│   │   ├── clean.md
│   │   ├── commit.md
│   │   ├── test.md
│   │   ├── optimize.md
│   │   ├── context.md
│   │   ├── build-context-system.md
│   │   ├── git-commit.md
│   │   ├── git-flow.md
│   │   ├── git-safety.md
│   │   ├── worktrees.md
│   │   ├── c4-architecture/
│   │   │   └── c4-architecture.md
│   │   ├── full-stack/
│   │   │   └── full-stack-feature.md
│   │   ├── incident-response/
│   │   │   ├── incident-response.md
│   │   │   └── smart-fix.md
│   │   ├── agent-orchestration/
│   │   │   ├── improve-agent.md
│   │   │   └── multi-agent-optimize.md
│   │   └── prompt-engineering/
│   │       ├── prompt-enhancer.md
│   │       └── prompt-optimizer.md
│   │
│   ├── context/                 # ★ 领域知识和上下文
│   │   ├── index.md             # 上下文索引
│   │   ├── core/                # 核心模式与标准
│   │   │   ├── essential-patterns.md
│   │   │   ├── standards/
│   │   │   │   ├── analysis.md
│   │   │   │   ├── code.md
│   │   │   │   ├── docs.md
│   │   │   │   ├── patterns.md
│   │   │   │   └── tests.md
│   │   │   ├── system/
│   │   │   │   └── context-guide.md
│   │   │   └── workflows/
│   │   │       ├── delegation.md
│   │   │       ├── design-iteration.md
│   │   │       ├── review.md
│   │   │       ├── sessions.md
│   │   │       └── task-breakdown.md
│   │   ├── development/         # 开发标准
│   │   │   ├── README.md
│   │   │   ├── api-design.md
│   │   │   ├── clean-code.md
│   │   │   ├── design-assets.md
│   │   │   ├── design-systems.md
│   │   │   ├── react-patterns.md
│   │   │   ├── animation-patterns.md
│   │   │   └── ui-styling-standards.md
│   │   ├── content/             # 内容标准
│   │   │   ├── README.md
│   │   │   ├── copywriting-frameworks.md
│   │   │   └── tone-voice.md
│   │   ├── data/                # 数据标准
│   │   │   └── README.md
│   │   ├── product/             # 产品上下文
│   │   │   └── README.md
│   │   ├── learning/            # 学习资源
│   │   │   └── README.md
│   │   ├── project/             # 项目特定
│   │   │   └── project-context.md
│   │   └── system-builder-templates/  # 系统构建模板
│   │       ├── README.md
│   │       ├── SYSTEM-BUILDER-GUIDE.md
│   │       ├── orchestrator-template.md
│   │       └── subagent-template.md
│   │
│   ├── hooks/                   # 生命周期钩子
│   │   ├── pre_tool_use.py
│   │   ├── post_tool_use.py
│   │   └── session_start.py
│   │
│   ├── skills/                  # ★ 可复用 Skills
│   │   ├── agent-factory/SKILL.md
│   │   ├── aws-solution-architect/SKILL.md
│   │   ├── changelog-generator/SKILL.md
│   │   ├── code-review/SKILL.md
│   │   ├── compound-engineering/SKILL.md
│   │   ├── dev-browser/SKILL.md
│   │   ├── developer-essentials/     # 开发者基础套件
│   │   │   ├── auth-implementation-patterns/SKILL.md
│   │   │   ├── bazel-build-optimization/SKILL.md
│   │   │   ├── e2e-testing-patterns/SKILL.md
│   │   │   ├── error-handling-patterns/SKILL.md
│   │   │   ├── git-advanced-workflows/SKILL.md
│   │   │   ├── monorepo-management/SKILL.md
│   │   │   ├── nx-workspace-patterns/SKILL.md
│   │   │   ├── sql-optimization-patterns/SKILL.md
│   │   │   └── turborepo-caching/SKILL.md
│   │   ├── docx/SKILL.md
│   │   ├── file-organizer/SKILL.md
│   │   ├── frontend-design/SKILL.md
│   │   ├── git-release/SKILL.md
│   │   ├── hook-factory/SKILL.md
│   │   ├── kubernetes/               # K8s 套件
│   │   │   ├── gitops-workflow/
│   │   │   │   ├── SKILL.md
│   │   │   │   └── references/
│   │   │   ├── helm-chart-scaffolding/
│   │   │   │   ├── SKILL.md
│   │   │   │   ├── assets/
│   │   │   │   ├── references/
│   │   │   │   └── scripts/
│   │   │   ├── k8s-manifest-generator/
│   │   │   │   ├── SKILL.md
│   │   │   │   ├── assets/
│   │   │   │   └── references/
│   │   │   └── k8s-security-policies/
│   │   │       ├── SKILL.md
│   │   │       ├── assets/
│   │   │       └── references/
│   │   ├── llm-dev/                  # LLM 开发套件
│   │   │   ├── embedding-strategies/SKILL.md
│   │   │   ├── hybrid-search-implementation/SKILL.md
│   │   │   ├── langchain-architecture/SKILL.md
│   │   │   ├── llm-evaluation/SKILL.md
│   │   │   ├── prompt-engineering-patterns/
│   │   │   │   ├── SKILL.md
│   │   │   │   ├── assets/
│   │   │   │   ├── references/
│   │   │   │   └── scripts/
│   │   │   ├── rag-implementation/SKILL.md
│   │   │   ├── similarity-search-patterns/SKILL.md
│   │   │   └── vector-index-tuning/SKILL.md
│   │   ├── mcp-builder/SKILL.md
│   │   ├── mlops/
│   │   │   └── ml-pipeline-workflow/SKILL.md
│   │   ├── pr-create/SKILL.md
│   │   ├── prd/SKILL.md
│   │   ├── skill-creator/SKILL.md
│   │   ├── systematic-debugging/SKILL.md
│   │   ├── tdd/SKILL.md
│   │   ├── tdd-guide/SKILL.md
│   │   ├── security/                 # 安全套件
│   │   │   ├── attack-tree-construction/SKILL.md
│   │   │   ├── sast-configuration/SKILL.md
│   │   │   ├── security-requirement-extraction/SKILL.md
│   │   │   ├── stride-analysis-patterns/SKILL.md
│   │   │   └── threat-mitigation-mapping/SKILL.md
│   │   └── stripe-integration/SKILL.md
│   │
│   ├── plugins/                 # 扩展/插件
│   │   ├── agent-validator.ts
│   │   ├── notify.ts
│   │   ├── docs/
│   │   │   └── VALIDATOR_GUIDE.md
│   │   ├── tests/
│   │   │   └── validator/
│   │   └── tsconfig.json
│   │
│   ├── tools/                   # 自定义工具
│   │   ├── index.ts
│   │   ├── README.md
│   │   ├── env/
│   │   │   └── index.ts
│   │   ├── gemini/
│   │   │   └── index.ts
│   │   └── template/
│   │       ├── index.ts
│   │       └── README.md
│   │
│   ├── prompts/                 # 模型特定提示词变体
│   │   ├── README.md
│   │   ├── core/
│   │   │   ├── openagent/
│   │   │   │   ├── README.md
│   │   │   │   ├── TEMPLATE.md
│   │   │   │   ├── gemini.md
│   │   │   │   ├── gpt.md
│   │   │   │   ├── grok.md
│   │   │   │   └── llama.md
│   │   │   └── opencoder/
│   │   │       ├── README.md
│   │   │       ├── TEMPLATE.md
│   │   │       ├── gemini.md
│   │   │       ├── gpt.md
│   │   │       ├── grok.md
│   │   │       └── llama.md
│   │   ├── development/
│   │   │   ├── backend-specialist/
│   │   │   │   └── README.md
│   │   │   ├── devops-specialist/
│   │   │   │   └── README.md
│   │   │   └── frontend-specialist/
│   │   │       └── README.md
│   │   ├── content/
│   │   │   ├── copywriter/
│   │   │   │   └── README.md
│   │   │   └── technical-writer/
│   │   │       └── README.md
│   │   └── data/
│   │       └── data-analyst/
│   │           └── README.md
│   │
│   ├── ai-docs/                 # AI 文档/参考
│   │   ├── anthropic_custom_slash_commands.md
│   │   ├── anthropic_docs_subagents.md
│   │   ├── anthropic_output_styles.md
│   │   ├── anthropic_quick_start.md
│   │   ├── cc_hook-path-best-practices.md
│   │   ├── cc_hooks_docs.md
│   │   ├── open-ai_models.md
│   │   ├── open-code.md
│   │   ├── openai_quick_start.md
│   │   ├── user_prompt_submit_hook.md
│   │   └── uv-single-file-scripts.md
│   │
│   ├── scripts/                 # 脚本
│   │   └── patch-hooks.js
│   │
│   └── npm-package/             # npm 包 (用于 hooks)
│       ├── src/
│       │   ├── index.ts
│       │   ├── cli/
│       │   │   ├── pre-tool-use.ts
│       │   │   ├── post-tool-use.ts
│       │   │   ├── pre-compact.ts
│       │   │   ├── session-start.ts
│       │   │   └── user-prompt-submit.ts
│       │   └── queue.test.ts
│       ├── dist/
│       ├── package.json
│       └── tsconfig.json
│
├── .claude/
│   └── skills/                  # Claude 兼容 Skills
├── .agents/
│   └── skills/                  # 通用兼容 Skills
└── README.md
```

### 2.3 OpenCode 兼容的 Hooks (Claude Code 专用)

```
.opencode/hooks-claude-code-only/    # 明确标注为 Claude 专用
├── README.md
├── notification.py
├── post_tool_use.py
├── pre_compact.py
├── pre_tool_use.py
├── session_start.py
├── stop.py
├── subagent_stop.py
├── user_prompt_submit.py
└── utils/
    ├── llm/
    │   ├── anth.py
    │   ├── oai.py
    │   └── ollama.py
    └── tts/
        └── kokoro_tts.py
```

---

## 三、各组成部分详解

### 3.1 AGENTS.md (核心指令文件)

- 每个项目可以有 `AGENTS.md` 文件来指引 OpenCode
- 类似于 Cursor 的 rules，包含 LLM 上下文指令
- 通过 `/init` 命令自动扫描项目并生成或改进

**发现顺序**（从当前目录向上遍历到 git worktree）：
1. `AGENTS.md` — 通用 agent 指令
2. `CLAUDE.md` — Claude 特定指令
3. `CONTEXT.md` — 上下文和背景信息

**全局文件**：
- `~/.opencode/AGENTS.md` — 全局 OpenCode 指令
- `~/.claude/CLAUDE.md` — 全局 Claude 指令

**配置指令**：`opencode.json` 中的 `instructions` 字段可以指定额外文件路径。

**`/init` 命令扫描内容**：
- build, lint, test 命令
- 命令顺序和验证步骤
- 架构和仓库结构
- 项目特定约定和注意事项
- 引用现有的 instruction sources

### 3.2 `opencode.json` (主配置文件)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["packages/*/AGENTS.md"],
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "skill": {
      "*": "allow"
    }
  },
  "agent": {
    "custom-agent": {
      "mode": "subagent",
      "description": "Custom agent for specific tasks",
      "permission": {
        "skill": {
          "internal-*": "deny"
        }
      }
    }
  }
}
```

### 3.3 Agent 定义 (`agents/*.md`)

OpenCode 的 Agent 定义是 Markdown 文件，文件名即 agent 名称。支持 YAML frontmatter：

**必填字段**：
- `description` — agent 用途描述（用于自动匹配）

**常用字段**：
- `mode` — `primary`（主 agent，Tab 切换）/ `subagent`（子 agent，@ 调用）/ `all`
- `model` — 模型 ID，格式 `provider/model-id`
- `temperature` — 0.0-1.0，默认模型相关
- `permission` — 权限对象，`ask` / `allow` / `deny`
- `steps` — 最大迭代步数
- `hidden` — `true` 时隐藏于 @ 自动补全菜单
- `color` — UI 显示颜色（hex 或主题色名）

⚠️ `tools` 字段已废弃，请使用 `permission`。

```markdown
---
description: Backend architecture expert specializing in Node.js/TypeScript APIs
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  read: allow
  edit: ask
  bash: deny
---

# Backend Specialist

You are a backend architecture expert specializing in Node.js/TypeScript APIs.

## Capabilities
- Design RESTful and GraphQL APIs
- Optimize database queries
- Implement authentication and authorization

## Guidelines
- Always validate input with Zod
- Use dependency injection patterns
- Write integration tests for all endpoints
```

### 3.4 Skills (`.opencode/skills/*/SKILL.md`)

OpenCode Skills 使用开放标准格式：

```markdown
---
name: git-release
description: Create a semantic-versioned Git release with changelog generation
license: MIT
compatibility: Requires Git >= 2.20
---

## Workflow
1. Verify working directory is clean
2. Determine next version from conventional commits
3. Generate changelog
4. Create Git tag
5. Push to remote
```

**Skill 发现路径** (向上遍历，直到 git worktree)：
1. `.opencode/skills/<name>/SKILL.md`
2. `.claude/skills/<name>/SKILL.md` (Claude 兼容)
3. `.agents/skills/<name>/SKILL.md` (通用兼容)

**全局 Skills**：
- `~/.config/opencode/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`
- `~/.agents/skills/<name>/SKILL.md`

**Frontmatter 要求**：
- `name` (required) — 必须与目录名一致，1-64 字符，小写字母数字和单连字符
- `description` (required) — 1-1024 字符
- `license` (optional)
- `compatibility` (optional)
- `metadata` (optional) — 字符串到字符串的映射

### 3.5 Commands (`commands/*.md`)

OpenCode 的 Slash 命令定义，文件名即命令名称：

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-sonnet-4-20250514
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

**Frontmatter 字段**：
- `description` (required)
- `agent` (optional) — 执行此命令的 agent
- `model` (optional) — 覆盖默认模型
- `subtask` (optional) — `true` 时强制以 subagent 执行

**模板语法**：
- `$ARGUMENTS` — 用户传入的全部参数
- `$1`, `$2`, `$3`... — 位置参数
- `!`command`` — 注入 shell 命令输出
- `@filename` — 引用文件内容

### 3.6 Context (`context/`)

领域知识组织：
- `core/` — 核心模式与标准 (essential-patterns, standards, workflows)
- `development/` — 开发标准 (api-design, clean-code, react-patterns)
- `content/` — 内容标准 (copywriting-frameworks, tone-voice)
- `data/` — 数据标准
- `product/` — 产品上下文
- `learning/` — 学习资源
- `project/` — 项目特定上下文
- `system-builder-templates/` — 系统构建模板

### 3.7 Prompts (`prompts/`)

模型特定的提示词变体：
- `core/openagent/` — OpenAgent 的模型变体 (gemini, gpt, grok, llama)
- `core/opencoder/` — OpenCoder 的模型变体
- `development/` — 开发专家的提示词
- `content/` — 内容创作的提示词
- `data/` — 数据分析的提示词

### 3.8 Hooks (`hooks/`)

⚠️ OpenCode 官方文档未将 hooks 作为独立功能进行标准化说明。官方提到 "Plugins extend OpenCode with custom tools, hooks, and integrations"，hooks 属于插件系统的一部分。

社区实践中存在的生命周期钩子：
- `pre_tool_use` — 工具调用前
- `post_tool_use` — 工具调用后
- `session_start` — 会话开始时

如需使用，建议通过 `.opencode/plugins/` 或 `plugin` 配置项实现。

### 3.9 Plugins (`plugins/`)

OpenCode 插件系统：
- `agent-validator.ts` — Agent 验证器
- `notify.ts` — 通知插件
- 使用 TypeScript 编写

### 3.10 Tools (`tools/`)

自定义工具：
- `env/` — 环境工具
- `gemini/` — Gemini 集成
- `template/` — 模板工具

---

## 四、关键文件命名规范

| 文件/目录 | 作用域 | 是否提交git | 说明 |
|-----------|--------|------------|------|
| `AGENTS.md` | 项目 | 是 | 核心指令文件 |
| `opencode.json` | 项目 | 是 | 主配置 |
| `.opencode/agents/*.md` | 项目 | 是 | Agent 定义 |
| `.opencode/commands/*.md` | 项目 | 是 | Slash 命令 |
| `.opencode/context/` | 项目 | ⚠️ | 领域知识 (社区约定，非官方标准) |
| `.opencode/hooks/` | 项目 | ⚠️ | 生命周期钩子 (未在官方文档中确认) |
| `.opencode/prompts/` | 项目 | ⚠️ | 提示词变体 (未在官方文档中确认) |
| `.opencode/plugins/` | 项目 | ⚠️ | 插件 (未在官方文档中确认) |
| `.opencode/tools/` | 项目 | ⚠️ | 自定义工具 (未在官方文档中确认) |
| `.opencode/skills/*/SKILL.md` | 项目 | 是 | Skills |
| `~/.config/opencode/skills/` | 全局 | 否 | 全局 Skills |

---

## 五、Monorepo 支持

### 根级 AGENTS.md
```markdown
# Monorepo
General conventions for the entire monorepo.
## Packages
Each package has its own `AGENTS.md` with package-specific rules.
```

### opencode.json
```json
{
  "instructions": ["packages/*/AGENTS.md"]
}
```

### 包级 AGENTS.md
```markdown
# API Package
Express.js API server.
## Routes
- All routes in `src/routes/`
```

---

## 六、转换到其他工具时的映射

| OpenCode | 通用 | Claude | Codex | Kimi |
|----------|------|--------|-------|------|
| `AGENTS.md` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| `.opencode/skills/*/` | `.agents/skills/*/` | `.claude/skills/*/` | `.agents/skills/*/` | `.kimi/skills/*/` |
| `.opencode/agents/*.md` | `.agents/agents/` | `.claude/agents/` | `~/.codex/agents/` | `.kimi/agents/` |
| `.opencode/commands/*.md` | `.agents/commands/` | Plan Mode | `PLANS.md` | `plan mode` |
| `.opencode/context/` | `.agents/context/` | `.claude/docs/` | `.agents/context/` | `.kimi/context/` | ⚠️ 社区约定 |
| `.opencode/hooks/` | `.agents/hooks/` | `.claude/settings.json` (hooks) | `~/.codex/hooks/` | `~/.kimi/hooks/` |
| `.opencode/prompts/` | `.agents/prompts/` | `.claude/output-styles/` | `~/.codex/prompts/` | `~/.kimi/prompts/` |
| `.opencode/plugins/` | `.agents/plugins/` | 无直接等价 | 无直接等价 | 无直接等价 |
| `.opencode/tools/` | `.agents/tools/` | 无直接等价 | 无直接等价 | 无直接等价 |
| `opencode.json` | `.agents/config.json` | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.kimi/config.toml` |
