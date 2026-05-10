# OpenCode 项目模板

## 快速开始

1. 将本目录内容复制到你的项目根目录
2. 编辑 `AGENTS.md` 添加项目特定指令
3. 编辑 `.opencode/agents/*.md` 定义自定义 Agent
4. 编辑 `opencode.json` 配置权限和模型

## 目录说明

```
.
├── AGENTS.md                  # 项目级指令（OpenCode 自动读取）
├── opencode.json              # 主配置文件
├── .opencode/                 # OpenCode 生态目录
│   ├── agents/                # Agent 定义（Markdown + YAML frontmatter）
│   └── skills/                # Skills（SKILL.md 格式）
└── .agents/                   # 通用兼容层
    ├── agents/                # 通用 Agent 定义
    ├── skills/                # 通用 Skills
    ├── rules/                 # 规则文件
    ├── context/               # 上下文/领域知识
    ├── hooks/                 # 生命周期钩子（如支持）
    ├── plans/                 # 计划模板
    ├── prompts/               # 提示词变体
    └── memory/                # 记忆文件
```

## 关键文件

### AGENTS.md
OpenCode 会自动发现从当前目录向上到 git worktree 根目录的 `AGENTS.md`、`CLAUDE.md`、`CONTEXT.md` 文件。

### opencode.json
```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["docs/guidelines.md"],
  "permission": {
    "edit": "ask",
    "bash": "ask"
  },
  "agent": {
    "planner": {
      "mode": "primary",
      "description": "Architecture planning specialist",
      "permission": {
        "edit": "deny"
      }
    }
  }
}
```

### Agent 定义 (.opencode/agents/*.md)
文件名即 agent 名称，frontmatter 支持：
- `description` (required)
- `mode`: `primary` | `subagent` | `all`
- `model`: `provider/model-id`
- `temperature`: 0.0 - 1.0
- `permission`: 权限对象（`ask` | `allow` | `deny`）
- `steps`: 最大迭代步数
- `hidden`: 是否隐藏于 @ 自动补全

⚠️ `tools` 字段已废弃，请使用 `permission`。

## 更多参考

- [OpenCode 官方文档](https://opencode.ai/docs/)
- [Agent 配置](https://opencode.ai/docs/agents/)
- [Config 配置](https://opencode.ai/docs/config/)
- [Skills 系统](https://opencode.ai/docs/skills/)
- [Commands 系统](https://opencode.ai/docs/commands/)
