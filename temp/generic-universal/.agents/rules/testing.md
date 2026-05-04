# Testing Standards

> **作用**: 测试文件规范
> **工具**: 通用
> **作用范围**: `tests/**` 和 `**/*.test.*` 文件

## 影响范围

- **作用域**: `tests/**` 和 `**/*.test.*` 文件
- **加载时机**: 匹配文件进入上下文时 / 始终加载
- **优先级**: 子目录规则 > 父目录规则 > 全局规则

## 格式说明

```yaml
---
description: "测试文件规范"
globs:
  - "src/**/*.ts"
  - "tests/**/*.ts"
alwaysApply: false
---

## Testing Standards

- 规则项 1
- 规则项 2
```

## 注意事项

- 无 `globs` 或 `alwaysApply: true` 表示**始终加载**
- 有 `globs` 表示**仅匹配文件在上下文中时加载**
- 规则之间冲突时，**后加载的规则优先**
