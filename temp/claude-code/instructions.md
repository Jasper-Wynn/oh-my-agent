# 项目指令 (CLAUDE.md)

> **作用**: Claude Code 项目级主指令文件
> **工具**: Claude Code
> **文件名**: `CLAUDE.md` (项目根) / `.claude/CLAUDE.md` (项目子目录)

## 影响范围

- **作用域**: 整个项目（也可在子目录 `*/CLAUDE.md` 中限定模块级作用域）
- **加载时机**: 会话开始时自动读取
- **合并方式**: 所有发现的文件**拼接**到上下文中，后加载的覆盖先加载的
- **层级**: `~/.claude/CLAUDE.md` → `./CLAUDE.md` → `src/*/CLAUDE.md` → `CLAUDE.local.md`

## 格式说明

纯 Markdown，**无 YAML Frontmatter**（但 `.claude/rules/*.md` 可用 `paths` frontmatter）：

```markdown
## Project
- 项目类型: Next.js / React / TypeScript
- 核心命令: npm run dev, npm test

## Stack
- Framework: Next.js 14
- ORM: Prisma

## Conventions
- 使用 named exports
- 组件文件共置

## Do Not
- 不要使用 `any` 类型
```

## 最佳实践

- 项目级不超过 **200 行**（避免消耗过多上下文）
- 避免人格指令（"Be a senior engineer"）
- 避免 @-mention 文档（会每次全量注入）
- 不写 formatter/linter 已覆盖的规则
- 多步骤流程或特定模块的指令，移至 [Skills](https://code.claude.com/docs/en/skills) 或 [Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)

## 本地覆盖

`CLAUDE.local.md` 放在项目根目录，gitignore，用于个人本地覆盖。

## Claude Code 功能清单

| 功能 | 路径 | 文档 |
|------|------|------|
| 项目指令 | `CLAUDE.md` / `.claude/CLAUDE.md` | [Memory](https://code.claude.com/docs/en/memory) |
| 规则 | `.claude/rules/*.md` | [Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |
| 设置 | `.claude/settings.json` | [Settings](https://code.claude.com/docs/en/settings) |
| Skills | `.claude/skills/<name>/SKILL.md` | [Skills](https://code.claude.com/docs/en/skills) |
| 子代理 | `.claude/agents/*.md` | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| 输出风格 | `.claude/output-styles/*.md` | [Output Styles](https://code.claude.com/docs/en/output-styles) |
| MCP | `.mcp.json` | [MCP](https://code.claude.com/docs/en/mcp) |
| 计划 | `~/.claude/plans/` (默认) | [Plan Mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) |
| 记忆 | `~/.claude/projects/<project>/memory/` | [Auto Memory](https://code.claude.com/docs/en/memory#auto-memory) |

## 来源

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
