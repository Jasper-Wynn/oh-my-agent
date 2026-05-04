# 自定义 Agent 定义

> **状态**: ⚠️ Codex 原生不支持独立的 Agent 定义文件
> **来源**: [Codex GitHub Repository](https://github.com/openai/codex)

## 说明

根据 Codex 仓库结构分析（`.codex/` 目录仅包含 `environments/` 和 `skills/`，无 `agents/` 目录），Codex 没有原生的独立 Agent 定义文件机制。

此目录在统一层中保留用于：
1. **跨工具转换** — 转换为其他支持 Agent 定义的工具格式
2. **未来兼容** — 如果 Codex 后续支持，可直接使用

## Codex 的替代方案

Codex 通过以下方式实现类似功能：
- **AGENTS.md**: 项目级主指令文件
- **Skills**: `.codex/skills/<name>/SKILL.md` 封装工作流
- **Plan Mode**: `/plan` 命令进行任务规划

## 来源

- [Codex GitHub Repository - .codex directory](https://github.com/openai/codex/tree/main/.codex)
