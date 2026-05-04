# 项目指令 (.cursorrules / AGENTS.md)

> **作用**: Cursor 项目级主指令文件
> **工具**: Cursor
> **文件名**: `.cursorrules` (遗留) / `.cursor/rules/*.mdc` (推荐) / `AGENTS.md` (兼容)

## 影响范围

- **作用域**: 整个项目（`.cursorrules` 全局）或匹配文件（`.mdc` globs）
- **加载时机**: 会话开始时 / 匹配文件进入上下文时
- **合并方式**: 所有规则拼接，后加载的覆盖先加载的

## 格式说明

### 遗留格式 (.cursorrules)
纯 Markdown：
```markdown
# Cursor Rules
## Tech Stack
- Next.js 14
## Code Style
- Use functional components
```

### 推荐格式 (.mdc)
YAML Frontmatter + Markdown：
```markdown
---
description: "React component standards"
globs: ["src/components/**/*.tsx"]
alwaysApply: false
---

## React Rules
- Functional components only
```

## 激活模式

| 模式 | 配置 |
|------|------|
| Always Apply | `alwaysApply: true` |
| Auto Attach | `globs: [...]` |
| Agent Requested | `alwaysApply: false` + `description` |
| Manual | `@rule-name` |
