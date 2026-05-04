# Testing Standards

> **作用**: 测试文件规范
> **工具**: Claude Code
> **原生路径**: `.claude/rules/testing.md`

## 影响范围

- **作用域**: `tests/**` 和 `**/*.test.*` 文件
- **加载时机**: 匹配文件进入上下文时
- **用途**: 测试编写规范和质量标准

## 格式说明

```markdown
---
paths:
  - "tests/**"
  - "**/*.test.*"
  - "**/*.spec.*"
---

# Testing Standards

- Write tests verifying behavior, not implementation
- One assertion per test
- Prefer real dependencies over mocks
- Every bug fix includes regression test
- Run full suite before marking complete: `npm test`
```

## 来源

- [Organize rules with .claude/rules/](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)
- [Path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules)
