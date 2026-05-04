# 项目指令 (copilot-instructions.md / AGENTS.md)

> **作用**: GitHub Copilot 项目级基础指令
> **工具**: GitHub Copilot (VS Code)
> **文件名**: `.github/copilot-instructions.md`

## 影响范围

- **作用域**: 整个仓库（所有 Copilot 请求都读取）
- **加载时机**: 每次 Copilot 请求时
- **层级**: Foundation（基础指令）→ Specialists（Agents）→ Capabilities（Skills/Prompts）

## 格式说明

纯 Markdown：

```markdown
## Project Overview
This is a Next.js 15 App Router project.

## Build Instructions
- Run `npm install` before building
- Run `npm run test` before committing

## Code Style
- Use functional components
- Named exports only
```

## 路径特定指令

`.github/instructions/*.instructions.md` 可限定作用范围：
```markdown
---
applyTo: "src/components/**/*.tsx"
---
- Use functional components only
```
