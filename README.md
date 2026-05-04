# Oh My Agent 🎯

> **Unified AI Agent Project Scaffold** — One directory structure, all major AI tools.

[中文文档](./README.zh-CN.md)

---

## Why?

Every AI coding tool has its own configuration format:
- Claude Code uses `CLAUDE.md` + `.claude/skills/`
- Cursor uses `.cursorrules` + `.cursor/rules/*.mdc`
- Kimi uses `AGENTS.md` + `.kimi/agents/`
- Codex uses `AGENTS.md` + `.codex/`
- Copilot uses `.github/copilot-instructions.md`
- Windsurf uses `.windsurfrules` + `.windsurf/rules/`
- OpenCode uses `AGENTS.md` + `.opencode/`

**Managing 7 different formats is painful.** Oh My Agent introduces a **two-layer architecture**:

```
.agents/          ← Universal layer (write once)
  ├── skills/     ← Cross-tool skills
  ├── agents/     ← Agent definitions
  ├── rules/      ← Shared rules
  ├── hooks/      ← Lifecycle hooks
  ├── prompts/    ← Prompt templates
  └── context/    ← Shared context

.<tool>/          ← Native layer (auto-generated)
  └── (tool-specific formats)
```

## Quick Start

1. **Copy the scaffold** for your primary tool:
   ```bash
   # For Claude Code
   cp -r temp/claude-code/.agents ./my-project/
   cp -r temp/claude-code/.claude ./my-project/
   ```

2. **Customize** the universal layer in `.agents/`:
   - Edit `.agents/skills/code-review/SKILL.md`
   - Add your rules in `.agents/rules/`
   - Define agents in `.agents/agents/`

3. **Sync** to native layers (manual or via your own scripts):
   - `.agents/skills/` → `.claude/skills/`, `.cursor/skills/`, etc.
   - `AGENTS.md` → root project file

## Repository Structure

```
oh-my-agent/
├── design/                    # Design specifications (9 docs)
│   ├── 01-claude-code.md
│   ├── 02-codex.md
│   ├── 03-kimi.md
│   ├── 04-opencode.md
│   ├── 05-cursor.md
│   ├── 06-github-copilot.md
│   ├── 07-windsurf-cascade.md
│   ├── 08-generic-universal.md   # Cross-tool compatibility design
│   └── 09-custom-agents-guide.md # Custom agent implementation guide
│
├── temp/                      # Scaffold templates (8 tools)
│   ├── claude-code/
│   ├── codex/
│   ├── cursor/
│   ├── generic-universal/
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

## Design Principles

1. **Maximum Common Divisor**: `AGENTS.md` + `.agents/skills/` + `.agents/agents/` + `.agents/hooks/` + `.agents/prompts/` + `.agents/context/`
2. **Write Once, Use Everywhere**: Define in `.agents/`, convert to native formats
3. **Tool-Agnostic**: No vendor lock-in; migrate between tools seamlessly
4. **Future-Proof**: Based on converging industry standards (YAML Frontmatter, Skill specs, Memory banks)

## Supported Features Matrix

| Tool | Main Config | Skills | Agents | Hooks | Prompts | Plan Mode |
|------|-------------|--------|--------|-------|---------|-----------|
| Claude Code | `CLAUDE.md` | ✅ | ✅ (Subagents) | ✅ | ✅ | ✅ |
| Cursor | `.cursorrules`/`.mdc` | ✅ | ✅ (Subagents) | ✅ | ✅ | ✅ |
| Kimi | `AGENTS.md` | ✅ | ✅ (agent.yaml) | ✅ | ✅ | ✅ |
| Codex | `AGENTS.md` | ✅ | ⚠️ (Profiles) | ✅ | ⚠️ | ❌ |
| Copilot | `copilot-instructions.md` | ✅ | ✅ | ✅ | ✅ | ❌ |
| Windsurf | `.windsurfrules`/`.md` | ✅ | ⚠️ (ACC) | ✅ | ⚠️ | ❌ |
| OpenCode | `AGENTS.md` | ✅ | ✅ | ✅ | ✅ | ❌ |

> All claims are verified against official documentation. See [AUDIT_REPORT.md](./AUDIT_REPORT.md) for details.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[MIT](./LICENSE)
