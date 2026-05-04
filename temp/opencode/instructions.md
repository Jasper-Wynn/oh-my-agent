# 项目指令 (AGENTS.md)

> **作用**: OpenCode 项目级主指令文件
> **工具**: OpenCode
> **文件名**: `AGENTS.md`

## 影响范围

- **作用域**: 整个项目
- **加载时机**: 每次会话开始时
- **初始化**: 可用 `/init` 命令自动生成

## 格式说明

纯 Markdown：

```markdown
# Project Name

## Tech Stack
- **Framework**: Next.js 14
- **Language**: TypeScript

## Commands
- `npm run dev` — 开发
- `npm test` — 测试

## Code Standards
- Use strict TypeScript
- Prefer named exports
```

## 配置

`opencode.json` 用于配置 Agent、Skills 权限等：
```json
{
  "instructions": ["packages/*/AGENTS.md"],
  "skills": {
    "permissions": {
      "allow": ["git-release"],
      "deny": ["dangerous-skill"]
    }
  }
}
```
