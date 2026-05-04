# Testing

> **作用**: 测试策略和最佳实践
> **工具**: Claude Code
> **原生路径**: `.claude/skills/testing/SKILL.md`

## 说明

Claude Code 原生支持 **Agent Skills** 开放标准。Skills 通过 `SKILL.md` 文件定义，可被 Claude 自动触发或通过 `/skill-name` 调用。

## 格式说明

```markdown
---
name: testing-code
description: |
  Guide test writing, test strategy, and test review.
  Use when asked to write tests, review test coverage,
  or improve test quality.
---

# Testing Skill

## Principles
- Write tests that verify behavior, not implementation
- One concept per test
- Prefer real dependencies over mocks when practical
- Every bug fix includes a regression test

## Process
1. Understand the code under test
2. Identify edge cases and error paths
3. Write the simplest test that covers the requirement
4. Run tests to verify they fail before implementation
5. Refactor with confidence
```

## 来源

- [Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview](https://docs.anthropic.com/en/agents-and-tools/agent-skills/overview)
