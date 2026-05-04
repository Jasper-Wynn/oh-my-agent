# Contributing to Oh My Agent

感谢你对 Oh My Agent 感兴趣！以下是参与贡献的指南。

## 如何贡献

### 1. 报告问题 (Issues)

发现设计文档中的错误？请提交 Issue 并包含：
- **工具名称**: 涉及哪个 AI 工具
- **错误描述**: 具体哪里不对
- **官方来源**: 请附上官方文档链接（我们要求每条声明都有来源）
- **建议修正**: 如果有的话

### 2. 提交改进 (Pull Requests)

- **Fork** 本仓库
- 在 **feature branch** 上修改：`git checkout -b fix/cursor-hooks`
- **保持最小改动**: 每个 PR 只解决一个问题
- **更新设计文档**: 如果修改了 `temp/` 模板，请同步更新 `design/` 中对应的设计规范
- **验证来源**: 所有工具能力声明必须基于官方文档，禁止猜测

### 3. 内容规范

#### 设计文档 (`design/`)
- 使用 Markdown 格式
- 表格对齐，易于阅读
- 路径声明必须标注来源（官方文档链接）
- 不确定的信息标注 `⚠️ 未确认` 而非猜测

#### 脚手架模板 (`temp/`)
- 每个工具目录包含 `.agents/`（通用层）和 `.<tool>/`（原生层）
- `.agents/` 中的文件是**工具无关的开放标准**
- `.<tool>/` 中的文件是**该工具的原生格式**
- 保持示例简洁，避免过度复杂

### 4. 审计标准

我们要求所有工具能力声明必须经过官方文档验证：

| 工具 | 官方文档 |
|------|---------|
| Claude Code | https://code.claude.com/docs |
| Cursor | https://cursor.com/docs |
| Kimi | https://moonshotai.github.io/kimi-cli |
| Codex | https://developers.openai.com/codex |
| Copilot | https://docs.github.com/en/copilot |
| Windsurf | https://docs.windsurf.com |
| OpenCode | https://opencode.ai/docs |

### 5. 代码风格

- Markdown 文件使用标准语法
- 代码示例优先使用相对路径，避免绝对路径
- 不要包含个人信息（用户名、邮箱、本地路径等）
- 使用 `#!/usr/bin/env python3` 作为 shebang（如果需要可执行脚本）

## 开发流程

```bash
# 1. Fork 并 clone
git clone https://github.com/YOUR-NAME/oh-my-agent.git
cd oh-my-agent

# 2. 创建分支
git checkout -b feature/new-skill-template

# 3. 修改并提交
git add .
git commit -m "feat: add testing skill template for Cursor"

# 4. 推送到你的 fork
git push origin feature/new-skill-template

# 5. 提交 Pull Request
```

## 社区

- 通过 GitHub Issues 讨论设计决策
- 重大改动建议先开 Issue 讨论，再提交 PR

再次感谢你的贡献！
