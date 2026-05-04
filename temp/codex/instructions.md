# 项目指令 (AGENTS.md)

> **作用**: Codex 项目级主指令文件
> **工具**: OpenAI Codex
> **文件名**: `AGENTS.md` (项目级) / `~/.codex/AGENTS.md` (全局)

## 影响范围

- **作用域**: 从当前目录向上到项目根的所有目录
- **加载时机**: 每次运行 Codex 时构建指令链
- **合并方式**: 从上到下拼接，用空行连接，后出现的覆盖前面的
- **大小限制**: 默认 `project_doc_max_bytes = 32 KiB`
- **层级**: `~/.codex/AGENTS.md` → `AGENTS.md` → `*/AGENTS.md` → `*/AGENTS.override.md`

## 格式说明

纯 Markdown，**无 YAML Frontmatter**：

```markdown
# Project Name

## Tech Stack
- **Framework**: Next.js 14
- **Language**: TypeScript

## Commands
- `npm run dev` — 开发服务器
- `npm test` — 运行测试

## Code Standards
- Use strict TypeScript
- Prefer named exports

## Do Not
- Do not commit secrets
```

## 覆盖文件

`AGENTS.override.md` 用于临时覆盖，优先级高于同目录的 `AGENTS.md`。

## 配置

在 `~/.codex/config.toml` 中可配置：
```toml
project_doc_max_bytes = 32768
project_doc_fallback_filenames = ["TEAM_GUIDE.md"]
```
