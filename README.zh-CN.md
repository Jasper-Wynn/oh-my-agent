# Oh My Agent 🎯

> **跨工具统一的 AI Agent 项目脚手架** — 一套目录结构，兼容所有主流 AI 工具。

[English README](./README.md)

---

## 为什么需要它？

每个 AI 编程工具都有自己的配置格式：
- Claude Code → `CLAUDE.md` + `.claude/skills/`
- Cursor → `.cursorrules` + `.cursor/rules/*.mdc`
- Kimi → `AGENTS.md` + `.kimi/agents/`
- Codex → `AGENTS.md` + `.codex/`
- Copilot → `.github/copilot-instructions.md`
- Windsurf → `.windsurfrules` + `.windsurf/rules/`
- OpenCode → `AGENTS.md` + `.opencode/`

**管理 7 种格式太痛苦了。** Oh My Agent 引入**两层架构**：

```
.agents/          ← 通用层（写一次）
  ├── skills/     ← 跨工具 Skills
  ├── agents/     ← Agent 定义
  ├── rules/      ← 共享规则
  ├── hooks/      ← 生命周期钩子
  ├── prompts/    ← 提示词模板
  └── context/    ← 共享上下文

.<tool>/          ← 原生层（转换生成）
  └── (各工具原生格式)
```

## 快速开始

1. **复制脚手架**到你项目：
   ```bash
   # 以 Claude Code 为例
   cp -r temp/claude-code/.agents ./my-project/
   cp -r temp/claude-code/.claude ./my-project/
   ```

2. **定制**通用层 `.agents/`：
   - 编辑 `.agents/skills/code-review/SKILL.md`
   - 在 `.agents/rules/` 添加规则
   - 在 `.agents/agents/` 定义 Agent

3. **同步**到原生层（手动或脚本）：
   - `.agents/skills/` → `.claude/skills/`、`.cursor/skills/` 等
   - `AGENTS.md` → 项目根目录

## 仓库结构

```
oh-my-agent/
├── design/                    # 设计规范（9 篇文档）
│   ├── 01-claude-code.md      # Claude Code 完整设计
│   ├── 02-codex.md            # OpenAI Codex 完整设计
│   ├── 03-kimi.md             # Kimi Code CLI 完整设计
│   ├── 04-opencode.md         # OpenCode 完整设计
│   ├── 05-cursor.md           # Cursor 完整设计
│   ├── 06-github-copilot.md   # GitHub Copilot 完整设计
│   ├── 07-windsurf-cascade.md # Windsurf 完整设计
│   ├── 08-generic-universal.md   # 跨工具兼容层设计
│   └── 09-custom-agents-guide.md # 自定义 Agent 实现指南
│
├── temp/                      # 脚手架模板（8 个工具）
│   ├── claude-code/
│   ├── codex/
│   ├── cursor/
│   ├── generic-universal/     # 跨工具通用脚手架
│   ├── github-copilot/
│   ├── kimi/
│   ├── opencode/
│   └── windsurf/
│
├── README.md
├── README.zh-CN.md
├── LICENSE
└── CONTRIBUTING.md
```

## 设计哲学

1. **最大公约数**: `AGENTS.md` + `.agents/skills/` + `.agents/agents/` + `.agents/hooks/` + `.agents/prompts/` + `.agents/context/`
2. **一次编写，处处运行**: 在 `.agents/` 中定义，转换到各工具原生格式
3. **工具无关**: 无厂商锁定，可在工具间无缝迁移
4. **面向未来**: 基于行业收敛趋势（YAML Frontmatter、Skill 开放标准、Memory Bank）

## 功能支持矩阵

| 工具 | 主指令文件 | Skills | Agents | Hooks | Prompts | Plan 模式 |
|------|-----------|--------|--------|-------|---------|----------|
| Claude Code | `CLAUDE.md` | ✅ | ✅ (Subagents) | ✅ | ✅ | ✅ |
| Cursor | `.cursorrules`/`.mdc` | ✅ | ✅ (Subagents) | ✅ | ✅ | ✅ |
| Kimi | `AGENTS.md` | ✅ | ✅ (agent.yaml) | ✅ | ✅ | ✅ |
| Codex | `AGENTS.md` | ✅ | ⚠️ (Profiles) | ✅ | ⚠️ | ❌ |
| Copilot | `copilot-instructions.md` | ✅ | ✅ | ✅ | ✅ | ❌ |
| Windsurf | `.windsurfrules`/`.md` | ✅ | ⚠️ (ACC) | ✅ | ⚠️ | ❌ |
| OpenCode | `AGENTS.md` | ✅ | ✅ | ✅ | ✅ | ❌ |

> 所有声明均基于官方文档验证，详见 [AUDIT_REPORT.md](./AUDIT_REPORT.md)。

## 贡献

欢迎提交 Issue 和 PR！详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 许可证

[MIT License](./LICENSE)
