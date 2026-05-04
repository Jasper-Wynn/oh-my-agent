# 自定义 Agent 定义 (Subagents)

> **作用**: 定义子代理 (Subagent) 的行为和工具集
> **工具**: Claude Code
> **原生路径**: `.claude/agents/*.md`

## 说明

Claude Code 支持通过 `.claude/agents/*.md` 文件定义**子代理 (Subagents)**。子代理是运行在独立工作目录中的 Claude 实例，拥有自己的提示词和工具集，用于隔离处理特定任务。

子代理与父会话的关系：
- 运行在独立的工作目录（git worktree）中
- 拥有独立的上下文窗口
- 通过 `Task` 工具委派任务
- 可以配置持久化记忆 (`agent-memory/<name>/`)

## 格式说明

纯 Markdown 文件，定义子代理的系统提示词：

```markdown
# Explorer Agent

You are a codebase exploration specialist. Your job is to:
1. Read and understand the codebase structure
2. Find relevant files for a given task
3. Report back with file paths and brief summaries

## Tools
- Use ReadFile, Glob, Grep for exploration
- Do NOT write files or execute commands
- Keep responses concise
```

## 来源

- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
