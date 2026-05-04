# Code Review

> **作用**: 代码审查工作流
> **工具**: Claude Code
> **原生路径**: `.claude/skills/code-review/SKILL.md`

## 说明

Claude Code 原生支持 **Agent Skills** 开放标准。Skills 是模块化的能力扩展，通过 `SKILL.md` 文件定义，可被 Claude 自动触发或通过 `/skill-name` 调用。

Skills 使用**渐进式加载**：
- **Level 1**: YAML frontmatter (name, description) 在启动时加载 (~100 tokens)
- **Level 2**: SKILL.md 主体内容在触发时加载 (<5k tokens)
- **Level 3+**: 附加资源文件按需加载

## 格式说明

```markdown
---
name: code-reviewing
description: |
  Perform thorough code reviews focusing on correctness,
  maintainability, and security. Use when asked to review
  code or pull requests.
---

# Code Review Skill

## Checklist
- [ ] Logic correctness
- [ ] Error handling
- [ ] Test coverage
- [ ] Security considerations
- [ ] Performance implications

## Process
1. Read the changed files
2. Understand the context and intent
3. Check for edge cases
4. Verify test coverage
5. Provide actionable feedback
```

## 目录结构

```
.claude/skills/
└── code-review/
    ├── SKILL.md          # 主指令文件
    ├── checklist.md      # 可选：详细检查清单
    └── examples/         # 可选：示例和参考
        └── good-pr.md
```

## 来源

- [Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview](https://docs.anthropic.com/en/agents-and-tools/agent-skills/overview)
- [Skill Authoring Best Practices](https://docs.anthropic.com/en/agents-and-tools/agent-skills/best-practices)
