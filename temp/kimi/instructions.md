# 项目指令 (AGENTS.md)

> **作用**: Kimi Code CLI 项目级主指令文件
> **工具**: Kimi Code CLI
> **文件名**: `AGENTS.md` (项目级 / 子目录级)

## 影响范围

- **作用域**: 所在目录及其整个子树
- **加载时机**: 会话开始时自动注入开发者消息
- **优先级**: 子目录 AGENTS.md > 父目录 AGENTS.md > 全局配置
- **冲突解决**: 更深层嵌套的 AGENTS.md 优先

## 格式说明

纯 Markdown，**无 YAML Frontmatter**：

```markdown
## Architecture Overview
- CLI entry: src/kimi_cli/cli/__init__.py
- Core loop: src/kimi_cli/soul/kimisoul.py

## Conventions
- Python >= 3.12; line length 100
- Ruff handles lint + format
- Tests use pytest + pytest-asyncio

## Git Commit
Conventional Commits: type(scope): subject
```

## 特殊变量

Kimi 通过模板变量注入系统信息：
- `${KIMI_AGENTS_MD}` — 所有适用的 AGENTS.md 内容
- `${KIMI_SKILLS}` — 可用 Skills 列表
- `${KIMI_WORK_DIR}` — 工作目录
- `${KIMI_OS}` — 操作系统
