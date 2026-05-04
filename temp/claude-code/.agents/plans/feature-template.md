# Plans (计划模板)

> **作用**: 计划模式下的任务分解模板
> **工具**: Claude Code
> **原生路径**: `~/.claude/plans/` (通过 `plansDirectory` 配置)

## 说明

Claude Code 支持**计划模式 (Plan Mode)**，在 `/plan` 命令或 `--plan` 标志下，Claude 先制定修改计划，经你批准后再执行。

计划文件默认存储在 `~/.claude/plans/` 目录下，可通过 `plansDirectory` 设置自定义路径。

## 格式说明

计划模式不依赖固定模板格式，但建议按以下结构组织：

```markdown
# Plan: [功能名称]

## Goal
[清晰的目标描述]

## Analysis
[对代码库的初步分析]

## Steps
1. [ ] 步骤 1: [具体操作] → Verify: [验证方式]
2. [ ] 步骤 2: [具体操作] → Verify: [验证方式]

## Risks
- [风险 1] → Mitigation: [缓解措施]

## Verification
- [ ] 所有测试通过
- [ ] 无回归问题
```

## 配置

在 `.claude/settings.json` 中配置计划目录：

```json
{
  "plansDirectory": "./plans"
}
```

## 来源

- [Plan Mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
