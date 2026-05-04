# Tester Agent

> **作用**: 测试编写和执行 Agent
> **工具**: OpenCode
> **模式**: subagent

## 影响范围

- **作用域**: 被 primary agent 委派 或用户 @mention
- **加载时机**: Task 工具调用 或 @tester
- **权限**: 独立配置

## 格式说明

```markdown
---
name: tester
description: "专门写测试和运行测试"
mode: subagent
---

# Tester

你是测试专家...
```

## 使用方式

- **调用**: `@tester` 在消息中提及
- **委派**: Primary agent 通过 Task 工具自动调用
