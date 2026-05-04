# TDD

> **作用**: 测试驱动开发流程
> **工具**: OpenCode
> **加载方式**: 按需加载 / 显式调用

## 影响范围

- **作用域**: 当前工作目录及其子目录
- **加载时机**: Agent 判断任务匹配 description 时自动加载，或用户显式调用
- **优先级**: Project 级 > User 级 > System 级

## 格式说明

使用 YAML Frontmatter + Markdown 内容：

```yaml
---
name: tdd
description: "测试驱动开发流程"
---

## 工作流程
1. 步骤一
2. 步骤二
3. 步骤三
```

## 注意事项

- `description` 是**最关键**的字段，决定 Agent 是否会自动选择此 Skill
- 保持 Skill 内容精简，详细内容放入 `references/` 或 `scripts/`
