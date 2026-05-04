# 项目指令 (跨工具通用)

> **作用**: 跨工具兼容的主指令文件
> **工具**: 所有 AI Agent 工具
> **文件名**: `AGENTS.md`（最大公约数）

## 影响范围

- **作用域**: 整个项目
- **加载时机**: 所有支持 AGENTS.md 的工具都会读取
- **兼容性**: Claude ⚠️ / Codex ✅ / Kimi ✅ / OpenCode ✅ / Cursor ⚠️ / Copilot ✅ / Windsurf ✅

## 格式说明

纯 Markdown，避免工具特定语法：

```markdown
# Project Name

## Tech Stack
- **Language**: TypeScript
- **Framework**: Next.js 14

## Project Structure
- `src/` — Source code
- `tests/` — Test files

## Commands
- `npm run dev` — Development
- `npm test` — Tests

## Code Conventions
- camelCase for variables
- PascalCase for components
- Prefer named exports

## Testing
- Unit tests for utilities
- Integration tests for APIs
- >80% coverage target

## Do Not
- Do not commit secrets
- Do not modify core logic without tests
```

## 最佳实践

- 保持精简（< 100 行）
- 提供具体示例而非模糊规则
- 包含 rationale（为什么有这个规则）
