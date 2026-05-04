# System Prompt

> **作用**: 系统提示模板
> **工具**: Kimi
> **类型**: 系统提示模板

## 影响范围

- **作用域**: 特定 Agent 或全局
- **加载时机**: Agent 初始化时注入
- **用途**: 自定义系统提示的基础行为

## 格式说明

纯 Markdown 文件，作为系统提示模板：

```markdown
# System Prompt

你是 {ROLE_NAME}，专门负责 {TASK}。

## 核心能力
- 能力 1
- 能力 2

## 约束
- 约束 1
- 约束 2
```

## 变量注入

部分工具支持模板变量：
- `{ROLE_ADDITIONAL}` — 角色补充说明
- `{KIMI_WORK_DIR}` — 工作目录
- `{KIMI_AGENTS_MD}` — AGENTS.md 内容
