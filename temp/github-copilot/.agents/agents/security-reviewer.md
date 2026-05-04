# Security Reviewer Agent

> **作用**: 安全审查专用 Agent
> **工具**: GitHub Copilot
> **文件名**: `.github/agents/*.agent.md`

## 影响范围

- **作用域**: 被调用时的会话
- **加载时机**: `@security-reviewer` 调用时
- **类型**: Custom Agent

## 格式说明

YAML Frontmatter + Markdown：

```markdown
---
name: security-reviewer
description: "Security-focused code reviewer"
model: gpt-5
tools: ["file_read", "file_write", "shell"]
permissions:
  file_write: deny
  bash: deny
---

# Security Reviewer

你是安全专家...
```

## 关键字段

| 字段 | 说明 |
|------|------|
| `name` | Agent 标识 |
| `description` | 用途描述 |
| `model` | 使用的模型 |
| `tools` | 可用工具 |
| `permissions` | 权限控制 |
