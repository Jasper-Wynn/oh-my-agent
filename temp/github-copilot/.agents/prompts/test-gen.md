# Test Generation Prompt

> **作用**: 测试生成提示模板
> **工具**: GitHub Copilot
> **文件名**: `.github/prompts/*.prompt.md`

## 影响范围

- **作用域**: 被调用时
- **加载时机**: 用户选择此 prompt 时
- **用途**: 可复用的提示模板

## 格式说明

```markdown
---
description: "Generate comprehensive unit tests"
---

# Test Generation

Given a function, generate unit tests that:
1. Cover all branches
2. Test edge cases
3. Mock external dependencies
```

## 使用方式

在 Copilot Chat 中选择此 prompt 模板。
