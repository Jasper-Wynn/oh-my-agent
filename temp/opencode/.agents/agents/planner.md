# Planner Agent

> **作用**: 架构规划和实施计划 Agent
> **工具**: OpenCode
> **模式**: primary

## 影响范围

- **作用域**: 主会话
- **加载时机**: Tab 键切换 或自动委派
- **权限**: 可通过 `permissions` 精确控制

## 格式说明

Markdown + YAML Frontmatter：

```markdown
---
name: planner
description: "专门做架构设计，只读不写"
mode: primary
temperature: 0.1
tools:
  read: true
  write: false
  edit: false
  bash: false
permissions:
  edit: deny
  bash: deny
---

# Planner

你是架构规划师...
```

## 使用方式

- **切换**: Tab 键在 primary agents 间切换
- **调用**: 自动根据 `description` 匹配，或用户显式切换
