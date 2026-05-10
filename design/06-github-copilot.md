# GitHub Copilot 完整项目目录设计

> 参考: GitHub Copilot 官方文档
> 参考: https://github.com/github/awesome-copilot
> 三层架构: Foundation → Specialists → Capabilities

---

## 一、设计哲学

GitHub Copilot 的目录设计围绕**三层架构模型**：

1. **Foundation (基础指令)** — 项目的 DNA，所有 AI 必须遵守
2. **Specialists (专家/Agent)** — 按需调用的预定义 AI 角色
3. **Capabilities (能力/工具)** — 执行具体任务的 Skills、Prompts、Instructions

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.copilot/
├── instructions/                # 个人全局指令
│   └── my-style.instructions.md
├── skills/                      # 个人 Skills
│   └── my-skill/
│       └── SKILL.md
├── agents/                      # 个人 Agents
│   └── my-agent.agent.md
└── prompts/                     # 个人 Prompts
    └── my-prompt.prompt.md

~/.claude/
└── rules/                       # Claude 规则 (Copilot 也读取)

~/.agents/
└── skills/                      # Agent Skills 标准目录
```

### 2.2 项目层级 (仓库级) — 核心结构

```
your-project/
├── .github/                     # ★ GitHub 生态配置中心
│   ├── copilot-instructions.md  # ★ 仓库级基础指令 (所有请求都读取)
│   │
│   ├── instructions/            # ★ 路径特定指令 (按需激活)
│   │   ├── frontend/
│   │   │   ├── react.instructions.md
│   │   │   └── accessibility.instructions.md
│   │   ├── backend/
│   │   │   └── api-design.instructions.md
│   │   └── testing/
│   │       └── unit-tests.instructions.md
│   │
│   ├── prompts/                 # ★ 可复用 Prompt 模板
│   │   ├── test-gen.prompt.md
│   │   ├── doc-review.prompt.md
│   │   └── explain-code.prompt.md
│   │
│   ├── agents/                  # ★ 自定义 Agent 定义
│   │   ├── frontend.agent.md
│   │   ├── backend-api.agent.md
│   │   ├── security-reviewer.agent.md
│   │   └── repo-architect.agent.md
│   │
│   └── skills/                  # ★ Agent Skills (多步骤能力包)
│       ├── webapp-testing/
│       │   ├── SKILL.md
│       │   ├── test-template.js
│       │   └── examples/
│       │       └── login-flow.md
│       └── git-workflow/
│           ├── SKILL.md
│           └── scripts/
│
├── AGENTS.md                    # 跨工具 Agent 指令 (根目录或任意子目录)
├── CLAUDE.md                    # Claude Code 专用 (Copilot 也兼容读取)
├── GEMINI.md                    # Gemini 专用
├── .cursor/                     # Cursor 兼容
│   └── rules/
├── .opencode/                   # OpenCode 兼容
│   └── skills/
└── README.md
```

### 2.3 复杂项目结构示例 (repo-architect Agent 生成)

```
your-project/
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   ├── prompts/
│   ├── agents/
│   └── skills/
│
├── .opencode/                   # 如果 OpenCode CLI 被检测到
│   ├── opencode.json
│   ├── agents/
│   └── skills/ → symlink to .github/skills/ (preferred)
│
├── AGENTS.md                    # CLI 系统提示
│
├── agents/                      # 可选: 项目根级 Agent 定义
│   └── custom.agent.md
│
└── README.md
```

---

## 三、各组成部分详解

### 3.1 `copilot-instructions.md` (基础指令)

**所有 Copilot 请求都会读取**的仓库级基础指令：

```markdown
## Project Overview
This is a Next.js 15 App Router project with TypeScript.

## Build Instructions
- Run `npm install` before building
- Run `npm run test` before committing

## Code Style
- Use functional components
- Named exports only
- Use `cn()` for conditional class names
```

### 3.2 Instructions (`.github/instructions/*.instructions.md`)

**路径特定指令**，按需激活：

```markdown
---
applyTo: "src/components/**/*.tsx,src/components/**/*.jsx"
---

- Use functional components only
- Always use named exports
- Use `cn()` for conditional class names
```

**Frontmatter**：
| 字段 | 说明 |
|------|------|
| `applyTo` | glob 模式，匹配文件时激活 |

### 3.3 Prompts (`.github/prompts/*.prompt.md`)

**可复用提示模板**：

```markdown
---
description: "Generate comprehensive unit tests for a function"
---

# Test Generation Prompt

Given a function, generate unit tests that:
1. Cover all branches
2. Test edge cases
3. Mock external dependencies
4. Use descriptive test names

## Function to test:
{{selection}}
```

### 3.4 Agents (`.github/agents/*.agent.md`)

**预定义 AI 角色/人格**：

```markdown
---
name: security-reviewer
description: "Security-focused code reviewer"
tools: ["file_read", "file_write", "shell"]
---

# Security Reviewer Agent

## Role
You are a security expert focused on finding vulnerabilities.

## Responsibilities
- Check for SQL injection risks
- Verify input validation
- Review authentication flows
- Identify sensitive data exposure

## Output Format
For each issue found, provide:
- Severity: [Critical/High/Medium/Low]
- Location: file and line number
- Description: what the issue is
- Fix: suggested remediation
```

**Frontmatter**：
| 字段 | 说明 |
|------|------|
| `name` | Agent 标识 |
| `description` | Agent 用途描述 |
| `model` | 使用的模型 |
| `tools` | 可用工具列表 |

### 3.5 Skills (`.github/skills/*/SKILL.md`)

**多步骤能力包**，使用开放标准格式：

```markdown
---
name: webapp-testing
description: "End-to-end testing workflow for web applications"
---

## Workflow
1. Analyze the feature to test
2. Identify user flows
3. Write Playwright test scenarios
4. Add test data setup
5. Verify test coverage
```

---

## 四、文件类型对照表

| 文件类型 | 扩展名 | 用途 | Frontmatter |
|----------|--------|------|-------------|
| 基础指令 | `.md` | 全局指令 | 无 |
| 路径指令 | `.instructions.md` | 按路径激活 | `applyTo` |
| 提示模板 | `.prompt.md` | 可复用提示 | `description` |
| 自定义 Agent | `.agent.md` | AI 角色定义 | `name`, `description`, `model`, `tools` |
| Skills | `SKILL.md` | 多步骤工作流 | `name`, `description` |
| 跨工具指令 | `AGENTS.md` | 跨工具兼容 | 无 |

---

## 五、三层架构模型

```
PROJECT ROOT
│
├── [LAYER 1: FOUNDATION]
│   "项目的 DNA"
│   ├── .github/copilot-instructions.md
│   ├── AGENTS.md
│   └── .cursor/rules/base.mdc
│
├── [LAYER 2: SPECIALISTS]
│   "按需调用的专业 Agent"
│   ├── .github/agents/*.agent.md
│   ├── .opencode/agent/
│   └── .cursor/rules/security.mdc
│
└── [LAYER 3: CAPABILITIES]
│   "执行具体任务的技能"
│   ├── .github/skills/*/SKILL.md
│   ├── .github/prompts/*.prompt.md
│   ├── .github/instructions/*.instructions.md
│   └── .windsurf/rules/*.md
```

---

## 六、转换到其他工具时的映射

| GitHub Copilot | 通用 | Claude | Codex | Kimi | OpenCode |
|----------------|------|--------|-------|------|----------|
| `.github/copilot-instructions.md` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| `.github/instructions/*.md` | `.agents/rules/*.md` | `.claude/rules/*.md` | `.agents/skills/*/` | `.agents/skills/*/` | `.opencode/skill/*/` |
| `.github/prompts/*.md` | `.agents/prompts/*.md` | `.claude/output-styles/` | `~/.codex/prompts/` | `~/.kimi/prompts/` | `.opencode/prompts/` |
| `.github/agents/*.md` | `.agents/agents/*.md` | `.claude/agents/` | `~/.codex/agents/` | `.kimi/agents/` | `.opencode/agent/` |
| `.github/skills/*/` | `.agents/skills/*/` | `.claude/skills/*/` | `.agents/skills/*/` | `.kimi/skills/*/` | `.opencode/skill/*/` |
| `applyTo:` | `paths:` | `paths:` | Skill 描述 | Skill 描述 | Skill 描述 |
