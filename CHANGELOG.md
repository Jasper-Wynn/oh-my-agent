# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Oh My Agent project scaffold
- Design specifications for 7 major AI tools (Claude Code, Cursor, Kimi, Codex, Copilot, Windsurf, OpenCode)
- Cross-tool universal compatibility layer design (`design/08-generic-universal.md`)
- Custom agent implementation guide (`design/09-custom-agents-guide.md`)
- Scaffold templates for all 7 tools in `temp/`
- Two-layer architecture: `.agents/` (universal) + `.<tool>/` (native)
- Official documentation audit report (`AUDIT_REPORT.md`)

### Fixed
- Corrected hooks mechanism descriptions across multiple design docs
- Fixed Cursor design: removed Windsurf concepts (global_rules.md, 6000 char limit)
- Fixed OpenCode config structure (`permission.skill`, `agents` pluralization)
- Removed fictional `model: gpt-5` field from Copilot examples
- Updated Cursor/Windsurf agent support status in comparison tables
- Fixed Claude Code memory format (`.md` not `.json`)
- Added disclaimers for unconfirmed/unimplemented features
