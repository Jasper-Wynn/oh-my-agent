# 项目指令 (.windsurfrules / AGENTS.md)

> **作用**: Windsurf / Cascade 项目级主指令文件
> **工具**: Windsurf (Codeium)
> **文件名**: `.windsurfrules` (遗留) / `.windsurf/rules/*.md` (推荐) / `AGENTS.md` (兼容)

## 影响范围

- **作用域**: 整个项目 或匹配文件
- **加载时机**: 每次消息时 / 匹配文件在上下文中时
- **合并方式**: 规则拼接

## 格式说明

### 遗留格式 (.windsurfrules)
纯 Markdown：
```markdown
# Windsurf Rules
## Tech Stack
- Next.js 14
```

### 推荐格式 (.md)
YAML Frontmatter + Markdown：
```markdown
---
trigger: always_on
description: "Core coding standards"
globs:
  - "src/components/**/*.tsx"
---

## Coding Standards
- Use TypeScript strict mode
```

## 激活模式

| 模式 | 配置 |
|------|------|
| Always On | `trigger: always_on` |
| Model Decision | `trigger: model_decision` |
| Glob | `trigger: glob` + `globs` |
| Manual | `trigger: manual` |
