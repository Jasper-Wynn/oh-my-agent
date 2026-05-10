# Planner Agent

> **作用**: 架构规划和实施计划 Agent
> **工具**: OpenCode
> **模式**: primary

## 影响范围

- **作用域**: 主会话
- **加载时机**: Tab 键切换 或自动委派
- **权限**: 可通过 `permission` 精确控制

## 格式说明

Markdown + YAML Frontmatter（文件名即 agent 名称，无需 `name` 字段）：

```markdown
---
description: "专门做架构设计，只读不写"
mode: primary
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

# Planner

你是架构规划师...
```

## 使用方式

- **切换**: Tab 键在 primary agents 间切换
- **调用**: 自动根据 `description` 匹配，或用户显式切换
