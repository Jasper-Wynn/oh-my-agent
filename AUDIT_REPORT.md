# Design/ 文档准确性审计报告

> 审计日期: 2026-05-01
> 审计方法: 4 个并行 subagent 深度审计 + 官方文档抓取 + 社区来源交叉验证
> 规则: 每条声明必须有来源，禁止猜测

---

## 审计总览

| 文档 | 评分 | 严重错误 | 未确认/待修正 | 状态 |
|------|------|---------|--------------|------|
| design/01-claude-code.md | **70/100** | 2 | 3 | Hooks 机制严重错误 |
| design/02-codex.md | **75/100** | 2 | 4 | Hooks 机制严重错误 |
| design/03-kimi.md | **88/100** | 0 | 2 | 最准确 |
| design/04-opencode.md | **65/100** | 4 | 5 | 目录名+配置结构错误 |
| design/05-cursor.md | **62/100** | 7 | 2 | 混合了 Windsurf 概念 |
| design/06-github-copilot.md | **82/100** | 1 | 3 | 虚构 model 字段 |
| design/07-windsurf-cascade.md | **85/100** | 1 | 3 | Agent Command Center 歧义 |
| design/08-generic-universal.md | — | **6+** | 4 | 对照表大量错误 |
| design/09-custom-agents-guide.md | — | **4+** | 2 | 总览表严重错误 |

---

## 一、共性严重错误（多个文档重复）

### 🔴 错误模式 A: Hooks 被错误描述为脚本目录

| 文档 | 错误声明 | 正确机制 |
|------|---------|---------|
| 01-claude-code.md | `.claude/hooks/*.py` | `settings.json` 中配置 JSON hooks，`.claude/hooks/` 只是脚本存放的可选目录 |
| 02-codex.md | `~/.codex/hooks/*.sh` | `hooks.json` 或 `config.toml` 内联 `[hooks]` 配置 |
| 03-kimi.md | `~/.kimi/hooks/` 作为配置机制 | Hooks 通过 `~/.kimi/config.toml` 的 `[[hooks]]` 数组配置 |

**根因**: 将所有工具的 hooks 都想象成 Claude Code 的 `.claude/hooks/` 目录形式，未查各工具实际配置方式。

---

## 二、逐文档详细审计

### design/01-claude-code.md (Claude Code)

#### ❌ 严重错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | `.claude/hooks/*.py` 是原生 hooks | Hooks 在 `settings.json` 中以 JSON 配置；`.claude/hooks/` 只是可选脚本存放目录 | https://code.claude.com/docs/en/hooks |
| 2 | 自动记忆文件是 `.json` (build-commands.json 等) | 自动记忆是 `.md` 文件，入口为 `MEMORY.md`，主题如 `debugging.md` | https://code.claude.com/docs/en/memory#auto-memory |

#### ⚠️ 需修正

| # | 声明 | 说明 |
|---|------|------|
| 3 | "~150-200 条指令上限" | 官方只说 "target under 200 lines per CLAUDE.md file"，不是硬性指令上限 |
| 4 | 三层层级 (Global→Project→Local) | 遗漏了 Managed Policy 层 (组织级 `/Library/Application Support/ClaudeCode/CLAUDE.md`) |
| 5 | Rules frontmatter 含 `description` | `description` 是 Skills 的字段，Rules 官方只展示了 `paths:` |

---

### design/02-codex.md (OpenAI Codex)

#### ❌ 严重错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | `~/.codex/hooks/` 下 `.sh` 文件 | Codex 使用 `hooks.json` 或 `config.toml` 内联 `[hooks]`，事件名为 SessionStart/PreToolUse/PermissionRequest/PostToolUse/UserPromptSubmit/Stop | https://developers.openai.com/codex/hooks |
| 2 | `~/.codex/plans/` 目录 | 官方文档中**不存在**该目录概念 | — |

#### ⚠️ 需修正/标注

| # | 声明 | 说明 |
|---|------|------|
| 3 | `PLANS.md` | Codex 有内置 plan skill 和 plan tool，但 `PLANS.md` 作为独立文件格式官方未明确提及 |
| 4 | `~/.codex/prompts/` | 官方文档中未找到该目录的明确说明 |
| 5 | `codex /init` 命令 | 官方文档中未找到该命令的明确说明 |
| 6 | `.codex/agents/` 目录 | 第三方集成文档有提及，但官方文档未明确确认 |

---

### design/03-kimi.md (Kimi Code CLI)

#### ⚠️ 需修正

| # | 声明 | 说明 |
|---|------|------|
| 1 | `~/.kimi/hooks/` 作为配置机制 | Hooks 通过 `~/.kimi/config.toml` 的 `[[hooks]]` 数组配置，目录只是脚本存放的推荐位置 |
| 2 | `~/.kimi/prompts/` | Kimi 有内置 `src/kimi_cli/prompts/`，但用户级 `~/.kimi/prompts/` 未在官方文档中明确 |

**总体评价**: Kimi 文档最准确 (88/100)。

---

### design/04-opencode.md (OpenCode)

#### ❌ 严重错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | `.opencode/agent/` (单数) | 官方使用 `.opencode/agents/` (复数) | https://open-code.ai/en/docs/agents |
| 2 | `.opencode/command/` (单数) | 官方使用 `.opencode/commands/` (复数) | https://opencode.ai/docs/commands/ |
| 3 | `.opencode/context/` 目录 | 官方文档中**不存在**该标准目录 | — |
| 4 | `.opencode/knowledge/` 目录 | 官方文档中**不存在**该目录 | — |
| 5 | `opencode.json` 中 `skills.permissions.allow/deny` | 官方格式是 `permission.skill` (如 `"*": "allow"`)，不是 `skills.permissions.allow` 数组；`agents` 应为 `agent` (单数) | https://opencode.ai/docs/skills/ |

#### ⚠️ 需修正/标注

| # | 声明 | 说明 |
|---|------|------|
| 6 | `.opencode/skill/` (单数) | 官方文档写 `.opencode/skills/` (复数)，但社区迁移指南说新版用 `skill/` (单数，在项目根)。需进一步确认 |
| 7 | `.opencode/prompts/` | 官方文档未明确确认项目级 prompts 目录 |
| 8 | `.opencode/hooks/` | OpenCode hooks 主要通过 plugin 系统实现，未在官方文档中作为标准项目级目录确认 |
| 9 | `0-category.json` | 这是 everything-opencode 等社区项目的约定，**不是官方标准** |

**总体评价**: 最需要修订 (65/100)。

---

### design/05-cursor.md (Cursor)

#### ❌ 严重错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | `~/.cursor/settings.json` | 实际路径: macOS `~/Library/Application Support/Cursor/User/settings.json`, Linux `~/.config/Cursor/User/settings.json` | — |
| 2 | `~/.cursor/global_rules.md` | 这是 **Windsurf** 的文件，Cursor 不存在此文件 | https://docs.windsurf.com/windsurf/cascade/memories |
| 3 | 6000 字符限制 | 这是 **Windsurf/Cascade** 的限制，Cursor 的 `.cursorrules` 没有硬性字符限制 | — |
| 4 | Custom Agents 支持 | Cursor 2.1 **移除了** Custom Modes，当前不支持用户自定义 Agents (注意: 2.4+ 支持 Subagents，但 Subagents 和 Custom Agents/Modes 是不同的机制) | https://forum.cursor.com/t/custom-modes-missing-in-cursor-2-1-0 |
| 5 | `.cursor/rules/*/RULE.md` 是"趋势" | 恰恰相反，该格式被官方描述但未实际实现，`.mdc` 才是唯一工作的格式。论坛有大量 bug 报告 | https://forum.cursor.com/t/project-rules-documented-rule-md-folder-format-not-working-only-undocumented-mdc-format-works/145907 |
| 6 | 企业级 `/Library/Application Support/Cursor/rules/*.md` | 无证据支持。Cursor Enterprise 通过 Dashboard (Web UI) 管理规则 | — |
| 7 | `.cursor/rules/.cursorrules` | `.cursorrules` 应仅在项目根目录，不应在 `.cursor/rules/` 下 | — |

#### ⚠️ 需修正

| # | 声明 | 说明 |
|---|------|------|
| 8 | 编号前缀控制优先级 (001-base.mdc) | 这是**社区约定**，非官方功能。官方行为是 "later filenames override earlier ones" |
| 9 | "Agent Mode 优先 0.43+" | 版本号极度过时 (当前已是 2.x 时代) |

**总体评价**: 大量错误 (62%)，混合了 Cursor、Windsurf 和其他工具的概念。

---

### design/06-github-copilot.md (GitHub Copilot)

#### ❌ 错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | Agent profile 含 `model: gpt-5` | 官方字段为 `name`, `description`, `prompt`, `tools`, `mcp-servers`，**无 `model` 字段** | https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-custom-agents |

#### ⚠️ 需修正/标注

| # | 声明 | 说明 |
|---|------|------|
| 2 | `~/.copilot/instructions/` | VS Code 支持用户级 instructions，但默认路径是 VS Code 用户数据目录，非 `~/.copilot/instructions/` |
| 3 | `~/.copilot/prompts/` | VS Code prompt files 的用户级路径在 VS Code 用户数据目录中，非 `~/.copilot/prompts/` |
| 4 | Hooks 路径 | 文档声明支持 Hooks (正确)，但未说明配置路径是 `.github/hooks/*.json` |
| 5 | "三层架构: Foundation→Specialists→Capabilities" | 这是文档作者的自行归纳，官方文档中不存在此术语体系 |

**总体评价**: 相对较好 (82/100)。

---

### design/07-windsurf-cascade.md (Windsurf)

#### ❌ 错误

| # | 声明 | 正确信息 | 来源 |
|---|------|---------|------|
| 1 | `.windsurf/rules/*.md` 字符限制 | 官方限制为 **12,000 字符/文件** (global_rules.md 为 6,000)。文档未明确区分 | https://docs.windsurf.com/windsurf/cascade/memories |

#### ⚠️ 需修正/标注

| # | 声明 | 说明 |
|---|------|------|
| 2 | Agent Command Center = "自定义 Agent" | 该功能是**管理已有 agents 的 Kanban 面板**，不是创建自定义 Agents 的机制。易产生歧义 |
| 3 | `memory-bank/` | **非 Windsurf 官方功能**，是社区持久化记忆方案，应明确标注 |
| 4 | 自动记忆子目录 `<workspace-hash>/` 及 JSON 文件名 | 官方确认记忆存储在 `~/.codeium/windsurf/memories/`，但未确认子目录结构和具体文件名 |

**总体评价**: 较好 (85/100)。

---

### design/08-generic-universal.md (通用层)

#### ❌ 已确认错误（有官方文档来源）

| # | 错误声明 | 正确信息 | 来源 |
|---|---------|---------|------|
| 1 | Cursor "Agent 定义" = "无" | Cursor 支持 Subagents (`.cursor/agents/*.md`) | https://cursor.com/docs/subagents |
| 2 | Cursor "钩子" = "无" | Cursor 支持 Hooks (`.cursor/hooks.json`) | https://cursor.com/docs/hooks |
| 3 | Cursor "计划/工作流" = "无" | Cursor 有 Plan 模式 | https://cursor.com/help/ai-features/agent |
| 4 | Windsurf "Agent 定义" = "无" | Windsurf 有 Agent Command Center (agent 会话管理) | https://docs.windsurf.com/windsurf/agent-command-center |
| 5 | Windsurf "钩子" = "无" | Windsurf 支持 Cascade Hooks (`.windsurf/hooks.json`) | Windsurf Changelog |
| 6 | Cursor `SKILL.md` = ❌ | Cursor 支持 `SKILL.md` (v2.4+) | https://cursor.com/changelog/2-4 |

#### 路径兼容性表 (表 3.1) 的问题

- Cursor 的 `.agents/skills/` 标为 ❌ — 实际上 Cursor 支持 Skills，但路径不同 (`.cursor/skills/`)。`.agents/skills/` 是 Codex/Kimi/OpenCode 的兼容路径。
- Windsurf 的 `.agents/skills/` 标为 ❌ — 同理，Windsurf 支持 Skills 但路径是 `.windsurf/skills/` 和 `~/.codeium/windsurf/skills/`。
- 大量 ❌ 可能应改为 ⚠️（不原生支持但可通过转换兼容）。

#### 转换映射表 (表 5.1/5.2) 的问题

- Cursor 的 "agents" 映射列为 "无" → 应映射到 `.cursor/agents/` (Subagents)
- Cursor 的 "hooks" 映射列为 "无" → 应映射到 `.cursor/hooks.json`
- Windsurf 的 "agents" 映射列为 "无" → Agent Command Center 不是自定义 Agent，但可标注为不同机制
- Windsurf 的 "hooks" 映射列为 "无" → 应映射到 `.windsurf/hooks.json`

---

### design/09-custom-agents-guide.md (Agent 实现指南)

#### ❌ 已确认错误

| # | 错误声明 | 正确信息 | 来源 |
|---|---------|---------|------|
| 1 | Cursor "❌ 不支持"自定义 Agent | Cursor 2.4+ 支持 Subagents (`.cursor/agents/*.md`)。虽然 2.1 移除了 Custom Modes，但 Subagents 是新的自定义 Agent 机制 | https://cursor.com/docs/subagents |
| 2 | Windsurf "❌ 不支持"自定义 Agent | Windsurf 有 Agent Command Center (多 agent 管理) 和 Skills。虽无 `agent/*.md` 机制，但不应简单标为"不支持" | https://docs.windsurf.com/windsurf/agent-command-center |
| 3 | Claude Code "没有原生自定义 Agent 系统" | Claude Code 官方支持 Subagents (`.claude/agents/*.md`) | https://code.claude.com/docs/en/sub-agents |
| 4 | Cursor "Cursor 只有一个 Agent" / "无 subagent" | Cursor 支持 Subagents，且 Agent 可以将任务委派给子代理 | https://cursor.com/help/ai-features/agent |

#### 需要澄清

- **Cursor**: 2.1 移除了 Custom Modes，2.4 引入了 Subagents。Subagents ≠ Custom Modes。文档需要区分这两者。
- **Windsurf**: Agent Command Center 是会话管理面板，不是 Agent 定义机制。Windsurf 没有类似 OpenCode `agent/*.md` 的原生自定义 Agent 文件格式，但有 Skills 和 Rules 可以实现类似效果。
- **Claude Code**: 支持 Subagents (`.claude/agents/*.md`)，这是官方功能，不是"社区方案"。

---

## 三、修正优先级

### 🔴 P0 — 立即修正（严重误导用户）

1. **所有文档的 Hooks 描述**: 将 `.py`/`.sh` 文件目录改为各工具实际的 JSON/config 配置机制
2. **design/05-cursor.md**: 删除 `~/.cursor/global_rules.md` 和 6000 字符限制（这是 Windsurf 的）
3. **design/05-cursor.md**: 修正 `.cursor/rules/*/RULE.md` "趋势" 声明 → 明确说明不工作
4. **design/08 表 1.2**: 修正 Cursor 和 Windsurf 的 "无" 声明（Agent/Hooks/Plan/Skills）
5. **design/09 总览表**: 修正 Cursor 和 Windsurf 的 "❌ 不支持" 为正确的支持状态

### 🟡 P1 — 尽快修正（信息错误）

6. **design/01-claude-code.md**: 修正 Auto Memory 文件格式 `.json` → `.md`
7. **design/04-opencode.md**: 修正目录名称 `agent/`→`agents/`, `command/`→`commands/`
8. **design/04-opencode.md**: 修正 `opencode.json` 配置结构 (`skills.permissions` → `permission.skill`)
9. **design/05-cursor.md**: 修正 `~/.cursor/settings.json` 路径
10. **design/06-github-copilot.md**: 删除虚构的 `model: gpt-5` 字段
11. **design/07-windsurf-cascade.md**: 修正 workspace rules 限制为 12,000 字符

### 🟢 P2 — 补充标注（不够严谨）

12. **所有文档**: 对社区约定（如编号前缀、`0-category.json`、`memory-bank/`）明确标注来源
13. **design/01-claude-code.md**: 补充 Managed Policy 层
14. **design/01-claude-code.md**: 修正注意力预算表述
15. **design/07-windsurf-cascade.md**: 标注 `memory-bank/` 为社区方案

---

## 四、根因分析

1. **以偏概全**: 将 Claude Code 的 `.claude/hooks/` 目录模式套用到所有工具，未查各工具实际配置方式
2. **混淆工具**: design/05-cursor.md 将 Windsurf 的 `global_rules.md` 和 6000 字符限制错误归属给 Cursor
3. **猜测代替查证**: `.cursor/rules/*/RULE.md` "趋势"、编号前缀控制优先级、6000 字符限制等均为猜测
4. **版本信息过时**: Cursor "0.43+" 版本号过时，未跟踪最新版本功能变化
5. **虚构字段**: GitHub Copilot 的 `model: gpt-5` 为凭空捏造
6. **社区约定未标注**: `0-category.json`、`memory-bank/`、编号前缀等未说明来源

---

*报告完成。所有 9 个 design 文档已由 4 个并行 subagent 完成深度审计。*
