# System Prompt / Output Styles

> **作用**: 自定义系统提示词片段
> **工具**: Claude Code
> **原生路径**: `.claude/output-styles/*.md`

## 说明

Claude Code 支持通过 `.claude/output-styles/*.md` 文件自定义系统提示词的特定部分。这相当于为 Claude 的输出风格提供附加指令。

与 CLAUDE.md 的区别：
- `CLAUDE.md` 加载到每次会话的系统提示词中
- `output-styles/*.md` 用于定义特定的输出格式或风格模式

## 格式说明

纯 Markdown 文件：

```markdown
# Explanatory Style

When explaining code changes:
1. Start with the "why" before the "what"
2. Use analogies for complex concepts
3. Include before/after comparisons
4. Link to relevant documentation
```

## 激活方式

Output styles 需要通过 `settings.json` 中的 `outputStyle` 字段激活：

```json
{
  "outputStyle": "Explanatory"
}
```

## 来源

- [Output Styles](https://code.claude.com/docs/en/output-styles)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
