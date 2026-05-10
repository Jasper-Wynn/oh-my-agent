# Cursor 完整项目目录设计

> 参考: Cursor 官方文档、社区最佳实践
> 参考: https://github.com/getcursor/cursor
> 演变: `.cursorrules` (遗留) → `.cursor/rules/*.mdc` (当前)
> ⚠️ `.cursor/rules/*/RULE.md` 格式被官方文档描述但未实际实现，`.mdc` 是唯一工作的格式

---

## 一、设计哲学

Cursor 的目录设计围绕四个核心概念：

1. **模块化规则系统** — 从单文件 `.cursorrules` 演变为 `.cursor/rules/*.mdc` 目录
2. **四种激活模式** — Always Apply / Auto Attach (Glob) / Agent Requested / Manual
3. **YAML Frontmatter 控制** — `alwaysApply`、`globs`、`description` 精确控制规则加载
4. **Agent Mode 优先** — Agent 模式 (含 Ask/Plan/Debug/Agent 四种模式) 是当前主要交互方式

---

## 二、完整目录结构

### 2.1 全局层级 (用户级)

```
~/.cursor/
├── rules/                       # 全局规则 (跨所有项目)
│   ├── my-style.mdc
│   ├── preferences.mdc
│   └── global-standards.mdc
└── settings.json                # Cursor 应用设置
    # ⚠️ 实际路径: macOS ~/Library/Application Support/Cursor/User/settings.json
    #             Linux ~/.config/Cursor/User/settings.json
```

### 2.2 项目层级 (仓库级)

```
your-project/
├── .cursorrules                 # ★ 遗留单文件格式 (仍支持，Agent 模式不读取)
├── .cursor/                     # ★ Cursor 配置目录 (0.43+)
│   └── rules/                   # 模块化规则目录
│       ├── base.mdc             # 基础规则 (alwaysApply: true)
│       ├── 001-base.mdc         # 编号前缀控制加载优先级
│       ├── 010-frontend.mdc
│       ├── 020-backend.mdc
│       ├── typescript.mdc       # TypeScript 规则
│       ├── react.mdc            # React 组件规则
│       ├── api.mdc              # API 路由规则
│       ├── testing.mdc          # 测试规则
│       ├── security/
│       │   └── review.mdc       # 子目录支持
│       └── index.mdc            # 主规则文件入口
│
├── .cursorignore                # 排除文件索引 (类 .gitignore 语法)
├── AGENTS.md                    # 跨工具标准 (Cursor 也支持读取)
├── .github/
│   └── copilot-instructions.md  # Copilot 兼容
└── README.md
```

### 2.3 企业/系统级配置

> ⚠️ Cursor Enterprise 的 Team Rules 通过 Dashboard (Web UI) 管理，
> 未确认是否支持本地文件系统路径配置。

---

## 三、各组成部分详解

### 3.1 MDC 文件格式 (`.cursor/rules/*.mdc`)

**核心文件类型**，使用 YAML Frontmatter：

```markdown
---
description: "React component standards"
globs: ["src/components/**/*.tsx", "src/components/**/*.jsx"]
alwaysApply: false
---

## React Component Rules
- Functional components only
- Named exports for all components
- Use `cn()` for conditional class names
```

**Frontmatter 字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| `description` | string | Agent 判断相关性时的描述 |
| `globs` | string[] | 文件匹配模式 (Auto Attach 模式) |
| `alwaysApply` | boolean | 是否始终加载 |

### 3.2 四种激活模式

| 模式 | 配置方式 | 说明 |
|------|----------|------|
| **Always Apply** | `alwaysApply: true` | 每次会话都注入上下文 |
| **Auto Attach (Glob)** | `globs: [...]` | 匹配文件出现在上下文时激活 |
| **Agent Requested** | `alwaysApply: false` + `description` | AI 根据描述判断相关性 |
| **Manual** | `@rule-name` | 手动 @ 提及激活 |

### 3.3 规则加载优先级

```
001-base.mdc      (最先加载)
010-frontend.mdc  (其次)
020-backend.mdc   (再次)
security/         (子目录)
```

编号前缀控制加载顺序，数字越小越先加载。

### 3.4 `.cursorrules` (遗留格式)

**单文件格式**，仍支持但功能受限：

```markdown
# Cursor Rules

## Tech Stack
- Next.js 14
- TypeScript
- Tailwind CSS

## Code Style
- Use functional components
- Named exports only
```

**限制**：
- Agent 模式不读取 `.cursorrules`
- 无激活模式控制
- 无路径范围限定

### 3.5 `.cursorignore`

类 `.gitignore` 语法，排除文件索引：

```
node_modules/
dist/
*.log
.env
```

### 3.6 与 AGENTS.md 的关系

Cursor 支持读取 `AGENTS.md` 作为跨工具兼容层：
- 根级 `AGENTS.md` = Always On
- 子目录 `AGENTS.md` = 该目录及子树生效
- 但功能弱于原生 MDC (无 frontmatter 控制)

---

## 四、文件类型对照表

| 文件类型 | 扩展名 | 用途 | Frontmatter |
|----------|--------|------|-------------|
| 模块化规则 | `.mdc` | 主要规则格式 | `description`, `globs`, `alwaysApply` |
| 遗留规则 | `.cursorrules` | 单文件格式 (遗留) | 无 |
| 跨工具指令 | `AGENTS.md` | 跨工具兼容 | 无 |
| 全局规则 | `.mdc` (在 `~/.cursor/rules/`) | 跨项目规则 | `description`, `globs`, `alwaysApply` |
| 排除文件 | `.cursorignore` | 文件排除 | 无 |

---

## 五、转换到其他工具时的映射

| Cursor | 通用 | Claude | Codex | Kimi | OpenCode |
|--------|------|--------|-------|------|----------|
| `.cursorrules` | `AGENTS.md` | `.claude/CLAUDE.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| `.cursor/rules/*.mdc` | `.agents/rules/*.md` | `.claude/rules/*.md` | `.agents/skills/*/` | `.agents/skills/*/` | `.opencode/skills/*/` |
| `~/.cursor/rules/*.mdc` | `~/.agents/rules/*.md` | `~/.claude/rules/*.md` | `~/.agents/skills/*/` | `~/.agents/skills/*/` | `~/.config/opencode/skills/*/` |
| `.cursorignore` | `.agents/ignore` | `.claude/ignore` | `.codexignore` | `.kimiignore` | `.opencodeignore` |
| `alwaysApply: true` | 无 globs 的 rule | 无 globs 的 rule | 无限制的 skill | 无限制的 skill | 始终加载的 skill |
| `globs: [...]` | `paths:` | `paths:` | Skill 描述 | Skill 描述 | Skill 描述 |
