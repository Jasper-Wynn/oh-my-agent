# Code Style

> **作用**: 通用代码风格规范
> **工具**: Claude Code
> **原生路径**: `.claude/rules/code-style.md`

## 影响范围

- **作用域**: 所有文件（无条件加载）或特定路径（条件加载）
- **加载时机**: 启动时（无条件）或匹配文件进入上下文时（有条件）
- **优先级**: 子目录规则 > 父目录规则 > 用户级规则 > 全局规则

## 格式说明

Claude Code 的 rules 使用 YAML frontmatter 中的 `paths` 字段限定作用范围：

### 无条件加载（全局规则）

```markdown
# Code Style Rules

- Use 2-space indentation
- Prefer named exports over default exports
- Use strict TypeScript mode
```

### 条件加载（路径限定）

```markdown
---
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
---

# TypeScript Code Style

- Use explicit return types on public APIs
- Avoid `any` type; use `unknown` with type guards
- Prefer interfaces over types for object shapes
```

## 路径匹配模式

| 模式 | 匹配 |
|------|------|
| `**/*.ts` | 所有 TypeScript 文件 |
| `src/**/*` | `src/` 下的所有文件 |
| `src/components/*.tsx` | 特定目录下的 React 组件 |
| `src/**/*.{ts,tsx}` | 多种扩展名 |

## 来源

- [Organize rules with .claude/rules/](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)
- [Path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules)
