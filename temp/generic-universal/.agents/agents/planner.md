# Planner Agent (通用模板)

> **作用**: 架构规划师 Agent
> **支持工具**: OpenCode ✅ / Kimi ✅ / Copilot ✅ / Codex ⚠️ / Claude ⚠️ / Cursor ❌ / Windsurf ❌

## 影响范围

- **作用域**: 主会话 或子会话
- **加载时机**: Tab 切换 / @mention / Task 委派
- **权限**: 只读（无 write/edit/bash 权限）

## 格式说明

通用 Markdown + YAML Frontmatter：

```markdown
---
description: "Architecture planning specialist, read-only"
mode: primary       # primary | subagent
# OpenCode 用
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
# Copilot 用
model: gpt-5
permissions:
  file_write: deny
---

# Planner

你是架构规划师...
```

## 转换映射

| 工具 | 目标路径 | 备注 |
|------|---------|------|
| OpenCode | `.opencode/agents/planner.md` | 直接可用 |
| Kimi | `.kimi/agents/planner/` (agent.yaml + system.md) | 需拆分 |
| Copilot | `.github/agents/planner.agent.md` | 直接可用 |
| Codex | `.agents/skills/planner/SKILL.md` | 作为 Skill |
| Claude | `.claude/rules/planner.md` | 作为 Rule |
| Cursor | `.cursor/rules/planner.mdc` | 作为 Rule |
| Windsurf | `.windsurf/rules/planner.md` | 作为 Rule |
