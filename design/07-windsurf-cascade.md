# Windsurf / Cascade 完整项目目录设计

> 参考: Windsurf 官方文档、社区最佳实践
> Cascade 是 Windsurf 内置的 AI Agent 系统
> 参考: https://github.com/rcore-os/humanize-opencode (Windsurf 相关)

---

## 一、设计哲学

Windsurf (Codeium) 的 Cascade AI 使用 **Rules + Memories + Workflows + Skills** 四层体系：

1. **Rules 模块化** — 从 `.windsurfrules` 单文件演变为 `.windsurf/rules/*.md` 目录
2. **四种激活模式** — Always On / Model Decision / Glob / Manual
3. **自动记忆系统** — `~/.codeium/windsurf/memories/` 持久化记忆
4. **企业级治理** — 支持组织级规则强制下发

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.codeium/
└── windsurf/
    ├── memories/
    │   └── global_rules.md        # 全局规则 (6000 字符限制)
    │                               # ⚠️ workspace rules (.windsurf/rules/*.md) 限制为 12,000 字符/文件
    └── settings.json              # Windsurf 应用设置

# 企业级系统规则 (IT 部署，只读)
# macOS:
/Library/Application Support/Windsurf/rules/*.md
# Linux/WSL:
/etc/windsurf/rules/*.md
# Windows:
C:\ProgramData\Windsurf\rules\*.md
```

### 2.2 项目层级 (仓库级)

```
your-project/
├── .windsurfrules                 # ★ 遗留单文件格式 (仍支持，无激活模式)
├── .windsurf/                     # ★ Windsurf 配置目录
│   └── rules/                     # 工作区规则目录
│       ├── project-overview.md    # 技术栈/架构规则
│       ├── coding-standards.md    # 编码规范
│       ├── testing.md             # 测试规则
│       ├── api-guidelines.md      # API 设计规则
│       ├── security.md            # 安全规则
│       └── 001-core.md            # 编号控制优先级
│
├── memory-bank/                   # 持久化记忆系统 (社区方案)
│   ├── activeContext.md           # 当前活跃上下文
│   ├── productContext.md          # 产品上下文
│   ├── progress.md                # 进度追踪
│   └── decisionLog.md             # 决策日志
│
├── .codeiumignore                 # 排除文件 (类 .gitignore 语法)
├── AGENTS.md                      # 跨工具标准 (Cascade 自动读取)
├── .github/
│   └── copilot-instructions.md    # Copilot 兼容
└── README.md
```

### 2.3 自动生成的记忆

```
~/.codeium/windsurf/memories/
└── <workspace-hash>/
    ├── discovered-commands.json
    ├── code-patterns.json
    ├── user-preferences.json
    └── corrections.json
```

---

## 三、各组成部分详解

### 3.1 Rules 文件格式 (`.windsurf/rules/*.md`)

使用 YAML Frontmatter 控制激活：

```markdown
---
trigger: always_on
description: "Core coding standards for this project"
globs:
  - "src/components/**/*.tsx"
  - "src/components/**/*.ts"
---

## Coding Standards
- Use TypeScript strict mode
- Functional components with named exports
- Colocate tests next to source files
```

**Frontmatter 字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| `trigger` | string | 激活模式: `always_on` / `model_decision` / `glob` / `manual` |
| `description` | string | Model Decision 模式下的描述 |
| `globs` | string[] | Glob 模式下的文件匹配 |

### 3.2 四种激活模式

| 模式 | 配置值 | 说明 |
|------|--------|------|
| **Always On** | `trigger: always_on` | 每次消息都注入上下文 |
| **Model Decision** | `trigger: model_decision` | 仅 description 进入上下文，AI 自行判断 |
| **Glob** | `trigger: glob` + `globs: [...]` | 匹配文件在上下文中时激活 |
| **Manual** | `trigger: manual` | `@rule-name` 手动激活 |

### 3.3 `.windsurfrules` (遗留格式)

单文件格式，仍支持但功能受限：

```markdown
# Windsurf Rules

## Project
- Next.js 14 App Router
- TypeScript strict mode
- Tailwind CSS + shadcn/ui

## Conventions
- Named exports for components
- Co-locate tests with source
- Use Zod for input validation
```

### 3.4 Memory Bank (`memory-bank/`)

社区持久化记忆方案，解决上下文持久化问题：

| 文件 | 用途 |
|------|------|
| `activeContext.md` | 当前会话的活跃上下文 |
| `productContext.md` | 产品背景和业务逻辑 |
| `progress.md` | 当前进度和待办事项 |
| `decisionLog.md` | 架构决策记录 (ADR) |

### 3.5 Auto-Generated Memories

Windsurf **自动生成**的记忆：
- 发现的构建命令
- 代码模式
- 用户偏好
- 用户纠正

存储在 `~/.codeium/windsurf/memories/` 下，不提交到仓库。

### 3.6 `.codeiumignore`

类 `.gitignore` 语法：

```
node_modules/
dist/
*.log
.env
.cursor/
```

---

## 四、文件类型对照表

| 文件类型 | 扩展名 | 用途 | Frontmatter |
|----------|--------|------|-------------|
| 模块化规则 | `.md` (在 rules/) | 主要规则格式 | `trigger`, `description`, `globs` |
| 遗留规则 | `.windsurfrules` | 单文件格式 (遗留) | 无 |
| 记忆文件 | `.md` (在 memory-bank/) | 持久化上下文 | 无 |
| 跨工具指令 | `AGENTS.md` | 跨工具兼容 | 无 |
| 排除文件 | `.codeiumignore` | 文件排除 | 无 |

---

## 五、转换到其他工具时的映射

| Windsurf | 通用 | Claude | Codex | Kimi | OpenCode | Cursor |
|----------|------|--------|-------|------|----------|--------|
| `.windsurfrules` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `.cursorrules` |
| `.windsurf/rules/*.md` | `.agents/rules/*.md` | `.claude/rules/*.md` | `.agents/skills/*/` | `.agents/skills/*/` | `.opencode/skill/*/` | `.cursor/rules/*.mdc` |
| `memory-bank/` | `.agents/memory/` | `~/.claude/projects/*/memory/` | 无直接等价 | 无直接等价 | 无直接等价 | 无直接等价 |
| `.codeiumignore` | `.agents/ignore` | `.claude/ignore` | `.codexignore` | `.kimiignore` | `.opencodeignore` | `.cursorignore` |
| `trigger: always_on` | 无 globs 的 rule | 无 globs 的 rule | 无限制的 skill | 无限制的 skill | 始终加载的 skill | `alwaysApply: true` |
| `trigger: glob` | `paths:` | `paths:` | Skill 描述 | Skill 描述 | Skill 描述 | `globs:` |
| `trigger: model_decision` | Skill 描述 | Skill 描述 | Skill 描述 | Skill 描述 | Skill 描述 | `alwaysApply: false` |
